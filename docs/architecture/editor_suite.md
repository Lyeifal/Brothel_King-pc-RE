# Editor Suite（编辑器套件）架构

> 最后更新: 2026-09-11（与代码核对）
> **目录**: `tools/bk_editor/`
> **详细文档**: [tools/bk_editor/README.md](../../tools/bk_editor/README.md)（本文只作架构级精简介绍，细节以该 README 与 `tools/bk_editor/AGENTS.md` 为准）
> **技术栈**: Python 3.9+，tkinter（Pillow 可选，已默认安装）

---

## 1. 系统职责

Editor Suite 是 BK Evolution 的可视化数据编辑工具链，让非程序员也能制作 Mod 内容。采用**三分独立编辑器**架构：

| 编辑器 | 目录 | 目标用户 | 核心职责 |
|--------|------|----------|---------|
| **女孩包编辑器** | `girl_pack_editor/` | Mod 作者 | 图片批量打标、`_BK.ini` 编辑、自定义 Trait/Perk、包验证 |
| **剧本编辑器** | `scenario_editor/` | 剧情/事件作者 | StoryEvent CRUD、剧本管理、地图/NPC/商店参考、对话标签扫描 |
| **开发控制台** | `dev_console/` | 核心开发者 | 成就、难度、NG+、局外养成（Meta）、I18n、数据同步 |

## 2. 关键约定

- **禁止跨目录引用**：每个编辑器只能导入自己的 `tabs/` 子模块、`bk_editor.shared` 共享库、标准库 + tkinter。
- **共享库 `shared/`**: `paths.py`（项目路径常量）、`json_io.py`（JSON 读写）、`widgets.py`（`LabeledEntry`/`EffectEditor`/`JsonTreeview` 等）、`validators.py`（字段校验）、`renpy_ref.py`（函数级延迟引用游戏内数据，**禁止模块顶层 import renpy**）。
- **统一入口**: `tools/bk_editor.py`，或各编辑器 `main.py` 单独启动。
- **JSON 契约**：编辑器产出 JSON → 游戏侧 `DataLoader.load_*()` 加载 → 注册表生效。改 JSON 后需重启游戏（注册表 init 期重建）。

## 3. 编辑器 ↔ 游戏数据映射（经 AGENTS.md 核实）

| 编辑器模块 | JSON 文件 | 游戏加载点 |
|-----------|-----------|-----------|
| `dev_console/achievement_editor` | `core/data/achievements/achievements.json` | `DataLoader.load_achievements()` |
| `dev_console/difficulty_editor` | `core/data/difficulty/difficulty.json` | `DataLoader.load_difficulty()` |
| `dev_console/ngp_editor` | `core/data/ngp/ngp_settings.json` | `DataLoader.load_ngp_settings()` |
| `dev_console/meta_editor` | `core/data/meta/meta_progression.json` | `DataLoader.load_meta_progression()` |
| `scenario_editor/event_editor` | `core/data/stories/story_events.json`、`core/data/sandbox/events.json` | `load_story_events()` / `load_sandbox_events()` |
| `scenario_editor/scenario_editor_tab` | `core/data/scenarios/scenarios.json` | `DataLoader.load_scenarios()` |
| `girl_pack_editor/trait_creator` | `core/data/traits/traits.json`、`core/data/perks/perks.json` | `load_traits()` / `load_perks()` |

## 4. 已知限制

- `_BK.ini` 编辑器保存时移除全部注释（configparser 限制）。
- tkinter PhotoImage 不装 Pillow 无法预览 WebP/AVIF（已默认装 Pillow）。
- District/Location/NPC/Shop 无 JSON（仍硬编码于 `start.rpy`），编辑器只提供参考查看与代码片段生成。
- Windows 控制台可能无法正确显示非 ASCII 文件名（文件操作正常）。

---

## 相关文档

- [tools/bk_editor/README.md](../../tools/bk_editor/README.md) — 三编辑器的完整使用文档
- [data_loader.md](data_loader.md) — 编辑器 JSON 的游戏侧加载
- [registry.md](registry.md) — 编辑器的注册表目标
- [girl_pack.md](girl_pack.md) — 女孩包编辑器的验证逻辑
