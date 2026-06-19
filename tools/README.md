# Brothel King 工具说明

本文档说明 `tools/` 目录下的工具及其使用方法。

## 目录结构

```
tools/
├── bk_editor.py              # BK Evolution 编辑器主入口
├── bk_editor/                # 编辑器包（剧情/出身/女孩/剧本/女孩包）
├── Scripts/                  # 工具脚本集合
│   ├── translation/          # 翻译工作流脚本
│   ├── checks/               # 代码检查脚本
│   ├── marking/              # 源代码标记/重构脚本
│   ├── bk_evolution/         # BK Evolution 数据工具
│   └── misc/                 # 杂项脚本
└── README.md                 # 本文件
```

所有脚本已配置自动检测项目根目录，**从项目根目录或 Scripts 子目录均可运行**：

```powershell
# 方式一：从项目根目录运行
cd C:\Users\akxls\Documents\Code\BK\Brothel_King-pc
python tools/Scripts/translation/find_untranslated.py

# 方式二：直接从 Scripts 子目录运行
cd C:\Users\akxls\Documents\Code\BK\Brothel_King-pc\tools\Scripts\translation
python find_untranslated.py
```

---

## 清理编译缓存

修改 `.rpy` 脚本后，Ren'Py 会自动重新编译生成 `.rpyc` 文件。但如果之前编译出错或缓存异常，可能需要手动清理缓存以确保使用最新代码。

### Windows PowerShell

```powershell
# 删除编译缓存文件夹
Remove-Item -Recurse -Path game\cache

# 删除所有 rpyc 文件
Remove-Item -Path game\*.rpyc
Remove-Item -Path game\**\*.rpyc -Recurse
```

### 一键清理脚本

```powershell
Remove-Item -Recurse -Path game\cache; Remove-Item -Path game\*.rpyc; Remove-Item -Path game\**\*.rpyc -Recurse
```

删除后下次启动会稍慢（需要重新编译所有脚本），但能确保运行的是最新的 `.rpy` 代码。

---

## 核心工作流

### 1. 查找未翻译内容

```bash
python tools/Scripts/translation/find_untranslated.py
```

- 扫描 `strings.rpy` 和剧情翻译文件
- 输出统计信息
- 生成 `to_translate_remaining.xlsx`

### 2. 导出完整待翻译文件（可选）

```bash
python tools/Scripts/translation/export_translation_xlsx.py
```

这会生成 `to_translate.xlsx`，包含全部 `strings.rpy` 条目和所有剧情对话。

### 3. 翻译

使用 Google Translate、DeepL 或手动翻译生成的 xlsx 文件：

- **主翻译**：翻译 `to_translate.xlsx`，保存为 `to_translated.xlsx`
- **补翻**：翻译 `to_translate_remaining.xlsx`，保存为 `to_translated_remaining.xlsx`

**重要提示**：翻译时务必保留以下占位符和标记：
- `%s`, `%d`, `%i`, `%f` 等格式占位符
- `[variable]` 形式的变量引用（如 `[girl.name]`, `[MC.name]`）
- `{color=...}`, `{b}`, `{i}` 等 Ren'Py 文本标记
- `\n` 换行符

### 4. 导入翻译

#### 导入主翻译文件

```bash
python tools/Scripts/translation/import_translated_xlsx.py to_translated.xlsx
```

#### 导入补翻文件

```bash
python tools/Scripts/translation/import_translated_remaining.py
```

这会读取项目根目录下的 `to_translate_remaining.xlsx` 和 `to_translated_remaining.xlsx`。

### 5. 机器翻译后修复（必须按顺序执行）

导入 Google Translate 结果后，由于机器翻译会破坏格式，必须依次运行以下修复脚本：

```bash
# 1. 修复被翻译的变量名（如 [女孩名字] → [girl.name]）
python tools/Scripts/checks/fix/fix_all_variables.py

# 2. 修复 %s 占位符数量不匹配
python tools/Scripts/translation/fix_placeholders.py

# 3. 修复文本标签不匹配（如 {b}, {color=...}）
python tools/Scripts/checks/fix/fix_all_tag_mismatches.py

# 4. 验证语法
python tools/Scripts/translation/verify_strings.py
```

### 6. 清理缓存并测试

删除 `.rpyc` 缓存文件（脚本通常会自动删除），然后启动游戏测试。

---

## 脚本索引

### 核心工作流脚本

| 脚本 | 说明 |
|------|------|
| 脚本 | 说明 |
|------|------|
| `Scripts/translation/find_untranslated.py` | 查找未翻译内容并生成 `to_translate_remaining.xlsx` |
| `Scripts/translation/export_translation_xlsx.py` | 导出全部待翻译内容到 xlsx |
| `Scripts/translation/import_translated_xlsx.py` | 导入主翻译文件 |
| `Scripts/translation/import_translated_remaining.py` | 导入补翻文件 |
| `Scripts/translation/fix_placeholders.py` | 检查并修复 `%s/%d` 占位符 |
| `Scripts/checks/fix/fix_all_variables.py` | 修复被误翻译的 `[variable]` 变量名 |
| `Scripts/checks/fix/fix_all_tag_mismatches.py` | 修复不匹配的 `{b}`/`{color}`/`{i}`/`{size}` 标签 |
| `Scripts/translation/verify_strings.py` | 验证 `strings.rpy` 语法和占位符数量 |

### 高级脚本

| 脚本 | 说明 |
|------|------|
| 脚本 | 说明 |
|------|------|
| `Scripts/translation/merge_translations.py` | 扫描源代码 `__()`/`_()` 调用，重新生成 `strings.rpy` |
| `Scripts/translation/merge_tl_strings.py` | 合并剧情文件中的 `strings:` 块到 `strings.rpy` |
| `Scripts/translation/wrap_dialogue.py` | 给 `BKdialogue.rpy` 的 `add_dialogue()` 包裹 `__()` |
| `Scripts/translation/restore_lost.py` | 从 git 历史恢复丢失的翻译 |
| `Scripts/translation/batch_translate_dialogue.py` | 使用 Google Translate 批量翻译对话（带占位符保护） |
| `Scripts/translation/export_translation_docx.py` | 导出翻译到 docx 格式 |
| `Scripts/translation/remove_duplicates.py` | 删除 `strings.rpy` 中重复的 `old` 键 |

### 原始开发工具（从 game/tools 迁移）

| 脚本 | 说明 |
|------|------|
| 脚本 | 说明 |
|------|------|
| `Scripts/translation/extract_translations.py` | 从源代码提取字符串生成模板 |
| `Scripts/translation/import_translation.py` | 导入 txt 格式翻译到 `strings.rpy` |
| `Scripts/translation/export_for_translation.py` | 导出待翻译内容为 txt |
| `Scripts/translation/docx/convert_docx.py` / `txt_to_docx.py` / `docx_to_txt.py` | docx/txt 格式转换 |
| `Scripts/checks/check_*.py` | 各类代码检查脚本 |
| `Scripts/marking/mark_*.py` | 源代码标记脚本（给字符串包裹 `__()`） |
| `Scripts/checks/fix/fix_broken_strings.py` | 修复损坏的字符串 |
| `Scripts/marking/split_menu_if.py` | 拆分 menu if 语句 |
| `Scripts/bk_evolution/export_hardcoded.py` | 将硬编码 Trait/Perk 导出为 JSON |

---

## 故障排查

### 游戏启动时报错 `TypeError: not all arguments converted during string formatting`

原因：`new` 翻译中缺少 `%s` 占位符。

解决：运行 `python tools/Scripts/translation/fix_placeholders.py`。

### 游戏启动时报错 `A translation for "..." already exists`

原因：剧情文件和 `strings.rpy` 中有重复的 `old` 键。

解决：运行 `python tools/Scripts/translation/merge_tl_strings.py`。

### 游戏启动时报错 `NameError: Name 'xxx' is not defined`

原因：`[variable]` 形式的变量名被 Google Translate 翻译成了中文（如 `[妓院广告]`）。

解决：运行 `python tools/Scripts/checks/fix/fix_all_variables.py`。

### 游戏启动时报错 `/x closes a text tag that isn't open`

原因：`{b}`, `{color=...}` 等文本标签不匹配。

解决：运行 `python tools/Scripts/checks/fix/fix_all_tag_mismatches.py`。

### 导入后很多对话仍是英文

1. 确认 `to_translate_remaining.xlsx` 中的原文列（A列）和翻译列（B列）正确
2. 重新运行 `python tools/Scripts/translation/find_untranslated.py` 查看最新统计
3. 如果源文件有新增文本，先运行 `python tools/Scripts/translation/merge_translations.py` 重新生成 `strings.rpy`


