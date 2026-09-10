# Trait / Perk 系统架构

> 最后更新: 2026-09-11（与代码核对）
> **核心文件**: `game/core/framework/character.rpy`（`Trait` 类 :207、`Perk` 类 :303）
> **数据**: `game/core/data/traits/traits.json`（**131 个**，实测）、`game/core/data/perks/perks.json`（**53 个**，实测）
> **注册表**: `game/core/systems/registry/trait_registry.rpy`、`perk_registry.rpy`（均 init -5）

---

## 1. 系统职责

### Trait（特质）

定义女孩/顾客的被动属性，影响行为、对话与互动：

- **效果挂载**: Trait 携带 `Effect` 列表（`framework/effects.rpy`），类型含 `change`（数值增减）/`boost`（倍率）/`special`，由 `EffectBearer`（Girl 的基类之一）统一评估。
- **标签**: `tags` 字段用于图片标签映射（如发色 → 对应图片）。
- **互斥**: `opposite` 字段声明互斥特质，生成时防止冲突共存。
- **分类**: positive / negative / background 等，注册时写入 category 以支持分组检索。

### Perk（天赋）

MC 与女孩的主动/被动强化：

- **成本与解锁**: 通常消耗技能点/天赋点，部分有前置条件。
- **效果系统**: 与 Trait 共用 `Effect` 机制，作用于 MC 全局或单个女孩。

## 2. 类结构（character.rpy）

| 类 | 行号 | 关键能力 |
|----|-----:|---------|
| `Trait` | :207 | `from_dict()` JSON 构造、效果列表、标签、互斥组 |
| `Perk` | :303 | `from_dict()` JSON 构造、成本/解锁、效果列表 |

两者均由 `DataLoader.load_traits()` / `load_perks()` 从 JSON 批量构造，注册进 `TraitRegistry` / `PerkRegistry`（覆盖语义：后注册者胜出，Mod 可覆盖官方定义）。

## 3. 运行时消费方

- **Girl**: 组件 `GirlTraits`（`girl/girl_traits.rpy`）管理女孩的特质增删；`get_effect()` 沿 Girl → 装备 → 特质链路聚合效果值。`generate_traits` 已在 Phase 2 迁入组件。
- **MC**: 天赋在 `screen_progress.rpy` 的 `perks` 界面选择，效果经同一 Effect 系统评估。
- **数据生成**: 女孩生成时按 `traits.json` 的正/负特质池随机抽取（负特质单抽一个）。

## 4. 系统间联系

```
game/core/data/traits/traits.json (131)
    └─→ DataLoader.load_traits() → TraitRegistry (init -5 注册表)
           ├─→ GirlTraits 组件 (生成/增删/查询)
           ├─→ EffectBearer.get_effect() 效果聚合
           └─→ ModAPI.register_trait() (Mod 覆盖/新增)

game/core/data/perks/perks.json (53)
    └─→ DataLoader.load_perks() → PerkRegistry
           ├─→ screen_progress (perks 界面)
           └─→ ModAPI.register_perk()
```

## 5. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 女孩包编辑器 `trait_creator.py` | ✅ | 读写 traits.json / perks.json，字段校验（validators.py） |
| 开发控制台 | ✅ 查看 | Trait/Perk 数据一致性经 data_sync 校验 |

修改 JSON 后需重启游戏生效（注册表 init 期重建，见 [registry.md](registry.md)）。

---

## 相关文档

- [registry.md](registry.md) — TraitRegistry / PerkRegistry 的基类机制
- [data_loader.md](data_loader.md) — JSON 加载与 fallback
- [girl_components.md](girl_components.md) — GirlTraits 组件
- [mod_system.md](mod_system.md) — Mod 注册 Trait/Perk 的 API
