# Mod 系统架构

> 最后更新: 2026-09-11（与代码核对）
> **核心文件**: `game/core/framework/challenges.rpy`（v1 Mod 类）、`game/core/systems/mods/mod_api.rpy`（v1 API）、`game/core/systems/mods/mod_api_v2.rpy`（v2 API）、`game/core/systems/mods/mod_hooks.rpy`（HookManager）
> **Phase**: Phase 5/6（Mod 支持）

---

## 1. 系统职责

Mod 系统让第三方内容以两种机制共存：

- **v1（Mod 类）**: 传统 Mod。作者在自己的 `.rpy` 中声明 `Mod(...)` 实例，自动进入 `detected_mods`，由玩家在游戏内逐存档启用/停用，带生命周期 label（early/init/night/update/load/remove）与 `persistent.mods` 持久化状态。
- **v2（ModAPIV2）**: 声明式 manifest 注册。Mod 调用 `ModAPIV2.instance().register_mod(mod_id, manifest)`，声明能力需求（capabilities）、钩子表、依赖与 UI 按钮；安装即常驻激活，无逐存档开关。

两套 API 各有**独立**的钩子存储（见第 5 节），互不干扰；v1 继续可用，靠兼容层保留。

## 2. v1 Mod 类

定义于 `game/core/framework/challenges.rpy:370`（`class Mod(object)`）。

### 2.1 构造参数（challenges.rpy:374）

- `name` / `folder` / `creator` / `version` / `pic` / `description` — 元数据；`self.path = "mods/" + folder + "/"`.
- 生命周期 label：`early_label`（开局、区/青楼建立前）、`init_label`（建立后）、`night_label`（每夜事件）、`update_label`、`load_label`（读档时）、`remove_label`（停用时清理）。
- `chapter_labels` — 按章节（1-7）触发的 label 表。
- `events` — Mod 事件字典（声明时全部打上 `ev.mod = self`）。
- `home_rightmenu_add_buttons` — 主页右侧菜单按钮。
- `help_prompts` — 帮助菜单项。

### 2.2 状态持久化技巧

`__setattr__` / `__getattribute__` 重写（challenges.rpy:441-465）：init 阶段之后的属性赋值写入全局 `mod_settings`（defaultdict(dict)，随存档保存），读取时优先从 `mod_settings[self.name]` 取——使 Mod 自定义属性跨存档会话保持，而 init 期声明的元数据不被每次 init 覆盖。

### 2.3 注册流程

```
Mod 作者 rpy 中: Mod(name=..., folder=..., ...) 实例化
        │  __init__ 末尾: detected_mods[self.name] = self   (challenges.rpy:432)
        ▼
detected_mods 全局字典 (init/variables.rpy:2389 置空, 声明期填充)
        ▼
游戏启动 Game.update_mods() (core_entities.rpy:201):
  - 新存档: 弹 yes_no 询问逐存档激活 (core_entities.rpy:233-237)
  - 旧存档: 对 persistent.mods 中已激活的 Mod 调 activate_mod (core_entities.rpy:225)
  - game_systems.rpy:158-172 清理 detected_mods 中已不存在的 Mod
        ▼
Game.activate_mod(mod, early=False) (core_entities.rpy:243):
  1. early=True: 仅调 early_label 后返回
  2. 把 mod.hooks 批量注册到 HookManager (core_entities.rpy:255-257)
  3. 把 mod.events 注册进 EventRegistry (category="mod") (core_entities.rpy:260-262)
  4. night_label 包装为每日 StoryEvent 追加 (core_entities.rpy:264-265)
  5. 调 init_label
Game.deactivate_mod(mod) (core_entities.rpy:277):
  - 移除 active_mods、hook_manager.unregister_mod(mod)、移除夜间事件、调 remove_label
```

Mod 管理界面：`screen mods`（ui/screens/screen_quest.rpy:564 起）列出 `detected_mods`，玩家可在此激活/停用。

## 3. v2 ModAPIV2

定义于 `game/core/systems/mods/mod_api_v2.rpy:17`（`class ModAPIV2(ModAPI)`，init -3），单例 `mod_api_v2` 注册为服务（mod_api_v2.rpy:205-206）。

- **Capabilities**（mod_api_v2.rpy:30-41）: `girl_stats`、`girl_traits`、`economy`、`events`、`dialogue`、`pictures`、`game_modes`、`origin`、`scenario`、`ngp_settings`，注册时校验，未知能力直接 `ValueError`。
- **`register_mod(mod_id, manifest)`**（:50）: manifest 含 `name/version/api_version(必须=2)/min_game_version/author/description/requires/hooks/dependencies/home_rightmenu_add_buttons`。重复注册报错。
- **常驻激活**: 无 per-save 开关；停用 = 从 `game/custom/mods/` 移除文件。
- **UI 集成**: `get_menu_buttons()` 供主页右侧菜单渲染；`get_mod_info()` 供 mods 界面展示。
- **v1 继承**: v2 继承 `ModAPI`，因此 `register_trait/perk/tag/dialogue/event/ngp_setting/scenario/origin/game_mode` 等注册包装 v2 Mod 同样可用。

## 4. 18 个 v2 钩子点（全部接线，逐一 grep 核实）

命名约定 `<domain>_<action>_<tense>`。钩子常量在 mod_api_v2.rpy:187-204 定义。除最后 2 个目的地钩子外**全部为纯通知型**——调用点以 `$ mod_api_v2.execute_hook(...)` 形式丢弃返回值，Mod 只能观察不能拦截游戏逻辑（`cancel_hook` 机制存在但目前没有任何游戏内调用点使用它）。`girl_destination_list`/`girl_destination_accept` 例外：返回值/参数用于把 Mod 注册的女孩安置目的地接入收购流程（见第 17/18 行及 "Courtyard" Mod 参考实现）。

| # | 常量 | 钩子名 | 调用点（文件:行号） | Context 键 |
|---|------|--------|--------------------|-----------|
| 1 | `HOOK_GIRL_GENERATED` | `girl_generated` | `framework/girl_factory.rpy:278` | `girl` |
| 2 | `HOOK_GIRL_ACQUIRED` | `girl_acquired` | `systems/events_dispatcher.rpy:8465` | `girl`, `price`, `context` |
| 3 | `HOOK_GIRL_SOLD` | `girl_sold` | `ui/main.rpy:839`、`ui/main.rpy:1452` | `girl`, `price` |
| 4 | `HOOK_GIRL_RUNAWAY` | `girl_runaway` | `systems/events_dispatcher.rpy:1173` | `girl` |
| 5 | `HOOK_DAY_STARTING` | `day_starting` | `systems/endday.rpy:1498` | `time` |
| 6 | `HOOK_DAY_ENDING` | `day_ending` | `systems/endday.rpy:340` | `time` |
| 7 | `HOOK_NIGHT_STARTING` | `night_starting` | `systems/endday.rpy:403` | `time` |
| 8 | `HOOK_NIGHT_FINISHED` | `night_finished` | `systems/endday.rpy:1431` | `time` |
| 9 | `HOOK_WEEK_STARTING` | `week_starting` | `framework/core_entities.rpy:1937` | `week`, `time` |
| 10 | `HOOK_EVENT_TRIGGERING` | `event_triggering` | `systems/events_dispatcher.rpy:1084` | `event`, `event_type`, `label` |
| 11 | `HOOK_EVENT_FINISHED` | `event_finished` | `systems/events_dispatcher.rpy:1087` | `event`, `event_type`, `label` |
| 12 | `HOOK_SECURITY_EVENT` | `security_event` | `systems/security.rpy:62` | `event_type`, `alert_level` |
| 13 | `HOOK_CHAPTER_STARTING` | `chapter_starting` | `systems/events_dispatcher.rpy:661` | `chapter` |
| 14 | `HOOK_CHAPTER_FINISHED` | `chapter_finished` | `systems/events_dispatcher.rpy:1053` | `chapter` |
| 15 | `HOOK_GAME_SAVED` | `game_saved` | `mods/mod_api_v2.rpy:215`（经 `renpy.config.save_json_callbacks`，注册于 :209-219） | — |
| 16 | `HOOK_GAME_LOADED` | `game_loaded` | `systems/events_dispatcher.rpy:191` | — |
| 17 | `HOOK_GIRL_DESTINATION_LIST` | `girl_destination_list` | `systems/events_dispatcher.rpy:8403` | `girl`, `at_working_cap`；回调返回 `[{"id", "text", "available"}]` |
| 18 | `HOOK_GIRL_DESTINATION_ACCEPT` | `girl_destination_accept` | `systems/events_dispatcher.rpy:8497` | `girl`, `destination` |

Mod 侧用法见模板 `game/core/templates/mod_template/mod_template.rpy:47-53`：`api.register_hook(api.HOOK_GIRL_GENERATED, on_girl_generated)`，回调签名 `callback(context: dict)`。

## 5. HookManager（mod_hooks.rpy）与 v2 钩子的关系

`HookManager`（mod_hooks.rpy:6，init -4，单例 `hook_manager`）是 **v1 时代的中心调度器**：

- 存储 `{hook_name: [(callback, mod), ...]}`，按注册顺序调用，异常在 developer 模式下记日志。
- v1 Mod 通过 `mod.hooks` 字典在激活时批量注册（core_entities.rpy:255-257）；`ModAPI.hook()`（mod_api.rpy:66-68）也指向它。
- 停用 Mod 时 `hook_manager.unregister_mod(mod)` 全量清理。

**当前 v1 钩子调用点**（grep 核实）：

| 钩子名 | 调用点 | 场景 |
|--------|--------|------|
| `on_day_end` | `systems/endday.rpy:337` | 日结 settlement_ctx |
| `on_settlement_girls_ready` | `systems/endday.rpy:555` | 女孩阶段就绪 |
| `on_settlement_end` | `systems/endday.rpy:1587`、`systems/settlement/settlement_pipeline.rpy:104` | 结算结束 |
| `on_day_start` | `systems/endday.rpy:1588` | 新一天开始 |
| `pre_settlement_phase` / `pre_settlement_<phase>` | `systems/settlement/settlement_pipeline.rpy:76-77` | 每阶段前 |
| `post_settlement_<phase>` / `post_settlement_phase` | `systems/settlement/settlement_pipeline.rpy:84-85` | 每阶段后 |
| `on_settlement_start` | `systems/settlement/settlement_pipeline.rpy:97` | 结算开始 |
| `on_event_trigger` | `systems/events/event_engine.rpy:183`（EventEngine.on_event_trigger） | 事件触发 |

两套系统并存的关系：

```
v1 Mod (challenges.rpy)
  └─ mod.hooks ──→ HookManager (mod_hooks.rpy) ──→ on_day_end / on_settlement_* / on_event_trigger
v2 Mod (manifest hooks + register_hook)
  └─ _mod_hooks (mod_api_v2.rpy:46, 独立存储!) ──→ girl_generated 等 18 个钩子（其中 girl_destination_list/accept 为交互型）
```

注意两点：

1. **存储完全分离**：v2 的 `register_mod` 把 manifest hooks 写进 `ModAPIV2._mod_hooks`（mod_api_v2.rpy:88-89），不经过 HookManager；反之 v1 的 `on_day_end` 等钩子在 v2 侧没有任何对应常量。
2. **HookManager 的 `invoke_first` 支持覆盖默认行为**（mod_hooks.rpy:67），但目前所有 v1 调用点都用 `invoke`，实际同样退化为纯通知。

## 6. 向后兼容与已知限制

- v1 Mod 完全保留原行为；`ModAPI`（v1）与 `ModAPIV2` 单例各自独立。
- v2 钩子命名（`girl_generated`）与 v1（`on_girl_generate`）风格不一致，是历史遗留，新 Mod 应使用 v2 常量。
- `game_saved` 钩子通过 `renpy.config.save_json_callbacks` 实现，有防重复注册守卫（mod_api_v2.rpy:218）。
- v1 钩子点数量少且集中在结算管线；v2 钩子点覆盖女孩/事件/章节/昼夜/存档全生命周期。

---

## 相关文档

- [services.md](services.md) — mod_api_v2 服务注册
- [registry.md](registry.md) — Mod 通过 API 注册的各类内容目标
- [event.md](event.md) — on_event_trigger / event_triggering 钩子的事件系统上下文
- [gamemode.md](gamemode.md) — v2 capability 中的 game_modes / scenario / origin
