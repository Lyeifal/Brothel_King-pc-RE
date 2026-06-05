################################################################################
##  Kidnap System — BK Evolution
##  EN: Forcible acquisition of girls, tied to the good/evil morality system.
##  ZH: 强制获取女孩，与善恶道德系统挂钩。
################################################################################

init -1 python:

    class KidnapAttempt(object):
        """
        EN: Records the outcome of a single kidnapping attempt.
        ZH: 记录单次掳走尝试的结果。
        """

        RESULT_SUCCESS = "success"
        RESULT_FAILED = "failed"
        RESULT_CAPTURED = "captured"      ## EN: MC was caught. ZH: MC 被捕。
        RESULT_FLED = "fled"              ## EN: Target escaped. ZH: 目标逃脱。

        def __init__(self, result, target_name, consequences=None):
            self.result = result
            self.target_name = target_name
            self.consequences = consequences or []
            self.date = calendar.day if calendar else 0


    class KidnapSystem(object):
        """
        EN: System for attempting to kidnap girls from the city.
            Success depends on MC's evil score, security resources, and location.
        ZH: 从城中尝试掳走女孩的系统。
            成功率取决于 MC 的邪恶值、安保资源和地点。
        """

        ## EN: Base success chance before modifiers.
        ## ZH: 调整前的基础成功率。
        BASE_CHANCE = 0.25

        def __init__(self):
            self.history = []               ## EN: Past kidnap attempts. ZH: 过去的掳走尝试。
            self.notoriety = 0              ## EN: Tracks how "wanted" MC is. ZH: 追踪 MC 的通缉程度。

        def can_kidnap(self, target, mc=None, location_security=0):
            """
            EN: Check if a kidnapping attempt is possible.

            Conditions:
            - Target is not already owned by MC.
            - MC has enough minions (security) available.
            - Target location is not heavily guarded.
            - MC has sufficient evil reputation OR is wearing a disguise.
            - MC is not currently captured/imprisoned.
            ZH: 检查掳走尝试是否可行。

            条件：
            - 目标不是 MC 已拥有的女孩。
            - MC 有足够的手下（安保）可用。
            - 目标地点不是重兵把守区。
            - MC 有足够邪恶声望 OR 穿着伪装。
            - MC 当前没有被捕/监禁。
            """
            if mc is None:
                mc = MC

            ## EN: Already owned.
            ## ZH: 已拥有。
            if hasattr(target, "name") and target in mc.girls:
                return False, __("她已经为你工作了。")

            ## EN: Need minions for the job.
            ## ZH: 需要手下执行任务。
            minions_available = getattr(mc, "minions", 0)
            if hasattr(mc, "get_effect"):
                minions_available = mc.get_effect("change", "minions", randomize=False)
            if minions_available < 1:
                return False, __("你没有足够的手下来做这件事。")

            ## EN: Location too secure.
            ## ZH: 地点太安全。
            if location_security >= 3:
                return False, __("这个区域戒备太森严了。")

            ## EN: Need evil reputation or disguise.
            ## ZH: 需要邪恶声望或伪装。
            evil_score = getattr(mc, "evil", 0)
            has_disguise = False  ## EN: TODO: check disguise item/effect. ZH: TODO: 检查伪装物品/效果。
            if evil_score < 10 and not has_disguise:
                return False, __("你缺乏无情（或一个好的伪装）来做成这件事。")

            return True, ""

        def calculate_success_chance(self, target, mc=None, location_security=0):
            """
            EN: Calculate kidnapping success chance (0.0 - 1.0).
            ZH: 计算掳走成功率（0.0 - 1.0）。
            """
            if mc is None:
                mc = MC

            chance = self.BASE_CHANCE

            ## EN: Evil score bonus (max +0.30).
            ## ZH: 邪恶值加成（最高 +0.30）。
            evil_score = getattr(mc, "evil", 0)
            chance += min(evil_score / 100.0, 0.30)

            ## EN: Minion strength bonus.
            ## ZH: 手下实力加成。
            minion_power = getattr(mc, "get_effect", lambda t, tg, **k: 0)("boost", "minion power", randomize=False)
            if minion_power:
                chance += (minion_power - 1.0) * 0.2

            ## EN: Location security penalty.
            ## ZH: 地点安保惩罚。
            chance -= location_security * 0.10

            ## EN: Notoriety penalty (repeated kidnappings increase heat).
            ## ZH: 恶名惩罚（重复掳走增加热度）。
            chance -= self.notoriety * 0.05

            ## EN: Good score penalty.
            ## ZH: 善良值惩罚。
            good_score = getattr(mc, "good", 0)
            chance -= min(good_score / 100.0, 0.25)

            return max(0.05, min(0.95, chance))

        def attempt_kidnap(self, target, mc=None, location_security=0):
            """
            EN: Attempt to kidnap a target. Returns KidnapAttempt with result.

            Outcomes:
            - Success: Target becomes MC's girl. Notoriety +1. May trigger chase event.
            - Failed: Target escapes. Notoriety +0.5. No other penalty.
            - Captured: MC is caught. Gold fine, reputation loss, possible imprisonment event.
            ZH: 尝试掳走目标。返回带结果的 KidnapAttempt。

            结果：
            - 成功：目标成为 MC 的女孩。恶名 +1。可能触发追捕事件。
            - 失败：目标逃脱。恶名 +0.5。无其他惩罚。
            - 被捕：MC 被抓。罚款、声望损失、可能触发监禁事件。
            """
            if mc is None:
                mc = MC

            can, reason = self.can_kidnap(target, mc, location_security)
            if not can:
                return KidnapAttempt(KidnapAttempt.RESULT_FAILED, getattr(target, "name", "?"),
                                     consequences=[reason])

            import random
            chance = self.calculate_success_chance(target, mc, location_security)
            roll = random.random()

            if roll < chance:
                ## EN: Success.
                ## ZH: 成功。
                self.notoriety += 1

                ## EN: Convert target to a Girl if needed.
                ## ZH: 如有需要将目标转换为 Girl。
                girl = target
                if not hasattr(target, "init_after_acquire"):
                    girl = get_rand_girl()
                    girl.name = getattr(target, "name", __("被掳走的女孩"))

                girl.original = False
                girl.init_after_acquire()
                mc.girls.append(girl)

                consequences = [__("你成功掳走了[girl.name]。")]
                if random.random() < 0.3:
                    consequences.append(__("可能有目击者看到了你..."))

                attempt = KidnapAttempt(KidnapAttempt.RESULT_SUCCESS, girl.name, consequences)
                self.history.append(attempt)
                return attempt

            elif roll < chance + 0.15:
                ## EN: Captured (15% base chance on failure).
                ## ZH: 被捕（失败时的 15% 基础几率）。
                self.notoriety += 2
                fine = int(mc.gold * 0.1) if hasattr(mc, "gold") else 500
                if hasattr(mc, "gold"):
                    mc.gold -= fine

                consequences = [
                    __("你被当局抓住了！"),
                    __("罚款[fine]金币。"),
                ]

                if hasattr(mc, "reputation"):
                    rep_loss = 20
                    mc.reputation -= rep_loss
                    consequences.append(__("失去[rep_loss]声望。"))

                attempt = KidnapAttempt(KidnapAttempt.RESULT_CAPTURED,
                                        getattr(target, "name", "?"), consequences)
                self.history.append(attempt)
                return attempt

            else:
                ## EN: Target escaped.
                ## ZH: 目标逃脱。
                self.notoriety += 0.5
                consequences = [__("你的目标逃走了。")]
                attempt = KidnapAttempt(KidnapAttempt.RESULT_FAILED,
                                        getattr(target, "name", "?"), consequences)
                self.history.append(attempt)
                return attempt

        def to_dict(self):
            return {
                "notoriety": self.notoriety,
                "history": [h.__dict__ for h in self.history],
            }

        @classmethod
        def from_dict(cls, data):
            sys = cls()
            sys.notoriety = data.get("notoriety", 0)
            ## EN: History restored as plain objects; detailed restoration optional.
            ## ZH: 历史记录恢复为简单对象；详细恢复可选。
            return sys


    ## EN: Global kidnap system instance.
    ## ZH: 全局掳走系统实例。
    kidnap_system = KidnapSystem()
