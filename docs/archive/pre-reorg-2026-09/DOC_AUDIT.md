# 文档-代码差异审计

> 审计日期：2026-06-20  
> 范围：`docs/` 下全部 Markdown 文件  
> 目的：找出与当前项目代码不一致、重复或已过时的描述，为文档整合提供依据。

## 1. 全局问题分类

| # | 问题类型 | 影响 | 涉及文档 |
|---|----------|------|----------|
| 1 | 引用旧版 `BK*.rpy` 根文件 | 高 | `PROJECT_GUIDE.md`, `i18n_progress.md` |
| 2 | 引用已拆分的 `classes.rpy` / `functions.rpy` 单体文件 | 高 | `PROJECT_GUIDE_V3.md`, `architecture/*.md` |
| 3 | 架构文档状态与 `DATA_MIGRATION.md`/`ROADMAP.md` 矛盾 | 高 | `architecture/README.md`, `architecture/goal.md`, `architecture/event.md`, `architecture/gamemode.md`, `architecture/editor_suite.md` |
| 4 | i18n 文档间完成度/工具存在性不一致 | 高 | `I18N_PLAN.md`, `I18N_REFACTOR_PLAN.md`, `I18N_BEST_PRACTICES.md`, `i18n_progress.md`, `TRANSLATION_COMPLETION_PLAN.md` |
| 5 | 数据路径命名不统一 | 中 | `CUSTOM_DIRECTORY_GUIDE.md`, `architecture/event.md`, `DATA_MIGRATION.md` |
| 6 | 版本化项目指南重叠 | 中 | `PROJECT_GUIDE.md`, `PROJECT_GUIDE_V3.md`, `PROJECT_GUIDE_V4.md` |
| 7 | 社区 Mod 路径不一致 | 中 | `BK_EVOLUTION_ROADMAP.md`, `ROADMAP.md`, `CUSTOM_DIRECTORY_GUIDE.md`, `architecture/girl_pack.md` |

---

## 2. 具体差异清单

### 2.1 旧版 `BK*.rpy` 文件引用

当前项目已将根目录 `BK*.rpy` 重构到 `game/core/` 下。以下文档仍按旧文件名描述项目结构：

| 文档 | 旧引用示例 | 代码实际 |
|------|-----------|----------|
| `PROJECT_GUIDE.md:47-76` | `BKmain.rpy`, `BKscreens.rpy`, `BKstart.rpy`, `BKgirlclass.rpy`, `BKclasses.rpy`, `BKfunctions.rpy` ... | `game/core/content/main.rpy`, `game/core/ui/screens.rpy`, `game/core/content/intro.rpy`, `game/core/framework/girlclass.rpy`, `game/core/framework/character.rpy`, `game/core/framework/utils.rpy` 等 |
| `i18n_progress.md:25-181` | 多次出现 `BKchapter1.rpy`, `BKclasses.rpy`, `BKfunctions.rpy`, `BKscreens.rpy` 等 | 对应内容已迁移到 `game/core/content/main_story/`, `game/core/framework/`, `game/core/ui/` 等 |

**建议**：`PROJECT_GUIDE.md` 按 `game/core/` 的 7 大目录重新梳理；`i18n_progress.md` 归档为历史记录，不再作为活跃参考。

### 2.2 已拆分的单体文件引用

`game/core/framework/classes.rpy`、`functions.rpy` 已拆分为多个小文件，但以下文档仍引用旧路径：

| 文档 | 旧引用 | 代码实际 |
|------|--------|----------|
| `PROJECT_GUIDE_V3.md:180, 197, 216, 376, 379, 440, 444` | `framework/classes.rpy`, `framework/functions.rpy` | `framework/character.rpy`, `framework/core_entities.rpy`, `framework/utils.rpy`, `framework/economy.rpy`, `framework/girlclass.rpy` 等 |
| `architecture/README.md:12-15` | `classes.rpy` | `character.rpy`, `core_entities.rpy`, `girlclass.rpy` 等 |
| `architecture/event.md:3` | `framework/classes.rpy` (StoryEvent) | `framework/core_entities.rpy` / `systems/events/event_engine.rpy` |
| `architecture/customer_affix.md:3,34-37` | `framework/classes.rpy` (Customer) | `systems/customer/customer_affixes.rpy` / `framework/core_entities.rpy` |
| `architecture/goal.md:3` | `framework/classes.rpy` (Goal) | `framework/core_entities.rpy` |
| `architecture/trait_perk.md:3` | `framework/classes.rpy` (Trait, Perk) | `framework/character.rpy` |
| `architecture/gamemode.md:4` | `framework/classes.rpy` (Game) | `framework/game_systems.rpy` / `framework/core_entities.rpy` |
| `architecture/girl_pack.md:3` | `BKgirlclass.rpy` | `framework/girlclass.rpy` |
| `DATA_MIGRATION.md:44-45,118-119,142` | `framework/functions.rpy` | 已拆分；相关数据文件路径正确，但源文件描述需更新为对应模块 |

**建议**：在所有架构文档中统一使用拆分后的真实文件名，并在 `architecture/README.md` 顶部增加“单体文件已拆分”提示。

### 2.3 架构完成状态矛盾

`ROADMAP.md` 与 `DATA_MIGRATION.md` 已将大量系统标记完成，但 `architecture/` 子文档仍显示为“计划中”或部分支持：

| 系统 | 文档状态 | 权威状态（`DATA_MIGRATION.md` / `ROADMAP.md`） |
|------|----------|-----------------------------------------------|
| Goal | `architecture/README.md`: 计划中 | `DATA_MIGRATION.md`: Goals 已迁移 ✅ |
| StoryEvent / EventEngine | `architecture/README.md`: ✅ 剧本编辑器；`event.md`: 69 事件已导出 | `BK_EVOLUTION_ROADMAP.md`: StoryEvent 批量导出仍“待继续”；需以代码为准 |
| CustomerAffix | `architecture/README.md`: 暂无 | `DATA_MIGRATION.md`: customer_affixes 已迁移 ✅ |
| GameMode / Scenario | `architecture/gamemode.md`: scenario 编辑“计划”；`editor_suite.md`: scenario_editor 部分 | `ROADMAP.md`: Phase F 100% 完成 |
| Resources / Contracts / Cleanliness / Treasure / MC Challenges | `architecture/README.md`: 计划中 | `DATA_MIGRATION.md` / `ROADMAP.md`: 多项已迁移 ✅ |

**建议**：以 `DATA_MIGRATION.md` 和当前代码为基准，统一刷新 `architecture/README.md` 中的支持矩阵和各子文档的完成状态。

### 2.4 i18n 文档不一致

| 问题 | 涉及文档 | 说明 |
|------|----------|------|
| 完成阶段冲突 | `I18N_PLAN.md`: Phase 5 待开始 | `ROADMAP.md`: Phase H 100% 完成；`TRANSLATION_COMPLETION_PLAN.md`: 翻译覆盖率 >99.9% |
| 工具存在性冲突 | `I18N_BEST_PRACTICES.md:254-297` 把 `i18n_lint.py`、`verify_i18n.py` 当作已有工具引用 | `I18N_REFACTOR_PLAN.md:139-500` 把它们列为“待创建” |
| 覆盖率数据冲突 | `i18n_progress.md` 给出旧版按 `BK*.rpy` 的统计 | `TRANSLATION_COMPLETION_PLAN.md` 给出 29,367 对话块、99.91% 覆盖率 |
| 工作流路径 | `TRANSLATION_COMPLETION_PLAN.md` 已更新到 `temp/translations/` | `I18N_REFACTOR_PLAN.md` 仍写 `to_translate_phase1.xlsx`（虽已改为 `temp/translations/`，但其他 i18n 文档未同步） |

**建议**：
- 将 `i18n_progress.md` 归档。
- 合并 `I18N_PLAN.md` + `I18N_REFACTOR_PLAN.md` 为 `I18N_ROADMAP.md`，删除旧文件。
- 在 `I18N_BEST_PRACTICES.md` 中核实 `i18n_lint.py`/`verify_i18n.py` 实际存在性并给出正确用法；若不存在则标记为待实现。
- 以 `TRANSLATION_COMPLETION_PLAN.md` 为唯一的当前翻译进度/工作流文档。

### 2.5 数据路径命名不统一

| 数据 | `CUSTOM_DIRECTORY_GUIDE.md` / 其他 | `DATA_MIGRATION.md` / 代码实际 |
|------|-------------------------------------|-------------------------------|
| StoryEvent JSON | `game/core/data/events/event_dict.json` (`event.md`) | `game/core/data/story_events/story_events.json` |
| Sandbox origins | `data/origins/origins.json` (`data_loader.md`) | `data/sandbox/origins.json` |
| Sandbox events | `data/sandbox/sandbox_events.json` (`data_loader.md`) | `data/sandbox/events.json` |

**建议**：统一使用代码中的实际路径；在 `DATA_MIGRATION.md` 已有正确路径，其他文档向它看齐。

### 2.6 社区 Mod / Girl Pack 路径不一致

| 文档 | 描述 | 代码实际 |
|------|------|----------|
| `BK_EVOLUTION_ROADMAP.md:15`, `ROADMAP.md:30` | 社区 Mod 统一放在 `game/custom/mods/` | 当前项目使用 `game/custom/girls/` 存放自定义女孩包；`game/custom/mods/` 未见主要使用 |
| `CUSTOM_DIRECTORY_GUIDE.md:141-189` | 详细说明 `custom/mods/` 结构 | 同上 |
| `architecture/girl_pack.md:3,4,19,29,36` | 官方 `game/MG/`，社区 `game/custom/mods/` | 实际为 `game/custom/girls/`（见根目录 `custom/girls/`） |

**建议**：以代码实际目录 `game/custom/girls/` 为准，统一所有 Mod/Girl Pack 路径描述；若 `game/custom/mods/` 确实保留，则说明两者区别。

### 2.7 版本化项目指南重叠

- `PROJECT_GUIDE.md`（旧版根目录结构，`BK*.rpy`）
- `PROJECT_GUIDE_V3.md`（Phase 6，Registry/ModAPI/EventEngine，仍引用 `classes.rpy`/`functions.rpy`）
- `PROJECT_GUIDE_V4.md`（最新 `game/core/` 7 目录标准、DataLoader/`from_dict`）

**建议**：以 V4 为基准重写 `PROJECT_GUIDE.md`，将 V3 归档，V4 改为重定向到新版 `PROJECT_GUIDE.md`。

---

## 3. 建议的整合优先级

1. **P0（阻塞）**：修正 `BK*.rpy`、`classes.rpy`、`functions.rpy` 等错误路径；统一 Mod/Girl Pack 路径。
2. **P1（高）**：统一架构完成状态；合并版本化项目指南；整合 i18n 文档。
3. **P2（中）**：统一数据 JSON 路径；修复内部 Markdown 链接；统一格式与状态标签。
4. **P3（低）**：归档 `i18n_progress.md` 等历史文档；补充 `docs/README.md` 文档地图。
