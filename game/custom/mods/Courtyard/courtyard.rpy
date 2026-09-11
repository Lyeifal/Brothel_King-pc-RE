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


    ## ============================================================
    ##  District / difficulty helpers (module level)
    ## ============================================================

    ## EN: Numeric mapping of the game's difficulty setting for the rent and
    ##     decay formulas. game.diff is one of diff_list ("very easy", "easy",
    ##     "normal", "hard", "insane") — same approach as the auction mod:
    ##     string -> index + 1 = 1-5. Unknown values fall back to 3 (normal).
    ## ZH: 租金与衰减公式所需的游戏难度数值映射。本体难度为字符串
    ##     （diff_list），按下标 +1 映射为 1-5（与拍卖 Mod 同一做法）；
    ##     未知或自定义值回退为 3（normal）。
    courtyard_difficulty_levels = ("very easy", "easy", "normal", "hard", "insane")

    def courtyard_difficulty_value():
        try:
            return courtyard_difficulty_levels.index(game.diff) + 1
        except Exception:
            return 3

    def courtyard_current_district():
        """
        EN: The district the brothel is currently in (store global "district",
            set by change_district()). Defensive: returns None when the game
            has not started or the global is missing.
        ZH: 青楼当前所在地区（store 全局 "district"，由 change_district()
            设置）。防御式：游戏未开始或全局缺失时返回 None。
        """
        try:
            return globals().get("district")
        except Exception:
            return None

    def courtyard_district_rank():
        """
        EN: Rank of the current district (1-5: Slums=1, Docks/Warehouse=2,
            Magic Gardens/Cathedra=3, The King's Hold=4, endless=5).
            Falls back to 1 (Slums pricing) when the district cannot be read.
        ZH: 当前地区的等级（1-5：贫民窟=1，码头/仓库=2，魔法花园/大教堂=3，
            王城=4，无尽模式=5）。地区读取失败时回退为 1（按贫民窟计价）。
        """
        try:
            rank = getattr(courtyard_current_district(), "rank", None)
            if isinstance(rank, (int, float)):
                return max(1, int(rank))
        except Exception:
            pass
        return 1


    class Courtyard(object):
        """
        EN: A secondary location for housing girls who are not actively working
            in the brothel. Girls here recover mood/energy slowly and can train
            at reduced efficiency.
            v2.0: Housing costs rent (scales with district rank, difficulty and
            headcount), girls left idle slowly lose skills (faster on higher
            difficulty), each district only offers a limited number of rooms,
            and a very expensive deed bought in the final district lifts the
            room cap entirely.
        ZH: 用于安置不在青楼工作的女孩的次要区域。
            这里的女孩缓慢恢复心情/能量，并可进行低效训练。
            v2.0：安置女孩需按日缴纳租金（随地区等级、难度与人数上涨）；
            闲置女孩的技能每日缓慢衰减（难度越高越快）；每个地区可租用的
            房间数量有限；在最终区域可购买天价地契解除房间上限。
        """

        ## EN: Hard cap on total girls that can be housed (used when the
        ##     expansion deed has been bought).
        ## ZH: 可安置女孩的总硬上限（购买扩建地契后启用）。
        MAX_CAPACITY = 99

        ## EN: Legacy pre-v2.0 cap, kept only for save/display fallbacks.
        ##     Use room_limit() for all capacity checks.
        ## ZH: v2.0 之前的旧硬上限，仅为存档/显示兜底保留。
        ##     所有容量检查请使用 room_limit()。
        LEGACY_CAPACITY = 50

        ## EN: Price of the villa expansion deed sold in the final district.
        ## ZH: 最终区域出售的别院扩建地契价格。
        EXPANSION_PRICE = 10000000

        ## EN: Save-compatibility defaults. Old pickles (Ren'Py restores
        ##     instances without running __init__) lack fields added in v2.0;
        ##     __getattr__ below supplies these values.
        ## ZH: 存档兼容默认值。旧存档实例（Ren'Py 恢复实例时不运行
        ##     __init__）缺少 v2.0 新增字段，由 __getattr__ 兜底。
        FIELD_DEFAULTS = {
            "expansion_unlocked": False,  ## EN: True once the deed is bought. ZH: 购得扩建地契后为 True。
        }

        ## EN: Default upkeep multiplier (50% of brothel upkeep).
        ## ZH: 默认维护费用倍率（青楼的 50%）。
        UPKEEP_MULTIPLIER = 0.5

        def __init__(self, name=None):
            self.name = name or __("Courtyard")
            self.girls = []           ## EN: Girls housed here. ZH: 安置在此的女孩。
            self.facilities = {}      ## EN: Facility ID -> CourtyardFacility. ZH: 设施 ID -> CourtyardFacility。
            self.expansion_unlocked = False  ## EN: Villa expansion deed bought. ZH: 是否已购得别院扩建地契。
            self._init_default_facilities()

        def __getattr__(self, name):
            ## EN: Old-save fallback (see FIELD_DEFAULTS). object.__getattribute__
            ##     avoids any recursion while the class is being restored.
            ## ZH: 旧存档兜底（见 FIELD_DEFAULTS）。恢复期间用
            ##     object.__getattribute__ 避免递归。
            defaults = object.__getattribute__(self, "__class__").FIELD_DEFAULTS
            if name in defaults:
                return defaults[name]
            raise AttributeError(name)

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

        def room_limit(self):
            """
            EN: Number of rooms rentable in the current district:
                   expansion bought -> MAX_CAPACITY (99)
                   otherwise        -> 4 + district_rank × 2
               District ranks: Slums=1 -> 6 rooms, Docks/Warehouse=2 -> 8,
               Magic Gardens/Cathedra=3 -> 10, The King's Hold=4 -> 12,
               endless King's Hold=5 -> 14.
               When the district cannot be determined, falls back to rank 1
               (the old Slums behaviour — 6 rooms).
            ZH: 当前地区可租用的房间数量：
                   已购扩建地契 → MAX_CAPACITY（99）
                   否则        → 4 + 地区rank × 2
               地区等级对应：贫民窟=1 → 6 间，码头/仓库=2 → 8 间，
               魔法花园/大教堂=3 → 10 间，王城=4 → 12 间，
               无尽模式王城=5 → 14 间。
               地区读取失败时回退为 rank 1（即旧版贫民窟行为——6 间）。
            """
            if self.expansion_unlocked:
                return self.MAX_CAPACITY
            return 4 + courtyard_district_rank() * 2

        def can_add_girl(self):
            """EN: Check if there's room for another girl.
               ZH: 检查是否还有空房容纳新女孩。"""
            return len(self.girls) < self.room_limit()

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

        ## EN: Stats that can decay from idleness: main stats then sex skills
        ##     (lowercase; change_stat() capitalizes to match stat names).
        ##     Defensive: the girl component is being refactored in parallel —
        ##     every girl is processed inside try/except and skipped on error.
        ## ZH: 可因闲置而衰减的属性：主属性 + 性爱技能（小写；
        ##     change_stat() 内部会首字母大写以匹配属性名）。
        ##     防御式编码：女孩组件正在并行重构，每个女孩都在 try/except
        ##     中处理，出错即跳过。
        DECAY_STATS = ("charm", "beauty", "body", "refinement", "sensitivity",
                       "libido", "constitution", "obedience",
                       "service", "sex", "anal", "fetish")

        def process_day(self):
            """
            EN: Called once per game day (via the HOOK_DAY_ENDING hook).
                Order: mood/energy recovery (existing behaviour) -> stat decay
                -> rent collection.
            ZH: 每个游戏日调用一次（经 HOOK_DAY_ENDING 钩子）。顺序：
                心情/能量恢复（原有行为）→ 属性衰减 → 收租。
            """
            for girl in list(self.girls):
                try:
                    self._recover_girl(girl)
                except Exception:
                    continue  ## EN: Skip a broken girl, keep processing others. ZH: 跳过出错的女孩，继续处理其他人。

            diff = courtyard_difficulty_value()

            for girl in list(self.girls):
                try:
                    self._decay_girl(girl, diff)
                except Exception:
                    continue

            self._collect_rent()

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

        def _decay_girl(self, girl, diff):
            """
            EN: Idle girls lose their edge: each day, every housed girl loses
                1-2 random skills/attributes by ceil(0.5 × difficulty) points
                each (difficulty 1-5 -> 1/1/2/2/3 points). Never drops below 0
                (Stat.change clamps at the stat minimum).
                Uses girl.change_stat() with negative values; falls back to
                girl.gain() if that is the only API available. All access is
                guarded — a failing girl is skipped for the day.
            ZH: 闲置女孩会松懈：每日每名安置女孩随机失去 1-2 项技能/属性，
                每项失去 ceil(0.5 × 难度档) 点（难度 1-5 → 1/1/2/2/3 点）。
                属性不会跌破下限 0（Stat.change 内部有下限钳制）。
                优先用女孩现有 API change_stat() 负值；若只有 gain() 则兜底。
                全部访问均有防御——当日处理失败则跳过该女孩。
            """
            import math

            amount = max(1, int(math.ceil(0.5 * diff)))

            picks = list(self.DECAY_STATS)
            renpy.random.shuffle(picks)
            for stat in picks[:renpy.random.randint(1, 2)]:
                change_stat = getattr(girl, "change_stat", None)
                if callable(change_stat):
                    try:
                        change_stat(stat, -amount, apply_boost=False, spillover=False, silent=True)
                        continue
                    except Exception:
                        pass
                gain = getattr(girl, "gain", None)
                if callable(gain):
                    try:
                        gain(stat, -amount)
                    except Exception:
                        pass

        ## ============================================================
        ##  Training
        ## ============================================================

        def train_girl(self, girl, skill, duration=1):
            """
            EN: Train a girl in the courtyard_villa. Efficiency is 30% of normal work training.
                Uses change_stat() with a positive value (falling back to gain()
                if that is the only API available); a failing girl is skipped.
            ZH: 在别院训练女孩。效率为正常工作训练的 30%。
                优先用 change_stat() 正值（若只有 gain() 则兜底）；
                训练失败则跳过该女孩。
            """
            if girl not in self.girls:
                return False

            training = self.facilities.get("training_ground")
            efficiency = 0.30
            if training:
                efficiency += 0.1 * training.upgrade_level

            xp_gain = 10 * duration * efficiency

            change_stat = getattr(girl, "change_stat", None)
            if callable(change_stat):
                try:
                    change_stat(skill, xp_gain, apply_boost=False, spillover=False, silent=True)
                    return True
                except Exception:
                    pass

            gain = getattr(girl, "gain", None)
            if callable(gain):
                try:
                    gain(skill, xp_gain)
                    return True
                except Exception:
                    pass

            return False

        ## ============================================================
        ##  Upkeep & Economy
        ## ============================================================

        def get_daily_upkeep(self):
            """
            EN: Calculate total daily upkeep for all courtyard girls.
                Roughly 50% of what they'd cost in the brothel.
                (Independent from rent — upkeep covers food and wages, rent
                covers the rooms. Both are charged daily.)
            ZH: 计算所有别院女孩的每日总维护费用。
                约为她们在青楼费用的 50%。
                （与租金相互独立——维护费覆盖伙食与工钱，租金覆盖房间，
                两者每日各收一次。）
            """
            total = 0
            for girl in self.girls:
                if hasattr(girl, "upkeep"):
                    total += girl.upkeep * self.UPKEEP_MULTIPLIER
                else:
                    total += 5 * self.UPKEEP_MULTIPLIER  ## EN: Default fallback. ZH: 默认回退值。
            return int(total)

        def get_daily_rent(self):
            """
            EN: Total rent due tonight for all housed girls.
                Formula (agreed design, see README.txt):
                    per_girl = 15 × district_rank × (1 + 0.20 × difficulty)
                    total    = per_girl × girl_count
                With district ranks 1-5 and difficulty 1-5, per-girl rent
                ranges from 18 (Slums, very easy) to 150 (endless Hold,
                insane) gold per day.
            ZH: 今晚应付的全部房租。
                公式（既定设计，见 README.txt）：
                    人均日租 = 15 × 地区rank × (1 + 0.20 × 难度档)
                    总租金  = 人均日租 × 女孩数
                地区 rank 1-5、难度 1-5 时，人均日租介于
                18（贫民窟·非常简单）到 150（无尽王城·疯狂）金币之间。
            """
            per_girl = 15 * courtyard_district_rank() * (1 + 0.20 * courtyard_difficulty_value())
            return int(per_girl * len(self.girls))

        def _collect_rent(self):
            """
            EN: Charge tonight's rent. If MC cannot pay in full, gold is
                drained to 0, every housed girl takes an extra -10 mood hit,
                and a warning is displayed for the unpaid difference.
                Defensive: missing MC/gold simply waives the rent.
            ZH: 收取今晚的租金。若 MC 无法全额支付，金币扣至 0 为止，
                差额部分每个安置女孩额外 -10 心情，并对差额发出警告。
                防御式：MC/金币缺失时直接免租。
            """
            rent = self.get_daily_rent()
            if rent <= 0:
                return

            mc = globals().get("MC")
            gold = getattr(mc, "gold", 0) if mc is not None else 0
            if not isinstance(gold, (int, float)):
                return

            if gold >= rent:
                mc.gold = gold - rent
                return

            ## EN: Unpaid: drain to zero, penalize mood, notify the shortage.
            ## ZH: 未付清：扣至 0，惩罚心情，并对差额发出警告。
            shortage = rent - gold
            mc.gold = 0

            for girl in list(self.girls):
                try:
                    change_mood = getattr(girl, "change_mood", None)
                    if callable(change_mood):
                        change_mood(-10)
                except Exception:
                    pass

            try:
                renpy.notify(__("Courtyard rent unpaid (%d gold short) — the girls are not pleased.") % shortage)
            except Exception:
                pass

        ## ============================================================
        ##  Villa expansion (final-district deed)
        ## ============================================================

        def is_final_district(self):
            """
            EN: True when the brothel has reached the final district. The
                King's Hold has rank 4 (rank 5 in endless mode); either the
                name or a rank >= 4 counts, read defensively.
            ZH: 青楼是否已抵达最终区域。王城 rank 为 4（无尽模式为 5）；
                名字匹配或 rank >= 4 即算数，读取全程防御式。
            """
            try:
                district = courtyard_current_district()
                if district is None:
                    return False
                if getattr(district, "name", None) == "The King's Hold":
                    return True
                rank = getattr(district, "rank", 0)
                return isinstance(rank, (int, float)) and rank >= 4
            except Exception:
                return False

        def can_buy_expansion(self):
            """EN: Deed offer is available: final district and not bought yet.
                   ZH: 地契报价可用：位于最终区域且尚未购买。"""
            return self.is_final_district() and not self.expansion_unlocked

        def buy_expansion(self):
            """
            EN: Buy the villa expansion deed for EXPANSION_PRICE (10,000,000
                gold). Raises the room cap to MAX_CAPACITY (99). The purchase
                is handled as a scene transaction + flag instead of a real
                inventory item — the item system is being reworked in
                parallel, so no item is registered (see README.txt).
                Returns (success, message).
            ZH: 以 EXPANSION_PRICE（10,000,000 金币）购买别院扩建地契，
                房间上限提升至 MAX_CAPACITY（99）。购买以场景交易 + 旗标
                实现而非真实背包道具——道具系统正在并行重构，
                不注册任何道具（见 README.txt）。
                返回 (是否成功, 消息文本)。
            """
            if self.expansion_unlocked:
                return False, __("The villa has already been expanded.")
            if not self.is_final_district():
                return False, __("No land is for sale here. Perhaps in the King's Hold...")

            mc = globals().get("MC")
            gold = getattr(mc, "gold", 0) if mc is not None else 0
            if not isinstance(gold, (int, float)) or gold < self.EXPANSION_PRICE:
                return False, __("You don't have enough gold (%d needed).") % self.EXPANSION_PRICE

            mc.gold = gold - self.EXPANSION_PRICE
            self.expansion_unlocked = True
            return True, __("The villa expansion is complete — the courtyard can now house up to [courtyard_villa.MAX_CAPACITY] girls.")

        ## ============================================================
        ##  Serialization
        ## ============================================================

        def to_dict(self):
            return {
                "name": self.name,
                "girl_ids": [getattr(g, "id", None) for g in self.girls],
                "facilities": {fid: f.upgrade_level for fid, f in self.facilities.items()},
                "expansion_unlocked": self.expansion_unlocked,
            }

        @classmethod
        def from_dict(cls, data):
            cy = cls(name=data.get("name"))
            levels = data.get("facilities", {})
            for fid, lvl in levels.items():
                if fid in cy.facilities:
                    cy.facilities[fid].upgrade_level = lvl
            cy.expansion_unlocked = bool(data.get("expansion_unlocked", False))
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
