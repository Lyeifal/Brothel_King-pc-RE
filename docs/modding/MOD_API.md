# BK Evolution — Mod API 参考（v1 + v2）

> 最后更新: 2026-09-11（与代码核对）
>
> 本文档是 Brothel King Evolution Mod 机制的权威参考，涵盖旧版 v1 `Mod()` 类与新版 `ModAPIV2` 两套机制。
> 所有行号、参数、行为均以当前代码为准（分支 `bk-evolution`）。

---

## 0. 快速选择：v1 还是 v2？

| | v1（`Mod()`） | v2（`ModAPIV2`） |
|---|---|---|
| 入口 | 实例化 `Mod(...)` 类 | `services.mod_api_v2.register_mod(mod_id, manifest)` |
| 注册方式 | 构造时自动加入 `detected_mods` | 显式 manifest 注册，带校验 |
| 激活语义 | **逐存档开关**：主菜单 Mods 界面可激活/停用，状态存 `persistent.mods` | **常驻激活**：文件放进 `game/custom/mods/` 即生效，无开关 |
| 停用方式 | Mods 界面 Deactivate | 删除 `game/custom/mods/<Mod>/` 整个文件夹 |
| 生命周期标签 | `early/init/night/update/load/remove_label` + `chapter_labels` | 无标签机制，用 hooks（`game_saved`/`game_loaded` 等） |
| 主页右侧菜单按钮 | `home_rightmenu_add_buttons` | manifest 的 `home_rightmenu_add_buttons`（v2 新增支持） |
| 事件注册 | `events={...}` + `add_event()` | 继承 `ModAPI.register_event()` 等 Registry 包装 |
| 钩子系统 | `mod.hooks` dict → `HookManager`（Phase 6 兼容层） | manifest `hooks` 或 `register_hook()` → 标准化钩子 |
| 模板 | `game/custom/mods/Goldo's cool mod/`（教程范例） | `game/core/templates/mod_template/mod_template.rpy` |
| 完整范例 | 同上（v1） | `game/custom/mods/Auction House/`（权威范例，见 §6） |

**建议**：

- **新 Mod 一律用 v2**——有版本声明、能力校验、标准化钩子，且主页菜单按钮等新 UI 集成只保证对 v2 持续维护。
- v1 仍完全可用，适合"逐存档开关"语义的场景（玩家可能想在某些存档关闭 Mod）。Goldo's cool mod 这类教程型事件 Mod 继续按 v1 工作。
- 两套机制可共存，互不影响（v2 有自己的单例与钩子表）。

---

## 1. v1 Mod 机制

### 1.1 `Mod()` 类全参数

定义：`game/core/framework/challenges.rpy:370`（`init -2 python`）。构造时**自动注册**到全局 `detected_mods` 字典（`challenges.rpy:432`）。

```python
Mod(
    name,                     # 必填。Mod 显示名，同时是 detected_mods / persistent.mods 的 key
    folder,                   # 必填。Mod 文件夹名，用于拼资源路径 "mods/" + folder + "/"
    creator="Unknown",        # 作者名
    version=1.0,              # 版本号。用于 check_for_updates() 检测更新
    pic=None,                 # 标题图片文件名（相对 Mod 路径），显示在 Mods 界面
    description=__("This is a mod for Brothel King."),  # 描述文本
    help_prompts=None,        # [(按钮文字, label), ...] 见 §1.3
    init_label="",            # 激活后、青楼建立后调用（call_in_new_context）
    night_label="",           # 激活后每晚调用（加入 daily_events，type="night"）
    update_label="",          # 存档加载时发现版本变化时调用
    home_rightmenu_add_buttons=None,  # [屏幕名, ...] 见 §1.4
    events=None,              # {事件名: StoryEvent, ...} 见 §1.3
    early_label="",           # 开局早期调用（district/brothel 建立之前）
    load_label="",            # 读档时调用（无参）
    remove_label="",          # 停用时调用（清理用）
)
```

构造后自动计算的属性：

| 属性 | 说明 | 代码位置 |
|------|------|----------|
| `path` | `"mods/" + folder + "/"`，资源查找路径 | `challenges.rpy:380` |
| `full_name` | `name + " v" + version + ", from " + creator` | `challenges.rpy:388` |
| `pic` | `Picture(pic, path+pic)` 或 `None` | `challenges.rpy:383-386` |
| `help_prompts` | 每个 prompt 自动加 `[Mod名] ` 前缀 | `challenges.rpy:393-397` |
| `chapter_labels` | `{1: None, ..., 7: None}`，每章开始时可调 label（**非构造参数**，init 后自行赋值） | `challenges.rpy:406` |
| `hooks` | `{}`，Phase 6 钩子表 `{hook_name: callback}`（**非构造参数**，init 后自行赋值） | `challenges.rpy:425` |
| `api_version` | 恒为 `1` | `challenges.rpy:426` |
| `active` / `seen` | 激活状态 / Mods 界面是否已查看 | `challenges.rpy:433-434` |

**自定义属性持久化**：`Mod` 重写了 `__setattr__`/`__getattribute__`（`challenges.rpy:441-465`）。init 阶段之后赋值的自定义属性会写入全局 `mod_settings`（`defaultdict(dict)`），**随存档保存**，init 重跑时从 `mod_settings` 恢复而非被默认值覆盖。注意 `name`、`init` 两个属性除外。

### 1.2 自动注册与激活流程

相关全局变量（`game/core/init/variables.rpy:2389-2395`）：`detected_mods = {}`、`persistent.mods = {}`（首次运行初始化）、`mod_traceback`、`updated_games`。

`persistent.mods[name]` 结构（`game/core/framework/game_systems.rpy:205`）：

```python
{"version": mod.version, "check": mod.get_check(), "active": mod.active}
```

`get_check()` 返回 `(version, path, init_label, len(events))` 用于检测版本变化（`challenges.rpy:468-469`）。

流程（按调用顺序）：

1. **init 阶段**：Mod 的 `.rpy` 在 `init -1`（惯例）实例化 `Mod(...)` → 自动进入 `detected_mods`。
2. **开局**（`label start`，`game/core/systems/events_dispatcher.rpy:94`）→ 调用 `update_mods()`（`game/core/framework/game_systems.rpy:150`）：
   - `persistent.mods` 中有但 `detected_mods` 中不存在的 → 删除记录并提示 "has been removed"；
   - 新 Mod（`persistent.mods` 无记录）→ `register_mod(mod)` 写入 persistent，提示 "has been added"；
   - `check_for_updates()` 不同 → 重新 register，提示 "has been updated" 并置 `active=True`；
   - 已记录且 `persistent.mods[name]["active"]` → 置 `mod.active = True`。
3. **早期激活**（`events_dispatcher.rpy:671`）→ `game.start_mods(early=True)`：对 `detected_mods` 中 active 的 Mod 调 `activate_mod(mod, early=True)`，只触发 `early_label`。
4. **完全激活**（`events_dispatcher.rpy:968`）→ `game.start_mods()`：`game.activate_mod(mod)`（`game/core/framework/core_entities.rpy:243`）依次：
   - 注册 `mod.hooks` 到 `hook_manager`（Phase 6 兼容层，`:254-257`）；
   - 注册 `mod.events` 到 `event_registry`（category="mod"，`:260-262`）；
   - `night_label` 非空 → 追加 `StoryEvent(label=night_label, type="night", once=False)` 到 `daily_events`（`:264-265`）；
   - `renpy.call_in_new_context(mod.init_label)`（`:270-272`）。
5. **Mods 界面开关**（`screen mods`，`game/core/ui/screens/screen_quest.rpy:564` 起）：
   - `mod.activate()`（`challenges.rpy:480`）：yes_no 确认 → `active=True` + 写 `persistent.mods` → `game.activate_mod(self)`；
   - `mod.deactivate()`（`challenges.rpy:495`）：yes_no 确认 → `active=False` + 写 persistent → `game.deactivate_mod(self)`（调用 `remove_label` 做清理，`core_entities.rpy:291-292`）。
   - 注意：主菜单 "Mods" 按钮只在 `detected_mods` 非空时显示（`game/core/config/screens.rpy:999`），v1 的开关都在这个界面完成。
6. **读档时**（`label after_load`，`events_dispatcher.rpy:186` 起）：刷新 `game.active_mods` 中的 Mod 实例引用、收集并 `call` 每个 active Mod 的 `load_label`；随后（`game/core/ui/main.rpy:907`）`game.update_mods()` 处理"Mod 被删/版本变化/新激活"三种情况，可能返回 `update_label` 列表待调用。
7. **每章开始**（`events_dispatcher.rpy:974-978`）：对每个 active Mod 检查 `mod.chapter_labels[game.chapter]`，非空且 label 存在则排入章节标签调用队列（不存在则抛 `AssertionError`）。

### 1.3 events 与 help_prompts

**events**：构造参数 `events={...}` 的值必须是 `StoryEvent` 对象（构造时 `ev.mod = self` 自动关联，`challenges.rpy:429-430`）。激活时全部注册到 `event_registry`（§1.2 第 4 步），之后用 `mod.add_event(event_name, type=..., date=..., delay=1, call_args=None)` 调度（`challenges.rpy:508`）：

- `type="alarm"` → `calendar.set_alarm(date, ev)`（默认 `date = calendar.time + delay`）；
- `type in ("morning", "day", "night")` → 加入 `daily_events`；
- `type="city"` → 加入 `city_events`（MC 到访对应地点时触发）。

**help_prompts**：`[(按钮文字, label), ...]`。游戏内 Help（"?"）菜单会把所有 active Mod 的 help_prompts 合并进选项列表（`game/core/systems/help.rpy:374-375`），按钮文字自动加 `[Mod名] ` 前缀。目标 label 用 `call` 调用，可做 Mod 选项菜单（Goldo's cool mod 的 "Surprise me tomorrow" 即此机制）。

**labels 一览**（均在 `game.activate_mod` / 读档 / 章节流程中 `call_in_new_context` 或 `call`，无参）：

| label | 触发时机 |
|-------|----------|
| `early_label` | 开局早期，district/brothel 建立**前**（`activate_mod(early=True)`，`core_entities.rpy:247-252`） |
| `init_label` | Mod 激活时（青楼建立后） |
| `night_label` | 每晚（经 daily_events） |
| `update_label` | 读档发现版本变化且无该 label 时回退为 reset 流程 |
| `load_label` | 每次读档（`after_load`，`events_dispatcher.rpy:203-210`） |
| `remove_label` | 停用时清理（`core_entities.rpy:291-292`） |
| `chapter_labels[n]` | 第 n 章开始时（1-7，`events_dispatcher.rpy:974`） |

### 1.4 home_rightmenu_add_buttons（v1）

构造参数，值为**无参 screen 名列表**。主页右侧菜单（`game/core/ui/screen_home.rpy`）：

- `:59-61` 遍历 `game.active_mods`，收集声明了按钮的 v1 Mod；
- `:73-74` 有任何 v1/v2 Mod 按钮时菜单加一行；
- 展开时由 `screen mod_menu_display(mod_menu, v2_buttons)`（`screen_home.rpy:382`）以 `use expression <screen名>` 逐个渲染（`:390-394`），按 Mod 分组、显示 Mod 名。

按钮 screen 内部通常是一个 `textbutton`，`action` 跳转 Mod 自己的界面（Goldo's cool mod 的 `test_mod_but` 与 Auction House 的 `right_menu_auction` 都是这个模式）。

---

## 2. v2 Mod 机制（ModAPIV2）

实现：`game/core/systems/mods/mod_api_v2.rpy`（`init -3 python`），类 `ModAPIV2(ModAPI)`。
单例：`mod_api_v2 = ModAPIV2()`（`:205`），注册进服务容器 `services.register("mod_api_v2", mod_api_v2)`（`:206`），可用 `services.mod_api_v2` 访问（属性定义 `game/core/systems/services/service_container.rpy:109-111`）。因为继承 `ModAPI`，v1 的 `register_trait` / `register_event` 等 Registry 包装方法在 v2 上同样可用（`game/core/systems/mods/mod_api.rpy`）。

### 2.1 `register_mod(mod_id, manifest)` 与 manifest 全字段

签名：`game/core/systems/mods/mod_api_v2.rpy:50`。

```python
services.mod_api_v2.register_mod("my_mod", {
    "name": "My Mod",                # 显示名（Mods 界面、主页菜单分组标题）
    "version": "1.0",                # Mod 版本（展示用；当前不做比较校验）
    "api_version": 2,                # 必须为 2，否则 ValueError
    "min_game_version": "0.3",       # 最低游戏版本（声明用；当前不做强制校验）
    "author": "Your Name",           # 作者
    "description": __("..."),        # 描述（Mods 界面展示）
    "requires": ["girl_traits"],     # 能力标志列表，见 §2.2
    "hooks": {"girl_generated": my_callback},  # {钩子名: 回调}，见 §3
    "dependencies": ["other_mod"],   # 依赖的 mod_id 列表（声明用；当前不做强制校验）
    "home_rightmenu_add_buttons": ["my_screen"],  # 主页右侧菜单按钮 screen 列表，见 §2.3
})
```

字段逐一说明：

| 字段 | 类型 | 必填 | 校验/行为 |
|------|------|------|-----------|
| `name` | str | 建议 | `get_menu_buttons()` / `get_mod_info()` 的显示名；缺省时回落到 `mod_id` |
| `version` | str | 建议 | 仅展示。代码不解析、不比较 |
| `api_version` | int | **是** | 必须 `== 2`，否则 `ValueError`（`mod_api_v2.rpy:74-76`） |
| `min_game_version` | str | 否 | 仅记录。**当前代码不强制** |
| `author` | str | 建议 | 仅展示 |
| `description` | str | 建议 | 仅展示（Mods 界面） |
| `requires` | [str] | 否 | 每项必须在 `CAPABILITIES` 集合内，否则 `ValueError`（`:78-80`），见 §2.2 |
| `hooks` | {str: callable} | 否 | 每个回调以 `(mod_id, callback, 0)` 注册进 `_mod_hooks`（`:88-89`） |
| `dependencies` | [str] | 否 | 仅记录。**当前代码不检查**依赖是否已注册 |
| `home_rightmenu_add_buttons` | [str] | 否 | 无参 screen 名列表，见 §2.3 |

注册期校验汇总（`:73-83`）：

1. `api_version != 2` → `ValueError`；
2. `requires` 含未知能力标志 → `ValueError`；
3. **重复注册同一 `mod_id` → `ValueError`**（`:82-83`）——init 重跑场景下需避免二次注册。

`renpy.config.developer` 为真时，注册成功会 `renpy.log` 输出（`:91-93`）。

### 2.2 常驻激活语义与能力标志

**常驻激活**（`mod_api_v2.rpy:67-71` 明确注释）：

- v2 Mod **安装即激活**——把文件夹放进 `game/custom/mods/` 即被 Ren'Py 加载并执行注册块，没有任何逐存档开关；
- **停用 = 删除文件**：从 `game/custom/mods/` 移除该 Mod 文件夹即可；
- 状态不写入 `persistent.mods`（那是 v1 的机制），v2 的 `_active_mods` 是 init 期内存注册表；
- `unregister_mod(mod_id)`（`:95-99`）存在但主要用于测试/热重载场景，正常 Mod 不需要调用。

**能力标志**（`CAPABILITIES`，`mod_api_v2.rpy:30-41`）——声明 Mod 需要的能力面，当前用于注册期校验与文档语义：

```python
"girl_stats"    # 修改女孩属性
"girl_traits"   # 注册自定义特质/天赋
"economy"       # 修改经济计算
"events"        # 注册/分发事件
"dialogue"      # 自定义对话行
"pictures"      # 自定义图片标签
"game_modes"    # 注册自定义游戏模式
"origin"        # 注册玩家出身
"scenario"      # 注册剧本
"ngp_settings"  # NG+ 设置
```

### 2.3 home_rightmenu_add_buttons（v2）

manifest 字段，值为**无参 screen 名列表**。`get_menu_buttons()`（`:109-119`）返回 `[(mod_id, 显示名, [按钮 screen 名])]`——只包含声明了按钮的激活 Mod。主页右侧菜单在 `screen_home.rpy:65-69` 通过 `services.mod_api_v2.get_menu_buttons()` 取列表，交由 `screen mod_menu_display` 的 `v2_buttons` 参数渲染（`screen_home.rpy:395-401`），与 v1 Mod 的按钮并列展示、按 Mod 分组。

### 2.4 生命周期钩子

v2 没有 v1 的 label 机制，生命周期事件通过钩子覆盖：

- `game_saved`：经 `renpy.config.save_json_callbacks` 在每次保存时触发（`mod_api_v2.rpy:214-218`，防重复注册）；
- `game_loaded`：在 `label after_load` 触发（`events_dispatcher.rpy:189-191`，带 `hasattr` 保护兼容旧存档）。

---

## 3. 钩子点完整参考（16 个）

常量定义：`game/core/systems/mods/mod_api_v2.rpy:187-202`。命名惯例 `<domain>_<action>_<tense>`（`girl_runaway`、`girl_sold`、`security_event` 三个名字不含 `_<tense>`，`tools/verify_mod_api.py` 会对此发出命名惯例警告，属已知事项）。

回调签名统一为 `callback(context: dict)`；`execute_hook` 把关键字参数打包成 context dict 传入（`mod_api_v2.rpy:143-159`）。

| # | 常量 | 字符串值 | 调用点（文件:行号） | context 键 |
|---|------|----------|---------------------|-----------|
| 1 | `HOOK_GIRL_GENERATED` | `girl_generated` | `game/core/framework/girl_factory.rpy:278` | `girl` |
| 2 | `HOOK_GIRL_ACQUIRED` | `girl_acquired` | `game/core/systems/events_dispatcher.rpy:8440` | `girl`, `price`, `context` |
| 3 | `HOOK_GIRL_SOLD` | `girl_sold` | `game/core/ui/main.rpy:839`、`game/core/ui/main.rpy:1452` | `girl`, `price` |
| 4 | `HOOK_GIRL_RUNAWAY` | `girl_runaway` | `game/core/systems/events_dispatcher.rpy:1173` | `girl` |
| 5 | `HOOK_DAY_STARTING` | `day_starting` | `game/core/systems/endday.rpy:1498` | `time` |
| 6 | `HOOK_DAY_ENDING` | `day_ending` | `game/core/systems/endday.rpy:340` | `time` |
| 7 | `HOOK_NIGHT_STARTING` | `night_starting` | `game/core/systems/endday.rpy:403` | `time` |
| 8 | `HOOK_NIGHT_FINISHED` | `night_finished` | `game/core/systems/endday.rpy:1431` | `time` |
| 9 | `HOOK_WEEK_STARTING` | `week_starting` | `game/core/framework/core_entities.rpy:1937` | `week`, `time` |
| 10 | `HOOK_EVENT_TRIGGERING` | `event_triggering` | `game/core/systems/events_dispatcher.rpy:1084` | `event`, `event_type`, `label` |
| 11 | `HOOK_EVENT_FINISHED` | `event_finished` | `game/core/systems/events_dispatcher.rpy:1087` | `event`, `event_type`, `label` |
| 12 | `HOOK_SECURITY_EVENT` | `security_event` | `game/core/systems/security.rpy:62` | `event_type`, `alert_level` |
| 13 | `HOOK_CHAPTER_STARTING` | `chapter_starting` | `game/core/systems/events_dispatcher.rpy:661` | `chapter` |
| 14 | `HOOK_CHAPTER_FINISHED` | `chapter_finished` | `game/core/systems/events_dispatcher.rpy:1053` | `chapter` |
| 15 | `HOOK_GAME_SAVED` | `game_saved` | `game/core/systems/mods/mod_api_v2.rpy:215`（save_json_callbacks） | 无 |
| 16 | `HOOK_GAME_LOADED` | `game_loaded` | `game/core/systems/events_dispatcher.rpy:191`（after_load） | 无 |

说明：

- `event_triggering` 在事件分发前触发，`event_finished` 在结束后触发，二者 context 相同；
- `girl_sold` 有两个调用点（女孩卖出的两个 UI 入口）；
- `game_saved`/`game_loaded` 无 context 键（调用时不带参数）；
- **当前游戏代码没有调用 `cancel_hook()` 的点**（§4），它由测试覆盖（`game/core/tools/test_runner.rpy:352-353`），供 Mod 作者自行 `call` 使用。

---

## 4. API 速查

全部定义在 `game/core/systems/mods/mod_api_v2.rpy`；另有服务接口抽象 `game/core/systems/services/interfaces/i_mod_service.rpy`。

### Mod 生命周期

| 方法 | 行号 | 说明 |
|------|------|------|
| `register_mod(mod_id, manifest)` | `:50` | 注册 v2 Mod，见 §2.1 |
| `unregister_mod(mod_id)` | `:95` | 移除 Mod 并清理其全部钩子 |
| `is_mod_active(mod_id)` | `:101` | `mod_id in _active_mods` |
| `list_active_mods()` | `:104` | 返回激活 mod_id 列表 |

### UI 集成

| 方法 | 行号 | 说明 |
|------|------|------|
| `get_menu_buttons()` | `:109` | `[(mod_id, 显示名, [按钮 screen 名])]`，仅含声明了主页菜单按钮的 Mod |
| `get_mod_info(mod_id)` | `:121` | manifest 副本（Mods 界面展示用）；未知 id 返回 `None` |

### 钩子

| 方法 | 行号 | 说明 |
|------|------|------|
| `register_hook(hook_name, callback, priority=0)` | `:132` | 注册回调 `callback(context)`；priority 越大越先执行，注册时立即按优先级排序 |
| `execute_hook(hook_name, **context)` | `:143` | 执行该钩子的全部回调；返回 `{mod_id: result}`（返回 `None` 的回调被过滤，mod_id 为 `"_direct"` 表示 `register_hook` 直注册）；回调异常被吞掉并 `renpy.notify`（developer 模式），**永不崩溃游戏** |
| `cancel_hook(hook_name)` | `:161` | 创建 `{"cancel": False}` context 逐个调用回调；任一回调置 `context["cancel"] = True` 则返回 `True`。**不能经由 `execute_hook` 中转**（注释 `:167-173`：`execute_hook` 用 `**kwargs` 重建 context，会丢取消信号——历史 bug 已修复） |

### 其他（继承自 `ModAPI`，`mod_api.rpy`）

`register_trait` / `register_perk` / `register_tag` / `register_dialogue` / `register_event` / `register_ngp_setting` / `register_scenario` / `register_origin` / `register_game_mode`，以及 v1 兼容的 `get_mod_path` / `is_mod_active` / `get_active_mods`（注意后两个操作的是 v1 `detected_mods`）。

### 验证工具

`python tools/verify_mod_api.py` —— 纯 Python 静态断言 + 模拟执行（不依赖 Ren'Py 运行时）：

- 断言 16 个 `HOOK_*` 常量存在且取值唯一（`EXPECTED_HOOK_COUNT = 16`）；
- 断言 `register_mod`/`unregister_mod`/`register_hook`/`execute_hook`/`cancel_hook` 存在；
- 断言 `mod_template.rpy` 引用的每个 `api.HOOK_*` 真实存在；
- 模拟执行注册、重复注册拒绝、未知能力拒绝、优先级排序、异常吞掉、取消流程、`get_menu_buttons`/`get_mod_info` 行为；
- 当前结果：**全部通过**，3 条命名惯例警告（`girl_sold`/`girl_runaway`/`security_event` 无 `_<tense>` 后缀）。

---

## 5. v1 兼容层（HookManager）

`game/core/systems/mods/mod_hooks.rpy`（`init -4 python`）是 Phase 6 的集中钩子分发器，v1 Mod 的 `mod.hooks` dict 在激活时经 `hook_manager.register(...)` 注册（`core_entities.rpy:254-257`）。

- `hook_manager.register(hook_name, callback, mod=None)` / `unregister` / `unregister_mod`；
- `invoke(hook_name, *args, **kwargs)` 返回全部回调结果列表；`invoke_first` 取第一个非 `None` 结果（用于覆盖默认行为）；
- 全局便捷函数 `register_hook(hook_name, callback, mod=None)`（`mod_hooks.rpy:101`）。

注意：这是独立于 v2 `_mod_hooks` 的另一张钩子表，名字相同但存储不同；v2 标准化钩子是 Mod 作者面向未来的接口。

---

## 6. 完整范例：Auction House（权威 v2 范例）

位置：`game/custom/mods/Auction House/`，三个文件分工明确，是模仿 v2 Mod 结构的最佳样本。

### 6.1 `mod.rpy`（44 行）— 注册入口 + 菜单按钮

```renpy
init -1 python:
    services.mod_api_v2.register_mod("auction_house", {
        "name": __("Auction House"),
        "version": "2.0",
        "api_version": 2,
        "min_game_version": "0.3",
        "author": "BK Evolution",
        "description": __("..."),
        "requires": [],
        "hooks": {},
        "dependencies": [],
        "home_rightmenu_add_buttons": ["right_menu_auction"],
    })

screen right_menu_auction():
    hbox xalign 1.0 spacing 20:
        text ""
        textbutton _("Auction") style_group "rm":
            action Show("auction_house")
            tooltip __("访问拍卖行买卖女孩。")
```

讲解：

- **独立注册块**：注册放在单独的 `mod.rpy`，`init -1`（晚于 ModAPIV2 的 `init -3`，保证服务已注册）；
- **mod_id 与文件夹解耦**：`"auction_house"` 是稳定 id，与文件夹名 "Auction House" 无关；
- 该 Mod 无需能力与钩子，`requires`/`hooks`/`dependencies` 都给空值——字段齐全便于扩展；
- `home_rightmenu_add_buttons` 指向同文件定义的 `right_menu_auction` screen：主页右侧菜单 "Mods" 行会通过 `use expression` 嵌入它；按钮样式沿用 `style_group "rm"`（right menu 按钮组）保持观感一致；
- 按钮动作为 `Show("auction_house")`——打开同 Mod 的主界面 screen。

### 6.2 `auction.rpy`（277 行）— 核心业务逻辑

纯 Python（`init -1 python`），与 UI 完全分离。四个类：

| 类 | 职责 |
|----|------|
| `AuctionBid` | 单次出价：`bidder_name`、`amount`、`is_player`、`timestamp` |
| `AuctionLot` | 单个拍品（女孩）：状态机 `pending/active/sold/unsold/cancelled`；`place_bid()` 校验最小加价；`npc_bid()` 按热情度模拟 NPC 出价（上限为女孩买价 ×(0.8+0.7×enthusiasm)）；`finalize()` 结拍返回 `(status, winner, price)` |
| `AuctionSession` | 一场拍卖会：`start_bidding()` 全开拍；`advance_lot()` 逐件结拍；`auto_resolve()` 后台模拟 NPC 竞价全部结拍；`player_buy_lot()` 保留价直购；`player_sell_girl()` 把 MC 队伍女孩挂入拍品 |
| `AuctionHouse` | 持久化全局实例（模块尾 `auction_house = AuctionHouse()`）：`history` 历史、`next_auction_day` + `frequency=30` 排期、`generate_npc_lots()` 从城里生成随机女孩 |

讲解要点：

- **直接复用核心 API**：`girl.get_price("sell"/"buy", raw=True)`、`get_girls(count)`、`MC.gold`/`MC.girls`、`calendar.day`——v2 Mod 与核心代码同进程运行，这些全局可用；
- **所有玩家可见文本包裹 `__()`**，包括状态文字 `get_status_text()` 与 NPC 名字，保证可进翻译系统；
- **模块级全局实例** `auction_house` 即该 Mod 的运行时状态（v2 无 v1 的 `mod_settings` 自动持久化，如需跨存档保存要自行处理，例如借助 `game_saved`/`game_loaded` 钩子）；
- 该文件零 UI、零注册，可被 screen 文件安全 import 引用。

### 6.3 `auction_screens.rpy`（331 行）— UI 层

两个 screen：

- `screen auction_house()`：主界面。`tag menu` + `modal True`；screen 局部变量（`current_session`/`selected_lot`/`bid_amount`）管理交互状态；左栏拍品列表、右栏详情与出价（`-`/`+` 调整、`出价` 按钮 `sensitive` 校验金币与加价、`立即购买` 仅限 NPC 拍品）；底栏 `下一个拍品` / `自动结拍` / `出售我的一个女孩`（`Show("auction_sell_girl", session=current_session)`）/ `关闭`。
- `screen auction_sell_girl(session)`：从 `MC.girls` 选女孩挂拍，`Function(session.player_sell_girl, girl)` 直接调核心逻辑。

讲解要点：

- **通过 `Function(...)` 调 Python 方法**，把 UI 事件桥接到 `auction.rpy` 的类方法；
- 中文界面文本直接写中文并包 `__()`（项目目标语言），展示 v2 Mod 文本同样进翻译系统；
- 迁移修复记录：原 `auction_sell_girl` 引用不存在的全局 `auction_house_session`，移入 Mod 时改为显式传 `session` 参数——Mod 内应避免依赖隐式全局会话状态。

### 6.4 为什么这是权威范例

1. 文件三分法（注册/逻辑/UI）是 v2 Mod 的推荐结构；
2. 展示了 `home_rightmenu_add_buttons` 从 manifest 到 screen 的完整链路；
3. 展示了与核心全局对象（`MC`、`calendar`、`get_girls`）的安全交互；
4. 展示了 v2 与 i18n 规范（`__()`/`_()`）的组合。

对照 v1 教程范例：`game/custom/mods/Goldo's cool mod/goldo's cool mod.rpy`（209 行）演示 v1 全流程——`Mod(...)` 构造、`help_prompts` 选项菜单、`early_label`/`init_label` 标签、`events` + `add_event()` 调度（alarm/morning/city 三种 type）、`set_condition` 条件事件、自定义 `register_trait`、`home_rightmenu_add_buttons` 按钮 screen。

---

## 7. 遗留与已知问题

| 项 | 状态 | 说明 |
|----|------|------|
| v2 `min_game_version` / `dependencies` 校验 | 📝 已知限制 | 仅记录不强制（`mod_api_v2.rpy:50` 注释声明语义） |
| manifest `hooks` 注册优先级恒为 0 | 📝 设计如此 | 需优先级时用 `register_hook(..., priority=N)` 单独注册 |
| `cancel_hook` 无游戏内调用点 | 📝 已知 | 仅测试覆盖；供 Mod/脚本自行调用 |
| 3 个钩子名不符合 `<domain>_<action>_<tense>` | 📝 已知 | `girl_sold` / `girl_runaway` / `security_event`，verify_mod_api 输出警告；改名会破坏已注册回调，保持现状 |
| v2 状态持久化 | 🚧 待规划 | v1 的 `mod_settings` 自动随存档保存；v2 Mod 需自行借助 `game_saved`/`game_loaded` 钩子实现 |
| Mod 内容翻译 | ⏳ 待规划 | `game/custom/` 内容默认保持原文；未来可通过统一字符串表支持 |

---

## 相关文档

- [`CUSTOM_DIRECTORIES.md`](CUSTOM_DIRECTORIES.md) — `game/custom/` 与 `game/core/` 目录边界
- [`../tools/TOOLS.md`](../tools/TOOLS.md) — `tools/verify_mod_api.py` 等工具清单
- [`../../game/core/templates/mod_template/mod_template.rpy`](../../game/core/templates/mod_template/mod_template.rpy) — v2 Mod 空白模板
- [`../../game/custom/mods/Auction House/mod.rpy`](../../game/custom/mods/Auction%20House/mod.rpy) — v2 范例入口
- [`../../game/custom/mods/Goldo's cool mod/goldo's cool mod.rpy`](../../game/custom/mods/Goldo's%20cool%20mod/goldo's%20cool%20mod.rpy) — v1 教程范例
