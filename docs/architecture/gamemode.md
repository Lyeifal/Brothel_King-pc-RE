# Game / GameMode 系统架构

> 最后更新: 2026-09-11（与代码核对）
> **核心文件**: `game/core/framework/core_entities.rpy`（`Game` 类 :19）、`game/core/framework/game_systems.rpy`（1,325 行）、`game/core/systems/gamemodes/`（7 个文件）
> **编辑支持**: ✅ 剧本编辑器（scenario 部分）

---

## 1. 系统职责

- **`Game`**（core_entities.rpy:19，`class Game(EffectBearer, Trackable)`）：对局状态总容器——章节、目标（`self.goals`，初始为 `chapter_goals[1]`，:34）、激活 Mod（`active_mods`）、游戏模式（`game_mode`）、商人/已见事件等。运行期注册为服务 `services.game`（start.rpy:245）。
- **`GameMode`**（systems/gamemodes/gamemode.rpy:9，init -10）：模式基类。每种模式定义规则集、胜利条件、目标频道与开局行为（`on_game_start`、`can_advance_chapter` 等可覆盖方法）。
- **`GameModeRegistry`**（gamemode.rpy:128）：模式注册表，`register(mode)` 按 `mode_id` 存储，`get()` / `list_modes()` 查询。三个内置模式注册点：`story_mode.rpy:63`、`sandbox_mode.rpy:227`、`scenario_mode.rpy:246`。

## 2. 三种游戏模式

| 模式 ID | 常量 | 注册位置 | 职责 |
|---------|------|---------|------|
| `story` | `MODE_STORY` | `story_mode.rpy:63` | 主线剧情，7 章线性推进，用章节目标（chapter_goals）门控推进 |
| `sandbox` | `MODE_SANDBOX` | `sandbox_mode.rpy:227` | 沙盒自由经营；含 `OriginRegistry`（sandbox_mode.rpy:150）提供玩家出身选择 |
| `scenario` | `MODE_SCENARIO` | `scenario_mode.rpy:246` | 自定义剧本；含 `ScenarioRegistry`（scenario_mode.rpy:165），剧本定义胜利条件与事件集 |

辅助模块：gamemodes/ 下还有 `kidnap_system.rpy`、`special_girl_npc.rpy`、`screen_gamemode.rpy`（开局模式选择界面）。

## 3. 与 Game 的协作

```
label start (init/start.rpy)
  ├─→ services.register("game", game) (:245)
  ├─→ 模式选择界面 (screen_gamemode.rpy) → gamemode_registry.get(mode_id)
  ├─→ game.game_mode = <mode实例>; game_mode.on_game_start(game)
  ├─→ game.goals = chapter_goals[1] (core_entities.rpy:34, story 模式)
  └─→ Game.update_mods() (core_entities.rpy:201) 处理 Mod 激活询问

章节推进 (events_dispatcher.rpy:1015):
  game.set_goals(chapter_goals[chapter]) → Goal.reached() 全达成才放行（见 goal.md）
```

模式过滤贯穿事件系统：EventEngine 入队时按 `event.modes` 与 `game.game_mode.mode_id` 比对（event_engine.rpy:78-83）。

## 4. game_systems.rpy 的角色

`framework/game_systems.rpy`（1,325 行）是 Game 相关的**函数层**（非类）：`update_mods` 的持久化清理（:158-172，移除 `detected_mods` 中已删除的 Mod 并同步 `persistent.mods`）、`load_quest_pics`（:227）等。Mod 生命周期管理跨 core_entities.rpy（activate/deactivate/update）与 game_systems.rpy（持久化清理）两处，阅读时注意区分。

## 5. Mod 集成

- `Game.activate_mod` / `deactivate_mod` / `update_mods`（core_entities.rpy:201-298）：逐存档 Mod 生命周期（详见 [mod_system.md](mod_system.md)）。
- v2 capability `game_modes` / `origin` / `scenario` 允许 Mod 注册新模式/出身/剧本（`ModAPI.register_game_mode/register_origin/register_scenario` → 对应 Registry）。

## 6. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 剧本编辑器 `scenario_editor_tab.py` | ✅ | 读写 `core/data/scenarios/scenarios.json` → `DataLoader.load_scenarios()` → ScenarioRegistry |
| 开局模式界面 | — | `screen_gamemode.rpy` 内嵌于游戏 |

---

## 相关文档

- [goal.md](goal.md) — 章节目标与模式推进门控
- [event.md](event.md) — 事件的 modes 过滤
- [mod_system.md](mod_system.md) — Mod 生命周期与新模式注册
- [services.md](services.md) — game 服务注册时机
