################################################################################
##  Scenario Template — BK Evolution
##  EN: Copy this file to game/custom/scenarios/ and rename it to start
##      building your own scenario. Replace all placeholder values.
##  ZH: 将此文件复制到 game/custom/scenarios/ 并重命名，开始构建
##      你自己的剧本。替换所有占位符值。
################################################################################

## EN: This init block registers the scenario with the game.
## ZH: 此 init 块向游戏注册剧本。
init -1 python:

    ## EN: Unique ID for your scenario. Use a namespace prefix to avoid conflicts.
    ## ZH: 剧本的唯一 ID。使用命名空间前缀以避免冲突。
    MY_SCENARIO_ID = "author.my_scenario"

    my_scenario = Scenario(
        scenario_id=MY_SCENARIO_ID,
        name_i18n_key="My Awesome Scenario",
        description_i18n_key="A custom scenario with unique rules and victory conditions.",
        author="Your Name",
        version="1.0.0",

        ## EN: Custom rules that override default gameplay.
        ## ZH: 覆盖默认玩法的自定义规则。
        rules={
            "max_girls": 12,           # EN: Override max working girls. ZH: 覆盖最大工作女孩数。
            "starting_chapter": 2,     # EN: Start at chapter 2. ZH: 从第 2 章开始。
            "disable_farm": False,     # EN: Set True to disable farm. ZH: 设为 True 禁用农场。
            "custom_intro_label": "my_scenario_intro",  # EN: Custom intro label. ZH: 自定义开场标签。
        },

        ## EN: Ren'Py label for scenario-specific events.
        ## ZH: 剧本专属事件的 Ren'Py 标签。
        events_script="my_scenario_events",

        ## EN: Starting conditions for the player.
        ## ZH: 玩家的起始条件。
        starting_conditions={
            "gold": 2500,
            "chapter": 2,
            "girls": 2,
        },

        ## EN: Victory conditions. At least one must be met to win.
        ## ZH: 胜利条件。至少满足一个即可获胜。
        victory_conditions=[
            {"gold_min": 50000},       # EN: Reach 50,000 gold. ZH: 达到 50,000 金币。
            {"girls_min": 20},         # EN: Acquire 20 girls. ZH: 获得 20 个女孩。
            {"chapter_min": 5},        # EN: Reach chapter 5. ZH: 达到第 5 章。
            {"custom_label": "my_scenario_victory_check"},  # EN: Custom logic. ZH: 自定义逻辑。
        ]
    )

    ## EN: Register with the Mod API.
    ## ZH: 通过 Mod API 注册。
    mod_api.register_scenario(my_scenario)


## ============================================================
## EN: Scenario intro event.
## ZH: 剧本开场事件。
## ============================================================

label my_scenario_intro:
    ## EN: This plays at the start of the game if "custom_intro_label" is set.
    ## ZH: 如果设置了 "custom_intro_label"，此标签在游戏开始时播放。

    scene black with fade

    "Welcome to My Awesome Scenario!"
    "This is where you set up the narrative framing for your custom campaign."

    return


## ============================================================
## EN: Scenario event dispatcher.
## ZH: 剧本事件调度器。
## ============================================================

label my_scenario_events:
    ## EN: This label is called periodically by the scenario mode.
    ##     Use it to trigger custom events, check conditions, etc.
    ## ZH: 此标签由剧本模式定期调用。
    ##     用于触发自定义事件、检查条件等。

    ## EN: Example: trigger a special event on day 30.
    ## ZH: 示例：在第 30 天触发特殊事件。
    if calendar.day == 30 and not story_flags.get("my_special_event_done"):
        $ story_flags["my_special_event_done"] = True
        call my_scenario_special_event

    return


label my_scenario_special_event:
    scene black with fade

    "A mysterious visitor arrives at your brothel..."

    ## EN: Add your custom event logic here.
    ## ZH: 在此添加你的自定义事件逻辑。

    return


## ============================================================
## EN: Custom victory check.
## ZH: 自定义胜利检查。
## ============================================================

label my_scenario_victory_check:
    ## EN: Return True (non-zero) if victory condition is met.
    ## ZH: 如果胜利条件满足则返回 True（非零）。

    if MC.gold >= 100000:
        return 1

    return 0
