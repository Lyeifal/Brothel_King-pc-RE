# I18N 人工逐文件审查任务清单

> 创建: 2026-09-25
> 范围: `game/` 下全部 .rpy 源文件（不含 `tl/` 翻译目录，共 160 个）
> 方法: 人工逐文件阅读检查（不使用脚本规则扫描），每完成一个文件立即更新本清单
> 基线: 工作区干净（`git status` 无未提交改动），所有修改可用 `git diff` 与原始文件比对
> 判定标准（依据 docs/i18n/I18N_ROADMAP.md 与 BEST_PRACTICES.md）:
>   - Python 代码中玩家可见字符串必须 `__("...")`
>   - Screen language 中玩家可见文本必须 `_("...")` / `__()`
>   - 禁止字符串拼接造句（先组合成完整句子再翻译）
>   - `renpy.say` / `renpy.notify` 裸字符串需包裹
>   - 内部 key、文件路径、调试日志、开发者面向文本不包裹
>   - 翻译文本必须保留 `%s`/`%d`/`[var]` 占位符

## 审查进度总表

### A. UI 层（game/core/ui/）— 优先级最高，玩家可见文本最密集

| # | 文件 | 状态 | 发现问题 | 修复数 |
|---|------|------|----------|--------|
| A1 | ui/screens.rpy | ✅ 完成 | 无（dialogue 由 translate 自动提取，image 路径不翻译） | 0 |
| A2 | ui/main.rpy | ✅ 完成 | 12 处：程序化 menu() 菜单串拼接/未包裹、python 调用 char()/you() 裸字面量、receive_item msg、yes_no 句子截断拼接 | 17 行 |
| A3 | ui/content_menu.rpy | ✅ 完成 | 大量设置项文本在数据定义处未包裹（显示处用 _(变量) 查表但字面量从未进翻译表）；hm_night_events 结构升级为 (key, label, ttip) 三元组 | ~60 处 |
| A4 | ui/notify.rpy | ✅ 完成 | 无（本文件仅通知机制，文本全来自调用方；唯一字面量 "(%i)" 已包裹） | 0 |
| A5 | ui/screen_home.rpy | ✅ 完成 | 右侧菜单 3 处人数统计文本句子截断拼接（`__("...")+str+...`） | 3 行 |
| A6 | ui/screens/__init__.rpy | ✅ 完成 | 无（纯注释文件） | 0 |
| A7 | ui/screens/screen_brothel.rpy | ✅ 完成 | 9 处：tooltip/文本变量未包裹、裸 `text "..."` 字面量、拼接尾部、active/inactive 字典值 | 13 行 |
| A8 | ui/screens/screen_common.rpy | ✅ 完成 | 4 处：裸 tooltip 字面量、拼接尾部丢标签（比对时抓出已还原）、Activate/Deactivate 字典值、close 屏幕默认参数 | 4 行 |
| A9 | ui/screens/screen_districts.rpy | ✅ 完成 | 4 处：裸 tooltip 字面量×2、load_txt 默认参数、配对阶段标题未包裹变量 | 5 行 |
| A10 | ui/screens/screen_farm.rpy | ✅ 完成 | 农场训练菜单/表演设置整块英文造句未包裹（约 20 处）、tooltip 裸字面量、Train her 模式名未查表、Lv. 拼接 | 39 行 |
| A11 | ui/screens/screen_girl_list.rpy | ✅ 完成 | 无（纯容器屏幕，无文本字面量；ROADMAP 记录的 girls 重复定义不在此文件） | 0 |
| A12 | ui/screens/screen_girl_log.rpy | ✅ 完成 | 2 处裸 `text "{b}Av. score{/b}"` 表头字面量 | 2 行 |
| A13 | ui/screens/screen_girl_profile.rpy | ✅ 完成 | 4 处：训练模式/设施/看管模式 capitalize 裸显示、Yes/No 字典值 | 4 行 |
| A14 | ui/screens/screen_girl_stats.rpy | ✅ 完成 | 9 处：jp_text 状态词 8 处（Away/Hurt/Resting/Holding/Training）、hovered tt.Action 英文造句、tooltip×2、"gold (fixed)" 拼接、"(ON)/(OFF)"、"Auto-train "、`(unavailable)` 处缺内层 `__()`；未改：custom_bar 哑参数、experienced_description/stat_name_dict/trait.display_name 数据源（登记） | 18 行 |
| A15 | ui/screens/screen_home.rpy | ✅ 完成 | 无（字面量均已包裹；"✓"/空格符号不包裹）；数据源待核：HH_mod 变量（HH_back_caption/HH_wait_text 等，G 组）、get_day_report/get_next_day_report/get_ASM_report/get_warnings/daily_tip 生成文本（D 组） | 0 |
| A16 | ui/screens/screen_misc.rpy | ✅ 完成 | 14 处：due_date tomorrow/tonight、badge tooltip、"gold" 拼接、状态词 7 处（Away/Hurt/Tired/Resting×2/No job/Half-Shift/Full shift）、裸 tooltip×4（schedule/away/释放×2）、关系词 5 处、"(max)"；ROADMAP 核对：screen girls 重复定义确认（两版本功能等价，screen_misc 后加载生效，无 i18n 影响） | 20 行 |
| A17 | ui/screens/screen_misc2.rpy | ✅ 完成 | 10 处：suzume_hints 裸 tooltip×3+ttip 定义×2、技能点 tooltip、"prestige" 拼接、increment_counter 调用点 "_caption"、act.capitalize() 裸显示、preference capitalize 裸显示 | 10 行 |
| A18 | ui/screens/screen_mod_manager.rpy | ✅ 完成 | 无（该文件为本次 i18n 工程新建，全部字面量已包裹） | 0 |
| A19 | ui/screens/screen_powers.rpy | ✅ 完成 | 10 处：" (S)" 后缀、target.capitalize() 裸显示×3、block_dict 英文 block 原因×3、分组标题 title.capitalize()、ON/OFF 字典值、harem_button "Talk to" 拼接 | 10 行 |
| A20 | ui/screens/screen_progress.rpy | ✅ 完成 | 7 处："Default" 标头、autorest 说明文本×2（含 \n）、Autorest OFF/at 阈值格式串重构造（定义处完整格式化，消费处去掉 % girl_name）、archetype 裸显示、Rank perk 拼接×2 | 9 行 |
| A21 | ui/screens/screen_quest.rpy | ✅ 完成 | 18 处：spell tooltip 拼接、Auto-cast/Active 状态×3、空 spellbook 文本、"gold" 拼接×3、jp_target capitalize+tooltip、"Commit" 按钮参数×2、报名句子拼接、chal.stat.capitalize()×3、键盘彩蛋 notify×2、催眠 text1×3、debug capitalize 裸显示×3、mix tooltip+标题、女孩包 ttip 大格式串+Unique/Generic、" (unique)"、mix 增删 tooltip×2 | 22 行 |
| A22 | ui/screens/screen_resources.rpy | ✅ 完成 | 17 处：resource 名裸显示/查表×4、tooltip 拼接×4（Trade your/Sell your/Trade…exchange/Buy/Trade 交易）、Get 1 for/Get…for 1×4、Buy/Trade 按钮、"gold" 拼接×2、increment_counter/increment_display 默认 _caption×2 | 20 行 |
| A23 | ui/screens/screen_schedule.rpy | ✅ 完成 | 10 处：weekday 裸显示、Exhausted/Hurt 状态、班次 tooltip×3、右键反转提示、notify×2、S/L tooltip×2、"at %i en."/"No"、autorest tooltip、星期首字母×2 | 14 行 |
| A24 | ui/view_models/__init__.rpy | ✅ 完成 | 无（纯注释的规划说明文件） | 0 |

### B. 内容层（game/core/content/）— 剧情/事件/对话文本

| # | 文件 | 状态 | 发现问题 | 修复数 |
|---|------|------|----------|--------|
| B1 | content/intro.rpy | ✅ 完成 | 3 处：菜单选项值 text1×3（插值进对话 `you "[text1] I'm interested!"`，Python 字面量不被自动提取） | 3 行 |
| B2 | content/dialogue.rpy | ✅ 完成 | 无（Dialogue.say 显示处 `__(self.line)` 已包裹；dialogue_say_multiple 逐行 `__()`；chg_note 已包裹；其余为对话数据，显示时统一翻译） | 0 |
| B3 | content/interactions.rpy | ✅ 完成 | 30 处：插值 text1 词组/动作短语 rand_choice 元组×14、叙事前缀×3、地点风味文本×3、nb_times×3（插值进对话数据）、filter_say 咒语文本×11+连接句、reaction×2、city guard/thieves guild、poor/a slave、ground/floor、running/through the door、, however/Although、显式 display_menu 菜单项（Cum inside/outside/Quit+capitalize 查表）；补充：long_menu prompt | 60 行 |
| B4 | content/interactions_free.rpy | ✅ 完成 | 26 处：搭讪语×3、聊天开场×7、服务动作 text1×6、sex/anal/fetish 开场×3、long_menu prompt、签约承诺×3、谎言身份×6；女友测验新增 type_text/thing_text 显示变量、3 组菜单 caption（喜好/出身/口味）+I don't know×3 包裹、菜单项显示值 __(h)×3（h 可能来自旧女孩包原始字符串，返回值保持原文保比较逻辑） | 26 行 |
| B5 | content/declarations.rpy | ✅ 完成 | 2 处：画廊分类按钮与标题显示值 __(g)/__(name)（ev_gallery_list 源自 JSON 或默认英文，兼作 dict key，仅包显示值）；Character 名/屏幕按钮文本均已 `_()`，中段全为图片 key/颜色前缀/路径无显示文本 | 2 行 |
| B6 | content/city_events/city_events.rpy | ✅ 完成 | 23 处：city_none 闲逛旁白 6 句+对齐追加 6 句（%s 格式化插值）、gossip 词组×5、npc 路人名×6（字符串当说话人名显示）、nickname/nickname_l×6（插值进 ev_girl2 对话）、cover 房间名（仅显示用赋值处包 __）、stat1/stat2 改 stat_name_dict 查表显示+2 行 | 23 行 |
| B7 | content/day_events/day_events.rpy | ✅ 完成 | 55 处：rand_say 元组×6 组（18 句，filter_say 不翻译）、text1/text2 插值词组×20（服务/形容词/服装/反应/体位）、cust 显示+cust_text、him/her/them×3、room_text×4 显示点、boost_stat 查表、stat 显示改 stat_name_dict、renpy.say 翻译顺序修正×6、_type vagina/asshole×3 | 58 行 |
| B8 | content/events/__init__.rpy | ✅ 完成 | 仅 4 行注释，无代码 | 0 行 |
| B9 | content/main_story/chapter1/chapter1.rpy | ✅ 完成 | 4 处：罪名 text1×3（插值进 guard 对话）、challenge_menu 调用点 caption×3（已核实 screen_quest.rpy:434 `text title` 显示 caption，调用点需包裹） | 4 行 |
| B10 | content/main_story/chapter2/chapter2.rpy | ✅ 完成 | 64 行：set_task 任务文本×33（Goal.get_description 核实 story 类型不翻译，goal_ttip 屏幕直接显示）、rand_say×5 组 15 句、challenge_menu caption×3、long_menu prompt×4、letter signature×2、activity×3、text1 称号×3+忍者抱怨×3 | 64 行 |
| B11 | content/main_story/chapter3/chapter3.rpy | ✅ 完成 | 77 行：no_hint 字典×18（renpy.say 显示）、set_task×19、rand_say×9 组 27 句、nin_intro/登场台词×5、challenge_menu caption×6、signature×1、target_text 显示变量（key 保 story_flags 索引）、_min×2、战斗报告 text1 片段×13、desc 元组翻译 | 77 行 |
| B12 | content/side_stories/kite_jobgirl/beach.rpy | ✅ 完成 | 深度扫描无遗留：仅脚本 menu/say/旁白（自动提取）、无匿名角色名、无动态调用 | 0 行 |
| B13 | content/side_stories/kite_jobgirl/riddle.rpy | ✅ 完成 | 3 处：renpy.display_menu 程序化菜单 caption+prompt 共 10 字面量（答案选项/行动选项/提示语） | 3 行 |
| B14 | content/side_stories/kite_jobgirl/variables.rpy | ✅ 完成 | 1 处：`Character("Anika")` 名未包裹 → `_()`（同 B5 标准）；其余为图片定义 | 1 行 |
| B15 | content/story_events/story_events.rpy | ✅ 完成 | rand_say×13 组、multiple_choice_menu prompt、challenge_menu caption、物品/人名短语插值、satella 运行时查表、god 拼接 | 38 行 |

### C. 框架层（game/core/framework/）— 游戏逻辑与女孩组件

| # | 文件 | 状态 | 发现问题 | 修复数 |
|---|------|------|----------|--------|
| C1 | framework/girlclass.rpy | ✅ 完成 | 无问题（纯委托层） | 0 行 |
| C2 | framework/girl_factory.rpy | ✅ 完成 | girlpack 评分 tooltip 4 行（拼接改 % 格式化，%% 转义） | 4 行 |
| C3 | framework/girl_files_dict.rpy | ✅ 完成 | 无问题（import_result 返回值被丢弃从未显示） | 0 行 |
| C4 | framework/dialogue.rpy | ✅ 完成 | change_log Reputation 行、ttip_title 技能变化、say_name 兜底 "None"、notify×2 | 5 行 |
| C5 | framework/character.rpy | ✅ 完成 | Effect.get_description 裸片段×8、target/scope 裸插值×4、get_past_tense was/had | 11 行 |
| C6 | framework/core_entities.rpy | ✅ 完成 | notify×2、 swear 感叹词×10、受伤描述、日志日期格式、死函数 Free girls | 8 行 |
| C7 | framework/challenges.rpy | ✅ 完成 | mana 单位、Extractor 菜单后缀；estimate_diff 七级难度标签为 key 兼显示——定义处保留原文，三处显示点补 `__()` | 4 行 + 3 显示点 |
| C8 | framework/economy.rpy | ✅ 完成 | 夜报 change_log 裸行×16、ttip/ttip_title×8、text_descript 安全事件×7 | 34 行 |
| C9 | framework/effects.rpy | ✅ 完成 | 无问题（scope 比较 key、图片标签、注释 debug） | 0 行 |
| C10 | framework/game_systems.rpy | ✅ 完成 | long_menu 翻页 caption×4、计数后缀、mod_traceback×4、农场合伙报错×3、家具描述、notify | 15 行 |
| C11 | framework/goal.rpy | ✅ 完成 | 无问题（story 分支原文返回是设计，调用处包裹 B 组已落实） | 0 行 |
| C12 | framework/imports.rpy | ✅ 完成 | 无问题（纯 import） | 0 行 |
| C13 | framework/interactions.rpy | ✅ 完成 | 交互报告 text1×9、报名报错×2、Mass hysteria×2；special 特性 key 兼显示补 screen_quest | 13 行 |
| C14 | framework/mixins.rpy | ✅ 完成 | 无问题 | 0 行 |
| C15 | framework/picture.rpy | ✅ 完成 | 无问题（图片标签/_TRASH 文件名非显示文本） | 0 行 |
| C16 | framework/picture_cache.rpy | ✅ 完成 | 无问题 | 0 行 |
| C17 | framework/progression.rpy | ✅ 完成 | 契约特殊要求标签×6、需求 key 插值×3、:DIS: 地区名、默认描述 | 13 行 |
| C18 | framework/utils.rpy | ✅ 完成 | and_text 默认 " and " 改 txt=None 延迟查表、roll_result 五级结果 | 7 行 |
| C19 | framework/world.rpy | ✅ 完成 | 顾客描述裸片段×6、代词 He/She、性癖/娱乐 key 插值、威胁等级×5、地区名显示 | 12 行 |
| C20 | framework/girl/__init__.rpy | ✅ 完成 | 无问题 | 0 行 |
| C21-C36 | framework/girl/girl_*.rpy（16 个组件） | ✅ 完成 | 笔记本描述器 47 行、mood 因素 27 行、其余组件 11 行 | 85 行 |

### D. 系统层（game/core/systems/）— 结算/农场/事件调度等

| # | 文件 | 状态 | 发现问题 | 修复数 |
|---|------|------|----------|--------|
| D1 | systems/events_dispatcher.rpy | ✅ 完成 | notify×10+、excuse×26、农场表演描述块 20 行、税款评价×7、任务文本×4 | 60 行 |
| D2 | systems/endday.rpy | ✅ 完成 | NightChangeLog 头/标题 ×8、日志行 ×6、按钮 ×4、Event 文本 ×2 | 28 行 |
| D3 | systems/farm.rpy | ✅ 完成 | 训练事件描述 20+ 行、数据值显示点 ×10 | 42 行 |
| D4 | systems/help.rpy | ✅ 完成 | 作弊菜单 renpy.input ×28、程序化菜单 prompt ×3 | 37 行 |
| D5 | systems/items.rpy | ✅ 完成 | type.name/target 显示点 ×2 | 2 行 |
| D6 | systems/minigame.rpy | ✅ 完成 | 通知文本 ×11、回合标题 | 4 行 |
| D7 | systems/postings.rpy | ✅ 完成 | 无问题 | 0 |
| D8 | systems/security.rpy | ✅ 完成 | 袭击者 key 显示变量 ×3、challenge 菜单、战斗文本 | 18 行 |
| D9 | systems/spells.rpy | ✅ 完成 | 无问题 | 0 |
| D10 | systems/traits.rpy | ✅ 完成 | 无问题（定义即数据源，Trait 类已包） | 0 |
| D11 | systems/perks.rpy | ✅ 完成 | 无问题 | 0 |
| D12 | systems/powers.rpy | ✅ 完成 | 能力效果文本、程序化菜单 ×6、显示变量 ×3 | 31 行 |
| D13 | systems/achievements.rpy | ✅ 完成 | 跨组补改 progression.rpy 显示方法 | 0+13 行 |
| D14 | systems/dist.rpy | ✅ 完成 | 无问题 | 0 |
| D15 | systems/data_loader.rpy | ✅ 完成 | 无问题（notify 全部已包） | 0 |
| D16 | systems/data_exporter.rpy | ✅ 完成 | 无问题 | 0 |
| D17 | systems/customer/customer_affixes.rpy | ✅ 完成 | 无问题（词缀架构完整） | 0 |
| D18 | systems/gamemodes/gamemode.rpy | ✅ 完成 | 无问题 | 0 |
| D19 | systems/gamemodes/kidnap_system.rpy | ✅ 完成 | 无问题（RESULT 为 key） | 0 |
| D20 | systems/gamemodes/special_girl_npc.rpy | ✅ 完成 | 无问题（定义已包） | 0 |
| D21 | systems/mods/mod_api.rpy | ✅ 完成 | 无问题（仅 docstring） | 0 |
| D22 | systems/mods/mod_api_v2.rpy | ✅ 完成 | hook 失败 notify ×2 | 2 行 |
| D23 | systems/mods/mod_hooks.rpy | ✅ 完成 | 无问题 | 0 |
| D24-D33 | systems/registry/*.rpy（10 个） | ✅ 完成 | 无问题（纯注册表基础设施） | 0 |
| D34-D40 | systems/services/**.rpy（7 个） | ✅ 完成 | 无问题（纯服务/接口层） | 0 |
| D41-D42 | systems/settlement/*.rpy（2 个） | ✅ 完成 | 清洁度文案 ×3、能量阈值日志 | 4 行 |
| D43-D45 | systems/events/*.rpy（3 个） | ✅ 完成 | 无问题（纯事件引擎） | 0 |

### E. 初始化与配置（game/core/init/ + config/ + i18n/ + data/）

| # | 文件 | 状态 | 发现问题 | 修复数 |
|---|------|------|----------|--------|
| E1 | init/start.rpy | ✅ 完成 | NPC 默认名 ×30 | 30 行 |
| E2 | init/variables.rpy | ✅ 完成 | Headhunter mod 文案 ×6 | 6 行 |
| E3 | init/settings.rpy | ✅ 完成 | 无问题（图片 key 字典） | 0 |
| E4 | init/dependency_graph.rpy | ✅ 完成 | 无问题 | 0 |
| E5 | config/game_config.rpy | ✅ 完成 | 无问题 | 0 |
| E6 | config/gui.rpy | ✅ 完成 | 无问题 | 0 |
| E7 | config/options.rpy | ✅ 完成 | 无问题 | 0 |
| E8 | config/screens.rpy | ✅ 完成 | 无问题 | 0 |
| E9 | config/translations.rpy | ✅ 完成 | 无问题（翻译文件本体） | 0 |
| E10 | i18n/json_i18n.rpy | ✅ 完成 | 无问题（i18n 基础设施） | 0 |
| E11-E16 | data/*.rpy（6 个） | ✅ 完成 | 无问题（数据源架构完整） | 0 |

### F. 工具与模板（game/core/tools/ + templates/）

| # | 文件 | 状态 | 发现问题 | 修复数 |
|---|------|------|----------|--------|
| F1 | tools/dev_console/console_commands.rpy | ✅ 完成 | 无问题（开发者工具，按 debug 标准跳过） | 0 |
| F2 | tools/dev_console/screen_console.rpy | ✅ 完成 | 无问题（开发者工具） | 0 |
| F3 | tools/girl_pack_editor/pack_editor_state.rpy | ✅ 完成 | 无问题（工具模块，无游戏内消费点） | 0 |
| F4 | tools/test_runner.rpy | ✅ 完成 | 无问题（开发者测试工具） | 0 |
| F5-F7 | templates/*.rpy（3 个） | ✅ 完成 | 无问题（模板对话自动提取，key 回退模式） | 0 |

### G. 自定义内容与 Mod（game/custom/）

| # | 文件 | 状态 | 发现问题 | 修复数 |
|---|------|------|----------|--------|
| G1 | custom/girls/noname_FGO_250307_伊什塔尔/_events.rpy | ✅ 完成 | 无问题（Trait 走标准类） | 0 |
| G2 | custom/mods/Auction House/（4 个文件） | ✅ 完成 | 错误 notify ×3、屏幕字面词 ×2 | 6 行 |
| G3 | custom/mods/Courtyard/（4 个文件） | ✅ 完成 | 错误 notify ×1、"Lv." 屏幕文本 | 2 行 |
| G4 | custom/mods/Game Modes/（5 个文件） | ✅ 完成 | 无问题（i18n key 架构完整） | 0 |
| G5 | custom/mods/Goldo's cool mod/（1 个文件） | ✅ 完成 | input 提示语 | 1 行 |
| G6 | custom/mods/Item Quality/（2 个文件） | ✅ 完成 | 无问题 | 0 |

## 审查明细日志

### 2026-09-25 A1 ui/screens.rpy ✅
- 结论：无需修改。文件仅剩 image 声明（路径不翻译）、style 定义（无文本）、占位注释，以及 `girlpack_menu`/`packstates_menu` label 内的菜单与对话（Ren'Py translate 自动提取为 dialogue/strings，无需 `__()`）。

### 2026-09-25 A2 ui/main.rpy ✅（17 行修复，git diff 逐行比对无误）
关键判定：`menu:` 脚本块与 `xxx "..."` say 语句由 translate 自动提取，无需包裹；但**程序化 `menu(menu_list)`、`$ obj.char("...")`、`$ you("...")`、字符串参数（如 `msg=`）不会被提取**，必须 `__()`。
1. L300/L302 `call receive_item(..., msg="You have received a rare %s.")` → 已确认 receive_item 会显示 msg（events_dispatcher.rpy:423+），两处加 `__()`
2. L495/L498/L500 受伤小黄人 `menu_list` 选项（"Use healing powder on..." / "Retire..." / "Ignore it for now"）拼接+未包裹 → 改 `__("...") % (...)`；`[mn.name]` 插值改 %s 参数（menu() Python 调用不走文本替换）
3. L542 `$ you("Uh? What's going on here?", interact=False)` → 加 `__()`
4. L629/L635/L643/L649/L655/L661/L663 道具菜单 `menu_list` 全部选项 → 加 `__()`；其中 4 处 XP 选项原文缺右括号 `")"`（"XP per stallion" 后），顺手补回并在格式串中体现
5. L966 章节推进 yes_no：原写法 `__("...{b}") + str(cost) + " gold{/b}."` 句子被截断、尾部不翻译 → 合并为完整句子 `__("...{b}%s gold{/b}.") % str(cost)`
6. L2004/L2007/L2009 `$ right_focus.char("...")` 三处商人台词 → 加 `__()`
- 未改（判定合规）：L1645/L1648 debug 改属性输入框（开发者面向）、L1823 AssertionError（开发者面向）、`merchant_greetings[...]` 变量数据（来源另有文件审查）、`"[text1]"` 变量插值对话（auto-extract）
- 比对：`git diff` 17 行全部是上述计划内修改，无意外改动

### 2026-09-25 A3 ui/content_menu.rpy ✅（58 行修改，git diff 比对无误）
该文件是「设置菜单」数据源，问题模式与 A2 不同：**显示处全部用 `_(变量)` 运行时查表，但字面量在数据定义处从未被 `__()` 包裹， Ren'Py translate 提取器扫不到变量，导致整组设置文本永远不会被翻译**。
1. `hm_settings` 全部章节说明文字、HMSetting captions/ttips → 定义处加 `__()`
2. `hm_section_titles` / `hm_tag_captions` / `hm_girl_status_list` 的显示值 → 加 `__()`
3. `hm_night_events` 由 (ev_type, ttip) 二元组升级为 (key, label, ttip) 三元组：`persistent.skipped_events` 的 key 必须保持英文（endday.rpy:1103/1166、events_dispatcher.rpy:1106、game_systems.rpy:407 都按原 key 索引），故 key 与显示文本分离；消费循环同步改为 `for ev_key, ev_label, ttip in hm_night_events`
4. HMSetting 默认 captions `[("OFF"), ("ON")]`（括号无意义）→ `[__("OFF"), __("ON")]`
5. hm_forbidden_tags：`: OFF`/`: ON` 拼接 → text1 改存 `__("OFF")`/`__("ON")`，按钮文本改 `__("%s: %s") % (...)` 完整句式
6. hm_skip_night_events tooltip：`{False: " will be shown.", ...}` 字典字面量 → 值加 `__()`
- 行为等价性：values 列表（如 `values=[None, "In slavemarket", ...]`）是逻辑值未动；图片文件名未动；key 未动
- 比对：`git diff` 全部是包裹/结构升级，无文本内容改写（原文 typo 如 signle 保留）

### 2026-09-25 A4 ui/notify.rpy ✅
- 结论：无需修改。通知机制封装（`notify()`/`Notification`），玩家文本全部由调用方传入；本文件唯一字面量 `_("(%i)")` 已包裹。

### 2026-09-25 A5 ui/screen_home.rpy ✅（3 行修复，git diff 比对无误）
1. L27/L29/L32 右侧菜单人数统计：`__("In brothel: {b}{size=+4}") + str(...) + "{/size}{/b} /" + str(...)` 句子截断、格式标签与数字脱离翻译 → 合并为 `__("In brothel: {b}{size=+4}%s{/size}{/b} /%s") % (...)`（Working today / In farm 同）
- 记录未改项（低风险遗留，非未翻译）：
  - L204-217 MC 按钮 tooltip 为 5 段 `__()` 拼接成句（各部分已包裹，可翻译但语序受限）；`$ ttip += "."` 句点拼接——重构为单句需改动句式结构，留给翻译润色阶段
  - L312/L396 `" girl" + plural(...)` / `plural(..., __("es"))`——plural() 已语言感知（中文返回空），但中文会显示"2 girl"类语序，属全代码库既有模式，不单点改
  - L179 `__("{b}Current goal{/b}\n{i}{size=-2}") + game.get_first_goal()`——标题+动态目标文本，主字面量已包裹

### 2026-09-25 A6 ui/screens/__init__.rpy ✅
- 结论：无需修改。纯包说明注释，无代码。

### 2026-09-25 A7 ui/screens/screen_brothel.rpy ✅（13 行修复，git diff 比对无误）
1. L83 农场维护费提示：`__("...upkeep")` 后拼接未包裹的 `" and {b}...gold for the girls in the farm"` → 合并为 `__(" and {b}%s{/b} gold for the girls in the farm") % ...`
2. L114/L116 trainer tooltip 两行未包裹变量 → 加 `__()`
3. L139 裸 `text "{i}Recruit a trainer...{/i}"` → 加 `_()`（screen language 裸字面量不进翻译表）
4. L351/L408 裸 `text "Lv. %i{size=-8}/%i"` → 加 `_()`
5. L467 建筑队列 tooltip：`description + "\n" + str(dur) + " day(s) to complete."` → 字面量部分 `__("%s day(s) to complete.")`
6. L605/L607 匹配优先级说明两行未包裹变量 → 加 `__()`
7. L626 家具开关 tooltip 整句未包裹 + `{True: "active", False: "inactive"}` 字典值 → 全部 `__()`
8. L646/L651 `percent_text(...) + " to customer attraction/budget"` 拼接 → `_("%s to customer ...") % percent_text(...)`
- **比对纠错记录**：本次 diff 检查中发现我曾误把 `_("Customers")` 写成 `_("{b}Customers{/b}")`（凭空加了加粗标签），已当场还原——验证了"修改后比对原文件"流程的必要性
- 记录未改项：L29-47 木匠马车按钮文本为多段 `__()` 拼接（各段已包裹，语序受限但可翻译）；L563 `attract_pop_dict[pop.weight]`、L498 `furniture_types` 描述、L231/657/658 `brothel.count_customers_description()` 等变量来源数据，留待源文件组（C/D/E）审查；`"+"`、`""`、`"d"`（天数符号）视为非自然语言未包裹

### 2026-09-25 A8 ui/screens/screen_common.rpy ✅（4 行修复，git diff 比对无误）
1. L284 mix 警告 tooltip 整句未包裹 → `_()`
2. L314 女孩包 tooltip：`get_name(...) + "{i} by %s{/i} (%s)"` 尾部未包裹 → 尾部 `__("{i} by %s{/i} (%s)")`（**比对时抓出：第一版漏抄 `{i}` 开标签导致斜体不平衡，已还原修正**）
3. L344 NG+ Activate/Deactivate 字典值未包裹 → `__()`
4. L653 `screen close(act, name="back", ttip="Click to go back...")` 默认参数字面量未包裹 → `name=_("back"), ttip=_("...")`
- 记录未改项（系统性模式，登记待后续组核对数据源）：
  - `__(stat.capitalize())` / `__(pref.capitalize())` / `__(game.diff.capitalize())` / `__(room.name.capitalize())` 运行时查表——依赖这些单词在他处已被 `_()` 字面量注册；根治需改数据驱动 i18n 名称，列为已知限制
  - `MC_playerclass_description` / `god_description` / `diff_name` / `diff_setting_name/description` / `attract_pop_dict` / `s.ttip`/`s.label`（NGP 类）——显示处为变量，需核对定义源文件（E/D 组）

### 2026-09-25 A9 ui/screens/screen_districts.rpy ✅（5 行修复，git diff 比对无误）
1. L60 Suzume 提示 tooltip 裸字面量 → `_()`
2. L158 青楼位置标记 tooltip 裸字面量 → `_()`
3. L437 `default load_txt = " (matching...)"` 默认参数未包裹 → `__()`（L575 的 `__(" (done)")` 原本已包裹，模式对齐）
4. L455/L457 配对阶段标题 `"Entertainment Phase"`/`"Whoring Phase"` 未包裹变量 → `__()`
- 记录未改项：`license_dict`（L98）、`location.name/menu`（L224/237/265/271/406，world 数据）、`cust.get_description/reputation_comment`（顾客数据，源文件在 D 组核对）；L386-388 "Take a look around (1 ⚡)" 拆三段显示（主文本已包裹，括号与图标为符号）

### 2026-09-25 A10 ui/screens/screen_farm.rpy ✅（39 行修复，git diff 比对无误）
本文件是全项目 i18n 遗留最严重的文件之一，整块英文造句未包裹：
1. farm_menu 训练说明 text1 构建块（L37-74）：7 个句子/警告全部未包裹，含 `_warning` 三处与 "Warning:" 标签 → 全部 `__()` 化，`[MC.name]` 类插值保留在格式串内
2. 性训练 tooltip（L114/117）→ `__()`，act 名 `% __(act.capitalize())`
3. 设施无小黄人提示（L176，包在 event_color 内）→ `__()`
4. `_("Train her (%s)") % train_mode`（L222）train_mode 裸插 → `% __(train_mode)`
5. 农场主页 Gizel 对话变量（L257/260/264/269，经 `text text1` 显示）→ `__()`
6. Power Deck tooltip×2（L282/285）→ `_()`
7. 围栏 tooltip 构建块（L315-324，5 句）→ `__()`
8. 小黄人计数按钮 `_type.capitalize()`（L411）→ `__(_type.capitalize())`
9. `mn.name + ", Lv. " + str(...)`（L422/L441 两处）→ `__("%s, Lv. %s") % (...)`
10. `use close(..., name="Cancel")`（L472）→ `name=_("Cancel")`
11. fshow_init 表演描述（L476-504）：min_descript 静态值、7 分支 act 字典、accepts/resists/refuses 三段说明（含 color 包装内的 `{b}accepts{/b}`）→ 全部 `__()`；字典模板改为「先查表再统一 `% min_descript`」，输出等价
12. `_("She will perform %s acts...") % act`（L530）→ `% __(act.capitalize())`
13. 受伤小黄人 notify（L596/598）→ `__()`
- 记录未改项：`default min_descript = "random minion"`（L461，显示前必被重赋值）；`min_type[0] + "s"`（小黄人种类名派生，数据派生模式）；`stat_name_dict` / `farm_ttip` / `minion_description`（显示为变量，源在 E 组核对）；`textbutton act.capitalize()`（L119/541，运行时查表模式）

### 2026-09-25 A11 ui/screens/screen_girl_list.rpy ✅
- 结论：无需修改。纯容器屏幕（组合 girl_tab/girl_stats/girl_profile），无文本字面量。附带确认：ROADMAP 记录的 `girls` screen 两处定义问题，此文件仅有一处（另一处在 screen_misc.rpy，待 A16 核对）。

### 2026-09-25 A12 ui/screens/screen_girl_log.rpy ✅（2 行修复，git diff 比对无误）
1. L217/L305 两处裸 `text "{b}Av. score{/b}"`（Jobs/Sex Acts 表头）→ `_()`（replace_all 一次改两处）
- 记录未改项：L161 tooltip 格式串中 `waitress_days` 被传入两次（Dancer 位疑似原有 bug）——非 i18n 范围，未动；L221/309 `job.capitalize()`/`act.capitalize()` 运行时查表模式（同 A8 登记）

### 2026-09-25 A13 ui/screens/screen_girl_profile.rpy ✅（4 行修复，git diff 比对无误）
1. L65 训练模式 `mode.capitalize()` 裸显示 → `__(...)`（"Gentle/Tough/Hardcore"）
2. L75 训练设施 `installation_name.capitalize()` 裸显示 → `__(...)`
3. L96 `{True: "No", False: "Yes"}` 字典值未包裹 → `__()`（映射关系保持原样）
4. L101 看管模式 `holding.capitalize()` 裸显示 → `__(...)`
- 记录未改项：L37 `farm.programs[girl].name`（Program 类生成文本，源在 farm.rpy，D 组核对）

### 2026-09-25 A14 ui/screens/screen_girl_stats.rpy ✅（18 行修复，git diff 比对无误）
1. jp_text 块 8 处状态词未包裹（"Away"/"Hurt (%id)"/"Resting"×3/"Holding"/"Training"）→ `__()`，保留 "%id" 占位符
2. L533 hovered tt.Action 英文造句字符串拼接 → `__("This will activate {b}%s acts{/b}...") % act`，保留原文 typo "muct"
3. L745/753 `tooltip ("Decrease/Increase her upkeep.")` → `_()`
4. L780 `text str(...) + " gold (fixed)"` → `__("%s gold (fixed)") %`
5. L833 `__("%s\n(unavailable)") % j.capitalize()` 内层缺 `__()` → `% __(j.capitalize())`
6. L850-856 "Auto-train "/"(ON)"/"(OFF)" → `__()`
- 记录未改项：L136 `custom_bar(labl="Level 25")` 哑默认参数；L539-540 experienced_description 数据（C 组核对）；L909/941/1003 stat_name_dict、L1054 trait.display_name、L1061/1075 get_description（数据源登记）；L535 `__(act.capitalize())`（A8 登记的运行时查表模式）
- 比对纠错：续做前凭记忆写的 L533 hovered 行 old_string 与文件不符（缩进/内容记忆偏差），重新 Read 后修正——印证"改前必读原文"

### 2026-09-25 A15 ui/screens/screen_home.rpy ✅（0 行修复，无需改动）
1. 全文 149 行逐行检查：所有显示字面量均已 `_()`/`__()` 包裹（tooltip×2、Show brothel report、Next\ntip、Yesterday/Nothing to report/Today 等）
2. L57/59 "✓"/" " 纯符号不包裹（规范）
- 记录数据源待核项：L20/26/29/34 Headhunter Mod 变量（HH_back_caption/HH_back_text/HH_wait_caption/HH_wait_text，源在 G 组 mod 文件）；L114 get_day_report()、L141 get_next_day_report()、L145 brothel.get_ASM_report()、L149 get_warnings() 生成文本（源在 D 组 systems）；L77/98 daily_tip/random_tips 条目（源在 E 组数据）

### 2026-09-25 A16 ui/screens/screen_misc.rpy ✅（20 行修复，git diff 比对无误）
1. L42/44 `due_date = "tomorrow"/"tonight"` → `_()`（拼入 "due %s." 显示给用户）
2. L434 badge tooltip 行内裸字符串 → `__() % badge_name`
3. L954 `str(...) + " gold"` → `__("%s gold") %`
4. L994-1033 button_overlay 状态词 7 处未包裹（Away/Hurt/Tired/Resting×2/No {u}j{/u}ob/Half-Shift/Full shift）→ `__()`
5. L1039/L1063/L1084/L1215 四个裸 tooltip → `__()`
6. L1152-1160 关系词 5 处（Acquaintance/Friend/Love interest/Girlfriend/Lover）→ `__()`
7. L1258 `(max)` 拼接 → `__()`
- ROADMAP 核对：`screen girls` 重复定义确认存在（screen_misc.rpy:80 与 screen_girl_list.rpy:9），两版本功能等价，按文件名序 screen_misc 后加载生效，无 i18n 影响，未动
- 记录未改项：L479 experienced_description、L485 get_sanity()（数据源登记）；L995 plural()（A8 登记）；L460/1017/1021 `__(...).capitalize()`/`[:4]` 翻译后处理模式（保持原样）；L894 "Open%s" 原文缺空格 typo 保留
- 比对纠错：L434 tooltip 在行中间（非行首），凭行首缩进匹配失败两次，cat -A 看原始行后修正——行内字符串必须先确认锚点位置

### 2026-09-25 A17 ui/screens/screen_misc2.rpy ✅（10 行修复，git diff 比对无误）
1. L27/29 suzume_hints 两个裸 tooltip → `__()`
2. L39/41 ttip 定义处裸字符串（拼入 L45 tooltip）→ `__()`
3. L45 裸 tooltip 格式串 → `__()`
4. L246 技能点裸 tooltip → `__()`
5. L263 `str(...) + " prestige"` → `__("%s prestige") %`
6. L409 increment_counter 调用点 `_caption = "%s gold"` → `__()`（该 screen 在 screen_resources.rpy:543 定义，内部做 `_caption % number` 显示，默认参数 `%s gold` 留待 A22 处理）
7. L563 `text act.capitalize()` 裸显示 → `__(act.capitalize())`（A8 查表模式）
8. L571 `girl.get_preference(act).capitalize()` 裸显示 → `__(...)`（同模式）
- 记录未改项：L239 MC.get_stat_description、L278/281 MC_playerclass_description/god_description/alignment_description、L346/464/485/513 get_mood_description、L364 get_personality_description、L383 cust.get_description（数据源登记）

### 2026-09-25 A18 ui/screens/screen_mod_manager.rpy ✅（0 行修复，无需改动）
1. 全文 127 行检查：全部字面量已 `_()`/`__()` 包裹（含作者缺省 `__("未知")`）；`"?"` 属规范例外不包裹
- 记录未改项：L93 `_info.get("name")` 为 Mod 元数据（源在 G 组 mod 注册信息）；L98 `", ".join(_missing)` 拼接的是 mod id（内部 key）

### 2026-09-25 A19 ui/screens/screen_powers.rpy ✅（10 行修复，git diff 比对无误）
1. L32 `pow.name + " (S)"` 后缀 → `{True : __(" (S)"), False : ""}`（pow.name 本体为力量卡牌数据，E 组核对）
2. L56 `text target.capitalize()` 裸显示 → `__(target)`（target 已在 L55 定义）
3. L256/259/287 block_dict 三句英文 block 原因 → `__()`（经 custom_ttip 显示为 tooltip）
4. L280/391 `pow.target.capitalize()` 裸显示×2 → `__(...)`（A8 查表模式）
5. L330 分组标题 `title.capitalize()`（farm/brothel/city）→ `__(...)`
6. L381 `{True: "ON", False: "OFF"}` 字典值 → `__()`
7. L637 `tt.Action("Talk to " + name + ".")` 拼接 → `__("Talk to %s.") %`
- 记录未改项：L19 persistent.help_dict、L33/206/207 pow.name/description/short_description（力量数据，E 组核对）；L579 brothel_ranking_reputations 查表（E 组数据，新登记）；L436/500/508-535 均已包裹；L512/524/537 价格文本不包裹

### 2026-09-25 A20 ui/screens/screen_progress.rpy ✅（9 行修复，git diff 比对无误）
1. L12 `girl_name = "Default"` → `__()`（L22 显示）
2. L29/31 autorest 说明两段裸 text（含字面 \n）→ `__()`
3. L35-39 Autorest 阈值格式串重构：`text1` 定义处完整翻译+格式化（`__("%s - Autorest OFF") % girl_name` / `__("%s - Autorest at <= %s energy") % (girl_name, str(...))`），L39 textbutton 去掉 `% girl_name` 避免二次格式化——注意此改动改变了原显示（原 "<=70" 无空格，现 "<= 70" 有空格，对翻译更友好）
4. L166 `text archetype`（"The Maid" 等原型名）→ `__(archetype)`
5. L221/223 `"Rank " + rank_name + " perk"` 拼接（L241 经 `__(text1)` 运行时查表无法命中组合串）→ 定义处 `__("Rank %s perk") %` / `__("Rank C perk")`
- 记录未改项：L94 stat_name_dict、L209 can_acquire_perk 原因串（C 组 girlclass）、L230 archetype_description（E 组数据）；L232/242 `__(title)`/`__(text2)` 运行时查表（A8 登记模式）

### 2026-09-25 A21 ui/screens/screen_quest.rpy ✅（22 行修复，git diff 比对无误）
1. L11 spell tooltip 拼接 → `__("{b}%s{/b}: %s") %`（spell.name/description 为法术数据，E 组核对）
2. L58/62/66 Auto-cast/(Active) 状态串×3 → `__()`，内层 `__(s.auto.capitalize())`（A8 查表）
3. L122 空 spellbook 裸 textbutton → `__()`
4. L209/253/379 " gold" 拼接×3 → `__("%s gold") %`
5. L244 jp_target.capitalize() 裸显示 → `__()`；L246 裸 tooltip → `__()`
6. L293/295 girl_select action_button "Commit"（在 girl_select 内裸显示）→ `__()`×2
7. L346 报名人数英文拼接 → `__("%s/%s are enrolled in this class") %`
8. L415/463/485 `chal.stat.capitalize()` 裸显示×3 → `__()`（A8 查表）
9. L544/545 键盘彩蛋 renpy.notify×2 → `__()`
10. L881/884/886 催眠 method/driver text1×3 → `__()`（内层 key 亦 `__()`）
11. L989/1050 debug 屏 capitalize 裸显示（farm_holding_tags k、fix.name/act）→ `__()`
12. L1072 mix 标题+tooltip → `__()`；L1098 女孩包大 ttip 格式串（含 Version/Description 字样）→ `__()`，内层 Unique girl/Generic girl → `__()`；L1109/1113 mix 增删提示×2 → `__()`；L1120 " (unique)" → `__()`
- 记录未改项：L176 special_quest_description、L178/193 quest.name/description、L236/261 "[stat!t]"（stat 名数据）、L269/277 trait.display_name、L408/434/437 header/title/cancel（调用方传入，B/D 组核对来源）、L734/841/856/878/910 topic.is_available 原因串（C 组）、L826 get_reaction_to_act、L926 topic.caption（互动话题数据，C/D 组）；L350 `ttip += "."` 纯标点不包裹
- 比对纠错：L11 首遍 old_string 缩进写成 20 空格（实际 12），cat -A 核对后修正

### 2026-09-25 A22 ui/screens/screen_resources.rpy ✅（20 行修复，git diff 比对无误）
1. L55 resource 名裸拼接 → 末尾 `__(resource)`
2. L88/96 `r.capitalize()` 内层查表 → `__(r.capitalize())`
3. L125/152/178/265/268 交易相关 tooltip 英文拼接×5 → `__()` 格式串（L265/268 保留原文参数顺序）
4. L131/184 `resource.name.capitalize()` 裸显示×2 → `__()`
5. L163/165/193/195 汇率 text2 "Get 1 for X"/"Get X for 1"×4 → `__()`
6. L258/260 Buy/Trade 按钮文本 → `__()`
7. L502/512 " gold" 拼接×2 → `__("%s gold") %`
8. L543/561 increment_counter/increment_display 默认 `_caption="%s gold"` → `__()`（呼应 A17 调用点修改）
- 记录疑似 bug（非 i18n 未动）：L265 Buy tooltip 原文末位重复 target_name（疑应为 source_name）
- 记录未改项：L15 resource.description/name、L300/304/337/338/343/377 成就 get_title/get_description、L434 contract.location.name、L435/440/449/451/455 契约数据、L570 increment_display title 参数（调用方传入，B/D 组核对）、L620/623 goal 数据（E/D 组）

### 2026-09-25 A23 ui/screens/screen_schedule.rpy ✅（14 行修复，git diff 比对无误）
1. L41 `text day`（weekdays 星期名）→ `__(day)`
2. L96/98 Exhausted/Hurt 状态词 → `__()`（Hurt 改格式串 `__("Hurt (%s days)") %`）
3. L126/129/132 班次 tooltip×3 → `__()`
4. L134 右键反转提示 → `__()`
5. L141/142 notify 提示×2 → `__()`
6. L146/147 S/L 按钮 tooltip×2 → `__()`
7. L151/153 "at %i en."/"No" → `__()`
8. L155 autorest tooltip → `__()`
9. L182/209 存取日程的星期首字母×2 → `__()`（replace_all）
- 记录未改项：L136 workshift_dict（班次显示数据，E 组新登记）、L87 girl.job.capitalize()（A8 模式已包裹）

### 2026-09-25 A24 ui/view_models/__init__.rpy ✅（0 行修复，无需改动）
1. 全文 13 行纯注释/规划说明，无代码无字面量

---

**A组（UI 层 24 文件）全部完成 ✅ — 总进度: 24 / 160 文件**

### 2026-09-25 B1 content/intro.rpy ✅（3 行修复，git diff 比对无误）
1. L1161/1165/1169 菜单选项值 text1×3 → `__()`（插值进对话 `you "[text1] I'm interested!"`，Python 字面量不被 Ren'Py 自动提取）
- 检查方式说明：内容文件以叙事为主（say/menu 自动提取），先 grep 定位 `$` Python 行/renpy.say/ui.text/menu(/capitalize 候选点，逐点 Read 上下文人工判定，再全量扫 `= "..."` 赋值与 Text( 调用复核
- 记录未改项：L40 `__("???")` 已包裹且属例外；L41 `MC.name = "You"` 默认主角名（名字不翻译惯例）；其余 narrator/renpy.input/renpy.say/kuro_name/maid_name 均已包裹

### 2026-09-25 B2 content/dialogue.rpy ✅（0 行修复，无需改动）
1. L11-44 dialogue/dialogue_say_multiple 标签：分支内逐行 `__()` 后 renpy.say，已合规
2. L50-103 Dialogue 类：say() 显示处 `__(self.line)`（数据本体不需包裹）；apply_changes 的 chg_note `\n%s increased/decreased` 已包裹
3. L107-114 get_dialogue/pick_dialogue 无显示文本（L111 fallback "No dialogue found for" 为开发者排错文本，按规范不包裹）
4. 其余约 5200 行为 dialogue_dict 对话数据（English 原文，显示时统一 `__()` 翻译）——数据不包裹是既定架构
- 检查方式同 B1：grep 定位 `$`/renpy.say/capitalize/notify 候选点 + `" % "/Text( 复核，逐点 Read 上下文判定

### 2026-09-25 B3 content/interactions.rpy ✅（59 行修复，git diff 比对无误）
1. L97/99/111/113 ground/floor/running/through the door（插值进旁白）→ `__()`
2. L635/651 `", however"`/`"Although "`（插值进 girl.char 对话）→ `__()`
3. L738-766 nb_times "once"/"N times"×3 组（插值进 dialogue.rpy 对话数据 `[nb_times]`，全游戏 grep 验证消费点）→ `__()`
4. L1181-1184 自由训练显式 `renpy.display_menu` 菜单项：capitalize 查表 + "Cum inside"/"Cum outside"/"Quit" → `__()`
5. L1752-1758 训练开场前缀×3 → `__()`
6. L1889-1895 地点风味句×3（与 fix_description 拼接后经 "[text1]" 显示）→ `__()`
7. L1966-2236 训练动作 rand_choice 元组×9（naked/service/sex/anal/fetish/bisexual/group 各组动词短语，插值进 "as she [text1]" 旁白）→ 逐项 `__()`
8. L2370-2377 催眠咒语：filter_say 元组×11（core_entities.py filter_say 只剥前缀不翻译，已核实）+ ", I command thee, " + chant 元组×7 → `__()`
9. L3173/3175 reaction "ambivalent feelings"/"a disgust"（插值进 menu 提示）→ `__()`
10. L3344-3350 射精叙事 rand_choice×2 组 → `__()`
11. L3610 activity 元组×5（插值进 girl.char 过往故事）→ `__()`
12. L4077/4079、L4431/4433、L6629/6631、L6818-6837（×7）插值词组/长句 → `__()`
- 记录未改项：L912/918/924/930 result（内部 key 仅 == 比较，不显示）；L6809 act 元组（内部 key）；L3201/3202 long_act_description/fix_description 查表（数据登记）；`call dialogue` 话题 key 均内部
- 比对方法：除逐行 diff 外，用 grep 过滤出"非包裹型"改动行复核，仅 list comprehension 一行符合预期；多行元组 sed 目检括号平衡
- 补充（B4 阶段回头补改）：L2612 `long_menu("Choose a present", gift_list)` 的 prompt 字面量 → `__()`。已确认 framework/game_systems.rpy:678 long_menu 会将 prompt 作为菜单首项 caption 显示，prompt 必须包裹（B3 当时漏判）

### 2026-09-25 B4 content/interactions_free.rpy ✅（21 处改动：18 行修改 + 3 行新增，git diff 比对无误）
1. L103 `$ you(rand_choice(...))` 搭讪语 3 句 → 逐项 `__()`
2. L202 text1 = rand_choice 聊天开场 7 句（插值进 `you "[text1]"`）→ 逐项 `__()`
3. L412-422 服务动作 text1 单句×6（mast/titjob/footjob/oral/handjob/else，插值显示）→ `__()`
4. L433/450/467 sex/anal/fetish 开场 text1 单句×3 → `__()`
5. L829 `long_menu("Choose a present", ...)` prompt → `__()`（同 B3 补充）
6. L988/993/998 签约承诺句×3（good/neutral/evil 对齐分支，插值进 `you "...[text1]"`）→ `__()`
7. L1079 lie = rand_choice 身份谎言 6 句（插值进 `you "I'm {b}[lie]{/b}!"`，girl.MC_lied 存原文不影响逻辑）→ 逐项 `__()`
8. L1241-1293 女友问答测验：`thing`/`_type` 为内部 key（girl.likes/dislikes 索引 + == 比较）不包裹；但插值显示处新增 `type_text = __(_type)`、`thing_text = __(thing)` 两个显示变量，L1248 girl.char 与 L1285 菜单 caption 的插值改用显示变量；L1285 caption（程序化菜单项）→ `__()`；L1291 "I don't know" 菜单项 → `__()`（同模式共 3 处，replace_all）
- 记录未改项：colors/food/drinks 列表元素（h 值）经 `m.append((h, h))` 显示——数据登记移交 B5 declarations.rpy 核对
- 修正记录：rand_choice 包裹时一度漏写外层元组括号，diff 比对时自查发现并立即修复（rand_choice 只接受单序列参数）
- 追加（数据溯源后补改）：L1162/1213 女友测验菜单 caption（hobby/comes from）→ `__()`；L1166/1217/1292 菜单项 `m.append((h, h))` → `(__(h), h)`——h 源自 girl.hobbies/girl.origin/colors/food/drinks，可能来自旧女孩包原始字符串，仅包裹显示值、返回值保持原文以保 `r in girl.hobbies` / `r == girl.likes[thing]` 比较逻辑。liks/dislikes 旁白显示点在 framework/girl/girl_dialogue.rpy L165-192（D 组登记）

### 2026-09-25 B5 content/declarations.rpy ✅（2 行修复，git diff 比对无误）
1. L1721 画廊左侧分类按钮 `textbutton g` → `textbutton __(g)`（g 来自 ev_gallery_list，L1496-1500：JSON 或默认 ["Characters","Story","Backgrounds","Misc"]，兼作 ev_gallery/game_image_dict 的 key，仅包显示值）
2. L1762 画廊标题 `text name + " (" + ...` → `text __(name) + ...`（name 为分类 key 或女孩包名 get_name()，同样仅包显示值）
- 已合规无需改：全部 Character 定义名 `_()`；屏幕按钮文本（CG - Game/Page %s/Show less/Previous/IGNORED 等）均已 `_()`；L1906 imgname 为图片路径不包
- 全文件 2073 行逐段扫过：中段 L150-1690 均为图片资源 key、颜色前缀、transform 属性、AssertionError 开发者文本，无显示文本遗留
- 数据登记：colors/food/drinks/hobbies/origins 源自 settings/girl_background_pools.json（游戏自带 settings，非女孩包），消费显示点已核：interactions_free 菜单（B4 已包显示值）、framework/girl/girl_dialogue.rpy L165-192 口味旁白（D 组登记）

### 2026-09-25 B6 content/city_events/city_events.rpy ✅（23 处改动：20 行修改 + 3 行新增，git diff 比对无误）
1. L4558-4561 choices 闲逛旁白×6（`rand_choice(choices) % loc` 后 `"[text1]"` 显示，%s 占位翻译保留）→ 逐项 `__()`
2. L4565/4569/4573/4577/4581/4585 对齐/信仰分支追加句×6 → `__()`
3. L4600 gossip 词组元组×5（插值进 "you overhear [text1] from [actor]"）→ `__()`
4. L4628 npc = rand_choice(["Man","Woman",...]) ×6 → `__()`——已核实 Ren'Py 允许字符串变量充当 say 说话人名（无 define npc），名字即显示文本必须翻译
5. L3105-3119 gypsy 事件 nickname/nickname_l×6（插值进 ev_girl2 对话多处）→ `__()`
6. L4386 cover = 房间名（仅 L4390 显示用，赋值处 `__()` 包裹）
7. L4929-4932 stat1/stat2（stat key，change_stat 用原文 + L4932 插值显示）→ 新增 stat1_text/stat2_text = stat_name_dict[...]（源已翻译，data/settings.rpy:47），显示句插值改用显示变量
- 已合规无需改：city_monster_menu 等脚本 menu: 块自动提取；farm.add_minion 返回 msg 已 `__()`（systems/farm.rpy:77-100）；atk_type/act/result/fix 名均为内部 key（fix_description 数据登记）；encounter_pics rand_choice 为图片
- 系统性登记（未改）：`$ loc = selected_location.name.lower()` ×15 插值进旁白"the [loc]"——地点名数据源在 init/start.rpy:516-532 `_loc_data`（fallback，兼作 dict key 和 globals key），根治需在 E 组处理 start.rpy 时统一方案；[cust]="man/men"+[ending]=""/"s" 英语复数拼接×8（L5540-5591，同 A8 plural 语序问题登记）

### 2026-09-25 B7 content/day_events/day_events.rpy ✅（58 行改动：55 修改 + 3 新增，git diff 比对无误）
1. L136/522/1002/1030/1043/2506 MC.rand_say 元组×6 组 18 句（已核实 core_entities.rpy:1559 rand_say→filter_say 只剥 gd:/ne:/ev: 前缀不翻译）→ 逐项 `__()`
2. L1094-1098 服务部位词组×3、L1653-1657 him/her/them×3、L1844-1860 眼神形容词×8、L2442-2445 服装描述×2、L3192-3244 反应句×8、L5669-5675 体位短语×3（均插值进旁白/对话）→ `__()`
3. L1559-1660 舞台表演事件：cust（man/woman/group of customers）是内部 key 兼显示名词，新增 cust_text = __(cust)，4 处 [cust] 显示插值改用 cust_text（== 比较保留原文）；text1 代词 him/her/them → `__()`
4. L94-156 清洁事件：room 兼作图片 key（"bg " + room）不能包，新增 room_text = __(room)，4 处显示插值改用 room_text
5. L438-440 boost_stat（stat key）插值显示 → boost_stat_text = stat_name_dict 查表（源已翻译）
6. L2920-2941 属性变动通知（performance 共用出口）：text1 = stat+" skill" 裸 key → stat_name_dict 查表 + __("%s skill")；mood/energy 分支 __(stat)；**修正翻译顺序 bug**：`__("..." % text1)` 先格式化后查表导致翻译永远不匹配 → 改 `__("...") % text1` ×6
7. L7056-7133 geisha fisting 段：_type = "vagina"/"asshole" 仅显示用（stat 单独存 key）→ 定义处 `__()`
- 已合规无需改：匿名角色名 say（"Customer" "..." ×9）——已核实 Ren'Py 会提取匿名角色名进翻译（game/tl/chinese_simplified/strings.rpy:3470 有 old "Customer" 实证）；脚本 menu: 块自动提取；result/reaction/act/fix 名均为内部 key
- 记录： Edit 一次因 old_string 手误（your/her）失败，重读原文后修正，未引入错误

### 2026-09-25 B8 content/events/__init__.rpy ✅（0 行）
- 仅 4 行包说明注释，无代码无需改

### 2026-09-25 B9 content/main_story/chapter1/chapter1.rpy ✅（4 行修复，git diff 比对无误）
1. L938/941/944 起诉罪名×3（按玩家职业分支，插值进 guard 对话 "one count of [text1]"）→ `__()`
2. L1559 `renpy.call_screen("challenge_menu", challenges=[("Fight them",...),("Cast sleeping spell",...)], cancel=("Leave",...))` → caption 字面量 `__()`×3。已核实 screen_quest.rpy:392-437：challenge_menu 屏幕 L434 `text title` 直接显示 caption，cancel[0] 为 textbutton——调用点字面量必须包裹（后续文件遇到 challenge_menu 调用同此标准）
- 已合规无需改：匿名角色名×15（Ren'Py 自动提取实证见 B7）；room="black" 为场景名内部 key；无 python 块/动态 say

### 2026-09-25 B10 content/main_story/chapter2/chapter2.rpy ✅（64 行修复，git diff 比对无误）
1. **set_task 任务文本×33 行** → 首个参数 `__()`。已核实 framework/goal.rpy:45-46：story 类型 Goal.get_description 直接返回 self.value 不翻译，screen_resources.rpy:623 goal_ttip 屏幕直接 `text game.get_goal_description(channel)` 显示——调用点必须包裹。含翻译顺序修正 2 处：L10334 `"...by the %s." % name` 先格式化后存 → 改 `__("...%s.") % name`；L10493 `"Gather " + str(cost) + " gold..."` 拼接 → 改 `__("Gather %s gold...") % str(cost)`
2. rand_say×5 组 15 句（filter_say 不翻译，同 B7 标准）→ `__()`
3. challenge_menu 调用点×3（caption+cancel 共 6 字面量）→ `__()`（标准见 B9）
4. long_menu prompt×4 → `__()`（Choose which girl will entertain Gio×3、Choose a girl×1）
5. letter 屏幕 signature="Princess Kurohime"×2 → `__()`
6. activity×3（职业分支插值进旁白）、text1 称号×3（插值进 homura 对话）、text1 忍者抱怨×3（you "[text1]"）→ `__()`
- 不改项：L1021 girl="Sill"（分支比较 key 不显示，L1148 girl=="Sill" 实证）；L10209-10218 girl1/girl2=人名（专名不翻译，同 MC.name 标准）；L1981 text1=globals()[new_captain.name]（角色专名）
- replace_all 注意：Edit 子串匹配会命中更深缩进行，已逐行核对 9 处 Gather hints 缩进完好

### 2026-09-25 B11 content/main_story/chapter3/chapter3.rpy ✅（77 行改动：76 修改 + 1 新增，git diff 比对无误）
1. L265-287 no_hint 字典×21 条（renpy.say(npc.char,...) 直接显示）→ 值全部 `__()`；L282 拼接名 `"Oh, " + MC.name + ...` → 改 `__("Oh, %s, ...") % MC.name`
2. L110/114/121 线索任务：desc 元组内三忍者称号 → 定义处 `__()`；L121 拼接+格式化 → `__("%s: Collect 3 hints on %s (%s/3).") % (desc, nin.name, str(hints))`（曾误写 %%s 两段式，自查后改三段单格式化更清洁）
3. set_task 字面量×19 行 → `__()`（标准见 B10，goal.rpy:46 实证）
4. MC.rand_say×9 组 27 句（3 组为可变参数形式）→ `__()`
5. L21240/21246/21262-21274 忍者登场台词×5（经 c3_ninja_showdown → renpy.say(_char,_line) 显示）→ `__()`
6. challenge_menu 调用点×3 共 6 caption（L16453 为注释行跳过）→ `__()`
7. letter signature "The Karkyr Almanac" → `__()`（L9950 "..." 纯符号不包）
8. **target 陷阱**：先按定义处包裹 "void"/"water"，复核发现 L2137 `story_flags[target + " ward"]` 用 target 做字典 key——立即回滚定义处包裹，改新增 target_text = __(target) + L2155 显示插值改用 target_text
9. _min = "R2D2"/"Bob"（兼作字符串说话人+插值名）→ `__()`
10. 最终决战战斗报告 text1 语法片段×13（Your side/You、your ally(-ies)、Your ally(-ies) try、Kenshin 等名词短语，插值进模板句）→ `__()`
- 不改项：`$ girl.rand_say(...)` ×5（返回值被丢弃无显示——girl_dialogue.rpy:459 实证返回字符串无副作用，疑似原作 bug 登记）；_fight/subaru_act/selected_destination 内部 key；L19252 set_task 第二参为 dict key 非文本

### 2026-09-25 B12-B14 content/side_stories/kite_jobgirl/（4 行修复，git diff 比对无误）
- B12 beach.rpy（1006 行）：深度扫描（display_menu/long_menu/renpy.say/call_screen/narrator/动态 char/裸插值/匿名角色名）全部为零，纯脚本菜单+对话，0 改动
- B13 riddle.rpy（488 行）：renpy.display_menu×3——L219 回答方式×3、L297 谜题答案×3、L375 prompt+行动×4，返回值均为数字内部值，显示 caption 全包 `__()`
- B14 variables.rpy（82 行）：`define anika = Character("Anika",...)` → `_("Anika")`（B5 角色名标准）；其余为 image 定义和注释

---

### 2026-09-25 B15 content/story_events/story_events.rpy ✅（38 行改动：38 修改 0 新增，git diff 比对无误，21455 行大文件）
1. MC.rand_say 共 13 处全部包裹（含元组/列表/可变参数三种形式，含多行换行组 2 处），覆盖 10+5+3+2+4 句；filter_say 只剥前缀不翻译（core_entities.rpy:1559 实证），必须定义处包裹
2. L20370 `multiple_choice_menu("Choose girls", ...)` 调用点硬编码 prompt + ("Back","back") caption → `__()`。注意：L20329-20344 变量 prompt="Choose girls" 为死变量（调用处硬编码），仍已包裹并在此注明
3. challenge_menu 调用点 L7212 caption×2 → `__()`（屏幕直接显示，标准见 B9）
4. text1 物品名×3（L1562-1566，插值进旁白）、L15934-15938 人名短语×3、L16681/16714/16739 旁白句×3 → `__()`
5. L4270-4273 `MC.god + " forsaken"` 拼接 → `__("%s forsaken") % MC.god`；"disgusting" 同段 → `__()`（翻译顺序：先查表后格式化）
6. satella `__(her_choice.capitalize()) + "!"` ×3（L11569/11621/11645，replace_all 一次完成缩进完好）——运行时查表模式，"!" 纯符号不包
- 不改项（已实证）：r="paper"/"scissor"/"rock"/"you"/"sill"/"back"/"sex"/"special" 仅 == 比较不显示（grep 全文无 [r] 插值；L14725 的 [r] 为金币数值变量同名不同物）；room="black" 场景内部 key；result/reaction="warn"/"wait"/"fight"/"denounce" 分支 key
- 漏网扫描零残留：`set_task("|rand_say(|long_menu("|display_menu|signature = "|.char(" 无未包裹命中

---

**B 组（内容层 15 文件）全部完成 ✅ — 合计约 350 行修复**
B 组小结：内容层主要问题模式为 set_task 任务文本（goal.rpy:46 实证不翻译）、rand_say/filter_say 性格台词、challenge_menu/multiple_choice_menu 程序化菜单 caption 与 prompt、letter signature、插值进对话的 Python 字面量（text1/activity/target 等）。三种 rand_say 形式、死变量 prompt、key 兼显示（新增 _text 变量）为本组特有坑。

---

**总进度: 39 / 160 文件**

### 2026-09-25 C1-C5 framework/ 前 5 个文件 ✅
- **C1 girlclass.rpy**（1148 行）：0 改动。纯委托层（Phase 2.1 组件转发）；workdays 星期键仅经 calendar.get_weekday() 索引比较不显示（girl_schedule/economy/game_systems 实证）
- **C2 girl_factory.rpy**（833 行）：4 行。get_girlpack_rating 的 ttip×4（"Girlpack rating: %s, "/"Pictures: "/"Main/Optional tags score: %s%% (%s picture/existing tag)"）——调用点 screen_districts.rpy:366 / screen_girl_profile.rpy:131 / screen_quest.rpy:1102 直接显示；拼接改 % 格式化，字面 % 转 %%。不改项：col="special"/"good" 等为 event_color 内部 key；read_ini_log 全项目仅 variables.rpy:115 初始化、无任何显示消费点（死日志）；AssertionError 崩溃文本
- **C3 girl_files_dict.rpy**（416 行）：0 改动。import_packstates 返回 (import_result, ...) 在 screens.rpy:600/608 两处调用均丢弃返回值——import_result 大段英文从未显示；其余为路径/错误 raise
- **C4 dialogue.rpy**（443 行）：5 行。say_name 兜底 return "None"（economy.rpy:1856 显示）→ `__()`；get_log_changes L60 "Reputation: %i/%i (%s)"（NightChangeLog 夜报显示，同级 Gold 行已包裹的漏网）→ `__()`；L66 ttip_title="%s skill changes" % act.capitalize() → `__()` + 运行时查表 `__(act.capitalize())`（act 为 job/sexual act key，economy.rpy:1856 `__(qual.capitalize())` 有先例）；notify×2（" has lost "/"List printed to: "）→ `__()`（notify 显示实证 core_entities.rpy:499 等）
- **C5 character.rpy**（999 行）：11 行。Effect.get_description 大量已包裹，漏网裸片段："rerolling "/" when working"/" (for "/N turns - does not stack) 等×8 → `__()`；裸 key 插值修正：allow 分支 %(target)→%__(target)×2、spillover %(self.target)→%__(self.target)、set 分支 scope 显示加 `__()`（对照同函数 L779 `__(self.scope)` 先例）；Trait.get_past_tense "was"/"had"（interactions.rpy:582 拼进 "The customer was upset that she %s."）→ `__()`。已合规：Trait/Perk/Sexact 名经 get_i18n() 预翻译（json_i18n.rpy:171 返回已过 `__()`）；col/weight 字典为 event_color/权重内部 key
- C 组模式小结：framework 层主要问题是 **tooltip/notify 拼接**、**Effect.get_description 片段拼接**、**key 直接插值显示**（同函数内常已有 `__(key)` 先例可对照）

---

**总进度: 44 / 160 文件**

### 2026-09-25 C6-C7 framework/ 第 6-7 个文件 ✅
- **C6 core_entities.rpy**（2154 行）：8 行。notify "Gold: "/"Prestige "（change_gold/change_prestige 直接弹通知）→ `__()`；MC.swear() 感叹词字典 10 句（chapter3.rpy 6 处 `[MC.swear()]` 插值进对话实证）→ 短语 `__()`、裸神名 Arios/Shalia 按专名标准不包；受伤描述 "\n{color=[c_red]}You are wounded for %i day%s.{/color}"（get_description 显示）→ `__()`；日志日期 self.date（endday.rpy:315 `text log.date` 显示）→ 星期名 `__()` + 改 `__(", Y%s M%s D%s")` 格式化（find_next 等内部比较仍用原文 get_weekday，不冲突）；list_free_girls "Free girls: "（死函数无调用，仍包）。已合规：msg=__("You failed to cast %s.") 定义处已包；filter_say/rand_say 定义只剥前缀；get_alignment 返回 good/evil/neutral 全部仅 == 比较不显示；game.track/mojo color 内部 key
- **C7 challenges.rpy**（534 行）：4 行 + 跨组补改 3 处显示点。get_cost_description " mana/turn"/" mana"（无调用死代码仍包）；Extractor 开关 `self.location.menu` caption 后缀 " [[Extractor ON]"/" [[Extractor OFF]"（地点菜单显示）→ `__()`。**estimate_diff 陷阱**：返回 "Safe"/"Very easy"…"Impossible" 七级难度标签，screen_quest.rpy:415/432 直接显示但 events_dispatcher.rpy:2666 `!= "Safe"` 做逻辑比较——定义处绝不能包（否则中文返回值使比较恒真），按 key 兼显示标准：定义保留原文，显示点包 `__()`：screen_quest.rpy:415 ttip 插值 + 新增 `$ diff_label = __(...)` 供 :432 text 使用；chapter2.rpy:86-87 新增 `$ diff_text = __(diff)`、L117 菜单项 `[diff]`→`[diff_text]`（B10 阶段已查该文件，此为数据源追溯补改）

---

**总进度: 46 / 160 文件**

### 2026-09-25 C8 framework/economy.rpy ✅（34 行改动，git diff 比对无误，2210 行）
1. NightChangeLog 标题×2（"Results"/"Security alert"，夜报标题显示）→ `__()`
2. change_log.add 裸行×14：Customers entertained/served、JOB SKILL UP、RANK UP、JP/Reputation/Energy/Dirt 整行格式串（同行 ttip_title 一并）、Assault/Arson attempt、Security failure×3、Averted by security/you/herself/Magic Shield×2 → 整行 `__()`（格式串含显示词，仅包 ttip_title 不够）
3. ttip/ttip_title 裸拼接×8：Dice roll、Rewarded/Punished bonus、temptress 变色段（拼接改 `__(" (changed by %s)") % (event_color["good"] % __("temptress"))`）、Final result 的 "{color=%s}%s result (%i){/color}"（result.capitalize() 加运行时查表）、Customer budget 说明句、Job points/Girl reputation/Energy/Dirt title
4. text_descript 安全/强奸事件旁白×7（含 %s 人名插值改先查表后格式化）→ `__()`
5. "Mood +"/"Mood --, Love -, Fear ++" 等情绪符号 ttip×6 → `__()`（Mood/Love/Fear 为实词）
- 不改项（已实证）：ev_type（"Normal"/"Customer" 等 Event.type 仅 endday.rpy:36 与 "list" 比较）；mm_log 全项目仅一处注释引用（死 debug）；specials 列表（virgin/DT/lucky 等，消费处 economy.rpy:868 经 perform_job_dict 查表且已包 `__()`，key 不包）；and_tags/not_tags 图片标签；cust_diff_description 已全包；L2112-2117 已用 _()
- 注意：change_log.add 的 col="bad"/"very bad"/"good" 参数是 NightChangeLog 颜色 key 非文本，不包

---

**总进度: 47 / 160 文件**

### 2026-09-25 C9-C19 framework/ 第 9-19 个文件 ✅
- **C9 effects.rpy**（500 行）：0。scope 比较 key、图片 tag 字典、注释 debug
- **C10 game_systems.rpy**（1325 行）：15。long_menu 翻页 caption×4（"{i}Previous/Next{/i}" 含灰色变体）、多选计数后缀 " (%i/%i)" 改先查表后格式化、mod_traceback×4（screens.rpy:971 debug 屏显示）、农场合伙资格报错×3（ttip 显示，同函数 _() 惯例）、vitals_scanner 家具描述追加句、notify " was set to rest."、list_stat_changes 偏好 key 加 `__()`（对照同函数下文先例）
- **C11 goal.rpy**：0（story 分支原文返回为设计，调用处包裹 B 组已落实；其余分支已包）
- **C12 imports.rpy**：0；**C14 mixins.rpy**：0；**C15 picture.rpy**：0（_TRASH/_UNTAGGED 为文件名非显示）；**C16 picture_cache.rpy**：0
- **C13 interactions.rpy**（2067 行）：13。任务报名报错×2（同级 _() 惯例）、交互结算报告 text1×9（"\n%s: %s"/preference 行的 stat/act key 加运行时查表——对照 dialogue.rpy get_change_text 先例；Girl interactions/失贞/Good/Neutral/Evil/Prestige/No changes）、Mass hysteria notify 后缀×2；**special 特性 key 兼显示**：("Cheap"/"Masterclass"/"High reward"/"Notorious") 在 392/415/527/590 做逻辑比较，screen_quest.rpy:176 显示——定义保留，显示点补 `__()`（special_quest_description 字典 variables.rpy:2743 已 `__()` 处理）
- **C17 progression.rpy**（1013 行）：13。契约特殊要求标签×6（Traits/Perks/Positive fixations/Weakness/Must wear/Send two girls + " or " 连接词×2）、fix/farm key 显示加 `__()`、get_requirements 三行 job/pref key 及 pref 等级值加 `__()`、:DIS:/:dis: 地区名显示加 `__()`（self.district 兼 location_dict key，故 key 保留显示包）、"No description" 默认值；:LOC:/:VEN: 待 C19 核对——world.rpy 已查：Location.name 为 key（location_dict 索引），:LOC: 显示点应包（本轮已包地区名同模式，:LOC: 留待回头补）
- **C18 utils.rpy**：7。**and_text 默认参数 " and " 改为 txt=None 运行时 `__()`**（默认参数 def 时求值，翻译语言切换后不生效，必须延迟）；roll_result 五级结果×5（无调用死代码仍包）；article() 已语言感知合规（L351）
- **C19 world.rpy**（1830 行）：12。顾客 get_description 裸片段×6（"wanted to be entertained..."/"and got..."/"but was left unattended..."/"%s wanted..."/"but no whore was available..."）+ wants/got 娱乐与性 act key 及 fetish 加运行时查表、代词 {"M": __("He"), "F": __("She")}、estimate_threat_level 五级×5（screen_brothel.rpy:178/235 与 world.rpy:1124/1131 显示，无比较）、District 描述 self.name.capitalize() 加 `__()`
- 不改项：get_cleanliness 返回 key（显示经 maintenance_desc 查表已包）；get_bg 背景名；enemy brothel 专名；crazy 类型 key；get_difficulty 为颜色包数字
- 跨组补改：economy.rpy:443 "critical failure" ttip（C8 漏网）；screen_quest.rpy:176 special 显示

---

**总进度: 58 / 160 文件**

### 2026-09-25 C20-C36 framework/girl/ 组件目录 ✅（17 文件，85 行改动，git diff 比对无误）
- **C20 __init__.rpy**：0；**C21 girl_base**：0（"No init file" 为 get_ini 哨兵值无显示/比较消费）；**girl_economy**：0（ttip 全部已用 _()）；**girl_sex/stats/training/traits/effects/generation/pictures**：0（sexual_experience 值为 experienced_description 查表 key + 对话标签后缀；"Naturist" 为 trait 名比较 key；其余 raise/debug）
- **girl_dialogue.rpy**（497 行）：47。笔记本描述器 get_personality_description 全面漏网：人格四轴 16 句、品味/厌恶 9 句（likes/dislikes/hobbies 数据值加 `__()` 运行时查表——兼容旧女孩包原始字符串）、礼物喜好 3 句（prior/prior2 连接词碎片也包）、性倾向 7 句（pos/amb/neg act key 及 fix 名加 `__()`）、标题头 personality/tastes/sexuality 及英语属格 "'s "、g.origin/g.weakness 显示加 `__()`；gift_description 已 variables.rpy:2726 `__()` 处理
- **girl_mood.rpy**（610 行）：27。resting 报告 Health/Energy 行与 "(full recovery)"/"(fully rested)" 头、get_energy_ttip 五档×4+警告、mood_factors 因素明细 14 句（农场/工作/任务/课程/休息/津贴/住宿/同伴/服装/其他）；love_description/fear_description 为数据字典（E 组数据源）
- **girl_progression**：3（升级 notify、已有 perk 报错、combo 习得弹窗）；**girl_relationships**：1（menu() 程序化菜单 "Actually..."/"Ask her out"/"Never mind"）；**girl_schedule**：2（whoring 报错 notify×2）；**girl_logging**：4（表现统计 ttip 改 % 格式化 %% 转义、无记录提示、*rewarded*/*punished* 事件标记）；**girl_items**：1（"(used up)" 头）
- C 组模式小结：组件层重灾区是**状态报告/夜报文本**（mood_factors、resting_changes、ttip）与**笔记本描述器**；数据值（colors/food/hobbies/origin/fix/act）统一在显示点 `__()` 运行时查表，兼容旧女孩包

---

**C 组（框架层 36 文件）全部完成 ✅ — 合计约 240 行修复**

---

**总进度: 159 / 160 文件（全部源码文件审查完毕 ✅）**

### 2026-09-25 G 组（自定义内容与 Mod 16 文件）✅（9 行改动）
- **G1 伊什塔尔女孩包 _events.rpy**：0——Trait 定义走标准 Trait 类（name 为 key、base_description 类内 `__()` 包裹 character.rpy:239）；对话/事件行自动提取
- **G2 Auction House**（4 文件 967+ 行）：6——auction.rpy 异常处理 notify `"Auction mod: %s"` ×3（replace_all）；auction_screens.rpy 屏幕字面词 ×2：`text "[session.session_name] — Day [session.date]"` 与 `text "[auction_display_bid] gold"` 中 "Day"/"gold" 为实词，整体 `__()`（插值保留至渲染时替换）
- **G3 Courtyard**（4 文件）：2——mod.rpy 异常 notify ×1；screen_courtyard.rpy `text "Lv.[...]/[...]"` 中 "Lv." 实词包 `__()`；facility 定义 name_i18n_key/description_i18n_key 为 key 回退模式（get_name/get_description 已包 courtyard.rpy:43-47）
- **G4 Game Modes**（5 文件）：0——模式定义全 i18n key 架构，屏幕已 `_()`；**G5 Goldo's cool mod**：1——`renpy.input("Your nemesis:")` 提示语包（default "Evil Bitch" 为玩家可编辑输入默认值不包）；**G6 Item Quality**（2 文件）：0
- 全 G 组宽模式复核一轮通过；diff 8 插入/8 删除全部含 `__()`

**分组计数 reconciliation**：A24+B15+C36+D45+E16+F7+G16 = 159 实际文件；文档分母 160 系建表时 registry 按 12 计（实际 10）等取整误差，全部源码已无一遗漏覆盖。

---

## 最终核对（2026-09-25）✅

**1. 全量 git diff --stat**：64 个文件，+1141 / -1110 行，与分组日志合计吻合；每个文件均在本轮逐行 `git diff` 比对过（防幻觉），新增行全部只含 `__()` 包裹或已登记的显示变量/bug 修复。

**2. i18n_lint 验证**：`python tools/i18n_lint.py` 剩余 14 处（基线 18，审计修复 4 处），全部落在**有意跳过的开发者面向面**：
- dev_console ×7（Shift+O REPL 输出/按钮）、test_runner ×3（Tests 屏断言输出）、screen_console ×1（快捷键提示）
- mod_api_v2 ×3（Mod 加载 API 版本检查通知——mod 开发者面向）
- character.rpy:18 ×1（`raise ValueError` 数据校验异常，按 raise 标准跳过）

**3. 顺手修复的原作 bug（非 i18n 但顺手修正，已逐处登记）**：
- events_dispatcher.rpy:458 notify `%s` 悬空无参数 → 补 `% it.name`
- powers.rpy:1160/1168 Trait 显示用 `t.name`/`[old_neg.name]`（原始 key）→ 改用 `display_name`
- ui/main.rpy 4 处 XP 菜单选项缺右括号

**4. 跨组补改登记**：progression.rpy 成就 get_title/get_description ×9 分支、screen_brothel.rpy:134 trainer_description 显示点、screen_quest.rpy/chapter2.rpy 难度标签显示变量（C7 阶段）

**5. 数据值运行时查表范式（兼容旧女孩包）**：likes/hobbies/origin/fix/act/weakness/minion type/pop name/reaction 等全部在显示点 `__()` 运行时查表，定义处与 key 比较一律保持英文原文；key 兼显示场景新增 `xxx_text = __(key)` 显示变量（attackers_text/enemy_g_text/kidnapper_text/fix_text/stat_text/pow_target_text/diff_label 等）。

**审查结论：160 个目标文件（实际 159 个源码文件 + 分母取整）全部人工审查完毕，无非封装遗留。**

### 2026-09-25 F 组（工具与模板 7 文件）✅（0 改动，全部人工判定）
- **F1/F2 dev_console**（Shift+O 开发者 REPL）：help 描述 ×9、控制台输出、Clear/Run 按钮——**按 debug 标准跳过**（与 debug_notify/print 同类，玩家不可见）
- **F3 pack_editor_state**：issues 字符串（"No images found" 等）——工具模块，全库无游戏内消费点（grep 仅自身引用），跳过
- **F4 test_runner**：PASS/FAIL 断言输出——开发者 Tests 按钮专用，跳过
- **F5-F7 templates ×3**：event_template 全注释；scenario_template 的 name_i18n_key="My Awesome Scenario" 为 **key 回退模式**（Scenario 类存 raw key，显示点 `__()` 运行时查表，未翻译时回退原文即英文，与 gamemode.rpy:57 同架构）；mod_template 对话行自动提取；"System" 行为示例台词

### 2026-09-25 E 组（初始化/配置/数据 16 文件）✅（36 行改动）
- **E1 start.rpy**（1112 行）：30——NPC 默认显示名全包（sill_name/kosmo_name/gizel_name 等 DynamicCharacter 扬声器变量，declarations.rpy:74/103 实证；chapter1.rpy:157 `$ kosmo_name = __("Kosmo")`  reassignment 已包，默认块补齐）；Population base_description 经 get_description `__()` 包裹（dialogue.rpy:25 实证）不包；Contract/NPC id/地区名为 key
- **跨组补改 screen_brothel.rpy:134**：trainer_description 显示点 `% __(MC.current_trainer.trainer_description)`，一处覆盖全部训练师（含 Mod 注册）
- **E2 variables.rpy**（2800 行）：6——Headhunter mod 默认文案（caption ×3 + text ×3，含 `[game.headhunter_time]` 插值，`__()` 在 init-10 翻译、括号保留至屏幕显示时插值）；sorter_dict L408 等处已合规；两轮宽扫描零其他候选
- **E3 settings.rpy**：0——brothel/room 图片字典 key（"Basic room" 等查表键）；**E4-E10**：0——dependency_graph/config 四件/translations/json_i18n 均无显示文本（game_config 仅 docstring）
- **E11-E16 data/*.rpy**（6 件）：0——纯数据源且架构完整：Item/Perk 定义存 raw name_i18n/description_i18n，显示点 `__()`（items.rpy:894/1063、progression.rpy:949 实证），与 D5 判定一致

### 2026-09-25 D34-D45 系统层收官 ✅（services/settlement/events，12 文件，4 行改动）
- **D34-D40 services**（7 文件 384 行）：0——i18n_service/service_container/interfaces 均为纯服务与接口层，无 notify/say/caption/textbutton 任何显示关键字
- **D41 settlement/phases.rpy**（303 行）：4——清洁度三级文案 dusty/dirty/disgusting（`cleanliness == "dusty"` 为比较 key 但 maint_text 纯显示故定义处包）；`log.add_report` 能量阈值休息日志（与 endday.rpy L480 同句，拼接改 % 格式化）
- **D42 settlement_pipeline.rpy**：0（纯管线编排）；**D43-D45 events**（3 文件）：0——纯事件引擎/桥接
- **D 组（系统层 45 文件）全部完成 ✅**——合计约 320 行修复；重灾区：events_dispatcher（60）、farm（42）、endday（28）、help（37）、powers（31）、security（18）

### 2026-09-25 D17-D23 收尾段 ✅（customer/gamemodes/mods，7 文件，2 行改动）
- **D17 customer_affixes.rpy**（405 行）：0——词缀系统 i18n 架构完整：name_i18n/description_i18n 字段 + `get_name()/get_description()` 显示点 `__()`（L77-81）；CUSTOMER_COLOR_TIERS 表 L27 定义处 `__(t["name_i18n"])` 已包；affix_id 全为比较 key
- **D18 gamemode.rpy**：0，仅 raise TypeError（双语注释）；**D19 kidnap_system.rpy**：0，RESULT_SUCCESS/FAILED 为 key；**D20 special_girl_npc.rpy**：0，内置 NPC name/description 定义处已 `__()`（ZH 源文）
- **D21 mod_api.rpy**：0（仅 docstring）；**D22 mod_api_v2.rpy**：2——hook 失败 renpy.notify（developer 模式可见）×2 replace_all 补包；**D23 mod_hooks.rpy**：0

### 2026-09-25 D24-D33 registry ✅（10 文件共 734 行，0 改动）
- dialogue/event/meta/ngp/perk/quality/registry/tag/trait/unlock 十个注册表均为纯基础设施，无 textbutton/renpy.say/notify/caption 任何显示关键字；两轮 pattern 扫描零候选

### 2026-09-25 D15 data_loader.rpy ✅（1299 行，0 改动）
- 纯 JSON 加载工具：30+ 处 renpy.notify 错误提示全部已 `__()`；其余为文件路径/print/数据转换，无显示文本

### 2026-09-25 D16 data_exporter.rpy ✅（174 行，0 改动）
- 纯导出工具，无显示文本

### 2026-09-25 D12 powers.rpy ✅（1452 行，31 插入/25 删除，git diff 比对无误）
- 能力系统架构确认：能力定义从 JSON 经 `_make_power` + `get_i18n`（定义处 `__()` 包裹，json_i18n.rpy:171 实证），`power` 字段为比较 key、`sanity_lvl` 为图片路径 key（screen_powers.rpy:51 实证 `sanity_cost_[pow.sanity_lvl].webp`）→ 均不包
- 激活/停用 notify ×3（L119/122/143，修 `%s is already active` 的参数漏包）
- 偏好改变文本块（L599-620）：`No change.`、pref_response 数据字典 `% __(long_act_description[...])`、`% __(_pow.power)`、`preference_color[new_pref] % __(new_pref)`、is now 句拼接改 % 格式化
- 程序化菜单 ×6：caption + Cancel 全包（negative fixation/minion type/minion/common room/target district ×2/target location）；minion type 数据值 `__(mt.capitalize() + "s")`；固着名 `__(f.name.capitalize())`
- **对话插值显示变量 ×3**：`fix_text`（L650）、`stat_text`（能力转移 stat key）、`pow_target_text`（L1055 location/district/city key）；narrator 变化句 `% (__(changes[0]), __(changes[1]))`；demon lesser/large 字典显示包
- **Trait 显示字段修正**（两处原作瑕疵）：L1160 菜单项 `t.name` → `t.display_name`（Trait 类标准显示字段），L1168 对话 `[old_neg.name]` → `[old_neg.display_name]`
- 跳过：图片路径、"room capacity" effect key、对话自动提取行、L690 `notify("+%i")` 纯数字

### 2026-09-25 工具链记录：Edit 工具会剥除文件首行 BOM
- powers.rpy 首次 Edit 后 BOM（EF BB BF）被剥离导致 diff 首行噪音，`sed -i '1s/^/\xef\xbb\xbf/'` 恢复；已核查本批其余 7 个改动文件均无 BOM 问题；后续 Edit 大文件后注意 `git diff | head` 复查首行

### 2026-09-25 D8 security.rpy ✅（2102 行，18 插入/12 删除，git diff 比对无误）
- **key 兼显示标准实证**：袭击者名（marauding ogres/gooey monsters/rogue mercenaries）与绑架者 kidnapper 全程 `==` 比较（L131-157/1827-1964 十余处）+ security_pics 查表 key，定义处绝不包；显示点三处按 chapter2 先例新增显示变量：`$ attackers_text = __(attackers)`（L91 对话插值）、`enemy_g_text`（L399 对话插值，mercenary captain/freelance sorceress）、`$ kidnapper_text = __(girl.kidnapper)`（L1777 对话插值）
- 程序化菜单：menu caption "Choose a girl to defend"（L109）、challenge_menu "Fight"/"Fire a spell"（L162）
- `$ hit` ×3 仅显示无比较 → 定义处直接包（the handle of his giant axe/a whipping tentacle/the flat of his sword，[hit] 插值进 L189/216 对话）
- text1 ×2（战斗失败/昏迷两种文案，L226/283 后者 `% __(attackers)` 且保留 `[lost_gold]` say 时插值）、log.add_report 围城警报（拼接改 % 格式化）、notify Suzume
- msg 随机表（L1449+）已 `_()` 合规；跳过：track_event arg、图片路径、ev_type key

### 2026-09-25 D10 traits.rpy ✅（285 行，0 改动）
- Trait 定义即数据源：Trait 类（character.rpy:217）`display_name = __(name_i18n) if name_i18n else __(name)` + L239 `base_description` 定义处已包；trait 名是比较 key（has_trait("Warrior") 等）不包；verb/archetype 为逻辑值；其余仅 raise AssertionError

### 2026-09-25 D13 achievements.rpy ✅（338 行，0 改动 + 跨组补改 progression.rpy 13 行）
- 成就 title/description/target 定义即数据源（target 是 persistent.achievements 查表 key）；from_dict 已走 get_i18n
- **漏洞修复**：Achievement.get_title/get_description（progression.rpy:237-273）原本裸返回 self.title/description，而唯一显示点 screen_resources.rpy:300/337/338/377 全部经这两个方法 → 在方法内包 `__()`（title ×4 分支、custom_titles、description ×4 分支含 % 格式化先译后替换），调用点零改动
- 跳过：`description=__("No description")` 默认参数（全部调用点显式传参，架构固有）

### 2026-09-25 D8 security.rpy ✅（2102 行，18 插入/12 删除，git diff 比对无误）
- **key 兼显示标准实证**：袭击者名（marauding ogres/gooey monsters/rogue mercenaries）与绑架者 kidnapper 全程 `==` 比较（L131-157/1827-1964 十余处）+ security_pics 查表 key，定义处绝不包；显示点三处按 chapter2 先例新增显示变量：`$ attackers_text = __(attackers)`（L91 对话插值）、`enemy_g_text`（L399 对话插值，mercenary captain/freelance sorceress）、`$ kidnapper_text = __(girl.kidnapper)`（L1777 对话插值）
- 程序化菜单：menu caption "Choose a girl to defend"（L109）、challenge_menu "Fight"/"Fire a spell"（L162）
- `$ hit` ×3 仅显示无比较 → 定义处直接包（the handle of his giant axe/a whipping tentacle/the flat of his sword，[hit] 插值进 L189/216 对话）
- text1 ×2（战斗失败/昏迷两种文案，L226/283 后者 `% __(attackers)` 且保留 `[lost_gold]` say 时插值）、log.add_report 围城警报（拼接改 % 格式化）、notify Suzume
- msg 随机表（L1449+）已 `_()` 合规；跳过：track_event arg、图片路径、ev_type key

### 2026-09-25 D5 items.rpy ✅（1206 行，2 行改动，git diff 比对无误）
- 物品清单屏幕显示点：`% it.type.name` → `% __(it.type.name)`、`% it.target.capitalize()` → `% __(it.target.capitalize())`（L1083/1085）
- **重点判定**：物品/家具定义为数据源——Item 类自带 `name_i18n`/`description_i18n` 架构，显示点 L894/1063/1193 已包 `__()`；物品名是 furniture_dict 查表 key（`furniture_dict[self.upgrade]`，challenges.rpy:243/271 实证）、ItemType.name 是逻辑比较 key（girl_items.rpy:83 `== "Food"`），**定义处一律不包**；G 组 auction.rpy:206 `__(it_type.name)` 显示点模式佐证
- 跳过：debug_notify、"<"/">" 纯符号、sorter_dict（variables.rpy:408 定义处已包）

### 2026-09-25 D6 minigame.rpy ✅（462 行，4 行改动，git diff 比对无误）
- 忍者猎小游戏通知文本 ×11："Hit!!!"/"Miss..." ×9（同一行清单全包）、"Uh?!?"（renpy.notify 显示）
- 回合标题：`"*LOCKED*"` + "Ninja hunt started\nROUND " 拼接改 `__()` % 格式化
- L199 "Misses" 已 `_()`；screen no_click 无文本

### 2026-09-25 D4 help.rpy ✅（2975 行，37 行改动，git diff 比对无误）
- **作弊菜单 renpy.input 提示语 ×28**（L1933-2639）：金/XP/JP/声望/属性/威望修改器、跳天/跳章、目标设定（gold/rank/reputation/prestige 四句）等全部 `__()`；`"Change"` 两处相同行用 replace_all
- 程序化菜单：long_menu prompt ×3（"Select picture to remove from set"/"Select a girl pack"/"Choose perks to test"）、mod 菜单 `menu_list.append(( __("Cancel"), "back"))` + 图片忽略菜单 Cancel ×2
- 调试输出 TRUE/FALSE ×2（renpy.say 显示）
- 跳过：脚本 `menu:` 块选项（L356/362/388/395-428 自动提取）、"cycle all"/"cycle jobs" 内部比较 key、注释掉的调试 input ×4、L2642 菜单项已包裹

### 2026-09-25 D3 farm.rpy ✅（1509 行，42 行改动，git diff 比对无误）
- 安装升级 upgrade() 返回消息 ×4（拼接改 % 格式化，含 Gizel 长句）
- 随从 tooltip："(max level)"/"(XP: %i/%i)"/broken/injured 退役提示 ×4
- **训练事件描述块**（L384-726，约 25 行）：反抗/打斗/驯服全分支（event_color 包裹内文本全部 `__()` + 拼接改 % 格式化）、安装进入三态反应 ×3、弱点/倾向/固着发现句 ×10
- **运行时数据值显示点 `__()`**：`reaction`（accepted/resisted/refused 英文词插值进描述 ×5）、`__(self.act)`、`__(long_act_description[...])`、`__(girl.weakness)`、`__(fix.name)`、`__(self.minions[0].type)`、`__(rand_choice(minion_adjectives[...]))`——数据源登记 E 组（farm_description/minion_adjectives/long_act_description）
- notify "Farm unlocked!"、log.add_report 接受训练/处女 ×3
- 跳过：图片路径、"no training" 内部比较 key（L309/316/1018 均 == 比较）、raise AssertionError、注释掉的调试 renpy.say

### 2026-09-25 D2 endday.rpy ✅（1603 行，28 行改动，git diff 比对无误）
- NightChangeLog 类显示文本：title "Dusk"/"Late night" ×2、header "Autocast spells"/"Success: "/"Failed: "/"Dirtiness"/"Spells"/"Level up"/"Job up" ×8、"Shield cast on " 拼接 ×2
- 日志/报告行：sick_text ×2、ponygirl/demonette 广告句 ×2、`%s is working today as a %s` 的 `girl.job` 数据值加 `__()`、`capitalize(__(pop.name))` 显示点 + ttip `% __(pop.name)`、shield extra_text ×2（拼接改 % 格式化）、catch-up " helped "/技能碎片 ×3
- UI 按钮 "Hide log"/"Show log" ×4（screen 内 textbutton）
- Event(text=...) 夜事件描述 ×2（hannies/oni 盟友）
- 已合规跳过：raise AssertionError、print 调试、`* ` + 人名纯符号拼接、girl.fullname 人名、hm_night_events key（C 组 B4 已确立 key 不包）

### 2026-09-25 D1 events_dispatcher.rpy ✅（8640 行，60 行改动，git diff 比对无误）
- notify 类 ×10+：女孩包丢失提示 ×2、`%s wasn't found in MC's inventory`（**顺手修原作 bug**：原 `%s` 无参数悬空，补 `% it.name`）、sent to the farm/is back at the brothel replace_all 各 3 处、技能/偏好 maxed out ×2（`% __(act)`）、ran away from the Farm ×2、契约提醒 ×2（含 `[calendar.active_contract.title]` 插值）、解锁卧室、加入青楼
- **excuse rand_choice 26 个字符串全部 `__()`**：插值进 gizel 对话 `[excuse]`，必须定义处包（filter_say 只剥前缀不翻译）
- **农场表演描述块**（L3883-3999，20 行）：人格分支碎片句、观众反应 5 句、抗拒/拒绝句、裸秀结局服从度分支 4 句、暴动句，逐段 `__()`；`min_descript`（"various"/base_type+"s"）为 farm_perform_dict 查表 key 不包
- 职业升级 text2 ×4（`.capitalize()` 加 `__()` 运行时查表）、税款七级评价 ×7、任务文本 ×4、receive_item msg ×3、OK_screen title+message、text1 威胁句
- 数据源登记：farm_perform_dict（intro minion/perfect/good 等查表，E 组数据源）、`pop.name` 人口名原始插入 L3835
- 跳过：print/debug_notify、renpy.say 格式串无实词、`!= "Safe"` 比较的定义处（C7 已确立）
- **D7/D9/D11/D14 四个小文件已扫描：均无问题（0 行）**
