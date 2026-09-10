#### Test Runner — Lightweight test framework for Brothel King ####
# Phase 6.4: In-game test harness for component-level testing.
#
# Usage in a test file:
#   label test_girl_stats:
#       $ runner = TestRunner.instance()
#       $ runner.assert_eq(girl.get_stat("charm"), 50, "Initial charm")
#       $ runner.report()
#
# EN: Run all smoke tests from the main menu "Tests" button (developer mode
#     only), which starts label bk_test_runner.
# ZH: 通过主菜单 "Tests" 按钮（仅开发者模式显示）运行全部冒烟测试，
#     入口为 label bk_test_runner。

init -1 python:

    class TestRunner(object):
        """Lightweight test framework for game components."""

        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(TestRunner, cls).__new__(cls)
            return cls._instance

        @classmethod
        def instance(cls):
            return cls.__new__(cls)

        def __init__(self):
            if hasattr(self, '_initialized'):
                return
            self._initialized = True
            self.reset()

        def reset(self):
            self.passed = 0
            self.failed = 0
            self.skipped = 0
            self.results = []

        # ── Assertions ──

        def assert_eq(self, actual, expected, label=""):
            if actual == expected:
                self.passed += 1
                self.results.append(("PASS", label, "%s == %s" % (repr(actual), repr(expected))))
            else:
                self.failed += 1
                self.results.append(("FAIL", label, "Expected %s, got %s" % (repr(expected), repr(actual))))

        def assert_true(self, condition, label=""):
            self.assert_eq(bool(condition), True, label)

        def assert_contains(self, container, item, label=""):
            self.assert_eq(item in container, True, label or "%s in container" % repr(item))

        def assert_not_none(self, value, label=""):
            self.assert_eq(value is not None, True, label or "value is not None")

        def skip(self, label=""):
            # EN: Mark a test as skipped (e.g. it needs a running game instance).
            # ZH: 标记测试为跳过（例如需要游戏实例已创建）。
            self.skipped += 1
            self.results.append(("SKIP", label, "skipped"))

        # ── Reporting ──

        def report(self):
            lines = [
                "{b}Test Results:{/b}",
                "  {color=[c_emerald]}Passed: %s{/color}" % self.passed,
                "  {color=[c_red]}Failed: %s{/color}" % self.failed,
            ]
            if self.skipped:
                lines.append("  {color=[c_yellow]}Skipped: %s{/color}" % self.skipped)
            for status, label, detail in self.results:
                if status == "PASS":
                    color = c_emerald
                elif status == "SKIP":
                    color = c_yellow
                else:
                    color = c_red
                lines.append("  {color=[%s]}[%s]{/color} %s: %s" % (color, status, label, detail))
            return "\n".join(lines)

        def summary(self):
            return "%s passed, %s failed" % (self.passed, self.failed)

    test_runner = TestRunner()


# ─────────────────────────────────────────────
# Smoke tests | 冒烟测试
# EN: Component smoke tests using stub Girl objects (no real Girl instance,
#     no savegame needed). They can run from the main menu via the
#     developer-mode "Tests" button (label bk_test_runner).
# ZH: 使用桩 Girl 对象的组件冒烟测试（不需要真实 Girl 实例与存档）。
#     可通过主菜单开发者模式 "Tests" 按钮运行（入口 label bk_test_runner）。
# ─────────────────────────────────────────────

init -1 python:

    class _BKFakeStat(object):
        """最小 Stat 桩，接口与真实 Stat 对齐 | Minimal Stat stub matching the real Stat API"""

        def __init__(self, name, value=0):
            self.name = name
            self.value = value

        def change(self, chg, _max=250):
            # 与 Stat.change 相同的截断语义 | Same clamping semantics as Stat.change
            if self.value + chg < 0:
                r = -self.value
                self.value = 0
                return r
            elif self.value + chg > _max:
                r = _max - self.value
                self.value = _max
                return r
            else:
                self.value += chg
                return chg

        def set(self, val):
            self.value = val

    class _BKFakeGirl(object):
        """最小 Girl 桩，仅供组件冒烟测试 | Minimal Girl stub for component smoke tests

        EN: Implements only the surface the tested components touch:
            stats / sex_stats / find_stat / get_effect / is_ / rank /
            auto_upkeep / effect_dict. will_do_sex_act is controlled by
            the _will_do attribute for the economy test.
        ZH: 只实现被测组件会访问到的接口：stats / sex_stats / find_stat /
            get_effect / is_ / rank / auto_upkeep / effect_dict。
            will_do_sex_act 由 _will_do 属性控制，供经济组件测试用。
        """

        def __init__(self):
            self.stats = [
                _BKFakeStat("Beauty", 50), _BKFakeStat("Charm", 50),
                _BKFakeStat("Refinement", 40), _BKFakeStat("Sensitivity", 30),
                _BKFakeStat("Constitution", 30), _BKFakeStat("Body", 30),
                _BKFakeStat("Obedience", 30), _BKFakeStat("Libido", 30),
            ]
            self.sex_stats = [
                _BKFakeStat("Service", 20), _BKFakeStat("Sex", 20),
                _BKFakeStat("Anal", 10), _BKFakeStat("Fetish", 10),
            ]
            self.rank = 1
            self.level = 1
            self.sanity = 50
            self.broken = False
            self.effects = []
            self.effect_dict = defaultdict(list)
            self.auto_upkeep = False
            self._will_do = True

        def is_(self, s):
            return False

        def will_do_sex_act(self, act):
            return self._will_do

        def get_effect(self, type, target, **kwargs):
            # EN: Neutral stub — boosts are 1.0 (no-op multiplier), everything else 0.
            # ZH: 中性桩——boost 返回 1.0（无影响），其余返回 0。
            return 1.0 if type == "boost" else 0

        def find_stat(self, stat_name):
            for s in self.stats + self.sex_stats:
                if s.name.lower() == stat_name.lower():
                    return s
            return False

        def get_stat(self, stat_name, raw=False):
            # EN: Route through the real GirlStats component, like Girl does.
            # ZH: 与真实 Girl 一样经由 GirlStats 组件。
            return GirlStats(self).get_stat(stat_name, raw)


# ── GirlStats | 属性组件 ──

label test_girl_stats_component:
    # EN: GirlStats smoke tests on a stub girl.
    # ZH: 基于桩女孩的 GirlStats 冒烟测试。
    python:
        runner = TestRunner.instance()
        girl = _BKFakeGirl()
        stats = GirlStats(girl)

        runner.assert_eq(stats.get_stat("charm", raw=True), 50, "GirlStats.get_stat reads base value")
        # EN: Unknown stats return 0 (they do NOT raise — by design).
        # ZH: 未知属性返回 0（按设计不抛异常）。
        runner.assert_eq(stats.get_stat("no_such_stat", raw=True), 0, "GirlStats.get_stat unknown name returns 0")
        runner.assert_true(not stats.find_stat("no_such_stat"), "GirlStats.find_stat unknown name returns False")

        stats.set_stat("charm", 80)
        runner.assert_eq(girl.stats[1].value, 80, "GirlStats.set_stat forces value")

        # EN: change_stat on a regular stat. test_achievements is monkeypatched
        #     to a no-op: the real one pops the achievement notification screen,
        #     which needs full game state (not available from the main menu).
        # ZH: 对普通属性调用 change_stat。此处临时将 test_achievements
        #     替换为空操作：真实实现会弹出成就通知屏幕，依赖完整游戏状态
        #     （主菜单环境下不可用）。
        _orig_test_achievements = globals().get("test_achievements")
        globals()["test_achievements"] = lambda *a, **k: None
        try:
            r = stats.change_stat("charm", 10, apply_boost=False, spillover=False, silent=True)
            runner.assert_eq(r, 10, "GirlStats.change_stat returns applied change")
            runner.assert_eq(girl.stats[1].value, 90, "GirlStats.change_stat adds to value")
            r = stats.change_stat("charm", 500, apply_boost=False, spillover=False, silent=True)
            runner.assert_eq(girl.stats[1].value, 100, "GirlStats.change_stat clamps to raw max 100")
        finally:
            if _orig_test_achievements is not None:
                globals()["test_achievements"] = _orig_test_achievements
    return


# ── GirlMood | 情绪/理智组件 ──

label test_girl_mood_component:
    # EN: GirlMood sanity boundary tests. debug_mode may be undefined before
    #     game start (it is set in label start), so define it if missing.
    # ZH: GirlMood 理智值边界测试。debug_mode 在游戏开始前可能未定义
    #     （它在 label start 中赋值），缺失时在此补默认值。
    python:
        runner = TestRunner.instance()
        if "debug_mode" not in globals():
            globals()["debug_mode"] = False

        girl = _BKFakeGirl()
        mood = GirlMood(girl)

        girl.sanity = 0
        runner.assert_true("Nearly broken" in mood.get_sanity(), "GirlMood.get_sanity sanity=0 -> Nearly broken")
        girl.sanity = 7
        runner.assert_true("Very frail" in mood.get_sanity(), "GirlMood.get_sanity sanity<10 -> Very frail")
        girl.sanity = 15
        runner.assert_true("Frail" in mood.get_sanity(), "GirlMood.get_sanity sanity<20 -> Frail")
        girl.sanity = 30
        runner.assert_true("Shaken" in mood.get_sanity(), "GirlMood.get_sanity sanity<50 -> Shaken")
        girl.sanity = 60
        runner.assert_true("Normal" in mood.get_sanity(), "GirlMood.get_sanity sanity>=50 -> Normal")
        girl.broken = True
        runner.assert_true("Broken" in mood.get_sanity(), "GirlMood.get_sanity broken -> Broken")
        girl.broken = False

        mood.init_sanity()
        runner.assert_true(girl.sanity >= 5, "GirlMood.init_sanity sets sanity from dice(11, rank) + mod")
    return


# ── GirlEconomy | 经济组件 ──

label test_girl_economy_component:
    # EN: GirlEconomy.estimate_performance returns a numeric score when the
    #     girl accepts the act, and -1 when she refuses.
    # ZH: GirlEconomy.estimate_performance：接受行为时返回数值型评分，
    #     拒绝时返回 -1。
    python:
        runner = TestRunner.instance()
        girl = _BKFakeGirl()
        econ = GirlEconomy(girl)

        score = econ.estimate_performance("service")
        runner.assert_true(isinstance(score, (int, float)) and not isinstance(score, bool),
                           "GirlEconomy.estimate_performance returns a number")
        runner.assert_true(score > 0, "GirlEconomy.estimate_performance score is positive when accepted")

        girl._will_do = False
        runner.assert_eq(econ.estimate_performance("service"), -1, "GirlEconomy.estimate_performance returns -1 when refused")
    return


# ── GirlEffects | 效果组件 ──

label test_girl_effects_component:
    # EN: get_effect on an empty effect list must return the type defaults
    #     (1.0 for boosts, 0 for changes). The underlying lookup reads
    #     game.world_effect_dict, so this test needs the game instance and
    #     is skipped from the main menu (before label init_game runs).
    # ZH: 空效果列表上调用 get_effect 应返回类型默认值（boost 为 1.0，
    #     change 为 0）。底层查找会读取 game.world_effect_dict，因此本测试
    #     需要游戏实例；在主菜单（label init_game 尚未运行）时跳过。
    if globals().get("game") is None:
        $ test_runner.skip("GirlEffects.get_effect (needs game instance)")
    else:
        python:
            runner = TestRunner.instance()
            girl = _BKFakeGirl()
            eff = GirlEffects(girl)
            runner.assert_eq(eff.get_effect("boost", "tip", raw=True), 1.0, "GirlEffects.get_effect empty list -> boost default 1.0")
            runner.assert_eq(eff.get_effect("change", "tip", raw=True), 0, "GirlEffects.get_effect empty list -> change default 0")
    return


# ── Mod API v2 | Mod 接口 ──

label test_mod_api_v2:
    # EN: Mod API v2 smoke test: register -> fire -> cancel. Complemented by
    #     tools/verify_mod_api.py, which runs the same flow outside Ren'Py.
    # ZH: Mod API v2 冒烟测试：注册 -> 触发 -> 取消。与 tools/verify_mod_api.py
    #     （在 Ren'Py 外运行同一流程）互补。
    python:
        runner = TestRunner.instance()
        api = ModAPIV2.instance()

        manifest = {
            "name": "Smoke Test Mod", "version": "0.0.1", "api_version": 2,
            "min_game_version": "0.3.0", "author": "test_runner",
            "description": "bk_test_runner smoke test", "requires": ["events"],
            "dependencies": [], "hooks": {},
        }
        api.register_mod("bk_smoke_test_mod", manifest)
        runner.assert_true(api.is_mod_active("bk_smoke_test_mod"), "ModAPIV2.register_mod activates mod")

        try:
            api.register_mod("bk_bad_ver", {"api_version": 1})
            runner.assert_true(False, "ModAPIV2.register_mod rejects api_version != 2")
        except ValueError:
            runner.assert_true(True, "ModAPIV2.register_mod rejects api_version != 2")

        try:
            api.register_mod("bk_bad_cap", {"api_version": 2, "requires": ["not_a_capability"]})
            runner.assert_true(False, "ModAPIV2.register_mod rejects unknown capability")
        except ValueError:
            runner.assert_true(True, "ModAPIV2.register_mod rejects unknown capability")

        _fired = []

        def _bk_smoke_hook(context):
            _fired.append(True)
            return "ok"

        api.register_hook("bk_smoke_hook", _bk_smoke_hook)
        _results = api.execute_hook("bk_smoke_hook")
        runner.assert_true(_fired, "ModAPIV2.execute_hook fires registered callback")
        runner.assert_eq(_results.get("_direct"), "ok", "ModAPIV2.execute_hook returns callback result")

        def _bk_smoke_cancel(context):
            context["cancel"] = True

        api.register_hook("bk_smoke_cancel", _bk_smoke_cancel)
        runner.assert_true(api.cancel_hook("bk_smoke_cancel"), "ModAPIV2.cancel_hook returns True when cancelled")
        runner.assert_true(not api.cancel_hook("bk_smoke_hook"), "ModAPIV2.cancel_hook returns False when not cancelled")

        # EN: Cleanup — remove the test mod and its hooks from the shared singleton.
        # ZH: 清理——从共享单例中移除测试 mod 及其钩子。
        api.unregister_mod("bk_smoke_test_mod")
        api._mod_hooks.pop("bk_smoke_hook", None)
        api._mod_hooks.pop("bk_smoke_cancel", None)
        runner.assert_true(not api.is_mod_active("bk_smoke_test_mod"), "ModAPIV2.unregister_mod deactivates mod")
    return


# ── Entry point | 入口 ──

label bk_test_runner:
    # EN: In-game test runner entry. Reachable from the main menu "Tests"
    #     button, which is only shown when config.developer is True.
    # ZH: 游戏内测试入口。通过主菜单 "Tests" 按钮进入，
    #     该按钮仅在 config.developer 为 True 时显示。
    $ test_runner.reset()
    call test_girl_stats_component
    call test_girl_mood_component
    call test_girl_economy_component
    call test_girl_effects_component
    call test_mod_api_v2
    $ _bk_test_report = test_runner.report()
    "[_bk_test_report]"
    return
