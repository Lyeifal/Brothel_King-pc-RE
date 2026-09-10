# Event / StoryEvent 系统架构

> 最后更新: 2026-09-11（与代码核对）
> **核心文件**: `game/core/framework/interactions.rpy`（`StoryEvent` 类 :55）、`game/core/systems/events_dispatcher.rpy`（8,611 行，运行时分发）、`game/core/systems/events/event_engine.rpy`（202 行）、`game/core/systems/events/event_bridge.rpy`（68 行）
> **编辑支持**: ✅ 剧本编辑器 (`scenario_editor`)

---

## 1. 系统职责

StoryEvent 是游戏内所有剧情/随机/城市/每日事件的统一封装（注意：类定义在 `framework/interactions.rpy:55`，**不在** core_entities.rpy——旧文档此处有误）：

- **触发条件**: `chapter`、`rank`、`date`、`location`、`seasons`、`condition_func` 等多维过滤。
- **生命周期**: `once=True` 一次性 / `once=False` 可重复。
- **模式过滤** (BK Evolution): `modes` 字段声明适用的 GameMode（`None` 全模式 / `str` 单模式 / `list` 多模式），入队时在 EventEngine 检查。
- **类型队列**: `city`（城市事件）与 `daily`（晨/日/夜）两大类全局队列，另有 alarm 精确日历闹钟。

## 2. 四个关键组件

### 2.1 StoryEvent（interactions.rpy:55）

底层数据类：label 指向 Ren'Py label，含优先级 `order`、触发条件与调用参数。Mod 的 `night_label` 也包装成每晚触发的 StoryEvent（core_entities.rpy:265）。

### 2.2 events_dispatcher.rpy（8,611 行）

运行时分发中枢：`city_events` / `daily_events` 队列的每日筛选、触发、执行（`call` 对应 label）。同时承载 v2 钩子 `event_triggering`/`event_finished`（:1084/:1087）、`chapter_starting`/`chapter_finished`（:661/:1053）、`girl_runaway`（:1173）、`girl_acquired`（:8440）、`game_loaded`（:191）的调用点。

### 2.3 EventEngine（systems/events/event_engine.rpy）

init -4 单例，注册为服务 `services.event_engine`（:202）。高层管理接口：

- `register_story_event()` / `register_event_from_dict()` — 注册进 EventRegistry，可顺带入队。
- `add_event_to_queue()` / `remove_event_from_queue()` — 运行时队列管理；入队前做 **modes 过滤**（:78-83）与位置强制 city 语义（:86）。
- `scan_custom_events()` / `load_event_pack()` — 扫描 `core/content/events/` 并用 `renpy.load_string()` 运行时加载事件包。
- `on_event_trigger()` — 经 HookManager 触发 v1 `on_event_trigger` 钩子（:183）。

### 2.4 EventBridge（systems/events/event_bridge.rpy）

init -11 单例。定位是新旧系统桥：旧 API（`add_event()` / `story_add_event()`）添加事件时同步到 EventEngine，保证两套系统看到同一批事件。

**⚠ 已知问题（与代码核对发现）**: `EventBridge.sync_to_engine()`（event_bridge.rpy:52）调用 `engine.register_runtime_event(event, event_type)`，但 `EventEngine` 上**并不存在**该方法（现有的是 `add_event_to_queue` / `remove_event_from_queue`，grep 全库无 `register_runtime_event` 定义）。由于桥接代码整体 try/except 静默吞掉异常，旧→新同步目前实际是**无声空操作**；反向（New→Old，event_dict 代理）由 `event_registry.rpy:65` 的代理正常处理。修复方向：把桥接改为调用现有入队 API。

## 3. 系统间联系

```
story_events.json / sandbox/events.json / scenarios.json
    └─→ DataLoader.load_story_events() / load_sandbox_events()
           └─→ EventRegistry (init -5)  ←── ModAPI.register_event (category="mod")
                  ├─→ event_dict 代理 (New→Old 兼容)
                  └─→ EventEngine ──→ city_events / daily_events 全局队列
                                         └─→ events_dispatcher.rpy 每日筛选触发
                                                ├─→ v1 钩子 on_event_trigger (HookManager)
                                                └─→ v2 钩子 event_triggering / event_finished

旧 API add_event()/story_add_event() ──→ EventBridge.sync_to_engine()（当前为空操作，见 2.4）
```

## 4. Mod 与钩子集成

- v1 Mod 激活时 events 自动注册进 EventRegistry（core_entities.rpy:260-262），`night_label` 成为每夜 StoryEvent。
- v2 钩子 `event_triggering` / `event_finished` 在 dispatcher :1084/:1087 触发，context 含 `event`、`event_type`、`label`。

## 5. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 剧本编辑器 `event_editor.py` | ✅ | story_events.json / sandbox events.json 的 CRUD，走 EventRegistry 契约 |
| 事件包热加载 | ✅ | `EventEngine.load_event_pack()` 支持运行时 `.rpy` 事件包 |

---

## 相关文档

- [registry.md](registry.md) — EventRegistry 基类机制
- [data_loader.md](data_loader.md) — 事件 JSON 加载
- [mod_system.md](mod_system.md) — v1/v2 事件钩子对照
- [gamemode.md](gamemode.md) — modes 过滤与 GameMode 的关系
