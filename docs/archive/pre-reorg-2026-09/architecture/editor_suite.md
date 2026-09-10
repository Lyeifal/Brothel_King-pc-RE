# Editor Suite 架构

> **文件**: `tools/bk_editor/`  
> **启动**: `python tools/bk_editor.py`（统一入口）或 `python tools/bk_editor/<editor>/main.py`（单独启动）  
> **技术栈**: Python 3.9+, tkinter（零第三方依赖，可选 Pillow/OpenCV）

---

## 1. 系统职责

Editor Suite 是 BK Evolution 的可视化数据编辑工具链，让非程序员也能制作 Mod 内容。采用**三分架构**：

| 编辑器 | 目录 | 目标用户 | 核心职责 |
|--------|------|----------|---------|
| **女孩包编辑器** | `tools/bk_editor/girl_pack_editor/` | Mod 作者 | 图片打标、`_BK.ini` 编辑、自定义 Trait/Perk、包验证 |
| **剧本编辑器** | `tools/bk_editor/scenario_editor/` | 剧情/事件作者 | StoryEvent CRUD、Scenario 管理、District/NPC/Shop 参考、对话标签扫描 |
| **开发控制台** | `tools/bk_editor/dev_console/` | 核心开发者 | Achievement / Difficulty / NG+ / Meta-progression / Goal / Customer Affix 等 JSON 数据增删改查 |

共享基础库 (`tools/bk_editor/shared/`)：
- `paths.py` — 项目路径常量
- `json_io.py` — JSON 读写封装（支持 `str/Path` 自动转换）
- `widgets.py` — tkinter 通用组件（带搜索的列表框、标签输入器等）
- `validators.py` — 字段校验
- `renpy_ref.py` — 延迟加载游戏内数据（如 `all_jobs`, `all_sex_acts`）

---

## 2. 解耦方式

- **三分隔离**: 三个编辑器**禁止目录间交叉引用**。统一通过 `bk_editor.shared` 获取能力。
- **与游戏引擎解耦**: 编辑器作为独立 Python 进程运行，不依赖 Ren'Py 运行时，仅通过 `renpy_ref.py` 读取 `.rpy` 中的常量定义。
- **与数据格式解耦**: 所有数据交互通过 `json_io.py` 进行，编辑器不直接操作 `.rpy` 源码（除 `renpy_ref.py` 的只读引用）。

---

## 3. 系统间联系

```
tools/bk_editor/
    ├─→ shared/
    │      ├─→ json_io.py  ←→ game/core/data/**/*.json
    │      ├─→ renpy_ref.py ←→ game/ 中的常量定义
    │      └─→ widgets.py   ←→ 所有编辑器的 UI 组件
    ├─→ girl_pack_editor/
    │      ├─→ image_tagger.py    ←→ TagRegistry (图片标签)
    │      ├─→ trait_creator.py   ←→ TraitRegistry / PerkRegistry
    │      └─→ pack_validator.py  ←→ Girl Pack 完整性规则
    ├─→ scenario_editor/
    │      ├─→ event_editor.py    ←→ StoryEvent / EventRegistry
    │      ├─→ scenario_editor_tab.py ←→ Scenario / GameMode
    │      └─→ npc_editor.py      ←→ NPC 参考数据
    └─→ dev_console/
           ├─→ achievement_editor.py ←→ AchievementRegistry
           ├─→ difficulty_editor.py  ←→ 难度设置 JSON
           ├─→ goal_editor.py        ←→ Goal / chapter_goals JSON
           ├─→ customer_affix_editor.py ←→ Customer Affix JSON
           └─→ data_sync.py          ←→ JSON Schema 验证
```

- 编辑器产出的 JSON 文件被 `DataLoader` 在游戏启动时加载。
- `DataLoader` 的加载顺序在 `init -1`，早于大多数游戏系统，确保编辑器修改的数据即时生效。

---

## 4. 编辑器支持矩阵

| 数据类型 | 女孩包编辑器 | 剧本编辑器 | 开发控制台 |
|----------|-------------|-----------|-----------|
| Trait/Perk | ✅ 完整 | ❌ | ❌ |
| Girl Pack / `_BK.ini` | ✅ 完整 | ❌ | ❌ |
| StoryEvent | ❌ | ✅ 完整 | ❌ |
| Scenario / GameMode | ❌ | ✅ 完整 | ✅ 数据同步 |
| Achievement | ❌ | ❌ | ✅ 完整 |
| Difficulty | ❌ | ❌ | ✅ 完整 |
| NG+ / Meta | ❌ | ❌ | ✅ 完整 |
| Goal | ❌ | ❌ | ✅ 完整 |
| Customer Affix | ❌ | ❌ | ✅ 数据同步 |

---

## 5. 向后兼容

- 编辑器输出的 JSON 均通过 Schema 验证，确保与游戏端 `from_dict()` 兼容。
- `json_io.py` 的 `load_json(path, default=...)` 在文件缺失时返回默认值，不抛异常。
- 所有编辑器标签页通过统一的初始化测试框架验证，确保新增/修改不会破坏现有功能。
