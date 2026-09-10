# `game/custom/` 与 `game/core/` 目录边界说明

> **设计原则**:  
> - `game/core/` ← **官方核心内容**：核心代码逻辑 + 官方 JSON 数据 + 官方模板  
> - `game/custom/` ← **用户/社区内容**：女孩包和社区 Mod

---

## 快速概览

```
game/
├── core/                        ← 官方核心（随版本更新）
│   ├── config/                  ← 核心配置
│   ├── content/                 ← 官方内容脚本
│   │   ├── city_events/         ← 城市事件
│   │   ├── day_events/          ← 每日事件
│   │   ├── events/              ← 自定义事件入口
│   │   ├── main_story/          ← 主线剧情
│   │   ├── scenarios/           ← 剧本包脚本
│   │   ├── side_stories/        ← 支线剧情
│   │   └── story_events/        ← 故事事件
│   ├── data/                    ← 官方 JSON 数据仓库
│   │   ├── _schemas/            ← JSON Schema 校验
│   │   ├── achievements/        ← 成就
│   │   ├── archetypes/          ← 职业/原型
│   │   ├── challenges/          ← MC 挑战
│   │   ├── chapters/            ← 章节元数据
│   │   ├── contracts/           ← 契约模板
│   │   ├── customers/           ← 顾客词缀
│   │   ├── difficulty/          ← 难度
│   │   ├── events/              ← StoryEvent JSON
│   │   ├── farm/                ← 农场描述/表演
│   │   ├── fixations/           ← 癖好
│   │   ├── goals/               ← 章节目标
│   │   ├── interactions/        ← 互动菜单
│   │   ├── items/               ← 物品
│   │   ├── jobs/                ← 职业表演数据
│   │   ├── meta/                ← 局外养成
│   │   ├── ngp/                 ← NG+ 设置
│   │   ├── perks/               ← 天赋
│   │   ├── personalities/       ← 性格
│   │   ├── powers/              ← 能力/权力
│   │   ├── ranks/               ← 等级
│   │   ├── resources/           ← 建筑资源
│   │   ├── rooms/               ← 房间
│   │   ├── sandbox/             ← 沙盒出身 + 沙盒事件
│   │   ├── scenarios/           ← 剧本注册表
│   │   ├── settings/            ← 全局设置/文本字典
│   │   ├── shops/               ← 商店
│   │   ├── spells/              ← 法术
│   │   ├── stats/               ← 属性
│   │   ├── stories/             ← 故事事件清单
│   │   ├── traits/              ← 特质
│   │   └── worlds/              ← 世界/街区配置
│   ├── framework/               ← 核心类与函数
│   ├── i18n/                    ← 国际化注册
│   ├── init/                    ← 初始化脚本
│   ├── systems/                 ← 子系统（Registry、DataLoader、GameMode 等）
│   ├── templates/               ← 空白模板
│   │   ├── event_template.rpy
│   │   ├── scenario_template.rpy
│   │   ├── girl_template/
│   │   └── mod_template/
│   └── ui/                      ← UI 相关
│
└── custom/                      ← 用户/社区内容（更新安全）
    ├── girls/                   ← 女孩包
    └── mods/                    ← 社区 Mod（含剧本 Mod）
```

---

## `game/core/` — 官方核心

### `core/data/` — 官方 JSON 数据仓库

这是 BK Evolution 数据驱动化的核心目录。所有 JSON 文件在 `init` 阶段由 `DataLoader` 加载到各 Registry。

| 子目录 | 内容 | 对应编辑器 |
|--------|------|-----------|
| `_schemas/` | JSON Schema，校验所有数据文件 | 全部 |
| `achievements/` | 成就定义 | `dev_console` |
| `archetypes/` | 职业/原型 | `girl_pack_editor` |
| `challenges/` | MC 挑战 | `dev_console` |
| `chapters/` | 章节标题等元数据 | `dev_console` |
| `contracts/` | 契约模板 | `dev_console` |
| `customers/` | 顾客词缀（颜色/性格/心情） | `dev_console` |
| `difficulty/` | 难度设置 | `dev_console` |
| `events/` | StoryEvent JSON（69 个事件） | `scenario_editor` |
| `farm/` | 农场描述/表演文本 | `scenario_editor` / `dev_console` |
| `fixations/` | 癖好 | `girl_pack_editor` |
| `goals/` | 章节目标 | `dev_console` |
| `interactions/` | 互动菜单配置 | `scenario_editor` |
| `items/` | 物品定义 | `dev_console` |
| `jobs/` | 职业表演数据 | `dev_console` |
| `meta/` | 局外养成 | `dev_console` |
| `ngp/` | NG+ 设置 | `dev_console` |
| `perks/` | 天赋 | `girl_pack_editor` |
| `personalities/` | 女孩性格 | `girl_pack_editor` |
| `powers/` | 能力/权力 | `dev_console` |
| `ranks/` | 等级定义 | `dev_console` |
| `resources/` | 建筑资源 | `dev_console` |
| `rooms/` | 房间定义 | `dev_console` |
| `sandbox/` | 沙盒出身 + 沙盒事件 | `scenario_editor` |
| `scenarios/` | 剧本注册表 | `scenario_editor` |
| `settings/` | 全局设置与文本字典 | `dev_console` |
| `shops/` | 商店 | `dev_console` |
| `spells/` | 法术 | `dev_console` |
| `stats/` | 属性/技能定义 | `dev_console` |
| `stories/` | 故事事件清单 | `scenario_editor` |
| `traits/` | 特质 | `girl_pack_editor` |
| `worlds/` | 世界/街区配置 | `dev_console` |

> **注意**: 部分 `.rpy` 数据文件（如 `systems/items.rpy`, `systems/perks.rpy`, `systems/powers.rpy`）仍作为 fallback 或运行时数据封装保留，但权威数据已迁移到上表对应的 JSON 文件。

### `core/content/events/` — 自定义事件脚本入口

放 `.rpy` 格式的事件脚本，适合复杂逻辑（多分支、自定义屏幕、特殊动画）。

- `__init__.rpy` — 注册该目录下的事件到 `EventRegistry`。
- Mod 作者如需添加自定义 `.rpy` 事件，优先通过 Mod 系统加载；核心框架的示例事件可放这里。

### `core/content/scenarios/` — 剧本包脚本

剧本模式 (`GameMode.MODE_SCENARIO`) 的 `.rpy` 资源。配合 `core/data/scenarios/scenarios.json` 注册表使用。

### `core/templates/` — 空白模板

给 Mod/女孩包作者复制的起点：

| 文件/目录 | 用途 |
|----------|------|
| `event_template.rpy` | 单个事件的 `.rpy` 模板 |
| `scenario_template.rpy` | 单个剧本包的 `.rpy` 模板 |
| `girl_template/` | 最小女孩包模板，含 `_BK.ini` 样本 |
| `mod_template/` | 最小 Mod 模板，含 `mod_template.rpy` 入口 |

---

## `game/custom/` — 用户/社区内容

这个目录只应该出现两类内容：**女孩包** 和 **Mod**。它的设计目标是：

1. **更新安全**: 游戏版本更新时不会被覆盖。
2. **社区友好**: 玩家和 Mod 作者只需关心这一层。
3. **与核心隔离**: `core/` 里的官方数据、代码、模板可以随意重构，不影响 `custom/` 内容。

### `custom/girls/` — 女孩包

每个子目录是一个独立女孩包：

```
custom/girls/
└── <作者>_<作品>_<角色名>/
    ├── _BK.ini
    ├── portrait/
    ├── profile/
    ├── act/
    └── ...
```

> **对应编辑器**: 女孩包编辑器 (`girl_pack_editor`)

### `custom/mods/` — 社区 Mod

每个子目录是一个独立 Mod：

```
custom/mods/
└── <Mod 名称>/
    ├── mod.rpy       # Mod 入口脚本
    └── ...           # 其他资源
```

Mod 可以：
- 通过 `HookManager` 注册钩子。
- 添加自定义 Trait、Perk、事件、女孩包。
- 实现自定义剧本（Scenario Mod）。

> **注意**: 剧本 Mod 也是一种 Mod，统一放在 `custom/mods/` 下，不要单独设 `custom/scenarios/` 目录。

---

## 与编辑器套件的对应关系

| 编辑器 | 读取路径 | 写入路径 |
|--------|---------|---------|
| 女孩包编辑器 | `custom/girls/*` | `custom/girls/*` |
| 剧本编辑器 - 事件 | `core/data/events/event_dict.json` | `core/data/events/event_dict.json` |
| 剧本编辑器 - 剧本 | `core/data/scenarios/scenarios.json` | `core/data/scenarios/scenarios.json` |
| 开发控制台 - 成就 | `core/data/achievements/achievements.json` | `core/data/achievements/achievements.json` |
| 开发控制台 - 难度 | `core/data/difficulty/difficulty.json` | `core/data/difficulty/difficulty.json` |
| 开发控制台 - NG+ | `core/data/ngp/ngp_settings.json` | `core/data/ngp/ngp_settings.json` |
| 开发控制台 - 元养成 | `core/data/meta/meta_progression.json` | `core/data/meta/meta_progression.json` |
| 开发控制台 - 目标 | `core/data/goals/chapter_goals.json` | `core/data/goals/chapter_goals.json` |
| 开发控制台 - 顾客词缀 | `core/data/customers/customer_affixes.json` | `core/data/customers/customer_affixes.json` |
| 女孩包编辑器 - Trait/Perk | `core/data/traits/traits.json`, `core/data/perks/perks.json` | `core/data/traits/traits.json`, `core/data/perks/perks.json` |

---

## 使用建议

### 如果你是玩家

- 女孩包 → 解压到 `custom/girls/`
- Mod → 解压到 `custom/mods/`
- 不要手动改 `core/data/` 下的 JSON，用编辑器更安全。

### 如果你是 Mod 作者

1. **改官方数据**: 用编辑器改 `core/data/` 下的 JSON（有 Schema 校验）。
2. **写自定义逻辑**: 写 `.rpy` 脚本，通过 Mod 系统注册；或参考 `core/templates/` 里的模板。
3. **做女孩包**: 复制 `core/templates/girl_template/`，改名后放 `custom/girls/`。
4. **做剧本 Mod**: 复制 `core/templates/scenario_template.rpy`，结合 `core/data/scenarios/scenarios.json` 注册；Mod 脚本放 `custom/mods/<你的 Mod>/`。

### 如果你是核心开发者

- 新增数据类别时，在 `core/data/` 下新建子目录。
- 必须在 `core/data/_schemas/` 中补充 JSON Schema。
- 在 `DataLoader` 中新增对应的 `load_xxx()` 方法。
- 绝对不要把新的官方 JSON 数据放到 `custom/data/`（该目录已废弃）。

---

## 历史变更

BK Evolution 早期曾将 JSON 数据放在 `game/custom/data/`，这与 `custom/` 作为"用户内容"层的设计意图冲突。现已全部迁移：

| 原位置 | 新位置 |
|--------|--------|
| `game/custom/data/` | `game/core/data/` |
| `game/custom/events/` | `game/core/content/events/` |
| `game/custom/scenarios/` | `game/core/content/scenarios/` |
| `game/custom/templates/` | `game/core/templates/` |

`game/custom/` 现在严格只保留 `girls/` 和 `mods/`。
