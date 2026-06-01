# Brothel King 国际化（i18n）重构进度

## 项目概况
- **项目**: Brothel King (Ren'Py游戏)
- **代码规模**: 46个.rpy文件，约11.27MB
- **目标**: 将硬编码文本重构为Ren'Py原生翻译系统，支持多语言

## 已完成的阶段

### Phase 0: 基础设施 ✅
- [x] 初始化Git仓库
- [x] 创建 `.gitignore`
- [x] 创建 `game/tl/` 目录结构
  - `game/tl/english/strings.rpy`
  - `game/tl/chinese/strings.rpy`
  - `game/tl/chinese_simplified/strings.rpy`
- [x] 创建 `game/translations.rpy` 翻译框架
  - 语言映射配置（English, 中文, 简体中文）
  - 语言切换函数 `bk_set_language()`，支持CJK字体自动切换
  - 启动时自动应用语言

### Phase 1: 核心系统文件 ✅
- [x] **BKscreens.rpy** (414处修改)
  - 标记了 text、textbutton、tooltip、label、tt.Action 中的用户可见文本
  - 使用 `_()` 包裹
- [x] **BKinit_variables.rpy** (大量修改)
  - 标记了 random_tips 列表项（421处）
  - 标记了 diff_name、diff_description、diff_setting_name、diff_setting_description 字典值
  - 标记了 MC_playerclass_description、MC_stat_description、god_description、alignment_description
  - 标记了 farm_description 等农场相关描述
  - 使用 `__()` 包裹
  - 排除了代码标识符、图片名称、罗马数字
- [x] **BKdeclarations.rpy** (72处修改)
  - 标记了 Character() 和 DynamicCharacter() 中的角色名称
  - 排除了变量引用（如 "MC.name"、"sill_name"）
- [x] **BKitems.rpy / BKhelp.rpy / BKendday.rpy / BKscreen_home.rpy / BKcontent_menu.rpy**
  - 标记了 screen 语言中的 UI 文本
- [x] **剧情和事件文件** (220处修改)
  - 标记了 menu 选项文本
  - 文件：BKintro.rpy, BKchapter1-3.rpy, BKevents.rpy, BKday_events.rpy, BKcity_events.rpy, BKstory_events.rpy, BKinteractions.rpy, BKinteractions_free.rpy
- [x] **BKspells.rpy / BKperks.rpy / BKpowers.rpy / BKpostings.rpy** (274处修改)
  - 标记了 Spell/Moon/Perk/Power 对象的 description 和 name 参数
- [x] **BKclasses.rpy / BKfunctions.rpy / BKgirlclass.rpy / BKeven*.rpy** (79处修改)
  - 标记了 description/name 等关键字参数

### Phase 2: 翻译模板与UI配置 ✅
- [x] **生成翻译模板**
  - 提取了 4321 处字符串，3395 个唯一字符串
  - 生成了 `game/tl/english/strings.rpy`
  - 生成了 `game/tl/chinese/strings.rpy`
  - 生成了 `game/tl/chinese_simplified/strings.rpy`
- [x] **添加语言选择界面**
  - 在 preferences screen (screens.rpy) 添加了语言选择框
  - 支持 English / 中文 / 简体中文
- [x] **CJK字体配置**
  - 在 gui.rpy 添加了 CJK 字体配置注释
  - 在 translations.rpy 中添加了语言切换时的字体自动切换逻辑

## 已创建的工具脚本

### `game/tools/mark_translations.py`
- **用途**: 标记 screen 语言中的可翻译字符串
- **支持模式**: screen / python / auto
- **标记规则**: text、textbutton、tooltip、label、tt.Action

### `game/tools/mark_lists.py`
- **用途**: 标记特定列表变量中的字符串项
- **默认目标**: random_tips, tip_list

### `game/tools/mark_dict_values.py`
- **用途**: 标记特定字典变量中的值（不标记键）
- **默认目标**: diff_name, diff_description 等

### `game/tools/mark_characters.py`
- **用途**: 标记 Character() 定义中的角色名称
- **排除**: 变量引用（如 "MC.name"）

### `game/tools/mark_menus.py`
- **用途**: 标记 menu 选项文本

### `game/tools/mark_kwargs.py`
- **用途**: 标记函数调用中的 description/name 等关键字参数

### `game/tools/extract_translations.py`
- **用途**: 提取所有 `_()` 和 `__()` 字符串，生成 Ren'Py 翻译文件

## 下一步行动（待完成）

### 高优先级
1. **下载并配置CJK字体**
   - 推荐字体：Noto Sans CJK SC (思源黑体)
   - 将字体文件放入 game/ 目录
   - 取消注释 gui.rpy 中的 CJK 字体配置

2. **继续标记剩余文件**
   - BKdialogue.rpy（对话系统，约986KB）
   - BKmain.rpy（主循环中的用户可见字符串）
   - BKfarm.rpy（农场相关文本）
   - BKsecurity.rpy（安全系统文本）
   - Mods/ 目录下的模组文本

3. **测试翻译系统**
   - 启动游戏，验证语言切换功能
   - 检查中文是否正确显示
   - 测试翻译文件是否正确加载

### 中优先级
4. **剧情文本处理**
   - Ren'Py 的 say 语句会自动生成 translate 块，通常不需要手动 `_()`
   - 但需要检查 narrator 文本和特殊对话格式
   - 对于大量剧情文本，建议使用 Ren'Py Launcher 的 Generate Translations 功能

5. **翻译工作流优化**
   - 提供翻译者指南
   - 设置翻译更新脚本
   - 建立翻译贡献流程

## Git提交历史
- `Initial commit`: 添加项目文件、gitignore、翻译框架
- `Add translation directory structure`: 创建tl目录和占位文件
- `i18n: Mark UI strings in BKscreens.rpy`: 414处UI文本标记
- `i18n: Mark translatable strings in BKinit_variables.rpy`: 系统变量和描述文本标记
- `i18n: Mark character names in BKdeclarations.rpy`: 72处角色名称标记
- `i18n: Mark screen UI strings in...`: 多个文件的screen文本标记
- `i18n: Mark menu option texts in剧情 and event files`: 220处菜单选项标记
- `i18n: Mark description/name kwargs in spells, perks, powers, postings`: 274处参数标记
- `i18n: Mark description/name kwargs in classes, functions, events`: 79处参数标记
- `i18n: Generate translation template files with 3395 unique strings`
- `i18n: Add language selector in preferences and CJK font configuration`
