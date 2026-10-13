# Brothel King - 存档格式与数据持久化

> 版本: 2026-10-13
> 用途: 理解存档结构，添加migration规则

---

## 📋 目录

1. [存档基础](#存档基础)
2. [存档内容](#存档内容)
3. [AutoRepair机制](#autorepair机制)
4. [添加Migration规则](#添加migration规则)
5. [兼容性最佳实践](#兼容性最佳实践)

---

## 💾 存档基础

### 存档位置

```
game/saves/
├── 1-1.save          # 存档槽 1 的第 1 页
├── 1-2.save          # 存档槽 1 的第 2 页
├── auto-1.save       # 自动存档 1
├── quick-1.save      # 快速存档 1
└── persistent        # 持久化数据（跨存档）
```

### 存档格式

BK 使用 Ren'Py 的标准存档格式（pickle + 压缩）：

- **主存档**: `.save` 文件，包含游戏状态快照
- **持久化数据**: `persistent` 文件，跨存档共享的数据

### 何时保存？

- **手动保存**: 玩家按 Esc → Save
- **自动保存**: 章节转换时，特定剧情点
- **快速保存**: 玩家按 F5
- **退出保存**: 游戏退出时（可选）

---

## 📦 存档内容

### 核心游戏状态

以下对象会被序列化到存档：

#### 1. Game 对象 (`services.game`)

```python
{
    "gold": 10000,              # 金钱
    "chapter": 2,               # 当前章节
    "girl_id_generated": 150,   # 已生成女孩ID计数
    "mixes": ["默认", "原神"],  # 激活的女孩包混合
    "free_girls": [...],        # 自由女孩列表
    "slavemarket_girls": [...], # 奴隶市场女孩
    # ... 更多字段
}
```

#### 2. Main (MC) 对象 (`services.mc`)

```python
{
    "name": "玩家名",
    "girls": [...],             # 玩家拥有的女孩列表
    "gold": 10000,              # MC金钱（与game.gold同步）
    "chapter": 2,
    # ... MC属性
}
```

#### 3. Calendar 对象 (`services.calendar`)

```python
{
    "time": 45,                 # 游戏内时间（天数）
    "day": 15,                  # 当月第几天
    "month": 2,                 # 月份
    "year": 1,                  # 年份
    # ...
}
```

#### 4. Girl 对象列表

每个Girl对象包含：

```python
{
    "name": "爱丽丝",
    "pack_name": "Alice_Pack",
    "charm": 45,
    "beauty": 50,
    # ... 所有属性
    "traits": ["Beautiful", "Loyal"],
    "perks": ["Master Waitress"],
    "love": 100,
    "fear": 20,
    "personality": "rebel",
    # ... 完整女孩状态
}
```

### Girl 组件数据

每个 Girl 有16个组件，每个组件的数据都会保存：

| 组件 | 保存的数据 |
|------|-----------|
| `GirlBase` | 基础信息（name, pack_name, path等） |
| `GirlStats` | 8个基础属性（charm等） |
| `GirlMood` | mood, energy, sanity |
| `GirlSex` | 性偏好，fixations，sex_acts |
| `GirlTraits` | 特质列表 |
| `GirlPerks` | Perk列表 |
| `GirlItems` | 装备的物品 |
| `GirlSchedule` | 工作日程 |
| `GirlEconomy` | upkeep, tips等经济数据 |
| `GirlRelationships` | 与其他女孩/MC的关系 |
| `GirlDialogue` | personality, background |
| `GirlEffects` | 当前生效的Effect列表 |
| `GirlPictures` | 图片缓存，文件列表 |
| `GirlLogging` | 日志记录，事件追踪 |
| `GirlTraining` | 训练进度，build_up等 |
| `GirlProgression` | 等级，XP，JP，Perk点数 |

### Mod 数据

#### v1 Mod (通过 `persistent.mods`)

```python
persistent.mods = {
    "Mod Name": {
        "active": True,
        "custom_var": "value",
        # Mod自定义数据
    }
}
```

#### v2 Mod 数据

v2 Mod 的状态通过 `persistent._bk_v2_mod_states` 保存：

```python
persistent._bk_v2_mod_states = {
    "mod_id": True,  # 启用/禁用状态
}
```

Mod 自定义数据需要自己序列化（使用 `HOOK_GAME_SAVED`）。

### 持久化数据 (`persistent`)

跨所有存档共享的数据：

```python
persistent.game_version = "0.3.0"
persistent.girl_mix = {
    "原神": ["角色1", "角色2", ...]
}
persistent.achievements = {...}
persistent.unlocked_perks = [...]
persistent.mods = {...}  # v1 Mod数据
persistent._bk_v2_mod_states = {...}  # v2 Mod启用状态
# ... 更多全局设置
```

---

## 🔧 AutoRepair机制

### 什么是AutoRepair？

AutoRepair是读档时自动修复存档数据的机制，用于：
- 处理旧版本存档
- 修复缺失的属性
- 适配代码重构

### AutoRepair触发时机

读档时，如果检测到以下情况，会触发AutoRepair：

1. 存档版本号与当前代码版本不一致
2. 对象缺少新增的属性
3. 数据结构发生变化

### AutoRepair位置

主要的AutoRepair逻辑在：

- `game/core/systems/game_systems.rpy` - `auto_repair()`
- `game/core/framework/core_entities.rpy` - 各实体的修复逻辑
- `game/core/framework/girlclass.rpy` - Girl对象修复

### AutoRepair示例

```python
# 在 auto_repair() 函数中

def auto_repair():
    # 1. 检查版本
    if not hasattr(game, "version"):
        game.version = "0.2.0"  # 旧存档

    # 2. 修复缺失属性
    if not hasattr(MC, "charisma"):
        MC.charisma = 3  # 新增属性的默认值

    # 3. 修复女孩对象
    for girl in MC.girls + farm.girls:
        if not hasattr(girl, "_progression"):
            # 新版本添加了 GirlProgression 组件
            girl._progression = GirlProgression(girl)

        # 修复缺失的属性
        if not hasattr(girl, "love"):
            girl.love = 0

    # 4. 数据迁移
    if hasattr(game, "old_attribute"):
        game.new_attribute = game.old_attribute
        del game.old_attribute
```

### AutoRepair日志

AutoRepair执行时会输出日志到 `log.txt`：

```
[AutoRepair] Detected save version: 0.2.0
[AutoRepair] Current version: 0.3.0
[AutoRepair] Adding missing attribute: MC.charisma
[AutoRepair] Fixed 15 girls
[AutoRepair] Repair complete
```

---

## ✏️ 添加Migration规则

### 何时需要Migration？

当你的代码修改会影响存档数据时，需要添加Migration：

| 修改类型 | 需要Migration？ | 示例 |
|---------|----------------|------|
| 添加新属性 | ✅ 是 | 给Girl添加新属性 `karma` |
| 删除属性 | ✅ 是 | 删除旧的 `old_stat` |
| 重命名属性 | ✅ 是 | `charm` → `charisma` |
| 修改数据结构 | ✅ 是 | 列表改为字典 |
| 修改计算逻辑 | ❌ 否 | 只是修改函数实现 |
| 添加新函数 | ❌ 否 | 不涉及数据 |
| UI修改 | ❌ 否 | 只是界面变化 |

### Migration步骤

#### 步骤1: 更新版本号

在 `game/core/init/variables.rpy` 或 `game/core/config/options.rpy`:

```python
define game_version = "0.3.1"  # 递增版本号
```

#### 步骤2: 在AutoRepair中添加规则

编辑 `game/core/systems/game_systems.rpy`:

```python
def auto_repair():
    # ... 现有代码 ...

    # ── Migration for version 0.3.1 ──
    if game.version < "0.3.1":
        renpy.log("[AutoRepair] Migrating to 0.3.1")

        # 示例1: 添加新属性
        for girl in MC.girls + farm.girls:
            if not hasattr(girl, "karma"):
                girl.karma = 0  # 默认值
                renpy.log(f"[AutoRepair] Added karma to {girl.name}")

        # 示例2: 重命名属性
        if hasattr(game, "old_name"):
            game.new_name = game.old_name
            del game.old_name
            renpy.log("[AutoRepair] Renamed game.old_name to game.new_name")

        # 示例3: 数据结构迁移
        if isinstance(game.some_data, list):
            # 从列表迁移到字典
            game.some_data = {item.id: item for item in game.some_data}
            renpy.log("[AutoRepair] Migrated some_data from list to dict")

        # 更新存档版本
        game.version = "0.3.1"
```

#### 步骤3: 测试Migration

1. 创建一个旧版本的存档
2. 修改代码（添加你的migration规则）
3. 读取旧存档
4. 检查 `log.txt` 确认Migration执行
5. 验证数据正确迁移

#### 步骤4: 处理边界情况

```python
# 安全检查
if hasattr(girl, "_stats") and girl._stats:
    # 只有当组件存在时才修复
    pass

# 使用 getattr 防止 AttributeError
old_value = getattr(game, "old_attr", None)
if old_value is not None:
    game.new_attr = old_value
```

### Migration最佳实践

#### ✅ 好的做法

```python
# 1. 版本号检查
if game.version < "0.3.1":
    # 只对需要迁移的版本执行

# 2. 详细日志
renpy.log(f"[AutoRepair] Migrating {girl.name}: added karma=0")

# 3. 安全检查
if hasattr(obj, "attr"):
    # 确保属性存在

# 4. 默认值合理
girl.karma = 0  # 而不是 None 或 -999

# 5. 清理旧数据
del game.old_attr  # 删除不再使用的属性
```

#### ❌ 避免的做法

```python
# ❌ 不检查版本，每次都执行
for girl in MC.girls:
    girl.karma = 0  # 会覆盖现有值！

# ❌ 没有日志
# （无法调试Migration问题）

# ❌ 不安全的访问
girl._stats.new_attr = 0  # 如果 _stats 不存在会崩溃

# ❌ 不合理的默认值
girl.karma = -1  # 负数可能导致游戏逻辑错误

# ❌ 不删除旧数据
# 旧属性永远留在存档中，浪费空间
```

---

## 🎯 兼容性最佳实践

### 1. 向后兼容（Backward Compatibility）

**目标**: 新代码能读取旧存档

**策略**:
- 使用 `getattr(obj, "attr", default)` 而不是直接访问
- 在 AutoRepair 中添加缺失属性
- 保留Migration逻辑至少2-3个版本

**示例**:
```python
# ✅ 兼容旧存档
karma = getattr(girl, "karma", 0)

# ❌ 不兼容
karma = girl.karma  # 旧存档会 AttributeError
```

### 2. 向前兼容（Forward Compatibility）

**目标**: 旧代码能读取新存档（有限支持）

**策略**:
- 不删除关键属性（即使不再使用）
- 渐进式弃用（deprecate → remove）
- 文档标注最低兼容版本

### 3. Mod兼容性

**v1 Mod**:
- Mod数据保存在 `persistent.mods[mod_name]`
- AutoRepair 不应删除Mod数据
- 即使Mod被删除，数据仍然保留

**v2 Mod**:
- 启用状态保存在 `persistent._bk_v2_mod_states`
- Mod需要自己处理数据持久化（使用 `HOOK_GAME_SAVED`）

### 4. 组件化架构的Migration

Girl 组件化后的Migration示例：

```python
def auto_repair():
    for girl in MC.girls + farm.girls:
        # 检查组件是否存在
        if not hasattr(girl, "_progression"):
            # 重构后新增的组件
            girl._progression = GirlProgression(girl)

        # 迁移旧属性到组件
        if hasattr(girl, "old_xp"):
            girl._progression.xp = girl.old_xp
            del girl.old_xp
```

### 5. 数据迁移检查清单

在提交代码前检查：

- [ ] 是否修改了保存到存档的数据结构？
- [ ] 是否更新了版本号？
- [ ] 是否添加了AutoRepair规则？
- [ ] 是否测试了旧存档加载？
- [ ] 是否添加了详细的日志？
- [ ] 是否更新了SAVE_FORMAT.md文档？
- [ ] 是否在 REFACTORING_PROGRESS.md 中记录了迁移？

---

## 📊 存档大小优化

### 常见问题

1. **图片缓存过大**: Girl对象缓存了大量图片路径
2. **日志数据膨胀**: GirlLogging 保存了所有历史事件
3. **重复数据**: 多个女孩共享相同的特质对象

### 优化策略

```python
# 1. 懒加载图片
@property
def pictures(self):
    if not hasattr(self, "_cached_pictures"):
        self._cached_pictures = load_pictures(self.path)
    return self._cached_pictures

# 2. 限制日志大小
def add_log(self, event):
    self.log.append(event)
    if len(self.log) > 100:  # 只保留最近100条
        self.log = self.log[-100:]

# 3. 使用引用而不是复制
girl.traits = [trait_registry.get(name) for name in trait_names]
# 而不是: girl.traits = [Trait(...) for name in trait_names]
```

---

## 🔍 调试存档问题

### 查看存档内容

```python
# 在开发者控制台 (Shift+O)

# 查看当前游戏状态
services.game.__dict__

# 查看女孩数据
MC.girls[0].__dict__

# 查看持久化数据
persistent.__dict__
```

### 常见存档错误

#### 错误1: AttributeError

```
AttributeError: 'Girl' object has no attribute 'karma'
```

**原因**: 旧存档缺少新属性

**修复**: 在AutoRepair中添加该属性

#### 错误2: PickleError

```
PickleError: Can't pickle <class 'xxx'>
```

**原因**: 对象不可序列化（包含函数、lambda等）

**修复**: 
- 不要在Girl对象中存储函数
- 使用 `__getstate__` 和 `__setstate__` 自定义序列化

#### 错误3: 存档损坏

```
Exception: Save file corrupt
```

**原因**: 
- 存档文件损坏
- 版本差异太大

**修复**:
- 删除损坏的存档
- 检查AutoRepair逻辑

---

## 📚 相关文档

- **重构进度**: `docs/project/REFACTORING_PROGRESS.md`
- **项目指南**: `docs/project/PROJECT_GUIDE.md`
- **Girl 组件**: `docs/architecture/girl_components.md`

---

**保持存档兼容，用户才能持续游戏！** 💾
