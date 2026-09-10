# Event / StoryEvent 系统架构

> **文件**: `game/core/framework/core_entities.rpy` (StoryEvent), `game/core/systems/events/event_engine.rpy`, `game/core/init/start.rpy` (event_dict 加载)  
> **数据**: `game/core/data/events/event_dict.json`  
> **编辑支持**: ✅ 剧本编辑器 (`scenario_editor`)

---

## 1. 系统职责

StoryEvent 是游戏内所有剧情/随机/城市/每日事件的统一封装：

- **触发条件**: `chapter`, `rank`, `date`, `location`, `seasons`, `condition_func` 等多维过滤。
- **生命周期**: `once=True` 一次性事件 / `once=False` 可重复事件。
- **模式过滤** (BK Evolution 新增): `modes` 字段声明事件适用的 `GameMode`，支持 `None`（全模式）、`str`（单模式）、`list`（多模式）。
- **JSON 反序列化**: `StoryEvent.from_dict()` 支持从 JSON 构造，自动解析 `condition_func` 字符串为全局函数引用。

核心类：
- `StoryEvent` — 事件定义。
- `EventEngine` — 事件调度引擎，负责按优先级/权重/条件筛选并入队。
- `EventRegistry` — 事件注册表（Registry 系统的一部分）。

---

## 2. 解耦方式

- **与 GameMode 解耦**: 事件不直接查询 `game.game_mode`，而是通过 `modes` 字段声明自身适用范围；`EventEngine` 在入队时统一过滤。
- **与硬编码解耦**: 事件从 `start.rpy` 的 `_event_dict_fallback` 导出到 `event_dict.json`，`start.rpy` 优先加载 JSON。
- **与条件函数解耦**: `condition_func` 在 JSON 中以字符串存储，反序列化时通过 `globals().get()` 解析，函数不存在时静默为 `None`（安全降级）。

---

## 3. 系统间联系

```
event_dict.json
    └─→ DataLoader.load_all() / start.rpy (StoryEvent.from_dict)
           └─→ EventRegistry.register_event()
                  ├─→ EventEngine (运行时筛选入队)
                  │       ├─→ GameMode.modes 过滤
                  │       └─→ 条件函数评估
                  └─→ calendar.set_alarm()  (定时事件)
```

- `EventEngine` 在每日/城市探索结算时调用，综合 `EventRegistry` 中所有事件进行筛选。
- 主线专属事件（`c1_*`, `c2_*`, `c3_*` 等）标记 `modes="story"`，确保不会出现在沙盒/剧本模式中。

---

## 4. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 剧本编辑器 (`scenario_editor`) | ✅ 完整 | StoryEvent 的完整 CRUD：`label`, `chapter`, `rank`, `modes`, `condition`, `weight` 等全部字段可视化编辑 |
| 开发控制台 (`dev_console`) | ✅ 数据同步 | JSON Schema 验证、批量格式化、元数据查看 |

---

## 5. 向后兼容

- `start.rpy` 保留 `_event_dict_fallback` 硬编码字典，JSON 缺失/损坏时自动回退。
- `StoryEvent.__init__` 的 `modes=None` 默认行为与旧代码完全一致（全模式可见）。
- `condition_func` 解析失败时不抛异常，避免单个坏事件导致整个注册表崩溃。
