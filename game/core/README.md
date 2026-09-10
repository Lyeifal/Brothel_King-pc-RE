# game/core/ 目录结构指南

> 本文档详细说明 `game/core/` 目录下所有文件与文件夹的职责、加载顺序及依赖关系。
> 对应分支：`bk-evolution`

---

## 一、顶层概览

```
game/core/
├── config/          # Ren'Py 配置层（GUI、选项、屏幕、翻译）
├── content/         # 剧情内容层（主线/支线/事件/对话）
├── data/            # 数据驱动层（JSON 配置 + Schema）
├── framework/       # 框架层（类定义、工具函数、Mixin）
├── init/            # 初始化层（变量声明、游戏启动）
├── systems/         # 系统层（拍卖、农场、顾客、法术等）
├── templates/       # 模板层（事件/女孩/MOD 模板）
└── ui/              # UI 层（屏幕定义、通知、主菜单）
```

---

## 二、各目录详解

### 2.1 `config/` — Ren'Py 配置

| 文件 | 说明 |
|------|------|
| `gui.rpy` | GUI 样式、颜色、字体定义 |
| `options.rpy` | 游戏选项（窗口标题、版本、存档槽数量等） |
| `screens.rpy` | 核心 Ren'Py 屏幕（say、choice、nvl、file 等） |
| `translations.rpy` | 多语言翻译映射 |
| `script_version.txt` | 脚本版本标记 |

**加载时机**：Ren'Py 默认在 `init` 阶段加载，无特殊优先级。

---

### 2.2 `content/` — 剧情与叙事内容

所有 `.rpy` 文件均为 `init` 默认优先级，存放**纯叙事内容**（标签/对话/事件）。

#### `content/city_events/` — 城市事件
- `city_events.rpy` — 城市探索时触发的随机事件池

#### `content/day_events/` — 日间事件
- `day_events.rpy` — 白天返回主屏幕时触发的事件

#### `content/main_story/` — 主线剧情
- `chapter1/chapter1.rpy` — 第一章主线
- `chapter2/chapter2.rpy` — 第二章主线
- `chapter3/chapter3.rpy` — 第三章主线

#### `content/side_stories/` — 支线剧情
- `kite_jobgirl/beach.rpy` — 风筝女孩海滩支线
- `kite_jobgirl/riddle.rpy` — 风筝女孩谜语支线
- `kite_jobgirl/variables.rpy` — 风筝女孩支线变量

#### `content/story_events/` — 故事事件
- `story_events.rpy` — 通用 StoryEvent 定义与注册

#### `content/` 根目录文件
| 文件 | 说明 |
|------|------|
| `declarations.rpy` | 图片/音频/角色声明（`image`、`define audio`、`define character`） |
| `dialogue.rpy` | 通用对话标签 |
| `events/__init__.rpy` | 事件模块初始化 |
| `interactions.rpy` | 女孩互动场景 |
| `interactions_free.rpy` | 自由女孩互动场景 |
| `intro.rpy` | 游戏开场/序章 |

---

### 2.3 `data/` — 数据驱动配置

> **设计原则**：所有曾硬编码在 `.rpy` 中的静态数据，逐步迁移至此目录的 JSON 文件。

#### 2.3.1 Schema 定义（`_schemas/`）

| 文件 | 校验目标 |
|------|---------|
| `chapter_title.schema.json` | `chapter_titles.json` |
| `goal.schema.json` | `chapter_goals.json` |
| `perk.schema.json` | `perks.json` |
| `scenario.schema.json` | `scenarios.json` |
| `story_event.schema.json` | `story_events.json` |
| `trait.schema.json` | `traits.json` |

#### 2.3.2 JSON 数据文件

| 路径 | 说明 | 对应 `.rpy` 回退 |
|------|------|-----------------|
| `achievements/achievements.json` | 成就定义 | `systems/achievements.rpy` |
| `challenges/challenges.json` | MC 挑战定义 | `start.rpy` 中 `_fallback_challenges` |
| `chapters/chapter_titles.json` | 章节标题 | `start.rpy` 中 `_fallback_chapter_titles` |
| `contracts/contracts.json` | 契约模板 | `start.rpy` 中 `_fallback_contract_templates` |
| `customers/customer_affixes.json` | 顾客词缀池 | `systems/customer/customer_affixes.rpy` |
| `difficulty/difficulty.json` | 难度参数 | `init/settings.rpy` |
| `events/event_dict.json` | 剧情事件字典 | `content/events/__init__.rpy` |
| `goals/chapter_goals.json` | 章节目标 | `framework/goal.rpy` 中硬编码回退 |
| `meta/meta_progression.json` | Meta 升级 | `systems/registry/meta_registry.rpy` |
| `ngp/ngp_settings.json` | NG+ 设置 | `systems/registry/ngp_registry.rpy` |
| `perks/perks.json` | 天赋定义 | `data/perks.rpy` |
| `personalities/personalities.json` | 人格原型 | `framework/character.rpy` |
| `ranks/ranks.json` | 等级/声望定义 | `data/settings.rpy` |
| `resources/resources.json` | 资源定义 | `start.rpy` 中 `_fallback_resource_dict` |
| `sandbox/events.json` | 沙盒事件 | `systems/gamemodes/sandbox_mode.rpy` |
| `sandbox/origins.json` | 出身定义 | `systems/gamemodes/sandbox_mode.rpy` |
| `scenarios/scenarios.json` | 剧本定义 | `systems/gamemodes/scenario_mode.rpy` |
| `settings/cleanliness_penalties.json` | 清洁度惩罚 | `start.rpy` 中 `_fallback_cleanliness` |
| `settings/treasure_thresholds.json` | 宝藏阈值 | `start.rpy` 中 `_fallback_treasure` |
| `stats/stats.json` | 属性定义 | `data/settings.rpy` |
| `stories/story_events.json` | 故事事件数据 | `content/story_events/story_events.rpy` |
| `traits/traits.json` | 特质定义 | `data/traits.rpy` |

#### 2.3.3 `.rpy` 数据回退文件

> 这些文件保留**硬编码回退数据**，当 JSON 加载失败时启用。

| 文件 | 说明 |
|------|------|
| `items.rpy` | 物品类型硬编码定义 |
| `jobs.rpy` | 工作类型硬编码定义 |
| `perks.rpy` | 天赋硬编码定义 |
| `powers.rpy` | 力量/能力硬编码定义 |
| `settings.rpy` | 全局设置、难度参数、属性定义 |

---

### 2.4 `framework/` — 核心框架

> **加载优先级**（Ren'Py `init` 数字越小优先级越高）：
> ```
> init -4  → picture.rpy
> init -3  → mixins.rpy, utils.rpy, girl_factory.rpy, game_systems.rpy, economy.rpy, effects.rpy, dialogue.rpy
> init -2  → core_entities.rpy, world.rpy, character.rpy, interactions.rpy, challenges.rpy, progression.rpy, girlclass.rpy, girl_files_dict.rpy, farm.rpy
> init -10 → goal.rpy
> ```

#### 2.4.1 Mixin 层

| 文件 | 优先级 | 说明 |
|------|--------|------|
| `mixins.rpy` | `init -3` | `EffectBearer`（效果包装）、`PicHolder`（图片获取）、`Trackable`（计数追踪） |

#### 2.4.2 类定义（原 `classes.rpy` 拆分）

| 文件 | 优先级 | 包含的类 |
|------|--------|---------|
| `picture.rpy` | `init -4` | `Picture`（图片管理）、`ProportionalScale`（比例缩放显示对象） |
| `goal.rpy` | `init -10` | `Goal`（章节目标） |
| `core_entities.rpy` | `init -2` | `Game`（全局游戏状态）、`Main`（玩家角色）、`NPC`（非玩家角色）、`Calendar`（日历）、`Log`（日志） |
| `world.rpy` | `init -2` | `District`（城市区域）、`Population`（顾客人群）、`Customer`（单个顾客）、`Brothel`（青楼）、`Location`（地点）、`Room`（房间）、`Moon`（月相） |
| `character.rpy` | `init -2` | `Stat`（属性）、`Trait`（特质）、`Perk`（天赋）、`PerkArchetype`（天赋原型）、`Effect`（效果）、`Sexact`（性行为）、`ItemType`（物品类型）、`Personality`（人格）、`Fixation`（执念） |
| `interactions.rpy` | `init -2` | `Event`（事件）、`StoryEvent`（故事事件）、`Quest`（任务）、`GirlInteractionTopic`（互动话题）、`GirlInteraction`（互动实例）、`GirlRecentEvent`（近期事件） |
| `challenges.rpy` | `init -2` | `Spell`（法术）、`MC_challenge`（挑战）、`Resource`（资源）、`Furniture`（家具）、`Loan`（贷款）、`Mod`（MOD） |
| `progression.rpy` | `init -2` | `Achievement`（成就）、`Contract`（契约）、`ContractTask`（契约任务）、`EnemyBrothel`（敌方青楼）、`NGPSetting`（NG+设置）、`MetaUpgrade`（Meta升级） |

#### 2.4.3 女孩类

| 文件 | 优先级 | 说明 |
|------|--------|------|
| `girlclass.rpy` | `init -2` | `Girl` 类（~5,900 行，游戏核心实体：属性、工作、性行为、心情、物品、对话） |
| `girl_files_dict.rpy` | `init -2` | `GirlFilesDict`（女孩包文件管理器）、`globalFilesDict`（全局实例） |

#### 2.4.4 函数层（原 `functions.rpy` 拆分）

| 文件 | 优先级 | 说明 |
|------|--------|------|
| `utils.rpy` | `init -3` | 基础工具：分辨率转换、数学/随机、字符串处理、列表操作、文件类型判断 |
| `girl_factory.rpy` | `init -3` | 女孩生成：`_BK.ini` 解析、包管理、克隆、生成条件判断 |
| `game_systems.rpy` | `init -3` | 游戏系统：回合更新、事件管理、任务刷新、UI 导航、报告生成、设置提交 |
| `economy.rpy` | `init -3` | 经济系统：交易、客户生成、匹配算法、税收、物品商店、表演逻辑 |
| `effects.rpy` | `init -3` | 效果系统：`get_effect`、`add_effects`、`remove_effects`；图片检索：`get_pic_list`、`get_pic` |
| `dialogue.rpy` | `init -3` | 对话辅助：描述生成、偏好符号、Minion 相关、骰子公式解析、审查过滤 |

#### 2.4.5 Python 兼容库

| 文件 | 说明 |
|------|------|
| `pythonlib/ConfigParser.py` | Ren'Py 环境兼容的 ConfigParser |
| `pythonlib/fractions.py` | Ren'Py 环境兼容的 fractions 模块 |

---

### 2.5 `init/` — 游戏初始化

| 文件 | 优先级 | 说明 |
|------|--------|------|
| `settings.rpy` | `init -3` | 游戏设置初始化（分辨率、音量、默认偏好） |
| `start.rpy` | `init` | **游戏启动入口**：`DataLoader.load_all()` 调用、JSON 数据回退初始化、主菜单跳转 |
| `variables.rpy` | `init -3` | 全局变量声明（常量字典、列表、默认值） |

> **加载顺序关键依赖**：`start.rpy` 中的 `DataLoader.load_all()` 依赖 `framework/mixins.rpy` 和 `framework/` 下所有类已定义，因此 `start.rpy` 使用默认 `init` 优先级（比 `-2`、`-3`、`-4`、`-10` 都低）。

---

### 2.6 `systems/` — 功能系统

#### 2.6.1 核心系统

| 文件 | 说明 |
|------|------|
| `achievements.rpy` | 成就系统 UI 与触发逻辑 |
| `data_loader.rpy` | **统一 JSON 加载器**：`DataLoader` 类，提供 `load_achievements()`、`load_challenges()`、`load_resources()` 等方法 |
| `data_exporter.rpy` | 数据导出工具（`.rpy` → JSON 迁移辅助） |
| `dist.rpy` | 区域/地图系统 |
| `endday.rpy` | 每日结束结算流程 |
| `events_dispatcher.rpy` | 事件分发器（日夜事件调度） |
| `farm.rpy` | 农场系统：`Installation`、`Minion`、`FarmProgram`、`Farm` 类 |
| `help.rpy` | 游戏内帮助系统 |
| `items.rpy` | 物品系统 UI 与逻辑 |
| `minigame.rpy` | 小游戏框架 |
| `perks.rpy` | 天赋系统 UI |
| `postings.rpy` | 布告栏/任务发布系统 |
| `powers.rpy` | 力量/能力系统 |
| `security.rpy` | 青楼安保系统 |
| `spells.rpy` | 法术系统 UI |
| `traits.rpy` | 特质系统 UI |

#### 2.6.2 拍卖系统 (已提取为 Mod)

| 位置 | 说明 |
|------|------|
| `custom/mods/Auction House/` | 拍卖系统已提取为 "Auction House" Mod（`mod.rpy` 声明 + `auction.rpy` 核心类 + `auction_screens.rpy` 屏幕）。原 `systems/auction/` 目录已删除。 |

#### 2.6.3 别院系统 → 已剥离为 "Courtyard" Mod

| 位置 | 说明 |
|------|------|
| `custom/mods/Courtyard/` | 庭院系统已提取为 "Courtyard" Mod（`mod.rpy` 注册 + 钩子接线、`courtyard.rpy` 核心类、`screen_courtyard.rpy` 屏幕、`courtyard_upgrade_costs.json` 数据）。原 `systems/courtyard/` 目录已删除。 |

#### 2.6.4 顾客系统 (`systems/customer/`)

| 文件 | 说明 |
|------|------|
| `customer_affixes.rpy` | 顾客词缀系统：`CustomerAffix` 类、词缀生成与应用 |

#### 2.6.5 事件引擎 (`systems/events/`)

| 文件 | 说明 |
|------|------|
| `__init__.rpy` | 事件模块初始化、事件字典注册 |
| `event_engine.rpy` | 事件引擎核心：`EventEngine` 类、条件评估、触发器管理 |

#### 2.6.6 游戏模式 (`systems/gamemodes/`)

| 文件 | 说明 |
|------|------|
| `gamemode.rpy` | `GameMode` 抽象基类 |
| `story_mode.rpy` | 剧情模式实现 |
| `sandbox_mode.rpy` | 沙盒模式实现 |
| `scenario_mode.rpy` | 剧本模式实现 |
| `screen_gamemode.rpy` | 模式选择屏幕 |
| `kidnap_system.rpy` | 掳走系统 |
| `special_girl_npc.rpy` | 特殊女孩 NPC 注册与管理 |

#### 2.6.7 MOD 系统 (`systems/mods/`)

| 文件 | 说明 |
|------|------|
| `mod_api.rpy` | MOD API 定义（钩子接口、版本检查） |
| `mod_hooks.rpy` | MOD 钩子注册与执行 |

#### 2.6.8 注册表 (`systems/registry/`)

> 集中式对象注册表，支持运行时查询与编辑器访问。

| 文件 | 注册内容 |
|------|---------|
| `registry.rpy` | `Registry` 基类 |
| `dialogue_registry.rpy` | 对话标签注册 |
| `event_registry.rpy` | 事件注册 |
| `meta_registry.rpy` | Meta 升级注册 |
| `ngp_registry.rpy` | NG+ 设置注册 |
| `perk_registry.rpy` | 天赋注册 |
| `tag_registry.rpy` | 图片标签注册 |
| `trait_registry.rpy` | 特质注册 |

#### 2.6.9 结算系统 (`systems/settlement/`)

| 文件 | 说明 |
|------|------|
| `settlement_pipeline.rpy` | 夜间结算流水线（收入、经验、事件触发） |
| `phases.rpy` | 结算阶段定义（工作阶段、娱乐阶段、性行为阶段等） |

---

### 2.7 `templates/` — 开发模板

| 路径 | 说明 |
|------|------|
| `event_template.rpy` | 事件脚本模板（供编辑器生成） |
| `scenario_template.rpy` | 剧本模板 |
| `girl_template/_BK.ini` | 女孩包标准 `_BK.ini` 模板 |
| `mod_template/mod_template.rpy` | MOD 开发模板 |

---

### 2.8 `ui/` — 用户界面

| 文件 | 说明 |
|------|------|
| `main.rpy` | 主游戏屏幕（HUD、状态栏） |
| `screens.rpy` | 通用 UI 屏幕（确认框、输入框等） |
| `screen_home.rpy` | 主页/青楼主界面 |
| `content_menu.rpy` | 内容选择菜单 |
| `notify.rpy` | 通知/提示系统 |

---

## 三、加载顺序与依赖关系

### 3.1 Ren'Py Init 优先级总览

```
init -10  ┃ goal.rpy (Goal 类，最早初始化)
init -4   ┃ picture.rpy (Picture, ProportionalScale)
init -3   ┃ mixins.rpy  (EffectBearer, PicHolder, Trackable)
          ┃ variables.rpy
          ┃ settings.rpy
          ┃ functions 拆分文件 (utils, girl_factory, game_systems, economy, effects, dialogue)
          ┃ data_loader.rpy
init -2   ┃ framework 类定义文件 (core_entities, world, character, interactions,
          ┃             challenges, progression, girlclass, girl_files_dict, farm)
          ┃ systems/ 下的大部分系统文件
init      ┃ start.rpy (游戏启动，最后执行，依赖所有前置类与函数)
```

### 3.2 关键依赖链

1. **`Picture` (`init -4`)** → 被 `Population`、`Spell`、`Furniture`、`Achievement` 等几乎所有带图片的类依赖。
2. **`Mixin` (`init -3`)** → `EffectBearer` / `PicHolder` 被 `Game`、`Main`、`Brothel`、`Girl`、`Farm` 等类继承。
3. **`functions` (`init -3`)** → `get_effect`、`add_effects`、`dice`、`weighted_choice` 等全局函数被所有 `init -2` 类的方法调用。
4. **`DataLoader` (`init -2`)** → `start.rpy` (`init`) 中调用 `DataLoader.load_all()` 加载所有 JSON。
5. **`start.rpy` (`init`)** → 初始化 `game`、`MC`、`brothel` 等全局实例，跳转到主菜单。

---

## 四、文件命名约定

| 模式 | 含义 |
|------|------|
| `screen_*.rpy` | Ren'Py 屏幕定义文件（UI 布局） |
| `*_registry.rpy` | 注册表文件（对象查找/枚举） |
| `*_template.rpy` | 代码生成模板 |
| `_fallback_*` | `start.rpy` 中的硬编码回退数据变量 |
| `*.schema.json` | JSON Schema（数据校验） |
| `__init__.rpy` | Python 包风格初始化文件 |

---

## 五、维护提示

1. **新增 JSON 数据**：在 `data/<domain>/` 下创建 `.json`，在 `data_loader.rpy` 的 `DataLoader` 类中新增 `load_*()` 方法，在 `start.rpy` 中添加 `_fallback_*` 回退。
2. **新增框架类**：根据领域放入 `framework/` 下对应文件（如角色相关放 `character.rpy`，世界相关放 `world.rpy`）。若类超过 ~800 行，考虑单独拆分为新文件。
3. **修改 Mixin**：`mixins.rpy` 使用 `init -3`，确保优先级高于使用它的类（`init -2`）。
4. **避免 `dict` 覆盖**：`girlclass.rpy` 曾因局部变量 `dict` 覆盖 Python 内置 `dict` 导致 `Achievement.from_dict()` 的 `isinstance` 检查失效。今后所有局部字典变量应使用 `_dict` / `d` 等命名。
