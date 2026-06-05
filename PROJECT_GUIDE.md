# Brothel King 项目指南

> 本文档说明项目目录结构、核心代码组织方式以及翻译工作流。

---

## 项目简介

**Brothel King** 是一款基于 Ren'Py 8.2.0 引擎开发的成人向模拟经营/视觉小说游戏。玩家经营一家妓院，管理女孩、接客、升级设施、探索剧情。

- **引擎**: Ren'Py 8.2.0 (Python 3.9)
- **版本**: Bro King 0.3 v260527
- **语言**: 英文原版 + 简体中文翻译 (`zh-Hans`)
- **平台**: Windows / Linux / macOS

---

## 目录结构

### 根目录

```
Brothel_King-pc/
├── Brothel_King.exe      # Windows 启动器
├── Brothel_King.py       # Python 启动脚本
├── Brothel_King.sh       # Linux/macOS 启动脚本
├── lib/                  # Python 运行时库（按平台分类）
│   ├── py3-windows-x86_64/
│   ├── py3-linux-x86_64/
│   └── python3.9/
├── renpy/                # Ren'Py 引擎源码
├── game/                 # 游戏主目录（所有脚本和资源）
├── tools/                # 翻译和开发工具脚本
├── README.html           # 项目说明（HTML）
├── faq.txt               # 常见问题
├── errors.txt            # 错误日志
├── log.txt               # 运行日志
└── traceback.txt         # 崩溃回溯
```

### game/ 主目录

#### 核心脚本（根目录 .rpy 文件）

| 文件 | 说明 |
|------|------|
| `BKmain.rpy` | 主游戏循环、妓院主屏幕逻辑 |
| `BKscreens.rpy` | **核心屏幕定义**（UI布局、按钮、文本显示等） |
| `BKstart.rpy` | 游戏启动、新游戏/继续游戏流程 |
| `BKintro.rpy` | 开场剧情、角色创建 |
| `BKchapter1.rpy` ~ `BKchapter3.rpy` | 主线剧情章节 |
| `BKstory_events.rpy` | 故事事件系统 |
| `BKcity_events.rpy` | 城市探索事件 |
| `BKday_events.rpy` | 每日随机事件 |
| `BKdialogue.rpy` | 对话系统、`add_dialogue()` 定义 |
| `BKgirlclass.rpy` | `Girl` 类定义（女孩属性、行为） |
| `BKclasses.rpy` | 其他核心类定义 |
| `BKfunctions.rpy` | 通用工具函数库 |
| `BKinteractions.rpy` / `BKinteractions_free.rpy` | 女孩互动系统 |
| `BKfarm.rpy` | 农场/寄养系统 |
| `BKsecurity.rpy` | 安保/冲突系统 |
| `BKminigame.rpy` | 小游戏逻辑 |
| `BKitems.rpy` | 物品系统 |
| `BKtraits.rpy` | 特质/性格系统 |
| `BKperks.rpy` | 技能/特长系统 |
| `BKspells.rpy` | 法术系统 |
| `BKpowers.rpy` | 能力/权力系统 |
| `BKachievements.rpy` | 成就系统 |
| `BKsettings.rpy` | 游戏设置、配置变量 |
| `BKdeclarations.rpy` / `BKinit_variables.rpy` | 变量声明与初始化 |
| `BKhelp.rpy` | 帮助/教程系统 |
| `BKendday.rpy` | 每日结算逻辑 |
| `BKpostings.rpy` | 告示/任务发布系统 |
| `BKdist.rpy` | 街区/区域管理系统 |
| `BKcontent_menu.rpy` | 内容菜单 |
| `BKevents.rpy` | 事件调度系统 |
| `gui.rpy` / `screens.rpy` / `options.rpy` | Ren'Py 标准配置文件 |
| `translations.rpy` | 翻译相关配置 |

#### 资源子目录

| 目录 | 内容 |
|------|------|
| `backgrounds/` | 场景背景图片 |
| `brothels/` | 妓院建筑、房间图片 |
| `girls/` | 女孩立绘、头像 |
| `MC/` | 主角（玩家角色）立绘 |
| `NPC/` | NPC 角色资源 |
| `default/` | 默认/通用角色头像 |
| `events/` | 事件 CG/插图 |
| `districts/` | 街区地图图片 |
| `items/` | 物品图标 |
| `perks/` | 技能/特长图标 |
| `spells/` | 法术图标 |
| `gui/` | GUI 界面图片素材 |
| `UI/` | UI 界面元素 |
| `music/` | 背景音乐 |
| `sounds/` | 音效 |
| `transitions/` | 转场动画效果 |

#### 数据与配置

| 目录 | 内容 |
|------|------|
| `data/` | 游戏数据文件（CSV/JSON/XML） |
| `cache/` | 运行时缓存（可安全删除） |
| `saves/` | 玩家存档 |

#### 模组

| 目录 | 内容 |
|------|------|
| `Mods/` | 模组目录（原版包含 `Goldo's cool mod` 示例模组） |

> **注意**: 模组（Mod）翻译文件已移除。游戏 `tl/` 目录下不再包含 `Mods/` 翻译，Mod 内容保持英文原文。

#### 翻译文件

| 目录 | 内容 |
|------|------|
| `tl/chinese_simplified/strings.rpy` | **字符串翻译文件**（`__()` / `_()` 调用的翻译） |
| `tl/chinese_simplified/*.rpy` | **剧情对话翻译文件**（Ren'Py `translate` 块） |

> 翻译采用双轨制：
> - `strings.rpy` 处理代码中的 `__()` / `_()` 字符串
> - 各章节 `.rpy` 文件处理对话文本的 `translate chinese_simplified` 块

---

## 翻译工作流

### 目录

所有翻译脚本统一存放在项目根目录的 `tools/` 文件夹中。

### 标准流程

```bash
# 1. 查找未翻译内容
python tools/find_untranslated.py
# 输出: to_translate_remaining.xlsx

# 2. 使用 Google Translate / DeepL 翻译 xlsx
# 保存为 to_translated_remaining.xlsx

# 3. 导入翻译
python tools/import_translated_remaining.py

# 4. 机器翻译后修复（必须按顺序！）
python tools/fix_all_variables.py      # 修复 [variable] 变量名
python tools/fix_placeholders.py       # 修复 %s 占位符
python tools/fix_all_tag_mismatches.py # 修复 {b}/{color} 标签

# 5. 验证
python tools/verify_strings.py

# 6. 清理缓存并测试
Remove-Item -Recurse -Path game\cache
Remove-Item -Path game\*.rpyc
Remove-Item -Path game\**\*.rpyc -Recurse
```

### 常见问题修复

| 报错 | 原因 | 解决 |
|------|------|------|
| `NameError: Name 'xxx' is not defined` | 变量名被翻译成了中文 | `python tools/fix_all_variables.py` |
| `/x closes a text tag that isn't open` | 文本标签不匹配 | `python tools/fix_all_tag_mismatches.py` |
| `TypeError: not all arguments converted` | `%s` 占位符丢失 | `python tools/fix_placeholders.py` |
| `A translation for "..." already exists` | 重复 `old` 键 | `python tools/remove_duplicates.py` |

详细说明请参阅 `tools/README.md`。

---

## 核心代码架构

### 1. 屏幕系统 (`BKscreens.rpy`)

游戏最核心的 UI 定义文件，包含：
- 妓房主界面 (`screen brothel()`)
- 女孩管理界面
- 商店/升级界面
- 对话/事件显示框

### 2. 女孩系统 (`BKgirlclass.rpy`)

`Girl` 类定义了所有女孩属性：
- 基础属性：名字、等级、职业、性格
- 工作属性：卖淫、服务、舞蹈、按摩等技能
- 身体属性：外貌、身材、敏感部位
- 状态：心情、健康、能量、服从度等

### 3. 事件系统 (`BKstory_events.rpy` / `BKcity_events.rpy` / `BKday_events.rpy`)

三种事件：
- **Story Events**: 主线剧情事件
- **City Events**: 城市探索触发的事件
- **Day Events**: 每日随机事件

### 4. 对话系统 (`BKdialogue.rpy`)

通过 `add_dialogue()` 函数注册对话，支持条件触发和随机选择。

### 5. 经营系统 (`BKmain.rpy` / `BKfarm.rpy` / `BKsecurity.rpy`)

- **主经营**: 接客、分配工作、管理设施
- **农场**: 将女孩送去农场进行特殊训练/工作
- **安保**: 处理顾客冲突、保护女孩

---

## 开发注意事项

1. **修改 .rpy 后必须清理缓存**: Ren'Py 使用 `.rpyc` 缓存文件，修改源文件后如果游戏行为未变，请删除 `game/cache/` 和所有 `.rpyc` 文件。

2. **不要直接修改 `strings.rpy` 的格式**: `strings.rpy` 使用 Ren'Py 标准格式（`old`/`new` 成对出现），手动修改时务必保持格式一致。

3. **变量名保护**: 代码中的 `[girl.name]`、`[brothel.name]` 等是运行时变量，翻译时**不能**将其翻译成中文。机器翻译后的修复脚本会自动处理，但最好在翻译阶段就保护好这些标记。

4. **Mod 不翻译**: `game/Mods/` 下的内容保持英文，不生成也不维护 Mod 的翻译文件。

5. **Git 管理**: 翻译导入和修复后会产生大量变更，建议在执行批量操作前先提交当前状态，以便必要时回退。

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `tools/README.md` | 翻译工具详细使用说明 |
| `i18n_progress.md` | 翻译进度记录 |
| `game/tl/chinese_simplified/strings.rpy` | 字符串翻译主文件 |
