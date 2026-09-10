# BK Evolution 系统架构文档

本文档目录涵盖 BK Evolution 分支中所有核心系统的架构说明。

> **提示**：`game/core/framework/classes.rpy` 与 `functions.rpy` 已拆分为多个小文件。下表中“核心文件”列已更新为当前实际文件；若在其他文档中仍看到旧文件名，请以本文档和 [`DATA_MIGRATION.md`](../DATA_MIGRATION.md) 为准。

---

## 文档清单

| 文档 | 系统 | 核心文件 | 编辑支持 |
|------|------|---------|---------|
| [gamemode.md](gamemode.md) | GameMode / GameModeRegistry | `game/core/systems/gamemodes/gamemode.rpy` | ✅ 剧本编辑器 |
| [goal.md](goal.md) | Goal / 章节目标 | `game/core/framework/core_entities.rpy`, `init/settings.rpy`, `data/goals/chapter_goals.json` | ✅ 开发控制台 |
| [event.md](event.md) | StoryEvent / EventEngine / EventRegistry | `game/core/framework/core_entities.rpy`, `systems/events/event_engine.rpy`, `init/start.rpy` | ✅ 剧本编辑器 |
| [customer_affix.md](customer_affix.md) | Customer / CustomerAffixes / PreferenceMatrix | `game/core/systems/customer/customer_affixes.rpy`, `framework/core_entities.rpy` | ✅ 数据同步 |
| [trait_perk.md](trait_perk.md) | Trait / Perk / Effect | `game/core/framework/character.rpy`, `systems/registry/*.rpy` | ✅ 女孩系统编辑器 |
| [girl_pack.md](girl_pack.md) | Girl Pack 系统 | `game/core/framework/girlclass.rpy`, `game/custom/girls/` | ✅ 女孩包编辑器 |
| [editor_suite.md](editor_suite.md) | 编辑器套件 (三分架构) | `tools/bk_editor/` | — |
| [data_loader.md](data_loader.md) | DataLoader (JSON 加载) | `game/core/systems/data_loader.rpy` | ✅ 数据同步 |
| [registry.md](registry.md) | Registry 注册中心 | `game/core/systems/registry/*.rpy` | 全部编辑器 |
| — | MC Challenges | `game/core/data/challenges/challenges.json` | ✅ 开发控制台 |
| — | Resources | `game/core/data/resources/resources.json` | ✅ 开发控制台 |
| — | Contract Templates | `game/core/data/contracts/contracts.json` | ✅ 开发控制台 |
| — | Cleanliness Penalties | `game/core/data/settings/cleanliness_penalties.json` | ✅ 开发控制台 |
| — | Treasure Thresholds | `game/core/data/settings/treasure_thresholds.json` | ✅ 开发控制台 |

---

## 文档规范

每篇架构文档包含四个固定章节：

1. **系统职责** — 该系统解决什么问题、提供哪些核心能力。
2. **解耦方式** — 如何与上下游系统保持低耦合。
3. **系统间联系** — 数据流/调用链图示，说明与其他系统的交互关系。
4. **编辑器支持** — 该系统在可视化编辑器中的支持情况（完整/部分/计划/无）。

---

## 相关文档

- [PROJECT_GUIDE.md](../PROJECT_GUIDE.md) — 目录规范与数据驱动架构（当前唯一活跃指南）
- [BK_EVOLUTION_ROADMAP.md](../BK_EVOLUTION_ROADMAP.md) — 总体计划与进度
- [DATA_MIGRATION.md](../DATA_MIGRATION.md) — 硬编码数据 → JSON 迁移完整清单
- [I18N_BEST_PRACTICES.md](../I18N_BEST_PRACTICES.md) — i18n 编码最佳实践
