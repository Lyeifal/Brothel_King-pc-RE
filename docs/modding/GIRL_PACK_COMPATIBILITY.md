# Brothel King - 女孩包兼容性指南

> 版本: 2026-10-13
> 目标读者: 女孩包作者和用户

---

## 📚 目录

1. [女孩包基础](#女孩包基础)
2. [_BK.ini 格式详解](#bkini-格式详解)
3. [兼容性检查](#兼容性检查)
4. [常见问题](#常见问题)
5. [升级指南](#升级指南)

---

## 📦 女孩包基础

### 什么是女孩包？

女孩包是包含女孩角色数据和图片的文件夹，放置在 `game/custom/girls/` 目录下。

### 标准女孩包结构

```
game/custom/girls/
└── Girl Name/
    ├── _BK.ini              # 女孩配置文件（必需）
    ├── profile (001).jpg    # 档案图片
    ├── nude (001).jpg       # 裸体图片
    ├── sex (001).jpg        # 性爱图片
    └── ...                  # 更多图片
```

### 图片命名规范

图片文件名由**标签**和**编号**组成：

```
<标签1> <标签2> ... (<编号>).<扩展名>

示例:
- profile (001).jpg          # 档案图片
- nude big (001).png         # 裸体 + 大胸
- sex anal cumshot (002).webp # 性爱 + 肛交 + 射精
```

**支持的图片格式**: `.jpg`, `.png`, `.webp`, `.avif`

**常用标签**:
- `profile` - 档案
- `nude` - 裸体
- `sex` - 性爱
- `service` - 服务
- `anal` - 肛交
- `group` - 多人
- `cumshot` - 射精
- 查看完整标签列表: `game/core/data/tags/` 下的JSON文件

---

## 📄 _BK.ini 格式详解

### 基础结构

`_BK.ini` 是女孩包的配置文件，使用INI格式：

```ini
#### 女孩名 - BK.ini 配置文件

[identity]
first_name = "爱丽丝"
last_name = "史密斯"
creator = "Your Name"

[base skills]
charm = 4
beauty = 3
body = 5
refinement = 4

[background story]
origin_story = "她来自一个富裕家庭..."
```

### 完整字段说明

#### Section: [identity]

| 字段 | 类型 | 必需？ | 说明 | 示例 |
|------|------|--------|------|------|
| `first_name` | 字符串 | ✅ | 名字 | `"爱丽丝"` |
| `last_name` | 字符串 | ❌ | 姓氏 | `"史密斯"` |
| `inverted_name` | 布尔 | ❌ | 姓在前（中文习惯） | `True` |
| `creator` | 字符串 | ❌ | 女孩包作者 | `"Your Name"` |

#### Section: [base skills]

女孩的初始属性（1-5，1最差，5最好，0随机）：

| 字段 | 说明 | 影响 |
|------|------|------|
| `charm` | 魅力 | 服务员工作/性服侍 |
| `beauty` | 美貌 | 按摩师工作/性交 |
| `body` | 身材 | 舞娘工作/肛交 |
| `refinement` | 优雅 | 艺妓工作/BDSM |
| `sensitivity` | 敏感度 | 性服侍/满意度 |
| `libido` | 性欲 | 性交/顾客满意 |
| `constitution` | 体格 | 肛交/精力 |
| `obedience` | 服从度 | BDSM/驯服 |

示例:
```ini
[base skills]
charm = 4
beauty = 3
body = 5
refinement = 4
sensitivity = 3
libido = 3
constitution = 2
obedience = 3
```

#### Section: [base positive traits]

女孩的正面特质（逗号分隔）：

```ini
[base positive traits]
traits = "Beautiful, Sexy, Loyal"
```

常用正面特质:
- `Beautiful` - 美丽
- `Sexy` - 性感
- `Loyal` - 忠诚
- `Energetic` - 精力充沛
- `Graceful` - 优雅
- 查看完整列表: `game/core/data/traits/traits.json`

#### Section: [base negative traits]

女孩的负面特质：

```ini
[base negative traits]
traits = "Shy, Weak"
```

常用负面特质:
- `Shy` - 害羞
- `Weak` - 虚弱
- `Stubborn` - 固执
- `Lazy` - 懒惰

#### Section: [background story]

| 字段 | 说明 | 示例 |
|------|------|------|
| `origin_story` | 背景故事文本 | `"她来自..."` |
| `generate_as` | 生成类型 | `"slave"` 或 `"free"` 或 `"all"` |
| `generate_in` | 生成地点 | `"slums"` 或 `"market"` 等 |
| `init_level` | 初始等级 | `1` 到 `7` |

示例:
```ini
[background story]
origin_story = "她曾是贵族的女儿，但家族没落后流落街头。"
generate_as = "all"
generate_in = "all"
init_level = 1
```

#### Section: [sexual preferences]

性偏好设置：

```ini
[sexual preferences]
acts = "anal: 0, oral: 1"  # -1=讨厌, 0=中立, 1=喜欢
```

#### Section: [cloning options]

克隆选项（高级）：

```ini
[cloning options]
unique = False  # 是否唯一（只能生成一次）
```

### 最小可用 _BK.ini

如果你想快速创建一个女孩包，这是最少必需的内容：

```ini
[identity]
first_name = "Test Girl"

[base skills]
charm = 0
beauty = 0
body = 0
refinement = 0
sensitivity = 0
libido = 0
constitution = 0
obedience = 0
```

**注意**: 所有技能设为0会随机生成数值

---

## ✅ 兼容性检查

### 自动检查工具

运行女孩包验证工具：

```bash
python tools/test_girl_packs.py
```

输出示例:
```
✅ Girl Pack 1
⚠️  Girl Pack 2
    警告: 图片目录为空
❌ Girl Pack 3
    错误: 缺少 _BK.ini 文件
```

### 手动检查清单

- [ ] `_BK.ini` 文件存在
- [ ] `[identity]` section 存在
- [ ] `first_name` 字段有值
- [ ] 至少有一张图片文件
- [ ] 图片文件名符合标签格式
- [ ] 图片格式是 jpg/png/webp/avif
- [ ] 文件编码是 UTF-8

### 常见兼容性问题

#### 问题1: 女孩无法在游戏中生成

**可能原因**:
- `_BK.ini` 缺失或格式错误
- `first_name` 为空
- 图片目录为空

**解决**:
1. 检查 `_BK.ini` 是否存在且格式正确
2. 确保 `[identity]` section 和 `first_name` 存在
3. 确保女孩包文件夹内至少有一张图片

#### 问题2: 女孩图片不显示

**可能原因**:
- 图片文件名不符合标签格式
- 图片文件损坏
- 图片格式不支持

**解决**:
1. 确保图片文件名包含标签（如 `profile`, `nude`等）
2. 确保图片文件名包含编号 `(001)`
3. 使用支持的图片格式
4. 测试图片能否用图片查看器打开

#### 问题3: 女孩属性异常

**可能原因**:
- `[base skills]` 数值超出范围（应该0-5）
- 特质名称拼写错误

**解决**:
1. 检查所有技能数值在 0-5 范围内
2. 对照 `game/core/data/traits/traits.json` 检查特质名称

#### 问题4: 中文乱码

**可能原因**:
- `_BK.ini` 文件编码不是 UTF-8

**解决**:
1. 用文本编辑器打开 `_BK.ini`
2. 另存为 UTF-8 编码（带BOM或无BOM都可以）
3. 推荐使用 VSCode 或 Notepad++ 编辑

---

## 🔄 升级指南

### 从旧版BK升级女孩包

BK Evolution 重构后，大部分旧女孩包**无需修改**即可使用，但建议检查以下内容：

#### 检查1: 文件编码

旧版可能使用了非UTF-8编码，建议转换：

1. 用 VSCode 打开 `_BK.ini`
2. 右下角点击编码（如 GBK）
3. 选择 "Save with Encoding" → "UTF-8"

#### 检查2: 特质名称

部分特质在新版中可能被重命名或移除，运行验证工具检查：

```bash
python tools/test_girl_packs.py --pack "你的女孩包名"
```

如果特质不存在，会显示警告。

#### 检查3: 图片标签

新版使用更标准化的标签系统，确保图片标签与 `game/core/data/tags/` 中的定义匹配。

### 添加新版特性

#### 特性1: 多语言支持

在女孩包内添加翻译：

```
Girl Pack/
├── _BK.ini
├── tl/
│   └── chinese_simplified/
│       └── translations.rpy
└── ...
```

`translations.rpy` 内容:
```renpy
translate chinese_simplified strings:
    old "Original English text"
    new "中文翻译"
```

#### 特性2: 自定义标签

在 `_BK.ini` 中定义自定义标签：

```ini
[custom tags]
my_tag = "tag1, tag2, tag3"
```

#### 特性3: 自定义对话

```ini
[custom dialogue]
free_greetings_polite = "你好呀！"
```

---

## 🛠️ 女孩包开发工具

### 1. Girl Pack Editor（游戏内）

游戏内置的女孩包编辑器：

1. 启动游戏（开发者模式）
2. 主菜单 → "Girl Pack Editor"
3. 选择女孩包并编辑

功能:
- 可视化编辑 `_BK.ini`
- 预览图片
- 验证格式

### 2. 独立编辑器（GUI）

```bash
python tools/bk_editor/girl_pack_editor/main.py
```

功能:
- 创建新女孩包
- 批量处理图片
- 自动标签图片（部分功能）

### 3. 命令行验证工具

```bash
# 验证所有女孩包
python tools/test_girl_packs.py

# 验证单个女孩包
python tools/test_girl_packs.py --pack "Girl Name"

# 详细输出
python tools/test_girl_packs.py --verbose
```

---

## 📋 女孩包发布清单

准备发布女孩包时，请确认：

- [ ] `_BK.ini` 格式正确，字段完整
- [ ] 至少有 10 张图片（推荐50+）
- [ ] 图片覆盖主要标签（profile, nude, sex等）
- [ ] 图片质量良好（无水印、无严重瑕疵）
- [ ] 运行验证工具无错误
- [ ] 在游戏中测试过（能正常生成和显示）
- [ ] 包含 README.txt 说明（可选但推荐）
- [ ] 注明作者和来源（如果使用他人图片）
- [ ] 文件编码是 UTF-8

### README.txt 模板

```
女孩包名称: 
角色来源: 
作者: 
版本: 
创建日期: 

图片数量: 
特殊说明: 

感谢使用！
```

---

## 🤝 社区资源

### 女孩包下载

- 官方论坛: （论坛地址）
- 社区分享: （Discord/Reddit等）

### 需要帮助？

- 查看官方文档: `docs/README.md`
- 运行验证工具: `python tools/test_girl_packs.py`
- 社区求助: （社区链接）

---

## 📚 参考

- **标签列表**: `game/core/data/tags/tags.json`
- **特质列表**: `game/core/data/traits/traits.json`
- **女孩工厂**: `game/core/framework/girl_factory.rpy`
- **女孩包模板**: `game/core/templates/girl_template/`

---

**祝你创作出优秀的女孩包！** 🎨
