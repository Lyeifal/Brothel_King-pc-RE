# BK Evolution — i18n 最佳实践

> 最后更新: 2026-09-25（新增 §2.5 init 翻译时机边界；§5 加入占位符审计；audit_placeholders 支持 %% 转义）
>
> 本文档定义 BK Evolution 项目的国际化（i18n）规范，确保所有玩家可见文本都能被 Ren'Py 翻译系统正确收集。
>
> 适用范围：`game/core/` 下的所有 `.rpy` 脚本和 `game/core/data/` 下的所有 JSON 数据文件。

---

## 核心原则

1. **所有玩家可见字符串必须显式标记为可翻译**
2. **禁止用 Python `+` 拼接玩家可见句子**
3. **数据驱动的文本必须放在 JSON 中，并使用 `_i18n` 后缀**
4. **翻译文件按源文件目录结构分布，符合 Ren'Py 标准**
5. **init 0 之前 `__()` 不产生翻译**：init < 0 构建的数据字典存原文，显示点运行时查表（见 §2.5）

---

## 1. Ren'Py 脚本层规范

### 1.1 字符串包裹

所有显示给玩家的字符串必须使用 `__()`（Screen Language 中使用 `_()`）：

```renpy
# ✅ 正确
renpy.call_screen("yes_no", __("Do you really want to buy this item?"))
renpy.say(npc, __("Hello, Master!"))
renpy.notify(__("Saved successfully."))

# ❌ 错误
renpy.call_screen("yes_no", "Do you really want to buy this item?")
renpy.say(npc, "Hello, Master!")
renpy.notify("Saved successfully.")
```

### 1.2 Screen Language

Screen 中的 `text`、`button`、`label` 等必须包裹 `_()`：

```renpy
# ✅ 正确
text _("Choose an option")
button _("Cancel") action Return()
label _("Settings") style "preferences_label"

# ❌ 错误
text "Choose an option"
button "Cancel" action Return()
label "Settings" style "preferences_label"
```

例外（不需要翻译）：
- 纯图标/图片标签：`{image=...}`
- 单字符符号：`"-"`、`"+"`、`">"`
- 纯数字或格式化占位符本身

### 1.3 menu: 选项

Ren'Py 原生 `menu:` 的字面量选项会自动提取。如果选项是变量，需要包裹 `__()`：

```renpy
# ✅ 正确：字面量自动提取
menu:
    "Train her gently":
        ...
    "Punish her":
        ...

# ✅ 正确：变量包裹
$ caption = __("Train her gently")
menu:
    "[caption]":
        ...

# ❌ 错误：变量未包裹
$ caption = "Train her gently"
menu:
    "[caption]":
        ...
```

### 1.4 禁止字符串拼接

禁止用 `+` 拼接玩家可见文本。改用完整模板 + 占位符：

```renpy
# ❌ 错误
"Are you sure you want to take a loan for " + str(r.amount) + " gold?"

# ✅ 正确：% 占位符
__("Are you sure you want to take a loan for %s gold?") % r.amount

# ✅ 正确：format 占位符
__("Are you sure you want to take a loan for {amount} gold?").format(amount=r.amount)

# ✅ 正确：Ren'Py 插值（推荐，当变量在 Ren'Py 上下文中可用时）
__("Are you sure you want to take a loan for [r.amount] gold?")
```

### 1.5 格式化字符串包裹

所有玩家可见的 `%` 格式化字符串必须包裹 `__()`：

```renpy
# ❌ 错误
"You gained %s gold." % amount

# ✅ 正确
__("You gained %s gold.") % amount
```

### 1.6 动态文本插值

优先使用 Ren'Py 内置插值 `[variable]`：

```renpy
# ✅ 推荐
__("Hello, [girl.name]!")

# ✅ 也可以
__("Hello, %s!") % girl.name
```

---

## 2. JSON 数据层规范

### 2.1 `_i18n` 后缀约定

所有可翻译文本字段必须以 `_i18n` 结尾：

```json
{
  "id": "pirate_captain",
  "name_i18n": "Pirate Captain",
  "description_i18n": "A feared captain of the high seas.",
  "icon_tag": "origin_pirate",
  "price": 100
}
```

| 字段类型 | 示例 | 是否需要 `_i18n` |
|----------|------|------------------|
| 显示名称 | `name_i18n` | ✅ 是 |
| 描述 | `description_i18n` | ✅ 是 |
| 内部 ID/代码 key | `id`, `key`, `tag` | ❌ 否 |
| 图片/音频路径 | `pic`, `icon`, `sound` | ❌ 否 |
| 数值 | `price`, `rank`, `cost` | ❌ 否 |
| 效果/条件表达式 | `effects`, `requirements` | ❌ 否 |

### 2.2 字典值集合

如果父字段本身以 `_i18n` 结尾，其字典值也视为可翻译：

```json
{
  "help_dict_i18n": {
    "intro": "Welcome to the help system.",
    "combat": "Combat is turn-based."
  }
}
```

`json_i18n.rpy` 会自动收集 `help_dict_i18n` 下的所有字符串值。

### 2.3 代码中使用

使用 `get_i18n()` 或 `I18nMixin` 从 JSON 读取并翻译：

```renpy
init python:
    # 方法 A：get_i18n()
    name = get_i18n(item, "name")
    description = get_i18n(item, "description")

    # 方法 B：I18nMixin
    class MyEntity(I18nMixin):
        @classmethod
        def from_dict(cls, data):
            d = cls._resolve_i18n(data)
            return cls(name=d["name"], description=d.get("description"))
```

### 2.4 JSON 字符串同步进翻译文件（必需）

JSON `_i18n` 字符串在 init 期**动态注册**（`game/core/i18n/json_i18n.rpy`），Ren'Py 的 `translate --empty` **看不到它们**——不手动同步，它们永远不会出现在提取结果里。

**在 JSON 中新增或修改任何 `_i18n` 字段后，必须运行：**

```powershell
python tools/import_json_i18n.py
```

该脚本会把缺失的 `_i18n` 文本以空 `old`/`new` 对追加到 `game/tl/chinese_simplified/strings.rpy`（按 `old` 文本去重），之后走常规导出 → 翻译 → 导入流程。随时可用 `python tools/audit_json_i18n.py` 核对覆盖（必须输出 "All JSON _i18n strings are translated!"）。

### 2.5 init 阶段翻译时机（关键边界）

**实测结论（2026-09-25，lint 探针验证）：字符串翻译表在 init 0 才完成加载。init 优先级 < 0 的代码块里调用 `__()` 一律返回英文原文**——不是报错，是静默失效：

```renpy
# ❌ 静默失效：init -4 时翻译表未加载，gstats_dict 永远存英文原文
init -4 python:
    gstats_dict = {k: __(v) for k, v in _stats_data["stat_descriptions"].items()}

# ✅ 正确：字典存原文，显示点运行时查表（tooltip 渲染时翻译表已就绪）
init -4 python:
    gstats_dict = {k: v for k, v in _stats_data["stat_descriptions"].items()}

# 显示点（屏幕/tooltip 求值期，init 0 之后）
def get_description(self, ...):
    description = __("%s%s. %s") % (..., __(gstats_dict[self.name]))
```

为什么大部分界面"看起来正常"：screen 的 `text` 显示件在**渲染时会二次查表**，init 期存下的英文值经 `text` 显示仍会被翻译。真正漏译的是**不经过 `text` 显示件的通路**：

- `tooltip` 属性值（tooltip 是字符串属性，不做渲染期查表）
- Python 侧字符串拼接/组合后的整串
- 直接参与 `%` 格式化的字典值

配套规则：

1. **init < 0 构建的数据字典一律存原文**，不要指望定义处 `__()`；显示点统一 `__(var)` 运行时查表（对变量查表只要 `old/new` 条目存在即生效，条目可手动维护在 `strings.rpy`）。
2. **反过来，逻辑 key 禁止翻译**：如 `gstat_job_skill` 的值（`"masseuse"` 等）被用作 `get_max_cust_served()` 等查找 key，必须保持英文原文——init 期"恰好失效"反而保证了这一点，不要"修"它。
3. **定位经验**：`game/core/init/variables.rpy` 的 `init -4` 统计字典（`gstats_dict` / `gstats_descript` / `gstat_job_skill`）与 `game/core/data/settings.rpy` 的 `init -10`（`stat_name_dict` / `diff_*`）均属此类。`init ≥ 0` 的 JSON 加载（`init 1` 的 `minion_description`、`MC_stat_description` 等）定义处 `__()` 有效。

---

## 3. 随机生成文本规范

### 3.1 模板池 JSON 化

女孩随机对话、流言、背景生成池等应放在 `game/core/data/settings/` 下的 JSON 文件中（由 `DataLoader` 对应 `load_*()` 方法加载）：

```json
{
  "greeting_i18n": {
    "friendly": [
      "Good morning, Master!",
      "I hope you're having a good day."
    ],
    "shy": [
      "H-hello...",
      "Um, good morning..."
    ]
  }
}
```

现有实例（2026-09-11 与代码核对）：

| JSON 文件 | 加载方法（`game/core/systems/data_loader.rpy`） | 内容 |
|-----------|------------------------------------------|------|
| `settings/gossip.json` | `load_gossip()` | 城市流言文本库 |
| `settings/dialogue_texts.json` | `load_dialogue_texts()` | 笑话/赞美等社交对话文本 |
| `settings/girl_background_pools.json` | `load_girl_background_pools()` | 女孩背景生成随机池（故事/家庭/ guardian /爱好等） |
| `settings/farm/…`（`farm/farm_perform_dict.json`） | `load_farm_perform_dict()` | 农场表演文本 |

### 3.2 运行时填充

代码中从模板池随机选择并填充占位符：

```renpy
init python:
    def get_girl_line(pool_name, personality, **kwargs):
        templates = girl_background_pools.get(pool_name, {}).get(personality, [])
        if templates:
            tmpl = random.choice(templates)
            return __(tmpl) % kwargs
        return ""
```

禁止在代码中按词拼接随机描述。

---

## 4. 翻译文件目录结构

Ren'Py `translate --empty` 会按源文件位置生成 `translate chinese_simplified strings:` 块。保持这种分布：

```
game/tl/chinese_simplified/
├── core/content/         # 剧情、事件、互动翻译
│   ├── main_story/
│   ├── city_events/
│   ├── day_events/
│   └── interactions.rpy
├── core/ui/              # UI 翻译
│   ├── screens.rpy
│   └── main.rpy
├── core/systems/         # 系统提示翻译
│   └── help.rpy
└── strings.rpy           # 通用字符串翻译
```

不要强制把所有字符串移回 `strings.rpy`。

---

## 5. 验证流程

每次提交前必须运行：

```powershell
# 0. 若 JSON `_i18n` 字段有变更：先同步（见 §2.4）
python tools/import_json_i18n.py

# 1. i18n 审计
python tools/i18n_lint.py

# 2. JSON _i18n 覆盖审计（必须输出 "All JSON _i18n strings are translated!"）
python tools/audit_json_i18n.py

# 3. 回归测试
python tools/verify_i18n.py

# 4. 占位符一致性审计（%% 转义感知；防止 "%s" 误写成 "%%s" 导致
#    运行时 "%s" % (a, b) 抛 TypeError: not all arguments converted）
python tools/audit_placeholders.py

# 5. Ren'Py lint
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . lint
```

所有检查必须通过。注意：`audit_placeholders.py` 会把**有空占位符的未翻译条目**（空 `new`）也报为 mismatch——这类条目运行时会回退英文原文、不崩溃，但凡是会被 `%`/`[var]` 格式化的字符串，空翻译即隐患，应优先补翻。

---

## 6. 常见反模式与修复

| 反模式 | 问题 | 修复 |
|--------|------|------|
| `call_screen("yes_no", "...")` | 确认框英文 | `call_screen("yes_no", __("..."))` |
| `"Hello " + name` | 语法不可译 | `__("Hello %s") % name` |
| `"%s gold" % amount` | 模板未进入翻译系统 | `__("%s gold") % amount` |
| `text "Settings"` | UI 英文 | `text _("Settings")` |
| 硬编码女孩描述 | 无法数据化翻译 | 迁移到 `data/settings/` 下的 JSON 模板池（见 §3.1） |
| JSON 字段 `name` 同时做显示和 key | 切换语言后持久化/查找失效 | 用 `id` 做 key，`name_i18n` 做显示 |
| `init -4 python:` 里 `gstats_dict = {k: __(v) ...}` | init 0 前翻译表未加载，静默存下英文原文；tooltip 等非 text 通路漏译 | 字典存原文，显示点 `__(dict[key])` 运行时查表（见 §2.5） |
| 译文把 `%s` 误写成 `%%s` | 占位符少一个，启用该翻译后运行到 `__("...%s...") % (a, b)` 直接抛 `TypeError: not all arguments converted` 崩溃（2026-09-25 性欲属性说明曾因此崩档） | 译文占位符数量/类型必须与原文一致；提交前跑 `tools/audit_placeholders.py`（已支持 `%%` 转义感知） |
| 译文引入原文不存在的 `[变量]` | 运行时 `renpy.substitutions` 抛 `NameError: Name 'xxx' is not defined` 崩档（2026-09-25 day_events 的 `[cntext]` 曾因此崩溃） | 译文中的 `[var]` 必须是原文行已有的变量；需要改写句式时用块内 `$` 赋值新变量承载翻译 |

---

## 7. 例外情况

以下情况可以保留英文/不翻译：

1. **调试信息**：只在开发者模式下显示
2. **图片/音频路径**：如 `resources/pics/foo.webp`
3. **代码 key/标识符**：如 `trait_id`、`effect_name`
4. **Ren'Py 内部标签**：如 `{image=...}`、`{color=...}`
5. **纯数字、单字符符号**

---

## 8. 剧情事件机制备忘（非 i18n，但影响翻译测试）

测试翻译时若发现"剧情 NPC/地区解锁怎么刷都不触发"，先排查机制而非翻译：

1. **一次性链式事件随存档持久化**。`c1_thieves_guild_tip`（盗贼公会链起点，任意地点 25%/次访问）、`farm_meet_gizel`（香料市场 50%）、`farm_meet_goldie`（农场 50%）等 `once=True` 事件只在 `init_events`（开局/换章）加入 `city_events`。若存档创建时它们没进列表（如调试开局），之后永远缺失。**新开局正常路径已验证可触发**；旧存档靠 `after_load` 的修复钩子自动补加（见 `events_dispatcher.rpy` after_load，幂等）。
2. **`init_events` 门槛**：`_use_story_mode and not debug_mode` 且 `chapter <= 1`。`debug_mode` 非空（Debug Fast/Custom 开局）会整批跳过第一章剧情事件——与官方原版行为一致；`game.game_mode` 为 `None` 时 `is_story_mode()` 默认 True（向后兼容），模式过滤不会拦截剧情事件。
3. **链式结构**：盗贼公会 = 小费(任意地点) → 香料市场 → 下水道 → 公会地点解锁（`thieves_guild.secret = False`）；农场 = 香料市场遇 Gizel → 垃圾场 → 农场。用 lint 探针（真实类 + 桩对象跑 `happens()` 数千次）可验证触发率是否符合 `chance` 设定。

---

## 相关文件

- [`game/core/i18n/json_i18n.rpy`](../../game/core/i18n/json_i18n.rpy) — JSON i18n 注册
- [`game/core/systems/data_loader.rpy`](../../game/core/systems/data_loader.rpy) — JSON 数据加载
- [`tools/i18n_lint.py`](../../tools/i18n_lint.py) — i18n 审计
- [`tools/verify_i18n.py`](../../tools/verify_i18n.py) — i18n 回归测试
- [`tools/audit_placeholders.py`](../../tools/audit_placeholders.py) — 占位符一致性审计
- [`I18N_ROADMAP.md`](I18N_ROADMAP.md) — 当前 i18n 状态与路线图
- [`TRANSLATION_STATUS.md`](TRANSLATION_STATUS.md) — 中文翻译补完记录（历史+当前基线）
