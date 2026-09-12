# BK Evolution — tools/ 工具清单

> 最后更新: 2026-09-11（与代码核对）
>
> 本文档盘点 `tools/` 目录下全部 35 个 Python 脚本及子目录，按用途分类。
> 标注 **历史** 的脚本为一次性迁移/修复所用，多数含硬编码绝对路径（`C:\Users\akxls\...`），**不可直接复用**，仅作历史记录。
> 标注 ⚠️ 的脚本含硬编码路径，运行前需先改路径。

---

## 1. 翻译工作流链（活跃）

标准工作流详见 [`../i18n/I18N_ROADMAP.md`](../i18n/I18N_ROADMAP.md) §4。核心链路：

```
translate --empty → export_empty_to_xlsx → （人工/机翻 Excel）
→ import_translated_empty → audit_placeholders → i18n_lint / verify_i18n
```

| 脚本 | 一句话说明 |
|------|-----------|
| `export_empty_to_xlsx.py` | 导出全部空翻译（`strings.rpy` 空条目 + 空 dialogue 块）到 Excel，供人工翻译 |
| `export_empty_to_xlsx_v2.py` | 同上，但只扫描 `game/tl/chinese_simplified/` 下所有 `.rpy` 的空 `new ""` 字符串块（不导 dialogue） |
| `import_translated_empty.py` | 从 Excel 导回空翻译（默认 `temp/translations/to_translate_empty.xlsx`），写回 Ren'Py 翻译文件 |
| `import_translated_remaining_v3.py` | 从 `to_translate_remaining_v3.xlsx` 导回翻译（strings / common / dialogue 三个工作表） |
| `auto_fill_nonenglish_empty.py` | 原文已是非英文（如中文硬编码）的空条目自动 `new = old` 填充，免去人工翻译 |
| `export_remaining_english.py` | 导出所有仍为英文的空翻译（strings + 各文件字符串块 + dialogue 块） |
| `batch_translate_empty.py` | 用 `deep_translator` 批量机翻 `strings.rpy` 空条目（需联网，小批次+进度输出） |
| `audit_placeholders.py` | 审计中文翻译与原文占位符一致性（`%s/%d` 与 `[var]` 插值），输出 mismatch Excel |
| `import_placeholder_fixes.py` | 把占位符修复后的 Excel 导回对应 `.rpy` 翻译文件（占位符仍不匹配的行跳过） |
| `audit_json_i18n.py` | 按 `json_i18n.rpy` 相同规则扫描 `game/core/data/**/*.json` 的 `_i18n` 字符串，检查 `strings.rpy` 缺失并输出 Excel |
| `import_json_i18n.py` | 把 JSON `_i18n` 缺失文本导入 `strings.rpy`（三引号多行、按原文去重、转义处理） |
| `import_json_i18n_translations.py` | 把 `audit_json_i18n.py` 生成的缺失 Excel 翻译导回 `strings.rpy`（复用 v3 导入逻辑） |
| `count_untranslated.py` | 快速统计 `strings.rpy` 及各翻译文件中的 `new ""` 空条目数 |
| `check_json_i18n.py` | 简易核对：建立 `strings.rpy` 原文索引并检查 JSON `_i18n` 文本收录情况 |
| `verify_i18n.py` | i18n 回归验证：依次跑 `translate --count`、`Ren'Py lint`、`i18n_lint.py` 并汇总 PASS/FAIL（路径从脚本位置自动推导） |
| `i18n_lint.py` | 静态审计 `game/core/**/*.rpy`：裸字符串、`+` 拼接、未包裹 `%` 格式化等（当前基线 17 处开发者面向文本误报，见 [`../i18n/I18N_ROADMAP.md`](../i18n/I18N_ROADMAP.md)） |
| `debug_lint.py` | i18n_lint 的调试辅助：验证 `is_translatable()` 判定逻辑 |
| `remove_orphan_translations.py` | 按 `文件.rpy:translate_id` 参数从翻译文件删除孤儿翻译块 ⚠️ 硬编码 TL_DIR |
| `audit_tl_structure.py` | 审计翻译目录结构与源目录的对应关系（孤儿翻译文件 / 缺翻译的源文件） |
| `scan_menu_options.py` | 扫描 `game/core/**/*.rpy` 中非字面量的 `menu:` 选项（变量选项需 `__()` 包裹） ⚠️ 硬编码 ROOT |
| `wrap_yes_no_strings.py` | 批量给 `call_screen("yes_no", ...)` 的裸字符串字面量包裹 `__()` ⚠️ 硬编码 GAME_DIR |
| `wrap_notify.py` | 批量给 `renpy.notify("...")` 裸字符串包裹 `__()` |
| `batch_wrap_economy.py` | 批量包裹 `economy.rpy` 中玩家可见的 `%` 格式化字符串（ttip/change_log/budget_ttip 等已知变量） |
| `fix_screens_job_tooltip.py` | 一次性修复 `screens.rpy` 顾客偏好 tooltip 的拼接字符串为 `__()` 分段包裹 ⚠️ 硬编码路径 |

## 2. Mod 验证（活跃）

| 脚本 | 一句话说明 |
|------|-----------|
| `verify_mod_api.py` | Mod API v2 验证：静态断言 19 个 `HOOK_*` 常量唯一、关键方法存在、v1 基类包装（含 `register_quality`）与 `CAPABILITIES` 含 `"items"`、模板引用有效；再模拟执行注册/重复拒绝/优先级/取消流程。纯 Python 不依赖 Ren'Py 运行时（当前全部通过，5 条命名惯例警告）。详见 [`../modding/MOD_API.md`](../modding/MOD_API.md) §4 |

## 3. 数据审计与导出

| 脚本 | 一句话说明 |
|------|-----------|
| `analyze_translation_gaps.py` | 对比旧 `_cn` 项目（`schinese`）与当前 `chinese_simplified` 翻译，分析覆盖缺口 ⚠️ 硬编码双项目路径 |
| `export_items.py` | **历史**：把 `data/items.rpy` 的物品定义导出为 JSON（items.json 迁移用） |
| `export_jobs.py` | **历史**：把 `data/jobs.rpy` 的 `perform_job_dict` 导出为 `jobs/perform_job_dict.json` |
| `export_meta_data.py` | **历史**：把硬编码的 Achievements / Difficulty / NG+ 设置导出为 JSON |
| `migrate_variables.py` | **历史**：把 `variables.rpy` 中硬编码 stats/personalities/ranks 迁移到 JSON |

## 4. 迁移历史脚本（已收官，仅供参考）

数据驱动化与翻译迁移已完成，以下脚本不再使用：

| 脚本 | 一句话说明 |
|------|-----------|
| `migrate_cn_translation.py` | **历史**：按 Ren'Py 翻译 hash 把旧 `_cn` 人工翻译迁移到当前项目（支持 speaker 标签） ⚠️ 硬编码路径 |
| `text_level_migration.py` | **历史**：按原文文本（而非 hash）匹配迁移旧翻译，覆盖代码重构导致的 hash 变化 ⚠️ 硬编码路径 |
| `split_classes.py` | **历史**：把巨型 `framework/classes.rpy` 拆分为 picture/goal/core_entities/world/character/interactions/challenges/progression 等模块（重构已完成） |
| `split_functions.py` | **历史**：把巨型 `framework/functions.rpy` 拆分为 utils/girl_factory/game_systems/economy/effects/dialogue（重构已完成） |
| `split_girlclass.py` | **历史**：从 `girlclass.rpy` 抽出 `GirlFilesDict` 为独立文件 `girl_files_dict.rpy` |

## 5. bk_editor 编辑器套件（活跃）

| 入口 | 说明 |
|------|------|
| `bk_editor.py` | 编辑器套件主入口（`python tools/bk_editor.py`），tkinter 图形界面 |
| `bk_editor/` | 套件本体：女孩包编辑器 / 剧本编辑器 / 开发控制台 + `shared/` 共享库 |

三个编辑器：**女孩包编辑器**（Mod 作者：图片打标、`_BK.ini`、Trait/Perk、包验证）、**剧本编辑器**（剧情作者：StoryEvent CRUD、剧本管理）、**开发控制台**（核心开发者：成就/难度/NG+/Meta 的 JSON 编辑）。

详细文档：[`bk_editor/README.md`](../../tools/bk_editor/README.md)（架构与数据文件映射）、[`bk_editor/AGENTS.md`](../../tools/bk_editor/AGENTS.md)（AI Agent 编码约定）。与 `game/core/data/` 的对应关系另见 [`../modding/CUSTOM_DIRECTORIES.md`](../modding/CUSTOM_DIRECTORIES.md)。

## 6. 其他子目录

| 目录 | 说明 |
|------|------|
| `tools/Scripts/` | 更早期的 PowerShell/Python 辅助脚本（translation/、checks/、bk_evolution/ 等），多已被根目录工具取代，属历史资产；其 `README.md` 有原始说明 |
| `tools/archive/` | 历次翻译导出 Excel 与报告存档（`to_translate*.xlsx`、`reports/`），纯归档 |

## 使用建议

- **日常翻译补翻**：只用第 1 节的活跃脚本，按 `I18N_ROADMAP.md` §4 工作流执行。
- **新增/修改 Mod API**：跑 `python tools/verify_mod_api.py` 做回归。
- **改 JSON 数据结构**：按 `tools/bk_editor/AGENTS.md` "修改 JSON 数据结构" 清单（DataLoader + DataExporter + Schema + 编辑器表单 + fallback）。
- **历史脚本**：不要直接运行（硬编码路径已失效）；如需类似功能，复制后改路径。

---

## 相关文档

- [`../i18n/I18N_ROADMAP.md`](../i18n/I18N_ROADMAP.md) — i18n 状态与标准翻译工作流
- [`../i18n/BEST_PRACTICES.md`](../i18n/BEST_PRACTICES.md) — 编码规范（`__()`/`_()`、`_i18n` 后缀、占位符）
- [`../modding/MOD_API.md`](../modding/MOD_API.md) — Mod 机制与 `verify_mod_api.py`
- [`../modding/CUSTOM_DIRECTORIES.md`](../modding/CUSTOM_DIRECTORIES.md) — 编辑器与数据目录对应关系
- [`../migration/DATA_MIGRATION.md`](../migration/DATA_MIGRATION.md) — 数据迁移记录（历史脚本背景）
