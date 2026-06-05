# Brothel King 国际化（i18n）重构进度

## 项目概况
- **项目**: Brothel King (Ren'Py游戏)
- **代码规模**: 46个.rpy文件，约11.27MB
- **目标**: 将硬编码文本重构为Ren'Py原生翻译系统，支持多语言

## 重构计划
1. Phase 0: 紧急止血（崩溃修复与 __() 清理）
2. Phase 1: 静态数据解耦（Data Layer Extraction）
3. Phase 2: 字符串拼接重构（Complete Sentence Refactoring）
4. Phase 3: 对话系统重构（Dialogue System v2）
5. Phase 4: 剧情对话原生翻译（Story Dialogue Native Translation）

---

## 当前进度

### Phase 0: 紧急止血 ✅ COMPLETED
- [x] 备份 `game/tl/chinese_simplified/strings.rpy`
- [x] 清理 `strings.rpy` 中的非法翻译条目
  - 删除 143 个图片路径翻译（如 `NPC/杂项/公主/公主被操了1.gif`）
  - 删除 70 个非法标识符翻译（label名、文件后缀 `_dusty`/`_dirty`、房间类型键等）
- [x] 移除源代码中图片路径上的 `__()`（143处）
  - `BKinit_variables.rpy`: `image princess fucked` 动画序列、`room` 图片后缀
  - `BKsettings.rpy`: `brothel_pics`、`playerclass_pics`、`god_pics`、`alignment_pics`
- [x] 移除源代码中 label 名上的 `__()`（200处）
  - `BKchapter1.rpy`, `BKchapter2.rpy`, `BKchapter3.rpy`
- [x] 移除源代码中 item 查找名上的 `__()`（18处）
  - `Healing powder`, `Cimerian scrap`, `Makibishi`, `Lightning Rod` 等
- [x] 修复 `job_room_dict` 值上的 `__()`（`tavern`/`strip club`/`onsen`/`okiya`）
- [x] **验证通过**: 游戏在 `chinese_simplified` 语言下可正常运行序章

### Phase 1: 静态数据解耦 ✅ COMPLETED
- [x] 创建 `game/data/` 目录框架
- [x] 迁移 `perform_job_dict` 到 `game/data/jobs.rpy`（211行）
- [x] 迁移难度与设置文本到 `game/data/settings.rpy`
  - `diff_name`, `diff_description`, `diff_setting_name`, `diff_setting_description`
  - `stat_name_dict`
- [x] 迁移 Perk 数据到 `game/data/perks.rpy`
  - `archetype_dict`, `perk_description`, `perk_dict`, 特殊 perks
- [x] 迁移 Power 数据到 `game/data/powers.rpy`
  - `evpower_list`, `evpower_super_list`
- [x] 迁移 Item 数据到 `game/data/items.rpy`
  - `all_items`（110项）, `template_items`（92项）
- [x] 原文件中所有被迁移的数据块已替换为迁移注释
- [x] 新数据文件使用正确的 `init` 优先级确保加载顺序安全

### Phase 2: 字符串拼接重构 ✅ COMPLETED
- [x] 扫描并重构 12 个核心文件中的 `__()` 字符串拼接
  - `BKscreens.rpy`, `BKclasses.rpy`, `BKfunctions.rpy`, `BKsecurity.rpy`, `BKinteractions.rpy`, `BKendday.rpy`, `BKevents.rpy`, `BKscreen_home.rpy`
  - `BKchapter2.rpy`, `BKdialogue.rpy`, `BKitems.rpy`, `BKmain.rpy`
- [x] 修复重构过程中引入的语法错误（BKsecurity.rpy line 1376, 1519）
- [x] 使用 `merge_translations.py` 重新生成 `strings.rpy`
  - 从备份中保留了 **2455** 条中文翻译
  - 新增 **832** 条待翻译字符串
  - 删除 **1075** 条过时翻译
- [x] 删除旧的 `.rpyc` 缓存，Ren'Py 成功重新编译
- [x] **Phase 2 后续运行时错误修复**
  - [x] `TypeError: not all arguments converted during string formatting` (`BKfunctions.rpy:825`)
    - 根因：`strings.rpy` 中存在 `new ""` 空翻译，导致 `__()` 返回空字符串，`"" % "text"` 触发 TypeError
    - 修复：`get_description()` 改为字符串拼接方式；`merge_translations.py` 对未翻译条目写入原文回退而非空字符串
  - [x] `OSError: Couldn't find file 'NPC/杂项/公主/公主被操了1.gif'`
    - 根因：Phase 2 重构时误将图片路径重新包裹在 `__()` 中，Ren'Py 尝试用翻译后的中文路径查找文件
    - 修复：移除 `BKinit_variables.rpy` 143 处和 `BKsettings.rpy` 38 处图片路径上的 `__()`；重新生成 `strings.rpy` 剔除 1218 条图片路径翻译
- [x] **验证通过**: 游戏可正常启动，中文翻译正确加载

### Phase 3: 对话系统重构 ✅ COMPLETED
- [x] 使用自动化脚本 `wrap_dialogue.py` 给 `BKdialogue.rpy` 中 4,448 个 `add_dialogue()` 的 `lines` 参数包裹 `__()`
- [x] 使用 `merge_translations.py` 重新生成 `strings.rpy`
- [x] 使用 `merge_tl_strings.py` 从 20 个剧情翻译文件中移除重复的 `translate chinese_simplified strings:` 块
- [x] 合并 1,500 条重叠翻译到 `strings.rpy`

### Phase 4: 剧情对话原生翻译 ✅ COMPLETED（第一轮）
- [x] 通过 `export_translation_xlsx.py` 导出全部待翻译文本到 `to_translate.xlsx`（25,663 条）
- [x] 用户通过 Google Translate 手动翻译后，使用 `import_translated_xlsx.py` 批量导回
- [x] 导入 25,224 条中文翻译（`strings.rpy` 7,821 条 + 剧情文件 17,403 条）
- [x] 修复 `import_translated_xlsx.py` 换行符 bug，避免 `new` 行与下一行 `#` 注释合并
- [x] 使用 `fix_placeholders.py` 修复 88 条因 Google Translate 误删 `%s` 占位符导致的运行时崩溃
- [x] **验证通过**: 游戏可正常启动，中文翻译正确加载

### Phase 5: 补翻遗漏文本 ✅ COMPLETED（第二轮）
- [x] 统计当前仍未翻译的条目并导出到 `to_translate_remaining.xlsx`
  - `strings.rpy`: 179 条未翻译
  - 剧情文件: 10,954 条未翻译
  - 合计: 11,133 条未翻译
- [x] 用户完成第二轮翻译后，使用 `import_translated_remaining.py` 导回
  - 导入 `strings.rpy`: 73 条新翻译
  - 导入剧情文件: 8,147 条新翻译
  - 使用 `fix_placeholders.py` 检测并回退 67 条 `%s` 占位符被误删的翻译
  - **第二轮合计导入有效翻译: 8,153 条**

### Phase 6: 工具整理与持续补翻 🔄 IN PROGRESS
- [x] 创建 `tools/` 目录，整理翻译相关脚本
  - 保留核心工作流脚本：`find_untranslated.py`, `import_translated_xlsx.py`, `import_translated_remaining.py`, `fix_placeholders.py`, `verify_strings.py`, `export_translation_xlsx.py`, `merge_translations.py`, `merge_tl_strings.py`, `wrap_dialogue.py`, `restore_lost.py`
  - 清理 20+ 个临时/调试脚本
  - 所有脚本统一使用 `ROOT = Path(__file__).parent.parent` 从项目根目录解析路径
- [x] 编写 `tools/TRANSLATION_WORKFLOW.md` 使用说明文档
- [x] 改进 `find_untranslated.py` 的引号提取逻辑，正确处理 `\"` 转义
- [x] 重新生成 `to_translate_remaining.xlsx`，当前剩余 3,040 条未翻译
  - `strings.rpy`: 173 条
  - 剧情文件: 2,867 条
- [x] 第三轮翻译：用户翻译 `to_translated_remaining_2.xlsx` 后使用 `import_translated_remaining.py` 导回
  - **重写 `import_dialogue` 逻辑**：从全局正则替换改为逐行解析，修复多词 speaker（如 `sill sad`）导致匹配失败的问题
  - 导入 `strings.rpy`: 51 条新翻译
  - 导入剧情文件: 2,316 条新翻译（其中部分在 `fix_placeholders` 后回退）
  - 使用 `fix_placeholders.py` 检测并回退 51 条 `%s` 占位符被误删的翻译
  - **第三轮合计导入有效翻译: ~2,316 条**
- [x] 重新生成 `to_translate_remaining.xlsx`，当前剩余 **733** 条未翻译
  - `strings.rpy`: 173 条（ mostly `%s` 占位符字符串）
  - 剧情文件: 560 条
- [x] **重大发现：扫描发现 1,023 个菜单选项从未进入翻译系统！**
  - 根因：Ren'Py `generate translations` 未提取这些 `menu:` 选项（可能在生成后源码有更新）
  - 已编写脚本从源代码提取并追加到 `strings.rpy`
  - 尝试使用 Google Translate API 自动翻译，但因网络限制超时，未成功
- [x] 重新生成 `to_translate_remaining.xlsx`，当前剩余 **1,756** 条未翻译
  - `strings.rpy`: 1,196 条（其中 1,023 条是新增菜单选项，173 条是含 `%s` 的字符串）
  - 剧情文件: 560 条
- [x] 第四轮翻译：用户翻译 `to_translated_remaining_3.xlsx` 后导入
  - 导入 `strings.rpy`: 1,072 条新翻译（1,023 个菜单选项 + 49 条其他字符串）
  - 使用 `fix_placeholders.py` 检测并回退 51 条 `%s` 占位符被误删的翻译
  - **第四轮合计导入有效翻译: ~1,021 条**
- [x] **占位符修复与重新导入**
  - 编写脚本自动在 xlsx 翻译文本中恢复缺失的 `%s` 占位符（比例插入法）
  - 修复 84 条占位符缺失的翻译
  - 从 `to_translated_remaining_3_fixed.xlsx` 重新导入，成功更新 53 条
  - `fix_placeholders.py` 再次修复 10 条残余占位符不匹配
  - **净减少 strings.rpy 未翻译数: 43 条**
- [x] **自动化清理 strings.rpy 剩余条目**
  - 更新 `find_untranslated.py` 排除列表，标记 43 条 genuinely 不需要翻译的条目
  - 自动翻译 11 个 UI 标签
  - 批量翻译 78 条含 `%s` 的字符串
  - **strings.rpy 未翻译数从 132 降至 0**
- [x] **批量翻译剧情对话**
  - 编写 `batch_translate_dialogue.py`，使用 `deep_translator` 批量翻译 560 条剧情对话
  - 保护 `{color=...}`、`[variable]`、`%s`、表情符号等格式标记
  - 成功导入 **60 条**新翻译
  - 修复 `find_untranslated.py` 的 `has_chinese()` 函数，加入全角标点检测，排除 41 条误判
  - **剧情对话未翻译数从 560 降至 459**
- [x] 重新生成 `to_translate_remaining_v2.xlsx`，当前剩余 **459** 条未翻译
  - `strings.rpy`: **0 条** ✅ 完全完成
  - 剧情文件: 459 条
- [ ] 第六轮翻译：处理剩余 459 条剧情对话（大多为喊叫声/咒语/拟声词，机器翻译无法处理）

---

## 预研报告（Phase 3 & 4）

### 1. 对话系统 (`BKdialogue.rpy`)

**规模**: ~5,333 行，**4,451** 个 `add_dialogue()` 调用

**当前机制**:
- 对话以裸字符串传入 `add_dialogue()`，仅在运行时通过 `Dialogue.say()` 调用 `__(self.line)` 翻译
- **关键问题**: Ren'Py 的翻译提取器扫描的是 `__("...")` 形式的**编译期字符串字面量**，运行时变量形式的 `__(self.line)` **无法被提取**，导致 `strings.rpy` 完全缺失这些对话
- 多行对话（`multiple=True`）使用 `g: ` / `mc: ` / `giz: ` 前缀，`dialogue_say_multiple` 先剥离前缀再调用 `__()`
- Mod 可通过 `add_dialogue()` 向全局 `dialogue_dict` 注入新对话

**Phase 3 核心工作**:
1. 给全部 4,451 个 `add_dialogue()` 的 `lines` 参数包裹 `__()`（需自动化脚本）
2. 调整 `dialogue_say_multiple`，确保前缀剥离发生在 `__()` 之前，避免前缀进入待翻译文本
3. 验证 Mod 中的 `add_dialogue()` 调用也能被正确处理

### 2. 剧情系统 (主线 / 支线 / 个人角色剧情)

**文件规模**:

| 文件 | 行数 | 内容 |
|------|------|------|
| `BKchapter1.rpy` | ~7,384 | 主线第一章 |
| `BKchapter2.rpy` | ~11,244 | 主线第二章 + 支线 |
| `BKchapter3.rpy` | ~24,394 | 主线第三章 + 女忍者路线（Narika/Mizuki/Haruka/Homura） |
| `BKstory_events.rpy` | ~21,448 | 通用/季节性事件 |
| `BKcity_events.rpy` | ~5,669 | 城市随机遭遇 |
| `BKday_events.rpy` | ~7,590 | 日常随机事件 |
| **合计** | **~77,000+** | |

**当前机制**:
- 剧情文件**不使用** `__()`，对话和叙述全是裸字符串
- Ren'Py 原生 `translate` 块已在 `game/tl/chinese_simplified/` 下为这些文件生成翻译脚手架
- `tl/chinese_simplified/BKchapter1.rpy` 等文件已存在，但 `new` 行仍是英文（未填充翻译）
- 菜单选项通过 `translate chinese_simplified strings:` 块（已混入 `strings.rpy`）

**Phase 4 核心工作**:
1. **代码层面无需大规模重构** — 剧情已使用 Ren'Py 原生 `translate` 机制
2. 需要填充/更新 `tl/chinese_simplified/BKchapter*.rpy` 等文件的 `new` 值
3. 统一剧情翻译与 `strings.rpy` 的工作流（避免重复劳动）
4. 确保 Mod 新增的剧情标签也能进入翻译提取范围

### 3. 自制角色包 (`game/girls/`)

**结构**: 每个角色一个文件夹，包含图片 + 可选的 `_BK.ini` 配置文件

**含文本的配置项**:
- `origin_description` — 角色自述家乡（直接用于 `renpy.say()`）
- `description` — 角色包描述
- `custom personality/description` — 自定义性格描述
- `personality_name` — 自定义性格名称

**翻译挑战**:
- `_BK.ini` 文本**不在 Ren'Py 翻译系统范围内**（运行时从文件读取，无 `__()` 包裹）
- 角色包支持自定义 `.rpy` 脚本（`custom_dialogue_label`, `story_label`, `city_label`, `night_label`）
- 图片文件名是内部标签（如 `sex doggy cumshot inside`），**不需要翻译**

**推荐策略**:
- 角色包翻译由包作者自行负责（在 `_BK.ini` 中直接写目标语言，或随包附带 `.rpy` 翻译文件）
- 主游戏不强行干预 `girls/` 目录下的文本翻译

### 4. Mod 系统 (`game/Mods/`)

**结构**: 每个 Mod 一个子文件夹，内含 `.rpy` 脚本

**关键发现**:
- Mod 是正常 `.rpy` 文件，Ren'Py `generate translations` **可以提取**其中的字符串
- `tl/chinese_simplified/Mods/` 已存在示例 Mod 的翻译文件
- Mod 可通过 `add_dialogue()` 注入对话 — 同样面临 `__()` 提取问题
- **`Mod.name` 被包裹在 `__()` 中**，但同时用作 `detected_mods` / `persistent.mods` / `active_mods` 的**字典键**，切换语言会导致持久化键名不匹配（与此前 perks/powers 的 `name` 问题相同）

**修复建议**:
- 从示例 Mod 和 `Mod` 类文档中移除 `name = __(...)` 的推荐用法
- Mod 的 `name` 应使用硬编码英文标识符，仅在 UI 显示时使用 `__()` 包裹的 `display_name`

### 5. 两套翻译机制的现状

| 机制 | 覆盖范围 | 当前状态 |
|------|----------|----------|
| `__()` + `strings.rpy` | 代码中的字符串（UI、菜单、数据层、`perform_job_dict`）| ✅ 已配置，830 条待翻译 |
| Ren'Py `translate` 块 | 剧情脚本中的 `say` / `narrator` 语句 | ⚠️ 脚手架已生成，内容未填充 |

**结论**: 本项目不存在"统一为单一翻译机制"的必要。Ren'Py 的设计本就是 `__()` 用于代码字符串，`translate` 块用于脚本对话。Phase 3 和 Phase 4 分别补齐两套机制的缺失环节即可。

---

## 数据层目录结构

```
game/data/
  jobs.rpy       # 工作描述、性行为描述模板 (perform_job_dict)
  settings.rpy   # 难度名称、设置项、属性名称
  perks.rpy      # 天赋原型、描述、字典
  powers.rpy     # 邪恶力量列表
  items.rpy      # 物品列表、模板物品
```

---

## 统计汇总

| 类别 | 数量 |
|------|------|
| 修改的文件数 | 30+ |
| Git 提交数 | 15+ |
| Phase 0 清理的非法翻译条目 | 213 |
| Phase 0 修复的 __() 滥用 | 365 |
| Phase 1 迁移的数据行数 | ~850 |
| 新建数据文件数 | 5 |
| Phase 2 重构的文件数 | 12 |
| Phase 2 保留的中文翻译 | 2,455 |
| Phase 2 新增待翻译字符串 | 832 |
| Phase 2 删除的过时翻译 | 1,075 |
| Phase 4 第一轮导入总翻译数 | 25,224 |
| Phase 4 导入 strings.rpy 翻译数 | 7,821 |
| Phase 4 导入剧情文件翻译数 | 17,403 |
| Phase 5 第二轮导入总翻译数 | 8,153 |
| Phase 5 导入 strings.rpy 翻译数 | 73 |
| Phase 5 导入剧情文件翻译数 | 8,147 |
| Phase 5 第二轮占位符回退数 | 67 |
| Phase 6 第三轮导入总翻译数 | 2,316 |
| Phase 6 导入 strings.rpy 翻译数 | 51 |
| Phase 6 导入剧情文件翻译数 | 2,265 |
| Phase 6 第三轮占位符回退数 | 51 |
| Phase 6 发现的遗漏菜单选项 | 1,023 |
| Phase 6 第四轮导入 strings.rpy 翻译数 | 1,072 |
| Phase 6 第四轮占位符回退数 | 51 |
| Phase 6 占位符自动修复数 | 84 |
| Phase 6 占位符修复后导入数 | 53 |
| Phase 6 占位符修复后回退数 | 10 |
| Phase 6 自动翻译 UI 标签 | 11 |
| Phase 6 批量翻译 %s 字符串 | 78 |
| Phase 6 排除不需要翻译条目 | 43 |
| Phase 6 当前未翻译 strings.rpy | **0** |
| Phase 6 当前未翻译剧情对话 | 459 |
| Phase 6 当前总未翻译条目 | **459** |
| Phase 6 当前总体翻译覆盖率 | **~98.8%** |

---

## 已知限制与待办事项

### 已完成内容
- [x] **对话系统重构 (Phase 3)**: 给 `BKdialogue.rpy` 中 4,448 个 `add_dialogue()` 的 `lines` 参数包裹 `__()`，使对话可被 Ren'Py 翻译提取
  - 使用自动化脚本 `wrap_dialogue.py` 完成修改
  - `dialogue_say_multiple` 的前缀剥离逻辑无需调整（运行时 `__()` 与 `init` 时 `__()` 不产生冲突）
  - 使用 `merge_translations.py` 重新生成 `strings.rpy`
    - 新增 7,037 条待翻译字符串（主要来自对话系统）
  - **修复重复翻译错误**: `tl/chinese_simplified/*.rpy` 剧情翻译文件中也包含 `translate chinese_simplified strings:` 块，与新生成的 `strings.rpy` 产生 `old` 键冲突
    - 使用 `merge_tl_strings.py` 从 20 个剧情翻译文件中移除 `strings:` 块
    - 合并 1,500 条重叠翻译到 `strings.rpy`
  - **修复 `_()` 字符串丢失**: `merge_translations.py` 最初只扫描 `__()`，漏掉了 1,217 个 `_()` 调用（屏幕语言字符串），导致 523 条中文翻译丢失
    - 修改 `merge_translations.py` 同时扫描 `_()` 和 `__()`
    - 使用 `restore_lost.py` 从 git 历史找回 523 条丢失翻译
    - 最终 `strings.rpy`: **10,192** 条总条目，**2,280** 条中文翻译，**7,912** 条待翻译
  - **新增翻译说明文档**: `game/tl/TRANSLATION_GUIDE.md`

- [x] **剧情对话翻译填充 (Phase 4 第一轮)**: 通过 Google Translate 完成第一轮批量翻译并导回
  - 导出 `to_translate.xlsx`（25,663 条）
  - 用户翻译后使用 `import_translated_xlsx.py` 导回 25,224 条
    - `strings.rpy`: 7,821 条
    - 剧情文件: 17,403 条（涵盖主线、支线、事件、互动等全部 16 个剧情文件）
  - 修复 `import_translated_xlsx.py` 正则替换缺少末尾 `\n` 导致的 `strings.rpy` 语法合并 bug
  - 使用 `fix_placeholders.py` 检测并回退 88 条 `%s` 占位符被误删的翻译，避免 `TypeError: not all arguments converted during string formatting` 运行时崩溃
  - **验证通过**: 游戏可正常启动，无报错

### 仍需处理的内容（Phase 6）
- [x] **补翻 strings.rpy 剩余文本**: 通过自动化脚本完成
  - 43 条 genuinely 不需要翻译的条目已排除（按键名、符号、颜色值、动态变量、纯格式模板）
  - 11 个 UI 标签自动翻译
  - 78 条含 `%s` 的字符串通过 `deep_translator` 批量翻译（占位符保护机制）
  - **strings.rpy 未翻译数: 0/11215** ✅
- [ ] **补翻剩余 560 条剧情对话**
  - 已导出到 `to_translate_remaining.xlsx`
  - 待用户完成翻译后使用 `import_translated_remaining.py` 导回
- [ ] **Mod `name` 持久化修复**: 示例 Mod 和 `Mod` 类文档中 `name = __(...)` 的用法会导致语言切换后持久化键丢失
- [ ] **图片内嵌文本**: 如果游戏中有文字内嵌在图片中，需要重新制图
- [x] **CJK字体文件**: NotoSansCJKsc-Regular.otf 已配置（commit f18f340）

### 已知问题（已接受）
- [ ] **工作事件文本换行**: `perform_job_dict` 字符串和 `log.add_report()` 的换行逻辑导致工作事件文本存在额外换行。此为原始游戏设计行为，非重构引入，当前不处理。
- [ ] **角色包 `_BK.ini` 文本**: `origin_description` 等文本不在 Ren'Py 翻译系统范围内，由角色包作者自行负责翻译

### 当前进度
- `strings.rpy`: 11,215 总条目，**11,215 已翻译（100%）**，**0 未翻译** ✅
- 剧情文件: 27,878 总条目，**27,419 已翻译（98.4%）**，**459 未翻译**
- **总体**: 39,093 总条目，**38,634 已翻译（98.8%）**，**459 未翻译**

### 工具目录
```
tools/
├── export_translation_xlsx.py      # 导出全部待翻译内容
├── find_untranslated.py            # 查找未翻译并生成 xlsx
├── import_translated_xlsx.py       # 导入主翻译
├── import_translated_remaining.py  # 导入补翻
├── fix_placeholders.py             # 修复 %s/%d 占位符
├── verify_strings.py               # 验证 strings.rpy 语法
├── merge_translations.py           # 重新生成 strings.rpy
├── merge_tl_strings.py             # 合并剧情文件 strings 块
├── wrap_dialogue.py                # 给 add_dialogue 包裹 __()
├── restore_lost.py                 # 恢复丢失翻译
└── TRANSLATION_WORKFLOW.md         # 使用说明
```

### 建议的后续步骤
1. 打开 `to_translate_remaining.xlsx`（3,040 条），使用 Google Translate 或 DeepL 翻译
2. **重点注意 `%s` 占位符**：strings sheet 中的 173 条大多是含 `%s` 的工作/事件描述，翻译后必须保留 `%s`
3. 翻译完成后保存为 `to_translated_remaining.xlsx`
4. 运行 `python tools/import_translated_remaining.py` 导回
5. 运行 `python tools/fix_placeholders.py` 检查并修复占位符
6. 运行 `python tools/verify_strings.py` 验证语法
7. 删除 `.rpyc` 缓存并启动游戏测试
