# BK Editor Suite — Agent Guide

> 本文档为 AI Agent 提供 `tools/bk_editor/` 的架构约定、编码规范与任务指引。

---

## 架构原则

### 1. 三分独立编辑器

```
girl_pack_editor/   ← 面向 MOD 作者（图片、INI、Trait、验证）
scenario_editor/    ← 面向剧情作者（事件、剧本、地图、NPC、商店、对话标签）
dev_console/        ← 面向核心开发者（成就、难度、NG+、Meta、I18n、数据同步）
```

**禁止跨目录引用**。每个编辑器只能导入：
- 自己的 `tabs/` 子模块
- `bk_editor.shared` 共享库
- Python 标准库 + tkinter

### 2. 共享库 (`shared/`)

所有编辑器共用的基础能力集中在此。添加新共享组件时：
1. 在 `shared/widgets.py`、`shared/validators.py` 等中实现
2. 在 `shared/__init__.py` 中导出
3. 在各编辑器的 `main.py` 中无需额外操作（已通过 `sys.path` 注入）

**现有共享组件**：
- `paths.py`: `PROJECT_ROOT`, `GAME_DIR`, `DATA_DIR`, `GIRLS_DIR`
- `json_io.py`: `load_json`, `save_json`, `merge_json`
- `widgets.py`: `LabeledEntry`, `LabeledSpinbox`, `LabeledCombobox`, `LabeledCheckbox`, `EffectEditor`, `JsonTreeview`
- `validators.py`: `validate`, `validate_type`, `validate_trait`, `validate_perk`, 等
- `renpy_ref.py`: 延迟引用游戏内 `tag_dict_data`（避免顶层 import renpy）

### 3. 入口规范

每个编辑器的 `main.py` 必须包含：

```python
import sys
from pathlib import Path
_TOOLS_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_TOOLS_DIR))
```

注意 `parent.parent.parent` 的层数：
- `tools/bk_editor/girl_pack_editor/main.py` → `tools/`
- `tools/bk_editor/dev_console/main.py` → `tools/`

### 4. tkinter UI 规范

- 主背景色：`#1a1a2e`
- 面板/工具栏背景：`#16213e`
- 按钮/强调色：`#0f3460`（普通），`#660000`（危险操作）
- 文字颜色：`#FFFFFF`（主文字），`#FFD700`（标题/强调），`#AAAAAA`（次要）
- 字体：`("Microsoft YaHei", size)` 用于中文界面，`("Consolas", size)` 用于代码/JSON
- 所有 Frame 需显式设置 `bg=` 以避免 tkinter 默认灰色

---

## 各编辑器数据文件映射

| 编辑器 | 编辑的 JSON 文件 | 对应游戏加载点 |
|---|---|---|
| **dev_console/achievement_editor** | `core/data/achievements/achievements.json` | `DataLoader.load_achievements()` |
| **dev_console/difficulty_editor** | `core/data/difficulty/difficulty.json` | `DataLoader.load_difficulty()` |
| **dev_console/ngp_editor** | `core/data/ngp/ngp_settings.json` | `DataLoader.load_ngp_settings()` |
| **dev_console/meta_editor** | `core/data/meta/meta_progression.json` | `DataLoader.load_meta_progression()` |
| **scenario_editor/event_editor** | `core/data/stories/story_events.json` | `DataLoader.load_story_events()` |
| **scenario_editor/event_editor** | `core/data/sandbox/events.json` | `DataLoader.load_sandbox_events()` |
| **scenario_editor/scenario_editor_tab** | `core/data/scenarios/scenarios.json` | `DataLoader.load_scenarios()` |
| **girl_pack_editor/trait_creator** | `core/data/traits/traits.json` | `DataLoader.load_traits()` |
| **girl_pack_editor/trait_creator** | `core/data/perks/perks.json` | `DataLoader.load_perks()` |

---

## 常见任务指引

### 添加新的编辑器标签页

1. 在对应编辑器的 `tabs/` 下新建 `.py` 文件
2. 继承 `tk.Frame`，接收 `(parent, app)` 参数
3. 在 `editor.py` 的 `__init__` 中通过 `_add_tab(title, TabClass)` 注册
4. 如果涉及 JSON 编辑，优先继承 `dev_console/tabs/base.py` 中的 `BaseJsonEditorTab`

### 添加新的共享组件

1. 在 `shared/widgets.py` 中创建新的 tkinter 组件类
2. 在 `shared/__init__.py` 中导出
3. 在各编辑器中通过 `from bk_editor.shared import NewWidget` 使用

### 修改 JSON 数据结构

1. 修改游戏内 `DataLoader` 的加载方法（`game/core/systems/data_loader.rpy`）
2. 修改 `DataExporter` 的导出方法（`game/core/systems/data_exporter.rpy`）
3. 更新 `_schemas/*.schema.json`（如有）
4. 更新对应编辑器的表单字段
5. **保留硬编码 fallback**，确保 JSON 文件缺失时游戏仍可启动

### 新增 JSON 数据源

参照已有范例（achievements / difficulty / ngp / meta）：
1. 在 `game/core/data/` 下创建子目录和 `.json` 文件
2. 在 `DataLoader` 中添加 `load_xxx()` 方法
3. 在 `DataExporter` 中添加 `export_xxx()` 方法
4. 在游戏初始化代码中改为「JSON 优先，硬编码 fallback」
5. 在 `dev_console/` 中新增对应编辑器标签页

---

## 已知限制与注意事项

1. **configparser 丢失注释**：`_BK.ini` 编辑器保存时会移除所有注释，无法避免
2. **tkinter PhotoImage 格式限制**：不使用 Pillow 时无法预览 WebP/AVIF，已默认安装 Pillow
3. **场景编辑器中的 District/Location/NPC/Shop 无 JSON**：这些游戏数据仍硬编码在 `start.rpy` 中，编辑器只提供参考查看器和代码片段生成器
4. **Ren'Py 未初始化时不能 import renpy**：`shared/renpy_ref.py` 使用函数级延迟导入，禁止在模块顶层 `import renpy`
5. **女孩包文件名编码**：Windows 控制台可能无法正确显示非 ASCII 文件名，但文件操作本身正常
