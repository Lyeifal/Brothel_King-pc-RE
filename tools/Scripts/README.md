# Scripts — 工具脚本集合

本目录包含 Brothel King 项目的各类辅助脚本，按功能分为子目录。

## 目录结构

```
Scripts/
├── bk_evolution/     # BK Evolution 数据驱动工具
├── checks/           # 代码检查与修复
│   └── fix/          # 自动修复脚本
├── marking/          # 源代码标记/重构
├── misc/             # 杂项
└── translation/      # 翻译工作流
    └── docx/         # docx 格式转换
```

## 子目录说明

### `bk_evolution/` — BK Evolution 数据工具

| 脚本 | 说明 |
|------|------|
| `export_hardcoded.py` | 将 `.rpy` 中的硬编码 Trait/Perk 定义导出为 JSON |

### `translation/` — 翻译工作流

| 脚本 | 说明 |
|------|------|
| `find_untranslated.py` | 查找未翻译内容并生成 `to_translate_remaining.xlsx` |
| `export_translation_xlsx.py` | 导出全部待翻译内容到 xlsx |
| `import_translated_xlsx.py` | 导入主翻译文件 |
| `import_translated_remaining.py` | 导入补翻文件 |
| `fix_placeholders.py` | 检查并修复 `%s/%d` 占位符 |
| `verify_strings.py` | 验证 `strings.rpy` 语法和占位符数量 |
| `merge_translations.py` | 扫描 `__()`/`_()` 调用，重新生成 `strings.rpy` |
| `merge_tl_strings.py` | 合并剧情文件中的 `strings:` 块到 `strings.rpy` |
| `wrap_dialogue.py` | 给 `BKdialogue.rpy` 的 `add_dialogue()` 包裹 `__()` |
| `restore_lost.py` | 从 git 历史恢复丢失的翻译 |
| `batch_translate_dialogue.py` | Google Translate 批量翻译（带占位符保护） |
| `export_translation_docx.py` | 导出翻译到 docx 格式 |
| `extract_translations.py` | 从源代码提取字符串生成模板 |
| `import_translation.py` | 导入 txt 格式翻译到 `strings.rpy` |
| `export_for_translation.py` | 导出待翻译内容为 txt |
| `docx/convert_docx.py` | docx/txt 双向转换 |

### `checks/` — 代码检查

| 脚本 | 说明 |
|------|------|
| `check_broken_strings.py` | 检查损坏的字符串 |
| `check_errors.py` | 检查常见错误 |
| `check_file.py` | 文件级检查 |
| `check_import.py` | 导入检查 |
| `check_init_vars.py` | init 变量检查 |
| `check_line.py` | 行级检查 |
| `check_bare_fonts.py` | 字体检查 |
| `check_fonts.py` | 字体相关检查 |

### `checks/fix/` — 自动修复

| 脚本 | 说明 |
|------|------|
| `fix_all_variables.py` | 修复被误翻译的 `[variable]` 变量名 |
| `fix_broken_strings.py` | 修复损坏的字符串 |
| `fix_corruption.py` | 修复文件损坏 |
| `fix_fonts.py` | 修复字体问题 |
| `fix_gui_paths.py` | 修复 GUI 路径 |

### `marking/` — 源代码标记/重构

| 脚本 | 说明 |
|------|------|
| `mark_characters.py` | 标记角色相关文本 |
| `mark_dict_values.py` | 标记字典值 |
| `mark_init_vars.py` | 标记 init 变量 |
| `mark_kwargs.py` | 标记 kwargs |
| `mark_lists.py` | 标记列表 |
| `mark_menus.py` | 标记菜单文本 |
| `mark_translations.py` | 给字符串包裹 `__()` |
| `refactor_move.py` | 重构移动 |
| `refactor_verify.py` | 重构验证 |
| `split_menu_if.py` | 拆分 menu if 语句 |

### `misc/` — 杂项

| 文件 | 说明 |
|------|------|
| `_scan_concat.py` | 扫描拼接报告 |
| `find_context.py` | 查找上下文 |

## 运行方式

所有脚本已配置自动检测项目根目录，**从任意位置均可运行**：

```powershell
# 从项目根目录运行
cd C:\Users\akxls\Documents\Code\BK\Brothel_King-pc
python tools/Scripts/translation/find_untranslated.py

# 从 Scripts 子目录运行
cd tools/Scripts/translation
python find_untranslated.py
```
