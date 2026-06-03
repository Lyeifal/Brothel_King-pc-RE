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

### Phase 3: 对话系统重构 ⏳ PENDING
### Phase 4: 剧情对话原生翻译 ⏳ PENDING

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

---

## 已知限制与待办事项

### 仍需处理的内容
- [ ] **对话系统重构 (Phase 3)**: 给 `BKdialogue.rpy` 中 4,451 个 `add_dialogue()` 的 `lines` 参数包裹 `__()`，使对话可被 Ren'Py 翻译提取；调整 `dialogue_say_multiple` 前缀剥离逻辑
- [ ] **剧情对话翻译填充 (Phase 4)**: `tl/chinese_simplified/BKchapter*.rpy` 等文件的 `translate` 脚手架已生成，需填充 `new` 值为实际中文翻译
- [ ] **Mod `name` 持久化修复**: 示例 Mod 和 `Mod` 类文档中 `name = __(...)` 的用法会导致语言切换后持久化键丢失
- [ ] **图片内嵌文本**: 如果游戏中有文字内嵌在图片中，需要重新制图
- [x] **CJK字体文件**: NotoSansCJKsc-Regular.otf 已配置（commit f18f340）

### 已知问题（已接受）
- [ ] **工作事件文本换行**: `perform_job_dict` 字符串和 `log.add_report()` 的换行逻辑导致工作事件文本存在额外换行。此为原始游戏设计行为，非重构引入，当前不处理。
- [ ] **角色包 `_BK.ini` 文本**: `origin_description` 等文本不在 Ren'Py 翻译系统范围内，由角色包作者自行负责翻译

### 建议的后续步骤
1. 完成 Phase 3 对话系统重构（自动化脚本给 `add_dialogue()` 包裹 `__()`，重新生成 `strings.rpy`）
2. 完成 Phase 4 剧情翻译填充（7 个剧情文件，`translate` 块 `new` 值待翻译）
3. 开始实际翻译工作（830 条代码字符串 + 数万行剧情对话待翻译）
4. 考虑使用 AI 辅助翻译（批量处理 `strings.rpy` 和 `tl/*.rpy` 中的待翻译条目）
