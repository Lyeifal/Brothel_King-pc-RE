################################################################################
##  Customer Affix System — BK Evolution
##  EN: Three-dimensional affixes (personality + wealth + mood) with color tiers
##      and an 8-slot preference matrix.
##  ZH: 三维词缀系统（性格+财富+心情），带有颜色等级和 8 槽偏好矩阵。
################################################################################

init -1 python:

    ## ============================================================
    ## EN: Color tier definitions (white → iridescent).
    ## ZH: 颜色等级定义（白→彩）。
    ## ============================================================

    CUSTOMER_COLOR_TIERS = [
        ("white",      __("White"),      "#FFFFFF", 1.0),   # EN: Common / ZH: 普通
        ("green",      __("Green"),      "#2ECC71", 1.2),   # EN: Uncommon / ZH: 优秀
        ("blue",       __("Blue"),       "#3498DB", 1.5),   # EN: Rare / ZH: 稀有
        ("purple",     __("Purple"),     "#9B59B6", 2.0),   # EN: Epic / ZH: 史诗
        ("gold",       __("Gold"),       "#FFD700", 2.8),   # EN: Legendary / ZH: 传说
        ("orange",     __("Orange"),     "#E67E22", 4.0),   # EN: Mythic / ZH: 神话
        ("red",        __("Red"),        "#E74C3C", 6.0),   # EN: Divine / ZH: 神圣
        ("iridescent", __("Iridescent"), "#FF00FF", 10.0),  # EN: Transcendent / ZH: 超凡
    ]

    def get_tier_by_index(index):
        """EN: Get color tier tuple by index (0-7).
           ZH: 通过索引获取颜色等级元组。"""
        if 0 <= index < len(CUSTOMER_COLOR_TIERS):
            return CUSTOMER_COLOR_TIERS[index]
        return CUSTOMER_COLOR_TIERS[0]

    def get_tier_budget_multiplier(index):
        """EN: Get budget multiplier for a tier index.
           ZH: 获取等级的预算倍率。"""
        return get_tier_by_index(index)[3]


    ## ============================================================
    ## EN: Personality prefixes — affect behavior and difficulty.
    ## ZH: 性格前缀 — 影响行为和难度。
    ## ============================================================

    class CustomerPersonality(object):
        """
        EN: A personality affix that modifies customer behavior.
        ZH: 修改顾客行为的性格词缀。
        """

        def __init__(self, affix_id, name_i18n_key, description_i18n_key,
                     difficulty_mod=0, satisfaction_mod=0, budget_mod=1.0,
                     defense_mod=0, crazy_chance=0, color_shift=0):
            self.affix_id = affix_id
            self.name_i18n_key = name_i18n_key
            self.description_i18n_key = description_i18n_key
            self.difficulty_mod = difficulty_mod      ## EN: Added to diff. ZH: 加到难度上。
            self.satisfaction_mod = satisfaction_mod  ## EN: Flat satis bonus. ZH: 满意度 flat 加成。
            self.budget_mod = budget_mod              ## EN: Budget multiplier. ZH: 预算倍率。
            self.defense_mod = defense_mod            ## EN: Defense adjustment. ZH: 防御调整。
            self.crazy_chance = crazy_chance          ## EN: Extra crazy proc %. ZH: 额外疯狂触发几率。
            self.color_shift = color_shift            ## EN: Shift color tier by N. ZH: 颜色等级偏移。

        def get_name(self):
            return __(self.name_i18n_key)

        def get_description(self):
            return __(self.description_i18n_key)

        def apply(self, customer):
            """EN: Apply this personality's modifiers to a customer.
               ZH: 将此性格的修正应用到顾客上。"""
            customer.diff += self.difficulty_mod
            customer.satisfaction += self.satisfaction_mod
            customer.defense += self.defense_mod
            ## EN: Budget is scaled in set_budgets via affix system.
            ## ZH: 预算在 set_budgets 中通过词缀系统缩放。


    class PersonalityRegistry(object):
        """EN: Registry for customer personalities.
           ZH: 顾客性格注册表。"""

        def __init__(self):
            self._personalities = {}

        def register(self, p):
            self._personalities[p.affix_id] = p

        def get(self, affix_id):
            return self._personalities.get(affix_id)

        def list_all(self):
            return list(self._personalities.values())

        def random_personality(self, tier_index=0):
            """
            EN: Pick a random personality weighted by tier.
                Higher tiers can access rarer personalities.
            ZH: 按等级加权随机选择性格。
                更高等级可以访问更稀有的性格。
            """
            import random
            candidates = list(self._personalities.values())
            ## EN: Filter by minimum tier requirement (if any).
            ## ZH: 按最低等级要求过滤（如有）。
            weights = [1 + abs(p.color_shift) * 0.5 for p in candidates]
            return weighted_choice([(p, w) for p, w in zip(candidates, weights)])


    personality_registry = PersonalityRegistry()

    ## EN: Default personalities.
    ## ZH: 默认性格。
    personality_registry.register(CustomerPersonality(
        "brutal", __("Brutal"), __("Violent and demanding. Harder to satisfy but pays well."),
        difficulty_mod=5, satisfaction_mod=-1, budget_mod=1.3, defense_mod=2, crazy_chance=5, color_shift=1))
    personality_registry.register(CustomerPersonality(
        "kind", __("Kind"), __("Gentle and forgiving. Easier to satisfy but tips less."),
        difficulty_mod=-3, satisfaction_mod=1, budget_mod=0.9, defense_mod=-1, crazy_chance=-2, color_shift=0))
    personality_registry.register(CustomerPersonality(
        "drunkard", __("Drunkard"), __("Unpredictable. Low defense, high budget from liquid courage."),
        difficulty_mod=2, satisfaction_mod=0, budget_mod=1.1, defense_mod=-2, crazy_chance=3, color_shift=0))
    personality_registry.register(CustomerPersonality(
        "noble", __("Noble"), __("Refined taste. Very demanding but extremely generous."),
        difficulty_mod=8, satisfaction_mod=-1, budget_mod=1.8, defense_mod=3, crazy_chance=0, color_shift=2))
    personality_registry.register(CustomerPersonality(
        "shy", __("Shy"), __("Timid and nervous. Easy to please, modest spending."),
        difficulty_mod=-5, satisfaction_mod=0, budget_mod=0.7, defense_mod=-3, crazy_chance=-1, color_shift=0))
    personality_registry.register(CustomerPersonality(
        "pervert", __("Pervert"), __("Obsessed with one thing. High budget for favorites, hates everything else."),
        difficulty_mod=3, satisfaction_mod=0, budget_mod=1.2, defense_mod=0, crazy_chance=2, color_shift=1))
    personality_registry.register(CustomerPersonality(
        "miser", __("Miser"), __("Hates spending. Low budget, but easy to satisfy."),
        difficulty_mod=-2, satisfaction_mod=0, budget_mod=0.5, defense_mod=0, crazy_chance=0, color_shift=0))
    personality_registry.register(CustomerPersonality(
        "celebrity", __("Celebrity"), __("Famous and flamboyant. Huge budget, draws attention."),
        difficulty_mod=10, satisfaction_mod=-2, budget_mod=2.5, defense_mod=1, crazy_chance=1, color_shift=3))


    ## ============================================================
    ## EN: Mood states — affect satisfaction and tip chance.
    ## ZH: 心情状态 — 影响满意度和打赏几率。
    ## ============================================================

    class CustomerMood(object):
        """
        EN: A mood affix representing the customer's current emotional state.
        ZH: 表示顾客当前情绪状态的心情词缀。
        """

        def __init__(self, affix_id, name_i18n_key, description_i18n_key,
                     satisfaction_mod=0, tip_chance=0.0, tip_multiplier=1.0,
                     patience_mod=0, color_shift=0):
            self.affix_id = affix_id
            self.name_i18n_key = name_i18n_key
            self.description_i18n_key = description_i18n_key
            self.satisfaction_mod = satisfaction_mod
            self.tip_chance = tip_chance
            self.tip_multiplier = tip_multiplier
            self.patience_mod = patience_mod  ## EN: Affects wait tolerance. ZH: 影响等待容忍度。
            self.color_shift = color_shift

        def get_name(self):
            return __(self.name_i18n_key)

        def get_description(self):
            return __(self.description_i18n_key)


    class MoodRegistry(object):
        """EN: Registry for customer moods.
           ZH: 顾客心情注册表。"""

        def __init__(self):
            self._moods = {}

        def register(self, m):
            self._moods[m.affix_id] = m

        def get(self, affix_id):
            return self._moods.get(affix_id)

        def list_all(self):
            return list(self._moods.values())

        def random_mood(self):
            """EN: Pick a random mood. Most are neutral; extremes are rare.
               ZH: 随机选择心情。大多为中性；极端心情稀有。"""
            import random
            candidates = list(self._moods.values())
            weights = [1 + abs(m.color_shift) * 0.3 for m in candidates]
            return weighted_choice([(m, w) for m, w in zip(candidates, weights)])


    mood_registry = MoodRegistry()

    ## EN: Default moods.
    ## ZH: 默认心情。
    mood_registry.register(CustomerMood(
        "cheerful", __("Cheerful"), __("In a great mood. Easy to please, might tip."),
        satisfaction_mod=1, tip_chance=0.15, tip_multiplier=1.2, patience_mod=2, color_shift=0))
    mood_registry.register(CustomerMood(
        "neutral", __("Neutral"), __("Nothing special. Standard behavior."),
        satisfaction_mod=0, tip_chance=0.05, tip_multiplier=1.0, patience_mod=0, color_shift=0))
    mood_registry.register(CustomerMood(
        "grumpy", __("Grumpy"), __("Already annoyed. Harder to satisfy, won't tip."),
        satisfaction_mod=-1, tip_chance=0.0, tip_multiplier=0.0, patience_mod=-2, color_shift=0))
    mood_registry.register(CustomerMood(
        "angry", __("Angry"), __("Furious about something. Very demanding, may cause trouble."),
        satisfaction_mod=-2, tip_chance=0.0, tip_multiplier=0.0, patience_mod=-4, color_shift=1))
    mood_registry.register(CustomerMood(
        "ecstatic", __("Ecstatic"), __("Overjoyed! Extremely generous and forgiving."),
        satisfaction_mod=3, tip_chance=0.35, tip_multiplier=2.0, patience_mod=5, color_shift=2))
    mood_registry.register(CustomerMood(
        "depressed", __("Depressed"), __("Seeking comfort. Low expectations, but little money."),
        satisfaction_mod=0, tip_chance=0.02, tip_multiplier=0.5, patience_mod=3, color_shift=0))
    mood_registry.register(CustomerMood(
        "lustful", __("Lustful"), __("Single-minded. High sex budget, ignores entertainment."),
        satisfaction_mod=0, tip_chance=0.1, tip_multiplier=1.3, patience_mod=-1, color_shift=1))


    ## ============================================================
    ## EN: Preference Matrix — 8 slots per customer.
    ## ZH: 偏好矩阵 — 每个顾客 8 个槽位。
    ## ============================================================

    class CustomerPreferenceMatrix(object):
        """
        EN: An 8-slot preference system:
            2 best (highly preferred)
            2 secondary (moderately preferred)
            2 disliked (avoided)
            2 hated (strongly avoided)
        ZH: 8 槽位偏好系统：
            2 最佳（高度偏好）
            2 次级（中度偏好）
            2 厌恶（回避）
            2 极度厌恶（强烈回避）
        """

        def __init__(self):
            self.best = []        ## EN: List of preferred act/job names. ZH: 偏好的行为/工作名称列表。
            self.secondary = []   ## EN: Moderate preference. ZH: 中度偏好。
            self.disliked = []    ## EN: Avoided. ZH: 回避的。
            self.hated = []       ## EN: Strongly avoided. ZH: 强烈回避的。

        def generate(self, all_acts, all_jobs, girl_traits=None):
            """
            EN: Randomly populate the 8 slots from available acts and jobs.
                If girl_traits provided, may align preferences with traits.
            ZH: 从可用行为和工作中随机填充 8 个槽位。
                如提供 girl_traits，可能使偏好与特质对齐。
            """
            import random
            pool = list(all_acts) + list(all_jobs)
            if not pool:
                return

            random.shuffle(pool)

            self.best = pool[0:2]
            self.secondary = pool[2:4]
            self.disliked = pool[4:6]
            self.hated = pool[6:8]

        def get_score_modifier(self, act_or_job):
            """
            EN: Return satisfaction modifier for providing this act/job.
                Best: +2, Secondary: +1, Disliked: -1, Hated: -3, Neutral: 0
            ZH: 返回提供此行为/工作的满意度修正。
                最佳: +2, 次级: +1, 厌恶: -1, 极度厌恶: -3, 中性: 0
            """
            if act_or_job in self.best:
                return 2
            elif act_or_job in self.secondary:
                return 1
            elif act_or_job in self.disliked:
                return -1
            elif act_or_job in self.hated:
                return -3
            return 0

        def to_dict(self):
            return {
                "best": self.best,
                "secondary": self.secondary,
                "disliked": self.disliked,
                "hated": self.hated,
            }

        @classmethod
        def from_dict(cls, data):
            pm = cls()
            pm.best = data.get("best", [])
            pm.secondary = data.get("secondary", [])
            pm.disliked = data.get("disliked", [])
            pm.hated = data.get("hated", [])
            return pm


    ## ============================================================
    ## EN: Customer Affix Bundle — wraps all three dimensions.
    ## ZH: 顾客词缀包 — 封装三个维度。
    ## ============================================================

    class CustomerAffixes(object):
        """
        EN: Holds all affixes for a single customer: personality, wealth tier, mood,
            and preference matrix.
        ZH: 保存单个顾客的所有词缀：性格、财富等级、心情和偏好矩阵。
        """

        def __init__(self, personality=None, tier_index=0, mood=None, preferences=None):
            self.personality = personality or personality_registry.get("neutral")
            if self.personality is None:
                self.personality = personality_registry.get("kind")
            self.tier_index = tier_index
            self.mood = mood or mood_registry.get("neutral")
            if self.mood is None:
                self.mood = mood_registry.get("neutral")
            self.preferences = preferences or CustomerPreferenceMatrix()

        def get_color(self):
            """EN: Return hex color string for this customer's tier.
               ZH: 返回此顾客等级的十六进制颜色字符串。"""
            return get_tier_by_index(self.tier_index)[2]

        def get_tier_name(self):
            """EN: Return translated tier name.
               ZH: 返回翻译后的等级名称。"""
            return get_tier_by_index(self.tier_index)[1]

        def get_budget_multiplier(self):
            """EN: Combined budget multiplier from tier + personality + mood.
               ZH: 来自等级+性格+心情的组合预算倍率。"""
            base = get_tier_budget_multiplier(self.tier_index)
            pers = self.personality.budget_mod if self.personality else 1.0
            ## EN: Mood doesn't directly affect budget in current design.
            ## ZH: 当前设计中心情不直接影响预算。
            return base * pers

        def get_full_title(self):
            """
            EN: Return a descriptive title like "Cheerful Rich Noble".
            ZH: 返回描述性标题，如 "高兴的高贵富人"。
            """
            parts = []
            if self.mood and self.mood.affix_id != "neutral":
                parts.append(self.mood.get_name())
            if self.personality and self.personality.affix_id != "kind":
                parts.append(self.personality.get_name())
            parts.append(self.get_tier_name())
            return " ".join(parts)

        def apply_to_customer(self, customer):
            """
            EN: Apply all affix modifiers to a Customer instance.
            ZH: 将所有词缀修正应用到 Customer 实例。
            """
            if self.personality:
                self.personality.apply(customer)
            if self.mood:
                customer.satisfaction += self.mood.satisfaction_mod
            ## EN: Preferences are checked during service scoring.
            ## ZH: 偏好在服务评分时检查。

        def to_dict(self):
            return {
                "personality_id": self.personality.affix_id if self.personality else None,
                "tier_index": self.tier_index,
                "mood_id": self.mood.affix_id if self.mood else None,
                "preferences": self.preferences.to_dict(),
            }

        @classmethod
        def from_dict(cls, data):
            pers = personality_registry.get(data.get("personality_id")) if data.get("personality_id") else None
            mood = mood_registry.get(data.get("mood_id")) if data.get("mood_id") else None
            prefs = CustomerPreferenceMatrix.from_dict(data.get("preferences", {}))
            return cls(personality=pers, tier_index=data.get("tier_index", 0), mood=mood, preferences=prefs)


    ## ============================================================
    ## EN: Utility function to generate affixes for a new customer.
    ## ZH: 为新顾客生成词缀的工具函数。
    ## ============================================================

    def generate_customer_affixes(pop_rank=1, forced_tier=None):
        """
        EN: Generate a full affix bundle for a customer.
            Higher population rank tends toward higher tiers.
        ZH: 为顾客生成完整的词缀包。
            更高的人口等级倾向于更高等级。
        """
        import random

        ## EN: Determine color tier. Base chance skews by pop rank.
        ## ZH: 确定颜色等级。基础几率按人口等级偏移。
        if forced_tier is not None:
            tier = forced_tier
        else:
            ## EN: Weighted roll: higher ranks get better tiers.
            ## ZH: 加权掷骰：更高等级获得更好等级。
            tier_weights = [max(0, 8 - abs(i - (pop_rank - 1) * 1.5)) for i in range(8)]
            tier = weighted_choice([(i, w) for i, w in enumerate(tier_weights)])
            tier = max(0, min(7, tier))

        personality = personality_registry.random_personality(tier)
        mood = mood_registry.random_mood()
        prefs = CustomerPreferenceMatrix()
        prefs.generate(all_sex_acts, all_jobs)

        return CustomerAffixes(personality=personality, tier_index=tier, mood=mood, preferences=prefs)
