# GameMode 系统架构

> **文件**: `game/core/systems/gamemodes/gamemode.rpy`  
> **依赖**: `game/core/framework/core_entities.rpy` / `game/core/framework/game_systems.rpy` (Game 类)  
> **编辑支持**: ✅ 剧本编辑器（完整）

---

## 1. 系统职责

GameMode 定义了游戏的三种运行模式，每种模式拥有独立的规则集、胜利条件和目标频道：

| 模式 ID | 常量 | 职责 |
|---------|------|------|
| `story` | `MODE_STORY` | 主线剧情模式，7 章线性推进，有固定的章节目标 (`chapter_goals`) |
| `sandbox` | `MODE_SANDBOX` | 沙盒模式，自由经营，使用 `sandbox_events` 事件池 |
| `scenario` | `MODE_SCENARIO` | 剧本模式，加载自定义 `Scenario` 包，可覆盖默认规则 |

核心类：
- `GameMode` — 基类，封装 `mode_id`、`name_i18n_key`、`start_label`、`goal_channels`、`allowed_event_pools` 等。
- `GameModeRegistry` — 单例注册表，管理所有可用模式实例。

---

## 2. 解耦方式

- **与 `Game` 解耦**: `Game` 只持有 `self.game_mode` 引用，通过 `is_story_mode()` 等接口查询，不直接硬编码模式逻辑。
- **与事件系统解耦**: `StoryEvent.modes` 字段允许事件声明自己适用的模式；`EventEngine` 在入队时过滤，而非事件自身判断。
- **与目标系统解耦**: `Goal` 的 `channel` 字段（如 `"advance"`）与 `GameMode.goal_channels` 对应，模式切换时自动切换活跃目标集。

---

## 3. 系统间联系

```
GameModeRegistry
    └─ 注册 story / sandbox / scenario 实例
           ├─→ Game.game_mode          (运行时当前模式)
           ├─→ EventEngine.filter()    (modes 过滤)
           ├─→ Goal.set_goals()        (按 channel 加载目标)
           └─→ Scenario                (scenario 模式的数据包)
```

- `Game.is_story_mode()` 替代了原全局变量 `story_mode`，消除了 17 处运行时硬编码引用。
- `init/start.rpy` 在新游戏启动时根据玩家选择设置 `game.game_mode`。

---

## 4. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 剧本编辑器 (`scenario_editor`) | ✅ 完整 | 可编辑 `Scenario` 的 `game_mode_override`、事件池与目标频道 |
| 开发控制台 (`dev_console`) | ✅ 数据同步 | 可查看/调整 GameMode 相关的 JSON 元数据 |
| 女孩包编辑器 | ❌ 无 | 不涉及 |

---

## 5. 向后兼容

- 旧存档中 `game_mode` 可能为 `None`，`is_story_mode()` 安全返回 `False`。
- 原全局变量 `story_mode` 在 `init/start.rpy` 初始化过渡代码中仍保留，确保旧存档加载后自动迁移到 `game.game_mode`。
