# Registry 系统架构

> 最后更新: 2026-09-13（与代码核对）
> **基类**: `game/core/systems/registry/registry.rpy`（init -10）
> **Phase**: Phase 6（系统解耦与 Mod 支持）

---

## 1. 系统职责

Registry 是 Phase 6 引入的统一注册中心，替代分散的全局字典（`trait_dict`、`perk_dict`、`event_dict`、`dialogue_dict` 等），提供：

- **统一 API**: `register` / `unregister` / `get` / `get_all` / `get_by_category` / `get_categories` / `clear` / `__contains__` / `__len__`（registry.rpy:37-100）。
- **分类管理**: `category` 参数支持按组检索（如 Trait 按 positive/negative/background）。
- **覆盖语义**: 重复 register 时 developer 模式记日志并覆盖——后来的注册胜出，这正是 Mod 覆盖官方内容的机制（registry.rpy:42-44）。
- **兼容代理**: `_RegistryProxy`（registry.rpy:103-144）把 Registry 包装成 dict 外观，旧代码的 `dict[key]` / `key in dict` / `.get()` 语法无感知。
- **单例保障**: 基类 `__new__` 按子类缓存实例（registry.rpy:14-20），各注册表全游戏只有一个实例。
- **不持久化**: 所有注册表在 init 期重建，不进存档文件。

## 2. 注册表清单（10 个文件，全部核实）

| 注册表 | 文件 | init 级 | 类定义行 | 用途 |
|--------|------|--------|---------|------|
| `Registry` | `registry.rpy` | -10 | :7 | 抽象基类 + `_RegistryProxy` |
| `UnlockRegistry` | `unlock_registry.rpy` | **-9** | :13 | 解锁条件注册 |
| `TagRegistry` | `tag_registry.rpy` | -5 | :7 | 图片标签映射 |
| `TraitRegistry` | `trait_registry.rpy` | -5 | :7 | 特质定义（见 [trait_perk.md](trait_perk.md)） |
| `PerkRegistry` | `perk_registry.rpy` | -5 | :7 | 天赋定义 |
| `DialogueRegistry` | `dialogue_registry.rpy` | -5 | :7 | 对话主题管理 |
| `EventRegistry` | `event_registry.rpy` | -5 | :7 | 事件定义 + 运行时队列（见 [event.md](event.md)） |
| `NGPRegistry` | `ngp_registry.rpy` | -5 | :7 | NG+ 设置 |
| `MetaRegistry` | `meta_registry.rpy` | -5 | :7 | Meta-progression / 解锁 |
| `QualityRegistry` | `quality_registry.rpy` | -5 | :78（`QualityTier` 值类型 :13） | 物品品质档位（`register_quality`；数据见 `data/quality.rpy` fallback + "Item Quality" Mod） |

基类 init -10，UnlockRegistry -9，其余子类统一 init -5。`QualityRegistry` 是唯一自带值类型（`QualityTier`）的注册表；它也是"框架留 core、数据进 Mod"的范例（见 [../modding/MOD_API.md](../modding/MOD_API.md) §6.6）。

## 3. 解耦方式

- **与全局命名空间解耦**: 旧的全局字典被注册表单例替代，避免 init 顺序依赖导致的 `KeyError`。
- **与具体类解耦**: 基类不依赖 Trait/Perk 等具体类型，泛型接口工作。
- **与旧代码解耦**: `_RegistryProxy` 在旧代码与注册表之间提供兼容层；旧语法 `trait_dict[id]` 实际经代理走 `TraitRegistry`，新旧混用无感知。
- **与 Mod 解耦**: Mod 只调 `ModAPI.register_*()`（见 [mod_system.md](mod_system.md)），不直接接触注册表实现；覆盖语义天然支持 Mod 替换官方定义。

## 4. 系统间联系

```
Registry (基类, init -10)
    ├─→ TagRegistry ──────→ GirlPack / 图片打标 / Room
    ├─→ TraitRegistry ────→ DataLoader.load_traits() / Girl(GirlTraits 组件) / girl_pack_editor
    ├─→ PerkRegistry ─────→ DataLoader.load_perks() / Girl / girl_pack_editor
    ├─→ EventRegistry ────→ DataLoader.load_story_events() / EventEngine / scenario_editor
    ├─→ DialogueRegistry ─→ GirlPack 自定义对话 / ModAPI.register_dialogue
    ├─→ NGPRegistry ──────→ dev_console (ngp_editor.py)
    ├─→ MetaRegistry ─────→ dev_console (meta_editor.py)
    ├─→ QualityRegistry ──→ systems/items.rpy（generate_new_item / init_items）/ "Item Quality" Mod
    └─→ UnlockRegistry ───→ 成就/目标/解锁条件评估
```

调用链：`game/core/data/*.json → DataLoader.load_*() → 各 Registry → 游戏运行时系统（Girl / EventEngine / Game / ...）`。

## 5. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 女孩包编辑器 | ✅ | Trait/Perk 直接操作 TraitRegistry/PerkRegistry；标签经 TagRegistry 解析 |
| 剧本编辑器 | ✅ | 直接操作 EventRegistry |
| 开发控制台 | ✅ | NGPRegistry、MetaRegistry、UnlockRegistry；`data_sync.py` 校验一致性 |

---

## 相关文档

- [data_loader.md](data_loader.md) — 注册表的主要填充方
- [trait_perk.md](trait_perk.md) — Trait/Perk 注册表的消费方
- [event.md](event.md) — EventRegistry 与 EventEngine 的关系
- [mod_system.md](mod_system.md) — ModAPI 注册包装的目标
