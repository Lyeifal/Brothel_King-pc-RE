# Goal 系统架构

> **文件**: `game/core/framework/core_entities.rpy` (Goal 类), `game/core/init/settings.rpy` (chapter_goals 回退)  
> **数据**: `game/core/data/goals/chapter_goals.json` + Schema  
> **编辑支持**: ✅ 开发控制台 (`dev_console`)

---

## 1. 系统职责

Goal 代表玩家需要达成的阶段性目标，驱动章节推进：

- **类型**: `gold`, `prestige`, `rep`, `bedrooms`, `girls`, `customers`, `districts`, `mc_level`, `free` 等
- **频道**: `channel="advance"` 表示阻止章节推进，直到目标达成；其他频道用于可选支线。
- **阻塞性**: `blocking=True` 时目标必须完成才能进入下一章。

核心方法：
- `Goal.from_dict(d)` — JSON 反序列化，支持 BK Evolution 数据驱动加载。
- `Game.set_goals()` / `goals_reached()` / `get_goal_description()` — 游戏主类中的目标管理接口。

---

## 2. 解耦方式

- **数据与逻辑分离**: 章节目标从 `settings.rpy` 的硬编码字典提取到 `chapter_goals.json`，`Goal` 类新增 `from_dict()` 支持纯数据构造。
- **与 GameMode 解耦**: `Goal` 通过 `channel` 与模式关联，而非直接引用 `GameMode` 实例。`GameMode.goal_channels` 决定哪些频道在当前模式下生效。
- **与章节系统解耦**: `MAX_CHAPTER = 7` 提取为常量，`chapter_district_unlocks` / `chapter_titles` 也 JSON 化，不再与 `Goal` 硬绑定。

---

## 3. 系统间联系

```
chapter_goals.json
    └─→ DataLoader.load_all() (优先加载 JSON，失败回退 _chapter_goals_fallback)
           └─→ Goal.from_dict()
                  └─→ Game.set_goals()    (按当前 chapter 和 channel 激活)
                         └─→ Game.goals_reached()   (每日/推进时检查)
                                └─→ chapter advance 逻辑
```

- `init/start.rpy` 在游戏初始化时调用 `game.set_goals(chapter)`。
- `GameMode` 的 `goal_channels` 决定了哪些目标频道在当前模式下被评估。

---

## 4. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 开发控制台 | ✅ 完整 | 可直接查看/编辑 `chapter_goals.json` 等目标元数据 |
| 剧本编辑器 | ❌ 无 | 不涉及 |
| 女孩包编辑器 | ❌ 无 | 不涉及 |

---

## 5. 向后兼容

- `settings.rpy` 保留 `_chapter_goals_fallback` 硬编码字典。
- 若 `game/core/data/goals/chapter_goals.json` 不存在或解析失败，自动回退到硬编码。
- `Goal.from_dict()` 兼容旧字段缺失的情况，使用默认值。
