# Customer / CustomerAffix 系统架构

> **文件**: `game/core/systems/customer/customer_affixes.rpy`, `game/core/framework/core_entities.rpy` (Customer)  
> **数据**: `game/core/data/customers/customer_affixes.json`  
> **编辑支持**: ✅ 数据同步（JSON 直接编辑 / 开发控制台查看）

---

## 1. 系统职责

CustomerAffix 为每位顾客附加三维词缀，使其行为、预算和评分反馈更具差异性：

### 1.1 三维词缀

| 维度 | 类 | 影响范围 |
|------|-----|---------|
| **颜色等级** (Color Tier) | `CustomerColorTier` | 预算倍率 (`budget_multiplier`) |
| **性格前缀** (Personality) | `CustomerPersonality` | 难度、满意度、预算、防御、疯狂率、颜色偏移 |
| **心情状态** (Mood) | `CustomerMood` | 满意度、小费概率、小费倍率、耐心 |

### 1.2 偏好矩阵

`CustomerPreferenceMatrix` 管理 8 槽位偏好：
- **2 Best** (+2 满意度)
- **2 Secondary** (+1 满意度)
- **2 Disliked** (-1 满意度)
- **2 Hated** (-3 满意度)
- **Neutral** (0)

### 1.3 评分集成点 (BK Evolution)

| 方法 | 文件 | 集成内容 |
|------|------|---------|
| `Customer.set_budgets()` | `core_entities.rpy` | `mod *= affixes.get_budget_multiplier()` |
| `Customer.get_entertainment_bonus()` | `core_entities.rpy` | `r += preferences.get_score_modifier(got_entertainment)` |
| `Customer.get_sex_act_bonus()` | `core_entities.rpy` | `r += preferences.get_score_modifier(got_sex_act)` |
| `Customer.get_reputation_change()` | `core_entities.rpy` | `base_rating += preferences + mood.satisfaction_mod + personality.satisfaction_mod` |
| `Girl.get_tip()` | `girlclass.rpy` | `tip_multiplier *= avg(mood.tip_multiplier) * (1 + avg(mood.tip_chance))` |

---

## 2. 解耦方式

- **与 `Customer` 类解耦**: `CustomerAffixes` 是独立对象，通过 `apply_to_customer()` 将修正应用到 `Customer` 实例属性（`diff`, `satisfaction`, `defense`），避免侵入 `Customer` 的构造逻辑。
- **与评分流程解耦**: 偏好矩阵不在 `Customer.__init__` 中写死，而是在评分方法（`get_entertainment_bonus`, `get_sex_act_bonus`, `get_reputation_change`）中按需查询。
- **与女孩类解耦**: 小费 mood 修正通过 `customers` 列表传入 `Girl.get_tip()`，由 `Girl` 方法遍历顾客并聚合平均值，不破坏原有接口签名。

---

## 3. 系统间联系

```
customer_affixes.json
    └─→ customer_affixes.rpy (init -1 加载 tiers/personalities/moods)
           ├─→ generate_customer_affixes(pop_rank)
           │       └─→ Customer.randomize()
           │              ├─→ affixes.apply_to_customer(self)   (diff/defense/satisfaction)
           │              ├─→ set_budgets()                     (budget multiplier)
           │              └─→ preferences.generate()            (8-slot matrix)
           └─→ 评分流程
                  ├─→ get_entertainment_bonus()  ← preference matrix
                  ├─→ get_sex_act_bonus()        ← preference matrix
                  ├─→ get_reputation_change()    ← preference + mood + personality
                  └─→ Girl.get_tip()             ← mood avg
```

- `Customer.randomize()` 在每日生成顾客时调用 `generate_customer_affixes()`。
- `HookManager.on_customer_generate` 允许 Mod 在 affix 生成后拦截并修改。

---

## 4. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 开发控制台 (`dev_console`) | ✅ 数据同步 | 可查看/编辑 `customer_affixes.json` 等纯 JSON 数据 |
| 女孩包编辑器 / 剧本编辑器 | ❌ 无 | 不涉及 |

---

## 5. 向后兼容

- `Customer.__init__` 中 `try/except` 包裹 affix 生成，失败时 `self.affixes = None`。
- 所有评分方法检查 `if self.affixes:` 后再查询偏好矩阵，确保无 affix 的顾客行为与旧代码完全一致。
- `Girl.get_tip()` 中 `hasattr(cust, 'affixes')` 防御旧存档/测试场景中顾客对象缺少该属性。
