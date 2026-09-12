# Brothel King — game/core 重构进度文档

> 最后更新: 2026-09-13（物品品质系统 Mod 化后）
> 当前分支: `bk-evolution`

---

## 1. 提交链总览 (59次提交)

```
b09f55e  ── 基线提交 (重构前代码快照)
512040f  ── Phase 0: 紧急修复 (I18N + 性能)
1ef902e  ── Phase 1: 核心架构 (服务容器 + 事件桥)
693682a  ── Phase 2: 女孩组件分解 (9 组件桩)
4b58404  ── Phase 4: I18N 系统 (I18nService)
a471a3c  ── Phase 3: UI 架构 (屏幕目录 + ViewModel)
138a51b  ── Phase 5-6: Mod API v2 + 开发工具
b8eed80  ── 增量: 控制台 UI + 经济委托
8d63053  ── 增量: Mood/Schedule/Stats 委托
ec48c12  ── 增量: Stats/Relationships/Dialogue 委托 + screen_girl_profile
559c217  ── 增量: Traits/Logging 委托 + get_fix_pic 迁移
227c586  ── GirlBase + 10/10 组件完成
027e94f  ── heal/change_energy + estimate_performance 迁移
5a712e2  ── change_love/change_fear 迁移
724695b  ── get_price 迁移
a93e923  ── get_xp/get_jp/get_rep + rest 迁移
138769b  ── generate_traits + pick_dialogue/say/rand_say 迁移
5518f2d  ── GirlSex 组件 + 30 个性行为委托
1b15d4d  ── will_do_sex_act/refresh/activate/deactivate 迁移
cf67f2a  ── generate_personality/adjust/generate_background 迁移
271051a  ── generate_preferences + get_tip 迁移
07772b6  ── get_stat/change_stat/set_stat 迁移
a40d8c4  ── GirlStats 实现体 + GirlTraining 组件 + 双语注释
e76ad4d  ── will_do_farm_act/will_rebel/farm_beg_test 迁移
02e3127  ── brothel/furniture/options 屏幕提取
8ba9ad3  ── 修复3: girl_traits缩进/rand_say残留代码/控制台UI语法
ff33161  ── 修复2: toggle_sex_act残留代码 + text xpadding参数
b3cfcd1  ── 修复3: deactivate_sex_act残留代码删除
eaa368d  ── 修复4: generate_background残旧代码删除 (~35行)
6f13f63  ── 修复5: get_interaction_modifier拼写 -> get_interaction_modifer
58d53d9  ── 修复6: ModAPIV2单例冲突 -> 独立 _instance 变量
45e4086  ── 修复7: mod_template 移除残留的 my_mod.hooks 旧版引用
(WIP)    ── 修复8: matchmaking screen声明行恢复 + 委托残留死代码清理 + generate_background计时返回 + foods->food
a7e4259  ── 修复8提交+基线验证 + 进度文档补记

── Phase 1 (2026-09-10): Girl 组件方法迁移收官 ──
6f7ae3b  ── 块1: obedience/training/run_away checks → GirlTraining
fc306e8  ── 块2: raise/change_preference → GirlSex
d873a42  ── 块3: test_fix/check_fix/get_sex_attitude → GirlSex
5e5094c  ── 块4: list_effects/get_effect/remove_effects → 新建 GirlEffects
d1ea8ae  ── 块5: randomize → 新建 GirlGeneration (GirlBase 委托改接)
773a732  ── 块6: get_pic/get_pic_not_tags → GirlPictures

── Phase 2 (2026-09-10): 屏幕提取收官 (108 screen 全部提取) ──
5a44989  ── 通用组件12个 → screen_common.rpy
6f41b0c  ── 女孩属性7个 → screen_girl_stats.rpy
e459c8d  ── girl_log + previous_night_log → screen_girl_log.rpy
905a0a0  ── autorest/level/perks → screen_progress.rpy
36a81ba  ── farm 4个 → screen_farm.rpy
8831575  ── districts 6个 → screen_districts.rpy
0d46852  ── schedule 3个 → screen_schedule.rpy
ecd2019  ── home/brothel_report → screen_home.rpy
f730004  ── 悬浮层+女孩控件11个 → screen_misc.rpy
22ffe6d  ── 主角/详情面板14个 → screen_misc2.rpy
c61dab4  ── 任务/挑战/互动15个 → screen_quest.rpy
b54f4b0  ── 邪恶力量/卡牌15个 → screen_powers.rpy
1ab8410  ── 资源/成就/契约14个 → screen_resources.rpy + stray归位 + __init__更新

── Phase 3 (2026-09-10): 系统验证与小项收尾 ──
c47440e  ── 任务1: Dev Console Shift+O 绑定修复 (shift_K_o + modal屏幕内补绑)
30674f6  ── 任务2: ModAPIV2.cancel_hook 失效修复 + tools/verify_mod_api.py
315e452  ── 任务3: Test Runner 组件冒烟测试 + bk_test_runner 主菜单入口
4a4a439  ── 任务4: I18N 收尾 — 修复i18n_lint/verify_i18n硬编码旧路径; translate_sync.py决策不实现
1c62fd1  ── 修复: GirlStats.get_stat还原基线语义 (消除效果双倍计入/恢复断言/取整下限)
8828540  ── 拍卖系统提取为Mod: systems/auction → custom/mods/Auction House + update_mods阴影bug修复

── Mod API v2 补完 (2026-09-11) ──
c6b3fa2  ── 16个钩子点接入游戏流程 (girl_*/day_*/night_*/event_*/chapter_*/security/game_saved/game_loaded)
1788c04  ── V2补完+拍卖Mod转V2: manifest菜单按钮/get_menu_buttons/get_mod_info/主页Mods菜单与Mods界面接入v2

── 庭院系统提取为Mod + 翻译治理 (2026-09-11) ──
1eb7f46  ── 修复翻译广播污染: 清空3个机翻导入错误广播句的1730个槽位(回退英文待重译)
5300eb2  ── 清理game/tl: 删孤儿chinese/strings.rpyc与english转储/移机翻工作文件出tl目录
d6e76d6  ── Mod翻译自管理: game/tl/custom/mods → 各Mod目录tl/chinese_simplified/ (TRANSLATION_GUIDE重写)
6384837  ── 修复庭院屏幕崩溃: 文本插值[len()]/[get_daily_upkeep()]改screen python预计算
待提交  ── 庭院系统提取为"Courtyard" Mod: systems/courtyard → custom/mods/Courtyard,
           新增2个v2钩子(girl_destination_list/accept, 18个总数), 收购流程菜单动态化,
           day_ending接线激活process_day()(原死代码), 翻译随迁Mod目录

── 游戏模式提取为Mod (2026-09-11) ──
待提交  ── 游戏模式提取为"Game Modes" Mod: systems/gamemodes 三模式实现+选择屏幕 →
           custom/mods/Game Modes, 框架(GameMode基类+注册表)留本体, 模式卡片改注册表驱动,
           start.rpy 按 renpy.has_screen 检测+Mod缺席兜底默认剧情模式,
           is_story_mode() None安全修复(旧存档默认剧情), 翻译随迁Mod目录

── Mod API v2 持久化启用 (2026-09-11) ──
待提交  ── v2 Mod 持久化启用机制: 开关存 persistent._bk_v2_mod_states(未记录默认启用),
           激活=已注册∧(always_on∨持久化启用)∧dependencies全激活(拓扑重建, 依赖缺失/未安装即失活),
           register_mod init期即读persistent(Ren'Py 在init前绑定), apply_startup_states 在
           before_main_menu 幂等兜底; execute_hook/cancel_hook 跳过未激活Mod回调;
           新增主菜单 Mod 管理界面 screen_mod_manager.rpy (名称/版本/作者/状态/切换/重启提示,
           主菜单Mods按钮改 Show("mod_manager")), Game Modes manifest 加 always_on:False 并
           以 is_mod_active 守卫模式注册(被禁用即回退纯剧情模式) + README.txt 前置依赖范例;
           verify_mod_api 增补持久化开关/依赖/always_on 断言

── Phase 7: Girl 组件化收官 (2026-09-11, 批次1-14, girlclass 3,910→1,148 行) ──
ac412bb  ── 批次1: mood/energy/health 实现迁入 GirlMood (sanity_warning 6分支完整版替换组件
           过时3分支副本/tire/get_hurt/health_check/get_energy_color/ttip/tired_check/
           update_mood/change_mood/get_mood_modifier/get_mood_description/get_mood_picture)
           (ROADMAP 遗留#5 收尾) —— 注: 本批 get_mood_description 只换了尾部, 135行孤儿体
           遗留至批次14a 清理
12df2ff  ── 批次2: 日志/追踪/记忆实现迁入 GirlLogging (commit/return_from/add_log/get_log/
           get_average_performance/track_event/get_recent_events×2/count_occurences/
           will_remember/remembers/forgets 共12方法)
d2f2b0b  ── 批次3: 性格描述/NGP解锁/is_/test_say/unlock_info 迁入 GirlDialogue
           (get_personality_description 240行; is_ 判归 GirlDialogue——只读 personality.attributes)
4accc78  ── 批次4: upkeep簇9方法+接待互动4方法+whore_on_street/get_street_tip 迁入 GirlEconomy
           (+顺手清理6个指向已迁移方法的遗留别名)
52d97f7  ── 批次5: receive_gift/update_relationships/change_relationship/get_compatibility/
           get_friendship/get_MC_relation/meet_MC/get_love/get_fear/spoil/terrify/
           refresh_spoil_terrify_points 迁入 GirlRelationships (girl_items 调用点改接)
7932658  ── 批次6: 新建 girl_progression.rpy (483行, 28方法) — level_up/rank_up/job_up/
           adjust_level/auto_level_up/debug_auto_level/ready_to_*/can_spend_upgrade_points/
           change_xp/change_jp/change_rep/get_*_can/perk簇9/属性升级3; __init__注册+
           Girl.__init__ self._progression
29eaa27  ── 批次7: set_job/will_do/set_rest/works_today/cycle_workday/set_workdays/load_schedule/
           get_day_off 迁入 GirlSchedule
87050c6  ── 批次8: generate_preferences(内外层合并)/add_random_fixation/remove_fixation/
           try_to_remove_fix/has_fixation/test_weakness/pop_virginity/restore_virginity/
           talk_tastes/get_preference/get_preference_bonus/reset_sex_acts/get_trainable_sex_acts/
           get_sex_act_modifier/count_available_sex_acts/does_anything/will_do_anything/
           has_activated_sex_acts/get_reaction_to_act 共19方法迁入 GirlSex
           —— 注: 本批引入 generate_preferences 双重执行bug(girlclass 外层包装未缩壳), 批次14a 修复
80ed767  ── 批次9: will_rebel_in_farm/farm_beg_test/get_obedience_check_target/get_working_chance/
           get_training_chance/build_up/get_build_up/reset_build_up 迁入 GirlTraining
           + 删除 will_rebel_in_farm/farm_beg_test 重复定义死壳(组件 farm_beg_test 过时副本
           阈值相反, 以girlclass为准覆盖)
49bfca4  ── 批次10: stat_spillover/get_stat_minmax/shuffle_skills/generate_stats/test_stats/
           raise_stats/average_stats 迁入 GirlStats —— 组件5行简化版 get_stat_minmax 被63行
           基线版覆盖, 修复 change_stat 技能上限回归(恢复 max(rank*50+...)), stat_spillover 遮蔽5处
2d0e192  ── 批次11: add_trait/remove_trait/has_trait/get_defense/add_shield/test_shield 迁入 GirlTraits
08b09d0  ── 批次12: use_item/unequip/take/get_equipped 迁入 GirlItems (use_item 组件旧简易版/
           take/get_equipped 旧版全部以girlclass为准覆盖)
85ffd84  ── 批次13: set_name/set_fullname/random_rename/load_ini/read_ini/update_files 迁入 GirlBase
           (girl_pictures 的 update_files 静态占位删除, help.rpy 调用点路由不变)
f027957  ── 批次14a: 修复批次8双重执行bug(generate_preferences 纯壳化) + 批次1孤儿体清理
           (get_mood_description 135行死链) + 补迁 has_perk→GirlTraits/
           customer_populations_safety_check→GirlEconomy/init_after_acquire→GirlBase
           + 清7死别名 + __init__.rpy 头部更新(16组件全★表)
```

**基线验证 (2026-09-10 会话)**: lint 通过（仅历史警告），游戏可正常启动至主菜单。
注意: `generate_background` 返回 `time.perf_counter()` 是**有意设计**——`Girl.__init__` 的性能计时埋点 (`t3 = self.generate_background(t2)`) 依赖该返回值。

**基准提交**: `b09f55e — 基线提交: game/core 重构前基准`

---

## 2. 核心架构 (Phase 1)

### GameServices 服务容器
**文件**: `game/core/systems/services/service_container.rpy`
**Init 级别**: -12 (最先加载)

已注册的服务:
| 服务 | 注册 key | 注册位置 | 说明 |
|------|----------|----------|------|
| Config | `config` | game_config.rpy | 集中配置 |
| GirlFilesDict | `girl_files_dict` | girl_files_dict.rpy | 女孩文件管理 |
| Game | `game` | start.rpy | 游戏实例 |
| Calendar | `calendar` | start.rpy | 日历 |
| MC | `mc` | start.rpy | 主角 |
| Farm | `farm` | start.rpy | 农场 |
| Brothel | `brothel` | events_dispatcher.rpy | 青楼 |
| EventEngine | `event_engine` | event_engine.rpy | 事件引擎 |
| I18nService | `i18n` | i18n_service.rpy | 翻译服务 |
| DevConsole | `dev_console` | console_commands.rpy | 调试控制台 |
| ModAPI v2 | `mod_api_v2` | mod_api_v2.rpy | Mod 接口 |

### 事件桥 (EventBridge)
**文件**: `game/core/systems/events/event_bridge.rpy`
**作用**: 同步旧 `city_events`/`daily_events` 和新 EventEngine

### 配置集中化 (GameConfig)
**文件**: `game/core/config/game_config.rpy`
**支持**: `custom/config/` JSON 覆盖

---

## 3. 女孩系统重构 (Phase 2 + Phase 7)

### girlclass.rpy 瘦身

| 指标 | 重构前 | Phase 2 后 | Phase 7 后 | 累计变化 |
|------|--------|-----------|-----------|---------|
| 行数 | 5,900 | 3,910 | **1,148** | **-4,752 (-81%)** |
| 方法数 | 212 | 211 | ~212 (绝大多数为一行委托壳) | — |
| 组件目录 | 无 | 15 文件 | 16 文件 +2,682→+5,618 行 | |

### 女孩组件 (16 个，14 个含迁移实现)

明细以 [../architecture/girl_components.md](../architecture/girl_components.md) 为真源（含每组件行数、★状态、Phase 7 批次映射）。Phase 7 新增 `girl_progression.rpy`（等级/XP-JP-rep/Perk/属性升级，28 方法）。

### 方法体迁移汇总

- Phase 2：33 个大块方法（stats/mood/economy/sex/dialogue/traits/items/schedule/training/effects/generation/pictures/relationships），明细见上文历史提交链
- Phase 7 批次1-14：再迁移 ~120 个方法，girlclass 仅剩 `__init__`(142行) + 委托壳 + 24 个活别名；同时修复 generate_preferences 双重执行、change_stat 技能上限回归两个事故，清理组件内 6 处过时副本、删除 3 处重复定义死壳

### 仍在 girlclass 中的内容（Phase 7 后，有意保留）

| 内容 | 行数 | 说明 |
|------|------|------|
| `__init__` | 142 | 属性初始化 + 16 组件实例化；**有意保持原样**（拆到各组件 init_* 有存档兼容风险，ROADMAP #3 暂缓） |
| `get_schedule` / `is_unique` | ~7 | 微方法，连同其活 `_impl` 别名保留 |
| 委托壳 | ~212 方法各 1-2 行 | Girl 公共 API，2,000+ 旧调用点零改动 |
| `_impl` 别名 | 24 | 仅指向真实现仍在 girlclass 的方法 |

### Phase 2 方法体迁移明细 (33 个，历史存档)

> Phase 7 已全部收尾，此为 Phase 2 时期的明细记录：

1. `get_fix_pic` (~112行) → girl_pictures
2. `get_status` + `get_status_summary` (~111行) → girl_schedule
3. `get_price` (~42行) → girl_economy
4. `change_energy` + `heal` + `full_rest` (~46行) → girl_mood
5. `estimate_performance` (~17行) → girl_economy
6. `change_love` + `change_fear` (~83行) → girl_relationships
7. `get_xp` + `get_jp` + `get_rep` (~88行) → girl_economy
8. `rest` (~57行) → girl_mood
9. `generate_traits` (~180行) → girl_traits
10. `pick_dialogue` + `say` + `rand_say` (~120行) → girl_dialogue
11. `will_do_sex_act` + `toggle_sex_act` (~42行) → girl_sex
12. `refresh_sex_acts` + `activate/deactivate` (~22行) → girl_sex
13. `generate_personality` + `adjust_personality` (~72行) → girl_dialogue
14. `generate_background` (~80行) → girl_dialogue
15. `generate_preferences` (~160行) → girl_sex
16. `get_tip` (~145行) → girl_economy
17. `get_stat` (~20行) → girl_stats
18. `change_stat` (~80行) → girl_stats
19. `set_stat` (~5行) → girl_stats
20. `average_skills` (~15行) → girl_stats
21-25. 理智值方法 (~40行) → girl_mood
26-30. 物品方法 (equip/unequip/use_item/take) → girl_items
31-33. 农场方法 (will_do_farm_act/will_rebel/farm_beg_test) → girl_training

---

## 4. I18N 系统 (Phase 4)

### I18nService
**文件**: `game/core/systems/services/i18n_service.rpy`
**API**:
- `t(text)` — 翻译字符串 (≈ `__()`)
- `tn(n, singular, plural)` — 复数翻译
- `tc(text, context)` — 上下文翻译 (pgettext)
- `pronoun(gender, form)` — 多语言代词
- `possessive(name)` — 所有格

### 语言扩展
**文件**: `game/core/config/translations.rpy`
**支持**: 通过 `custom/config/languages.json` 添加新语言

### 已修复的 I18N 问题
- `plural()` / `article()` — 英文外返回空/原词
- 日均报告 `get_day_report()` — 全部 ~60 行用 `__()` 包裹
- UI tooltip 字符串拼接 → `__()` 模板 (9+ 处)
- 全 15 个组件文件头部中英双语注释

---

## 5. Mod API v2 (Phase 5)

**文件**: `game/core/systems/mods/mod_api_v2.rpy`

### 特性
- 版本化 API: `api_version = 2`
- 能力标记: `requires = ["girl_traits", "events", "items", ...]`
- 19 个标准化钩子点 (HOOK_GIRL_GENERATED, HOOK_DAY_STARTING, HOOK_ITEM_GENERATED 等)
- 钩子取消支持 (`cancel_hook`)
- 本版不兼容旧 Mod (需求要求)
- ✅ **钩子已接线** (2026-09-11, c6b3fa2): 全部钩子点已接入游戏流程
  （日/夜循环、女孩生成/获得/出售/逃跑、事件、章节、安保、存档/读档），纯通知型
- ✅ **UI 集成** (2026-09-11, 1788c04): manifest 支持 `home_rightmenu_add_buttons`
  （主页右侧菜单按钮）；`get_menu_buttons()` / `get_mod_info()` 供 UI 查询；
  Mods 界面展示 v2 Mod（常驻激活，只读）；重复注册被拒绝
- ⚠️ **v2 Mod 语义**: 安装即常驻激活，无逐存档开关（与 v1 不同）；停用需移除文件

### 模板更新
**文件**: `game/core/templates/mod_template/mod_template.rpy`
- 展示 v2 模式 (register_mod + 钩子注册)

### 物品品质系统 Mod 化 (2026-09-13)

物品系统重构第一任务：把模板物品的 0-6 档品质系统提取为独立 v2 Mod，遵循 "框架留 core、数据进 Mod、core 留兜底" 的 Game Modes 先例。

- **core 框架**（新）: `systems/registry/quality_registry.rpy`（init -5）——`QualityTier`（前缀/价格乘数/稀有度提升/效果缩放）+ `QualityRegistry`（`register_quality`/`get_tier`/`get_tiers`/`get_max_rank`）；
- **core 兜底**（新）: `data/quality.rpy`（init -4）——原 `settings/quality.json` 的 7 档数据逐字硬编码，**勿删**；
- **新 Mod**: `custom/mods/Item Quality/`（mod_id `item_quality`）——`mod.rpy`（注册 + `is_mod_active` 门控）+ `quality.rpy`（init -9 定义、读自带 `quality.json`）+ `tl/chinese_simplified/`（Mod 自管翻译）+ `README.txt`；
- **API 扩展**: CAPABILITIES 加 `"items"`；新增 `HOOK_ITEM_GENERATED = "item_generated"`（第 19 个钩子，纯通知型，context `{item, template, tier}`）；v1 基类加 `register_quality`；
- **items.rpy 重构**: `generate_new_item` / `transform_template` / `init_items` 改走注册表，行为逐位等价（522 例对拍全等）；
- **删除旧路径**: `DataLoader.load_quality()`、`variables.rpy` 全局加载块、`data/settings/quality.json`；
- **翻译迁移**: 31 条前缀词条从 `tl/chinese_simplified/strings.rpy` 移入 Mod 自有 `tl/`（core 保留 Fine/Broken/Medium/Cheap 等共用词条）；
- **验证**: `tools/verify_mod_api.py` 19/19 钩子通过；三方数据对拍全等；522 例生成结果对拍全等；空注册表边界返回 None 不崩溃。

---

## 6. 开发工具 (Phase 6)

### Dev Console
**后端**: `game/core/tools/dev_console/console_commands.rpy`
**前端**: `game/core/tools/dev_console/screen_console.rpy`

**命令**:
- `help` — 显示帮助
- `girls [brothel/market/free/farm]` — 列出女孩
- `gold <amount>` — 加钱
- `stats` — 显示状态
- `event <label>` — 触发事件
- `heal` — 治疗全部
- `repair` — 运行 AutoRepair
- `services` — 列出已注册服务
- Python 表达式直接执行

**快捷键**: Shift+O (仅在 developer mode)

### Girl Pack Editor
**文件**: `game/core/tools/girl_pack_editor/pack_editor_state.rpy`
- 浏览/创建/验证 女孩包

### Test Runner
**文件**: `game/core/tools/test_runner.rpy`
- assert_eq/assert_true/assert_contains/assert_not_none/skip
- 组件冒烟测试: GirlStats/GirlMood/GirlEconomy/GirlEffects (桩 Girl) + ModAPIV2
- 入口: `label bk_test_runner`，主菜单 Tests 按钮（仅 developer mode）

---

## 7. 屏幕提取 (Phase 3) ✅ 已完成 (2026-09-10)

### 进度

| 原文件 | 状态 | 行数 |
|--------|------|------|
| `screens.rpy` | ✅ 全部提取完毕，仅剩 image/style 声明、label 块 (girlpack_menu/pic_test/packstates_menu) 与占位注释 | 8,886 → **620** |

**108 个 screen 全部提取至 `game/core/ui/screens/`（16 个文件）**，经 `temp/verify_extract.py` 与基线 773a732 逐字比对一致：

| 新文件 | 行数 | 内容 |
|--------|------|------|
| `screen_common.rpy` | 695 | tool/overlay/quick_start/dark_filter/yes_no/OK_screen/show_img/show_event/show_sex_event/shortcuts/close/receive_item 等 12 个通用组件 |
| `screen_girl_stats.rpy` | 1,096 | girl_stats/girl_stats_light/assign_job/stat_bar/custom_bar/trait_details/perk_details |
| `screen_girl_log.rpy` | 336 | girl_log + previous_night_log |
| `screen_progress.rpy` | 250 | autorest/level/perks |
| `screen_farm.rpy` | 604 | farm_menu/farm_tab/minion_button/fshow_init |
| `screen_districts.rpy` | 678 | districts/district_button/visit_district/visit_location/matchmaking/customer_satisfaction |
| `screen_schedule.rpy` | 214 | schedule/save_schedule/load_schedule |
| `screen_home.rpy` | 149 | home/brothel_report |
| `screen_misc.rpy` | 1,306 | 悬浮层+女孩控件 11 个 |
| `screen_misc2.rpy` | 628 | 主角/详情面板 14 个 |
| `screen_quest.rpy` | 1,120 | 任务/挑战/互动 15 个 |
| `screen_powers.rpy` | 638 | 邪恶力量/卡牌 15 个 |
| `screen_resources.rpy` | 627 | 资源/成就/契约 14 个 |
| (早前已有) | — | screen_girl_list / screen_girl_profile / screen_brothel |

全部 `use`/`call screen` 按名解析，未改任何调用点。

---

## 8. 文件变更统计

### 新建文件 (35+)

```
game/core/
  config/game_config.rpy              — 集中配置
  init/dependency_graph.rpy           — Init 依赖图
  systems/services/service_container.rpy — 服务容器
  systems/services/i18n_service.rpy     — 翻译服务
  systems/events/event_bridge.rpy       — 事件桥
  systems/mods/mod_api_v2.rpy           — Mod API v2
  framework/picture_cache.rpy           — 图片缓存
  framework/girl/ (17 个文件)           — 女孩组件
  tools/dev_console/console_commands.rpy — 控制台命令
  tools/dev_console/screen_console.rpy  — 控制台界面
  tools/girl_pack_editor/*.rpy         — 女孩包编辑器
  tools/test_runner.rpy                 — 测试框架 (+bk_test_runner 入口/主菜单 Tests 按钮)
  ui/screens/ (16 个文件)              — 全部提取的屏幕 (108 screen)
  ui/view_models/*.rpy                — ViewModel 层
tools/
  verify_mod_api.py                   — Mod API v2 验证脚本
```

### 主要修改文件

| 文件 | 变化 |
|------|------|
| `girlclass.rpy` | 5,900 → 3,910 行 (-1,990, -34%) |
| `girl_files_dict.rpy` | 倒排索引 + 惰性加载 |
| `screens.rpy` | 9,500 → 620 行 (-8,866, 108 screen 全部提取) |
| `picture.rpy` | 惰性标签解析 |
| `utils.rpy` | plural/article 语言感知 |
| `effects.rpy` | LRU 图片缓存 |
| `endday.rpy` | I18N 修复 |
| `core_entities.rpy` | AutoRepair 降频 |
| `start.rpy` | 服务注册 |

---

## 9. 下一步优先事项

1. **验证测试** — ✅ 部分完成 (2026-09-10): lint 通过 + 启动至主菜单正常；**待人工抽查**: 新游戏开档、一天结算、女孩面板/青楼/农场界面；**Phase 3 增量**: 主菜单 Tests 按钮（developer mode）可运行组件冒烟测试
2. **剩余方法迁移** — ✅ 全部完成 (Phase 7, 2026-09-11): 批次1-14 迁移 ~120 方法、新建 GirlProgression、修复 generate_preferences 双重执行与 change_stat 上限回归、清 6 处过时副本与 3 处死壳。**girlclass.rpy 5,900→1,148 行**。唯一遗留: `__init__` 拆分（暂缓，存档兼容风险）、`get_schedule`/`is_unique` 微方法（有意保留）
3. **屏幕提取** — ✅ 全部完成 (Phase 2, 2026-09-10): screens.rpy 8,886 → 620 行，108 screen → 16 个文件，逐字比对验证一致
4. **翻译工具** — ✅ 已决策不实现 `translate_sync.py` (Phase 3): 同步需求由现有工具链覆盖——缺失检测 `verify_i18n.py`(`translate --count`)、占位符完整性 `audit_placeholders.py`、空翻译往返 `export_empty_to_xlsx.py`/`import_translated_empty.py`、陈旧条目由 Ren'Py `translate` 重写时清理。详见 `docs/i18n/I18N_ROADMAP.md` 第 6 节。另修复 `i18n_lint.py`/`verify_i18n.py` 硬编码旧路径（改为按脚本位置推导项目根）。
5. **Mod API v2 测试** — ✅ 已完成 (Phase 3): `tools/verify_mod_api.py` 静态断言 + 桩环境全流程模拟（注册→触发→取消），`python tools/verify_mod_api.py` 全过；游戏内 `test_mod_api_v2` 冒烟 label 同步加入 Test Runner。**发现并修复**: `cancel_hook` 经 `execute_hook` 中转导致 context 永不达回调、永远返回 False。现状（2026-09-13）: 19 个 HOOK_* 常量全部接线，游戏代码有多处 `execute_hook` 调用点（`items.rpy` 的 `item_generated` 等）；`cancel_hook` 仍无游戏内调用点。
6. **Dev Console 快捷键** — ✅ 已修复 (Phase 3, c47440e): 根因有二——①keymap 绑定的是无修饰键 `K_o`（应为 `shift_K_o`）；②console screen 为 `modal True`，modal 阻断下层事件，underlay Keymap 在控制台显示期间收不到按键，无法关闭。修复：underlay 负责全局打开，屏幕内 `key "shift_K_o"` 负责关闭，输入框聚焦时忽略切换（避免输入大写 O 误关）。

---

## 10. 关键约定

### 代码规范
- 所有新代码中英双语注释
- 组件类通过 `self.girl` 访问 Girl 实例
- 方法体迁移模式: 实现放在组件 → Girl 类委托
- `_impl` 别名: 已迁移的可以删除，未迁移的保留

### Init 优先级
```
init -12   service_container  ── GameServices
init -11   game_config       ── GameConfig
init -10   settings/translations
init -9    mod definitions    ── Mod 自有类/函数定义（如 Item Quality 的 load_quality_tiers）
init -5    registry           ── 各种 Registry（含 QualityRegistry）
init -4    variables          ── 全局变量 + 硬编码 fallback（含 data/quality.rpy）
init -3    utils/effects      ── 工具函数（含 ModAPIV2 定义）
init -2    class definitions  ── 所有类定义 + 组件
init -1    mods               ── v2 Mod 注册入口（register_mod + is_mod_active 门控）
init       start label        ── 游戏实例创建
```

### 服务访问
```python
services.game       # Game 实例
services.mc         # Main 主角
services.brothel    # Brothel 青楼
services.farm       # Farm 农场
services.calendar   # Calendar 日历
services.i18n       # I18nService 翻译
services.config     # GameConfig 配置
services.mod_api_v2 # Mod API v2
services.dev_console # Dev Console
```
