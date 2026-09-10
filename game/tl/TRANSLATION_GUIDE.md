# Brothel King 翻译系统说明文档

## 概述

本项目使用 Ren'Py 原生双轨翻译机制：

| 机制 | 用途 | 覆盖范围 |
|------|------|----------|
| `__()` / `_()` + `strings.rpy` | 代码字符串翻译 | UI 文本、菜单选项、数据层字符串、对话系统 |
| `translate` 块 | 剧情脚本翻译 | 主线/支线/事件对话、叙述文本 |

两种机制并行工作，互不冲突。译者需要分别处理。

---

## 目录结构

```
game/tl/
├── chinese_simplified/              # 游戏本体简体中文翻译（仅本体，不含 Mod）
│   ├── strings.rpy                  # 代码字符串翻译（_() / __()）
│   ├── common.rpy                   # Ren'Py 通用界面翻译
│   └── core/                        # 镜像 game/core/ 源码树的对话翻译
│       ├── content/                 #   剧情内容（intro、interactions、章节、事件…）
│       ├── framework/               #   框架层
│       ├── systems/                 #   系统层
│       └── ui/ …
└── TRANSLATION_GUIDE.md             # 本说明文档
```

**Mod 翻译不由本目录管理。** 每个 Mod 在自己的目录内自带翻译，
与 Mod 源码同址，随 Mod 一起安装/卸载：

```
game/custom/mods/<Mod名称>/
├── <mod源码>.rpy
└── tl/
    └── chinese_simplified/          # 该 Mod 的简体中文翻译
        └── <对应源码文件>.rpy
```

> Ren'Py 启动时递归扫描整个 game/ 目录加载 `translate` 块，
> 翻译文件放在 `game/tl/` 下还是 Mod 目录下效果完全相同。
> 约定：**本体翻译 → `game/tl/<语言>/`；Mod 翻译 → Mod 自带 `tl/<语言>/`**。

---

## 各文件说明

### 1. `strings.rpy` — 代码字符串翻译

**格式：**
```renpy
translate chinese_simplified strings:

    # game/BKscreens.rpy:42
    old "Game settings"
    new "游戏设置"

    # TODO game/BKdialogue.rpy:151
    old "My, I didn't expect to meet a true gentleman here!"
    new "My, I didn't expect to meet a true gentleman here!"
```

**说明：**
- `old` 为原始英文，`new` 为翻译后的中文
- `# TODO` 标记表示该条目尚未翻译（`new` 与 `old` 相同）
- 来源格式：`# <文件路径>:<行号>`
- **不可手动编辑 `old` 值**，否则 Ren'Py 会找不到对应的源字符串
- 所有 `_()` 和 `__()` 调用的字符串最终都汇总到此文件

**当前规模：** ~10,192 条总条目，~2,280 条已翻译，~7,912 条待翻译

**主要来源：**
- `game/BKdialogue.rpy` — 4,448 条女孩对话（Phase 3 新增）
- `game/BKscreens.rpy` / `screens.rpy` — UI 文本
- `game/data/*.rpy` — 数据层（难度名称、属性名、工作描述等）
- `game/BKclasses.rpy` / `BKfunctions.rpy` — 核心代码字符串
- 各章节/事件文件中的 `_()` 调用

---

### 2. 剧情翻译文件 (`BKchapter*.rpy`, `BKstory_events.rpy`, etc.)

**格式：**
```renpy
translate chinese_simplified c1_guards_visit_4d36ba71:
    # kosmo happy "Oh, nothing, nothing..."
    kosmo happy "Oh, nothing, nothing..."
```

**说明：**
- 每个 `translate chinese_simplified <hash>:` 块对应源文件中的一句对话/叙述
- `#` 注释行是 Ren'Py 自动生成的原始文本参考
- 实际翻译需修改下方的 `kosmo happy "..."` 行
- 这些文件**不应包含** `translate chinese_simplified strings:` 块（已统一合并到 `strings.rpy`）

**翻译方法：**
1. 找到对应源文件中的对话行（通过 hash 或上下文）
2. 将 `translate` 块中的目标语言行替换为中文
3. 保留角色标签（如 `kosmo happy`、`narrator`、`you`）

**示例：**
```renpy
# 翻译前
translate chinese_simplified c1_guards_visit_4d36ba71:
    # kosmo happy "Oh, nothing, nothing..."
    kosmo happy "Oh, nothing, nothing..."

# 翻译后
translate chinese_simplified c1_guards_visit_4d36ba71:
    # kosmo happy "Oh, nothing, nothing..."
    kosmo happy "哦，没什么，没什么..."
```

---

### 3. `common.rpy` — 通用界面翻译

包含 Ren'Py 通用提示、按钮、错误消息等。这些通常是 Ren'Py 框架级别的字符串。

---

### 4. `screens.rpy` — 屏幕界面翻译

包含 Ren'Py 标准屏幕（如保存/加载界面、设置界面）的翻译。

---

## 数据层翻译 (`game/data/`)

静态数据已从主代码中提取到 `game/data/` 目录：

| 文件 | 内容 | 翻译方式 |
|------|------|----------|
| `jobs.rpy` | `perform_job_dict` — 工作描述、性行为描述 | `__()` 包裹，进入 `strings.rpy` |
| `settings.rpy` | 难度名称、设置项、属性名称 | `__()` 包裹，进入 `strings.rpy` |
| `perks.rpy` | 天赋名称、描述 | `__()` 包裹，进入 `strings.rpy` |
| `powers.rpy` | 邪恶力量名称、描述 | `__()` 包裹，进入 `strings.rpy` |
| `items.rpy` | 物品名称、描述 | `__()` 包裹，进入 `strings.rpy` |

**注意：** 数据层文件中的字符串字面量已包裹 `__()`，Ren'Py 翻译提取器会自动找到它们。

---

## 对话系统翻译 (`game/BKdialogue.rpy`)

Phase 3 已完成重构：所有 `add_dialogue()` 的 `lines` 参数已包裹 `__()`。

```python
# 翻译前（Ren'Py 提取器找不到）
add_dialogue("free_greetings_polite", "generic", "Hello!")

# 翻译后（Ren'Py 提取器可找到）
add_dialogue("free_greetings_polite", "generic", __("Hello!"))
```

对话模板支持变量插值（如 `[girl.fullname]`、`[girl.origin]`），翻译时**必须保留**这些方括号变量。

多行对话格式：
```python
add_dialogue("topic", "key", [
    __("g: What do you want?"),
    __("mc: Just to talk."),
    __("g: Fine..."),
], multiple=True)
```

前缀说明：
- `g: ` — 女孩说的话
- `mc: ` — 主角（MC）说的话
- `giz: ` — Gizel 说的话
- 无前缀 — 旁白

**注意：** 前缀在显示时会自动剥离，不需要在翻译中保留前缀。但当前实现中前缀属于字符串的一部分，所以翻译时请保留前缀并翻译后面的内容。

---

## Mod 翻译 (`game/Mods/` 和 `game/tl/chinese_simplified/Mods/`)

Mod 是独立的 `.rpy` 文件，Ren'Py 翻译系统会自动提取其中的 `_()` 和 `__()` 调用。

- Mod 源码：`game/Mods/<mod_name>/<mod_name>.rpy`
- Mod 翻译：`game/tl/chinese_simplified/Mods/<mod_name>/<mod_name>.rpy`

**重要：** Mod 的 `name` 参数**不应**包裹 `__()`，因为它是字典键，切换语言会导致持久化丢失。

```python
# 错误（会导致语言切换后 Mod 失效）
name = __("Goldo's cool mod")

# 正确
name = "Goldo's cool mod"
```

---

## 角色包翻译边界 (`game/girls/`)

**角色包不由主游戏仓库追踪**，其文本也不在 Ren'Py 翻译系统范围内：

| 内容 | 是否可翻译 | 说明 |
|------|-----------|------|
| `_BK.ini` 中的 `origin_description` | ❌ 不由主游戏处理 | 角色包作者自行负责 |
| `_BK.ini` 中的 `description` | ❌ 不由主游戏处理 | 角色包作者自行负责 |
| `_BK.ini` 中的 `custom personality/description` | ❌ 不由主游戏处理 | 角色包作者自行负责 |
| 图片文件名标签 | ❌ 不需要翻译 | 内部系统标签，如 `sex doggy cumshot` |
| 角色包内自定义 `.rpy` 脚本 | ✅ 可由 Ren'Py 提取 | 若包含 `_()`/`__()` 则自动进入翻译系统 |

**推荐做法：** 角色包作者直接在 `_BK.ini` 中写入目标语言文本，或随包附带翻译文件。

---

## 翻译工作流

### 更新 `strings.rpy`

当源码中的 `_()`/`__()` 字符串发生变化时，运行：

```bash
python merge_translations.py
```

此脚本会：
1. 扫描所有 `.rpy` 文件中的 `_()` 和 `__()` 调用
2. 读取现有 `strings.rpy` 的翻译
3. 保留已有翻译，新增字符串使用英文 fallback
4. 生成新的 `strings.rpy`

### 翻译剧情文件

剧情翻译文件（`BKchapter*.rpy` 等）通常通过 Ren'Py SDK 的 **Generate Translations** 功能自动生成脚手架。手动翻译时：

1. 打开对应的 `.rpy` 翻译文件
2. 找到未翻译的 `translate` 块
3. 将下方的对话/叙述行替换为中文

### 翻译数据层

数据层字符串统一进入 `strings.rpy`。直接编辑 `strings.rpy` 中对应的 `new` 值即可。

---

## 注意事项

1. **不要手动修改 `old` 值**：Ren'Py 通过 `old` 值查找对应的源字符串，修改 `old` 会导致翻译失效。
2. **保留变量插值**：翻译时必须保留 `[variable]` 和 `{tag}` 语法。
3. **避免重复 `strings:` 块**：所有 `translate chinese_simplified strings:` 块必须仅在 `strings.rpy` 中定义。剧情翻译文件中不应包含 `strings:` 块（已由 `merge_tl_strings.py` 清理）。
4. **备份旧 `strings.rpy`**：运行 `merge_translations.py` 前会自动创建 `.backup` 文件。
5. **CJK 字体已配置**：`game/NotoSansCJKsc-Regular.otf` 已配置为简体中文显示字体。

---

## 统计（截至 Phase 3 完成）

| 类别 | 数量 |
|------|------|
| `strings.rpy` 总条目 | ~10,192 |
| `strings.rpy` 已翻译 | ~2,280 |
| `strings.rpy` 待翻译 | ~7,912 |
| 剧情文件总行数 | ~77,000+ |
| 对话系统字符串 | ~4,448 |

---

## 相关脚本

| 脚本 | 用途 |
|------|------|
| `merge_translations.py` | 扫描 `_()`/`__()` 并重新生成 `strings.rpy` |
| `merge_tl_strings.py` | 清理剧情文件中的重复 `strings:` 块 |
| `wrap_dialogue.py` | 给 `BKdialogue.rpy` 的 `add_dialogue()` 包裹 `__()` |
| `restore_lost.py` | 从 git 历史恢复丢失的翻译 |
