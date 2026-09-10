# Trait / Perk 系统架构

> **文件**: `game/core/framework/character.rpy` (Trait, Perk), `game/core/systems/registry/trait_registry.rpy`, `game/core/systems/registry/perk_registry.rpy`  
> **数据**: `game/core/data/traits/traits.json`, `game/core/data/perks/perks.json`  
> **编辑支持**: ✅ 女孩包编辑器 (`girl_pack_editor`)

---

## 1. 系统职责

### Trait（特质）
定义女孩或顾客的被动属性，影响行为、对话和互动：
- **效果系统**: `Effect` 对象封装 `type/target/value/scope/chance/scales_with/dice`，支持运行时评估。
- **标签系统**: `tags` 字段用于图片标签映射（如 `blonde` 对应金发图片）。
- **互斥组**: `opposite` 字段防止冲突特质共存。

### Perk（天赋/技能）
定义女孩可学习的主动或被动能力：
- **层级**: `level=1/2/3` 支持多段升级。
- **原型**: `archetype` 字段按职业/路线分类（如 `warrior`, `mage`）。
- **解锁条件**: `requires` 字段声明前置 Perk。

核心类：
- `Trait` / `Perk` — 数据模型，支持 `from_dict()` / `to_dict()`。
- `TraitRegistry` / `PerkRegistry` — Registry 系统，替换原 `trait_dict` / `perk_dict`。
- 编辑器内嵌 Effect 编辑组件，可视化编辑 Effect 字段。

---

## 2. 解耦方式

- **与硬编码解耦**: Trait 和 Perk 从 `.rpy` 导出到 JSON，`DataLoader` 在 `init` 阶段加载到注册表。
- **与 Girl 类解耦**: `Girl` 通过 `trait_list` / `perk_list` 持有 ID 引用，实际效果评估时向注册表查询 `Trait/Perk` 定义，不硬编码任何特质逻辑。
- **与注册表解耦**: `TraitRegistry` / `PerkRegistry` 继承通用 `Registry` 基类，统一生命周期管理。

---

## 3. 系统间联系

```
traits.json / perks.json
    └─→ DataLoader.load_all() / load_traits() / load_perks()
           └─→ TraitRegistry / PerkRegistry
                  ├─→ Girl.__init__()    (初始化默认特质)
                  ├─→ Girl.get_effect()  (效果聚合)
                  ├─→ Girl.has_trait()   (条件判断)
                  └─→ girl_pack_editor   (可视化 CRUD)
```

- `Girl.get_effect(type, target)` 遍历 `trait_list` + `perk_list` + `equipment_list`，向对应注册表查询效果并聚合。
- `Trait` 的 `tags` 与 `TagRegistry` 联动，影响女孩图片标签解析。

---

## 4. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 女孩包编辑器 (`girl_pack_editor`) | ✅ 完整 | Trait/Perk 的完整 CRUD；Effect 字段可视化编辑 |
| 开发控制台 (`dev_console`) | ✅ 数据同步 | JSON Schema 验证、批量格式化 |

---

## 5. 向后兼容

- 旧存档中的 `trait_list` / `perk_list` 存储的是 Trait/Perk ID，注册表查询失败时安全返回空效果。
- `_RegistryProxy` 让旧代码的 `trait_dict[id]` / `id in trait_dict` 语法继续工作。
- `Trait.from_dict()` / `Perk.from_dict()` 兼容旧字段缺失，使用合理默认值。
