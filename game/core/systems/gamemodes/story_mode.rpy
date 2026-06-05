################################################################################
##  Story Mode — BK Evolution
##  EN: Traditional story-driven gameplay with chapter progression.
##  ZH: 传统的剧情驱动玩法，带有章节推进机制。
################################################################################

init -9 python:

    class StoryMode(GameMode):
        """
        EN: Classic story mode. Chapters advance via goal completion.
            Story events are gated by chapter progress.
        ZH: 经典剧情模式。章节通过完成目标来推进。
            剧情事件按章节进度锁定。
        """

        def __init__(self):
            super(StoryMode, self).__init__(
                mode_id=GameMode.MODE_STORY,
                name_i18n_key="剧情模式",
                description_i18n_key="跟随主线剧情，包含章节推进和叙事目标。"
            )

        def on_game_start(self, game):
            """
            EN: Set up story mode goal channels.
            ZH: 设置剧情模式的目标频道。
            """
            game.goal_channels = (
                "story", "story2", "story3",
                "advance", "advance2",
                "papa", "contract", "other"
            )

        def can_advance_chapter(self, game):
            """
            EN: Chapter advancement requires all current goals to be reached.
            ZH: 章节推进需要完成所有当前目标。
            """
            return game.goals_reached()

        def get_goal_channels(self):
            return (
                "story", "story2", "story3",
                "advance", "advance2",
                "papa", "contract", "other"
            )

        def is_story_locked(self):
            return True

        def on_chapter_advanced(self, game, new_chapter):
            """
            EN: Set new chapter goals automatically.
            ZH: 自动设置新章节目标。
            """
            if new_chapter in chapter_goals:
                game.goals = chapter_goals[new_chapter]


    ## EN: Register story mode in the global registry.
    ## ZH: 在全局注册表中注册剧情模式。
    gamemode_registry.register(StoryMode())
