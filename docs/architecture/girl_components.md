# Girl 组件系统架构

> 最后更新: 2026-09-11（Phase 7 批次1-14 后，与代码核对）
> **核心文件**: `game/core/framework/girlclass.rpy`（1,148 行，原约 5,900 行）、`game/core/framework/girl/`（组件包）
> **Phase**: Phase 2（组件化解耦）+ Phase 7（组件化收官 — 方法体全量迁移）

---

## 1. 系统职责

Girl 类原本是约 5,900 行的上帝类。Phase 2 将其按领域拆分为 **16 个组件类**，每个组件持有 Girl 实例引用，负责一个专注领域；`Girl` 类本体（girlclass.rpy，`class Girl(EffectBearer)`）现只保留 `__init__`（状态字段 + 组件实例化）、已迁移方法的委托壳、少量有意保留的微方法（如 1 行 `get_schedule`）和 24 个活 `_impl` 别名。

关键数字（全部经 grep 核实，Phase 7 后）：

- 组件类：**16 个**（`game/core/framework/girl/girl_*.rpy`，每文件一类，init -2；含 Phase 7 新建 `girl_progression.rpy`）。
- `_impl` 别名：**24 个**（仅保留真实现仍在 girlclass 的方法，如 `get_schedule`/`is_unique`）。
- Girl 类方法 ~212 个（`def ` 计数），几乎全部为一行委托壳；全部 2,000+ 旧调用点无需改动。

> 口径说明：旧文档的"15 组件 + 宿主 + 工厂 = 17"口径已更新为 16 组件（新增 GirlProgression）。

## 2. 组件清单

| 组件类 | 文件 | 行数 | 职责 | 已迁移实现（★） |
|--------|------|-----:|------|----------------|
| `GirlBase` | `girl_base.rpy` | 166 | 身份：命名、ini 加载、获得后初始化 | ★ `set_name` / `load_ini` / `init_after_acquire` |
| `GirlStats` | `girl_stats.rpy` | 389 | 属性、上下限、溢出、测试 | ★ `get_stat` / `change_stat` / `get_stat_minmax` / `stat_spillover` 等 |
| `GirlProgression` | `girl_progression.rpy` | 483 | 等级/排名/职业等级、XP-JP-rep、Perk、属性升级 | ★ 全部 28 方法（Phase 7 批次6 新建） |
| `GirlTraits` | `girl_traits.rpy` | 244 | 特质/天赋管理、护盾、防御 | ★ `generate_traits` / `add_trait` / `has_perk` / `test_shield` |
| `GirlItems` | `girl_items.rpy` | 170 | 装备、物品使用、交付 | ★ `use_item` / `equip` / `take` |
| `GirlSchedule` | `girl_schedule.rpy` | 244 | 工作分配、工作日、日程 | ★ `set_job` / `will_do` / `get_status` |
| `GirlSex` | `girl_sex.rpy` | 784 | 性行为、性癖、偏好、品味 | ★ 49 方法（含 `generate_preferences` 内外层合并） |
| `GirlMood` | `girl_mood.rpy` | 610 | 心情、理智、体力、健康、疲劳 | ★ 心情簇 / `change_energy` / `heal` / `rest` / `tired_check` |
| `GirlRelationships` | `girl_relationships.rpy` | 372 | 爱、恐惧、MC 关系、spoiling/恐吓 | ★ `change_love/fear` / `receive_gift` / `update_relationships` |
| `GirlEconomy` | `girl_economy.rpy` | 489 | 价格、保养费、小费、接待能力 | ★ `get_price` / upkeep 簇 / `whore_on_street` / `get_tip` |
| `GirlDialogue` | `girl_dialogue.rpy` | 497 | 对话、`say()`、性格、`is_`、描述 | ★ `pick_dialogue` / `get_personality_description` / `is_` |
| `GirlPictures` | `girl_pictures.rpy` | 426 | 图片选择、刷新、评估 | ★ `get_fix_pic` 等（早前已迁移） |
| `GirlEffects` | `girl_effects.rpy` | 59 | 效果包装（委托 EffectBearer） | —（纯委托） |
| `GirlGeneration` | `girl_generation.rpy` | 116 | 随机化、性格、背景编排 | —（编排入口，依赖各组件） |
| `GirlLogging` | `girl_logging.rpy` | 253 | 日志、追踪、记忆、近期事件 | ★ `add_log` / `track_event` / `remembers` 等 12 方法 |
| `GirlTraining` | `girl_training.rpy` | 316 | 农场训练、服从检定、build-up | ★ `will_do_farm_act` / `get_obedience_check_target` / `reset_build_up` |

`girl/__init__.rpy` 头部为 16 组件全 ★ 表（仅 effects/generation 为薄包装），以代码为准。

## 3. 委托模式

### 3.1 组件实例化

Girl.__init__ 末尾（girlclass.rpy:158-173）创建全部组件，组件通过 `self.girl` 反向访问 Girl 的任意状态/方法：

```python
# girlclass.rpy:158-173（节选）
# Phase 2.1: Component delegation (see game/core/framework/girl/)
self._base = GirlBase(self)
self._stats = GirlStats(self)
self._traits = GirlTraits(self)
# ... 共 15 个
```

### 3.2 方法委托（薄包装）

Girl 类保留原方法签名，方法体一行转调组件，旧调用点完全无感知：

```python
# girlclass.rpy:183-195（GirlMood 委托示例）
## Phase 2.1: Delegated to GirlMood component ##
def init_sanity(self):
    return self._mood.init_sanity()

def get_sanity(self):
    return self._mood.get_sanity()
```

### 3.3 `_impl` 别名约定

方法体仍在 Girl 类内、但由组件"认领"的领域，组件通过 `_impl` 别名调用 Girl 上的**未绑定原始实现**，绕过委托层，避免无限递归：

```python
# girlclass.rpy:3713-3721（Economy 别名区，类体内部）
# ── Phase 2.1: Economy delegation aliases ──
_get_price_impl = get_price
_get_med_upkeep_impl = get_med_upkeep
_adjust_upkeep_impl = adjust_upkeep
```

```python
# girl/girl_stats.rpy:127-129 — 组件侧调用
def stat_spillover(self, stat, chg, job=None):
    '''属性溢出处理 | Handle stat spillover between main and sex stats'''
    return self.girl._stat_spillover_impl(stat, chg, job)
```

别名在类体执行期绑定为普通函数对象（非 bound method），组件拿到 Girl 实例后显式传 `self.girl` 调用。全类共 156 个此类别名（按 `^\s+_[a-z_]+_impl = [a-z_]+$` 精确计数）。

## 4. 方法迁移模式

每个迁移提交遵循统一四步（见 git log 中 Phase 2 系列提交）：

1. **新建组件文件**（`girl_<domain>.rpy`，init -2），类持有 `girl` 引用。
2. **方法体迁入组件**：实现代码从 girlclass.rpy 移入组件方法，语义保持不变。
3. **Girl 侧留委托**：原方法变为一行 `return self._<comp>.<method>(...)`。
4. **加 `_impl` 别名**：若组件内部需回调 Girl 的其他方法，在类体注册别名。

未迁移的方法体（如 `_stat_spillover_impl`、`_test_stats_impl`、`_get_xp_cap_impl` 等仍留在 girlclass.rpy）通过别名暴露给组件，形成"组件管接口、宿主保留实现"的过渡形态。

## 5. 迁移教训：`get_stat` 双倍计入 bug

**这是组件迁移中最具代表性的事故，修复于提交 `1c62fd1`（2026-09-11）。**

### 现象

迁移 `get_stat` 到 `GirlStats` 时，实现把效果加成计算了两次：

```python
# 有 bug 的版本（girl_stats.rpy 历史版本）
eff = g.get_effect("change", stat_name) + g.get_effect("change", "all skills")
# ... 主属性/性属性分支还会再加 "all main skills" / "all sex skills" ...
stat_obj = g.find_stat(stat_name)
if not stat_obj:
    return 0
val = stat_obj.value + eff
# 处理额外效果 | Handle additional effects          ← 重复累加
extra = (g.get_effect("change", stat_name) + g.get_effect("change", "all skills"))
return val + extra
```

`eff` 已含 `change <stat>` 与 `change all skills`，`extra` 又把同一对效果加了一遍 —— 所有效果加成双倍计入，直接抬高女孩属性评估、绩效与价格。

### 修复（当前代码 girl_stats.rpy:25-50）

1. 删除重复的 `extra` 累加，恢复基线语义：`result = stat_obj.value + eff`。
2. 恢复非法属性名的硬断言（`raise AssertionError(...)`，列出合法名）——bug 版把断言换成了静默 `return 0`，掩盖了调用方传错名。
3. 恢复取整与下限：`round_int(result)`，负值归零。
4. 测试同步更新（`tools/test_runner.rpy` 同提交修改）。

### 教训

- **迁移时必须逐行对照原实现的求值顺序**，尤其是效果/加成类"累加型"代码，最容易在搬运时"顺手再补一次"。
- **不要用静默降级替换断言**。bug 版为"健壮性"把 `AssertionError` 改成 `return 0`，使错误传播到下游数值而非在源头暴露。
- 效果加成代码必须配套断言语义的回归测试（本次修复同步改了 test_runner）。

## 6. Phase 7 迁移教训（2026-09-11，批次1-14）

### 6.1 `generate_preferences` 双重执行 bug

**最具代表性的 Phase 7 事故，修复于 f027957。**

早期迁移把 `generate_preferences` 的**内层**（偏好/固恋生成）放进 GirlSex，Girl 侧留**外层包装**（调内层 + generate_stats + 贞洁管制 + NGP 设置）——当时正确。Phase 7 批次 8 把外层并入组件时，girlclass 侧的外层包装**未同步缩减为纯壳**，导致 `girl.generate_preferences()` 把外层逻辑执行两遍：性属性二次生成（dice 重摇）、NGP 偏好设置二次叠加（`change_preference` 非幂等）、贞洁管制二次运行。

### 修复

组件持有 inner+outer 合并实现，girlclass 改为 `self._sex.generate_preferences()` 纯壳——与迁移前"全部逻辑在一个方法体内"的语义一致。

### 教训

- **包装器型方法迁移时，组件侧合并与宿主侧缩壳必须成对完成**；只并一边就会双执行。迁移后应 grep 宿主方法体，确认不再残留已并入组件的逻辑。
- **幂等性自检**：若并入的逻辑含随机生成（dice）或非幂等变更（偏好叠加），双执行立刻可见；审查时优先检查这类方法。

### 6.2 组件内过时副本

Phase 7 发现组件里存在多个**与 girlclass 真身语义不同的旧副本**：`sanity_warning`（组件 3 分支 vs 真身 6 分支）、`farm_beg_test`（判定阈值相反）、`use_item`（简化版）、`take`/`get_equipped`（行为不同）、`get_stat_minmax`（5 行简化版 vs 63 行领域版）。

### 教训

- **组件里的同名方法不一定是壳**，迁移前必须逐字 diff girlclass 真身与组件副本；以 girlclass（活代码）为准。
- `get_stat_minmax` 的简化副本还导致 `change_stat` 技能上限从基线的 `max(rank*50+...)` 退化为恒定 100（批次 10 随迁移一并修复，恢复基线语义）——**同名方法双实现并存时，内部调用方可能已在用错误的那个**。

### 6.3 列表推导变量遮蔽

组件方法统一约定 `g = self.girl`，而原代码惯用 `g` 作推导式/循环变量（`[g.name for g in self.friends]`）。机械替换会把 girl 引用遮蔽。Phase 7 全部批次共处理 20+ 处，一律重命名循环变量（`gf`/`gv` 等）。

### 教训

- `self→g` 机械替换后必须搜索方法体内的 `for g in` / `[g for` / `if g !=` 逐一核对。

---

## 相关文档

- [services.md](services.md) — 服务容器（同批重构工程）
- [girl_pack.md](girl_pack.md) — 女孩包与 GirlFilesDict
- [trait_perk.md](trait_perk.md) — GirlTraits 组件对接的 Trait/Perk 注册表
- [ui_screens.md](ui_screens.md) — girl_profile 等屏幕已随组件化同步提取
