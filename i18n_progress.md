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
- [x] **BKscreens.rpy** (414+处修改)
  - 标记了 text、textbutton、tooltip、label、tt.Action 中的用户可见文本
- [x] **BKinit_variables.rpy** (大量修改)
  - 标记了 random_tips 列表项
  - 标记了 diff_name、diff_description、diff_setting_name、diff_setting_description
  - 标记了 MC/god/alignment/farm 描述字典
- [x] **BKdeclarations.rpy** (82处修改)
  - 标记了 Character() 定义中的角色名称
  - 标记了 CG Gallery 中的 UI 文本
- [x] **BKitems.rpy / BKhelp.rpy / BKendday.rpy / BKscreen_home.rpy / BKcontent_menu.rpy**
  - 标记了 screen 语言中的 UI 文本
- [x] **剧情和事件文件** (220+处修改)
  - 标记了 menu 选项文本
- [x] **BKspells.rpy / BKperks.rpy / BKpowers.rpy / BKpostings.rpy** (274处修改)
  - 标记了 Spell/Moon/Perk/Power 的 description 和 name 参数
- [x] **BKclasses.rpy / BKfunctions.rpy / BKgirlclass.rpy** (79处修改)
  - 标记了 description/name 等关键字参数
- [x] **BKmain.rpy / BKfarm.rpy / BKsecurity.rpy / BKstart.rpy / BKminigame.rpy**
  - 标记了 menu 选项和 kwargs
- [x] **BKsettings.rpy** (139处修改)
  - 标记了 stat_name_dict 值
- [x] **Mods/** (3处修改)
  - 标记了模组中的 UI 文本

### Phase 2: 翻译模板与UI配置 ✅
- [x] **生成翻译模板**
  - 提取了 4754 处字符串，**3727 个唯一字符串**
  - 生成了 `game/tl/english/strings.rpy`
  - 生成了 `game/tl/chinese/strings.rpy`
  - 生成了 `game/tl/chinese_simplified/strings.rpy`
- [x] **添加语言选择界面**
  - 在 preferences screen (screens.rpy) 添加了语言选择框
  - 支持 English / 中文 / 简体中文
- [x] **CJK字体配置**
  - 在 gui.rpy 添加了 CJK 字体配置注释
  - 在 translations.rpy 中添加了语言切换时的字体自动切换逻辑

## 统计汇总

| 类别 | 数量 |
|------|------|
| 修改的文件数 | 30+ |
| Git 提交数 | 15+ |
| 提取的字符串位置 | 4754 |
| 唯一可翻译字符串 | **3727** |
| 已创建工具脚本 | 7 |

## 已创建的工具脚本

| 脚本 | 用途 |
|------|------|
| `mark_translations.py` | 标记 screen 语言中的可翻译字符串 |
| `mark_lists.py` | 标记列表变量中的字符串项 |
| `mark_dict_values.py` | 标记字典变量中的值（不标记键） |
| `mark_characters.py` | 标记 Character() 定义中的角色名称 |
| `mark_menus.py` | 标记 menu 选项文本 |
| `mark_kwargs.py` | 标记函数调用中的 description/name 等参数 |
| `extract_translations.py` | 提取所有标记字符串，生成 Ren'Py 翻译文件 |

## 使用说明

### 添加翻译
1. 打开 `game/tl/chinese/strings.rpy`（或对应的语言文件）
2. 在 `new ""` 中填入翻译文本
3. 示例：
   ```renpy
   old "Hello"
   new "你好"
   ```

### 添加CJK字体
1. 下载支持中文的字体（推荐：Noto Sans CJK SC）
2. 将字体文件放入 `game/` 目录
3. 在 `game/gui.rpy` 中取消注释 CJK 字体配置行
4. 修改字体文件名以匹配实际文件

### 切换语言
1. 在游戏中打开 Options / Preferences
2. 选择 Language 下的选项
3. 游戏会自动切换语言和字体

## 已知限制与待办事项

### 仍需处理的内容
- [ ] **剧情对话文本**: Ren'Py 的 say 语句会自动生成 translate 块，不需要手动 `_()`。但大量剧情文本（intro, chapter1-3, events, dialogue）需要实际的翻译工作。
- [ ] **表达式中的字符串**: 如 `text " (%s mood)" % plus_text(...)` 需要手动重构为 `text __(" (%s mood)") % plus_text(...)`
- [ ] **图片内嵌文本**: 如果游戏中有文字内嵌在图片中，需要重新制图
- [ ] **CJK字体文件**: 需要下载并配置中文字体文件

### 建议的后续步骤
1. 下载 Noto Sans CJK SC 字体并配置
2. 启动游戏测试语言切换功能
3. 开始实际翻译工作（从最常用的UI文本开始）
4. 使用 Ren'Py Launcher 的 Generate Translations 功能补充对话文本的翻译模板
