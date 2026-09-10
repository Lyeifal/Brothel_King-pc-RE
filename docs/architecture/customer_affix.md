# Customer Affix 系统架构

> 最后更新: 2026-09-11（与代码核对）
> **核心文件**: `game/core/systems/customer/customer_affixes.rpy`（405 行，init -1）
> **数据**: `game/core/data/customers/customer_affixes.json`（加载点 customer_affixes.rpy:18）
> **消费方**: `framework/world.rpy:418`（`Customer.__init__` 调用 `generate_customer_affixes`）

---

## 1. 系统职责

CustomerAffix 为每位顾客附加三维词缀，使其行为、预算和评分反馈更具差异性：

### 三维词缀

| 维度 | 类 | 影响 |
|------|-----|------|
| 性格前缀 | `CustomerPersonality`（customer_affixes.rpy，前缀段） | 行为与难度修正 |
| 财富/预算 | 颜色等级（color tier） | 预算倍率 |
| 心情 | mood affix | 满意度倾向 |

### 颜色等级（8 级）

`CUSTOMER_COLOR_TIERS`（customer_affixes.rpy:26-41）：white(1.0×) → green(1.2×) → blue(1.5×) → purple(2.0×) → gold(2.8×) → orange(4.0×) → red(6.0×) → iridescent(10.0×)。JSON 定义在 `customer_affixes.json` 的 `color_tiers` 数组（id/color/budget_multiplier/name_i18n）。

### 核心类

- `CustomerAffixes`（:298）：单个顾客的完整词缀组合，方法含 `get_color()`、`get_tier_name()`、`get_budget_multiplier()`、`get_full_title()`、`apply_to_customer(customer)`、`to_dict()` / `from_dict()`（存档序列化）。
- `generate_customer_affixes(pop_rank=1, forced_tier=None)`（:380）：按人群等级随机生成词缀；`forced_tier` 可强制颜色等级。

## 2. 数据迁移后状态

- **JSON 优先**: `_ca_path = gamedir/core/data/customers/customer_affixes.json`（:18），用原生 `os.path` + `json.load` 自载（**不走 DataLoader**，是两类自载路径之一）。
- **硬编码 fallback 保留**: JSON 缺失或 `color_tiers` 为空时，回退到文件内硬编码的 8 级表（:31-41）。fallback 是有意保留的兼容策略。
- 词缀数据进存档：顾客保存的是 `CustomerAffixes.to_dict()` 快照，读档 `from_dict()` 恢复，不受 JSON 后续修改影响。

## 3. 解耦方式

- **与生成逻辑解耦**: `generate_customer_affixes()` 是纯函数式生成器，不依赖 Customer 实例。
- **与应用逻辑解耦**: `apply_to_customer()` 单向把词缀效果写入顾客（预算倍率等），顾客本体（`world.rpy` 的 `Customer`）不感知词缀内部结构。
- **与人群系统解耦**: 只接收 `pop_rank`，由调用方（district 人群）决定生成参数。

## 4. 系统间联系

```
customer_affixes.json ──(自载, :18)──→ CUSTOMER_COLOR_TIERS + 词缀定义
                                         │
world.rpy:418 Customer.__init__ ──→ generate_customer_affixes(pop_rank=self.pop.rank)
                                         │
                                         ▼
                              CustomerAffixes ──→ apply_to_customer(customer)
                                         │
                                         ▼
                          预算倍率/行为修正 → 夜间结算评分反馈
```

## 5. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 直接编辑 JSON | ✅ | customer_affixes.json 结构简单（color_tiers 数组 + 词缀表），改后重启生效 |
| 开发控制台 | ✅ 查看 | 经 data_sync 校验 |

目前无专门的可视化编辑器标签页，规模尚小。

---

## 相关文档

- [data_loader.md](data_loader.md) — 自载 JSON 与 DataLoader 路径的对照
- [girl_components.md](girl_components.md) — 顾客评分与女孩绩效的交互（GirlEconomy）
- [event.md](event.md) — 顾客满意度事件
