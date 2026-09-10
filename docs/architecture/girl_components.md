# Girl 组件系统架构

> 最后更新: 2026-09-11（与代码核对）
> **核心文件**: `game/core/framework/girlclass.rpy`（3,910 行，原约 5,900 行）、`game/core/framework/girl/`（组件包）
> **Phase**: Phase 2（Girl 系统重构 — 组件化解耦）

---

## 1. 系统职责

Girl 类原本是约 5,900 行的上帝类。Phase 2 将其按领域拆分为 **15 个组件类**，每个组件持有 Girl 实例引用，负责一个专注领域；`Girl` 类本体（girlclass.rpy:26，`class Girl(EffectBearer)`）保留状态字段、序列化和尚未迁移的方法，并对已迁移方法做委托。

关键数字（全部经 grep 核实）：

- 组件类：**15 个**（`game/core/framework/girl/girl_*.rpy`，每文件一类，init -2）。
- `_impl` 别名：**156 个**（girlclass.rpy 内 `_<method>_impl = <method>` 形式的类体别名）。
- Girl 类剩余方法约 215 个（`def ` 计数），全部 2,000+ 旧调用点无需改动。

> 口径说明：任务口径的"17"若指女孩子系统文件总数，则为 15 组件 + `girlclass.rpy`（宿主类）+ `girl_factory.rpy`（工厂函数）= 17；组件类本身为 15 个。

## 2. 组件清单

| 组件类 | 文件 | 行数 | 职责 | 已迁移实现（★） |
|--------|------|-----:|------|----------------|
| `GirlBase` | `girl_base.rpy` | 34 | 身份：姓名、等级、序列化 | —（轻量包装） |
| `GirlStats` | `girl_stats.rpy` | 188 | 属性、上限、变更、溢出 | ★ `get_stat` / `change_stat` / `set_stat` / `average_skills` |
| `GirlTraits` | `girl_traits.rpy` | 155 | 特质/天赋管理 | ★ `generate_traits` |
| `GirlItems` | `girl_items.rpy` | 110 | 装备、物品、背包 | — |
| `GirlSchedule` | `girl_schedule.rpy` | 155 | 工作分配、工作日、日程 | ★ `get_status` |
| `GirlSex` | `girl_sex.rpy` | 415 | 性行为、性癖、偏好 | ★ `will_do_sex_act` / `refresh` / `activate` / `deactivate` 等 30 个 |
| `GirlMood` | `girl_mood.rpy` | 196 | 心情、理智、体力、健康 | ★ `change_energy` / `heal` / `rest` |
| `GirlRelationships` | `girl_relationships.rpy` | 98 | 爱、恐惧、服从、MC 关系 | ★ `change_love` / `change_fear` |
| `GirlEconomy` | `girl_economy.rpy` | 274 | 价格、保养费、小费、绩效 | ★ `get_price` / `get_xp` / `get_jp` / `get_rep` / `estimate_performance` |
| `GirlDialogue` | `girl_dialogue.rpy` | 217 | 对话选择、`say()`、性格 | ★ `pick_dialogue` / `say` / `rand_say` |
| `GirlPictures` | `girl_pictures.rpy` | 431 | 图片选择、刷新、评估 | ★ `get_fix_pic` |
| `GirlEffects` | `girl_effects.rpy` | 59 | 效果包装（委托 EffectBearer） | —（纯委托） |
| `GirlGeneration` | `girl_generation.rpy` | 116 | 随机化、性格、背景、偏好 | —（`randomize` 入口） |
| `GirlTraining` | `girl_training.rpy` | 177 | 训练 | 部分方法体 |
| `GirlLogging` | `girl_logging.rpy` | 32 | 日志、追踪、近期事件 | —（薄组件） |

`girl/__init__.rpy` 头部注释（"Total: 11 components"）已过时——当时只完成了 10 个组件 + 1 个 stub，现为 15 个组件类，勿再引用。

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

---

## 相关文档

- [services.md](services.md) — 服务容器（同批重构工程）
- [girl_pack.md](girl_pack.md) — 女孩包与 GirlFilesDict
- [trait_perk.md](trait_perk.md) — GirlTraits 组件对接的 Trait/Perk 注册表
- [ui_screens.md](ui_screens.md) — girl_profile 等屏幕已随组件化同步提取
