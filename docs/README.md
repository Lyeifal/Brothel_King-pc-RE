# Brothel King — 文档中心

> 最后更新: 2026-09-11（与代码核对）
> 分支: `bk-evolution`（Brothel King Evolution / Ren'Py 8.2.0）

本目录是 BK Evolution 项目的**唯一活跃文档库**。所有文档以当前代码为准；旧文档快照统一存放在 [archive/](archive/)，内容已过时，**请勿引用**。

**English version**: 全套文档的英文版在与本目录同级的 `docs_EN/` 下，结构完全镜像（仅 progress 文档的提交信息保留中文原文）。

---

## 按角色导航

### 🎮 玩家

游戏说明与常见问题不在 `docs/` 内，位于项目根目录：

- [`../README.html`](../README.html) — 项目介绍（HTML）
- [`../faq.txt`](../faq.txt) — 常见问题

### 🧩 Mod 作者

| 文档 | 说明 |
|------|------|
| [modding/CUSTOM_DIRECTORIES.md](modding/CUSTOM_DIRECTORIES.md) | `game/custom/` 与 `game/core/` 的目录边界：女孩包放 `custom/girls/`，社区 Mod 放 `custom/mods/` |
| [architecture/girl_pack.md](architecture/girl_pack.md) | 女孩包系统架构（`_BK.ini` 格式、加载流程） |
| [architecture/event.md](architecture/event.md) | StoryEvent / EventEngine 事件系统架构 |
| [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md) | 数据驱动架构与 JSON 数据规范（Mod 数据扩展必读） |
| [`../tools/bk_editor/README.md`](../tools/bk_editor/README.md) | 编辑器套件使用说明（女孩包 / 剧本 / 数据编辑） |

Mod 接口现状：v1 `Mod()`（`game/core/framework/challenges.rpy`）与 v2 `ModAPIV2`（`game/core/systems/mods/mod_api_v2.rpy`，16 个钩子点已接线）并存，v2 模板见 `game/core/templates/mod_template/`，范例 Mod 见 `game/custom/mods/Auction House/`。

### 🌐 译者

| 文档 | 说明 |
|------|------|
| [i18n/I18N_ROADMAP.md](i18n/I18N_ROADMAP.md) | i18n 工作唯一活跃参考：当前状态、`_i18n` 后缀约定、路线图 |
| [i18n/BEST_PRACTICES.md](i18n/BEST_PRACTICES.md) | i18n 编码规范（`__()` / `_()` 包裹规则、占位符约束） |
| [i18n/TRANSLATION_STATUS.md](i18n/TRANSLATION_STATUS.md) | 中文翻译补完计划与覆盖率快照（2026-06，部分数字已被后续机翻刷新） |
| [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md) §翻译工作流 | 标准翻译流程（extract → xlsx → 回填 → lint） |

### 🏗️ 核心开发者

| 文档 | 说明 |
|------|------|
| [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md) | **项目唯一活跃指南**：目录标准、Init 优先级链、服务容器、数据驱动架构 |
| [project/ROADMAP.md](project/ROADMAP.md) | 总览路线图：已完成 / 进行中 / 遗留待办 / 未来方向 |
| [project/REFACTORING_PROGRESS.md](project/REFACTORING_PROGRESS.md) | 重构进度真源：逐提交链（基线 `b09f55e` 之后 60+ 次提交）、组件迁移明细 |
| [architecture/README.md](architecture/README.md) | 子系统架构文档索引（DataLoader、事件、女孩包、注册表等） |
| [migration/DATA_MIGRATION.md](migration/DATA_MIGRATION.md) | 硬编码 → JSON 数据迁移完整清单 |

### 🛠️ 工具使用者

| 文档 | 说明 |
|------|------|
| [architecture/editor_suite.md](architecture/editor_suite.md) | 编辑器套件（三分架构）设计与数据文件映射 |
| [`../tools/bk_editor/README.md`](../tools/bk_editor/README.md) | 编辑器套件（tkinter GUI）使用说明 |
| [`../tools/bk_editor/AGENTS.md`](../tools/bk_editor/AGENTS.md) | 编辑器开发约定（给维护编辑器代码的人） |

`tools/` 下还有大量翻译/审计脚本（`audit_placeholders.py`、`export_empty_to_xlsx.py`、`i18n_lint.py`、`verify_mod_api.py` 等），用法见 [i18n/I18N_ROADMAP.md](i18n/I18N_ROADMAP.md) 与 [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md)。

---

## 全量文档索引

### 项目层（project/）

| 文档 | 说明 |
|------|------|
| [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md) | 项目指南：目录标准、核心文件速查、Init 链、服务访问、数据驱动架构、编辑器套件、命名规范、缓存卫生 |
| [project/ROADMAP.md](project/ROADMAP.md) | 总览路线图（合并自两份旧路线图，以当前代码核对刷新） |
| [project/REFACTORING_PROGRESS.md](project/REFACTORING_PROGRESS.md) | 重构进度真源：Phase 0–6 逐提交链、Girl 组件迁移明细、屏幕提取记录 |

### 架构层（architecture/）

| 文档 | 说明 |
|------|------|
| [architecture/README.md](architecture/README.md) | 架构文档索引与核心文件对照表 |
| [architecture/data_loader.md](architecture/data_loader.md) | DataLoader：JSON 加载、fallback 模式、各 load_* 方法 |
| [architecture/registry.md](architecture/registry.md) | Registry 层：Trait/Perk/Tag/Dialogue/Event/NGP/Meta/Unlock 注册表 |
| [architecture/event.md](architecture/event.md) | StoryEvent / EventEngine / EventRegistry 事件系统 |
| [architecture/gamemode.md](architecture/gamemode.md) | GameMode / GameModeRegistry（story / sandbox / scenario） |
| [architecture/girl_pack.md](architecture/girl_pack.md) | 女孩包系统：`_BK.ini`、图片标签、加载与验证 |
| [architecture/goal.md](architecture/goal.md) | Goal / 章节目标系统 |
| [architecture/trait_perk.md](architecture/trait_perk.md) | Trait / Perk / Effect 体系 |
| [architecture/customer_affix.md](architecture/customer_affix.md) | Customer / CustomerAffixes / PreferenceMatrix |
| [architecture/editor_suite.md](architecture/editor_suite.md) | 编辑器套件三分架构（girl_pack / scenario / dev_console） |

### 国际化（i18n/）

| 文档 | 说明 |
|------|------|
| [i18n/I18N_ROADMAP.md](i18n/I18N_ROADMAP.md) | i18n 唯一活跃参考：状态、`_i18n` 约定、工具链 |
| [i18n/BEST_PRACTICES.md](i18n/BEST_PRACTICES.md) | i18n 编码最佳实践 |
| [i18n/TRANSLATION_STATUS.md](i18n/TRANSLATION_STATUS.md) | 中文翻译补完计划（2026-06 快照） |

### Modding（modding/）

| 文档 | 说明 |
|------|------|
| [modding/CUSTOM_DIRECTORIES.md](modding/CUSTOM_DIRECTORIES.md) | `game/custom/` 与 `game/core/` 目录边界说明 |

### 迁移（migration/）

| 文档 | 说明 |
|------|------|
| [migration/DATA_MIGRATION.md](migration/DATA_MIGRATION.md) | 硬编码数据 → JSON 迁移清单（源文件、目标路径、状态） |

### 工具（tools/）

> 该目录目前为空，预留用于工具脚本文档。编辑器套件文档见 [`../tools/bk_editor/README.md`](../tools/bk_editor/README.md)。

### 存档（archive/）— ⚠️ 内容过时，勿引用

| 条目 | 说明 |
|------|------|
| [archive/pre-reorg-2026-09/](archive/pre-reorg-2026-09/) | 2026-09 文档重整前的旧文档快照（旧 PROJECT_GUIDE / ROADMAP / BK_EVOLUTION_ROADMAP / I18N 系列等），仅作历史参考 |
| [archive/PROJECT_GUIDE_V3.md](archive/PROJECT_GUIDE_V3.md) | 更早一版项目指南（Phase 6 时期） |
| [archive/I18N_PLAN.md](archive/I18N_PLAN.md)、[archive/I18N_REFACTOR_PLAN.md](archive/I18N_REFACTOR_PLAN.md)、[archive/i18n_progress.md](archive/i18n_progress.md) | 旧 i18n 计划与进度（内容已整合进 [i18n/I18N_ROADMAP.md](i18n/I18N_ROADMAP.md)） |

---

## 相关文档

- [project/PROJECT_GUIDE.md](project/PROJECT_GUIDE.md) — 项目指南（建议先读）
- [project/ROADMAP.md](project/ROADMAP.md) — 总览路线图
- [project/REFACTORING_PROGRESS.md](project/REFACTORING_PROGRESS.md) — 重构进度真源
