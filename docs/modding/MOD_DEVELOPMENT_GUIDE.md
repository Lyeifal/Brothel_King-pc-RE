# Brothel King - Mod开发完整指南

> 版本: 2026-10-13
> API版本: ModAPI v2
> 目标读者: Mod开发者

---

## 📚 目录

1. [快速开始](#快速开始)
2. [Mod项目结构](#mod项目结构)
3. [Manifest配置](#manifest配置)
4. [钩子系统](#钩子系统)
5. [注册API](#注册api)
6. [完整示例](#完整示例)
7. [调试与测试](#调试与测试)
8. [常见问题](#常见问题)

---

## 🚀 快速开始

### 第一步: 创建Mod目录

```bash
# 在 game/custom/mods/ 下创建你的Mod目录
game/custom/mods/My First Mod/
├── mod.rpy          # Mod主文件（必需）
├── README.md        # Mod说明（推荐）
└── tl/              # 翻译文件（可选）
    └── chinese_simplified/
        └── mod.rpy
```

### 第二步: 创建基础Mod文件

创建 `game/custom/mods/My First Mod/mod.rpy`:

```python
## My First Mod - 我的第一个Mod

init -1 python:
    # 获取Mod API实例
    api = ModAPIV2.instance()
    
    # Mod配置
    my_mod_manifest = {
        "name": "My First Mod",
        "version": "1.0.0",
        "api_version": 2,
        "min_game_version": "0.3.0",
        "author": "Your Name",
        "description": __("这是我的第一个Mod，用于学习Mod开发。"),
        "requires": [],      # 能力标识（见下文）
        "dependencies": [],  # 依赖的其他Mod ID
        "hooks": {},         # 钩子（见下文）
        "home_rightmenu_add_buttons": [],  # 主页按钮（见下文）
    }
    
    # 注册Mod
    api.register_mod("my_first_mod", my_mod_manifest)
    
    # 注册一个简单的钩子
    def on_day_starting(context):
        renpy.notify("新的一天开始了！")
    
    api.register_hook(api.HOOK_DAY_STARTING, on_day_starting)

## 就这么简单！你的第一个Mod完成了
```

### 第三步: 测试Mod

1. 启动游戏
2. 主菜单点击 "Mods" 按钮
3. 确认你的Mod出现在列表中
4. 进入游戏，每天开始时应该看到通知 "新的一天开始了！"

---

## 📁 Mod项目结构

### 标准结构

```
game/custom/mods/My Mod Name/
├── mod.rpy                  # Mod主文件（必需）
├── README.md                # Mod说明
├── data/                    # 数据文件（如果需要覆盖游戏数据）
│   ├── traits/
│   │   └── custom_traits.json
│   └── perks/
│       └── custom_perks.json
├── screens/                 # 自定义屏幕
│   └── my_custom_screen.rpy
├── images/                  # 图片资源
│   └── my_mod_icon.png
└── tl/                      # 翻译文件
    ├── chinese_simplified/
    │   └── mod.rpy
    └── english/
        └── mod.rpy
```

### 文件说明

| 文件/目录 | 必需？ | 说明 |
|----------|--------|------|
| `mod.rpy` | ✅ 必需 | Mod入口文件，包含注册代码 |
| `README.md` | 推荐 | Mod说明文档（用户可见） |
| `data/` | 可选 | 数据覆盖（JSON文件） |
| `screens/` | 可选 | 自定义UI屏幕 |
| `images/` | 可选 | Mod专用图片资源 |
| `tl/` | 推荐 | 多语言翻译 |

---

## ⚙️ Manifest配置

### 完整的Manifest示例

```python
my_mod_manifest = {
    # ── 基础信息 ──
    "name": "高级定价系统",           # Mod显示名称
    "version": "1.2.0",              # 版本号（语义化版本）
    "api_version": 2,                # 必须是2（使用v2 API）
    "min_game_version": "0.3.0",     # 最低游戏版本要求
    "author": "Your Name",           # 作者名
    "description": __("一个重新设计女孩定价算法的Mod，基于属性和特质动态计算价格。"),
    
    # ── 能力标识 ──
    "requires": [
        "girl_stats",     # 需要访问女孩属性
        "girl_traits",    # 需要访问女孩特质
        "economy",        # 需要修改经济系统
    ],
    
    # ── 依赖关系 ──
    "dependencies": [
        "item_quality",   # 依赖 Item Quality Mod
    ],
    
    # ── 钩子（稍后注册） ──
    "hooks": {},
    
    # ── 主页按钮 ──
    "home_rightmenu_add_buttons": [
        ("定价设置", "my_mod_pricing_settings"),  # (按钮文本, 屏幕名)
    ],
}
```

### 能力标识（requires）

声明你的Mod需要的能力，游戏会在注册时验证：

| 能力标识 | 说明 | 何时使用 |
|---------|------|---------|
| `girl_stats` | 访问/修改女孩属性（Charm, Beauty等） | 修改属性计算逻辑 |
| `girl_traits` | 访问/修改女孩特质（Traits） | 添加自定义特质 |
| `economy` | 访问/修改经济系统（价格、收入等） | 修改定价、支付逻辑 |
| `events` | 注册自定义事件 | 添加新事件 |
| `dialogue` | 注册自定义对话 | 添加新对话内容 |
| `pictures` | 访问女孩图片系统 | 自定义图片标签 |
| `game_modes` | 注册游戏模式 | 添加新游戏模式 |
| `origin` | 注册角色起源 | 添加新起源 |
| `scenario` | 注册剧本 | 添加新剧本 |
| `ngp_settings` | 注册NG+设置 | 添加NG+选项 |
| `items` | 注册物品/品质等级 | 添加新物品或品质 |

**注意**: 不声明能力标识不会报错，但建议声明以便用户了解Mod的功能范围

### 依赖关系（dependencies）

如果你的Mod依赖其他Mod，列出它们的ID：

```python
"dependencies": [
    "item_quality",      # Mod ID（不是显示名）
    "advanced_traits",
]
```

游戏会确保依赖的Mod先加载。

---

## 🪝 钩子系统

钩子（Hooks）是Mod介入游戏流程的主要方式。

### 可用的钩子列表

| 钩子常量 | 钩子名 | 触发时机 | 上下文参数 |
|---------|--------|---------|-----------|
| `HOOK_GIRL_GENERATED` | `girl_generated` | 女孩生成完成后 | `girl` |
| `HOOK_GIRL_ACQUIRED` | `girl_acquired` | 女孩被获得后 | `girl`, `price`, `context` |
| `HOOK_GIRL_SOLD` | `girl_sold` | 女孩被出售后 | `girl`, `price` |
| `HOOK_GIRL_RUNAWAY` | `girl_runaway` | 女孩逃跑后 | `girl` |
| `HOOK_DAY_STARTING` | `day_starting` | 每天开始时 | `time` |
| `HOOK_DAY_ENDING` | `day_ending` | 每天结束时 | `time` |
| `HOOK_NIGHT_STARTING` | `night_starting` | 夜间开始时 | `time` |
| `HOOK_NIGHT_FINISHED` | `night_finished` | 夜间结束后 | `time` |
| `HOOK_WEEK_STARTING` | `week_starting` | 每周开始时 | `week`, `time` |
| `HOOK_EVENT_TRIGGERING` | `event_triggering` | 事件触发前 | `event`, `event_type`, `label` |
| `HOOK_EVENT_FINISHED` | `event_finished` | 事件结束后 | `event`, `event_type`, `label` |
| `HOOK_SECURITY_EVENT` | `security_event` | 安全事件发生时 | `event_type`, `alert_level` |
| `HOOK_CHAPTER_STARTING` | `chapter_starting` | 章节开始时 | `chapter` |
| `HOOK_CHAPTER_FINISHED` | `chapter_finished` | 章节结束后 | `chapter` |
| `HOOK_GAME_SAVED` | `game_saved` | 游戏保存后 | 无 |
| `HOOK_GAME_LOADED` | `game_loaded` | 游戏读档后 | 无 |
| `HOOK_GIRL_DESTINATION_LIST` | `girl_destination_list` | 获取女孩目的地列表时 | `girl`, `at_working_cap` |
| `HOOK_GIRL_DESTINATION_ACCEPT` | `girl_destination_accept` | 女孩被送往目的地时 | `girl`, `destination` |
| `HOOK_ITEM_GENERATED` | `item_generated` | 物品生成后 | `item`, `template`, `tier` |

### 钩子注册方式1: 直接注册

```python
def on_girl_acquired(context):
    girl = context.get("girl")
    price = context.get("price")
    
    # 你的逻辑
    renpy.notify(f"{girl.name} 加入了你的青楼，花费 {price} 金币")
    
    # 可选：修改上下文（某些钩子支持）
    # context["price"] = int(price * 0.9)  # 打9折

# 注册钩子
api.register_hook(api.HOOK_GIRL_ACQUIRED, on_girl_acquired)
```

### 钩子注册方式2: Manifest批量注册

```python
def on_day_starting(context):
    pass

def on_night_finished(context):
    pass

# 在Manifest中批量注册
my_mod_manifest = {
    # ... 其他配置
    "hooks": {
        "day_starting": on_day_starting,
        "night_finished": on_night_finished,
    }
}
```

### 钩子优先级

```python
# priority越小越早执行（默认0）
api.register_hook(api.HOOK_GIRL_GENERATED, my_callback, priority=-10)  # 最先执行
api.register_hook(api.HOOK_GIRL_GENERATED, another_callback, priority=0)  # 正常顺序
api.register_hook(api.HOOK_GIRL_GENERATED, last_callback, priority=10)  # 最后执行
```

### 钩子最佳实践

#### ✅ 好的做法

```python
def on_girl_generated(context):
    girl = context.get("girl")
    
    # 检查参数有效性
    if not girl:
        return
    
    # 使用try-except保护
    try:
        # 你的逻辑
        girl.add_trait("Custom Trait")
    except Exception as e:
        renpy.log(f"[My Mod] Error: {e}")
```

#### ❌ 避免的做法

```python
def on_girl_generated(context):
    # ❌ 不检查参数直接使用
    girl = context["girl"]  # 可能KeyError
    
    # ❌ 没有异常处理
    girl.add_trait("NonExistent Trait")  # 可能崩溃
    
    # ❌ 阻塞操作
    time.sleep(5)  # 会卡住游戏
```

---

## 📦 注册API

Mod可以注册自定义内容到游戏系统。

### 1. 注册自定义特质（Trait）

```python
from游戏 import Trait, Effect

# 创建自定义特质
lucky_trait = Trait(
    name="Lucky",
    name_i18n=__("幸运"),
    verb="be",
    eff=[
        Effect("special", "lucky", 1.2),  # 特殊效果
    ],
    base_description=__("这个女孩运气特别好"),
    archetype="The Lucky One"
)

# 注册特质
api.register_trait(lucky_trait, category="positive")
```

### 2. 注册自定义Perk

```python
from游戏 import Perk, Effect

custom_perk = Perk(
    name="Master Waitress",
    name_i18n=__("服务大师"),
    eff=[
        Effect("boost", "waitress", 2),  # 服务员技能翻倍
    ],
    base_description=__("这个女孩是服务专家"),
    pic="my_mod_icon.png"  # 可选图标
)

api.register_perk(custom_perk)
```

### 3. 注册自定义事件

```python
from游戏 import StoryEvent

custom_event = StoryEvent(
    label="my_mod_random_event",  # 对应的label名
    type="city",                   # "city" 或 "daily"
    location="market",             # 地点（可选）
    chapter=2,                     # 章节要求（可选）
    once=False,                    # 是否只触发一次
    chance=0.3                     # 触发概率
)

api.register_event("my_mod_event_id", custom_event, category="community")
```

然后创建对应的label:

```renpy
label my_mod_random_event:
    "这是一个自定义事件！"
    "在市场发生了有趣的事情..."
    return
```

### 4. 注册自定义物品品质

```python
from游戏 import QualityTier

# 添加一个"传说"品质
legendary_tier = QualityTier(
    rank=7,  # 比原版最高的6还高
    price_modifier=50.0,  # 价格x50
    rarity_bump=0,
    effect_scaling=5.0,  # 效果x5
    prefixes={
        "dress": "Legendary",
        "misc": "Legendary",
        "furniture": "Legendary",
    },
    prefixes_i18n={
        "dress": __("传说级"),
        "misc": __("传说级"),
        "furniture": __("传说级"),
    }
)

api.register_quality(legendary_tier)
```

### 5. 注册自定义标签（Tag）

```python
# 注册新的图片标签
api.register_tag("my_custom_tag", ("custom", "special"))
```

### 6. 注册自定义对话

```python
from游戏 import Dialogue

# 为某个对话主题添加新内容
api.register_dialogue(
    topic="free_greetings_polite",  # 对话主题
    key="my_mod_greeting",           # 唯一key
    dialogue=Dialogue(__("你好呀，主人！这是来自Mod的问候。")),
    merge=True  # 合并到现有对话而不是覆盖
)
```

---

## 💡 完整示例

### 示例1: 简单的通知Mod

```python
## Notification Mod - 每日提醒

init -1 python:
    api = ModAPIV2.instance()
    
    notification_manifest = {
        "name": "Daily Reminder",
        "version": "1.0.0",
        "api_version": 2,
        "min_game_version": "0.3.0",
        "author": "Your Name",
        "description": __("每天提醒你重要事项"),
        "requires": [],
        "dependencies": [],
        "hooks": {},
        "home_rightmenu_add_buttons": [],
    }
    
    api.register_mod("daily_reminder", notification_manifest)
    
    # 钩子：每天开始时检查
    def check_daily_reminders(context):
        time = context.get("time")
        
        # 检查是否周一
        if time and calendar.get_day_of_week() == 0:
            renpy.notify("今天是周一，别忘了安排女孩的工作日程！")
        
        # 检查金钱
        if services.game and services.game.gold < 100:
            renpy.notify("警告：金钱不足100！")
    
    api.register_hook(api.HOOK_DAY_STARTING, check_daily_reminders)
```

### 示例2: 自定义特质包

```python
## Custom Traits Pack - 自定义特质包

init -1 python:
    api = ModAPIV2.instance()
    
    traits_pack_manifest = {
        "name": "扩展特质包",
        "version": "1.1.0",
        "api_version": 2,
        "min_game_version": "0.3.0",
        "author": "Trait Master",
        "description": __("添加20个新特质到游戏"),
        "requires": ["girl_traits"],
        "dependencies": [],
        "hooks": {},
        "home_rightmenu_add_buttons": [],
    }
    
    api.register_mod("custom_traits_pack", traits_pack_manifest)
    
    # 定义多个自定义特质
    custom_traits = [
        Trait(
            name="Bookworm",
            name_i18n=__("书虫"),
            verb="be",
            eff=[Effect("change", "refinement", 1)],
            base_description=__("喜欢读书的女孩"),
            archetype="The Scholar"
        ),
        Trait(
            name="Athletic",
            name_i18n=__("运动健将"),
            verb="be",
            eff=[Effect("change", "constitution", 2)],
            base_description=__("体格强壮"),
            archetype="The Athlete"
        ),
        # ... 更多特质
    ]
    
    # 批量注册
    for trait in custom_traits:
        api.register_trait(trait, category="positive")
```

### 示例3: 价格修改Mod（使用钩子修改数据）

```python
## Price Override Mod - 价格覆盖

init -1 python:
    api = ModAPIV2.instance()
    
    price_mod_manifest = {
        "name": "高级定价系统",
        "version": "1.0.0",
        "api_version": 2,
        "min_game_version": "0.3.0",
        "author": "Economist",
        "description": __("基于女孩属性重新计算价格"),
        "requires": ["girl_stats", "economy"],
        "dependencies": [],
        "hooks": {},
        "home_rightmenu_add_buttons": [
            ("定价设置", "price_mod_settings")
        ],
    }
    
    api.register_mod("advanced_pricing", price_mod_manifest)
    
    # 自定义定价算法
    def calculate_custom_price(girl):
        base_price = 100
        
        # 根据属性计算
        stats_avg = (girl.charm + girl.beauty + girl.body + girl.refinement) / 4
        price = base_price * (1 + stats_avg / 10)
        
        # 特质加成
        if girl.has_trait("Beautiful"):
            price *= 1.5
        if girl.has_trait("Virgin"):
            price *= 2.0
        
        return int(price)
    
    # 钩子：女孩获得时重新计算价格
    def on_girl_acquired(context):
        girl = context.get("girl")
        if girl:
            original_price = context.get("price", 0)
            new_price = calculate_custom_price(girl)
            
            renpy.log(f"[Price Mod] {girl.name}: {original_price} -> {new_price}")
            # 注意：这只是日志，实际修改价格需要拦截型钩子（见下文）
    
    api.register_hook(api.HOOK_GIRL_ACQUIRED, on_girl_acquired)

# 自定义设置屏幕
screen price_mod_settings():
    frame:
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 400
        
        vbox:
            text "高级定价系统设置" size 24
            null height 20
            text "这里可以添加设置选项..."
            null height 20
            textbutton "关闭" action Hide("price_mod_settings")
```

---

## 🐛 调试与测试

### 1. 使用开发者控制台

按 `Shift+O` 打开控制台：

```python
# 查看已注册的Mod
services.mod_api_v2.get_mod_info()

# 查看已注册的钩子
services.mod_api_v2._mod_hooks

# 手动触发钩子测试
services.mod_api_v2.execute_hook("day_starting", {"time": calendar.time})

# 检查服务
services
```

### 2. 日志输出

```python
# 使用renpy.log输出到控制台
renpy.log("[My Mod] Debug message")

# 使用renpy.notify显示游戏内通知
renpy.notify("Mod已加载")
```

### 3. 测试清单

创建 `game/custom/mods/My Mod/TEST_CHECKLIST.md`:

```markdown
# 测试清单

- [ ] Mod出现在主菜单Mod列表
- [ ] Mod信息显示正确
- [ ] 钩子正确触发（检查日志）
- [ ] 自定义内容正确注册（Trait/Perk等）
- [ ] 没有控制台错误
- [ ] 存档/读档正常工作
- [ ] 与其他Mod兼容
```

### 4. 常见调试技巧

#### 检查Mod是否加载

```python
def on_game_loaded(context):
    renpy.notify("My Mod loaded successfully!")

api.register_hook(api.HOOK_GAME_LOADED, on_game_loaded)
```

#### 钩子触发日志

```python
def on_girl_acquired(context):
    girl = context.get("girl")
    renpy.log(f"[My Mod] Girl acquired: {girl.name if girl else 'None'}")
    renpy.log(f"[My Mod] Context: {context}")

api.register_hook(api.HOOK_GIRL_ACQUIRED, on_girl_acquired)
```

---

## ❓ 常见问题

### Q1: 我的Mod不出现在Mod列表中？

**检查**:
1. 文件名是否正确（`mod.rpy`）
2. 是否在 `game/custom/mods/` 目录下
3. 是否调用了 `api.register_mod()`
4. 查看控制台是否有错误信息
5. 确保 `api_version = 2`

### Q2: 钩子没有触发？

**检查**:
1. 钩子名是否正确（使用 `api.HOOK_*` 常量）
2. 回调函数是否正确接收 `context` 参数
3. 查看控制台是否有异常
4. 使用 `renpy.log()` 输出调试信息

### Q3: 如何访问游戏对象（如MC、女孩列表）？

```python
# 通过服务容器访问
game = services.game
mc = services.mc
calendar = services.calendar
brothel = services.brothel

# 获取女孩列表
girls = mc.girls  # 玩家拥有的女孩
free_girls = game.free_girls  # 自由女孩
```

### Q4: 如何让Mod支持多语言？

创建翻译文件：

```
game/custom/mods/My Mod/
└── tl/
    ├── chinese_simplified/
    │   └── mod.rpy
    └── english/
        └── mod.rpy
```

在主文件中使用 `__()`:

```python
description=__("这是Mod描述")
```

然后在翻译文件中：

```renpy
translate chinese_simplified strings:
    old "This is mod description"
    new "这是Mod描述"
```

### Q5: Mod会影响存档吗？

- **v2 Mod是永久激活的**（安装即启用）
- Mod注册的内容会保存在存档中
- 删除Mod后，旧存档可能需要AutoRepair
- 建议在Mod说明中提醒用户备份存档

### Q6: 如何拦截游戏逻辑而不是只观察？

**当前状态**: 19个钩子都是"通知型"，暂不支持拦截

**未来计划**: 部分钩子将支持 `cancel_hook` 返回值来拦截默认逻辑

**临时方案**: 使用猴子补丁（Monkey Patching）覆盖原函数（高级，不推荐）

### Q7: 可以添加新的UI界面吗？

**可以**！通过 `home_rightmenu_add_buttons` 在主页右侧菜单添加按钮。

**步骤1**: 在Manifest中注册按钮screen名称

```python
"home_rightmenu_add_buttons": ["right_menu_my_button"],
```

**步骤2**: 定义右侧菜单按钮screen（必须使用 `style_group "rm"`）

```renpy
screen right_menu_my_button():
    textbutton __("我的功能") style_group "rm":
        action Show("my_custom_screen")
        tooltip __("打开自定义界面")
```

**步骤3**: 定义你的主界面screen

```renpy
screen my_custom_screen():
    modal True
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 400
        
        vbox:
            spacing 20
            text __("这是自定义界面") size 24 bold True
            
            null height 20
            
            textbutton __("关闭") action Hide("my_custom_screen")
```

**⚠️ 常见错误**：

❌ **错误1**: 使用元组格式
```python
# 错误！
"home_rightmenu_add_buttons": [
    ("按钮文本", "screen_name")  # ❌ 不要用元组！
]
```

✅ **正确**: 只提供screen名称列表
```python
# 正确！
"home_rightmenu_add_buttons": ["right_menu_button_screen"]
```

❌ **错误2**: 忘记 `style_group "rm"`
```renpy
# 错误！按钮样式会不一致
screen right_menu_my_button():
    textbutton "我的功能" action Show("...")  # ❌ 缺少 style_group
```

✅ **正确**: 必须使用 `style_group "rm"`
```renpy
# 正确！
screen right_menu_my_button():
    textbutton __("我的功能") style_group "rm":  # ✅ 使用 rm 样式组
        action Show("...")
```

---

## 🚨 翻译文件注意事项

### Mod翻译只包含Mod特有字符串

**原则**: Mod的翻译文件（`tl/chinese_simplified/`）应该**只翻译Mod特有的字符串**，不要翻译游戏本体已有的通用词汇。

**❌ 不要翻译这些通用字符串**：
- `ON` / `OFF`
- `Yes` / `No`
- `True` / `False`
- `Close` / `OK` / `Cancel` / `Confirm`
- `Save` / `Load` / `Delete`
- 其他游戏本体UI已有的文本

**原因**: 这些字符串已在游戏本体的翻译文件中定义，重复定义会导致 **翻译冲突错误**：

```
Exception: A translation for "OFF" already exists at 
game/custom/mods/YourMod/tl/chinese_simplified/mod.rpy:29.
```

**✅ 正确做法**：

```renpy
# tl/chinese_simplified/mod.rpy

translate chinese_simplified strings:

    # ✅ 翻译Mod特有的字符串
    old "Advanced Pricing System"
    new "高级定价系统"
    
    old "Custom Price: [custom_price] gold"
    new "自定义价格：[custom_price] 金币"
    
    # ❌ 不要翻译通用字符串（会冲突）
    # old "ON"
    # new "开启"
    
    # old "Close"
    # new "关闭"
    
    # 注释说明为什么不翻译
    # 注意：ON/OFF/Close 等通用字符串已在游戏本体中翻译，此处不重复定义
```

---

## 📚 参考资源

### 官方文档
- **项目文档**: `docs/README.md`
- **Mod系统架构**: `docs/architecture/mod_system.md`
- **数据加载器**: `docs/architecture/data_loader.md`

### 示例Mod（必看）
- **Auction House**: `game/custom/mods/Auction House/`
- **Item Quality**: `game/custom/mods/Item Quality/`
- **Mod模板**: `game/core/templates/mod_template/mod_template.rpy`

### 开发工具
- **Mod API验证**: `python tools/verify_mod_api.py`
- **测试框架**: 游戏内Tests按钮（开发者模式）

---

## 🎉 祝你Mod开发顺利！

如有问题，欢迎查看示例Mod或在社区提问。

Happy Modding! 🚀
