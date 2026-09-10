# Registry 系统架构

> **文件**: `game/core/systems/registry/*.rpy`  
> **基类**: `game/core/systems/registry/registry.rpy`  
> **Phase**: Phase 6 (System Decoupling & Mod Support)

---

## 1. 系统职责

Registry 是 Phase 6 引入的统一注册中心，替代分散的全局字典（`trait_dict`, `perk_dict`, `event_dict`, `dialogue_dict` 等），提供：

- **统一生命周期**: `register` / `unregister` / `clear` / `has` / `get` / `get_by_category`
- **分类管理**: `category` 参数支持按组检索（如 Trait 按 `positive`/`negative`/`background` 分类）。
- **向后兼容代理**: `_RegistryProxy` 让旧代码的 `dict[key]` / `key in dict` / `dict.get()` 语法继续工作。
- **运行时扩展**: Mod 可在游戏运行时安全地向注册表添加/移除条目。

---

## 2. 已实现的注册表

| 注册表 | 文件 | 替换的原全局变量 | 用途 |
|--------|------|----------------|------|
| `Registry` | `registry.rpy` | — | 抽象基类 |
| `TagRegistry` | `tag_registry.rpy` | `tag_dict`, `tag_list_dict` | 图片标签映射 |
| `TraitRegistry` | `trait_registry.rpy` | `trait_dict` | 特质定义 |
| `PerkRegistry` | `perk_registry.rpy` | `perk_dict` | 天赋定义 |
| `DialogueRegistry` | `dialogue_registry.rpy` | `dialogue_dict` | 对话主题管理 |
| `EventRegistry` | `event_registry.rpy` | `event_dict` | 事件定义 + 运行时队列 |
| `NGPRegistry` | `ngp_registry.rpy` | `NGP_settings_dict` | NG+ 设置 |
| `MetaRegistry` | `meta_registry.rpy` | `meta_dict` | Meta-progression / 解锁 |
| `UnlockRegistry` | `unlock_registry.rpy` | `unlock_dict` | 解锁条件注册 |

---

## 3. 解耦方式

- **与全局命名空间解耦**: 旧全局字典（`trait_dict = {}`）被替换为注册表单例，避免 `init` 阶段顺序依赖导致的 `KeyError`。
- **与具体类解耦**: 基类 `Registry` 不依赖 `Trait` / `Perk` 等具体类型，通过泛型接口工作。
- **与旧代码解耦**: `_RegistryProxy` 和 `_TagListDictProxy` 在旧代码和注册表之间提供兼容层，旧语法无需修改即可工作。

---

## 4. 系统间联系

```
Registry (基类)
    ├─→ TagRegistry
    │       ├─→ GirlPack / image_tagger.py
    │       └─→ Room (init -10 阶段安全访问)
    ├─→ TraitRegistry
    │       ├─→ DataLoader.load_traits()
    │       ├─→ Girl.__init__() / get_effect()
    │       └─→ girl_pack_editor (trait_creator.py)
    ├─→ PerkRegistry
    │       ├─→ DataLoader.load_perks()
    │       ├─→ Girl.get_effect()
    │       └─→ girl_pack_editor (trait_creator.py)
    ├─→ EventRegistry
    │       ├─→ DataLoader.load_story_events()
    │       ├─→ EventEngine (运行时筛选)
    │       └─→ scenario_editor (event_editor.py)
    ├─→ DialogueRegistry
    │       ├─→ GirlPack (自定义对话)
    │       └─→ HookManager.on_dialogue_select
    ├─→ NGPRegistry
    │       └─→ dev_console (ngp_editor.py)
    ├─→ MetaRegistry
    │       └─→ dev_console (meta_editor.py)
    └─→ UnlockRegistry
            └─→ 成就/目标/解锁条件评估
```

### Init 优先级链

```
init -10: Registry 基类
init -9:  settings.rpy 批量注册到 TagRegistry
init -6:  Trait / Perk / Tag / Dialogue / Event / NGP / Meta / Unlock 注册表实例化
init -4:  ModAPI, EventEngine
init -2:  DataLoader.load_all() (加载 JSON 到注册表)
```

---

## 5. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 女孩包编辑器 | ✅ 间接→完整 | 图片标签通过 TagRegistry 解析；Trait/Perk 直接操作对应注册表 |
| 剧本编辑器 | ✅ 完整 | 直接操作 EventRegistry |
| 开发控制台 | ✅ 完整 | 直接操作 NGPRegistry、MetaRegistry、UnlockRegistry；`data_sync.py` 验证注册表数据一致性 |

---

## 6. 向后兼容

- `_RegistryProxy` 支持 `obj[key]`, `key in obj`, `obj.get(key)`, `len(obj)`, `iter(obj)` 等全部 dict 语义。
- `_TagListDictProxy` 解决了 `init -10` 阶段 `Room` 对象提前访问 `tag_list_dict` 的 `KeyError` 问题。
- 旧代码中的 `trait_dict[id]` 实际上通过代理访问 `TraitRegistry`，新旧代码混用无感知。
