# BK Editor Suite

BK Evolution 编辑器套件，为 Brothel King 提供三个独立的可视化数据编辑器。

## 概述

| 编辑器 | 目标用户 | 核心职责 |
|--------|----------|----------|
| **女孩包编辑器** (`girl_pack_editor/`) | MOD 作者 | 图片打标、`_BK.ini` 编辑、自定义 Trait/Perk、包验证 |
| **剧本编辑器** (`scenario_editor/`) | 剧情/事件作者 | StoryEvent CRUD、剧本管理、地图/NPC/商店参考、对话标签扫描 |
| **开发控制台** (`dev_console/`) | 核心开发者 | 成就、难度、NG+、局外养成的 JSON 数据增删改查 |

---

## 目录结构

```
tools/bk_editor/
├── shared/                    # 共享基础库（所有编辑器共用）
│   ├── paths.py               # 项目路径常量
│   ├── json_io.py             # JSON 读写封装
│   ├── widgets.py             # tkinter 通用组件
│   ├── validators.py          # 字段校验
│   └── renpy_ref.py           # 延迟加载游戏内数据
│
├── girl_pack_editor/          # 女孩包编辑器
│   ├── main.py                # 启动入口
│   ├── editor.py              # 主窗口
│   └── tabs/
│       ├── image_tagger.py    # 图片批量打标
│       ├── ini_editor.py      # _BK.ini 可视化编辑
│       ├── trait_creator.py   # Trait/Perk 创建器
│       └── pack_validator.py  # 包完整性验证
│
├── scenario_editor/           # 剧本编辑器
│   ├── main.py                # 启动入口
│   ├── editor.py              # 主窗口
│   └── tabs/
│       ├── event_editor.py         # StoryEvent / sandbox events
│       ├── scenario_editor_tab.py  # 剧本包 (Scenario)
│       ├── district_editor.py      # District/Location 参考
│       ├── npc_editor.py           # NPC 参考
│       ├── shop_editor.py          # 商店设置参考
│       └── image_tag_editor.py     # 对话图片标签扫描
│
└── dev_console/               # 开发控制台
    ├── main.py                # 启动入口
    ├── editor.py              # 主窗口
    └── tabs/
        ├── achievement_editor.py   # achievements.json
        ├── difficulty_editor.py    # difficulty.json
        ├── ngp_editor.py           # ngp_settings.json
        ├── meta_editor.py          # meta_progression.json
        ├── i18n_editor.py          # i18n key 审查
        └── data_sync.py            # JSON 批量验证/格式化
```

---

## 环境要求

- **Python 3.9+**（与 Ren'Py 内置 Python 版本一致）
- **Windows / Linux / macOS**

### Python 依赖

```powershell
# 女孩包编辑器需要（图片预览）
pip install Pillow pillow-avif-plugin opencv-python
```

| 包 | 用途 | 必需 |
|---|---|---|
| `Pillow` | 图片预览（WebP/AVIF/常规格式） | 建议安装 |
| `pillow-avif-plugin` | AVIF 格式解码 | 建议安装 |
| `opencv-python` | 视频首帧提取（WebM/AVI/MPEG） | 建议安装 |

> 如果不安装 Pillow/OpenCV，女孩包编辑器仍可运行，但图片预览会显示占位提示。

---

## 启动方式

### 从项目根目录

```powershell
# 女孩包编辑器
python tools\bk_editor\girl_pack_editor\main.py

# 剧本编辑器
python tools\bk_editor\scenario_editor\main.py

# 开发控制台
python tools\bk_editor\dev_console\main.py
```

### 从 `tools/bk_editor/` 目录

```powershell
cd tools\bk_editor
python girl_pack_editor\main.py
python scenario_editor\main.py
python dev_console\main.py
```

---

## 女孩包编辑器 (Girl Pack Editor)

面向 MOD 作者的女孩包制作工具。启动后，顶部工具栏会自动列出 `game/custom/girls/` 下的所有女孩包，选择后即可开始编辑。

### 图片打标

- **左侧文件列表**：显示当前包内所有图片/视频文件（支持多选：Ctrl+点击、Shift+连续选择）
- **中间预览区**：显示第一张选中图片的预览
  - 支持格式：`.png` `.jpg` `.jpeg` `.webp` `.gif` `.bmp` `.avif`
  - 视频格式：`.webm` `.mkv` `.avi` `.mpg` `.mpeg`（通过 OpenCV 提取首帧）
- **右侧标签面板**：按 14 个分类组织所有标签按钮（频率、肖像/资料、情绪、休息/工作、裸露、地点、侍奉、性交、肛交、调教、多人/特殊、农场、癖好、射精/高潮）
  - 点击按钮 → 将对应模式词添加到所有选中文件名
  - 勾选「移除模式」→ 点击按钮从文件名中移除该标签
- **底部验证报告**：
  - 检查 `portrait` / `profile` 是否缺失
  - 拼写检查：识别疑似拼写错误（如 `sexy`→建议`sex`，`figth`→建议`fight`）
  - 场景覆盖：19 个游戏场景的标签需求覆盖状态
- **一键整理**：自动规范化所有图片文件名格式

### _BK.ini 编辑器

- 按 Section 分块表单编辑（identity、base skills、traits、personality、tastes、sexual preferences、background story 等）
- 自动识别 boolean / integer / list / string 字段类型
- traits/personality 列表字段提供下拉选择器（数据来自 `core/data/traits/traits.json` 与 `personalities/personalities.json`）
- 切换 Section 时自动保存当前 Section 的修改
- **注意**：保存时会移除原文件中的注释，如需保留请提前备份

### Trait / Perk 创建器

- 表单化创建自定义 Trait 或 Perk
- 使用共享 `EffectEditor` 组件实时编辑 Effect 链
- 保存到 `core/data/traits/traits.json` 或 `perks/perks.json`
- 支持已有条目双击加载修改

### 包验证器

- 检查 `portrait` / `profile` 图片是否存在
- 检查 `_BK.ini` 引用的 trait/personality 是否存在于 JSON 中
- 检查重复图片基名
- 检查子文件夹中的图片（可能未被游戏读取）
- 一键修复：自动重命名图片为 `portrait.ext` / `profile.ext`

---

## 剧本编辑器 (Scenario Editor)

面向剧情与事件作者的剧本编辑工具。

### 事件编辑器

- **数据源切换**：可在 `stories/story_events.json` 与 `sandbox/events.json` 之间切换
- **完整 StoryEvent 表单**：label、chapter、rank、date、year、month、day、weekday、chance、type、location、locations、seasons、min_gold、condition、not_condition、room、once、AP_cost、order、weight、modes、call_args、description
- 树形列表展示所有事件，支持搜索过滤
- 增删改查并直接保存回 JSON

### 剧本管理

- `scenarios.json` 的增删改查
- 管理字段：scenario_id、name、description、author、version、events_script、starting_conditions、victory_conditions、rules
- starting_conditions / victory_conditions / rules 使用 JSON 文本区直接编辑

### 地图/地点参考

- **只读参考**：现有 6 个 District（The Slums / The Docks / The Warehouse / The Magic Gardens / The Cathedra / The King's Hold）和 36 个 Location 的完整列表
- 点击 District 可过滤显示其下属 Location
- **代码片段生成器**：一键生成添加新 District / Location 的 Python 代码模板

### NPC 编辑

- **商店 NPC 参考**：列出 10 位现有商人（Riche、Ramias、Gurigura 等）及其售卖类型、背景、肖像标签
- **特殊女孩 NPC 参考**：列出 3 位内置特殊女孩（艾拉腊女士、未来、伊尔莎军士）及其任务前缀、最低章节
- **代码片段生成器**：生成 `NPC(...)` 构造函数和 `SpecialGirlNPC` 注册代码

### 商店编辑

- **商店设置参考**：`shop_item_number`（库存骰子公式）和 `shop_chapter_modifiers`（章节修正表）
- **物品类型列表**：Weapon、Dress、Ring、Necklace、Accessory、Food、Gift 等
- **代码片段生成器**：生成 `Item(...)` 构造函数代码模板

### 对话图片标签

- **自动扫描**：遍历全部 `.rpy` 文件，提取 `{image=...}` 和 `emo_xxx` 标签
- **统计与上下文**：显示每个标签的出现次数，点击后显示最多 20 条上下文片段（包含文件路径）
- **搜索过滤**：支持实时搜索标签名
- **复制到剪贴板**：一键复制所有扫描到的标签列表

---

## 开发控制台 (Dev Console)

面向游戏核心开发者的数据控制台，所有数据直接读写 `game/core/data/` 下的 JSON 文件。

### 成就编辑器

- `achievements.json` 的增删改查
- 字段：name_i18n_key、description_i18n_key、target、requirements、multi、pic、hidden

### 难度编辑器

- `difficulty.json` 的 `diff_list` 顺序管理与 `diff_dict` 配置编辑
- 使用 Notebook 分两个标签页：`diff_list`（列表排序）与 `diff_dict`（键值编辑）

### NG+ 编辑器

- `ngp_settings.json` 的增删改查
- 字段：name、type、label、category、values、cost、ttip

### Meta 编辑器

- `meta_progression.json` 中 `meta_upgrades` 的增删改查
- 字段：upgrade_id、name_i18n_key、description_i18n_key、max_rank、cost_per_rank、effects、unlock_condition
- 支持动态添加/移除 Effect 编辑器

### I18n Keys 审查

- 只读审查从 achievements / meta / ngp JSON 中提取的所有国际化键名
- 按来源文件分组，支持搜索过滤
- 支持导出 CSV

### 数据同步

- 扫描 `core/data/` 下所有 JSON 文件
- 一键验证所有 JSON 的格式合法性
- 一键格式化所有 JSON（统一缩进）

---

## 共享库 (`shared/`)

各编辑器禁止跨目录引用，统一通过 `bk_editor.shared` 获取能力：

```python
from bk_editor.shared import (
    PROJECT_ROOT, GAME_DIR, DATA_DIR, GIRLS_DIR,
    load_json, save_json, merge_json,
    LabeledEntry, LabeledSpinbox, LabeledCombobox, LabeledCheckbox,
    EffectEditor, JsonTreeview,
)
```

### 组件说明

| 组件 | 用途 |
|---|---|
| `LabeledEntry` | 标签 + Entry 输入框，支持 get/set |
| `LabeledSpinbox` | 标签 + 数字选择框 |
| `LabeledCombobox` | 标签 + 下拉选择框 |
| `LabeledCheckbox` | 标签 + 复选框 |
| `EffectEditor` | 单条 Effect 对象的可视化编辑（type/target/value/scope） |
| `JsonTreeview` | 带索引 tag 的 JSON 列表树（通过 tag 反向查找原始 dict） |

---

## 架构约定

1. **禁止跨目录引用**：`girl_pack_editor/` 只能导入 `bk_editor.shared`，不能导入 `dev_console/` 或 `scenario_editor/` 下的模块
2. **sys.path 注入**：每个 `main.py` 负责将 `tools/` 加入 `sys.path`，使得 `import bk_editor.xxx` 正常工作
3. **延迟加载游戏数据**：`shared/renpy_ref.py` 使用延迟导入，避免在顶层 `import renpy`
4. **JSON fallback**：所有游戏内 JSON 加载点保留硬编码 fallback，确保文件缺失时游戏仍可启动

---

## 故障排除

### `ModuleNotFoundError: No module named 'bk_editor'`

必须使用正确的启动入口：
```powershell
# ✅ 正确
python tools\bk_editor\girl_pack_editor\main.py

# ❌ 错误（旧文件已删除）
python tools\bk_editor\girl_editor.py
```

### 图片预览显示「无法预览」

安装 Pillow 和 OpenCV：
```powershell
pip install Pillow pillow-avif-plugin opencv-python
```

### `_BK.ini` 编辑器保存后注释丢失

这是 `configparser` 的已知限制。保存前请备份原文件，或使用版本控制（git）管理变更。

### Ren'Py lint 报错与编辑器无关

游戏根目录 `errors.txt` 中可能存在预存在的 Ren'Py 编译错误（如非 ASCII 字符截断），这些与编辑器代码无关。编辑器是纯 Python 脚本，不影响 Ren'Py 编译。

---

## 开发进度

参见 [TASK_PROGRESS.md](./TASK_PROGRESS.md)
