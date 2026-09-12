#### BK ITEMS AND FURNITURE ####
## Labels are used instead of Functions to make sure we are using global variables

## ITEM TYPES ##
init -2 python:
    IT_Weapon = ItemType("Weapon", usage = "wear", slot = "hands", filter = "hands", sound = s_sheath)
    IT_Dress = ItemType("Dress", usage = "wear", slot = "body", filter = "body", sound = "equip dress.ogg", adjectives = "dress")
    IT_Ring = ItemType("Ring", usage = "wear", slot = "finger", filter = "finger", sound = s_equip_item, adjectives = "ring")
    IT_Necklace = ItemType("Necklace", usage = "wear", slot = "neck", filter = "neck", sound = s_equip_item, adjectives = "necklace")
    IT_Accessory = ItemType("Accessory", usage = "wear", slot = "accessory", filter = "accessory", sound = s_equip_item, adjectives = "dress")
    IT_Toy = ItemType("Toy", usage = "auto_rest", filter = "consumable", sound = "vibro.ogg")
    IT_Supplies = ItemType("Supplies", usage = "auto_work", filter = "consumable", sound = "spell.ogg")
    IT_Food = ItemType("Food", usage = "use", filter = "consumable", sound = "crunch.ogg", adjectives = "food") # Food effects may not stack
    IT_Gift = ItemType("Gift", usage = "gift", sound = s_sigh, adjectives = "misc")
    IT_Flower = ItemType("Flower", usage = "gift", sound = s_surprise, adjectives = "misc", dir="Gift")
    IT_Misc = ItemType("Misc", usage = "use", sound = "spell.ogg", adjectives = "misc") # Misc effects may not stack
    IT_Story = ItemType("Misc", usage = None, sound = "spell.ogg", adjectives = "misc", sellable=False, giveable=False)
    IT_Passive = ItemType("Misc", usage = "wear", slot = "misc", sound = s_equip_item, adjectives = "misc", sellable=False)

    item_type_by_name = {
        "Weapon": IT_Weapon,
        "Dress": IT_Dress,
        "Ring": IT_Ring,
        "Necklace": IT_Necklace,
        "Accessory": IT_Accessory,
        "Toy": IT_Toy,
        "Supplies": IT_Supplies,
        "Food": IT_Food,
        "Gift": IT_Gift,
        "Flower": IT_Flower,
        "Misc": IT_Misc,
        "Story": IT_Story,
        "Passive": IT_Passive,
    }

    ## EN: all_equipement_types and furniture_types loaded from JSON in init python below.
    ## ZH: all_equipement_types 和 furniture_types 在下面的 init python 中从 JSON 加载。


    # Item instantiating: In an effort to save memory, all common properties of items are stored once as Items, individual instance only track equipped and charges status


    class Item(object):
        """This class holds common data for inanimate objects that the MC or girls can own."""

        def __init__(self, name, target, type, pic = None, template = False, rank = 1, max_rank = 5, rarity = 1, charges = None, price = 10000, effects = None, description = "", adjectives = None, sound = None, hidden_effect = False, pic_dir = None, sellable="type", giveable="type", usage="type", name_i18n=None):

            # Parent properties - Shared with every instance of the Item
            self.base_name = name
            self.name = name
            self.name_i18n = name_i18n if name_i18n is not None else name
            self.target = target
            self.type = type

            if pic_dir:
                self.pic_dir = pic_dir
            else:
                self.pic_dir = self.type.dir
            if pic:
                self.pic = Picture(pic, "resources/items/" + self.pic_dir + "/" + pic)
            else:
                self.pic = Picture("misc.webp", "resources/items/misc/misc.webp")

            self.template = template
            self.min_rank = rank
            self.rank = rank
            self.max_rank = max_rank
            self.rarity = rarity
            self.base_charges = charges
            self.base_price = price
            self.price = price
            if effects == None: effects = []
            self.base_effects = effects
            self.hidden_effect = hidden_effect

            ## Inherited properties from item type
            if usage == "type":
                self.usage = self.type.usage
            else:
                self.usage = usage

            ## Base charge sanity check
            if self.usage in ("use", "auto") and not self.base_charges:
                self.base_charges = 1

            self.slot = self.type.slot
            self.filter = self.type.filter

            if sellable == "type":
                self.sellable = self.type.sellable
            else:
                self.sellable = sellable
            if giveable == "type":
                self.giveable = self.type.giveable
            else:
                self.giveable = giveable

            if adjectives: # An individual item can override type adjectives and sound if necessary
                self.adjectives = adjectives
            else:
                self.adjectives = self.type.adjectives
            if sound:
                self.sound = sound
            else:
                self.sound = self.type.sound

            self.base_description = description
            self.description_i18n = description

        @classmethod
        def from_dict(cls, d):
            effects = d.get("effects", [])
            _builtin_dict = __import__('builtins').dict
            effects = [Effect.from_dict(e) if isinstance(e, _builtin_dict) else e for e in effects]
            return cls(
                name=d.get("name"),
                target=d.get("target"),
                type=item_type_by_name.get(d.get("type"), IT_Misc),
                pic=d.get("pic"),
                template=d.get("template", False),
                rank=d.get("rank", 1),
                max_rank=d.get("max_rank", 5),
                rarity=d.get("rarity", 1),
                charges=d.get("charges"),
                price=d.get("price", 10000),
                effects=effects,
                description=d.get("description_i18n", d.get("description", "")),
                adjectives=d.get("adjectives"),
                sound=d.get("sound"),
                hidden_effect=d.get("hidden_effect", False),
                pic_dir=d.get("pic_dir"),
                sellable=d.get("sellable", "type"),
                giveable=d.get("giveable", "type"),
                usage=d.get("usage", "type"),
                name_i18n=d.get("name_i18n", d.get("name")),
            )

        def to_dict(self):
            return {
                "name": self.base_name,
                "target": self.target,
                "type": self.type.name,
                "pic": self.pic.filename,
                "template": self.template,
                "rank": self.rank,
                "max_rank": self.max_rank,
                "rarity": self.rarity,
                "charges": self.base_charges,
                "price": self.base_price,
                "effects": [e.to_dict() for e in self.base_effects],
                "description": self.base_description,
                "adjectives": self.adjectives,
                "sound": self.sound,
                "hidden_effect": self.hidden_effect,
                "pic_dir": getattr(self, 'pic_dir', None),
                "sellable": self.sellable,
                "giveable": self.giveable,
                "usage": self.usage,
            }

        def get_instance(self): # generates a child item instance on the fly. Specify rank for template items.
            return ItemInstance(self)

        def get_pic(self, x = int(config.screen_height*0.0694), y = int(config.screen_height*0.0694)):
            return self.pic.get(x = x, y = y)

        def can_wear(self, type):
            if self.usage != "wear":
                return False

            elif self.target == type:
                return True

            return False

        def can_use(self, type):
            if self.usage not in ("use", "auto"):
                return False

            elif self.target == type:
                return True

            return False

        def get_key(self): # in use?
            return (self.type.name, self.rank, self.base_name, self.price)

        def get_price(self, operation): # Item property

            modifier = MC.get_modifier(operation)
            baseprice = self.price
            finalprice = round_int(baseprice * modifier)

            return finalprice

        def available_at_rank(self, rank): # Useless? Item property.
            if rank >= self.min_rank and rank <= self.max_rank:
                return True
            else:
                return False

        def generate_new_item(self, target_rank): # Creates new Item from this template item

            if self.template == True:

                ## EN: Quality tiers live in the QualityRegistry (core fallback +
                ##     "Item Quality" mod, see systems/registry/quality_registry.rpy).
                ## ZH: 品质档位存于 QualityRegistry（核心回退 + "Item Quality" Mod）。
                tier = quality_registry.get_tier(target_rank)

                if tier is None:
                    debug_notify("No quality tier registered for rank %s (%s)" % (target_rank, self.name))
                    return None

                new_it = copy.deepcopy(self)

                new_it.name = self.quality_name(tier.get_prefix(self.adjectives))
                new_it.name_i18n = new_it.name
                new_it.price = tier.apply_price(self.base_price)
                new_it.rarity = tier.apply_rarity(self.rarity, self.min_rank)

                new_it.base_effects = []

                for eff in self.base_effects:
                    eff = copy.deepcopy(eff)
                    eff.value = tier.apply_effect_value(eff.value)
                    new_it.base_effects.append(eff)

                # new_it.min_rank = max(target_rank - 2, 0)
                new_it.rank = min(target_rank, quality_registry.get_max_rank())

                ## EN: Pure-notification hook, lets Mods observe item generation.
                ## ZH: 纯通知钩子，供 Mod 观察物品生成。
                mod_api_v2.execute_hook(mod_api_v2.HOOK_ITEM_GENERATED, item=new_it, template=self, tier=tier)

                return new_it

            else:
                debug_notify("This item cannot be generated as a template (%s)" % self.name)

        def quality_name(self, prefix): # Compose the quality-prefixed name of a template item (template items only)
            ## EN: base_name is lowered on purpose (pre-existing behaviour):
            ##     generated names become item_dict keys, and transform_template
            ##     looks items up by that same lowered key. Both call sites must
            ##     go through here so the keys can never drift apart.
            ## ZH: 基名转小写是既有行为：生成名会成为 item_dict 的键，
            ##     transform_template 按同一小写键查表。两处调用都必须走本方法，
            ##     否则键不一致会 KeyError。
            _base = self.base_name.lower()
            if prefix is None:
                return __(_base)
            return __("{0} {1}").format(__(prefix), __(_base))

        def transform_template(self, target_rank): # Instantiate a new ItemInstance corresponding to a different rank (template items only)
            if self.min_rank <= target_rank <= self.max_rank:
                tier = quality_registry.get_tier(target_rank)
                if tier is None:
                    raise AssertionError("Transform item failed: no quality tier registered for rank %i (%s)" % (target_rank, self.name))
                new_name = self.quality_name(tier.get_prefix(self.adjectives))
                print("transforming " + self.name + " to " + new_name)
                return item_dict[new_name].get_instance()
            else:
                raise AssertionError("Transform item failed: Item rank %i out of bounds for %s (%i to %i)" % (target_rank, self.name, self.min_rank, self.max_rank))

        def get_acts(self, owner, counterpart): # This is a sanity check to control that only instances are called by a buy/sell interface
            raise AssertionError("Item called instead of ItemInstance: '%s' is not properly instanciated." % self.name)


    class ItemInstance(object):
        """This class is for inanimate objects that the MC or girls can own."""

        def __init__(self, parent):

            # Instance properties
            self.parent = parent
            self.equipped = False
            self.effects = parent.base_effects # copy is necessary to avoid contagion when effects are changed by perks. This is handled in girlclass equip/unequip
            self.used_up = False
            self.charges = parent.base_charges

            if parent.usage in ("use", "auto") and not self.charges:
                self.charges = 1

            self.update_description()

        def __getattr__(self, attr): # Intercepts attributes that are out of this object's namespace and addresses the request to the prototype
            # if attr.startswith('__') and attr.endswith('__'): # failsafe to avoid improper behavior when unpickling
            #     raise AttributeError
            try:
                return getattr(self, attr)
            except:
                return getattr(self.parent, attr)

        # Overriding these two methods is vital to keep the game from crashing on unpickling (reloading)
        def __getstate__(self):
            return vars(self)
        def __setstate__(self, state):
            vars(self).update(state)

        def get_instance(self):
            debug_notify("Warning: Trying to instantiate an already-existing instance (%s)" % self.parent.name)
            return self

        def update_description(self): # self.description stores the effect description only (to split the tooltips with base_description)

            if self.hidden_effect:
                self.description = ""
            else:
                self.description = get_description("", self.effects, final_dot=False)

                if self.usage in ("use", "auto"):
                    if self.charges > 1:
                        self.description += " (" + str(self.charges) + " uses left)"

            if self.usage == "gift":
                if self.description:
                    self.description += ", Gift"
                else:
                    self.description += "Gift"

        def has_effect(self, type="any", target="any"): # Item instance property (because effects can be changed by girl perks)
            for eff in self.effects:
                if (type in (eff.type, "any")) and (target in (eff.target, "any")):
                    return True
            return False

        def get_effect(self, type, target): # Item instance property (because effects can be changed by girl perks)
            return get_effect(self, type, target, iterate=True)

        def get_price(self, operation):
            mod = 1.0
            if self.parent.usage in ("use", "auto") and not self.parent.base_charges:
                self.parent.base_charges = 1
            if self.charges and self.charges != self.parent.base_charges:
                try:
                    mod = self.charges / self.parent.base_charges
                except:
                    notify("ERROR: Couldn't calculate used charge modifier for this Item (%s)" % self.name, col=c_red)

            # BK Evolution: Shop economy price multiplier
            price_mult = getattr(self, '_price_multiplier', 1.0)
            return round_int(self.parent.get_price(operation) * mod * price_mult)

        def use_me(self, nb = 1): # Item instance property
            if self.charges >= nb:
                self.charges -= nb

                if self.charges <= 0:
                    self.used_up = True
                    return "used_up"
                else:
                    return self.charges

            else:
                renpy.say("", __("Not enough charges (%s)") % str(self.charges))

                return "no charges"

            self.update_description()

        def transform(self, target_rank): # Returns an item which is a better or worse version of itself
            return self.parent.transform_template(target_rank)
            
        def get_acts(self, owner, counterpart): # Item instance property
            possible_acts = []

            if owner.type == "NPC":
                if owner in (NPC_renza, NPC_captain):
                    possible_acts.append("bargain")
                else:
                    possible_acts.append("buy")
                    if counterpart:
                        if self.can_wear(counterpart.type):
                            possible_acts.append("buy and equip")

            if counterpart and counterpart.type == "NPC":
                if self.sellable:
                    possible_acts.append("sell")

            if owner.type in ("MC", "girl"):
                if self.can_use(owner.type):
                    possible_acts.append("use")
                if self.can_wear(owner.type):
                    if not self.equipped:
                        possible_acts.append("equip")
                    else:
                        possible_acts.append("unequip")
                if counterpart and counterpart.type == "girl":
                    if self.usage == "gift":
                        possible_acts.append("gift")
                    else:
                        if self.giveable:
                            possible_acts.append("give")
                            if self.can_wear("girl"):
                                possible_acts.append("give and equip")
                        if self.can_use("girl"):
                            possible_acts.append("use on her")

            if owner.type == "girl":
                if counterpart and counterpart.type == "MC":
                    possible_acts.append("take")

            return possible_acts


## ITEMS ##

label init_items():
    # Each item exists only once as an Item object. Copies used in-game are instances of the ItemInstance object.

    python:

        # REGULAR ITEMS #

        # <MIGRATED: see data/items.rpy>


        # SPECIAL ITEMS AND FURNITURE #

        vitals_scanner = Furniture('Strange machine', type='Gizmos', pic='scanner.webp', rank=2, chapter=2, cost=[('wood', 20), ('dye', 20), ('leather', 20)], duration=4, effects=[Effect("special", "autorest", 1, scope="brothel")], base_description="This mysterious machine glows with pulsating magical energy.") #  It scans your girls automatically to make sure they are fit to work.

        billboard = Furniture('Clockwork billboard', type='Furnishing', pic='billboard.webp', rank=2, chapter=2, cost=[('wood', 40), ('dye', 25), ('leather', 10)], duration=5, effects=[Effect("special", "advanced advertising", 1, scope="brothel")], base_description="This imposing billboard is sure to draw some attention. Unlocks advanced advertising settings.") #  Unlocks advanced advertising settings

        extractor_items = {"extractor1" : Item(name="Extractor Mk I", target="MC", type=IT_Story, pic="extractor1.webp", template = False, rarity = "S", price = 5000, effects=[], description = "This strange steam machine lets you harvest wood, dye or leather automatically. Deploy on site."),
                            "extractor2" : Item(name="Extractor Mk II", target="MC", type=IT_Story, pic="extractor2.webp", template = False, rarity = "S", price = 25000, effects=[], description = "This strange steam machine lets you harvest marble, silk or ore automatically. Deploy on site."),
                            }

        mizuki_kimono = Item(name = "Mizuki's Kimono", target = 'MC', type = IT_Story, pic = 'Mizuki Kimono.webp', template = False, rank = 1, rarity = "S", price = 0, pic_dir="dress", description = "A kimono left behind by Mizuki Ike, the mysterious eldest Kunoichi.", hidden_effect = True).get_instance()

        mizuki_kimono2 = Item(name = "Mizuki's Kimono", target = 'girl', type = IT_Dress, pic = 'Mizuki Kimono.webp', template = False, rank = 1, rarity = "S", price = 1000, effects = [Effect("special", "immune", 1, chance=0.75)], description = "A kimono left behind by Mizuki Ike, the mysterious elder Kunoichi. Chance to negate hurt damage.")

        subaru_tunic = Item(name = "Subaru's Tunic", target = 'girl', type = IT_Dress, pic = 'subaru tunic.webp', template = False, rank = 1, rarity = "S", price = 1000, effects = [Effect("special", "ignore energy", 1, chance=0.25)], description = "Once worn by a fearsome kunoichi, this sturdy tunic is no longer of use to her.")

        makibishi = Item(name = "Makibishi", target = 'MC', type = IT_Misc, pic = 'bronze makibishi.webp', template = False, rank = 1, rarity = "S", price = 500, description = "Automatically catches a Kunoichi when hunting ninjas (skip minigame).", hidden_effect = True)
#                       Item(name = "Iron Makibishi", target = 'MC', type = IT_Story, pic = 'iron makibishi.webp', template = False, rank = 2, rarity = "S", price = 1000, description = "Slows down Kunoichi movements during ninja hunt (medium effect).", hidden_effect = True),
#                       Item(name = "Steel Makibishi", target = 'MC', type = IT_Story, pic = 'steel makibishi.webp', template = False, rank = 3, rarity = "S", price = 1500, description = "Slows down Kunoichi movements during ninja hunt (large effect).", hidden_effect = True),

        rep_item = Item(name = "Royal Commendation", target = "girl", type = IT_Misc, pic = 'edict.webp', template = False, rank = 1, rarity = "S", price = 1000, effects = [Effect("gain", "reputation", 10)], description = "This honorific scroll bears the seal of the Pharo royal family. Proudly displayed in a girl's room, it is sure to get people's attention.")


        ## Already instantiated items (unique items, ready to add to MC inventory). This is important if direct inventory checks are done (item X in MC.items); Not recommended otherwise

        magic_notebook = Item(name = 'Magic notebook', target = 'MC', type = IT_Passive, pic = 'Magic notebook.webp', template = False, rank = 1, rarity = "S", price = 0, effects = (Effect('special', 'notebook', 1), ), description = "This handy notebook will store all the information you know about your girls. It magically records all your thoughts. Wait, don't think about {i}that{/i}... Too late.", hidden_effect = True).get_instance()

        toy_hammer = Item(name="Hammer Of Light", target = 'MC', type = IT_Story, pic = 'toy hammer.webp', template = False, rank = 1, rarity = "S", price = 0, description = "A diminutive 'warhammer' made of cheap materials. Supposed to work against the Kunoichi, but it looks like it couldn't even whack a mole.", hidden_effect = True).get_instance()

        mania_amulet = Item(name = "Cheap charm", target = 'MC', type = IT_Story, pic = 'cheap charm.webp', template = False, rank = 1, rarity = "S", price = 10, description = "A cheap amulet found with a mysterious letter mentioning a club called 'Mania' in the guild quarter.", hidden_effect = True).get_instance()

        bast_letter = Item("Bast's love letter", "MC", type=IT_Story, pic="Scroll of etiquette.webp", template = False, rank = 1, rarity = "S", price = 0, effects = [], description = "A love letter written by Bast to her former paramour. Contains incriminating information.", hidden_effect = True).get_instance()

        blueprint_item = Item(name = 'Ancient blueprint', target = 'MC', type = IT_Story, pic = 'scanner blueprint.webp', template = False, rank = 1, rarity = "S", price = 0, effects = [], description = "An ancient blueprint written on a light yet strong paper-like material. The instructions are foreign and indecipherable, but a skilled craftsman could perhaps make sense of it.", hidden_effect = True).get_instance()

        narika_hair = Item(name = "Lock of Narika's hair", target = 'MC', type = IT_Story, pic = 'hair.webp', template = False, rank = 1, rarity = "S", price = 0, description = "A lock of pink hair, belonging to the Kunoichi prodigy Narika Shihoudou.", hidden_effect = True).get_instance()

        blue_ribbon = Item(name = "Homura's ribbon", target = 'MC', type = IT_Story, pic = 'blue ribbon.webp', template = False, rank = 1, rarity = "S", price = 0, pic_dir="necklace", description = "A ribbon given to you by Lady Henso. Tie it to a pole in the city {b}Plaza{/b} to let her know you want to see her.", hidden_effect = True).get_instance()

        earth_rune = Item(name = "Earth Rune", target = 'MC', type = IT_Story, pic = 'earth rune.webp', template = False, rank = 1, rarity = "S", price = 0, pic_dir="misc", description = "This runestone has a strong inhibitive effect on Earth magic and disorients their users. This could help you out against the Earth ninja.", hidden_effect = True).get_instance()
        water_rune = Item(name = "Water Rune", target = 'MC', type = IT_Story, pic = 'water rune.webp', template = False, rank = 1, rarity = "S", price = 0, pic_dir="misc", description = "This runestone has a strong inhibitive effect on Water magic and disorients their users. This could help you out against the Water ninja.", hidden_effect = True).get_instance()
        void_rune = Item(name = "Void Rune", target = 'MC', type = IT_Story, pic = 'void rune.webp', template = False, rank = 1, rarity = "S", price = 0, pic_dir="misc", description = "This runestone can manipulate time to slow down super fast people and objects, or something. This could help you out against the Void ninja.", hidden_effect = True).get_instance()
        fire_rune = Item(name = "Fire Rune", target = 'MC', type = IT_Story, pic = 'fire rune.webp', template = False, rank = 1, rarity = "S", price = 0, pic_dir="misc", description = "This runestone has a strong inhibitive effect on Fire magic and disorients their users. You don't know any Fire magic users, so would that really be useful to you?", hidden_effect = True).get_instance()

        MU_entry_scroll = Item(name = "M.U. registration scroll", target = 'MC', type = IT_Story, pic = 'Scroll of Gomorrah.webp', template = False, rank = 1, rarity = "S", price = 0, pic_dir="misc", description = "This scroll gives you access to the Magic University for a week.", hidden_effect = True).get_instance()

        # Chaos

        chaos_full_charge = Item(name = 'Full Power Chaos', target = 'MC', type = IT_Weapon, sellable=False, giveable=False, pic = 'Demon sword.webp', rank = 4, rarity = "S", price = 0, effects = (Effect('change', 'strength', 4), Effect('change', 'charisma', 4), Effect('change', 'spirit', 4)), description = "The blade pulses with the dark fury of the greater daemon trapped inside. It refills its energy from cavorting with girls, somehow. It is fully charged.").get_instance()
        chaos_high_charge = Item(name = 'Mid Power Chaos', target = 'MC', type = IT_Weapon, sellable=False, giveable=False, pic = 'Demon sword.webp', rank = 4, rarity = "S", price = 0, effects = (Effect('change', 'strength', 3), Effect('change', 'charisma', 3), Effect('change', 'spirit', 3)), description = "The blade pulses with the dark fury of the greater daemon trapped inside. It refills its energy from cavorting with girls, somehow. It is well charged.").get_instance()
        chaos_low_charge = Item(name = 'Low Power Chaos', target = 'MC', type = IT_Weapon, sellable=False, giveable=False, pic = 'Demon sword.webp', rank = 4, rarity = "S", price = 0, effects = (Effect('change', 'strength', 2), Effect('change', 'charisma', 2), Effect('change', 'spirit', 2)), description = "The blade pulses with the dark fury of the greater daemon trapped inside. It refills its energy from cavorting with girls, somehow. It is partially charged.").get_instance()
        chaos_no_charge = Item(name = 'Depleted Chaos', target = 'MC', type = IT_Weapon, sellable=False, giveable=False, pic = 'Demon sword.webp', rank = 4, rarity = "S", price = 0, effects = (Effect('change', 'strength', 1), Effect('change', 'charisma', 1), Effect('change', 'spirit', 1)), description = "The blade pulses with the dark fury of the greater daemon trapped inside. It refills its energy from cavorting with girls, somehow. It is not charged.").get_instance()

        # NG+ items (do not instantiate)

        seduction_potion = Item(name = "Potion of Seduction", target = 'gift', type = IT_Gift, pic = 'love potion.webp', template = False, rank = 1, rarity = "S", price = 0, effects = [Effect("potion", "seduction", 1)], pic_dir="misc", description = "This potion raises the relationship level with any free girl in the city to the next step.", sound = s_bubbling, hidden_effect = True)
        restoration_balm = Item(name = "Balm of Restoration", target = 'girl', type = IT_Misc, pic = 'monster juice.webp', template = False, rank = 1, rarity = "S", price = 0, effects = [Effect("special", "virginity", 1)], pic_dir="misc", description = "This balm is prized by the nobility. It restores a girl's virginity (in appearance, anyway).", sound = s_dress, hidden_effect = True)
        bliss_incense = Item(name = "Incense of Bliss", target = 'girl', type = IT_Misc, pic = 'extractor2.webp', template = False, rank = 1, rarity = "S", price = 0, effects = [Effect("special", "sanity", 1)], pic_dir="misc", description = "This exotic drug helps forget even the worst traumas.", sound = s_fire, hidden_effect = True)
        magic_powder = Item(name = "Magic Powder", target = 'MC', type = IT_Misc, pic = 'healing powder.webp', template = False, rank = 1, rarity = "S", price = 0, effects = [Effect("special", "MC interactions", 1)], pic_dir="misc", description = "Snort some to recover all of your AP and Mana. It's completely legal. Maybe.", sound = s_maniacal_laugh, hidden_effect = True)
        wyvern_egg = Item(name = 'Wyvern egg', target = 'girl', type = IT_Misc, pic = 'Wyvern egg.webp', template = False, rank = 1, rarity = "S", charges = 1, price = 10000, sellable=False, effects = (Effect('gain', 'perk', 1), ), description = "A dish fit for a brothel queen.", sound = s_roar) # Also used in events/gift shop


    ### TEMPLATE ITEMS ###

        # <MIGRATED: see data/items.rpy>


        # Generate variable quality items
#        all_items += generate_template_items(template_items)

        for it in template_items:
            for tier in quality_registry.get_tiers():   # EN: tiers come from QualityRegistry (core fallback + mods) | ZH: 档位来自 QualityRegistry（核心回退 + Mod）
                if it.min_rank <= tier.rank <= it.max_rank:
                    new_item = it.generate_new_item(tier.rank)
                    if new_item is not None:
                        all_items.append(new_item)

        item_dict = {it.name : it for it in all_items}

    return


## FURNITURE ##

label init_furniture():

    python:

        all_furniture = [
            Furniture('Cardboard', type='Decoration', pic='Cardboard box.webp', rank=0, chapter=0, cost=[], duration=0, effects=[Effect("allow", "beggars", 1, scope="brothel")], ),
            Furniture('Beer keg', type='Decoration', pic='Beer keg.webp', rank=0, chapter=0, cost=[], duration=0, effects=[Effect("allow", "thugs", 1, scope="brothel")], ),
            Furniture('Basic painting', type='Decoration', pic='Decorative painting.webp', rank=1, chapter=1, cost=[('wood', 1), ('dye', 1), ('leather', 1), ], duration=1, effects=[Effect("allow", "laborers", 1, scope="brothel")], ),
            Furniture('Model boat', type='Decoration', pic='Model boat.webp', rank=2, chapter=2, cost=[('wood', 2), ('dye', 2), ('leather', 2), ], duration=1, effects=[Effect("allow", "sailors", 1, scope="brothel")], ),
            Furniture('Hearth', type='Decoration', pic='Hearth.webp', rank=2, chapter=2, cost=[('wood', 4), ('leather', 4), ], duration=2, effects=[Effect("allow", "commoners", 1, scope="brothel")], ),
            Furniture('Fine painting', type='Decoration', pic='Fantasy painting.webp', rank=2, chapter=3, cost=[('wood', 4), ('dye', 12), ('leather', 4), ], duration=3, effects=[Effect("allow", "craftsmen", 1, scope="brothel")], ),
            Furniture('Wine cases', type='Decoration', pic='Wine cases.webp', rank=3, chapter=4, cost=[('wood', 6), ('dye', 6), ('silk', 4), ], duration=4, effects=[Effect("allow", "bourgeois", 1, scope="brothel")], ),
            Furniture('Model airship', type='Decoration', pic='Model airship.webp', rank=3, chapter=4, cost=[('dye', 14), ('silk', 4), ('ore', 4), ], duration=5, effects=[Effect("allow", "guild members", 1, scope="brothel")], ),
            Furniture('Master painting', type='Decoration', pic='Erotic painting.webp', rank=3, chapter=5, cost=[('wood', 6), ('dye', 6), ('silk', 8), ('ore', 4), ], duration=6, effects=[Effect("allow", "patricians", 1, scope="brothel")], ),
            Furniture('Sparkling fountain', type='Decoration', pic='Sparkling fountain.webp', rank=4, chapter=6, cost=[('leather', 6), ('marble', 12), ('ore', 4), ], duration=7, effects=[Effect("allow", "aristocrats", 1, scope="brothel")], ),
            Furniture('Armorial bearings', type='Decoration', pic='Armorial bearings.webp', rank=4, chapter=6, cost=[('dye', 6), ('marble', 6), ('silk', 12), ('diamond', 1), ], duration=8, effects=[Effect("allow", "nobles", 1, scope="brothel")], ),
            Furniture('Chapel', type='Decoration', pic='Chapel.webp', rank=5, chapter=7, cost=[('marble', 8), ('silk', 8), ('ore', 4), ('diamond', 2), ], duration=9, effects=[Effect("allow", "royals", 1, scope="brothel")], ),

            Furniture('Small bar counter', type='Furnishing', pic='bar counter1.webp', rank=2, chapter=2, cost=[('wood', 4), ('leather', 4), ], duration=1, effects=[Effect("allow", "waitress preference", 1, scope="brothel")], ),
            Furniture('Polished bar counter', type='Furnishing', pic='bar counter2.webp', rank=3, chapter=4, cost=[('wood', 4), ('dye', 4), ('leather', 4), ('marble', 4), ('ore', 2), ], duration=3, upgrade='Small bar counter', effects=[Effect("allow", "waitress preference", 2, scope="brothel")], ),
            Furniture('Varnished bar counter', type='Furnishing', pic='bar counter3.webp', rank=4, chapter=6, cost=[('wood', 6), ('marble', 6), ('ore', 12), ], duration=5, upgrade='Polished bar counter', effects=[Effect("allow", "waitress preference", 3, scope="brothel")], ),
            Furniture('Lacquered bar counter', type='Furnishing', pic='bar counter4.webp', rank=5, chapter=7, cost=[('marble', 5), ('ore', 10), ], duration=7, upgrade='Varnished bar counter', effects=[Effect("allow", "waitress preference", 5, scope="brothel")], ),
            Furniture('Small washroom', type='Furnishing', pic='washroom1.webp', rank=2, chapter=2, cost=[('dye', 8), ], duration=1, effects=[Effect("allow", "masseuse preference", 1, scope="brothel")], ),
            Furniture('Clean washroom', type='Furnishing', pic='washroom2.webp', rank=3, chapter=4, cost=[('wood', 4), ('dye', 4), ('leather', 4), ('marble', 6), ], duration=3, upgrade='Small washroom', effects=[Effect("allow", "masseuse preference", 2, scope="brothel")], ),
            Furniture('Hot washroom', type='Furnishing', pic='washroom3.webp', rank=4, chapter=6, cost=[('wood', 6), ('marble', 12), ('silk', 6), ], duration=5, upgrade='Clean washroom', effects=[Effect("allow", "masseuse preference", 3, scope="brothel")], ),
            Furniture('Luxurious washroom', type='Furnishing', pic='washroom4.webp', rank=5, chapter=7, cost=[('marble', 10), ('silk', 5), ], duration=7, upgrade='Hot washroom', effects=[Effect("allow", "masseuse preference", 5, scope="brothel")], ),
            Furniture('Small stage', type='Furnishing', pic='stage1.webp', rank=2, chapter=2, cost=[('wood', 4), ('dye', 4), ], duration=1, effects=[Effect("allow", "dancer preference", 1, scope="brothel")], ),
            Furniture('Amateur stage', type='Furnishing', pic='stage2.webp', rank=3, chapter=4, cost=[('leather', 12), ('marble', 4), ('ore', 2), ], duration=3, upgrade='Small stage', effects=[Effect("allow", "dancer preference", 2, scope="brothel")], ),
            Furniture('Theatre stage', type='Furnishing', pic='stage3.webp', rank=4, chapter=6, cost=[('leather', 6), ('marble', 6), ('silk', 12), ], duration=5, upgrade='Amateur stage', effects=[Effect("allow", "dancer preference", 3, scope="brothel")], ),
            Furniture('Opera stage', type='Furnishing', pic='stage4.webp', rank=5, chapter=7, cost=[('marble', 5), ('silk', 10), ], duration=7, upgrade='Theatre stage', effects=[Effect("allow", "dancer preference", 5, scope="brothel")], ),
            Furniture('Small tatami room', type='Furnishing', pic='tatami room1.webp', rank=2, chapter=2, cost=[('dye', 4), ('leather', 4), ], duration=1, effects=[Effect("allow", "geisha preference", 1, scope="brothel")], ),
            Furniture('Fancy tatami room', type='Furnishing', pic='tatami room2.webp', rank=3, chapter=4, cost=[('dye', 12), ('silk', 6), ], duration=3, upgrade='Small tatami room', effects=[Effect("allow", "geisha preference", 2, scope="brothel")], ),
            Furniture('Rare tatami room', type='Furnishing', pic='tatami room3.webp', rank=4, chapter=6, cost=[('dye', 6), ('silk', 12), ('ore', 6), ], duration=5, upgrade='Fancy tatami room', effects=[Effect("allow", "geisha preference", 3, scope="brothel")], ),
            Furniture('Unique tatami room', type='Furnishing', pic='tatami room4.webp', rank=5, chapter=7, cost=[('silk', 10), ('ore', 5), ], duration=7, upgrade='Rare tatami room', effects=[Effect("allow", "geisha preference", 5, scope="brothel")], ),
            Furniture('Candy dispenser', type='Furnishing', pic='dispenser1.webp', rank=2, chapter=3, cost=[('wood', 6), ('dye', 4), ('leather', 6), ], duration=2, effects=[Effect("allow", "service preference", 1, scope="brothel")], ),
            Furniture('Ice cream dispenser', type='Furnishing', pic='dispenser2.webp', rank=3, chapter=5, cost=[('wood', 10), ('leather', 5), ('marble', 8), ('ore', 10), ], duration=4, upgrade='Candy dispenser', effects=[Effect("allow", "service preference", 2, scope="brothel")], ),
            Furniture('Lollipop dispenser', type='Furnishing', pic='dispenser3.webp', rank=4, chapter=6, cost=[('leather', 6), ('marble', 8), ('ore', 12), ], duration=6, upgrade='Ice cream dispenser', effects=[Effect("allow", "service preference", 3, scope="brothel")], ),
            Furniture('Magic mint dispenser', type='Furnishing', pic='dispenser4.webp', rank=5, chapter=7, cost=[('marble', 8), ('ore', 10), ], duration=8, upgrade='Lollipop dispenser', effects=[Effect("allow", "service preference", 5, scope="brothel")], ),
            Furniture('Small erotica collection', type='Furnishing', pic='shelves1.webp', rank=2, chapter=3, cost=[('wood', 6), ('dye', 6), ('leather', 4), ], duration=2, effects=[Effect("allow", "sex preference", 1, scope="brothel")], ),
            Furniture('Curious erotica collection', type='Furnishing', pic='shelves2.webp', rank=3, chapter=5, cost=[('wood', 5), ('leather', 10), ('marble', 10), ('ore', 8), ], duration=4, upgrade='Small erotica collection', effects=[Effect("allow", "sex preference", 2, scope="brothel")], ),
            Furniture('Mysterious erotica collection', type='Furnishing', pic='shelves3.webp', rank=4, chapter=6, cost=[('wood', 6), ('marble', 12), ('ore', 8), ], duration=6, upgrade='Curious erotica collection', effects=[Effect("allow", "sex preference", 3, scope="brothel")], ),
            Furniture('Mindblowing erotica collection', type='Furnishing', pic='shelves4.webp', rank=5, chapter=7, cost=[('marble', 10), ('ore', 8), ], duration=8, upgrade='Mysterious erotica collection', effects=[Effect("allow", "sex preference", 5, scope="brothel")], ),
            Furniture('Painted venus', type='Furnishing', pic='venus1.webp', rank=2, chapter=3, cost=[('dye', 16), ], duration=2, effects=[Effect("allow", "anal preference", 1, scope="brothel")], ),
            Furniture('Marble venus', type='Furnishing', pic='venus2.webp', rank=3, chapter=5, cost=[('dye', 15), ('marble', 10), ('silk', 8), ], duration=4, upgrade='Painted venus', effects=[Effect("allow", "anal preference", 2, scope="brothel")], ),
            Furniture('Veiled venus', type='Furnishing', pic='venus3.webp', rank=4, chapter=6, cost=[('dye', 6), ('marble', 8), ('silk', 12), ], duration=6, upgrade='Marble venus', effects=[Effect("allow", "anal preference", 3, scope="brothel")], ),
            Furniture('Ardent venus', type='Furnishing', pic='venus4.webp', rank=5, chapter=7, cost=[('marble', 10), ('silk', 8), ], duration=8, upgrade='Veiled venus', effects=[Effect("allow", "anal preference", 5, scope="brothel")], ),
            Furniture('Toy wooden horse', type='Furnishing', pic='woodhorse1.webp', rank=2, chapter=3, cost=[('wood', 6), ('dye', 2), ('leather', 8), ], duration=2, effects=[Effect("allow", "fetish preference", 1, scope="brothel")], ),
            Furniture('Spiked wooden horse', type='Furnishing', pic='woodhorse2.webp', rank=3, chapter=5, cost=[('wood', 15), ('silk', 10), ('ore', 8), ], duration=4, upgrade='Toy wooden horse', effects=[Effect("allow", "fetish preference", 2, scope="brothel")], ),
            Furniture('Polished wooden horse', type='Furnishing', pic='woodhorse3.webp', rank=4, chapter=6, cost=[('wood', 6), ('silk', 12), ('ore', 8), ], duration=6, upgrade='Spiked wooden horse', effects=[Effect("allow", "fetish preference", 3, scope="brothel")], ),
            Furniture('Mobile wooden horse', type='Furnishing', pic='woodhorse4.webp', rank=5, chapter=7, cost=[('silk', 8), ('ore', 10), ], duration=8, upgrade='Polished wooden horse', effects=[Effect("allow", "fetish preference", 5, scope="brothel")], ),

            Furniture('Basic outfit', type='Utility', pic='Basic outfit.webp', rank=0, chapter=0, cost=[], duration=0, effects=[Effect("special", "advertising power", 1, scope="brothel")], ),
            Furniture('Shepherd outfit', type='Utility', pic='Shepherd outfit.webp', rank=1, chapter=1, cost=[('wood', 2), ('leather', 6), ], duration=1, upgrade='Basic outfit', effects=[Effect("special", "advertising power", 2, scope="brothel")], ),
            Furniture('Priestess outfit', type='Utility', pic='Priestess outfit.webp', rank=2, chapter=3, cost=[('dye', 8), ('leather', 12), ], duration=1, upgrade='Shepherd outfit', effects=[Effect("special", "advertising power", 3, scope="brothel")], ),
            Furniture('Skimpy outfit', type='Utility', pic='Skimpy outfit.webp', rank=3, chapter=4, cost=[('dye', 8), ('leather', 4), ('silk', 4), ], duration=3, upgrade='Priestess outfit', effects=[Effect("special", "advertising power", 4, scope="brothel")], ),
            Furniture('Slutty outfit', type='Utility', pic='Slutty outfit.webp', rank=3, chapter=5, cost=[('dye', 10), ('leather', 2), ('silk', 10), ('ore', 4), ], duration=3, upgrade='Skimpy outfit', effects=[Effect("special", "advertising power", 5, scope="brothel")], ),
            Furniture('Kimono outfit', type='Utility', pic='Kimono outfit.webp', rank=4, chapter=6, cost=[('dye', 6), ('silk', 18), ], duration=4, upgrade='Slutty outfit', effects=[Effect("special", "advertising power", 6, scope="brothel")], ),
            Furniture('Idol outfit', type='Utility', pic='Idol outfit.webp', rank=5, chapter=7, cost=[('silk', 12), ('ore', 4), ], duration=4, upgrade='Kimono outfit', effects=[Effect("special", "advertising power", 7, scope="brothel")], ),

            Furniture('Basic door', type='Utility', pic='Basic door.webp', rank=0, chapter=0, cost=[], duration=0, effects=[Effect("boost", "security", 0, scope="brothel")], ),
            Furniture('Fence', type='Utility', pic='Fence.webp', rank=1, chapter=1, cost=[('wood', 4), ('leather', 4), ], duration=1, upgrade='Basic door', effects=[Effect("boost", "security", 0.1, scope="brothel")], ),
            Furniture('Small traps', type='Utility', pic='Small traps.webp', rank=2, chapter=3, cost=[('leather', 20), ], duration=1, upgrade='Fence', effects=[Effect("boost", "security", 0.2, scope="brothel")], ),
            Furniture('Large traps', type='Utility', pic='Large traps.webp', rank=3, chapter=4, cost=[('wood', 8), ('leather', 4), ('ore', 4), ], duration=2, upgrade='Small traps', effects=[Effect("boost", "security", 0.3, scope="brothel")], ),
            Furniture('Alarm system', type='Utility', pic='Alarm system.webp', rank=3, chapter=5, cost=[('leather', 12), ('marble', 4), ('ore', 10), ], duration=2, upgrade='Large traps', effects=[Effect("boost", "security", 0.4, scope="brothel")], ),
            Furniture('Explosive traps', type='Utility', pic='Explosive traps.webp', rank=4, chapter=6, cost=[('leather', 6), ('ore', 18), ], duration=3, upgrade='Alarm system', effects=[Effect("boost", "security", 0.5, scope="brothel")], ),
            Furniture('Zap traps', type='Utility', pic='Zap traps.webp', rank=5, chapter=7, cost=[('marble', 4), ('ore', 12), ], duration=3, upgrade='Explosive traps', effects=[Effect("boost", "security", 0.6, scope="brothel")], ),

            Furniture('Basic broom', type='Utility', pic='Broom.webp', rank=0, chapter=0, cost=[], duration=0, effects=[Effect("boost", "maintenance", 0, scope="brothel")], ),
            Furniture('Buckets', type='Utility', pic='Buckets.webp', rank=1, chapter=1, cost=[('wood', 6), ('leather', 2), ], duration=1, upgrade='Basic broom', effects=[Effect("boost", "maintenance", 0.25, scope="brothel")], ),
            Furniture('Towels', type='Utility', pic='Towels.webp', rank=2, chapter=3, cost=[('dye', 5), ('leather', 5), ], duration=1, upgrade='Buckets', effects=[Effect("boost", "maintenance", 0.35, scope="brothel")], ),
            Furniture('Wheelbarrow', type='Utility', pic='Wheelbarrow.webp', rank=3, chapter=4, cost=[('wood', 4), ('dye', 4), ('leather', 4), ('ore', 4), ], duration=1, upgrade='Buckets', effects=[Effect("boost", "maintenance", 0.5, scope="brothel")], ),
            Furniture('Magic broom', type='Utility', pic='magic broom.webp', rank=3, chapter=5, cost=[('wood', 10), ('leather', 6), ('silk', 6), ], duration=2, upgrade='Wheelbarrow', effects=[Effect("boost", "maintenance", 1, scope="brothel")], ),
            Furniture('Steam cart', type='Utility', pic='Steam cart.webp', rank=4, chapter=6, cost=[('leather', 6), ('marble', 6), ('silk', 6), ('ore', 6), ], duration=2, upgrade='Wheelbarrow', effects=[Effect("boost", "maintenance", 1.5, scope="brothel")], ),
            Furniture('Mechanical maid', type='Utility', pic='Robot maid.webp', rank=5, chapter=7, cost=[('silk', 6), ('ore', 10), ], duration=3, upgrade='Steam cart', effects=[Effect("boost", "maintenance", 3, scope="brothel")], ),

            Furniture('Wood statue', type='Decoration', pic='Bronze statue.webp', rank=2, chapter=2, cost=[('wood', 4), ('dye', 4), ], duration=1, effects=[Effect("change", "brothel reputation", 6, scope="brothel")], ),
            Furniture('Marble statue', type='Decoration', pic='Silver statue.webp', rank=3, chapter=4, cost=[('dye', 15), ('marble', 6), ], duration=2, upgrade='Wood statue', effects=[Effect("change", "brothel reputation", 12, scope="brothel")], ),
            Furniture('Gold statue', type='Decoration', pic='Gold statue.webp', rank=4, chapter=6, cost=[('dye', 6), ('ore', 20), ], duration=3, upgrade='Marble statue', effects=[Effect("change", "brothel reputation", 18, scope="brothel")], ),
            Furniture('Platinum statue', type='Decoration', pic='Platinum statue.webp', rank=5, chapter=7, cost=[('ore', 20), ('diamond', 1), ], duration=4, upgrade='Gold statue', effects=[Effect("change", "brothel reputation", 24, scope="brothel")], ),

            Furniture('Crude safe', type='Utility', pic='safe1.webp', rank=1, chapter=1, cost=[('wood', 4), ('dye', 2), ('leather', 4), ], duration=2, effects=[Effect("special", "safe", 5000, scope="brothel")]),
            Furniture('Simple safe', type='Utility', pic='safe2.webp', rank=2, chapter=2, cost=[('wood', 4), ('dye', 2), ('leather', 4), ], duration=3, upgrade='Crude safe', effects=[Effect("special", "safe", 25000, scope="brothel")]),
            Furniture('Locked safe', type='Utility', pic='safe3.webp', rank=3, chapter=4, cost=[('wood', 5), ('leather', 10), ('ore', 6), ], duration=5, upgrade='Simple safe', effects=[Effect("special", "safe", 50000, scope="brothel")]),
            Furniture('Secure safe', type='Utility', pic='safe4.webp', rank=4, chapter=6, cost=[('wood', 6), ('marble', 8), ('ore', 12), ('diamond', 1), ], duration=7, upgrade='Locked safe', effects=[Effect("special", "safe", 100000, scope="brothel")]),
            Furniture('Unbreakable safe', type='Utility', pic='safe5.webp', rank=5, chapter=7, cost=[('marble', 10), ('ore', 10), ('diamond', 2), ], duration=9, upgrade='Secure safe', effects=[Effect("special", "safe", 500000, scope="brothel")]),

            Furniture('Good tools', type='Utility', pic='tools1.webp', rank=1, chapter=2, cost=[('wood', 9), ('leather', 9), ], duration=2, effects=[Effect("change", "building duration", -1, scope="brothel")]),
            Furniture('Great tools', type='Utility', pic='tools2.webp', rank=3, chapter=4, cost=[('wood', 12), ('leather', 12), ("ore", 12)], duration=4, upgrade="Good tools", effects=[Effect("change", "building duration", -2, scope="brothel")]),
            Furniture('Master tools', type='Utility', pic='tools3.webp', rank=4, chapter=6, cost=[("diamond", 5), ('wood', 15), ('leather', 15), ("ore", 15)], duration=6, upgrade="Great tools", effects=[Effect("change", "building duration", -3, scope="brothel")]),

            Furniture('Glass window', type='Windows', pic='glass1.webp', rank=2, chapter=3, cost=[('wood', 5), ('dye', 5), ('leather', 5), ], duration=3, effects=[Effect("boost", "naked preference increase", 0.25, scope="brothel")], ),
            Furniture('Persian window', type='Windows', pic='oriental1.webp', rank=2, chapter=3, cost=[('wood', 6), ('dye', 6), ('leather', 6), ], duration=3, effects=[Effect("boost", "service preference increase", 0.25, scope="brothel")], ),
            Furniture('Mirror', type='Windows', pic='mirror1.webp', rank=2, chapter=3, cost=[('wood', 7), ('dye', 7), ('leather', 7), ], duration=4, effects=[Effect("boost", "sex preference increase", 0.25, scope="brothel")], ),
            Furniture('Red curtains', type='Windows', pic='red curtains1.webp', rank=2, chapter=3, cost=[('wood', 6), ('dye', 10), ('leather', 6), ], duration=4, effects=[Effect("boost", "anal preference increase", 0.25, scope="brothel")], ),
            Furniture('Barred window', type='Windows', pic='barred1.webp', rank=2, chapter=3, cost=[('wood', 10), ('dye', 7), ('leather', 7), ], duration=4, effects=[Effect("boost", "fetish preference increase", 0.25, scope="brothel")], ),
            Furniture('Double window', type='Windows', pic='double window1.webp', rank=2, chapter=3, cost=[('wood', 12), ('dye', 6), ('leather', 6), ], duration=5, effects=[Effect("boost", "bisexual preference increase", 0.25, scope="brothel")], ),
            Furniture('Stained glass', type='Windows', pic='stainglass1.webp', rank=2, chapter=3, cost=[('wood', 10), ('dye', 8), ('leather', 8), ], duration=5, effects=[Effect("boost", "group preference increase", 0.25, scope="brothel")], ),
            Furniture('Glass window XL', type='Windows', pic='glass2.webp', rank=3, chapter=5, cost=[('wood', 5), ('dye', 10), ('marble', 6), ('silk', 6), ], duration=5, upgrade='Glass window', effects=[Effect("boost", "naked preference increase", 0.5, scope="brothel")], ),
            Furniture('Persian window XL', type='Windows', pic='oriental2.webp', rank=3, chapter=5, cost=[('wood', 10), ('leather', 5), ('marble', 5), ('silk', 10), ], duration=5, upgrade='Persian window', effects=[Effect("boost", "service preference increase", 0.5, scope="brothel")], ),
            Furniture('Mirror XL', type='Windows', pic='mirror2.webp', rank=3, chapter=5, cost=[('dye', 5), ('leather', 10), ('silk', 5), ('ore', 12), ], duration=6, upgrade='Mirror', effects=[Effect("boost", "sex preference increase", 0.5, scope="brothel")], ),
            Furniture('Red curtains XL', type='Windows', pic='red curtains2.webp', rank=3, chapter=5, cost=[('dye', 10), ('silk', 18), ], duration=6, upgrade='Red curtains', effects=[Effect("boost", "anal preference increase", 0.5, scope="brothel")], ),
            Furniture('Barred window XL', type='Windows', pic='barred2.webp', rank=3, chapter=5, cost=[('wood', 10), ('leather', 5), ('marble', 10), ('ore', 10), ], duration=6, upgrade='Barred window', effects=[Effect("boost", "fetish preference increase", 0.5, scope="brothel")], ),
            Furniture('Double window XL', type='Windows', pic='double window2.webp', rank=3, chapter=5, cost=[('leather', 15), ('marble', 10), ('silk', 6), ('ore', 6), ], duration=7, upgrade='Double window', effects=[Effect("boost", "bisexual preference increase", 0.5, scope="brothel")], ),
            Furniture('Stained glass XL', type='Windows', pic='stainglass2.webp', rank=3, chapter=5, cost=[('dye', 15), ('marble', 5), ('silk', 5), ('ore', 14), ], duration=7, upgrade='Stained glass', effects=[Effect("boost", "group preference increase", 0.5, scope="brothel")], ),

            Furniture('Washtub', type='Comfort', pic='Washtub.webp', rank=1, chapter=1, cost=[('wood', 3), ('dye', 3), ], duration=1, effects=[Effect("boost", "energy when resting", 0.1, scope="brothel")], ),
            Furniture('Large washtub', type='Comfort', pic='Washtub2.webp', rank=1, chapter=3, cost=[('wood', 6), ('dye', 6), ], duration=2, upgrade='Washtub', effects=[Effect("boost", "energy when resting", 0.2, scope="brothel")], ),
            Furniture('Bathtub', type='Comfort', pic='Bathtub.webp', rank=3, chapter=4, cost=[('dye', 10), ('marble', 5), ], duration=3, upgrade='Large washtub', effects=[Effect("boost", "energy when resting", 0.3, scope="brothel")], ),
            Furniture('Fancy bathtub', type='Comfort', pic='fancy bathtub.webp', rank=3, chapter=4, cost=[('dye', 20), ('marble', 10), ], duration=4, upgrade='Bathtub', effects=[Effect("boost", "energy when resting", 0.4, scope="brothel")], ),
            Furniture('Royal bathtub', type='Comfort', pic='Royal bathtub.webp', rank=4, chapter=6, cost=[('dye', 10), ('marble', 15), ('silk', 15), ('diamond', 1), ], duration=6, upgrade='Fancy bathtub', effects=[Effect("boost", "energy when resting", 0.5, scope="brothel")], ),
            Furniture('Steam jacuzzi', type='Comfort', pic='Steam jacuzzi.webp', rank=5, chapter=7, cost=[('marble', 20), ('silk', 20), ('ore', 20), ('diamond', 3), ], duration=8, upgrade='Royal bathtub', effects=[Effect("boost", "energy when resting", 0.6, scope="brothel")], ),

            ## Old version ##
            # Furniture('Washtub', type='Comfort', pic='Washtub.webp', rank=1, chapter=1, cost=[('wood', 4), ('dye', 4), ], duration=1, effects=[Effect("boost", "energy use", -0.1, scope="brothel")], ),
            # Furniture('Bathtub', type='Comfort', pic='Bathtub.webp', rank=3, chapter=4, cost=[('dye', 15), ('marble', 6), ], duration=3, upgrade='Washtub', effects=[Effect("boost", "energy use", -0.2, scope="brothel")], ),
            # Furniture('Royal bathtub', type='Comfort', pic='Royal bathtub.webp', rank=4, chapter=6, cost=[('dye', 8), ('marble', 15), ('silk', 15), ('diamond', 1), ], duration=5, upgrade='Bathtub', effects=[Effect("boost", "energy use", -0.3, scope="brothel")], ),
            # Furniture('Steam jacuzzi', type='Comfort', pic='Steam jacuzzi.webp', rank=5, chapter=7, cost=[('marble', 20), ('silk', 20), ('ore', 20), ('diamond', 3), ], duration=7, upgrade='Royal bathtub', effects=[Effect("boost", "energy use", -0.4, scope="brothel")], ),
            ##             ##

            Furniture('Simple bench', type='Comfort', pic='bench1.webp', rank=2, chapter=3, cost=[('wood', 25), ], duration=2, effects=[Effect("change", "job customer capacity", 1, scope="brothel")], ),
            Furniture('Large bench', type='Comfort', pic='bench2.webp', rank=3, chapter=5, cost=[('wood', 10), ('leather', 6), ('marble', 15), ('ore', 10), ], duration=4, upgrade='Simple bench', effects=[Effect("change", "job customer capacity", 2, scope="brothel")], ),
            Furniture('Comfortable sofa', type='Comfort', pic='sofa1.webp', rank=4, chapter=6, cost=[('leather', 10), ('silk', 20), ('diamond', 1), ], duration=6, upgrade='Large bench', effects=[Effect("change", "job customer capacity", 3, scope="brothel")], ),
            Furniture('Royal sofa', type='Comfort', pic='sofa2.webp', rank=5, chapter=7, cost=[('marble', 8), ('silk', 15), ('diamond', 2), ], duration=8, upgrade='Comfortable sofa', effects=[Effect("change", "job customer capacity", 4, scope="brothel")], ),

            Furniture('Comfortable bed', type='Comfort', pic='bed1.webp', rank=3, chapter=4, cost=[('wood', 12), ('leather', 10), ('silk', 6), ], duration=5, effects=[Effect("change", "whore customer capacity", 1, scope="brothel")], ),
            Furniture('Queen size bed', type='Comfort', pic='bed2.webp', rank=5, chapter=7, cost=[('marble', 10), ('silk', 20), ('diamond', 3), ], duration=10, upgrade='Comfortable bed', effects=[Effect("change", "whore customer capacity", 2, scope="brothel")], ),

            Furniture('Shoddy Altar of Mana', type='Altars', pic='mana altar1.webp', rank=2, chapter=2, cost=[('wood', 2), ('dye', 2), ('leather', 4), ], duration=2, effects=[Effect("change", "mana", 1, scope="brothel")], ),
            Furniture('Working Altar of Mana', type='Altars', pic='mana altar2.webp', rank=3, chapter=4, cost=[('leather', 15), ('marble', 3), ('silk', 2), ('ore', 1), ], duration=4, upgrade='Shoddy Altar of Mana', effects=[Effect("change", "mana", 2, scope="brothel")], ),
            Furniture('Powerful Altar of Mana', type='Altars', pic='mana altar3.webp', rank=4, chapter=6, cost=[('dye', 6), ('marble', 4), ('silk', 8), ('ore', 4), ('diamond', 1), ], duration=6, upgrade='Working Altar of Mana', effects=[Effect("change", "mana", 3, scope="brothel")], ),
            Furniture('Devastating Altar of Mana', type='Altars', pic='mana altar4.webp', rank=5, chapter=7, cost=[('marble', 6), ('silk', 6), ('ore', 6), ('diamond', 2), ], duration=8, upgrade='Powerful Altar of Mana', effects=[Effect("change", "mana", 4, scope="brothel")], ),

            Furniture('Weapon rack', type='Utility', pic='weapon rack1.webp', rank=2, chapter=2, cost=[('dye', 2), ('leather', 4), ], duration=1, effects=[Effect("change", "defense", 1, scope="brothel")], ),
            Furniture('Weapon rack XL', type='Utility', pic='weapon rack2.webp', rank=4, chapter=6, cost=[('wood', 6), ('marble', 10), ('ore', 12), ], duration=3, upgrade='Weapon rack', effects=[Effect("change", "defense", 2, scope="brothel")], ),

            Furniture('Small dressing', type='Comfort', pic='dressing1.webp', rank=1, chapter=1, cost=[('wood', 4), ('dye', 4), ('leather', 2), ], duration=2, effects=[Effect("boost", "upkeep", -0.05, scope="brothel")], ),
            Furniture('Fancy dressing', type='Comfort', pic='dressing2.webp', rank=3, chapter=4, cost=[('wood', 10), ('dye', 5), ('marble', 2), ('silk', 6), ], duration=4, upgrade='Small dressing', effects=[Effect("boost", "upkeep", -0.1, scope="brothel")], ),
            Furniture('Noble dressing', type='Comfort', pic='dressing3.webp', rank=4, chapter=6, cost=[('leather', 6), ('marble', 20), ('silk', 5), ], duration=6, upgrade='Fancy dressing', effects=[Effect("boost", "upkeep", -0.15, scope="brothel")], ),

            Furniture('Dim lights', type='Comfort', pic='dim.webp', rank=3, chapter=4, cost=[('wood', 5), ('leather', 10), ('silk', 4), ('ore', 2), ], duration=3, effects=[Effect("boost", "customer events", 0.5, scope="brothel"), Effect("boost", "crazy", 1, scope="brothel")], can_deactivate=True),
            Furniture('Bright lights', type='Comfort', pic='bright.webp', rank=3, chapter=4, cost=[('wood', 10), ('leather', 5), ('silk', 2), ('ore', 4), ], duration=3, effects=[Effect("boost", "customer events", -1, scope="brothel"), Effect("boost", "crazy", -0.5, scope="brothel")], can_deactivate=True),

            Furniture('Simple Bookcase', type='Comfort', pic='bookshelf1.webp', rank=1, chapter=1, cost=[('wood', 4), ('dye', 4), ('leather', 4), ], duration=3, effects=[Effect("set", "all skill max", 60, scope="brothel"), Effect("set", "all skill max", 60, scope="farm")], ),
            Furniture('Engraved Bookcase', type='Comfort', pic='bookshelf2.webp', rank=3, chapter=4, cost=[('wood', 15), ('leather', 10), ('marble', 5), ('ore', 5), ], duration=6, upgrade='Simple Bookcase', effects=[Effect("set", "all skill max", 115, scope="brothel"), Effect("set", "all skill max", 115, scope="farm")], ),
            Furniture('Opulent Bookcase', type='Comfort', pic='bookshelf3.webp', rank=4, chapter=6, cost=[('wood', 6), ('marble', 15), ('silk', 5), ('ore', 5), ('diamond', 2), ], duration=9, upgrade='Engraved Bookcase', effects=[Effect("set", "all skill max", 170, scope="brothel"), Effect("set", "all skill max", 170, scope="farm")], ),
            Furniture('Lavish Bookcase', type='Comfort', pic='bookshelf4.webp', rank=5, chapter=7, cost=[('marble', 15), ('silk', 5), ('ore', 5), ('diamond', 4), ], duration=12, upgrade='Opulent Bookcase', effects=[Effect("set", "all skill max", 225, scope="brothel"), Effect("set", "all skill max", 225, scope="farm")], ),

            ]

        furniture_dict = {}
        for furn in all_furniture:
            furniture_dict[furn.name] = furn

    return


## INVENTORY SCREENS ##

screen item_tab(context, left_party, right_party): # Where X_party are a list of inventory-holding characters

    zorder 5

    default show_search_left = False
    default show_search_right = False

    if right_focus:
        default display_stats = right_focus
    else:
        default display_stats = left_focus

    ## Add contextual UI elements

    use overlay(context)

    if context == "shop":
        if story_flags["shop restock"]:
            use restock_button(right_focus, upgrade=True)

    elif context in ("visit_location", "city_merchant", "minion_merchant"): # Merchants
        if story_flags["shop restock"]:
            use restock_button(right_focus)

    elif context == "girls":
        textbutton _("Collect all items") text_size res_font(16) xalign 0.5 yalign 0.1 tooltip _("This will collect non-equipped items from all girls and store them in the left character's inventory.") action Return("collect all")

    key "mouseup_3" action (Return("back"))
    use close(Return("back"))
    use shortcuts()

    fixed:
        if left_focus:
            vbox xsize xres(255) xalign 0.0 ypos 0.1:
                hbox xfill True ysize yres(80) xalign 0.0:
                    use universal_selector(party=left_party, current=left_focus, var="left_focus", avoid=right_focus, sc_prefix="shift_") id "sel1"
                hbox spacing xres(6) xalign 0.0:
                    frame xsize xres(38) ysize yres(20) xpadding 0 ypadding 0 xmargin 0 ymargin 0:
                        textbutton {True: "Hide", False: "Search"}[show_search_left] text_xalign 0.5 text_italic True text_color c_darkbrown text_size res_font(14) xpadding 0 ypadding 0 xalign 0.5 yalign 0.6 xsize xres(38) ysize yres(20) idle_background None action (ToggleScreenVariable("show_search_left"), SetField(MC, "active_text_filter", ""), SelectedIf(show_search_left))
                    use sorting_tab(context + " items", sort_target=left_focus.items, sorters=["type", "price", "alpha"]) id "st1"
                hbox xalign 0.0:
                    use item_list(items=left_focus.items, owner=left_focus, counterpart=right_focus, sc_prefix="shift_", search=show_search_left) id "il1"
                    use item_filter() id "if1"
                    if left_focus.type in ("MC", "girl"):
                        use inventory(left_focus, counterpart=right_focus) id "inv1"

        if right_focus:
            vbox xsize xres(255) xalign 1.0 ypos 0.1:
                hbox ysize yres(80) xalign 1.0:
                    use universal_selector(party=right_party, current=right_focus, var="right_focus", avoid=left_focus, sc_prefix="noshift_") id "sel2"
                hbox xalign 1.0:
                    use sorting_tab(context + " items", sort_target=right_focus.items, sorters=["type", "price", "alpha"]) id "st2"
                hbox xalign 1.0:
                    if right_focus.type in ("MC", "girl"):
                        use inventory(right_focus, counterpart=left_focus) id "inv2"
                    use item_filter() id "if2"
                    use item_list(items=right_focus.items, owner=right_focus, counterpart=left_focus, sc_prefix="noshift_") id "il2"

screen universal_selector:

    zorder 5

    $ previous = get_previous(party, current, loop=True, avoid=avoid)
    $ next = get_next(party, current, loop=True, avoid=avoid)

    # hbox xfill True ysize yres(80) xalign algn:
    if previous != current:
        key sc_prefix + "K_LEFT" action (SetVariable(var, previous), Return((var, "cycle_left")))

        textbutton "<" ysize yres(80) xalign 0.0 yalign 0.5:
            action (SetVariable(var, previous), Return((var, "cycle_left")))
            if sc_prefix == "shift_":
                tooltip "Use shift + left/right arrow keys to change the focused character."
            else:
                tooltip "Use left/right arrow keys to change the focused character."


    frame xalign 0.0 yfill True ypadding 0 ymargin 0:
        xfill True

        has hbox
        yalign 0.5
        spacing 12

        if current.type == "MC":
            $ por = Picture(path=playerclass_pics[MC.playerclass]).get()
        elif current.type == "girl":
            $ por = current.portrait.get()
        else: # NPC
            $ por = current.portrait

        # frame xsize yres(80) ysize yres(80) xfill True ypadding 0 ymargin 0 xalign 0.5 yalign 0.5:
        if por != None:
            fixed xsize yres(70) ysize yres(70) xalign 0.5 yalign 0.5:
                add por xalign 0.5 yalign 0.5 fit "contain"

                if current.type == "girl":
                    $ badge = current.get_badge()
                    if badge:
                        add ProportionalScale(badge, *res_tb(30)) xalign 0.9 yalign 0.1

        if current.type == "MC":
            $ text1 = "{b}%s{/b}\n" % current.name + MC.playerclass + " level " + str(current.level)
            $ col = c_main
            $ sz = 20

        elif current.type == "girl":
            $ text1 = __("{b}%s{/b}\nRank %s - Level %s") % (current.fullname, rank_name[current.rank], current.level)
            $ col = c_brown
            $ sz = 16

            if current.job:
                $ text1 += "\n%s" % __(current.job.capitalize())
                if current.job in all_jobs and current.work_whore:
                    $ text1 += __("/Whore")
                $ sched = current.workdays[calendar.get_weekday()]

            else:
                $ text1 += __("\nNo job")
                $ sched = 0

            if current.away:
                $ text1 += __(" (away)")
            elif current.hurt > 0:
                $ text1 += __(" (hurt)")
            elif current.exhausted > 0:
                $ text1 += __(" (tired)")
            elif current.resting or sched == 0:
                $ text1 += __(" (resting)")
            elif sched == 50:
                $ text1 += __(" (half-shift)")
        else:
            $ text1 = "{b}%s{/b}\n" % capitalize(current.name) + merchant_title[current.id]
            $ col = c_darkpurple
            $ sz = 20

        text text1 size res_font(sz) xalign 0.0 ypos 0.1 yanchor 0.0 color col

    if next != current:
        key sc_prefix + "K_RIGHT" capture True action (SetVariable(var, next), Return((var, "cycle_right")))

        textbutton ">" ysize yres(80) xalign 1.0 yalign 0.5:
            action (SetVariable(var, next), Return((var, "cycle_right")))
            if sc_prefix == "shift_":
                tooltip "Use shift + left/right arrow keys to change the focused character."
            else:
                tooltip "Use left/right arrow keys to change the focused character."


screen sorting_tab(context, sort_target=None, sorters=[], use_stats=False, small=False): # Sorters are defined in BKinit_variables.rpy

    zorder 5

    if small:
        default but_w = 30
        default but_txt = 12
    else:
        default but_w = 38
        default but_txt = 14
    
    default but_h = 20

    hbox xalign 0.5:
        for s in sorters:
            $ _caption, _attr, _ttip, _reverse = sorter_dict[s] # sorter format: [caption, attribute, tooltip, reverse order]
            if game.sorting_dict[context] and game.sorting_dict[context][1] == _attr and game.sorting_dict[context][3] == _reverse: # If the same sorting method is selected twice, reverses sorting order:
                $ _reverse = not _reverse

            frame xsize yres(but_w) ysize yres(but_h) xpadding 0 ypadding 0 xmargin 0 ymargin 0:

                textbutton _caption text_italic True text_color c_darkbrown text_size res_font(but_txt) xpadding 0 ypadding 0 xalign 0.5 yalign 0.6 xsize yres(but_w) ysize yres(but_h) idle_background None:
                    if use_stats:
                        action (Function(sort_target.sort, key=lambda x, s=_attr: x.get_stat(s), reverse=_reverse), SetDict(game.sorting_dict, context, [_caption, _attr, _ttip, _reverse, True]))
                    else:
                        action (Function(sort_target.sort, key=lambda x, s=_attr: getattr(x, s), reverse=_reverse), SetDict(game.sorting_dict, context, [_caption, _attr, _ttip, _reverse, False]))
                    tooltip __("Click to sort by %s.") % _ttip

screen item_list(items, owner, counterpart, sc_prefix, search=False): # May also accept Minions as 'items'

    default page = 1
    default line_nb = 7
    default page_offset = 0
    default page_button_nb = 8
    default old_filter = ""

    $ page_nb = round_up(len(items)/line_nb)
    if page_nb < page and page > 1:
        $ page = page_nb

    if MC.active_text_filter and MC.active_text_filter != old_filter: # There must be a better way to do this :(
        $ page = 1
        $ page_offset = 0

    if MC.active_text_filter:
        $ items = [it for it in items if MC.active_text_filter.lower() in it.name.lower()]
        $ old_filter = MC.active_text_filter
    elif MC.active_inv_filter:
        $ items = [it for it in items if it.filter in MC.active_inv_filter]

    $ page_index = line_nb * (page-1)

    vbox xsize xres(180):
        frame xfill True:
            ysize yres(415)
            # else:
            #     ysize yres(400)
            has vbox

            if search:
                hbox:
                    text _("Search: ") size res_font(16) color c_brown
                    input size res_font(16) color c_darkorange changed(MC.add_text_filter)

            if items:

                for i in range(line_nb):
                    if page_index+i < len(items):
                        $ it = items[page_index+i]
                        $ acts = it.get_acts(owner, counterpart)

                        button style "girlbutton_blue" xpadding 6:
                            xfill True
                            action (Show("item_profile", it=it, transition = dissolve), SetVariable("selected_item", it), SetVariable("owner", owner), SetVariable("counterpart", counterpart), SelectedIf(selected_item==it))
                            if isinstance(it, ItemInstance):
                                tooltip it.base_description
                            tooltip it.description

                            hbox spacing 3:

                                frame yalign 0.5 xysize res_tb(55) ymargin 3:
                                    add it.pic.get(*res_tb(45)) xalign 0.5 yalign 0.5


                                vbox yalign 0.5:
                                    $ text1 = __(it.name_i18n)

                                    if isinstance(it, ItemInstance):
                                        if it.charges and it.charges > 1:
                                            $ text1 += " (" + str(it.charges) + ")"

                                        if it.equipped:
                                            $ text1 += __("\n{i}Equipped{/i}")

                                    elif isinstance(it, Minion):
                                        $ text1 +=  __("\nLevel ") + str(it.level)

                                    if "sell" in acts:
                                        $ text1 += "\n" + str(it.get_price("sell")) + " gold"

                                    if "buy" in acts:
                                        $ text1 += "\n" + str(it.get_price("buy")) + " gold"

                                    text __(text1) size res_font(14)

            else:
                if MC.active_inv_filter:
                    text _("No items available (filters are on).") size res_font(14) color c_brown
                else:
                    text _("No items available.") size res_font(14) color c_brown

        if items:
            $ start = page_offset

            # No arrows required
            if page_nb <= page_button_nb:
                $ previous = None
                $ next = None
                $ finish = page_nb
            # More than one set of page numbers is needed
            else:
                if page_offset:
                    $ previous = page_button_nb-2
                else:
                    $ previous = None

                if page_nb-page_offset >= page_button_nb-1:
                    $ next = page_button_nb-2
                else:
                    $ next = None

                if next:
                    $ finish = start + next
                else:
                    $ finish = page_nb

            if page_nb > 1:
                if page > 1:
                    if is_renpy_8_1(): # Only works in Ren'py 8.1.1 and above
                        $ my_key = [sc_prefix + "K_UP", sc_prefix + "mousedown_4"]
                    else:
                        if sc_prefix == "noshift_": # Workaround until a solution is found for shift+mousewheel
                            $ my_key = [sc_prefix + "K_UP", "mousedown_4"]
                        else:
                            $ my_key = sc_prefix + "K_UP"

                    key my_key capture True:
                        if page-1 <= start and previous:
                            action (SetLocalVariable("page", page-1), SetLocalVariable("page_offset", page_offset-previous))
                        else:
                            action SetLocalVariable("page", page-1)
                if page < page_nb:
                    if is_renpy_8_1(): # Only works in Ren'py 8.1.1 and above
                        $ my_key = [sc_prefix + "K_DOWN", sc_prefix + "mousedown_5"]
                    else:
                        if sc_prefix == "noshift_": # Workaround until a solution is found for shift+mousewheel
                            $ my_key = [sc_prefix + "K_DOWN", "mousedown_5"]
                        else:
                            $ my_key = sc_prefix + "K_DOWN"

                    key my_key capture True:
                        if page+1 > finish and next:
                            action (SetLocalVariable("page", page+1), SetLocalVariable("page_offset", page_offset+next))
                        else:
                            action SetLocalVariable("page", page+1)

                hbox tooltip _("Change item page"):
                    if next:
                        xsize xres(180)
                    else:
                        xmaximum xres(180)

                    if previous:
                        textbutton "↑" style "UI_button":
                            xalign 0.0
                            xsize xres(22)
                            ysize yres(22)
                            action (SetLocalVariable("page_offset", page_offset-previous), SetLocalVariable("page", page_offset))
                            text_size res_font(14)
                            text_font "resources/fonts/DejaVuSans.ttf"

                    for p in range(start, finish):
                        textbutton str(p+1) style "UI_button":
                            xalign 0.0
                            xsize xres(22)
                            ysize yres(22)
                            action SetLocalVariable("page", p+1)
                            text_size res_font(14)
                            text_selected_bold True

                            if sc_prefix == "shift_":
                                tooltip "Use shift + up/down arrows or mousewheel to cycle item pages."
                            else:
                                tooltip "Use up/down arrows or mousewheel to cycle item pages."

                    if next:
                        textbutton "↓" style "UI_button":
                            xalign 0.0
                            xsize xres(22)
                            ysize yres(22)
                            action (SetLocalVariable("page_offset", page_offset+next), SetLocalVariable("page", page_offset+next+1))
                            text_size res_font(14)
                            text_font "resources/fonts/DejaVuSans.ttf"


screen item_profile(it):

    zorder 7

    $ acts = it.get_acts(owner, counterpart)

    if owner.type == "girl":
        default focused_char = owner
    elif counterpart and counterpart.type == "girl":
        default focused_char = counterpart
    else:
        default focused_char = None

    on "hide" action SetVariable("selected_item", None)

    frame:

        id "item_profile"

        if owner == MC:
            background c_ui_darkblue
        elif isinstance(owner, Girl):
            background c_ui_darkpink
        else:
            background c_ui_darker

        xalign 0.5
        yalign 0.3
        xpadding 6
        ypadding 6
        xsize xres(300)
        xfill True
        yfill False

        has vbox

        if "bargain" not in acts:
            use close(Hide("item_profile"), name = "hide")
            key "mouseup_3" action Hide("item_profile")


        frame xalign 0.5 xfill True:
            add it.pic.get(*res_tb(100)) xalign 0.5

        frame xalign 0.5 xfill True:
            background None

            has vbox xfill True xalign 0.5

            $ text1 = __(it.name_i18n)

            if isinstance(it, ItemInstance):
                if it.charges and it.charges > 1 and it.usage == "use":
                    $ text1 += " (" + str(it.charges) + ")"

            text text1 xalign 0.5

            if it.target == "MC":
                $ col = c_main
            elif it.target == "girl":
                $ col = c_pink
            elif it.target == "minion":
                $ col = c_purple
            else:
                $ col = c_orange

            text "" size res_font(8)

            if isinstance(type, ItemType):
                text "{color=[col]}%s{/color}" % it.type.name xalign 0.5 size res_font(18)
            else:
                text "{color=[col]}%s{/color}" % it.target.capitalize() xalign 0.5 size res_font(18)

            if isinstance(it, ItemInstance):
                text __(it.base_description) size res_font(14) xalign 0.5 italic True
            text "" size res_font(14)
            text __(it.description) size res_font(14) xalign 0.5

            text ""

            if "buy" in acts:
                text str(it.get_price("buy")) + " gold" xalign 0.5
                text ""

            if "bargain" in acts:
                text str(it.get_price("bargain")) + " gold" xalign 0.5
                text ""

            if "sell" in acts:
                text str(it.get_price("sell")) + " gold" xalign 0.5
                text ""

            if isinstance(it, ItemInstance) and it in MC.items and not it.sellable:
                text _("Unsellable") italic True xalign 0.5
                text ""

            hbox spacing 10 xalign 0.5:
                for act in acts:
                    textbutton __(capitalize(act)) action Return((it, act)) xalign 0.5:
                        if owner.type == "girl" and act in ("equip", "unequip", "use"):
                            hovered SetScreenVariable("focused_char", owner)
                        elif counterpart and counterpart.type == "girl":
                            hovered SetScreenVariable("focused_char", counterpart)
                            if owner.type == "girl":
                                unhovered SetScreenVariable("focused_char", owner)

                if "bargain" in acts:
                    textbutton __("Skip") action Return("leave") xalign 0.5

    if isinstance(it, ItemInstance) and focused_char and (it.can_wear("girl") or it.can_use("girl")):
        if focused_char == left_focus:
            use girl_stats_light(left_focus, panel="left")
        else:
            use girl_stats_light(right_focus, panel="right")

screen inventory(char, counterpart=None):
    frame:
        xalign 0.5
        yalign 0.0
        xfill False
        yfill False

        has vbox spacing 10 box_wrap True

        if char:
            for slot in char.slots:
                $ eq = None
                for it in char.equipped:
                    if it.slot == slot:
                        $ eq = it
                        $ acts = it.get_acts(char, counterpart)

                vbox:
                    text slot.capitalize() size res_font(14) xalign 0.5 color c_brown

                    button xsize yres(60) ysize yres(60) xfill True yfill True xalign 0.5:
                        style "girlbutton_blue"
                        if eq:
                            add eq.pic.get(*res_tb(45)) xalign 0.5 yalign 0.5
                            action (Show("item_profile", it=eq, transition = dissolve), SetVariable("owner", char), SetVariable("counterpart", counterpart), SetVariable("selected_item", eq), SetField(MC, "active_inv_filter", [slot]), SelectedIf(slot in MC.active_inv_filter))
                            tooltip __(eq.description)
                        else:
                            text _("Empty") size res_font(12) italic True xalign 0.5 yalign 0.5
                            action (SetField(MC, "active_inv_filter", [slot]), SelectedIf(slot in MC.active_inv_filter))
                            tooltip _("No item is equipped to this slot.")


screen item_filter(filters=inventory_filters["base"]):

    if MC.active_inv_filter not in filters:
        $ active_inv_filter = []

    vbox xfill False yfill False spacing 3:
        for filter in filters:
            # frame  xpadding 0 xmargin 0:
            button xsize xres(35) ysize yres(35) xpadding 0 xmargin 0 style "contrast_button":
                action (SetField(MC, "active_inv_filter", filter_list[filter]), Function(renpy.restart_interaction))

                if filter:
                    if MC.active_inv_filter and MC.active_inv_filter[0] in filter_list[filter]:
                        add "filter_" + filter xalign 0.5 yalign 0.5
                    else:
                        add "filter_" + filter + "_unselect" xalign 0.5 yalign 0.5
                    tooltip __("Show %s items.") % __(filter)
                else:
                    if not MC.active_inv_filter:
                        add "filter_all" xalign 0.5 yalign 0.5
                    else:
                        add "filter_all_unselect" xalign 0.5 yalign 0.5
                    tooltip _("Show all items.")


init python:
    ## EN: Load equipment types and furniture type descriptions from JSON (BK Evolution), fallback to hardcoded.
    ## ZH: 从 JSON 加载装备类型和家具类型描述（BK Evolution），否则使用硬编码。
    _itp_json = DataLoader.load_item_type_params()
    if _itp_json:
        all_equipement_types = _itp_json.get("all_equipement_types", [])
        _ft = _itp_json.get("furniture_types", [])
        furniture_types = [(t["type"], __(t.get("description_i18n", t["description"]))) for t in _ft]
    else:
        all_equipement_types = ["weapon", "dress", "ring", "necklace", "accessory", "passive"]
        furniture_types = [("Decoration", "Attracts new kinds of customers to your brothel"),
                            ("Furnishing", "Unlocks more options for attracting customers"),
                            ("Utility", "Help with advertising, security and maintenance"),
                            ("Comfort", "Help your girls feel more comfortable in the brothel"),
                            ("Windows", "Influences your girl's preferences"),
                            ("Altars", "Pray here and get results, for once"),
                            ("Arcane", "Helps with dark rituals"),
                            ("Gizmos", "Strange artefacts from a bygone technological age")
                            ]

#### END OF BK ITEMS FILE ####
