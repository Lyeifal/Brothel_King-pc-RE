################################################################################
##  Courtyard (Villa) System — BK Evolution
##  EN: A third area (besides brothel and farm) for housing excess girls.
##  ZH: 青楼和农场之外的第三区域，用于安置超编女孩。
################################################################################

init -1 python:

    ## EN: Load upgrade costs from the mod's own JSON, fallback to hardcoded values.
    ## ZH: 从 Mod 自带的 JSON 加载升级成本，失败则使用硬编码值。
    _garden_uc = {2: 500, 3: 1500}
    _hotspring_uc = {2: 800, 3: 2000}
    _training_uc = {2: 1000, 3: 2500}
    try:
        import json as _cuc_json
        with renpy.loader.load("custom/mods/Courtyard/courtyard_upgrade_costs.json") as _cuc_file:
            _cuc = _cuc_json.load(_cuc_file).get("courtyard_upgrade_costs", {})
        if _cuc.get("garden"):
            _garden_uc = {int(k): v for k, v in _cuc["garden"].items()}
        if _cuc.get("hotspring"):
            _hotspring_uc = {int(k): v for k, v in _cuc["hotspring"].items()}
        if _cuc.get("training_ground"):
            _training_uc = {int(k): v for k, v in _cuc["training_ground"].items()}
    except Exception:
        pass

    class CourtyardFacility(object):
        """
        EN: A facility within the courtyard that provides passive benefits.
        ZH: 别院内的设施，提供被动收益。
        """

        def __init__(self, facility_id, name_i18n_key, description_i18n_key,
                     effects=None, upgrade_level=1, max_level=3, upgrade_cost=None):
            self.facility_id = facility_id
            self.name_i18n_key = name_i18n_key
            self.description_i18n_key = description_i18n_key
            self.effects = effects or []      ## EN: List of Effect objects. ZH: Effect 对象列表。
            self.upgrade_level = upgrade_level
            self.max_level = max_level
            self.upgrade_cost = upgrade_cost or {}  ## EN: {level: gold_cost}. ZH: {等级: 金币花费}。

        def get_name(self):
            return __(self.name_i18n_key)

        def get_description(self):
            return __(self.description_i18n_key)

        def upgrade(self, mc):
            """
            EN: Upgrade facility if MC has enough gold.
            ZH: 若 MC 有足够金币则升级设施。
            """
            if self.upgrade_level >= self.max_level:
                return False, __("Already at max level.")

            cost = self.upgrade_cost.get(self.upgrade_level + 1, 0)
            if mc.gold < cost:
                return False, __("Not enough gold.")

            mc.gold -= cost
            self.upgrade_level += 1
            return True, __("Upgraded to level [self.upgrade_level].")

        def get_active_effects(self):
            """
            EN: Return effects scaled by upgrade level.
            ZH: 返回按升级等级缩放的效果。
            """
            scaled = []
            for eff in self.effects:
                scaled_eff = Effect(
                    type=eff.type,
                    target=eff.target,
                    value=eff.value * self.upgrade_level,
                    chance=eff.chance,
                    scales_with=eff.scales_with,
                    scope=eff.scope,
                    dice=eff.dice,
                    change_cap=eff.change_cap,
                    duration=eff.duration,
                    source=eff.source,
                )
                scaled.append(scaled_eff)
            return scaled


    class Courtyard(object):
        """
        EN: A secondary location for housing girls who are not actively working
            in the brothel. Girls here recover mood/energy slowly and can train
            at reduced efficiency.
        ZH: 用于安置不在青楼工作的女孩的次要区域。
            这里的女孩缓慢恢复心情/能量，并可进行低效训练。
        """

        ## EN: Hard cap on total girls that can be housed.
        ## ZH: 可安置女孩的总硬上限。
        MAX_CAPACITY = 50

        ## EN: Default upkeep multiplier (50% of brothel upkeep).
        ## ZH: 默认维护费用倍率（青楼的 50%）。
        UPKEEP_MULTIPLIER = 0.5

        def __init__(self, name=None):
            self.name = name or __("Courtyard")
            self.girls = []           ## EN: Girls housed here. ZH: 安置在此的女孩。
            self.facilities = {}      ## EN: Facility ID -> CourtyardFacility. ZH: 设施 ID -> CourtyardFacility。
            self._init_default_facilities()

        def _init_default_facilities(self):
            """EN: Set up default courtyard facilities.
               ZH: 设置默认别院设施。"""
            self.facilities = {
                "garden": CourtyardFacility(
                    facility_id="garden",
                    name_i18n_key="Garden",
                    description_i18n_key="A peaceful garden that improves mood recovery for all housed girls.",
                    effects=[Effect("boost", "mood recovery", 0.1, scope="courtyard")],
                    upgrade_cost=_garden_uc,
                ),
                "hotspring": CourtyardFacility(
                    facility_id="hotspring",
                    name_i18n_key="Hot Spring",
                    description_i18n_key="A soothing hot spring that boosts energy recovery.",
                    effects=[Effect("boost", "energy recovery", 0.15, scope="courtyard")],
                    upgrade_cost=_hotspring_uc,
                ),
                "training_ground": CourtyardFacility(
                    facility_id="training_ground",
                    name_i18n_key="Training Ground",
                    description_i18n_key="A quiet training area. Girls can train skills at 30%% efficiency.",
                    effects=[Effect("boost", "courtyard training", 0.3, scope="courtyard")],
                    upgrade_cost=_training_uc,
                ),
            }

        ## ============================================================
        ##  Girl Management
        ## ============================================================

        def can_add_girl(self):
            """EN: Check if there's room for another girl.
               ZH: 检查是否还有空位容纳新女孩。"""
            return len(self.girls) < self.MAX_CAPACITY

        def add_girl(self, girl):
            """
            EN: Move a girl to the courtyard_villa. Returns True on success.
            ZH: 将女孩移到别院。成功返回 True。
            """
            if not self.can_add_girl():
                return False

            ## EN: Remove from brothel active roster if present.
            ## ZH: 如果她在青楼活跃名单中，则移除。
            if girl in MC.girls:
                MC.girls.remove(girl)

            ## EN: Remove from farm if present.
            ## ZH: 如果她在农场，则移除。
            if hasattr(farm, "girls") and girl in farm.girls:
                farm.girls.remove(girl)

            ## EN: Clear her job assignment.
            ## ZH: 清除她的工作分配。
            if hasattr(girl, "set_job"):
                girl.set_job(None)

            if girl not in self.girls:
                self.girls.append(girl)

            return True

        def remove_girl(self, girl):
            """
            EN: Remove a girl from the courtyard (e.g. to move back to brothel).
            ZH: 从别院移除女孩（例如调回青楼）。
            """
            if girl in self.girls:
                self.girls.remove(girl)
                return True
            return False

        def move_to_brothel(self, girl):
            """
            EN: Move a girl from courtyard back to active brothel roster.
                Fails if brothel is at working capacity (24).
            ZH: 将女孩从别院调回青楼活跃名单。
                若青楼已达工作上限（24）则失败。
            """
            if girl not in self.girls:
                return False, __("Girl is not in the courtyard_villa.")

            ## EN: Check working capacity limit.
            ## ZH: 检查工作容量上限。
            if len(MC.girls) >= 24:
                return False, __("Brothel is at maximum working capacity (24).")

            self.remove_girl(girl)
            MC.girls.append(girl)
            if hasattr(girl, "init_after_acquire"):
                girl.init_after_acquire()

            return True, __("[girl.name] has returned to the brothel.")

        ## ============================================================
        ##  Daily Processing
        ## ============================================================

        def process_day(self):
            """
            EN: Called once per game day. Handles mood/energy recovery and training.
            ZH: 每个游戏日调用一次。处理心情/能量恢复和训练。
            """
            for girl in self.girls:
                self._recover_girl(girl)

        def _recover_girl(self, girl):
            """
            EN: Apply daily recovery effects to a courtyard girl.
            ZH: 对别院女孩应用每日恢复效果。
            """
            ## EN: Base recovery values.
            ## ZH: 基础恢复值。
            mood_recover = 5
            energy_recover = 10

            ## EN: Apply facility boosts.
            ## ZH: 应用设施加成。
            garden = self.facilities.get("garden")
            if garden:
                mood_recover *= (1.0 + 0.1 * garden.upgrade_level)

            hotspring = self.facilities.get("hotspring")
            if hotspring:
                energy_recover *= (1.0 + 0.15 * hotspring.upgrade_level)

            ## EN: Apply recovery.
            ## ZH: 应用恢复。
            if hasattr(girl, "mood"):
                girl.mood = min(getattr(girl, "mood_max", 100), girl.mood + int(mood_recover))
            if hasattr(girl, "energy"):
                girl.energy = min(getattr(girl, "energy_max", 100), girl.energy + int(energy_recover))

        ## ============================================================
        ##  Training
        ## ============================================================

        def train_girl(self, girl, skill, duration=1):
            """
            EN: Train a girl in the courtyard_villa. Efficiency is 30% of normal work training.
            ZH: 在别院训练女孩。效率为正常工作训练的 30%。
            """
            if girl not in self.girls:
                return False

            training = self.facilities.get("training_ground")
            efficiency = 0.30
            if training:
                efficiency += 0.1 * training.upgrade_level

            ## EN: Apply training (delegated to girl's existing method if available).
            ## ZH: 应用训练（如有则委托给女孩的现有方法）。
            if hasattr(girl, "gain"):
                xp_gain = 10 * duration * efficiency
                girl.gain(skill, xp_gain)

            return True

        ## ============================================================
        ##  Upkeep & Economy
        ## ============================================================

        def get_daily_upkeep(self):
            """
            EN: Calculate total daily upkeep for all courtyard girls.
                Roughly 50% of what they'd cost in the brothel.
            ZH: 计算所有别院女孩的每日总维护费用。
                约为她们在青楼费用的 50%。
            """
            total = 0
            for girl in self.girls:
                if hasattr(girl, "upkeep"):
                    total += girl.upkeep * self.UPKEEP_MULTIPLIER
                else:
                    total += 5 * self.UPKEEP_MULTIPLIER  ## EN: Default fallback. ZH: 默认回退值。
            return int(total)

        ## ============================================================
        ##  Serialization
        ## ============================================================

        def to_dict(self):
            return {
                "name": self.name,
                "girl_ids": [getattr(g, "id", None) for g in self.girls],
                "facilities": {fid: f.upgrade_level for fid, f in self.facilities.items()},
            }

        @classmethod
        def from_dict(cls, data):
            cy = cls(name=data.get("name"))
            levels = data.get("facilities", {})
            for fid, lvl in levels.items():
                if fid in cy.facilities:
                    cy.facilities[fid].upgrade_level = lvl
            return cy


    ## EN: Global courtyard instance. Named courtyard_villa (not "courtyard")
    ##     because start.rpy exposes every city location as a store global
    ##     (globals()["courtyard"] = Location("Courtyard")), which would
    ##     shadow a plain "courtyard" name.
    ## ZH: 全局别院实例。命名为 courtyard_villa 而非 "courtyard"——
    ##     start.rpy 会把每个城区地点暴露为 store 全局
    ##     （globals()["courtyard"] = Location("Courtyard")），
    ##      plain "courtyard" 名称会被其遮蔽。
    courtyard_villa = Courtyard()


    ## EN: Wrapper for Function() actions whose target returns a value.
    ##     In Ren'Py 8, a Function action whose callable returns non-None
    ##     ends the current interaction with that value as the result; the
    ##     main loop then treats it as a teleport destination and crashes
    ##     (jump expression <object>). _run discards the return value so the
    ##     interaction keeps running.
    ## ZH: 用于"被调函数会返回值"的 Function() action 的包装。
    ##     Ren'Py 8 中，Function action 的 callable 返回非 None 时会
    ##     立即结束当前交互并以该值为交互结果；主循环随后把它当作
    ##     teleport 目的地而崩溃（jump expression <对象>）。
    ##     _run 丢弃返回值，使交互继续进行。
    def _run(f, *a, **k):
        f(*a, **k)
