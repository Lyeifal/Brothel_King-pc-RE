# BK Evolution 系统架构文档

> 最后更新: 2026-09-11（与代码核对，分支 bk-evolution）

本目录是 BK Evolution 分支核心系统的架构说明。所有路径、类名、行数、钩子调用点均已对当前代码逐一 grep 核实；重整前旧版快照见 `docs/archive/pre-reorg-2026-09/architecture/`，可对照。

> **注意**：`classes.rpy` / `functions.rpy` 早已拆分为 `framework/` 下的多个小文件，任何文档引用这两个文件名均为过时信息。

---

## 子系统状态矩阵

| 子系统 | 状态 | 核心文件 | 说明 |
|--------|------|---------|------|
| 服务容器 GameServices | 🚧 进行中 | `systems/services/`、`config/game_config.rpy` | 11 个服务已注册（init -12 容器）；`mod_api`/`data_loader` 属性未接线；接口抽象（interfaces/）待完成 |
| Girl 组件化 | 🚧 进行中 | `framework/girlclass.rpy`（3,910 行，原 ~5,900）、`framework/girl/`（15 组件） | 15/15 组件类就位、156 个 `_impl` 别名；部分方法体仍在宿主类（过渡形态） |
| UI 屏幕提取 | ✅ 完成 | `ui/screens.rpy`（620 行，原 8,886）、`ui/screens/`（16 文件） | screens.rpy 已无 screen，仅剩 image/style/label；16 文件按域拆分 |
| Mod 系统 | 🚧 进行中 | `framework/challenges.rpy`（v1 Mod）、`systems/mods/` | v1/v2 并存；16 个 v2 钩子全部接线（纯通知型）；`cancel_hook` 拦截语义尚无调用点；两套钩子存储未统一 |
| DataLoader / JSON 化 | 🚧 进行中 | `systems/data_loader.rpy`（1,319 行） | ~45 个 load_* 方法；fallback 模式刻意保留未清理（双数据源共存） |
| Registry 注册表 | ✅ 完成 | `systems/registry/`（10 文件） | 基类 + 8 个子类 + UnlockRegistry；覆盖语义支持 Mod 替换 |
| Trait / Perk | ✅ 完成 | `framework/character.rpy`、`data/traits/`（131 个）、`data/perks/`（53 个） | JSON 驱动 + GirlTraits 组件消费 |
| 事件系统 | 🚧 进行中 | `framework/interactions.rpy`（StoryEvent）、`systems/events_dispatcher.rpy`（8,611 行）、`systems/events/` | EventEngine/EventRegistry 就位；**EventBridge 旧→新同步因调用不存在的方法而静默失效**（详见 event.md 2.4） |
| Game / GameMode | ✅ 完成 | `framework/core_entities.rpy`（Game :19）、`systems/gamemodes/` | story/sandbox/scenario 三模式注册完毕；modes 过滤贯穿事件入队 |
| Goal | ✅ 完成 | `framework/goal.rpy`、`data/goals/chapter_goals.json`（7 章） | settings.rpy 独立加载（含 fallback）；5 种类型门控章节推进 |
| CustomerAffix | ✅ 完成 | `systems/customer/customer_affixes.rpy`、`data/customers/customer_affixes.json` | 三维词缀 + 8 级颜色；自载 JSON + 硬编码 fallback |
| Girl Pack | ✅ 完成 | `framework/girl_files_dict.rpy`、`framework/girl_factory.rpy`、`custom/girls/`（102 包） | GirlFilesDict 服务化；三层包验证 |
| 编辑器套件 | ✅ 完成 | `tools/bk_editor/`（三编辑器） | 女孩包/剧本/开发控制台；JSON 契约经 DataLoader |
| I18N | 🚧 进行中 | `systems/services/i18n_service.rpy`、`i18n/json_i18n.rpy`、`tl/` | I18nService 服务化；翻译覆盖持续扩充 |

## 文档清单

### 基础设施（本次新增）

| 文档 | 内容 |
|------|------|
| [services.md](services.md) | GameServices 容器、11 个已注册服务表、GameConfig、init 优先级链 |
| [girl_components.md](girl_components.md) | Girl 组件系统：15 组件清单、委托模式、`_impl` 别名、get_stat 双倍计入 bug 教训 |
| [ui_screens.md](ui_screens.md) | UI 屏幕架构：screens.rpy 剩余内容 + ui/screens/ 16 文件逐文件 screen 清单 |
| [mod_system.md](mod_system.md) | v1 Mod 类与 v2 ModAPIV2 并存架构、注册流程、18 个钩子点全表（调用点已逐一核实）、HookManager 关系 |

### 子系统（本次刷新）

| 文档 | 系统 | 核心文件 |
|------|------|---------|
| [data_loader.md](data_loader.md) | DataLoader + fallback 模式 | `systems/data_loader.rpy` |
| [registry.md](registry.md) | Registry 注册表体系 | `systems/registry/` |
| [trait_perk.md](trait_perk.md) | Trait / Perk | `framework/character.rpy`、`data/traits/`、`data/perks/` |
| [event.md](event.md) | StoryEvent / EventEngine / EventBridge | `framework/interactions.rpy`、`systems/events/`、`events_dispatcher.rpy` |
| [gamemode.md](gamemode.md) | Game / GameMode | `framework/core_entities.rpy`、`systems/gamemodes/` |
| [goal.md](goal.md) | Goal 章节目标 | `framework/goal.rpy`、`data/goals/` |
| [customer_affix.md](customer_affix.md) | CustomerAffix 词缀 | `systems/customer/`、`data/customers/` |
| [girl_pack.md](girl_pack.md) | 女孩包系统 | `framework/girl_files_dict.rpy`、`girl_factory.rpy`、`custom/girls/` |
| [editor_suite.md](editor_suite.md) | 编辑器套件（精简） | `tools/bk_editor/` |

## 阅读顺序建议

1. 先读 [services.md](services.md) 了解 init 优先级链——所有系统的注册时机都依赖它。
2. 按兴趣读子系统文档；跨系统问题（Mod、数据流）读 [mod_system.md](mod_system.md) 与 [data_loader.md](data_loader.md)。
3. 目录级文件职责另见 `game/core/README.md`。

---

## 相关文档

- `game/core/README.md` — game/core 目录结构指南
- `tools/bk_editor/README.md` — 编辑器套件使用文档
- `docs/i18n/` — 国际化文档
- `docs/tools/` — 工具链文档
- 旧版快照：`docs/archive/pre-reorg-2026-09/architecture/`
