# BK Evolution — 总览路线图

> **项目**: Brothel King Evolution (数据驱动改造 + 可视化编辑器)  
> **分支**: `bk-evolution`  
> **技术栈**: Ren'Py 8.2.0, Python 3.9, tkinter (零第三方依赖)  
> **最后更新**: 2026-06-08

---

## 目录

- [项目目标](#项目目标)
- [总体进度](#总体进度)
- [核心架构](#核心架构)
- [Phase A-G 详情](#phase-ag-详情)
- [系统解耦记录](#系统解耦记录)
- [技术债务](#技术债务)
- [测试记录](#测试记录)
- [附录：目录结构](#附录目录结构)
- [相关文档](#相关文档)

---

## 项目目标

将 BK 从一个纯代码驱动的 Ren'Py 视觉小说，改造为**数据驱动 + 可视化编辑**的 Mod 友好型框架：

1. **编辑器工具链**: 提供独立 GUI 工具 `python tools/bk_editor.py`，让非程序员也能制作 Mod 内容
2. **数据驱动改造**: 将硬编码的 Trait、Perk、Origin、StoryEvent、Scenario 等逐步提取到 JSON
3. **Mod 生态**: 女孩包统一放在 `game/custom/girls/`，保持 `_BK.ini` 兼容；剧本/数据 Mod 通过 `game/core/data/` 和 `game/custom/` 扩展
4. **零新增 Lint 错误**: 所有改动保持 `lint` 通过
5. **系统解耦**: Farm / World / Location / Unlock 四个系统各自独立，通过 Registry 通信

---

## 总体进度

| Phase | 内容 | 状态 | 完成度 |
|---|---|---|---|
| A | 基础设施 (核心模块、JSON Schema、目录结构) | ✅ 已完成 | 100% |
| B | 剧情事件编辑器 + 出身编辑器 | ✅ 已完成 | 100% |
| C | 女孩系统编辑器 (Trait/Perk CRUD + Effect 可视化) | ✅ 已完成 | 100% |
| D | 硬编码导出 JSON | ✅ 已完成 | 100% |
| E | 女孩包制作工具 (`_BK.ini` 可视化) | ✅ 已完成 | 100% |
| F | 剧本编辑器完善 (Scenario CRUD) | ✅ 已完成 | 100% |
| G | 代码去硬编码 (从 .rpy 迁移到 JSON) | ✅ 阶段性完成 | 95% |
| H | i18n 全面适配 (`_i18n` 后缀约定) | ✅ 已完成 | 100% |
| I | 系统解耦 (UnlockRegistry + Farm/Location 分离) | ✅ 已完成 | 100% |

---

## 核心架构

```
┌─────────────────────────────────────────────┐
│              Game State Layer                │
│  (持久化到存档: MC, girls, calendar, flags)  │
├─────────────────────────────────────────────┤
│              Registry Layer                  │
│  (只读配置: traits, perks, locations,        │
│   unlock_rules, events — JSON 驱动)          │
├─────────────────────────────────────────────┤
│              System Layer                    │
│  (Farm, World, Customer, Economy...)         │
│  系统间通过 Registry + Event 通信，          │
│  禁止直接引用全局变量                         │
├─────────────────────────────────────────────┤
│              UI Layer                        │
│  (screens.rpy, main.rpy...)                  │
│  只读 Game State + Registry，不直接调用系统   │
└─────────────────────────────────────────────┘
```

---

## Phase A-G 详情

### Phase A — 基础设施 ✅

- [x] 创建 `tools/bk_editor/` 包结构
- [x] 创建 `game/core/data/` 目录及子目录
- [x] 编写 JSON Schema (`_schemas/*.json`)
- [x] 编写 `DataLoader` (`game/core/systems/data_loader.rpy`)
- [x] 所有新增屏幕文本已中文化

### Phase B/C — 编辑器 GUI ✅

- [x] **剧情事件编辑器** — StoryEvent 完整 CRUD，`modes` 字段支持 story/sandbox/scenario
- [x] **出身编辑器** — Origin/OriginTalent 完整 CRUD
- [x] **女孩系统编辑器** — Trait/Perk 完整 CRUD + Effect 可视化编辑

### Phase D — 硬编码导出 JSON ✅

- [x] 导出 **131 个 Trait** 到 `data/traits/traits.json`
- [x] 导出 **53 个 Perk** 到 `data/perks/perks.json`
- [x] 游戏内 Debug 菜单支持 Trait/Perk/StoryEvent 导出

### Phase E — 女孩包制作工具 ✅

- [x] `_BK.ini` 文件读写 (自定义 `ListAwareConfigParser`)
- [x] 8 个标签页完整编辑（基础信息、技能、特质、个性、喜好、性偏好、背景故事）

### Phase F — 剧本编辑器完善 ✅

- [x] Scenario 完整 CRUD
- [x] 起始条件 / 胜利条件动态编辑
- [x] JSON Schema 验证集成

### Phase G — 代码去硬编码 ✅

- [x] Origin / Trait / Perk / Powers / Spells / Classes / Challenges / Contracts / Resources / Customers / Cleanliness / Treasure / Meta / NGP / Stats / Ranks / Personalities / Achievements / Goals / Fixations / Interactions / Tags / Shop / Items / Jobs / Brothel params / Tax / Minion / Installations / Rooms / Difficulty / Help texts / Encounters / Security / Training / Quest / Inventory / Sex training / Background pools / Audio / Contract params / Resource params / Archetypes / Game constants / Job params / XP/Rank params / Economy modifiers / Customer params / Unlock params / Location tooltips / Personality gift params / Chapter titles

### Phase H — i18n 全面适配 ✅

- [x] 105 个 JSON 数据文件全部完成 `_i18n` 适配
- [x] 1,531 条可翻译字符串被 `generate translations` 自动收集
- [x] `json_i18n.rpy` 白名单已移除，采用纯 `_i18n` 后缀扫描

### Phase I — 系统解耦 ✅

- [x] 创建 `UnlockRegistry` (`game/core/systems/registry/unlock_registry.rpy`)
- [x] `Farm.active` 改为 property，自动同步到 `UnlockRegistry`
- [x] `farm.action` / `farmland.action` 混用问题修复，迁移为 `is_unlocked("farmland")`
- [x] `activate_world_map()` 集成 `UnlockRegistry`，按 `loc_id` expose location

---

## 系统解耦记录

| 问题 | 影响 | 修复方案 | 状态 |
|------|------|----------|------|
| `farmland` 未定义 / `farm.action` 混用 | Farm 系统与 Location 系统耦合，运行时 NameError/AttributeError | 创建 `UnlockRegistry`，`Farm.active` 改为 property，`farm.action` 迁移为 `is_unlocked("farmland")` | ✅ 已修复 |
| `activate_world_map()` 全局变量泄露 | Location 对象直接注入 store，导致命名冲突 | 按 `loc_id` 额外 expose（如 `farmland`），解锁状态同步到 `UnlockRegistry` | ✅ 已修复 |

---

## 技术债务

| 问题 | 影响 | 计划修复 |
|------|------|---------|
| 大量 Trait/Perk 仍硬编码在 .rpy | 编辑器无法编辑已有内容 | ✅ Phase 5 已完成 JSON 导出；`.rpy` 注册保留 fallback |
| `story_mode` 全局变量散布 | 代码维护困难 | ✅ 已完成：Game 类新增 `is_story_mode()`，17 处运行时引用全部替换 |
| 顾客 `affixes` 未完全集成到评分 | 新系统未实际影响玩法 | Phase 4 后续 |
| `girlclass.rpy` 覆盖内置 `dict` | 导致 `isinstance(x, dict)` 全局失效 | ✅ 已修复（变量重命名为 `_wd_dict`） |
| `classes.rpy` / `girlclass.rpy` / `functions.rpy` 过大 | 单文件维护困难 | ✅ 已拆分：classes→8文件、girlclass→2文件、functions→6文件 |
| `gameplay/` 目录不符合规范 | 内容/系统/初始化混杂 | ✅ 已拆分至 `content/`/`init/`/`systems/` |
| `farmland` 未定义 / `farm.action` 混用 | Farm 系统与 Location 系统耦合 | ✅ 已修复：UnlockRegistry + property |

---

## 测试记录

### 2026-06-08 UnlockRegistry + Farm/Location 解耦验证

| 测试项 | 状态 | 备注 |
|--------|------|------|
| `unlock_registry.rpy` 加载 | ✅ 通过 | `init -9` 正常初始化，无 traceback |
| `Farm.active` property | ✅ 通过 | getter/setter 自动同步 `unlock_registry`，旧存档兼容 |
| `farm.action` 迁移 | ✅ 通过 | 3 处引用全部替换为 `unlock("farmland")` / `is_unlocked("farmland")` |
| `activate_world_map()` 集成 | ✅ 通过 | `action=True` 的 location 自动注册到 `unlock_registry` |
| lint 检查 | ✅ 通过 | 零新增错误，全部 105 JSON 文件扫描正常 |

---

## 附录：目录结构

```
game/core/
├── config/        — gui.rpy, options.rpy, screens.rpy, translations.rpy
├── content/       — dialogue.rpy, interactions.rpy, intro.rpy, declarations.rpy,
│                    city_events/, day_events/, events/, main_story/, scenarios/,
│                    side_stories/, story_events/
├── data/          — JSON data dirs + .rpy data definitions (items.rpy, jobs.rpy,
│                    perks.rpy, powers.rpy, settings.rpy)
├── framework/     — character.rpy, core_entities.rpy, girlclass.rpy, utils.rpy, world.rpy, pythonlib/
├── init/          — start.rpy, settings.rpy, variables.rpy
├── systems/       — achievements.rpy, auction/, courtyard/, customer/,
│                    data_loader.rpy, endday.rpy, events/, events_dispatcher.rpy,
│                    farm.rpy, gamemodes/, help.rpy, items.rpy, minigame.rpy,
│                    mods/, perks.rpy, postings.rpy, powers.rpy, registry/,
│                    security.rpy, settlement/, spells.rpy, traits.rpy
├── templates/     — event_template.rpy, girl_template/, mod_template/,
│                    scenario_template.rpy
└── ui/            — content_menu.rpy, main.rpy, notify.rpy, screen_home.rpy,
                     screens.rpy
```

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [`DATA_MIGRATION.md`](./DATA_MIGRATION.md) | 硬编码数据 → JSON 迁移完整清单（含源文件、目标路径、状态、i18n 状态） |
| [`I18N_ROADMAP.md`](./I18N_ROADMAP.md) | 当前 i18n 状态、路线图与最佳实践 |
| [`architecture/README.md`](./architecture/README.md) | 子系统架构文档索引 |
| [`CUSTOM_DIRECTORY_GUIDE.md`](./CUSTOM_DIRECTORY_GUIDE.md) | 自定义目录使用指南 |
| [`PROJECT_GUIDE.md`](./PROJECT_GUIDE.md) | 项目目录规范与开发约定（当前唯一活跃指南） |
