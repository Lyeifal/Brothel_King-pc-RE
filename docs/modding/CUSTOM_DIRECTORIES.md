# `game/custom/` 与 `game/core/` 目录边界说明

> 最后更新: 2026-09-11（与代码核对）
>
> **设计原则**:
> - `game/core/` ← **官方核心内容**：核心代码逻辑 + 官方 JSON 数据 + 官方模板
> - `game/custom/` ← **用户/社区内容**：女孩包和社区 Mod

---

## 快速概览

```
game/
├── core/                        ← 官方核心（随版本更新）
│   ├── config/                  ← 核心配置（含 screens.rpy 等）
│   ├── content/                 ← 官方内容脚本
│   │   ├── city_events/         ← 城市事件
│   │   ├── day_events/          ← 每日事件
│   │   ├── events/              ← 自定义事件入口（__init__.rpy 注册）
│   │   ├── main_story/          ← 主线剧情
│   │   ├── scenarios/           ← 剧本包脚本
│   │   ├── side_stories/        ← 支线剧情
│   │   └── story_events/        ← 故事事件
│   ├── data/                    ← 官方 JSON 数据仓库（含少量 fallback .rpy）
│   ├── framework/               ← 核心类与函数（含 Mod() 类、Game/GameServices 等）
│   ├── i18n/                    ← 国际化注册（json_i18n.rpy）
│   ├── init/                    ← 初始化脚本（variables.rpy / settings.rpy / start.rpy）
│   ├── systems/                 ← 子系统（Registry、DataLoader、services、mods 等）
│   ├── templates/               ← 空白模板
│   │   ├── event_template.rpy
│   │   ├── scenario_template.rpy
│   │   ├── girl_template/
│   │   └── mod_template/        ← v2 Mod 模板（register_mod + manifest）
│   ├── tools/                   ← 游戏内工具（test_runner、dev_console）
│   └── ui/                      ← UI 相关（screen_home.rpy、main.rpy 等）
│
└── custom/                      ← 用户/社区内容（更新安全）
    ├── girls/                   ← 女孩包
    └── mods/                    ← 社区 Mod（v1 与 v2 共存）
```

---

## `game/core/` — 官方核心

### `core/data/` — 官方 JSON 数据仓库

这是 BK Evolution 数据驱动化的核心目录。所有 JSON 文件在 `init` 阶段由 `DataLoader`（`game/core/systems/data_loader.rpy`）加载到各 Registry（`game/core/systems/registry/`）。

| 子目录 | 内容 | 对应编辑器 |
|--------|------|-----------|
| `_schemas/` | JSON Schema，校验所有数据文件 | 全部 |
| `achievements/` | 成就定义 | `dev_console` |
| `archetypes/` | 职业/原型 | `girl_pack_editor` |
| `challenges/` | MC 挑战 | `dev_console` |
| `chapters/` | 章节标题等元数据 | `dev_console` |
| `classes/` | 主角职业/法术书 | `dev_console` |
| `contracts/` | 契约模板 | `dev_console` |
| `customers/` | 顾客词缀（颜色/性格/心情） | `dev_console` |
| `difficulty/` | 难度设置 | `dev_console` |
| `economy/` | 青楼参数/税收等经济参数 | `dev_console` |
| `events/` | StoryEvent JSON（event_dict.json，69 个事件） | `scenario_editor` |
| `farm/` | 农场描述/表演文本 | `scenario_editor` / `dev_console` |
| `fixations/` | 癖好 | `girl_pack_editor` |
| `goals/` | 章节目标 | `dev_console` |
| `interactions/` | 互动菜单配置 | `scenario_editor` |
| `items/` | 物品定义 | `dev_console` |
| `jobs/` | 职业表演数据 | `dev_console` |
| `meta/` | 局外养成 | `dev_console` |
| `minions/` | 爪牙（minion）定义 | `dev_console` |
| `ngp/` | NG+ 设置 | `dev_console` |
| `perks/` | 天赋 | `girl_pack_editor` |
| `personalities/` | 女孩性格 | `girl_pack_editor` |
| `powers/` | 能力/权力 | `dev_console` |
| `ranks/` | 等级 | `dev_console` |
| `resources/` | 建筑资源 | `dev_console` |
| `rooms/` | 房间 | `dev_console` |
| `sandbox/` | 沙盒出身 + 沙盒事件 | `scenario_editor` |
| `scenarios/` | 剧本注册表 | `scenario_editor` |
| `settings/` | 全局设置/文本字典/音频注册表/图片映射 | `dev_console` |
| `shops/` | 商店（shops.json + shop_economy.json） | `dev_console` |
| `spells/` | 法术 + 月相 | `dev_console` |
| `stats/` | 属性 | `dev_console` |
| `stories/` | 故事事件清单（story_events.json） | `scenario_editor` |
| `traits/` | 特质 | `girl_pack_editor` |
| `worlds/` | 世界/街区配置 | `dev_console` |

> **注意**: 部分 `.rpy` 文件（`data/items.rpy`、`data/jobs.rpy`、`data/perks.rpy`、`data/powers.rpy`、`data/settings.rpy`、`data/spells.rpy`）仍作为 fallback 硬编码保留——JSON 缺失时游戏仍可启动。权威数据始终是同名子目录下的 JSON。详见 [`../migration/DATA_MIGRATION.md`](../migration/DATA_MIGRATION.md)。

### `core/content/events/` — 自定义事件脚本入口

放 `.rpy` 格式的事件脚本，适合复杂逻辑（多分支、自定义屏幕、特殊动画）。

- `__init__.rpy` — 注册该目录下的事件到 `EventRegistry`。
- Mod 作者如需添加自定义 `.rpy` 事件，优先通过 Mod 系统加载；核心框架的示例事件可放这里。

### `core/content/scenarios/` — 剧本包脚本

剧本模式 (`GameMode.MODE_SCENARIO`) 的 `.rpy` 资源。配合 `core/data/scenarios/scenarios.json` 注册表使用。

### `core/systems/mods/` — Mod 机制实现

| 文件 | 说明 |
|------|------|
| `mod_api.rpy` | v1 `ModAPI`（Registry 包装 + HookManager 包装） |
| `mod_api_v2.rpy` | v2 `ModAPIV2`（register_mod / manifest / 16 个标准化钩子） |
| `mod_hooks.rpy` | Phase 6 `HookManager`（v1 兼容层钩子分发器） |

详见 [`MOD_API.md`](MOD_API.md)。

### `core/templates/` — 空白模板

给 Mod/女孩包作者复制的起点：

| 文件/目录 | 用途 |
|----------|------|
| `event_template.rpy` | 单个事件的 `.rpy` 模板 |
| `scenario_template.rpy` | 单个剧本包的 `.rpy` 模板 |
| `girl_template/` | 最小女孩包模板，含 `_BK.ini` 样本 |
| `mod_template/mod_template.rpy` | v2 Mod 模板：`register_mod` + manifest 全字段 + `register_hook` 示例 |

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
├── Auction House/            ← v2 Mod 范例（拍卖行，权威参考实现）
│   ├── mod.rpy               # register_mod 入口 + 主页菜单按钮 screen
│   ├── auction.rpy           # 拍卖核心类（AuctionLot/AuctionSession/AuctionHouse）
│   └── auction_screens.rpy   # UI screen
└── Goldo's cool mod/         ← v1 Mod 教程范例（含 title.png）
    └── goldo's cool mod.rpy  # Mod(...) 构造 + events + help_prompts + labels
```

Mod 可以：

- 通过 v1 `Mod()` 或 v2 `services.mod_api_v2.register_mod()` 注册（两套机制共存，见 [`MOD_API.md`](MOD_API.md)）；
- 注册钩子（v2 标准化钩子或 v1 HookManager）；
- 添加自定义 Trait、Perk、事件、游戏模式、出身、剧本；
- 声明主页右侧菜单按钮（`home_rightmenu_add_buttons`）。

> **注意**: 剧本 Mod 也是一种 Mod，统一放在 `custom/mods/` 下，不要单独设 `custom/scenarios/` 目录。

---

## 与编辑器套件的对应关系

编辑器套件位于 `tools/bk_editor/`（详见 [`../tools/TOOLS.md`](../tools/TOOLS.md) 与 `tools/bk_editor/README.md`）。

| 编辑器 | 读取路径 | 写入路径 |
|--------|---------|---------|
| 女孩包编辑器 | `custom/girls/*` | `custom/girls/*` |
| 剧本编辑器 - 事件 | `core/data/stories/story_events.json`、`core/data/sandbox/events.json` | 同读取路径 |
| 剧本编辑器 - 剧本 | `core/data/scenarios/scenarios.json` | `core/data/scenarios/scenarios.json` |
| 开发控制台 - 成就 | `core/data/achievements/achievements.json` | `core/data/achievements/achievements.json` |
| 开发控制台 - 难度 | `core/data/difficulty/difficulty.json` | `core/data/difficulty/difficulty.json` |
| 开发控制台 - NG+ | `core/data/ngp/ngp_settings.json` | `core/data/ngp/ngp_settings.json` |
| 开发控制台 - 元养成 | `core/data/meta/meta_progression.json` | `core/data/meta/meta_progression.json` |
| 女孩包编辑器 - Trait/Perk | `core/data/traits/traits.json`、`core/data/perks/perks.json` | 同读取路径 |

---

## 使用建议

### 如果你是玩家

- 女孩包 → 解压到 `custom/girls/`
- Mod → 解压到 `custom/mods/`
- v1 Mod 在主菜单 Mods 界面开关；v2 Mod 安装即生效，删除文件夹即停用。
- 不要手动改 `core/data/` 下的 JSON，用编辑器更安全。

### 如果你是 Mod 作者

1. **新 Mod 用 v2**：复制 `core/templates/mod_template/`，参考 `custom/mods/Auction House/` 的三文件结构；需要"逐存档开关"时才用 v1 `Mod()`（参考 Goldo's cool mod）。
2. **改官方数据**: 用编辑器改 `core/data/` 下的 JSON（有 Schema 校验）。
3. **做女孩包**: 复制 `core/templates/girl_template/`，改名后放 `custom/girls/`。
4. **做剧本 Mod**: 复制 `core/templates/scenario_template.rpy`，结合 `core/data/scenarios/scenarios.json` 注册；Mod 脚本放 `custom/mods/<你的 Mod>/`。

### 如果你是核心开发者

- 新增数据类别时，在 `core/data/` 下新建子目录。
- 必须在 `core/data/_schemas/` 中补充 JSON Schema。
- 在 `DataLoader`（`game/core/systems/data_loader.rpy`）中新增对应的 `load_xxx()` 方法。
- **保留硬编码 fallback**，确保 JSON 文件缺失时游戏仍可启动。
- 绝对不要把新的官方 JSON 数据放到 `custom/data/`（该目录已废弃且不存在）。

---

## 历史变更

BK Evolution 早期曾将 JSON 数据放在 `game/custom/data/`，这与 `custom/` 作为"用户内容"层的设计意图冲突。现已全部迁移：

| 原位置 | 新位置 |
|--------|--------|
| `game/custom/data/` | `game/core/data/` |
| `game/custom/events/` | `game/core/content/events/` |
| `game/custom/scenarios/` | `game/core/content/scenarios/` |
| `game/custom/templates/` | `game/core/templates/` |

`game/custom/` 现在严格只保留 `girls/` 和 `mods/` 两个子目录（2026-09-11 与代码核对确认，不存在 `custom/config/` 等其他子目录）。

---

## 相关文档

- [`MOD_API.md`](MOD_API.md) — v1/v2 Mod 机制完整参考（含 Auction House 范例讲解）
- [`../migration/DATA_MIGRATION.md`](../migration/DATA_MIGRATION.md) — JSON 数据迁移记录与 fallback 清单
- [`../tools/TOOLS.md`](../tools/TOOLS.md) — 编辑器套件等工具清单
- [`../../game/core/templates/mod_template/mod_template.rpy`](../../game/core/templates/mod_template/mod_template.rpy) — v2 Mod 模板
