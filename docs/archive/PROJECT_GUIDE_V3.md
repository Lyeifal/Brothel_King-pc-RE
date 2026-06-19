# Brothel King — Phase 6 重构进度文档 (PROJECT_GUIDE_V3)

> 本文档记录 **Phase 6 (System Decoupling & Mod Support)** 的全部设计决策、已实现功能、待办事项和 Mod 开发指南。
> 
> **版本**: BK 0.3 v260527 · Ren'Py 8.2.0 · Python 3.9  
> **分支**: `refactor-phase6`  
> **最后更新**: 2026-06-06

---

## 目录

1. [Phase 6 总览](#1-phase-6-总览)
2. [已完成的子阶段](#2-已完成的子阶段)
   - 6.1 统一注册中心
   - 6.2 Mod 系统重构
   - 6.3 事件系统重构
   - 6.4 结算系统重构
   - 6.5 对话系统增强
   - 6.6 Girl Pack 系统增强
   - 6.8 数值系统数据化
   - 6.9 NGP+ 系统增强
3. [待完成的子阶段](#3-待完成的子阶段)
4. [架构说明](#4-架构说明)
5. [Mod API 参考](#5-mod-api-参考)
6. [文件清单](#6-文件清单)
7. [Lint 基线与已知问题](#7-lint-基线与已知问题)
8. [向后兼容说明](#8-向后兼容说明)

---

## 1. Phase 6 总览

### 目标
将原本硬编码、耦合紧密的核心系统解耦为可扩展、可拦截的模块化架构，为 Mod 作者和 Girl Pack 作者提供安全、稳定的扩展接口。

### 设计原则
1. **最小侵入** — 不破坏现有存档、不修改现有游戏逻辑。
2. **向后兼容** — 所有旧代码继续工作，新系统通过代理/钩子叠加。
3. **注册中心** — 用 Registry 替代分散的全局字典，统一生命周期管理。
4. **钩子驱动** — Mod 通过 HookManager 拦截核心事件，而非直接覆盖源码。
5. **数据化** — 核心类支持 `from_dict()` / `to_dict()`，为 future JSON/YAML 数据加载做准备。

---

## 2. 已完成的子阶段

### 6.1 统一注册中心 (Registry System)

**状态**: ✅ 完成  
**核心文件**: `game/core/systems/registry/`

| 注册表 | 替换的原全局变量 | 功能 |
|--------|----------------|------|
| `Registry` (基类) | — | 统一 `register/get/unregister/has/clear/get_by_category` |
| `TagRegistry` | `tag_dict`, `tag_list_dict` | 运行时扩展图片标签映射 |
| `TraitRegistry` | `trait_dict` | 特质定义注册 |
| `PerkRegistry` | `perk_dict` | 技能定义注册 |
| `DialogueRegistry` | `dialogue_dict` | 对话主题管理 |
| `EventRegistry` | `event_dict` | 事件定义 + 运行时队列 (`city_events`/`daily_events`) |
| `NGPRegistry` | `NGP_settings_dict` | NG+ 设置注册 |

**关键设计**:
- `_RegistryProxy` 让旧代码的 `dict[key]` / `key in dict` / `dict.get()` 语法继续工作。
- `_TagListDictProxy` 解决了 `init -10` 阶段 `Room` 对象提前访问 `tag_list_dict` 导致的 `KeyError`。
- 所有注册表均为单例，支持 `category` 分组（便于 UI 按类别展示）。

**Init 优先级链**:
```
init -10: Registry 基类
init -6:  Trait/Perk/Tag/Dialogue/Event/NGP 注册表
init -9:  settings.rpy 将数据批量注册到 TagRegistry
init -4:  ModAPI, EventEngine
```

---

### 6.2 Mod 系统重构 (HookManager + ModAPI)

**状态**: ✅ 完成  
**核心文件**: `game/core/systems/mods/`

#### HookManager
`game/core/systems/mods/mod_hooks.rpy`

提供 8 个官方钩子点：

| 钩子名 | 触发时机 | 回调签名 |
|--------|---------|---------|
| `on_girl_generate` | 女孩生成完毕 | `callback(girl)` |
| `on_girl_acquire` | 玩家获得女孩 | `callback(girl)` |
| `on_day_start` | 新的一天开始 | `callback(context)` |
| `on_day_end` | 玩家点击 "End Day" | `callback(context)` |
| `on_settlement_girls_ready` | 结算中女孩分类完成 | `callback(context)` |
| `on_settlement_end` | 结算全部结束 | `callback(context)` |
| `on_event_trigger` | 事件被触发 | `callback(event_id, context)` |
| `on_customer_generate` | 顾客生成时 | `callback(customers)` |
| `on_girl_perform` | 女孩表演/接客时 | `callback(girl, act, customers)` |
| `on_dialogue_select` | 对话被选中时 | `callback(topic, girl, dialogue)` |
| `pre_settlement_<phase>` | 某结算 phase 前 | `callback(context)` |
| `post_settlement_<phase>` | 某结算 phase 后 | `callback(context)` |

所有钩子内部已包 `try/except`，单个 Mod 的异常不会崩溃游戏。

#### ModAPI
`game/core/systems/mods/mod_api.rpy`

安全封装了所有注册表和钩子系统：

```python
mod_api.register_trait(trait_id, trait)
mod_api.register_perk(perk_id, perk)
mod_api.register_tag(tag_id, tag_value)
mod_api.register_dialogue(topic, key, dialogue_obj)
mod_api.register_event(event_id, event)
mod_api.register_ngp_setting(setting_id, setting)
mod_api.hook(event_name, callback, priority=0)
```

#### Mod 生命周期集成
- `Mod` 类新增 `api_version` 字段。
- `Game.activate_mod()` 自动调用 `hook_manager.invoke("on_mod_activated", mod)`。
- Mod 作者可在 `mod_template.rpy` 中参考完整示例。

---

### 6.3 事件系统重构 (EventEngine)

**状态**: ✅ 完成  
**核心文件**: `game/core/systems/events/event_engine.rpy`

`EventEngine` 是事件管理的高级接口：

```python
event_engine.register_story_event(event_id, story_event, auto_add=False)
event_engine.register_event_from_dict(event_id, data_dict)
event_engine.add_event_to_queue(event_id, event_type="city")
event_engine.remove_event_from_queue(event_id, event_type="city")
event_engine.scan_custom_events()        # 扫描 game/core/content/events/
event_engine.load_event_pack(filepath)   # 运行时加载 .rpy
event_engine.on_event_trigger(event_id, context)
```

**自动加载器**: `game/core/content/events/` 目录已创建。Mod 作者可将自定义事件 `.rpy` 文件放入该目录，通过 `event_engine.load_event_pack()` 在运行时加载。

**模板**: `game/core/templates/event_template.rpy` 提供了 4 种注册事件的示例。

**向后兼容**: 继续使用全局 `city_events` / `daily_events` 列表；`story_add_event()` / `add_event()` 保持原语义。

---

### 6.4 结算系统重构 (SettlementPipeline)

**状态**: ✅ 框架 + Phase Handlers 完成  
**核心文件**: `game/core/systems/settlement/`

#### 核心类
- `SettlementContext` — 可变上下文，携带所有结算阶段共享的状态（女孩列表、顾客、收入、日志等）。
- `SettlementPipeline` — 管理有序 phase 列表，每个 phase 前后自动触发 hook。
- `run_phase_by_name(name, context)` — 支持按名称运行单个 phase。

#### 已注册的默认 Phase

| Phase | 顺序 | 功能 |
|-------|------|------|
| `categorize_girls` | 10 | 将女孩分类为 working/striking/resting/sick/away/job/whore |
| `generate_customers` | 20 | 生成顾客，应用清洁度惩罚 |
| `calculate_income` | 80 | 计算收入、成本、净收益 |
| `levelup` | 90 | 处理女孩升级、技能提升、catch-up |
| `end_night` | 100 | 重置交互、更新情绪、love/fear 衰减 |
| `morning_prep` | 110 | 逃跑检查、疲劳检查、农场退出、刷新肖像 |

**与 endday.rpy 的关系**: `endday.rpy` 中已插入 4 个 hook 点（`on_day_end`, `on_settlement_girls_ready`, `on_settlement_end`, `on_day_start`）。由于 endday.rpy 混合了大量 Ren'Py UI 语句，完整替换为 Pipeline 驱动风险较高；当前策略是保留原有流程，Phase Handlers 供 Mod 作者通过 hook 拦截或未来逐步迁移。

---

### 6.5 对话系统增强

**状态**: ✅ 完成  
**核心文件**: `game/core/systems/registry/dialogue_registry.rpy`, `game/core/framework/functions.rpy`

- `DialogueRegistry` 替换了全局 `dialogue_dict`，支持 `add()` / `get()` / `merge()`。
- `add_dialogue()` 现在委托给 `dialogue_registry.add()`。
- `_BK.ini` 新增 `[custom dialogue]` 段，允许 Girl Pack 作者直接为特定 topic 定义对话行：
  ```ini
  [custom dialogue]
  slave_first_visit = ["Welcome, Master.", "I hope I can be of service."]
  rest = ["*yawns* I'm so tired..."]
  ```
- `register_custom_dialogue_for_pack()` 在女孩加载时自动注册到全局对话系统。

---

### 6.6 Girl Pack 系统增强

**状态**: ✅ 完成  
**核心文件**: `game/core/framework/functions.rpy`, `game/core/framework/girlclass.rpy`

`_BK.ini` 新增 `[custom tags]` 段：
```ini
[custom tags]
custom_pose = ["posing", "model"]
custom_outfit = ["dress", "gown"]
```

- `read_init_file()` 支持动态段解析：`parser.options(section)` 遍历所有键。
- `register_custom_tags_for_pack()` 将自定义标签注册到 `tag_registry`，并重新为该 pack 的所有图片调用 `make_tags_from_filename()`。
- `Girl.custom_tags` / `Girl.custom_dialogue` 在 `__init__()` 和 `load_ini()` 中初始化。
- `_BK.ini` 模板已更新示例。

---

### 6.8 数值与养成系统数据化

**状态**: ✅ 基础完成  
**核心文件**: `game/core/framework/classes.rpy`

为以下类添加了 `from_dict()` / `to_dict()`：

| 类 | `from_dict` 支持 | `to_dict` 支持 |
|----|-----------------|----------------|
| `Effect` | ✅ | ✅ |
| `Trait` | ✅ | ✅ |
| `Perk` | ✅ | ✅ |

为未来 JSON/YAML 数据驱动加载打下基础。

---

### 6.9 多周目（NG+）系统增强

**状态**: ✅ 完成  
**核心文件**: `game/core/systems/registry/ngp_registry.rpy`

- `NGPRegistry` 管理所有 `NGPSetting` 实例。
- `start.rpy` 中创建 `NGP_settings` 列表后，自动按 category 注册到 `ngp_registry`。
- `NGP_settings_dict` 被替换为 `_RegistryProxy(ngp_registry)`，旧代码无需修改。
- 支持按 category 查询：`ngp_registry.get_by_category("resources")`。

---

## 3. 待完成的子阶段

### 6.7 多语言补完与 i18n 基础设施

**优先级**: 低  
**状态**: ⏸️ 待做

已知硬编码英文位置：
- `game/core/init/start.rpy` — Debug 模式菜单选项（仅开发者可见）
- `game/core/ui/screens.rpy` — 部分 packstate 字符串
- `game/core/ui/content_menu.rpy` — 设置描述

这些字符串在 `strings.rpy` 中部分已有翻译，部分因是菜单文本需要手动加 `__()`。

**计划**: 逐个文件排查，用 `__()` / `_()` 包裹所有用户可见的硬编码英文。

---

## 4. 架构说明

### 4.1 注册中心架构

```
┌─────────────────────────────────────────┐
│              Registry (基类)              │
│  _registry: {id -> obj}                  │
│  _categories: {id -> category}           │
│  _by_category: {cat -> {id -> obj}}      │
└─────────────────────────────────────────┘
            ▲           ▲           ▲
    ┌───────┘    ┌──────┘    ┌──────┘
TagRegistry  TraitRegistry  PerkRegistry
DialogueRegistry  EventRegistry  NGPRegistry
```

### 4.2 Mod 系统架构

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Mod 作者    │────▶│     ModAPI       │────▶│  Registries │
│              │     │ (安全封装)        │     │             │
└──────────────┘     └──────────────────┘     └─────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   HookManager    │
                    │  pre/post 钩子   │
                    └──────────────────┘
```

### 4.3 结算 Pipeline 架构

```
label end_day
    │
    ▼
SettlementContext() 创建上下文
    │
    ▼
hook_manager.invoke("on_day_end", ctx)
    │
    ▼
┌─────────────────────────────────────────┐
│  [原有逻辑] 或 [settlement_pipeline.run] │
│  1. categorize_girls                    │
│  2. generate_customers                  │
│  ...                                    │
│  6. morning_prep                        │
└─────────────────────────────────────────┘
    │
    ▼
hook_manager.invoke("on_day_start", ctx)
```

---

## 5. Mod API 参考

### 5.1 快速开始

在 Mod 的 `.rpy` 文件中：

```renpy
init 1 python:
    # 注册一个新特质
    my_trait = Trait("My Trait", "be", effects=[Effect("change", "beauty", 5)])
    mod_api.register_trait("my_trait", my_trait)

    # 注册一个事件
    my_event = StoryEvent("my_custom_event", chapter=1, location="docks")
    mod_api.register_event("my_event", my_event)
    event_engine.add_event_to_queue("my_event", event_type="city")

    # 注册一个钩子
    def on_day_start_hook(context):
        renpy.notify("A new day begins!")
    mod_api.hook("on_day_start", on_day_start_hook)
```

### 5.2 API 版本

- `mod_api.version = 1`
- Mod 的 `api_version` 字段用于未来兼容性检查。

---

## 6. 文件清单

### 6.1 新增文件 (Phase 6)

| 文件路径 | 说明 |
|----------|------|
| `game/core/systems/registry/registry.rpy` | Registry 基类 + `_RegistryProxy` |
| `game/core/systems/registry/tag_registry.rpy` | TagRegistry + `_TagListDictProxy` |
| `game/core/systems/registry/trait_registry.rpy` | TraitRegistry |
| `game/core/systems/registry/perk_registry.rpy` | PerkRegistry |
| `game/core/systems/registry/dialogue_registry.rpy` | DialogueRegistry |
| `game/core/systems/registry/event_registry.rpy` | EventRegistry |
| `game/core/systems/registry/ngp_registry.rpy` | NGPRegistry |
| `game/core/systems/mods/mod_hooks.rpy` | HookManager |
| `game/core/systems/mods/mod_api.rpy` | ModAPI |
| `game/core/systems/settlement/settlement_pipeline.rpy` | SettlementPipeline + SettlementContext |
| `game/core/systems/settlement/phases.rpy` | 6 个默认 phase handler |
| `game/core/systems/events/__init__.rpy` | Event Engine 包 init |
| `game/core/systems/events/event_engine.rpy` | EventEngine 主类 |
| `game/core/content/events/__init__.rpy` | 自定义事件目录占位 |
| `game/core/templates/mod_template/mod_template.rpy` | Mod 开发模板 |
| `game/core/templates/event_template.rpy` | 自定义事件模板 |

### 6.2 修改文件 (Phase 6)

| 文件路径 | 修改内容 |
|----------|----------|
| `game/core/init/settings.rpy` | `tag_dict` 迁移到 TagRegistry |
| `game/core/framework/classes.rpy` | Effect/Trait/Perk 的 `from_dict/to_dict`；Mod 类 `api_version`；`activate_mod` 钩子 |
| `game/core/init/start.rpy` | `event_dict` / `NGP_settings` 注册到对应 Registry |
| `game/core/systems/endday.rpy` | 插入 SettlementContext 和 4 个 hook 点 |
| `game/core/framework/functions.rpy` | `_BK.ini` 动态段解析；`register_custom_tags_for_pack`；`register_custom_dialogue_for_pack` |
| `game/core/framework/girlclass.rpy` | `custom_tags` / `custom_dialogue` 初始化与加载 |
| `game/core/templates/girl_template/_BK.ini` | 新增 `[custom tags]` 和 `[custom dialogue]` 示例 |

---

## 7. Lint 基线与已知问题

### 当前 Lint 状态
运行 `renpy . lint` 的输出仅包含**预存在**的警告：

```
game/core/content/city_events/city_events.rpy:4629+  Could not evaluate 'npc'
game/core/content/city_events/city_events.rpy:4744+  Could not evaluate 'girl.char'
```

这些警告在原始 `BKcity_events.rpy` 中已存在，由动态角色（`npc`, `girl.char`）的 say 语句导致。**不是 Phase 6 引入的**。

### 无新增 Parser 错误
Phase 6 所有新增/修改的 `.rpy` 文件均通过 Ren'Py lint 检查。

---

## 8. 向后兼容说明

### 存档兼容性
- 所有 Registry 在 `init` 阶段重建，不持久化到存档。
- `persistent.NGPsettings` 继续由 `NGPSetting` 类直接读写，不受 Registry 迁移影响。

### 旧 Mod 兼容性
- Goldo's cool mod 等旧 Mod 使用 label-based 系统，完全不受影响。
- 旧 Mod 如果直接读取 `tag_dict` / `trait_dict` / `event_dict`，通过 `_RegistryProxy` 仍可正常访问。

### Girl Pack 兼容性
- 不含 `[custom tags]` / `[custom dialogue]` 的旧 `_BK.ini` 文件继续正常工作。
- `read_init_file()` 的动态段解析使用 `try/except`，不会因缺少段而报错。

---

## 附录：Git 提交建议

建议在完成 Phase 6 全部工作后，按以下方式提交：

```bash
# 提交 Registry 系统
git add game/core/systems/registry/
git commit -m "Phase 6.1: Unified Registry System (Tag, Trait, Perk, Dialogue, Event, NGP)"

# 提交 Mod 系统
git add game/core/systems/mods/ game/core/templates/mod_template/
git commit -m "Phase 6.2: Mod HookManager + ModAPI + template"

# 提交事件引擎
git add game/core/systems/events/ game/core/content/events/ game/core/templates/event_template.rpy
git commit -m "Phase 6.3: EventEngine with custom event auto-loader"

# 提交结算 Pipeline
git add game/core/systems/settlement/ game/core/systems/endday.rpy
git commit -m "Phase 6.4: SettlementPipeline + phase handlers"

# 提交 Girl Pack 扩展
git add game/core/framework/functions.rpy game/core/framework/girlclass.rpy game/core/templates/girl_template/_BK.ini
git commit -m "Phase 6.5/6.6: Girl Pack custom tags & dialogue in _BK.ini"

# 提交数据化基础
git add game/core/framework/classes.rpy
git commit -m "Phase 6.8: Data-driven from_dict/to_dict for Effect, Trait, Perk"

# 提交 NGP 注册
git add game/core/systems/registry/ngp_registry.rpy game/core/init/start.rpy
git commit -m "Phase 6.9: NGPRegistry migration"
```

---

> **文档结束** — 如有新增子阶段或架构调整，请同步更新本文件。
