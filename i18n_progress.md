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
  - 语言映射配置
  - 语言切换函数 `bk_set_language()`
  - 启动时自动应用语言

### Phase 1: 核心系统文件（进行中）
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
- [ ] **BKdeclarations.rpy** - 角色声明中的名称需要标记
- [ ] **BKfunctions.rpy** - 函数中的用户可见字符串
- [ ] **BKclasses.rpy** - 类中的用户可见字符串
- [ ] **BKsettings.rpy** - 设置中的用户可见字符串
- [ ] **BKitems.rpy** - 物品描述
- [ ] **BKtraits.rpy** - 特质描述
- [ ] **BKspells.rpy** - 法术描述
- [ ] **BKpowers.rpy** - 能力描述
- [ ] **BKachievements.rpy** - 成就描述

### Phase 2: 游戏内容文本（待开始）
- [ ] **BKintro.rpy** - 游戏开场
- [ ] **BKchapter1.rpy / BKchapter2.rpy / BKchapter3.rpy** - 主线剧情（约2.2MB）
- [ ] **BKevents.rpy / BKday_events.rpy / BKcity_events.rpy** - 事件系统（约800KB）
- [ ] **BKdialogue.rpy** - 对话系统（约986KB）
- [ ] **BKstory_events.rpy / BKinteractions.rpy** - 互动与故事事件
- [ ] **BKhelp.rpy** - 帮助文本
- [ ] **NPC/ 子目录** - 角色相关文本
- [ ] **Mods/** - 模组文本

### Phase 3: 生成翻译文件与测试（待开始）
- [ ] 生成 `game/tl/<language>/strings.rpy`
- [ ] 为中文添加CJK字体支持
- [ ] 测试语言切换功能

## 已创建的工具脚本

### `game/tools/mark_translations.py`
- **用途**: 标记 screen 语言中的可翻译字符串
- **支持模式**: screen / python / auto
- **标记规则**: 
  - text "..." → text _("...")
  - textbutton "..." → textbutton _("...")
  - tooltip "..." → tooltip _("...")
  - tt.Action("...") → tt.Action(_("..."))
- **排除项**: 表达式中的字符串（+、%、)等操作符后）、图片标签、纯格式字符串

### `game/tools/mark_lists.py`
- **用途**: 标记特定列表变量中的字符串项
- **默认目标**: random_tips, tip_list
- **标记方式**: "text" → __("text")

### `game/tools/mark_dict_values.py`
- **用途**: 标记特定字典变量中的值（不标记键）
- **默认目标**: diff_name, diff_description, diff_setting_name, diff_setting_description
- **标记方式**: "key" : "value" → "key" : __("value")

### `game/tools/check_errors.py`
- **用途**: 检查翻译标记后的常见语法错误

## 已知问题与注意事项

1. **DynamicCharacter变量名**: 如 `DynamicCharacter("MC.name")` 中的 `"MC.name"` 是变量引用，不应翻译
2. **表达式中的字符串**: 如 `text " (%s mood)" % plus_text(...)` 需要手动重构为 `text __(" (%s mood)") % plus_text(...)`
3. **图片/图标名称**: 如 `"tb willow"`, `"side homura"` 是内部标识符，不应翻译
4. **罗马数字**: `"I"`, `"II"` 等通常不需要翻译
5. **字典键**: 代码使用的键（如 `"gold"`, `"stats"`）不应翻译

## 下一步行动

### 立即行动
1. 修复并应用 `mark_characters.py` 脚本（排除变量引用）
2. 继续处理 BKdeclarations.rpy 中的其他声明
3. 处理 BKfunctions.rpy 和 BKclasses.rpy 中的错误/提示消息

### 后续行动
4. 处理 BKitems.rpy、BKtraits.rpy 等声明文件
5. 处理剧情文本（intro, chapter1-3）
6. 处理事件和对话文本
7. 生成翻译模板文件
8. 添加中文字体支持
9. 测试并修复问题

## Git提交历史
- `Initial commit`: 添加项目文件、gitignore、翻译框架
- `Add translation directory structure`: 创建tl目录和占位文件
- `i18n: Mark UI strings in BKscreens.rpy`: 414处UI文本标记
- `i18n: Mark translatable strings in BKinit_variables.rpy`: 系统变量和描述文本标记
