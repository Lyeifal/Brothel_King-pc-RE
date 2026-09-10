# Brothel King 项目指南

> 最后更新: 2026-09-11（与代码核对）
> 本文档是 BK Evolution 的**唯一活跃项目指南**，取代 `docs/archive/` 下所有旧版项目指南。
> 分支: `bk-evolution`

---

## 1. 项目简介

**Brothel King** 是一款基于 Ren'Py 引擎开发的成人向模拟经营/视觉小说游戏。玩家经营一家妓院，管理女孩、接客、升级设施、探索剧情。

- **引擎**: Ren'Py 8.2.0 / Python 3.9
- **版本**: Brothel King Evolution
- **语言**: 英文原版 + 简体中文 (`chinese_simplified`)
- **平台**: Windows / Linux / macOS
- **分支**: `bk-evolution`

---

## 2. 根目录结构

```
Brothel_King-pc/
├── Brothel_King.exe      # Windows 启动器
├── Brothel_King.py       # Python 启动脚本（ Ren'Py launcher）
├── Brothel_King.sh       # Linux/macOS 启动脚本
├── lib/                  # 平台 Python 运行时（py3-windows-x86_64/ 等）
├── renpy/                # Ren'Py 引擎源码
├── game/                 # 游戏脚本与资源（唯一游戏代码目录）
├── tools/                # 翻译、审计、迁移脚本 + bk_editor/ 编辑器套件
├── docs/                 # 项目文档（本文件所在）
├── temp/                 # 日志、翻译临时文件、备份
├── README.html           # 项目说明（面向玩家）
└── faq.txt               # 常见问题（面向玩家）
```

> 运行时日志（`errors.txt`、`log.txt`、`traceback.txt`）在游戏运行后生成于根目录；工具输出统一写入 `temp/`。

`game/` 根目录只保留标准 Ren'Py 目录与入口资源：

```
game/
├── core/                 # 全部官方代码与数据（见第 3 节）
├── cache/                # Ren'Py 编译缓存（*.rpyb）
├── custom/               # 用户/社区内容：girls/（女孩包）、mods/（社区 Mod）
├── resources/            # 资源目录
├── saves/                # 存档
├── tl/                   # 翻译（chinese_simplified/ 等）
└── presplash_*.png       # 启动画面
```

---

## 3. `game/core/` 目录标准

`game/core/` 是官方代码、数据和内容的**唯一规范位置**。`game/` 根目录不直接存放 `.rpy` 脚本。

当前 `game/core/` 共 10 个目录（另有一个 `README.md`）：

```
game/core/
├── config/        # Ren'Py 配置与集中配置：gui.rpy, options.rpy, screens.rpy,
│                  #   translations.rpy, game_config.rpy（GameConfig 服务）
├── content/       # 叙事内容：dialogue.rpy, interactions.rpy, intro.rpy, declarations.rpy,
│                  #   main_story/, side_stories/, story_events/, city_events/, day_events/,
│                  #   scenarios/, events/
├── data/          # 数据驱动 JSON 仓库（40+ 领域子目录）+ 少量 .rpy 数据定义
│                  #   （items.rpy, jobs.rpy, perks.rpy, powers.rpy, settings.rpy）
│                  #   _schemas/ 存放 JSON Schema；HARDCODED_DATA_AUDIT.md 为审计记录
├── framework/     # 基类与核心实体：girlclass.rpy, character.rpy, core_entities.rpy,
│                  #   world.rpy, interactions.rpy, challenges.rpy, utils.rpy,
│                  #   girl/（16 个 Girl 组件文件）, pythonlib/（vendored 库）
├── i18n/          # json_i18n.rpy —— JSON `_i18n` 字段注册进 Ren'Py 翻译系统
├── init/          # 启动：start.rpy（游戏实例创建/服务注册）, settings.rpy,
│                  #   variables.rpy, dependency_graph.rpy（Init 依赖断言）
├── systems/       # 游戏系统：endday.rpy, events_dispatcher.rpy, data_loader.rpy,
│                  #   data_exporter.rpy, farm.rpy, security.rpy, traits.rpy, perks.rpy,
│                  #   items.rpy, mods/（mod_api, mod_api_v2, mod_hooks）,
│                  #   events/（event_engine, event_bridge）, registry/（9 个注册表）,
│                  #   services/（service_container, i18n_service）,
│                  #   gamemodes/, customer/, auction/, courtyard/, settlement/
├── templates/     # 开发者/Mod 模板：event_template.rpy, scenario_template.rpy,
│                  #   girl_template/（_BK.ini 模板）, mod_template/（v2 Mod 范例）
├── tools/         # 游戏内工具：dev_console/（Shift+O 控制台）,
│                  #   girl_pack_editor/, test_runner.rpy（bk_test_runner 入口）
└── ui/            # UI：screens.rpy（620 行，仅余 image/style/label 声明）,
                     screens/（16 个 screen 文件，112 个 screen 声明）,
                     screen_home.rpy, main.rpy, content_menu.rpy, notify.rpy,
                     view_models/
```

### 3.1 代码安放决策表

| 如果它是... | 放在... | 当前示例 |
|-------------|---------|----------|
| 角色定义、图片声明、转场 | `content/` | `declarations.rpy`, `intro.rpy` |
| 对话字符串、互动菜单、剧情 | `content/` | `dialogue.rpy`, `interactions.rpy`, `main_story/` |
| JSON 数据文件 | `data/<domain>/` | `traits/traits.json`, `perks/perks.json`, `achievements/achievements.json` |
| 基类与核心实体 | `framework/` | `character.rpy`, `core_entities.rpy`, `girlclass.rpy` |
| Girl 组件方法 | `framework/girl/` | `girl_stats.rpy`, `girl_economy.rpy` 等 15 个 `girl_*.rpy` |
| vendored/backported 标准库 | `framework/pythonlib/` | — |
| 游戏启动、难度选择、游戏实例创建 | `init/` | `start.rpy` |
| 全局变量、持久化默认值 | `init/` | `variables.rpy`, `settings.rpy` |
| 结算、事件调度、每日结束 | `systems/` | `endday.rpy`, `events_dispatcher.rpy` |
| 注册表、DataLoader、Mod API | `systems/` | `registry/`, `data_loader.rpy`, `mods/` |
| 服务容器、翻译服务 | `systems/services/` | `service_container.rpy`, `i18n_service.rpy` |
| UI 屏幕 | `ui/screens/` | `screen_home.rpy`, `screen_girl_stats.rpy` 等 |
| Mod/剧本模板 | `templates/` | `mod_template/`, `scenario_template.rpy` |
| 游戏内调试工具 | `tools/` | `dev_console/`, `test_runner.rpy` |
| 独立 GUI 编辑器（非游戏内） | `tools/bk_editor/`（项目根 `tools/` 下） | `girl_pack_editor/`, `scenario_editor/`, `dev_console/` |

### 3.2 核心文件速查

| 领域 | 核心文件 | 规模 |
|------|----------|------|
| Girl 类（重构后） | `game/core/framework/girlclass.rpy` | 3,910 行（重构前 5,900） |
| Girl 组件 | `game/core/framework/girl/girl_*.rpy` × 15 + `__init__.rpy` | 16 个文件 |
| 特性/技能/效果基类 | `game/core/framework/character.rpy`, `effects.rpy` | — |
| 核心实体（Game/MC/Calendar 等） | `game/core/framework/core_entities.rpy` | — |
| 服务容器 | `game/core/systems/services/service_container.rpy` | 159 行，init -12 |
| 翻译服务 | `game/core/systems/services/i18n_service.rpy` | 121 行，init -10 |
| 集中配置 | `game/core/config/game_config.rpy` | 121 行，init -11 |
| DataLoader | `game/core/systems/data_loader.rpy` | 1,319 行，init -11 |
| 事件引擎 | `game/core/systems/events/event_engine.rpy` | — |
| 事件调度 | `game/core/systems/events_dispatcher.rpy` | 8,611 行（遗留大文件） |
| 每日结算 | `game/core/systems/endday.rpy` | 1,603 行 |
| Mod API v2 | `game/core/systems/mods/mod_api_v2.rpy` | 219 行 |
| 屏幕主文件（提取后） | `game/core/ui/screens.rpy` | 620 行（原 8,886） |
| 屏幕目录 | `game/core/ui/screens/` | 16 个文件，112 个 screen 声明 |
| 女孩文件字典 | `game/core/framework/girl_files_dict.rpy` | 416 行，init -2 注册服务 |
| 游戏启动 | `game/core/init/start.rpy` | 1,081 行 |
| 测试框架 | `game/core/tools/test_runner.rpy` | 379 行，`label bk_test_runner` |
| i18n JSON 注册 | `game/core/i18n/json_i18n.rpy` | 274 行 |

---

## 4. Init 优先级链

以 `game/core/init/dependency_graph.rpy` 与代码中实际 `init` 声明为准（2026-09-11 grep 核实）：

```
init -12   service_container.rpy    GameServices 单例（services = GameServices()）
init -11   game_config.rpy          GameConfig 类 + 注册 "config"
init -11   data_loader.rpy          DataLoader 类定义
init -11   variables.rpy            早期变量
init -10   settings.rpy             girl_directories、config 调整
init -10   translations.rpy         bk_language_map、字体映射
init -10   i18n_service.rpy         I18nService（注册 "i18n" 在其后段）
init -5    tag_registry.rpy         Tag 注册表初始化
init -4    variables.rpy            tag_dict（JSON 加载）、persistent 变量
init -4    event_engine.rpy         EventEngine 类 + 注册 "event_engine"
init -3    utils.rpy/effects.rpy/dialogue.rpy/economy.rpy/game_systems.rpy
init -3    girl_factory.rpy         get_girl_path、create_girl
init -3    mod_api_v2.rpy           ModAPIV2 类 + 实例化 + 注册 "mod_api_v2"
init -2    core_entities.rpy        Game、Main、NPC、Calendar 类
init -2    world.rpy                Brothel、District、Population 等
init -2    character.rpy            Trait、Perk、Effect、ItemType 等
init -2    girlclass.rpy            Girl 类（委托组件方法）
init -2    girl_files_dict.rpy      GirlFilesDict 实例化 + 注册 "girl_files_dict"
init -2    challenges.rpy           Spell、MC_challenge、Mod（v1）
init -2    mod_api_v2.rpy           game_saved 钩子挂到 save_json_callbacks
init -1    test_runner.rpy          TestRunner 类
init -1    console_commands.rpy     注册 "dev_console"
init 0     start.rpy label          创建 game / calendar / MC / farm 并注册服务
           events_dispatcher.rpy    注册 "brothel"（Brothel 实例创建点）
```

依赖断言：在 init 块开头调用 `require_service("key")`（`service_container.rpy:137` 定义），启动期即暴露顺序错误，而不是运行时才报错。

---

## 5. 服务访问（Service Container）

服务容器 `GameServices` 是全局单例（`service_container.rpy`，init -12），用法：

```python
services = GameServices.instance()   # 或直接用全局 services
services.register("key", obj)        # 注册（重复注册覆盖，兼容热重载）
services.get("key", default)         # key 访问
services.require("key")              # 缺失即抛 RuntimeError
services.game                        # 类型化 property 访问
```

当前**实际注册**的 key（grep `services.register(` 核实，共 11 个）：

| key | 服务对象 | 注册位置 | 说明 |
|-----|----------|----------|------|
| `config` | GameConfig | `config/game_config.rpy:121` (init -11) | 集中配置，支持 `custom/config/` JSON 覆盖 |
| `girl_files_dict` | GirlFilesDict | `framework/girl_files_dict.rpy:412` (init -2) | 女孩文件倒排索引 + 惰性加载 |
| `game` | Game | `init/start.rpy:245` | 游戏实例 |
| `calendar` | Calendar | `init/start.rpy:246` | 日历 |
| `mc` | Main | `init/start.rpy:339` | 主角 |
| `farm` | Farm | `init/start.rpy:557` | 农场 |
| `brothel` | Brothel | `systems/events_dispatcher.rpy:753` | 青楼 |
| `event_engine` | EventEngine | `systems/events/event_engine.rpy:202` (init -4) | 事件引擎 |
| `i18n` | I18nService | `systems/services/i18n_service.rpy:121` (init -10) | 翻译服务 |
| `dev_console` | DevConsole | `tools/dev_console/console_commands.rpy:120` (init -1) | 调试控制台 |
| `mod_api_v2` | ModAPIV2 | `systems/mods/mod_api_v2.rpy:206` (init -3) | Mod 接口 v2 |

注意：容器上还定义了 `services.mod_api` 与 `services.data_loader` 两个 property 访问器，但代码中**没有对应的 register 调用**（访问返回 `None`）——使用时请以实际注册的 key 为准。

常用速查：

```python
services.game          # Game 实例
services.mc            # Main 主角
services.brothel       # Brothel 青楼
services.farm          # Farm 农场
services.calendar      # Calendar 日历
services.i18n          # I18nService：t() / tn() / tc() / pronoun() / possessive()
services.config        # GameConfig 配置
services.mod_api_v2    # Mod API v2（16 个 HOOK_* 常量）
services.dev_console   # Dev Console
services.event_engine  # EventEngine
services.girl_files_dict  # 女孩文件字典
```

---

## 6. 数据驱动架构

### 6.1 `from_dict()` / `to_dict()` 契约

所有能从 JSON 定义的实体必须实现：

```python
@classmethod
def from_dict(cls, d, **resolvers):
    """从 JSON-compatible dict 构建实例。"""

def to_dict(self):
    """序列化为 JSON-compatible dict。"""
```

### 6.2 DataLoader + Fallback 模式

所有 JSON 加载经由 `DataLoader`（`systems/data_loader.rpy`，init -11 类定义）：

```python
resource_dict = DataLoader.load_resources(location_resolver=lambda name: globals().get(name)) \
                or _fallback_resource_dict
```

规则：
1. JSON 缺失或无效时 `load_*` 返回 `None`，调用方回退到 `_fallback_*` 硬编码字典/列表。
2. **fallback 目前仍保留**（JSON 迁移尚未做到 100% 无回归验证），清理是遗留待办（见 ROADMAP）。
3. 新增 JSON 数据源的标准步骤见 [`../tools/bk_editor/AGENTS.md`](../../tools/bk_editor/AGENTS.md)：`data/` 建子目录 → `DataLoader.load_xxx()` → `DataExporter.export_xxx()` → `_schemas/` 加 schema → dev_console 加编辑器标签页。

### 6.3 运行时 Resolver 模式

JSON 只保存**字符串名**，`from_dict()` 接受可选 resolver 在运行时解析为对象：

```python
# JSON: {"wood": {"location": "shipyard", ...}}
location = location_resolver("shipyard")   # → shipyard Location 对象
```

### 6.4 数据迁移现状

迁移完整清单见 [migration/DATA_MIGRATION.md](../migration/DATA_MIGRATION.md) 与 [architecture/data_loader.md](../architecture/data_loader.md)。覆盖领域包括：traits、perks、achievements、challenges、contracts、resources、difficulty、ngp、meta、goals、scenarios、story_events、sandbox events 等。编辑器数据映射见 [`../tools/bk_editor/AGENTS.md`](../../tools/bk_editor/AGENTS.md) 的表格。

---

## 7. 编辑器套件

三分独立 tkinter 编辑器（零第三方依赖，仅标准库 + tkinter + Pillow），位于 `tools/bk_editor/`：

| 编辑器 | 启动命令 | 面向 | 主要输出 |
|--------|----------|------|---------|
| 女孩包编辑器 | `python tools/bk_editor/girl_pack_editor/main.py` | Mod 作者 | `game/custom/girls/`、`core/data/traits/`、`core/data/perks/` |
| 剧本编辑器 | `python tools/bk_editor/scenario_editor/main.py` | 剧情作者 | `core/data/scenarios/`、`core/data/stories/`、`core/data/sandbox/` |
| 开发控制台（GUI） | `python tools/bk_editor/dev_console/main.py` | 核心开发者 | `core/data/achievements/`、`difficulty/`、`ngp/`、`meta/` |

架构约定：三分编辑器禁止跨目录引用，共享能力统一走 `bk_editor/shared/`；细节见 [`../tools/bk_editor/README.md`](../../tools/bk_editor/README.md) 与 [`../tools/bk_editor/AGENTS.md`](../../tools/bk_editor/AGENTS.md)，以及 [architecture/editor_suite.md](../architecture/editor_suite.md)。

游戏内另有独立工具（不属于编辑器套件）：Dev Console（`game/core/tools/dev_console/`，Shift+O，仅 developer mode）、游戏内女孩包编辑器（`game/core/tools/girl_pack_editor/`）、Test Runner（`game/core/tools/test_runner.rpy`，主菜单 Tests 按钮，仅 developer mode）。

---

## 8. 命名规范

| 规范 | 示例 | 适用范围 |
|------|------|----------|
| `PascalCase` | `Achievement`, `Resource`, `DataLoader`, `GameServices` | 类名 |
| `snake_case` | `load_challenges()`, `resource_dict` | 函数、变量 |
| `UPPER_SNAKE` | `HOOK_GIRL_GENERATED` | 常量、钩子名 |
| `_fallback_*` | `_fallback_resource_dict` | 硬编码 fallback 数据 |
| `girl_<domain>.rpy` | `girl_stats.rpy`, `girl_mood.rpy` | Girl 组件文件 |
| `screen_<domain>.rpy` | `screen_quest.rpy`, `screen_farm.rpy` | 屏幕文件 |
| `core/data/<domain>/` | `core/data/traits/`, `core/data/achievements/` | JSON 数据目录 |
| `<domain>_<action>_<tense>` | `girl_generated`, `day_starting` | Mod v2 钩子命名 |

---

## 9. 缓存与构建卫生

修改任何 `.rpy` 或 `.json` 后，应清理编译缓存：

```powershell
# 删除编译脚本
Get-ChildItem -Path "game" -Filter "*.rpyc" -Recurse | Remove-Item -Force

# 删除字节码缓存
Get-ChildItem -Path "game\cache" -Filter "*.rpyb" | Remove-Item -Force
```

Ren'Py 下次启动时会重新编译。**修改 `init` 块内容或移动文件后，切勿依赖 `.rpyc` 的新鲜度。**

常用验证命令（Windows，经 lib 内 Python）：

```powershell
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . lint
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . translate --count chinese_simplified
```

---

## 10. 相关文档

| 文档 | 说明 |
|------|------|
| [../README.md](../README.md) | 文档中心（按角色导航 + 全量索引） |
| [ROADMAP.md](ROADMAP.md) | 总览路线图 |
| [REFACTORING_PROGRESS.md](REFACTORING_PROGRESS.md) | 重构进度真源（逐提交链） |
| [../architecture/README.md](../architecture/README.md) | 子系统架构文档索引 |
| [../migration/DATA_MIGRATION.md](../migration/DATA_MIGRATION.md) | 数据迁移完整清单 |
| [../i18n/I18N_ROADMAP.md](../i18n/I18N_ROADMAP.md) | i18n 状态与工具链 |
| [../modding/CUSTOM_DIRECTORIES.md](../modding/CUSTOM_DIRECTORIES.md) | `custom/` 与 `core/` 目录边界 |
| [`../../tools/bk_editor/README.md`](../../tools/bk_editor/README.md) | 编辑器套件说明 |
