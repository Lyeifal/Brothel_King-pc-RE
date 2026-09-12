# Brothel King — game/core Refactoring Progress Document

> Last updated: 2026-09-13 (after the Item Quality system was moved into a mod)
> Current branch: `bk-evolution`

---

## 1. Commit chain overview (59 commits)

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

── Phase 7 (2026-09-11, batches 1-14, girlclass 3,910→1,148 lines): Girl component migration completion ──
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

**Baseline verification (2026-09-10 session)**: lint passes (historical warnings only), the game launches normally to the main menu.
Note: `generate_background` returning `time.perf_counter()` is **intentional** — the performance timing instrumentation in `Girl.__init__` (`t3 = self.generate_background(t2)`) relies on that return value.

**Baseline commit**: `b09f55e — 基线提交: game/core 重构前基准`

---

## 2. Core architecture (Phase 1)

### GameServices service container
**File**: `game/core/systems/services/service_container.rpy`
**Init level**: -12 (loads first)

Registered services:
| Service | Registration key | Registration location | Description |
|------|----------|----------|------|
| Config | `config` | game_config.rpy | Centralized configuration |
| GirlFilesDict | `girl_files_dict` | girl_files_dict.rpy | Girl file management |
| Game | `game` | start.rpy | Game instance |
| Calendar | `calendar` | start.rpy | Calendar |
| MC | `mc` | start.rpy | Main character |
| Farm | `farm` | start.rpy | Farm |
| Brothel | `brothel` | events_dispatcher.rpy | Brothel |
| EventEngine | `event_engine` | event_engine.rpy | Event engine |
| I18nService | `i18n` | i18n_service.rpy | Translation service |
| DevConsole | `dev_console` | console_commands.rpy | Debug console |
| ModAPI v2 | `mod_api_v2` | mod_api_v2.rpy | Mod API |

### Event bridge (EventBridge)
**File**: `game/core/systems/events/event_bridge.rpy`
**Purpose**: synchronizes the legacy `city_events`/`daily_events` with the new EventEngine

### Configuration centralization (GameConfig)
**File**: `game/core/config/game_config.rpy`
**Supports**: JSON overrides via `custom/config/`

---

## 3. Girl system refactoring (Phase 2 + Phase 7)

### girlclass.rpy slimming

| Metric | Before | After Phase 2 | After Phase 7 | Cumulative change |
|------|--------|------|------|------|
| Lines | 5,900 | 3,910 | **1,148** | **-4,752 (-81%)** |
| Method count | 212 | 211 | ~212 (almost all one-line delegation shells) | — |
| Component directory | None | 15 files | 16 files, +2,682→+5,618 lines | |

### Girl components (16, 14 with migrated implementations)

Details live in [../architecture/girl_components.md](../architecture/girl_components.md) as the source of truth (per-component lines, ★ status, Phase 7 batch mapping). Phase 7 added `girl_progression.rpy` (level/XP-JP-rep/Perks/stat upgrades, 28 methods).

### Method body migration summary

- Phase 2: 33 large block methods (stats/mood/economy/sex/dialogue/traits/items/schedule/training/effects/generation/pictures/relationships); see the historical commit chain above
- Phase 7 batches 1-14: another ~120 methods migrated; girlclass left with only `__init__` (142 lines) + delegation shells + 24 live aliases; also fixed two incidents (generate_preferences double execution, change_stat skill cap regression), cleaned up 6 stale copies inside components, deleted 3 duplicate-definition dead shells

### Still in girlclass (after Phase 7, intentionally retained)

| Content | Lines | Notes |
|------|------|------|
| `__init__` | 142 | Attribute initialization + 16 component instantiations; **intentionally left as-is** (splitting into per-component init_* carries save-compatibility risk, deferred per ROADMAP #3) |
| `get_schedule` / `is_unique` | ~7 | Micro-methods, kept together with their live `_impl` aliases |
| Delegation shells | ~212 methods, 1-2 lines each | The Girl public API; 2,000+ existing call sites unchanged |
| `_impl` aliases | 24 | Only pointing at methods whose real implementation still lives in girlclass |

### Phase 2 method migration detail (33 items, archived)

> Phase 7 completed all remaining items; this is the Phase 2 record:

1. `get_fix_pic` (~112 lines) → girl_pictures
2. `get_status` + `get_status_summary` (~111 lines) → girl_schedule
3. `get_price` (~42 lines) → girl_economy
4. `change_energy` + `heal` + `full_rest` (~46 lines) → girl_mood
5. `estimate_performance` (~17 lines) → girl_economy
6. `change_love` + `change_fear` (~83 lines) → girl_relationships
7. `get_xp` + `get_jp` + `get_rep` (~88 lines) → girl_economy
8. `rest` (~57 lines) → girl_mood
9. `generate_traits` (~180 lines) → girl_traits
10. `pick_dialogue` + `say` + `rand_say` (~120 lines) → girl_dialogue
11. `will_do_sex_act` + `toggle_sex_act` (~42 lines) → girl_sex
12. `refresh_sex_acts` + `activate/deactivate` (~22 lines) → girl_sex
13. `generate_personality` + `adjust_personality` (~72 lines) → girl_dialogue
14. `generate_background` (~80 lines) → girl_dialogue
15. `generate_preferences` (~160 lines) → girl_sex
16. `get_tip` (~145 lines) → girl_economy
17. `get_stat` (~20 lines) → girl_stats
18. `change_stat` (~80 lines) → girl_stats
19. `set_stat` (~5 lines) → girl_stats
20. `average_skills` (~15 lines) → girl_stats
21-25. sanity methods (~40 lines) → girl_mood
26-30. item methods (equip/unequip/use_item/take) → girl_items
31-33. farm methods (will_do_farm_act/will_rebel/farm_beg_test) → girl_training

---

## 4. I18N system (Phase 4)

### I18nService
**File**: `game/core/systems/services/i18n_service.rpy`
**API**:
- `t(text)` — translate string (≈ `__()`)
- `tn(n, singular, plural)` — plural translation
- `tc(text, context)` — context translation (pgettext)
- `pronoun(gender, form)` — multilingual pronouns
- `possessive(name)` — possessive form

### Language extensions
**File**: `game/core/config/translations.rpy`
**Supports**: adding new languages via `custom/config/languages.json`

### Fixed I18N issues
- `plural()` / `article()` — return empty/original word outside English
- Daily report `get_day_report()` — all ~60 lines wrapped with `__()`
- UI tooltip string concatenation → `__()` templates (9+ sites)
- Bilingual (Chinese-English) header comments on all 15 component files

---

## 5. Mod API v2 (Phase 5)

**File**: `game/core/systems/mods/mod_api_v2.rpy`

### Features
- Versioned API: `api_version = 2`
- Capability flags: `requires = ["girl_traits", "events", "items", ...]`
- 19 standardized hook points (HOOK_GIRL_GENERATED, HOOK_DAY_STARTING, HOOK_ITEM_GENERATED, etc.)
- Hook cancel support (`cancel_hook`)
- This version is incompatible with old mods (by requirement)
- ✅ **Hooks wired** (2026-09-11, c6b3fa2): all hook points connected to the game flow
  (day/night cycle, girl generated/acquired/sold/runaway, events, chapters, security, save/load), notification-only
- ✅ **UI integration** (2026-09-11, 1788c04): manifest supports `home_rightmenu_add_buttons`
  (home right-menu buttons); `get_menu_buttons()` / `get_mod_info()` for UI queries;
  Mods screen displays v2 mods (read-only list); duplicate registration rejected
- ⚠️ **v2 mod semantics**: active as soon as installed; enable/disable is toggled in the main-menu Mod Manager screen and stored in `persistent._bk_v2_mod_states` (takes full effect after a restart); `always_on: True` mods cannot be disabled

### Template update
**File**: `game/core/templates/mod_template/mod_template.rpy`
- Demonstrates the v2 pattern (register_mod + hook registration)

### Item Quality system moved into a mod (2026-09-13)

First task of the item-system refactor: extract the 0-6 quality tiers of template items into a standalone v2 mod, following the "framework stays in core, data moves into the mod, core keeps a fallback" precedent set by Game Modes.

- **Core framework** (new): `systems/registry/quality_registry.rpy` (init -5) — `QualityTier` (prefixes / price modifier / rarity bump / effect scaling) + `QualityRegistry` (`register_quality`/`get_tier`/`get_tiers`/`get_max_rank`);
- **Core fallback** (new): `data/quality.rpy` (init -4) — the 7 tiers of the former `settings/quality.json`, hardcoded verbatim; **do not delete**;
- **New mod**: `custom/mods/Item Quality/` (mod_id `item_quality`) — `mod.rpy` (registration + `is_mod_active` gating) + `quality.rpy` (definitions at init -9, reads its own `quality.json`) + `tl/chinese_simplified/` (mod-owned translations) + `README.txt`;
- **API extensions**: CAPABILITIES gained `"items"`; new `HOOK_ITEM_GENERATED = "item_generated"` (the 19th hook, notification-only, context `{item, template, tier}`); v1 base class gained `register_quality`;
- **items.rpy refactor**: `generate_new_item` / `transform_template` / `init_items` now go through the registry, bit-for-bit behaviour-preserving (522 cases compared, all equal);
- **Old paths deleted**: `DataLoader.load_quality()`, the globals block in `variables.rpy`, `data/settings/quality.json`;
- **Translation migration**: 31 prefix entries moved from `tl/chinese_simplified/strings.rpy` into the mod's own `tl/` (core kept the shared entries Fine/Broken/Medium/Cheap);
- **Verification**: `tools/verify_mod_api.py` passes 19/19 hooks; three-way data comparison all equal; 522-case generation parity all equal; the empty-registry edge case returns None without crashing.

---

## 6. Dev tools (Phase 6)

### Dev Console
**Backend**: `game/core/tools/dev_console/console_commands.rpy`
**Frontend**: `game/core/tools/dev_console/screen_console.rpy`

**Commands**:
- `help` — show help
- `girls [brothel/market/free/farm]` — list girls
- `gold <amount>` — add gold
- `stats` — show stats
- `event <label>` — trigger event
- `heal` — heal everyone
- `repair` — run AutoRepair
- `services` — list registered services
- Python expressions executed directly

**Hotkey**: Shift+O (developer mode only)

### Girl Pack Editor
**File**: `game/core/tools/girl_pack_editor/pack_editor_state.rpy`
- Browse/create/validate girl packs

### Test Runner
**File**: `game/core/tools/test_runner.rpy`
- assert_eq/assert_true/assert_contains/assert_not_none/skip
- Component smoke tests: GirlStats/GirlMood/GirlEconomy/GirlEffects (stub Girl) + ModAPIV2
- Entry: `label bk_test_runner`, main-menu Tests button (developer mode only)

---

## 7. Screen extraction (Phase 3) ✅ Completed (2026-09-10)

### Progress

| Original file | Status | Lines |
|--------|------|------|
| `screens.rpy` | ✅ fully extracted; only image/style declarations, label blocks (girlpack_menu/pic_test/packstates_menu), and placeholder comments remain | 8,886 → **620** |

**All 108 screens extracted to `game/core/ui/screens/` (16 files)**, verified character-for-character identical against baseline 773a732 via `temp/verify_extract.py`:

| New file | Lines | Content |
|--------|------|------|
| `screen_common.rpy` | 695 | 12 common components: tool/overlay/quick_start/dark_filter/yes_no/OK_screen/show_img/show_event/show_sex_event/shortcuts/close/receive_item, etc. |
| `screen_girl_stats.rpy` | 1,096 | girl_stats/girl_stats_light/assign_job/stat_bar/custom_bar/trait_details/perk_details |
| `screen_girl_log.rpy` | 336 | girl_log + previous_night_log |
| `screen_progress.rpy` | 250 | autorest/level/perks |
| `screen_farm.rpy` | 604 | farm_menu/farm_tab/minion_button/fshow_init |
| `screen_districts.rpy` | 678 | districts/district_button/visit_district/visit_location/matchmaking/customer_satisfaction |
| `screen_schedule.rpy` | 214 | schedule/save_schedule/load_schedule |
| `screen_home.rpy` | 149 | home/brothel_report |
| `screen_misc.rpy` | 1,306 | overlay + girl widgets, 11 screens |
| `screen_misc2.rpy` | 628 | MC/detail panels, 14 screens |
| `screen_quest.rpy` | 1,120 | quests/challenges/interactions, 15 screens |
| `screen_powers.rpy` | 638 | evil powers/cards, 15 screens |
| `screen_resources.rpy` | 627 | resources/achievements/contracts, 14 screens |
| (pre-existing) | — | screen_girl_list / screen_girl_profile / screen_brothel |

All `use`/`call screen` references resolve by name; no call sites were changed.

---

## 8. File change statistics

### New files (35+)

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

### Major modified files

| File | Change |
|------|------|
| `girlclass.rpy` | 5,900 → 3,910 lines (-1,990, -34%) |
| `girl_files_dict.rpy` | Inverted index + lazy loading |
| `screens.rpy` | 9,500 → 620 lines (-8,866, all 108 screens extracted) |
| `picture.rpy` | Lazy tag parsing |
| `utils.rpy` | plural/article language-aware |
| `effects.rpy` | LRU picture cache |
| `endday.rpy` | I18N fixes |
| `core_entities.rpy` | AutoRepair frequency reduced |
| `start.rpy` | Service registration |

---

## 9. Next priorities

1. **Verification testing** — ✅ partially complete (2026-09-10): lint passes + launches to main menu; **pending manual spot checks**: new-game start, one full day settlement, girl panel/brothel/farm screens; **Phase 3 increment**: main-menu Tests button (developer mode) runs component smoke tests
2. **Remaining method migration** — ✅ fully complete (Phase 7, 2026-09-11): batches 1-14 migrated ~120 methods, created the new GirlProgression component, fixed the generate_preferences double execution and the change_stat cap regression, cleaned up 6 stale component copies and 3 dead shells. **girlclass.rpy 5,900→1,148 lines**. Only leftovers: `__init__` split (deferred, save-compatibility risk) and the `get_schedule`/`is_unique` micro-methods (intentionally retained)
3. **Screen extraction** — ✅ fully complete (Phase 2, 2026-09-10): screens.rpy 8,886 → 620 lines, 108 screens → 16 files, verified identical by character-by-character comparison
4. **Translation tools** — ✅ decided not to implement `translate_sync.py` (Phase 3): the sync need is covered by the existing toolchain — missing detection `verify_i18n.py`(`translate --count`), placeholder integrity `audit_placeholders.py`, empty-translation round trip `export_empty_to_xlsx.py`/`import_translated_empty.py`, stale entries cleaned when Ren'Py `translate` rewrites. See `docs/i18n/I18N_ROADMAP.md` Section 6. Also fixed hardcoded stale paths in `i18n_lint.py`/`verify_i18n.py` (now derived from the script location).
5. **Mod API v2 testing** — ✅ complete (Phase 3): `tools/verify_mod_api.py` static assertions + stub-environment full-flow simulation (register→trigger→cancel), `python tools/verify_mod_api.py` all passing; the in-game `test_mod_api_v2` smoke label added to the Test Runner. **Found and fixed**: `cancel_hook` routed through `execute_hook` meant the context never reached callbacks and it always returned False. Current state (2026-09-13): all 19 HOOK_* constants are wired, and the game code has several `execute_hook` call sites (`item_generated` in `items.rpy`, among others); `cancel_hook` still has no in-game call site.
6. **Dev Console hotkey** — ✅ fixed (Phase 3, c47440e): two root causes — ① the keymap bound the unmodified key `K_o` (should be `shift_K_o`); ② the console screen is `modal True`; modal blocks lower-layer events, so the underlay Keymap receives no keys while the console is open and cannot close it. Fix: the underlay handles global opening, an in-screen `key "shift_K_o"` handles closing, and toggling is ignored while the input box is focused (to avoid closing on a capital O being typed).

---

## 10. Key conventions

### Coding conventions
- All new code has bilingual (Chinese-English) comments
- Component classes access the Girl instance via `self.girl`
- Method body migration pattern: implementation in the component → Girl class delegates
- `_impl` aliases: can be deleted once migrated, retained while not

### Init priority
```
init -12   service_container  ── GameServices
init -11   game_config       ── GameConfig
init -10   settings/translations
init -9    mod definitions    ── mod-owned classes/functions (e.g. Item Quality's load_quality_tiers)
init -5    registry           ── the various Registries (incl. QualityRegistry)
init -4    variables          ── globals + hardcoded fallbacks (incl. data/quality.rpy)
init -3    utils/effects      ── utility functions (incl. the ModAPIV2 class)
init -2    class definitions  ── all class definitions + components
init -1    mods               ── v2 mod registration entry points (register_mod + is_mod_active gating)
init       start label        ── game instance creation
```

### Service access
```python
services.game       # Game instance
services.mc         # Main character
services.brothel    # Brothel
services.farm       # Farm
services.calendar   # Calendar
services.i18n       # I18nService (translation)
services.config     # GameConfig
services.mod_api_v2 # Mod API v2
services.dev_console # Dev Console
```
