# BK Evolution 文档中心

欢迎来到 BK Evolution 的文档目录。本文档中心旨在让开发者、Mod 作者和翻译贡献者快速找到所需信息。

---

## 阅读顺序

| 读者 | 推荐阅读顺序 |
|------|-------------|
| **新加入的开发者** | [`PROJECT_GUIDE.md`](PROJECT_GUIDE.md) → [`DATA_MIGRATION.md`](DATA_MIGRATION.md) → [`architecture/README.md`](architecture/README.md) |
| **Mod / 女孩包作者** | [`CUSTOM_DIRECTORY_GUIDE.md`](CUSTOM_DIRECTORY_GUIDE.md) → [`architecture/girl_pack.md`](architecture/girl_pack.md) → [`architecture/editor_suite.md`](architecture/editor_suite.md) |
| **翻译贡献者** | [`I18N_BEST_PRACTICES.md`](I18N_BEST_PRACTICES.md) → [`I18N_ROADMAP.md`](I18N_ROADMAP.md) → [`TRANSLATION_COMPLETION_PLAN.md`](TRANSLATION_COMPLETION_PLAN.md) |
| **项目管理者** | [`ROADMAP.md`](ROADMAP.md) → [`BK_EVOLUTION_ROADMAP.md`](BK_EVOLUTION_ROADMAP.md) → [`DATA_MIGRATION.md`](DATA_MIGRATION.md) |

---

## 文档地图

### 项目级指南

| 文档 | 说明 | 状态 |
|------|------|------|
| [`PROJECT_GUIDE.md`](PROJECT_GUIDE.md) | **当前唯一活跃的项目指南**：目录结构、`game/core/` 规范、数据驱动架构、翻译工作流、编辑器套件 | ✅ 活跃 |
| [`CUSTOM_DIRECTORY_GUIDE.md`](CUSTOM_DIRECTORY_GUIDE.md) | `game/core/` 与 `game/custom/` 的边界说明，Mod/女孩包放置规范 | ✅ 活跃 |
| [`ROADMAP.md`](ROADMAP.md) | BK Evolution 高阶段总览路线图（Phase A-I） | ✅ 活跃 |
| [`BK_EVOLUTION_ROADMAP.md`](BK_EVOLUTION_ROADMAP.md) | 编辑器工具链与数据迁移专项路线图 | ✅ 活跃 |

### 数据与 i18n

| 文档 | 说明 | 状态 |
|------|------|------|
| [`DATA_MIGRATION.md`](DATA_MIGRATION.md) | 硬编码数据 → JSON 迁移的权威清单（105+ 文件） | ✅ 活跃 |
| [`I18N_ROADMAP.md`](I18N_ROADMAP.md) | i18n 当前状态、路线图与标准工作流 | ✅ 活跃 |
| [`I18N_BEST_PRACTICES.md`](I18N_BEST_PRACTICES.md) | `__()` / `_()`、`_i18n` 后缀、JSON i18n、占位符保护等编码规范 | ✅ 活跃 |
| [`TRANSLATION_COMPLETION_PLAN.md`](TRANSLATION_COMPLETION_PLAN.md) | 中文翻译补完记录与具体工作流 | ✅ 活跃 |

### 系统架构

详见 [`architecture/README.md`](architecture/README.md)。

| 文档 | 系统 |
|------|------|
| [`architecture/gamemode.md`](architecture/gamemode.md) | GameMode / GameModeRegistry |
| [`architecture/goal.md`](architecture/goal.md) | Goal / 章节目标 |
| [`architecture/event.md`](architecture/event.md) | StoryEvent / EventEngine / EventRegistry |
| [`architecture/customer_affix.md`](architecture/customer_affix.md) | Customer / CustomerAffixes |
| [`architecture/trait_perk.md`](architecture/trait_perk.md) | Trait / Perk / Effect |
| [`architecture/girl_pack.md`](architecture/girl_pack.md) | Girl Pack 系统 |
| [`architecture/editor_suite.md`](architecture/editor_suite.md) | 编辑器套件架构 |
| [`architecture/data_loader.md`](architecture/data_loader.md) | DataLoader（JSON 加载） |
| [`architecture/registry.md`](architecture/registry.md) | Registry 注册中心 |

### 审计与历史归档

| 文档 | 说明 |
|------|------|
| [`DOC_AUDIT.md`](DOC_AUDIT.md) | 本次文档整合前的差异审计清单 |
| [`archive/PROJECT_GUIDE_V3.md`](archive/PROJECT_GUIDE_V3.md) | Phase 6 项目指南（历史） |
| [`archive/i18n_progress.md`](archive/i18n_progress.md) | 旧版 i18n 进度记录（历史） |
| [`archive/I18N_PLAN.md`](archive/I18N_PLAN.md) | 原 JSON i18n 迁移计划（历史） |
| [`archive/I18N_REFACTOR_PLAN.md`](archive/I18N_REFACTOR_PLAN.md) | 原 9 阶段 i18n 重构计划（历史） |

---

## 文档维护规范

1. **单一活跃入口**：项目级指南以 `PROJECT_GUIDE.md` 为准；i18n 以 `I18N_ROADMAP.md` + `I18N_BEST_PRACTICES.md` 为准。
2. **历史版本归档**：过时或版本化的文档统一放入 `archive/`，并在顶部注明“历史版本，不再维护”。
3. **路径准确性**：引用代码文件时使用当前 `game/core/` 下的真实路径；`classes.rpy` / `functions.rpy` 等已拆分的旧文件名不得再出现。
4. **状态标签**：使用统一的状态emoji：✅ 已完成 / 🚧 进行中 / ⏳ 待开始 / ❌ 未支持。
5. **交叉链接**：活跃文档之间应相互引用，避免信息孤岛；引用归档文档时需明确标注为历史版本。

---

## 快速命令参考

```powershell
# 运行 lint
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . lint

# 统计翻译
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . translate --count chinese_simplified

# 导出空翻译
python tools/export_empty_to_xlsx.py

# 导入翻译
python tools/import_translated_empty.py

# i18n 审计
python tools/i18n_lint.py
python tools/verify_i18n.py
python tools/audit_placeholders.py

# 启动编辑器
python tools/bk_editor.py
```
