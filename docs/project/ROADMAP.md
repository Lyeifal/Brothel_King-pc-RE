# BK Evolution — 总览路线图

> 最后更新: 2026-09-11（与代码核对）
> **项目**: Brothel King Evolution（数据驱动改造 + 游戏架构重构 + 可视化编辑器）
> **分支**: `bk-evolution`
> **技术栈**: Ren'Py 8.2.0, Python 3.9, tkinter（零第三方依赖）

本文档合并自两份旧路线图（`docs/archive/pre-reorg-2026-09/ROADMAP.md`、`BK_EVOLUTION_ROADMAP.md`），全部条目已与当前代码核对。逐提交明细以 [REFACTORING_PROGRESS.md](REFACTORING_PROGRESS.md) 为真源（基线提交 `b09f55e` 之后累计 65 次提交，2026-09-11 `git log` 核实）。

**项目目标**：将 BK 从纯代码驱动的 Ren'Py 视觉小说，改造为**数据驱动 + Mod 友好**的框架——JSON 承载游戏数据、Registry/DataLoader 分层、服务容器解耦全局状态、可视化编辑器降低 Mod 制作门槛。

---

## 1. 总体进度

| 阶段 | 内容 | 状态 |
|------|------|------|
| 数据驱动 Phase A–G | 基础设施、编辑器 GUI、硬编码导出 JSON、女孩包工具、剧本编辑器、去硬编码 | ✅ 已完成 |
| 数据驱动 Phase H | i18n 全面适配（`_i18n` 后缀约定） | ✅ 已完成 |
| 数据驱动 Phase I | 系统解耦（UnlockRegistry + Farm/Location 分离） | ✅ 已完成 |
| 重构 Phase 0 | 紧急修复（I18N + 性能） | ✅ 已完成 |
| 重构 Phase 1 | 核心架构：服务容器 + 事件桥 | ✅ 已完成 |
| 重构 Phase 2 | Girl 组件分解（girlclass 5,900 → 3,910 行） | ✅ 已完成 |
| 重构 Phase 7 | Girl 组件化收官：方法体全量迁移（3,910 → 1,148 行，16 组件） | ✅ 已完成 |
| 重构 Phase 3 | UI 架构：屏幕提取（screens.rpy 8,886 → 620 行） | ✅ 已完成 |
| 重构 Phase 4 | I18N 系统（I18nService） | ✅ 已完成 |
| 重构 Phase 5–6 | Mod API v2 + 开发工具（Dev Console / Test Runner） | ✅ 已完成 |
| 后续增量 | Mod v2 钩子接线 + UI 集成、拍卖系统 Mod 化 | ✅ 已完成 |

---

## 2. 已完成（✅）

### 2.1 数据驱动 Phase A–G（2026-06）

- ✅ **Phase A 基础设施** — `tools/bk_editor/` 包结构、`game/core/data/` 目录体系、JSON Schema（`_schemas/`）、`DataLoader`（`game/core/systems/data_loader.rpy`，1,319 行）
- ✅ **Phase B/C 编辑器 GUI** — 剧情事件编辑器（StoryEvent CRUD）、出身编辑器、Trait/Perk CRUD + Effect 可视化
- ✅ **Phase D 硬编码导出** — 131 个 Trait、53 个 Perk 等导出至 JSON
- ✅ **Phase E 女孩包工具** — `_BK.ini` 可视化编辑（8 个标签页）
- ✅ **Phase F 剧本编辑器** — Scenario 完整 CRUD + JSON Schema 验证
- ✅ **Phase G 去硬编码** — Origin/Trait/Perk/Powers/Challenges/Contracts/Resources/Achievements/Goals/Difficulty 等 50+ 领域迁移至 `game/core/data/` JSON（完整清单见 [migration/DATA_MIGRATION.md](../migration/DATA_MIGRATION.md)）
- ✅ **Phase H i18n 适配** — 105 个 JSON 数据文件完成 `_i18n` 适配；`json_i18n.rpy` 改为纯 `_i18n` 后缀扫描（白名单已移除）
- ✅ **Phase I 系统解耦** — `UnlockRegistry`（`systems/registry/unlock_registry.rpy`）；`Farm.active` 改为 property 自动同步解锁状态；`farm.action` 混用修复

### 2.2 重构 Phase 0–3（2026-09，详见 REFACTORING_PROGRESS.md）

- ✅ **Phase 0 紧急修复** — I18N 问题修复 + 性能（图片缓存、惰性标签解析、AutoRepair 降频）
- ✅ **Phase 1 核心架构**
  - 服务容器 `GameServices`（`systems/services/service_container.rpy`，init -12），11 个服务已注册（见 PROJECT_GUIDE §5）
  - 事件桥 EventBridge（`systems/events/event_bridge.rpy`）同步旧事件系统与新 EventEngine
  - 配置集中化 GameConfig（`config/game_config.rpy`），支持 `custom/config/` JSON 覆盖
  - Init 依赖断言（`init/dependency_graph.rpy` + `require_service()`）
- ✅ **Phase 2 Girl 组件分解**
  - `girlclass.rpy` 5,900 → **3,910 行**（-34%）；`framework/girl/` 下 15 个 `girl_*.rpy` 组件 + `__init__.rpy`（16 个文件）
  - 33 个大块方法迁移完毕（stats/mood/economy/sex/dialogue/traits/items/schedule/training/effects/generation/pictures/relationships），迁移模式：实现进组件 → Girl 类委托
- ✅ **Phase 7 Girl 组件化收官** (2026-09-11，批次1-14，15 次提交)
  - `girlclass.rpy` 3,910 → **1,148 行**（累计 -81%）；16 组件（新建 `girl_progression.rpy` 进阶组件）
  - 再迁移 ~120 个方法；修复 `generate_preferences` 双重执行、change_stat 技能上限回归；清理 6 处组件过时副本、3 处重复定义死壳
  - 每批次 lint 通过；委托壳模式全程 2,000+ 旧调用点零改动
- ✅ **Phase 3 UI 架构**
  - `ui/screens.rpy` 8,886 → **620 行**；108 个 screen 提取至 `ui/screens/` 16 个文件，经 `temp/verify_extract.py` 与基线逐字比对一致；当前 112 个 screen 声明（后续新增 `mods` 等 4 个）
  - ViewModel 层（`ui/view_models/`）
- ✅ **Phase 4 I18N 系统**
  - `I18nService`（`systems/services/i18n_service.rpy`）：`t()` / `tn()` / `tc()` / `pronoun()` / `possessive()`
  - `plural()` / `article()` 语言感知；语言扩展走 `custom/config/languages.json`
  - JSON `_i18n` 迁移完成；中文覆盖对话 27,933/29,367 块
- ✅ **Phase 5–6 Mod API v2 + 开发工具**
  - `ModAPIV2`（`systems/mods/mod_api_v2.rpy`，219 行）：版本化 manifest、`register_hook`/`execute_hook`/`cancel_hook`
  - **16 个钩子点全部接线**（2026-09-11，`c6b3fa2`）：girl_generated/acquired/sold/runaway、day_starting/ending、night_starting/finished、week_starting、event_triggering/finished、chapter_starting/finished、security_event、game_saved/loaded——已 grep 核实 16 处 `execute_hook` 调用点
  - **UI 集成**（`1788c04`）：manifest 支持 `home_rightmenu_add_buttons`；`get_menu_buttons()`/`get_mod_info()`；Mods 界面只读展示 v2 Mod（常驻激活语义）
  - Dev Console（`game/core/tools/dev_console/`，Shift+O，仅 developer mode）；Test Runner（`game/core/tools/test_runner.rpy`，主菜单 Tests 按钮，组件冒烟测试 + ModAPIV2 测试）
  - 拍卖系统从 `systems/auction` 提取为范例 Mod：`game/custom/mods/Auction House/`（已转 v2）

### 2.3 验证记录

- ✅ lint 通过（仅历史警告），游戏可正常启动至主菜单（2026-09-10 基线验证）
- ✅ `tools/verify_mod_api.py` 静态断言 + 桩环境全流程模拟全过；发现并修复 `cancel_hook` 经 `execute_hook` 中转导致取消语义丢失的 bug
- ✅ 屏幕提取逐字比对一致（`temp/verify_extract.py`）

---

## 3. 进行中（🚧）

| 事项 | 说明 |
|------|------|
| 🚧 机翻质量审核 | 大批机器翻译已回填（对话与 strings），需人工抽查语义、语气、占位符正确性；工具：`tools/audit_placeholders.py`、`tools/check_excel*.py` |
| 🚧 剧情文本润色 | 中文剧情文本的通顺度与人名/术语一致性润色 |
| 🚧 旧存档兼容观察 | 重构后的存档格式依赖 AutoRepair 自动修复，需持续观察玩家旧存档载入反馈（与下节"遗留待办"第 6 项相关） |

---

## 4. 遗留待办（⏳，按价值排序）

| # | 事项 | 现状（已核实） | 价值/理由 |
|---|------|----------------|-----------|
| 1 | ⏳ Mod v2 `cancel_hook` 消费方 | 16 个钩子点已接线但**全部为纯通知型**；游戏流程内无任何 `cancel_hook` 调用点（仅 `test_runner.rpy:352` 测试用） | 让 Mod 能真正拦截/取消事件，完成 v2 钩子语义闭环 |
| 2 | ⏳ fallback 字典清理 | `_fallback_*` 硬编码回退仍保留在 `start.rpy`、`settings.rpy`、各 registry 中 | JSON 迁移 100% 无回归验证后移除，消除双份数据源 |
| 3 | ⏳ `Girl.__init__` 拆分 | 约 120 行，属性初始化 + 组件实例化，有意保持原样 | 拆到各组件 `init_*` 有存档兼容风险，性价比低，暂缓 |
| 4 | ✅ ~800 行小方法归组 — 已完成 (Phase 7, 2026-09-11)：批次1-14 全部归组迁移，girlclass 仅剩 __init__+委托壳+24 活别名 | — |
| 5 | ✅ `change_mood` 与 GirlMood 归属 — 已完成 (Phase 7 批次1)：心情簇 5 方法实现全部迁入 GirlMood，边界清晰 | — |
| 6 | ⏳ 旧存档兼容观察 | AutoRepair 负责旧档修复，尚无大规模负反馈 | 长期观察项；出问题再补修复规则 |

其他已知小问题（顺带跟进，不单独立项）：
- `ui/screens/` 中 `girls` screen 存在两处定义（`screen_girl_list.rpy:9` 与 `screen_misc.rpy:80`），需确认是否有意覆盖
- `events_dispatcher.rpy` 8,611 行仍是最大遗留文件，可随事件系统演进逐步拆解

---

## 5. 未来方向（⏳ 畅想，未立项）

| 方向 | 说明 |
|------|------|
| 新语言接入 | 语言扩展机制已就绪（`custom/config/languages.json` + `translations.rpy` 字体映射），接入新语言只需翻译文件 + 字体配置 |
| 编辑器增强 | 剧本编辑器支持 District/Location/NPC/Shop 的 JSON 化（当前仍硬编码在 `start.rpy`，编辑器仅提供参考查看器）；更多 `core/data/` 领域的编辑器标签页 |
| 事件系统演进 | EventEngine 完全接管旧 `city_events`/`daily_events` 路径后，退役 EventBridge 与事件桥兼容层 |
| Mod 生态 | 更多官方范例 Mod（参考 `Auction House`）；v1 Mod API 退役评估 |

> 本节为方向性设想，不代表已承诺的排期；开工前请在 [REFACTORING_PROGRESS.md](REFACTORING_PROGRESS.md) 追加提交记录。

---

## 6. 相关文档

| 文档 | 说明 |
|------|------|
| [PROJECT_GUIDE.md](PROJECT_GUIDE.md) | 项目指南：目录标准、Init 链、服务访问、数据驱动架构 |
| [REFACTORING_PROGRESS.md](REFACTORING_PROGRESS.md) | 重构进度真源（逐提交链、组件迁移明细） |
| [../README.md](../README.md) | 文档中心 |
| [../migration/DATA_MIGRATION.md](../migration/DATA_MIGRATION.md) | 硬编码 → JSON 迁移完整清单 |
| [../architecture/README.md](../architecture/README.md) | 子系统架构文档索引 |
| [../i18n/I18N_ROADMAP.md](../i18n/I18N_ROADMAP.md) | i18n 状态、约定与工具链 |
| [../modding/CUSTOM_DIRECTORIES.md](../modding/CUSTOM_DIRECTORIES.md) | `custom/` 与 `core/` 目录边界 |
