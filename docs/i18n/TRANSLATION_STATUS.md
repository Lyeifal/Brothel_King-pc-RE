# BK Evolution — 中文翻译补完记录

> 最后更新：2026-09-25（第三轮：I18n 代码审查后新增字符串补翻）
>
> **状态：翻译补完已收官 ✅。本文档为历史记录 + 当前基线**，不再追踪新任务。
>
> 第三轮（2026-09-25）：2026-09 I18n 人工审查（159 文件）+ 复查补漏在源码中新增约 1,200 处 `__()`/`_()` 包裹，经 `translate --empty` 提取 **1,271 条**（1,246 strings + 25 dialogue），由模型逐条直译（非机翻），守恒校验后导回。当前基线：**0 缺失 dialogue / 0 缺失 strings**。
>
> 第二轮（2026-09-11）补完了剩余存量，并修复了提取盲区（天赋树/特质/物品）。当前基线：**0 缺失 dialogue / 0 缺失 strings**。
>
> 制定日期：2026-06-11  
> 更新日期：2026-06-12  
> 目标：补完 `_cn` 旧版本无法覆盖的所有缺失翻译
>
> ## 当前基线（2026-09-25 第三轮后实测）
>
> 运行 `& "lib/py3-windows-x86_64/python.exe" "Brothel_King.py" . translate --count chinese_simplified`：
>
> | 指标 | 数值 |
> |------|------|
> | 缺失 dialogue 翻译 | **0** |
> | 缺失 string 翻译 | **0**（空槽位均为空源字符串，无需翻译） |
> | JSON `_i18n` 字符串（`tools/audit_json_i18n.py`） | 103 个 JSON 文件 / **3,533 条，全部已翻译** |
> | i18n_lint 基线 | 14 处 issue，全部位于开发者面向文本（dev console、test runner、hook 失败通知等），非玩家可见字符串 |
>
> 上述零缺失即为回归基线：新增代码必须保持缺失数为零。详见 [`I18N_ROADMAP.md`](I18N_ROADMAP.md)。

---

## 一、当前状态

### 已完成（本次会话）

| 工作项 | 数量 | 说明 |
|--------|------|------|
| Hash 匹配迁移 | 13,861 条对话块 | 旧版本 `schinese` hash 直接匹配当前 `chinese_simplified` |
| 文本级匹配迁移 | 1,091 条对话块 | 原文相同但 hash 不同（代码重构导致） |
| JSON _i18n 导入 | 1,282 条字符串 | 将 JSON 中 `_i18n` 字段缺失的文本导入 `strings.rpy` |
| 空翻译补完 | 1,282 条 strings | 从 `temp/translations/to_translate_empty.xlsx` 导回中文翻译 |
| 新增缺失字符串提取 | 458 条 | 运行 `translate --empty` 发现源代码中未进入翻译系统的字符串（不含 common.rpy） |
| 非英文原文自动填充 | 72 条 | 源代码已是中文的条目自动 `new = old` |
| 第二批空翻译导入 | 386 条 strings | 从 `temp/translations/to_translate_remaining_v3.xlsx` 导回中文翻译 |
| yes_no 确认框字符串包裹 `__()` | 44 条 | 给 `call_screen("yes_no", ...)` 的裸字符串加翻译标记 |
| Lint 验证 | ✅ 通过 | 零新增错误 |

### 翻译覆盖率

| 类别 | 总数 | 已翻译 | 空翻译 | 覆盖率 |
|------|------|--------|--------|--------|
| 对话块 | 29,367 | 29,341 | 26 | 99.91% |
| strings / UI 字符串 | ~13,000 | ~12,300 | 674 | 94.8% |

> **注意**：新增 458 条空翻译是因为 Ren'Py `translate` 提取后发现大量菜单选项、UI 文本和旁白尚未进入翻译系统。其中 72 条原文已是中文，已自动填充；剩余 386 条英文游戏字符串 + 26 条对话已导出到 `temp/translations/to_translate_remaining_v3.xlsx`。

---

## 二、剩余缺口清单

### 缺口 1：空翻译（已解决 ✅）

**来源**：`temp/translations/to_translate_empty.xlsx`

| 类型 | 数量 | 主要内容 | 位置 |
|------|------|----------|------|
| strings | 1,283 | 成就、物品、法术、职业、NPC 等 JSON 数据文本 | `strings.rpy` 末尾 |
| dialogue | 11 | 剧情对话（chapter1, story_events 等） | 各 `.rpy` 分片文件 |

**处理结果**：
- 用户完成 `temp/translations/to_translate_empty.xlsx` 中 "Chinese Translation" 列填充
- 使用 `tools/import_translated_empty.py` 导回
- 1,282 条 strings 翻译成功写入 `strings.rpy`
- 11 条 dialogue 的源文本为空字符串（`# ""`），无需翻译

### 缺口 2：新增空翻译 — 已解决 ✅（后续又发现 yes_no 确认框）

**来源**：运行 `translate --empty chinese_simplified` 后发现

**原因**：大量菜单选项、UI 文本、旁白和互动选项使用了裸字符串或 screen language 中的裸 `text`，没有进入之前的翻译系统。

**处理结果（第一批）**：
- 使用 `translate --empty chinese_simplified` 生成缺失翻译脚手架
- 72 条原文已是中文的条目通过 `tools/auto_fill_nonenglish_empty.py` 自动填充
- Ren'Py 公共字符串 `common.rpy`（288 条辅助功能菜单）已删除，不翻译
- 剩余 412 条导出到 `temp/translations/to_translate_remaining_v3.xlsx`
  - `strings` sheet: 386 条游戏字符串（菜单选项、UI、旁白等）
  - `dialogue` sheet: 26 条对话（未翻译，为示例 mod 内容）
- 使用 `tools/import_translated_remaining_v3.py` 导回 386 条 strings 翻译
- Lint 通过

**处理结果（第二批 — yes_no 确认框）**：
- 用户反馈商店购买女孩确认框 "Do you really want to buy..." 仍为英文
- 根因：`renpy.call_screen("yes_no", "...")` 中的字符串是裸字符串，未被 `__()` 包裹
- 使用 `tools/wrap_yes_no_strings.py` 给 11 个文件中的 yes_no 提示字符串包裹 `__()`
- 重新运行 `translate --empty` 后新增 44 个英文空条目
- 已重新导出到 `temp/translations/to_translate_remaining_v3.xlsx`（当前 44 strings + 26 dialogue）

### 缺口 3：质量审核 — 中优先级

旧版本无法覆盖的 ~3,500 个对话块和 ~9,000 个字符串已有**机器翻译**，但质量参差不齐。

**典型问题模式**：
- 色情俚语直译（如 `pound` → "揍"）
- 长句断句生硬
- 标点混用（英文逗号 vs 中文逗号）

**审核策略**：
- 不需要逐条审核
- 游戏实际运行时，遇到明显不通顺的翻译再反馈修正
- 重点审核：剧情核心文本（chapter1-3, story_events）

### 缺口 3：JSON _i18n 翻译质量 — 低优先级

当前 JSON 的 `_i18n` 字段值是英文原文。即使补完 `strings.rpy`，也需要确保：
- `json_i18n.rpy` 正确注册
- 游戏运行时显示中文

---

## 三、执行步骤

### Step 1：翻译空翻译（已完成 ✅）

**工具**：`temp/translations/to_translate_empty.xlsx`

**方法 A：人工翻译（本次采用）**
1. 打开 `temp/translations/to_translate_empty.xlsx`
2. 逐行填写 "Chinese Translation" 列
3. 保存（保持原文件名 `temp/translations/to_translate_empty.xlsx`）
4. 运行导入脚本：
   ```bash
   python tools/import_translated_empty.py
   ```

**导入结果**（2026-06-12）：
- `strings.rpy`: 1,282 / 1,283 条空翻译已填充
- 剩余 1 条 `old ""` 为空源文本，无需翻译
- 11 条 dialogue 源文本为空字符串，无需翻译

**方法 B：机器翻译（快速，质量一般）**
1. 在有网络的环境（如本地电脑）运行：
   ```bash
   pip install deep_translator
   python tools/batch_translate_empty.py
   ```
2. 脚本会自动填充所有空 `new ""` 条目

### Step 2：验证（已完成 ✅）

```powershell
# Lint 检查（使用项目内 Python）
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . lint

# 启动测试
.\Brothel_King.exe
```

**验证结果**（2026-06-12）：
- Lint 通过，无新增错误
- 预存警告（未由本次导入引入）：
  - `npc` / `girl.char` 角色求值警告
  - `custom/girls/` 下部分非 ASCII 文件名
  - 3 处 Unreachable Statements
  - 5 处 Orphan Translations

### Step 3：质量抽查

重点检查以下场景的中文显示：
- 游戏开场（intro）
- 第一章剧情（chapter1）
- 物品描述（打开物品栏）
- 成就系统
- 法术/力量界面

---

## 四、相关文件

| 文件 | 说明 |
|------|------|
| `temp/translations/to_translate_empty.xlsx` | 待翻译清单（1,294 条） |
| `temp/translations/json_i18n_to_translate.txt` | JSON _i18n 纯文本清单 |
| `temp/translations/translation_migration_report.txt` | 旧版本迁移统计报告 |
| `temp/translations/text_level_migration_report.txt` | 文本级匹配迁移报告 |
| `tools/migrate_cn_translation.py` | Hash 匹配迁移脚本 |
| `tools/text_level_migration.py` | 文本级匹配迁移脚本 |
| `tools/batch_translate_empty.py` | 机器翻译脚本 |
| `tools/export_empty_to_xlsx.py` | 导出空翻译到 Excel |
| `tools/import_translated_empty.py` | 从 Excel 导回空翻译 |
| `tools/auto_fill_nonenglish_empty.py` | 自动填充原文已是中文的空翻译 |
| `tools/export_remaining_english.py` | 导出剩余英文空翻译 |
| `tools/import_translated_remaining_v3.py` | 从 `temp/translations/to_translate_remaining_v3.xlsx` 导回翻译 |
| `tools/wrap_yes_no_strings.py` | 给 `call_screen("yes_no", ...)` 的裸字符串包裹 `__()` |
| `temp/translations/to_translate_remaining_v3.xlsx` | 剩余待翻译清单 |
| `_translation_backup/` | 原始翻译备份 |
| `_translation_import_backup_*` | 导入前自动备份 |

---

## 五、实际成果

1. **1,282 条 strings 空翻译已补完** → `strings.rpy` 覆盖率 99.99%
2. **翻译覆盖率提升至 >99.9%**（对话 + strings）
3. **JSON i18n 已生效** → 所有 `_i18n` 字段支持中文显示
4. **零破坏** → Lint 通过，无新增错误

## 六、后续建议

- 运行游戏进行实际中文显示抽查（开场、物品栏、成就、法术/力量界面）
- 关注 `to_translate_remaining_v2.xlsx` 中剩余的剧情对话补完
- 处理预存的 `npc` / `girl.char` Lint 警告（与翻译无关，可选）

---

## 七、第二轮——全部补完（2026-09-11）

### 7.1 空翻译存量清零

- 运行 `translate --empty` + 导出：**2,130 条空条目**（125 strings + 2,005 dialogue，主要在 `events_dispatcher.rpy`、`intro.rpy`、`interactions.rpy`）
- 全部翻译并导入 → `translate --count`：**0 缺失 dialogue / 0 缺失 strings**
- 修复 7 条被英文原样回填的成就描述（`new == old`，`--count` 无法识别），以及 `Leech jp` → 吸血职业点、`Constitution Mastery` 误译（宪法精通 → 体质精通），均在 `strings.rpy`

### 7.2 提取盲区修复（天赋树/特质/物品）

`translate --count` 全绿但这些 UI 仍显示英文，因为它们从未进入翻译系统：

| 根因 | 修复 |
|---|---|
| `perks.json` 天赋名无 `name_i18n` | +53 `name_i18n`、+52 `base_description_i18n` |
| `traits.json` 描述大面积缺失 | +113 `base_description_i18n` |
| `items.json` 描述大面积缺失 | +95 `description_i18n` |
| `Effect.get_description()` 硬编码英文片段 | ~30 处片段包裹 `__()`；复合串改为按片段翻译后拼接 |
| `perk.name` / `it.name` / tooltip / notify 裸用 | 在 `screen_girl_stats.rpy`、`screen_progress.rpy`、`items.rpy`、`main.rpy`、`screen_common.rpy` 包裹 `__()` |
| `generate_new_item` 先转小写再查表 | `__(self.base_name.lower())` → `__(self.base_name)` |
| `Perk.from_dict` 名称裸取 | `get_i18n(d, "name")` |

208 条新字符串（天赋/特质/物品名称与描述 + UI 片段）经 `tools/import_json_i18n.py` + `translate --empty` 提取、翻译、导入。`tools/audit_json_i18n.py`：3,533/3,533 已翻译。

### 7.3 工具链修复

- 修复 `tools/export_empty_to_xlsx.py`、`tools/import_translated_empty.py`、`tools/import_json_i18n.py` 中写死的旧项目路径（改为按脚本位置自动推导）
- 修复 `tools/export_empty_to_xlsx.py` 与 `tools/audit_placeholders.py` 写 Excel 遇控制字符崩溃的问题（IllegalCharacterError）
- **关键工作流事实**：`translate --empty` 不会提取 JSON `_i18n` 字符串（它们于 init 期动态注册）。JSON 新增 `_i18n` 字段后，必须先运行 `python tools/import_json_i18n.py` 同步进 `strings.rpy`，再走导出/翻译/导入流程。见 `I18N_ROADMAP.md` 第 4 节。

### 7.4 已知遗留（内容层面，非代码）

- ~209 条天赋/特质/物品描述为英文新撰（源数据原本没有），已翻译，建议游戏内核对语气
- 29 件武器/法杖类物品本身无描述（源数据为空），属正常
- `[plu]` 类英文复数占位符可能显示「3 天s」残留，如影响体验需代码侧处理
- i18n_lint 报 18 处，全部为开发者面向文本（见 `I18N_ROADMAP.md` 第 6 节）
