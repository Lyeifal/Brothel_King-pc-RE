# DataLoader 系统架构

> 最后更新: 2026-09-11（与代码核对）
> **文件**: `game/core/systems/data_loader.rpy`（1,319 行）
> **调用时机**: 类定义 `init -11`（data_loader.rpy:7）；`DataLoader.load_all()` 在 `label start` 运行期调用（`game/core/init/start.rpy:258`）
> **数据目录**: `game/core/data/`

---

## 1. 系统职责

DataLoader 是 BK Evolution 中所有 JSON 驱动内容的统一加载入口：

- **一次性加载**: 每个 JSON 文件每会话只解析一次（`cls._loaded` 缓存集合，data_loader.rpy:18）。
- **安全降级**: `_load_json_file()`（:41）经 `renpy.loadable()` / `renpy.open_file()` 读取；文件不存在或非法时 `renpy.notify()` 提示并返回 `None`，不阻止游戏启动。
- **多类别支持**: 约 45 个 `load_*` 类方法（:27-1308），覆盖 Trait、Perk、Origin、StoryEvent、SandboxEvent、Scenario、Achievement、Challenge、Difficulty、NGP、Meta、Item、Power、Shop、Spell、MC 职业、Minion、Installation、Gossip、对话文本、近期事件、清洁惩罚、宝藏阈值、税率、维护描述、目标 UI、安全事件、事件颜色等。
- **运行时覆盖**: 文件尾部 `init -1` 块（data_loader.rpy:1309-1319）用 `load_difficulty()` 的 JSON 覆盖全局难度表。

核心方法：

| 方法 | 说明 |
|------|------|
| `DataLoader.load_all()` (:27) | 加载全部核心类别（traits/perks/origins/story+sandbox events/scenarios/achievements/challenges/difficulty/ngp/meta） |
| `DataLoader.reset_cache()` (:34) | 清缓存，支持运行时重载（调试） |
| `DataLoader._load_json_file(rel_path)` (:41) | 统一安全读取，`DATA_DIR = "core/data"` |

## 2. Fallback 模式（仍在，未清理）

**DataLoader 自身只返回数据或 None，不做回退**；回退逻辑分散在各调用点，模式统一为「JSON 优先，硬编码 fallback」。已核实的 fallback 点：

| 调用点 | 文件:行 | 说明 |
|--------|---------|------|
| 模板/全部物品 | `game/core/data/items.rpy:98-99` | `load_items() or _fallback_template_items / _fallback_all_items` |
| 工作绩效字典 | `game/core/data/jobs.rpy:227` | `perform_job_dict = _fallback_perform_job_dict` |
| 对抗挑战概率 | `framework/challenges.rpy:36` | JSON 缺失用硬编码表 |
| 核心实体查表 | `framework/core_entities.rpy:7` | 实体 lookup table |
| 顾客等级/性行为简评 | `framework/economy.rpy:1894, 1902` | 顾客 rank 顺序、sex act 短描述 |
| UI 颜色映射 / EV 画廊 | `content/declarations.rpy:292, 1494` | |
| 自由女孩互动好感上限 | `content/interactions_free.rpy:6` | |
| 贷款参数 | `content/story_events/story_events.rpy:14312` | |
| 章节目标 | `init/settings.rpy:101-123` | `_chapter_goals_fallback` + `Goal.from_dict` |
| 安全事件 | `init/settings.rpy:231-240` | `load_security_events()` 失败置 `{}` |

**现状评估**: fallback 是刻意的兼容策略而非临时方案（`tools/bk_editor/AGENTS.md` 明确要求"保留硬编码 fallback，确保 JSON 文件缺失时游戏仍可启动"），暂无清理计划；称其为"未清理"是指双份数据源长期共存，修改数据时须同时意识到两处。

## 3. 解耦方式

- **与游戏逻辑解耦**: DataLoader 只读 JSON 并构造对象，不干预运行逻辑。
- **与注册表解耦**: 加载器知道注册表接口（如 `trait_registry.register_trait()`）但不依赖其内部实现；构造产物交给注册表管理（见 [registry.md](registry.md)）。
- **与文件系统解耦**: 用 Ren'Py `renpy.loadable()` / `renpy.open_file()` 而非原生 Python IO，打包发行（Android/Steam）后仍可工作。例外：`customer_affixes.rpy:18` 与 `settings.rpy` 中章节目标等少数点仍用 `os.path` + 原生 open——已知不一致。

## 4. 系统间联系

```
game/core/data/
    ├─→ traits/traits.json (131 条)      → load_traits()        → TraitRegistry
    ├─→ perks/perks.json (53 条)         → load_perks()         → PerkRegistry
    ├─→ sandbox/origins.json               → load_origins()       → sandbox OriginRegistry
    ├─→ stories/story_events.json          → load_story_events()  → EventRegistry
    ├─→ sandbox/events.json                → load_sandbox_events()→ EventRegistry
    ├─→ scenarios/scenarios.json           → load_scenarios()     → ScenarioRegistry
    ├─→ achievements/achievements.json     → load_achievements()  → 成就系统
    ├─→ difficulty/difficulty.json         → load_difficulty()    → init -1 覆盖 diff_list 等
    ├─→ ngp/ngp_settings.json              → load_ngp_settings()  → NGPRegistry
    ├─→ meta/meta_progression.json         → load_meta_progression() → MetaRegistry
    ├─→ goals/goal_ui.json                 → load_goal_ui()       → settings.rpy:520
    ├─→ settings/security_events.json      → load_security_events() → settings.rpy:231
    ├─→ customers/customer_affixes.json    → （不走 DataLoader，customer_affixes.rpy 自载）
    └─→ 其余 settings/*.json（清洁/宝藏/税率/事件颜色等）→ 对应 load_* 方法
```

注意两类"例外"： goals/chapter_goals.json 由 `init/settings.rpy` 自行加载（含 fallback，见 [goal.md](goal.md)）；customers/customer_affixes.json 由 `systems/customer/customer_affixes.rpy:18` 自行加载（见 [customer_affix.md](customer_affix.md)）。

## 5. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 全部编辑器 | ✅ 间接 | 编辑器产出 JSON → DataLoader 加载 → 游戏生效 |
| 开发控制台 `data_sync.py` | ✅ | JSON 格式/Schema 批量校验 |

---

## 相关文档

- [registry.md](registry.md) — DataLoader 的加载目标
- [trait_perk.md](trait_perk.md) — traits/perks JSON 的消费方
- [goal.md](goal.md) — chapter_goals.json 的独立加载路径
- [customer_affix.md](customer_affix.md) — 另一处自载 JSON 的范例
- [editor_suite.md](editor_suite.md) — 编辑器与 DataLoader 的 JSON 契约
