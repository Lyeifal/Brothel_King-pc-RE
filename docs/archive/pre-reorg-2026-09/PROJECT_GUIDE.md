# Brothel King 项目指南

> 本文档是 BK Evolution 项目的**唯一活跃项目指南**，说明目录结构、核心代码组织方式、数据驱动架构、翻译工作流和编辑器套件。
>
> 历史版本：[`docs/archive/PROJECT_GUIDE_V3.md`](archive/PROJECT_GUIDE_V3.md)（Phase 6）

---

## 1. 项目简介

**Brothel King** 是一款基于 Ren'Py 8.2 引擎开发的成人向模拟经营/视觉小说游戏。玩家经营一家妓院，管理女孩、接客、升级设施、探索剧情。

- **引擎**: Ren'Py 8.2.0 / Python 3.9
- **版本**: Brothel King Evolution
- **语言**: 英文原版 + 简体中文 (`chinese_simplified`)
- **平台**: Windows / Linux / macOS

---

## 2. 根目录结构

```
Brothel_King-pc/
├── Brothel_King.exe      # Windows 启动器
├── Brothel_King.py       # Python 启动脚本
├── Brothel_King.sh       # Linux/macOS 启动脚本
├── lib/                  # Python 运行时库（按平台分类）
├── renpy/                # Ren'Py 引擎源码
├── game/                 # 游戏主目录（所有脚本和资源）
├── tools/                # 翻译、迁移和开发工具脚本
├── docs/                 # 项目文档（开发指南、架构文档、路线图）
├── temp/                 # 临时文件：翻译清单、报告、日志、备份
├── README.html           # 项目说明（HTML）
└── faq.txt               # 常见问题
```

> 运行时日志（`errors.txt`、`log.txt`、`traceback.txt`）和翻译临时文件现在统一输出到 `temp/`，不会堆积在根目录。

---

## 3. `game/core/` 目录标准

`game/core/` 是引擎代码、数据和内容的**唯一规范位置**。`game/` 根目录不再直接存放 `.rpy` 脚本，只保留标准 Ren'Py 目录（`cache/`、`custom/`、`resources/`、`saves/`、`tl/`）。

```
game/core/
├── config/        # Ren'Py 配置（gui.rpy, options.rpy, screens.rpy, translations.rpy）
├── content/       # 叙事内容：剧情、对话、互动、角色声明
├── data/          # 游戏数据：JSON 数据文件 + 少量 .rpy 数据定义
├── framework/     # 基类、工具函数、vendored Python 库
├── i18n/          # 国际化注册与辅助函数（json_i18n.rpy）
├── init/          # 启动脚本：游戏开始、全局设置、变量声明
├── systems/       # 游戏系统：农场、事件调度、结算、注册表等
├── templates/     # 开发者/Mod 模板（非运行时资产）
└── ui/            # UI 屏幕脚本
```

### 3.1 代码安放决策表

| 如果它是... | 放在... | 当前示例 |
|-------------|---------|----------|
| 角色定义、图片声明、转场 | `content/` | `declarations.rpy`, `intro.rpy` |
| 对话字符串、互动菜单、剧情 | `content/` | `dialogue.rpy`, `interactions.rpy`, `main_story/` |
| JSON 数据文件 | `data/<domain>/` | `traits/traits.json`, `items/items.json`, `events/event_dict.json` |
| 基类与核心实体 | `framework/` | `character.rpy`, `core_entities.rpy`, `girlclass.rpy`, `utils.rpy` |
| vendored/backported 标准库 | `framework/pythonlib/` | `ConfigParser.py`, `fractions.py` |
| 游戏启动、难度选择 | `init/` | `start.rpy` |
| 全局变量、持久化默认值 | `init/` | `variables.rpy` |
| 引擎配置、平衡参数 | `init/` | `settings.rpy` |
| 结算、事件调度、每日结束 | `systems/` | `endday.rpy`, `events_dispatcher.rpy` |
| 注册表、DataLoader | `systems/` | `registry/`, `data_loader.rpy` |
| UI 屏幕 | `ui/` | `screens.rpy`, `main.rpy` |
| Mod/剧本模板 | `templates/` | `event_template.rpy`, `scenario_template/` |

### 3.2 主要代码文件速查

| 领域 | 核心文件 |
|------|----------|
| 女孩类 | `game/core/framework/girlclass.rpy` |
| 特性/技能/效果 | `game/core/framework/character.rpy`, `game/core/framework/effects.rpy` |
| 核心实体（成就、目标、资源等） | `game/core/framework/core_entities.rpy` |
| 对话系统 | `game/core/content/dialogue.rpy` |
| 互动系统 | `game/core/framework/interactions.rpy`, `game/core/content/interactions.rpy` |
| 事件调度 | `game/core/systems/events_dispatcher.rpy` |
| 每日结算 | `game/core/systems/endday.rpy` |
| UI 屏幕 | `game/core/ui/screens.rpy`, `game/core/ui/main.rpy` |
| 注册表 | `game/core/systems/registry/registry.rpy` |
| DataLoader | `game/core/systems/data_loader.rpy` |
| i18n 注册 | `game/core/i18n/json_i18n.rpy` |

---

## 4. 数据驱动架构

### 4.1 `from_dict()` / `to_dict()` 契约

所有能从 JSON 定义的实体必须实现：

```python
@classmethod
def from_dict(cls, d, **resolvers):
    """从 JSON-compatible dict 构建实例。"""
    ...

def to_dict(self):
    """序列化为 JSON-compatible dict。"""
    ...
```

示例：
- `Achievement.from_dict()` — 将字符串键转换为 `requirements` 的整型键。
- `Resource.from_dict(d, location_resolver=...)` — 在运行时将位置名字符串解析为 `Location` 对象。
- `Contract.from_dict(d, character_resolver=...)` — 在运行时将角色名字符串解析为 `Character` 对象。

### 4.2 DataLoader + Fallback 模式

所有 JSON 加载都通过 `DataLoader` 完成：

```python
# 在 init/start.rpy 的 init_game 中
resource_dict = DataLoader.load_resources(location_resolver=lambda name: globals().get(name)) \
                or _fallback_resource_dict
```

规则：
1. `DataLoader._loaded` 跟踪已解析文件，每个会话只加载一次。
2. JSON 缺失或无效时返回 `None`，调用方提供 `_fallback_*` 硬编码字典/列表。
3. Fallback 会保留到 JSON 迁移 100% 验证通过后再移除。

### 4.3 运行时 Resolver 模式

对于引用运行时对象（如 `Location`、`Character`）的实体，JSON 只保存**字符串名**。`from_dict()` 接受可选的 `resolver`：

```python
# JSON
{"wood": {"location": "shipyard", ...}}

# from_dict
location = location_resolver("shipyard")  # → shipyard Location 对象
```

这保持 JSON 纯文本可序列化，同时允许运行时绑定。

### 4.4 已完成的数据迁移

| 领域 | JSON 路径 | Fallback 位置 | 状态 |
|------|-----------|---------------|------|
| MC 挑战 | `data/challenges/challenges.json` | `init/start.rpy` | ✅ 已迁移 |
| 资源 | `data/resources/resources.json` | `init/start.rpy` | ✅ 已迁移 |
| 契约模板 | `data/contracts/contracts.json` | `init/start.rpy` | ✅ 已迁移 |
| 清洁度惩罚 | `data/settings/cleanliness_penalties.json` | `init/start.rpy` | ✅ 已迁移 |
| 宝藏阈值 | `data/settings/treasure_thresholds.json` | `init/start.rpy` | ✅ 已迁移 |
| 特性 (Traits) | `data/traits/traits.json` | `systems/registry/trait_registry.rpy` | ✅ 已迁移 |
| 技能 (Perks) | `data/perks/perks.json` | `systems/registry/perk_registry.rpy` | ✅ 已迁移 |
| 故事事件 | `data/events/event_dict.json` | `init/start.rpy` | ✅ 已迁移 |
| 成就 | `data/achievements/achievements.json` | `systems/achievements.rpy` | ✅ 已迁移 |
| NG+ 设置 | `data/ngp/ngp_settings.json` | `init/start.rpy` | ✅ 已迁移 |
| 章节目标 | `data/goals/chapter_goals.json` | `init/settings.rpy` | ✅ 已迁移 |

完整迁移清单见 [`DATA_MIGRATION.md`](DATA_MIGRATION.md)。

---

## 5. Init 优先级链

```
init -10: Registry 基类、Goal 类
init -9:  TagRegistry 批量注册（settings.rpy）
init -6:  Trait/Perk/Tag/Dialogue/Event/NGP 注册表实例化
init -4:  ModAPI、EventEngine
init -2:  Location、Achievement、Resource、Contract、MC_challenge、Picture 等基类
init -1:  DataLoader 类
init 0:   各系统的 _fallback_* 数据定义
init 1:   items.rpy、powers.rpy 等数据定义
```

**运行时（`label init_game`）**:

```
DataLoader.load_all()  → traits, perks, origins, events, scenarios, achievements, difficulty, ngp, meta
DataLoader.load_resources(location_resolver=...)
DataLoader.load_challenges()
DataLoader.load_cleanliness_penalties()
DataLoader.load_treasure_thresholds()
DataLoader.load_contracts(character_resolver=...)
```

---

## 6. 翻译工作流

中文翻译采用 Ren'Py 标准双轨制：

- `game/tl/chinese_simplified/strings.rpy` — 代码中 `__()` / `_()` 字符串的翻译。
- `game/tl/chinese_simplified/**/*.rpy` — 剧情对话的 `translate chinese_simplified` 块。
- JSON `_i18n` 字段 — 通过 `game/core/i18n/json_i18n.rpy` 注册到 Ren'Py 翻译系统。

### 6.1 标准流程

```powershell
# 1. 提取当前空翻译
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . translate --empty chinese_simplified

# 2. 导出到 Excel（输出到 temp/translations/）
python tools/export_empty_to_xlsx.py

# 3. 填写 temp/translations/to_translate_empty.xlsx 的 Chinese Translation 列

# 4. 导回翻译
python tools/import_translated_empty.py

# 5. 占位符审计
python tools/audit_placeholders.py

# 6. 验证
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . lint
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . translate --count chinese_simplified
```

旧版本迁移/剩余英文导出等高级流程见 [`TRANSLATION_COMPLETION_PLAN.md`](TRANSLATION_COMPLETION_PLAN.md)。

### 6.2 i18n 最佳实践

- 玩家可见字符串使用 `__()`（运行时翻译）或 `_()`（屏幕语言翻译）。
- JSON 中可翻译字段统一加 `_i18n` 后缀（如 `name_i18n`、`description_i18n`）。
- 图片路径、音效路径、代码标识符**不要**包裹 `__()`。
- 中文翻译必须保留 `%s` / `%d` / `[var]` 占位符的数量和顺序。

详见 [`I18N_BEST_PRACTICES.md`](I18N_BEST_PRACTICES.md)。

---

## 7. 编辑器套件 (BK Editor Suite)

三个独立可视化编辑器位于 `tools/bk_editor/`，直接读写 `game/core/data/`：

| 编辑器 | 启动命令 | 用途 | 主要输出目录 |
|--------|----------|------|-------------|
| 女孩包编辑器 | `python tools/bk_editor/girl_pack_editor/main.py` | 女孩包图片打标、`_BK.ini` 编辑、Trait/Perk 创建、包验证 | `game/custom/girls/`, `game/core/data/traits/` |
| 剧本编辑器 | `python tools/bk_editor/scenario_editor/main.py` | StoryEvent / Scenario JSON 编辑、地图/NPC/商店参考、对话标签扫描 | `game/core/data/scenarios/`, `game/core/data/events/` |
| 开发控制台 | `python tools/bk_editor/dev_console/main.py` | 成就、难度、NG+、Meta 等 JSON 数据增删改查 | `game/core/data/achievements/`, `game/core/data/difficulty/`, `game/core/data/ngp/`, `game/core/data/meta/` |

### 7.1 编辑器架构

- `tools/bk_editor/shared/`：三个编辑器共用的基础库（路径、JSON IO、tkinter 组件、校验器）。
- 各编辑器禁止跨目录引用，统一通过 `bk_editor.shared` 获取共享能力。
- 所有 JSON 数据文件位于 `game/core/data/`，编辑器直接读写。

详细说明请参阅 [`tools/bk_editor/README.md`](../tools/bk_editor/README.md) 和 [`tools/bk_editor/AGENTS.md`](../tools/bk_editor/AGENTS.md)。

---

## 8. 命名规范

| 规范 | 示例 | 适用范围 |
|------|------|----------|
| `PascalCase` | `Achievement`, `Resource`, `DataLoader` | 类名 |
| `snake_case` | `load_challenges()`, `resource_dict` | 函数、局部变量 |
| `UPPER_SNAKE` | `RES_BASE_X`, `MAX_CHAPTER` | 配置常量 |
| `_fallback_*` | `_fallback_resource_dict` | 硬编码 fallback 数据 |
| `core/data/<domain>/` | `core/data/traits/`, `core/data/items/` | JSON 数据目录 |

---

## 9. 缓存与构建卫生

修改任何 `.rpy` 或 `.json` 后，应清理缓存：

```powershell
# 删除编译脚本
Get-ChildItem -Path "game" -Filter "*.rpyc" -Recurse | Remove-Item -Force

# 删除字节码缓存
Get-ChildItem -Path "game\cache" -Filter "*.rpyb" | Remove-Item -Force
```

Ren'Py 下次启动时会重新编译。**修改 `init` 块内容或移动文件后，切勿依赖 `.rpyc` 的新鲜度**。

---

## 10. 开发注意事项

1. **不要直接修改 `strings.rpy` 的格式**：`old`/`new` 必须成对出现，且占位符需与原文一致。
2. **变量名保护**：`[girl.name]`、`[brothel.name]` 等运行时变量翻译时不能译成中文；机器翻译后可用 `tools/audit_placeholders.py` 审计。
3. **Mod 翻译**：`game/custom/` 下的内容保持原文逻辑；若需中文显示，通过代码包裹 `__()` 或新增字符串翻译实现。
4. **Git 管理**：批量翻译导入和大型重构前请先提交当前状态，便于回退。

---

## 11. 相关文档

| 文件 | 说明 |
|------|------|
| [`README.md`](README.md) | 本文档（项目指南） |
| [`ROADMAP.md`](ROADMAP.md) | BK Evolution 高阶段路线图 |
| [`BK_EVOLUTION_ROADMAP.md`](BK_EVOLUTION_ROADMAP.md) | 编辑器和迁移专项路线图 |
| [`DATA_MIGRATION.md`](DATA_MIGRATION.md) | 硬编码数据 → JSON 迁移完整清单 |
| [`I18N_BEST_PRACTICES.md`](I18N_BEST_PRACTICES.md) | i18n 编码与翻译最佳实践 |
| [`TRANSLATION_COMPLETION_PLAN.md`](TRANSLATION_COMPLETION_PLAN.md) | 中文翻译补完记录与工作流 |
| [`architecture/README.md`](architecture/README.md) | 子系统架构文档索引 |
| [`tools/README.md`](../tools/README.md) | 工具脚本说明 |
| [`tools/bk_editor/README.md`](../tools/bk_editor/README.md) | 编辑器套件说明 |
| [`game/tl/chinese_simplified/strings.rpy`](../game/tl/chinese_simplified/strings.rpy) | 字符串翻译主文件 |
