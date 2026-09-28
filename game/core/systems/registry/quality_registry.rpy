## BK Phase 8 — Quality Registry
## EN: Registry for item quality tiers. Framework stays in core; the default
##     0-6 tier DATA is provided by the "Item Quality" mod
##     (game/custom/mods/Item Quality/), with a hardcoded fallback copy
##     registered from game/core/data/quality.rpy (do NOT delete, see
##     docs/migration/DATA_MIGRATION.md).
## ZH: 物品品质档位注册表。框架留在核心；默认 0-6 档数据由 "Item Quality" Mod
##     提供（game/custom/mods/Item Quality/），另有硬编码回退副本由
##     game/core/data/quality.rpy 注册（勿删，见 docs/migration/DATA_MIGRATION.md）。

init -5 python:

    class QualityTier(object):
        """EN: One item quality tier. Reproduces the former quality_prefix /
               quality_modifier JSON behaviour exactly, data-driven per rank.
           ZH: 一个物品品质档位。以数据驱动方式逐档复刻原 quality_prefix /
               quality_modifier JSON 的行为。"""

        ## EN: Item rarities that keep their own value instead of being bumped
        ##     by the tier (special / unique / minion items).
        ## ZH: 不随档位提升、保持自身数值的稀有度（特殊/独特/随从物品）。
        DEFAULT_RARITY_KEEP = ("S", "U", "M")

        def __init__(self, rank, price_modifier, prefixes=None, rarity_keep=None):
            self.rank = int(rank)
            self.price_modifier = float(price_modifier)
            ## EN: adjective category -> English prefix string (e.g. "dress" -> "Ragged")
            ## ZH: 形容词类别 -> 英文前缀串（如 "dress" -> "Ragged"）
            self.prefixes = prefixes or {}
            self.rarity_keep = tuple(rarity_keep) if rarity_keep else self.DEFAULT_RARITY_KEEP

        @classmethod
        def from_dict(cls, d):
            return cls(
                rank=d.get("rank"),
                price_modifier=d.get("price_modifier", 1.0),
                prefixes=d.get("prefixes"),
                rarity_keep=d.get("rarity_keep"),
            )

        def to_dict(self):
            return {
                "rank": self.rank,
                "price_modifier": self.price_modifier,
                "prefixes": dict(self.prefixes),
                "rarity_keep": list(self.rarity_keep),
            }

        def get_prefix(self, category):
            """EN: Prefix for an adjective category, falling back to the "misc"
                   category (which covers gift/flower/toy/supplies items).
                   Returns None if no prefix is defined at all.
               ZH: 按形容词类别取前缀，缺失时回落 "misc" 类别（覆盖礼品/花/玩具/
                   补给类物品）。完全没有前缀时返回 None。"""
            return self.prefixes.get(category) or self.prefixes.get("misc")

        def apply_price(self, base_price):
            """ZH: 原 quality_modifier[rank] * base_price"""
            return round_int(self.price_modifier * base_price)

        def apply_rarity(self, rarity, min_rank):
            """EN: Rarity bump, except for the rarities listed in rarity_keep.
               ZH: 稀有度提升，rarity_keep 中的稀有度保持不变。"""
            if rarity in self.rarity_keep:
                return rarity
            return rarity + self.rank - min_rank

        def apply_effect_value(self, value):
            """EN: Effect scaling (kept un-rounded, exactly as before).
               ZH: 效果数值缩放（保持不取整，与原行为一致）。"""
            if self.rank > 0:
                return self.rank * value
            return value / 2

        def __repr__(self):
            ## EN: Developer-facing repr, not player text — hence no __() wrapper
            ##     (written with .format() to stay clear of the %-format i18n lint).
            ## ZH: 开发者调试用，非玩家可见文本，故不包 __()
            ##     （用 .format() 书写，避开 % 格式化的 i18n lint 规则）。
            return "<QualityTier rank={0} x{1}>".format(self.rank, self.price_modifier)

    class QualityRegistry(Registry):
        """EN: Registry of QualityTier objects keyed by str(rank). Later
               registrations overwrite earlier ones (Mod override mechanism).
           ZH: 按 str(rank) 键控的品质档位注册表。后注册覆盖先注册（Mod 覆盖机制）。"""

        def __init__(self):
            super(QualityRegistry, self).__init__(name="QualityRegistry")

        def register_quality(self, tier, category=None):
            """
            EN: Register a QualityTier. Overwrites the tier of the same rank.
            ZH: 注册一个品质档位，同 rank 覆盖。
            :param tier: QualityTier object
            """
            self.register(str(tier.rank), tier, category=category)
            return tier

        def get_tier(self, rank):
            return self.get(str(rank))

        def get_tiers(self):
            """EN: All tiers sorted ascending by rank.
               ZH: 按 rank 升序返回全部档位。"""
            return sorted(self.values(), key=lambda t: t.rank)

        def get_max_rank(self):
            _tiers = self.get_tiers()
            return _tiers[-1].rank if _tiers else 6

    _quality_registry = QualityRegistry()
    quality_registry = _quality_registry
    quality_tier_dict = _RegistryProxy(_quality_registry)
