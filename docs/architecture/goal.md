# Goal 系统架构

> 最后更新: 2026-09-11（与代码核对）
> **核心文件**: `game/core/framework/goal.rpy`（`Goal` 类 :4，init -10）
> **数据**: `game/core/data/goals/chapter_goals.json`（**7 章**，实测）+ `goal_ui.json`
> **加载点**: `game/core/init/settings.rpy:101-123`（独立加载，不经 DataLoader）

---

## 1. 系统职责

Goal 是驱动章节推进的阶段性目标：

- **类型** (`type`): `gold`（持有金币）、`ranked`（N 个女孩达到某 rank）、`reputation`（青楼声望）、`prestige`（MC 声望）、`story`（剧情 flag，值即 label）。
- **门控语义**: `reached()`（goal.rpy:52）——`blocking=True` 且未达成时阻止章节推进；`max_chapter` 声明适用章节上限；非 blocking 目标恒为 reached。
- **频道**: `channel="advance"` 为主推进频道；其他频道用于可选支线。
- **描述**: `get_description()`（goal.rpy:34）按类型生成（或取 story 类型的文本值）。

## 2. 数据流

```
game/core/data/goals/chapter_goals.json (7 章, 每章一个 Goal dict 列表)
    └─→ init/settings.rpy:101-123
           ├─ JSON 存在: Goal.from_dict(g) 逐条构造 → chapter_goals[int(ch)]
           └─ JSON 缺失: chapter_goals = _chapter_goals_fallback (settings.rpy:101 硬编码回退)
    └─→ Game.goals = chapter_goals[1]          (core_entities.rpy:34, 开局)
    └─→ game.set_goals(chapter_goals[chapter]) (events_dispatcher.rpy:1015, 每章切换)

goal_ui.json ─→ DataLoader.load_goal_ui() ─→ settings.rpy:520 (目标界面展示配置)
```

注意：Goal 类型只接收上述 5 种；旧文档中提到的 `bedrooms/girls/customers/districts/mc_level/free` 等类型在 `reached()` 中**没有实现分支**（会落入 `return False` 恒阻塞），属于历史残留描述，勿依赖。

## 3. 解耦方式

- **与 Game 解耦**: Goal 只读全局 `MC`/`brothel`/`game`/`story_flags`，不持有 Game 引用。
- **与存档解耦**: Goal 由 JSON 每次 init 重建，不进存档；进度判定始终是当前实际数值（金币/声望等）。
- **与 DataLoader 解耦**: 历史原因走 settings.rpy 自载（含自己的 fallback），是两类自载路径之一（另一处是 customer_affixes）。

## 4. 系统间联系

- **章节推进**: `events_dispatcher.rpy:1015` 换章时 `set_goals`；推进检查调 `Goal.reached()`。
- **模式门控**: story 模式用目标门控，sandbox 模式可自由推进（见 [gamemode.md](gamemode.md) 的 `can_advance_chapter`）。
- **目标界面**: `screen_resources.rpy` 的 `goal_ttip` 等展示当前目标，`goal_ui.json` 提供 UI 配置。

## 5. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 开发控制台 | ✅ 查看 | chapter_goals.json 经 data_sync 校验格式 |
| 直接编辑 JSON | ✅ | 结构简单（每章一个 dict 列表），改后重启生效 |

---

## 相关文档

- [gamemode.md](gamemode.md) — 章节推进与模式规则
- [data_loader.md](data_loader.md) — goal_ui.json 走 DataLoader 的例外对照
- [event.md](event.md) — story 类型 Goal 与 story_flags 的关系
