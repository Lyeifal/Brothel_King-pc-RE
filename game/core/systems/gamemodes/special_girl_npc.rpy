################################################################################
##  Special Girl NPC System — BK Evolution
##  EN: Distinguishes special girls from random free girls via quest chains.
##  ZH: 通过任务链将特殊女孩与随机自由女孩区分开来。
################################################################################

init -1 python:

    class SpecialGirlNPC(object):
        """
        EN: A special NPC girl encountered in the city. Unlike random free girls,
            she has a fixed identity, unique portrait, and a quest chain that
            must be completed to recruit her.
        ZH: 城中遇到的特殊 NPC 女孩。与随机自由女孩不同，她有固定身份、
            独特立绘和必须完成才能招募她的任务链。
        """

        STATUS_UNMET = "unmet"          ## EN: Not yet encountered. ZH: 尚未遇到。
        STATUS_MET = "met"              ## EN: Encountered, quest active. ZH: 已遇到，任务激活。
        STATUS_QUESTING = "questing"    ## EN: Quest chain in progress. ZH: 任务链进行中。
        STATUS_RECRUITABLE = "recruitable"  ## EN: Ready to join. ZH: 可以招募。
        STATUS_RECRUITED = "recruited"  ## EN: Already joined MC. ZH: 已加入 MC。
        STATUS_LOST = "lost"            ## EN: Quest failed or abandoned. ZH: 任务失败或放弃。

        def __init__(self, npc_id, name, description,
                     portrait_tag=None, quest_label_prefix="",
                     recruit_condition=None, min_chapter=1):
            self.npc_id = npc_id
            self.name = name
            self.description = description
            self.portrait_tag = portrait_tag      ## EN: Image tag for portrait. ZH: 立绘图片标签。
            self.quest_label_prefix = quest_label_prefix  ## EN: Prefix for quest labels. ZH: 任务标签前缀。
            self.status = self.STATUS_UNMET
            self.quest_stage = 0                  ## EN: Current quest stage (0 = not started). ZH: 当前任务阶段。
            self.recruit_condition = recruit_condition  ## EN: Optional callable. ZH: 可选的可调用条件。
            self.min_chapter = min_chapter        ## EN: Minimum chapter to appear. ZH: 出现所需最低章节。

        def can_appear(self, game):
            """
            EN: Check if this NPC can appear in the current game state.
            ZH: 检查此 NPC 是否可在当前游戏状态下出现。
            """
            if self.status == self.STATUS_RECRUITED or self.status == self.STATUS_LOST:
                return False
            if game.chapter < self.min_chapter:
                return False
            if game.game_mode and not game.game_mode.is_story_locked():
                ## EN: In sandbox/scenario, chapter gates are relaxed.
                ## ZH: 在沙盒/剧本模式中，章节限制放宽。
                pass
            return True

        def advance_quest(self):
            """
            EN: Advance to the next quest stage.
            ZH: 推进到下一任务阶段。
            """
            self.quest_stage += 1
            if self.status == self.STATUS_UNMET:
                self.status = self.STATUS_MET
            elif self.status == self.STATUS_MET:
                self.status = self.STATUS_QUESTING

        def is_recruitable(self, mc):
            """
            EN: Check if MC can recruit this girl now.
            ZH: 检查 MC 现在是否可以招募此女孩。
            """
            if self.status != self.STATUS_RECRUITABLE:
                return False
            if self.recruit_condition and not self.recruit_condition(mc):
                return False
            return True

        def recruit(self, mc):
            """
            EN: Add this special girl to MC's roster as a Girl instance.
                Returns the created Girl or None.
            ZH: 将此特殊女孩作为 Girl 实例加入 MC 队伍。
                返回创建的女孩或 None。
            """
            if not self.is_recruitable(mc):
                return None

            ## EN: Generate a Girl object with this NPC's traits.
            ## ZH: 用此 NPC 的特质生成 Girl 对象。
            girl = get_rand_girl()
            if girl:
                girl.name = self.name
                girl.original = True
                girl.original_price = girl.get_price("buy")
                girl.init_after_acquire()
                mc.girls.append(girl)
                self.status = self.STATUS_RECRUITED
            return girl

        def get_current_quest_label(self):
            """
            EN: Return the Ren'Py label for the current quest stage.
            ZH: 返回当前任务阶段的 Ren'Py 标签。
            """
            if not self.quest_label_prefix:
                return None
            return "%s_stage_%d" % (self.quest_label_prefix, self.quest_stage)

        def to_dict(self):
            return {
                "npc_id": self.npc_id,
                "status": self.status,
                "quest_stage": self.quest_stage,
            }

        @classmethod
        def from_dict(cls, data):
            ## EN: Look up the NPC definition and restore state.
            ## ZH: 查找 NPC 定义并恢复状态。
            npc = special_girl_registry.get(data.get("npc_id"))
            if npc:
                npc.status = data.get("status", cls.STATUS_UNMET)
                npc.quest_stage = data.get("quest_stage", 0)
            return npc


    class SpecialGirlRegistry(object):
        """
        EN: Registry for all special girl NPCs.
        ZH: 所有特殊女孩 NPC 的注册表。
        """

        def __init__(self):
            self._npcs = {}

        def register(self, npc):
            if not isinstance(npc, SpecialGirlNPC):
                raise TypeError("EN: Expected SpecialGirlNPC instance. ZH: 需要 SpecialGirlNPC 实例。")
            self._npcs[npc.npc_id] = npc

        def get(self, npc_id):
            return self._npcs.get(npc_id)

        def list_npcs(self):
            return list(self._npcs.values())

        def list_available(self, game):
            """EN: Return NPCs that can appear now.
               ZH: 返回现在可以出现的 NPC。"""
            return [n for n in self._npcs.values() if n.can_appear(game)]


    ## EN: Global special girl registry.
    ## ZH: 全局特殊女孩注册表。
    special_girl_registry = SpecialGirlRegistry()


    ## ============================================================
    ## EN: Built-in default special girls.
    ## ZH: 内置默认特殊女孩。
    ## ============================================================

    special_girl_registry.register(SpecialGirlNPC(
        npc_id="lost_noble",
        name=__("艾拉腊女士"),
        description=__("一位逃离包办婚姻的贵族女子。她在城中街头徘徊，对未来感到迷茫。"),
        portrait_tag="elara_portrait",
        quest_label_prefix="quest_elara",
        min_chapter=1,
    ))

    special_girl_registry.register(SpecialGirlNPC(
        npc_id="cursed_dancer",
        name=__("未来"),
        description=__("一位被诅咒永远舞动的舞者。她在寻找能打破诅咒的人——或者至少给她一个舞台。"),
        portrait_tag="mirai_portrait",
        quest_label_prefix="quest_mirai",
        min_chapter=2,
    ))

    special_girl_registry.register(SpecialGirlNPC(
        npc_id="ex_knight",
        name=__("伊尔莎军士"),
        description=__("一位被剥夺军衔的蒙羞骑士。骄傲而固执，她拒绝乞求——但她需要工作。"),
        portrait_tag="yrsa_portrait",
        quest_label_prefix="quest_yrsa",
        min_chapter=2,
    ))
