#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mod API v2 验证脚本 | Mod API v2 verification script.

纯 Python 实现，不依赖 Ren'Py 运行时 | Pure Python, no Ren'Py runtime needed.
两种验证方式 | Two verification strategies:
  1. 静态断言 | Static assertions:
     - mod_api_v2.rpy 定义了全部 19 个 HOOK_* 常量且取值唯一
       (All 19 HOOK_* constants are defined with unique values)
     - register_mod / unregister_mod / register_hook / execute_hook /
       cancel_hook / set_mod_enabled / is_mod_enabled / apply_startup_states /
       list_registered_mods / missing_dependencies 关键方法存在
       (key methods exist)
     - mod_api.rpy（v1 基类，被 ModAPIV2 继承）定义了 register_trait /
       register_perk / register_event / register_quality / register_game_mode
       (v1 base wrappers the v2 class inherits exist)
     - CAPABILITIES 集合包含 "items"（物品品质档位注册）
       (CAPABILITIES includes "items")
     - mod_template.rpy 引用的每个 api.HOOK_* 都真实存在
       (every api.HOOK_* referenced by the template exists)
     - 模板 Ren'Py 语法由项目 lint 保证（模板位于 game/ 目录内）
       (template syntax is covered by project lint; it lives under game/)
  2. 动态模拟 | Simulated execution:
     - 在桩 (stub) 环境下 exec ModAPIV2 类定义，真实执行
       注册 -> 触发 -> 取消 全流程，以及持久化启用/禁用、
       always_on、dependencies 前置解析、禁用 Mod 钩子跳过
       (exec the ModAPIV2 class with stubbed globals and run the full
       register -> fire -> cancel flow, plus persistent enable/disable,
       always_on, dependency resolution and inactive-mod hook skipping)

用法 | Usage: python tools/verify_mod_api.py
退出码 | Exit code: 0 = 全部通过 (all checks passed), 1 = 存在失败 (failures)
"""

import collections
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API_FILE = ROOT / "game" / "core" / "systems" / "mods" / "mod_api_v2.rpy"
BASE_API_FILE = ROOT / "game" / "core" / "systems" / "mods" / "mod_api.rpy"
TEMPLATE_FILE = ROOT / "game" / "core" / "templates" / "mod_template" / "mod_template.rpy"
GAME_DIR = ROOT / "game"

# EN: The progress doc says 15 hook points; the code now defines 19
#     HOOK_* constants (16 original + 2 girl-destination hooks added with
#     the Courtyard mod extraction + item_generated added with the
#     Item Quality mod extraction) — the code is the source of truth here.
# ZH: 进度文档写 15 个钩子点；代码现定义 19 个 HOOK_* 常量
#     （原有 16 个 + 庭院 Mod 剥离时新增的 2 个目的地钩子 + 物品品质 Mod
#     剥离时新增的 item_generated），此处以代码为准。
EXPECTED_HOOK_COUNT = 19

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"

_failures = []
_warnings = []


def check(ok, label):
    """记录一条检查结果 | Record one check result."""
    print("  [%s] %s" % (PASS if ok else FAIL, label))
    if not ok:
        _failures.append(label)
    return ok


def warn(label):
    """记录一条警告（不失败）| Record a warning (non-fatal)."""
    print("  [%s] %s" % (WARN, label))
    _warnings.append(label)


# ─────────────────────────────────────────────
# 1. 静态检查 | Static checks
# ─────────────────────────────────────────────

def extract_init_block(path):
    """取出 rpy 文件中第一个 `init <n> python:` 块并去缩进。

    Extract and dedent the first `init <n> python:` block. Stops at the next
    top-level `init` statement (the file may contain several init blocks).
    """
    src = path.read_text(encoding="utf-8")
    m = re.search(r"^init\s+-?\d+\s+python:\s*\n((?:(?!^init\s)[^\n]*\n?)*)",
                  src, re.M | re.S)
    if not m:
        raise RuntimeError("no init python block found in %s" % path)
    return textwrap.dedent(m.group(1))


def static_checks():
    print("\n== 1. Static checks | 静态检查 ==")

    src = API_FILE.read_text(encoding="utf-8")

    # 1a. HOOK_* 常量 | HOOK_* constants
    hooks = re.findall(r'^\s+HOOK_(\w+)\s*=\s*"([^"]+)"', src, re.M)
    check(len(hooks) == EXPECTED_HOOK_COUNT,
          "HOOK_* constants defined: %d/%d" % (len(hooks), EXPECTED_HOOK_COUNT))
    values = [v for _name, v in hooks]
    check(len(set(values)) == len(values), "HOOK_* values are unique | 钩子取值唯一")

    # 命名约定 <domain>_<动词分词> | naming convention (see the file's own
    # examples: girl_generated, day_starting — the "<domain>_<action>_<tense>"
    # comment in mod_api_v2.rpy is aspirational, the values are 2-part)
    convention = re.compile(r"^[a-z]+_[a-z]+(ing|ed)$")
    for name, value in hooks:
        if not convention.match(value):
            warn("HOOK_%s = '%s' does not match <domain>_<action>_<tense>"
                 % (name, value))

    # 1b. 关键方法 | Key methods
    for method in ("register_mod", "unregister_mod", "register_hook",
                   "execute_hook", "cancel_hook", "set_mod_enabled",
                   "is_mod_enabled", "apply_startup_states",
                   "list_registered_mods", "missing_dependencies"):
        check(re.search(r"def %s\(self" % method, src) is not None,
              "ModAPIV2.%s exists" % method)

    # 1c. 模板引用的钩子常量都存在 | Template hook references exist
    tpl = TEMPLATE_FILE.read_text(encoding="utf-8")
    defined = {"HOOK_" + n for n, _v in hooks}
    referenced = set(re.findall(r"api\.(HOOK_\w+)", tpl))
    check(referenced <= defined,
          "template api.HOOK_* references all defined: %s"
          % (sorted(referenced) or "(none)"))
    check('ModAPIV2.instance()' in tpl and "register_mod" in tpl,
          "template uses register_mod + ModAPIV2.instance()")
    check(re.search(r'"api_version":\s*2', tpl) is not None,
          'template manifest declares "api_version": 2')

    # 1e. v1 基类的注册包装（v2 继承）| v1 base registration wrappers
    #     register_quality 等定义在 mod_api.rpy，ModAPIV2 继承它们。
    base_src = BASE_API_FILE.read_text(encoding="utf-8")
    for method in ("register_trait", "register_perk", "register_event",
                   "register_quality", "register_game_mode"):
        check(re.search(r"def %s\(self" % method, base_src) is not None,
              "ModAPI.%s exists" % method)

    # 1f. 能力标志 | capability flags
    caps = re.search(r"CAPABILITIES\s*=\s*\{(.*?)\}", src, re.S)
    check(caps is not None and '"items"' in caps.group(1),
          'CAPABILITIES includes "items" (item quality tiers)')

    # 1d. 游戏内触发点接线情况 | In-game hook wiring (informational)
    wired = []
    for rpy in GAME_DIR.rglob("*.rpy"):
        if rpy == API_FILE:
            continue
        for m in re.finditer(r"\b(mod_api_v2|api)\.(execute_hook|cancel_hook)\(",
                             rpy.read_text(encoding="utf-8", errors="replace")):
            wired.append("%s: %s.%s" % (rpy.relative_to(ROOT), m.group(1), m.group(2)))
    if wired:
        print("  [INFO] in-game hook call sites | 游戏内钩子调用点: %s" % wired)
    else:
        warn("no in-game execute_hook/cancel_hook call sites found outside "
             "mod_api_v2.rpy (hooks are defined but never fired by game code)")


# ─────────────────────────────────────────────
# 2. 动态模拟 | Simulated execution
# ─────────────────────────────────────────────

class _StubRenpy(object):
    """renpy 模块桩 | renpy module stub."""

    class config(object):
        developer = False  # EN: keep notify silent | ZH: 保持 notify 静默

    notifications = []

    @classmethod
    def notify(cls, msg):
        cls.notifications.append(msg)

    @classmethod
    def log(cls, msg):
        pass


class _StubServices(object):
    """services 容器桩 | services container stub."""

    registered = {}

    @classmethod
    def register(cls, key, value):
        cls.registered[key] = value


class _StubPersistent(object):
    """persistent 桩：普通对象，支持 getattr/setattr | Plain stub object."""


class ModAPI(object):
    """ModAPI v1 基类桩 | ModAPI v1 base class stub."""

    def __init__(self):
        pass


def load_api_class():
    """从 rpy 提取 ModAPIV2 类并在桩环境中执行 | Exec ModAPIV2 with stubs."""
    block = extract_init_block(API_FILE)
    # 去掉单例注册尾部（依赖真实 services）| Drop the singleton tail
    block = block.split("# ── Singleton ──")[0]
    env = {
        "ModAPI": ModAPI,
        "defaultdict": collections.defaultdict,
        "renpy": _StubRenpy,
        "services": _StubServices,
        "persistent": _StubPersistent(),
    }
    exec(block, env)
    return env["ModAPIV2"]


def simulated_checks():
    print("\n== 2. Simulated execution | 动态模拟 ==")
    ModAPIV2 = load_api_class()
    api = ModAPIV2()

    # 2a. register_mod: 合法清单 | valid manifest
    manifest = {
        "name": "Verify Mod", "version": "1.0.0", "api_version": 2,
        "min_game_version": "0.3.0", "author": "verify_mod_api",
        "description": "verification", "requires": ["events"],
        "dependencies": [],
        "hooks": {},
    }
    api.register_mod("verify_mod", manifest)
    check(api.is_mod_active("verify_mod"), "register_mod activates mod | 注册后 mod 激活")

    # 2b. register_mod: 非法 api_version | invalid api_version
    try:
        api.register_mod("bad_ver", {"api_version": 1})
        check(False, "register_mod rejects api_version != 2")
    except ValueError:
        check(True, "register_mod rejects api_version != 2")

    # 2c. register_mod: 未知能力 | unknown capability
    try:
        api.register_mod("bad_cap", {"api_version": 2, "requires": ["not_a_capability"]})
        check(False, "register_mod rejects unknown capability")
    except ValueError:
        check(True, "register_mod rejects unknown capability")

    # 2d. register_hook + execute_hook: 触发并回传结果 | fire and collect
    fired = []

    def hook_a(context):
        fired.append("a")
        return "ok-a"

    def hook_b(context):
        fired.append("b")
        return None  # EN: None results are filtered out | ZH: None 结果会被过滤

    api.register_hook("verify_hook", hook_a, priority=0)
    api.register_hook("verify_hook", hook_b, priority=5)
    results = api.execute_hook("verify_hook")
    check(fired == ["b", "a"], "execute_hook runs high priority first | 高优先级先执行")
    check(results == {"_direct": "ok-a"},
          "execute_hook returns {mod_id: result}, None filtered | 返回字典且过滤 None")

    # 2e. execute_hook: 异常被吞掉不崩溃 | exceptions are swallowed
    def hook_bad(context):
        raise RuntimeError("boom")

    api.register_hook("verify_bad_hook", hook_bad)
    _StubRenpy.config.developer = True
    try:
        res = api.execute_hook("verify_bad_hook")
        check(res == {} and _StubRenpy.notifications,
              "execute_hook swallows hook exceptions and notifies")
    finally:
        _StubRenpy.config.developer = False

    # 2f. cancel_hook: 取消信号回归守卫 | cancellation regression guard
    def cancel_cb(context):
        context["cancel"] = True

    api.register_hook("verify_cancel", cancel_cb)
    check(api.cancel_hook("verify_cancel") is True,
          "cancel_hook returns True when a hook sets context['cancel']")
    check(api.cancel_hook("verify_hook") is False,
          "cancel_hook returns False when nobody cancels | 无人取消时返回 False")

    # 2g. unregister_mod: 状态清理 | state cleanup
    api.register_hook("verify_lifecycle", cancel_cb)
    api.unregister_mod("verify_mod")
    check(not api.is_mod_active("verify_mod"), "unregister_mod deactivates mod")
    check(all(mid != "verify_mod" for lst in api._mod_hooks.values()
              for mid, _cb, _p in lst),
          "unregister_mod removes the mod's hooks | 注销时清理其钩子")

    # 2h. 重复注册被拒绝 | duplicate registration rejected
    api.register_mod("verify_mod", manifest)
    try:
        api.register_mod("verify_mod", manifest)
        check(False, "register_mod rejects duplicate mod_id")
    except ValueError:
        check(True, "register_mod rejects duplicate mod_id")
    api.unregister_mod("verify_mod")

    # 2i. UI 集成: 主页菜单按钮 + mod 信息 | UI integration: menu buttons + info
    ui_manifest = dict(manifest)
    ui_manifest["home_rightmenu_add_buttons"] = ["verify_button_screen"]
    api.register_mod("verify_ui_mod", ui_manifest)
    check(("verify_ui_mod", "Verify Mod", ["verify_button_screen"]) in api.get_menu_buttons(),
          "get_menu_buttons returns declared button screens | 菜单按钮清单正确")
    info = api.get_mod_info("verify_ui_mod")
    check(info is not None and info.get("version") == "1.0.0",
          "get_mod_info returns manifest copy | mod 信息返回 manifest 副本")
    check(api.get_mod_info("no_such_mod") is None,
          "get_mod_info returns None for unknown mod | 未知 mod 返回 None")
    api.unregister_mod("verify_ui_mod")
    check(api.get_menu_buttons() == [],
          "get_menu_buttons empty after unregister | 注销后按钮清单清空")

    # 2j. 持久化启用/禁用 | persistent enable/disable
    toggle_manifest = dict(manifest)
    toggle_manifest["hooks"] = {"verify_toggle_hook": lambda ctx: "toggle-ok"}
    api.register_mod("verify_toggle", toggle_manifest)
    check(api.is_mod_enabled("verify_toggle"),
          "unrecorded mod defaults to enabled | 未记录的 mod 默认启用")
    api.set_mod_enabled("verify_toggle", False)
    check(not api.is_mod_active("verify_toggle"),
          "set_mod_enabled(False) deactivates in memory | 禁用后立即失活")
    check(not api.is_mod_enabled("verify_toggle"),
          "is_mod_enabled reflects the persistent flag | 开关反映持久化标志")
    check(api.execute_hook("verify_toggle_hook") == {},
          "execute_hook skips callbacks of a disabled mod | 禁用 Mod 的钩子被跳过")
    api.set_mod_enabled("verify_toggle", True)
    check(api.is_mod_active("verify_toggle"),
          "set_mod_enabled(True) re-activates in memory | 启用后立即复活")
    check(api.execute_hook("verify_toggle_hook") == {"verify_toggle": "toggle-ok"},
          "execute_hook fires again once re-enabled | 复活后钩子恢复触发")
    try:
        api.set_mod_enabled("no_such_mod", False)
        check(False, "set_mod_enabled rejects unknown mod_id")
    except ValueError:
        check(True, "set_mod_enabled rejects unknown mod_id")

    # 2k. dependencies 前置解析 | dependency resolution
    dep_manifest = dict(manifest)
    dep_manifest["always_on"] = True
    api.register_mod("verify_dep", dep_manifest)
    child_manifest = dict(manifest)
    child_manifest["dependencies"] = ["verify_dep", "verify_missing"]
    api.register_mod("verify_child", child_manifest)
    check(not api.is_mod_active("verify_child"),
          "mod with an uninstalled dependency stays inactive | 依赖未安装则不激活")
    check(api.missing_dependencies("verify_child") == ["verify_missing"],
          "missing_dependencies reports only inactive deps | 仅报告未激活的依赖")
    check(api.missing_dependencies("no_such_mod") == [],
          "missing_dependencies empty for unknown mod | 未知 mod 无缺失")

    api.set_mod_enabled("verify_dep", False)
    check(api.is_mod_active("verify_dep"),
          "always_on mod stays active when disabled | always_on 禁用无效")
    check(api.is_mod_enabled("verify_dep") is False,
          "set_mod_enabled still records the flag for always_on mods | 开关仍被记录")

    child2_manifest = dict(manifest)
    child2_manifest["dependencies"] = ["verify_dep"]
    api.register_mod("verify_child2", child2_manifest)
    check(api.is_mod_active("verify_child2"),
          "mod activates when its dependency is active | 依赖激活则随之激活")
    check(api.list_registered_mods() == ["verify_toggle", "verify_dep",
                                         "verify_child", "verify_child2"],
          "list_registered_mods returns every registered mod | 返回全部已注册")
    api.set_mod_enabled("verify_dep", True)

    # 2l. apply_startup_states 幂等 | idempotent startup re-sync
    api.set_mod_enabled("verify_child2", False)
    check(not api.is_mod_active("verify_child2"),
          "child2 disabled before startup sync | 同步前 child2 已禁用")
    api.apply_startup_states()
    check(not api.is_mod_active("verify_child2"),
          "apply_startup_states keeps persistent state | 幂等重建保持持久化状态")
    api.apply_startup_states()
    check(not api.is_mod_active("verify_child2"),
          "apply_startup_states is idempotent | 重复调用结果一致")

    # 2m. 清理 | cleanup
    for _mid in ("verify_toggle", "verify_dep", "verify_child", "verify_child2"):
        api.unregister_mod(_mid)
    check(api.list_registered_mods() == [],
          "unregister removes from the registry as well | 注销同时移出注册表")

    print("  [INFO] simulated flow register -> fire -> cancel all exercised | "
          "注册->触发->取消 全流程已 exercised")


def main():
    print("Mod API v2 verification | Mod API v2 验证")
    print("API file | 文件: %s" % API_FILE.relative_to(ROOT))

    static_checks()
    simulated_checks()

    print("\n== Summary | 汇总 ==")
    for w in _warnings:
        print("  [WARN] %s" % w)
    if _failures:
        print("  %d check(s) FAILED | 项检查失败:" % len(_failures))
        for f in _failures:
            print("    - %s" % f)
        return 1
    print("  All checks passed | 全部检查通过 (%d warning(s))." % len(_warnings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
