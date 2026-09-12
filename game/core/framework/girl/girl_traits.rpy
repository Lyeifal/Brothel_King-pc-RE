#### GirlTraits — Trait and perk management | 特质与天赋管理 ####
# Phase 2.1: Traits, perks, archetypes, combo checks.
# 特质、天赋、原型、连携检查
# ★ generate_traits — 特质生成（已从 girlclass.rpy 移入）
# Methods: has_trait, has_perk, add_trait, remove_trait,
#          acquire_perk, refund_perks, check_combo_perks.

init -2 python:

    class GirlTraits(object):
        """Trait and perk management for a Girl. 1 impl + delegation stubs."""

        def __init__(self, girl):
            self.girl = girl

        # ── Trait generation (implemented here, moved from girlclass.rpy) ──

        def generate_traits(self, p_traits=None, n_trait=None):
            g = self.girl
            gold_traits_nb = starting_traits_gold
            pos_traits_nb = starting_traits_gold + starting_traits_positive
            neg_traits_nb = starting_traits_negative

            if game.has_active_mod("traitking"):
                d = dice(100)
                if d > traitking_t1_chance:
                    gold_traits_nb = traitking_t1_gold
                    pos_traits_nb = traitking_t1_positive
                    neg_traits_nb = traitking_t1_regular
                elif d > traitking_t2_chance:
                    gold_traits_nb = traitking_t2_gold
                    pos_traits_nb = traitking_t2_positive
                    neg_traits_nb = traitking_t2_regular
                elif d > traitking_t3_chance:
                    gold_traits_nb = traitking_t3_gold
                    pos_traits_nb = traitking_t3_positive
                    neg_traits_nb = traitking_t3_regular
                elif d > traitking_t4_chance:
                    gold_traits_nb = traitking_t4_gold
                    pos_traits_nb = traitking_t4_positive
                    neg_traits_nb = traitking_t4_regular
                elif d > traitking_t5_chance:
                    gold_traits_nb = traitking_t5_gold
                    pos_traits_nb = traitking_t5_positive
                    neg_traits_nb = traitking_t5_regular
                elif d > traitking_t6_chance:
                    gold_traits_nb = traitking_t6_gold
                    pos_traits_nb = traitking_t6_positive
                    neg_traits_nb = traitking_t6_regular
                else:
                    gold_traits_nb = traitking_t7_gold
                    pos_traits_nb = traitking_t7_positive
                    neg_traits_nb = traitking_t7_regular

            new_traits = []
            if p_traits:
                new_traits = p_traits

            use_ini = use_ini_traits
            if use_ini and g.init_dict["base positive traits/always"]:
                renpy.random.shuffle(g.init_dict["base positive traits/always"])
                for trait_name in g.init_dict["base positive traits/always"]:
                    if trait_name not in new_traits:
                        new_traits.append(trait_name)

            if g.original:
                gold_traits_nb += 1

            for trait_name in new_traits:
                if trait_name in gold_trait_dict.keys():
                    gold_traits_nb -= 1

            while gold_traits_nb > 0 and len(new_traits) < pos_traits_nb:
                gold_list = []
                for trait in gold_traits:
                    if not trait.public: continue
                    elif trait.name in new_traits: continue
                    elif use_ini and trait.name in g.init_dict["base positive traits/never"]: continue
                    elif use_ini and trait.name in g.init_dict["base positive traits/often"]: gold_list.append((trait.name, 4))
                    elif use_ini and trait.name in g.init_dict["base positive traits/rarely"]: gold_list.append((trait.name, 1))
                    else: gold_list.append((trait.name, 2))
                new_traits.append(weighted_choice(gold_list))
                gold_traits_nb -= 1

            while len(new_traits) < pos_traits_nb:
                trait_list = []
                if NGP_settings_dict["naturist frequency"].get():
                    for t in new_traits:
                        if t == "Naturist": break
                    else:
                        trait_list.append(("Naturist", NGP_settings_dict["naturist frequency"].get()))
                for trait in pos_traits:
                    if not trait.public: continue
                    elif trait.name in new_traits: continue
                    elif use_ini and trait.name in g.init_dict["base positive traits/never"]: continue
                    else:
                        for opp in trait.opposite:
                            if opp in new_traits: break
                        else:
                            if use_ini and trait.name in g.init_dict["base positive traits/often"]: trait_list.append((trait.name, 4))
                            elif use_ini and trait.name in g.init_dict["base positive traits/rarely"]: trait_list.append((trait.name, 1))
                            else: trait_list.append((trait.name, 2))
                new_traits.append(weighted_choice(trait_list))

            if len(new_traits) > pos_traits_nb:
                new_traits = new_traits[:pos_traits_nb]

            if n_trait:
                new_traits.append(n_trait)
            elif use_ini and g.init_dict["base negative traits/always"]:
                new_traits.append(rand_choice(g.init_dict["base negative traits/always"]))

            while len(new_traits) - pos_traits_nb < neg_traits_nb:
                trait_list = []
                for trait in neg_traits:
                    if not trait.public: continue
                    elif trait.name in new_traits: continue
                    elif use_ini and trait.name in g.init_dict["base negative traits/never"]: continue
                    else:
                        for opp in trait.opposite:
                            if opp in new_traits: break
                        else:
                            if use_ini and trait.name in g.init_dict["base negative traits/often"]: trait_list.append((trait.name, 4))
                            elif use_ini and trait.name in g.init_dict["base negative traits/rarely"]: trait_list.append((trait.name, 1))
                            else: trait_list.append((trait.name, 2))
                new_traits.append(weighted_choice(trait_list))

            for trait_name in new_traits:
                g.add_trait(trait_dict[trait_name], forced=True)

        # ── Delegation stubs (implementations remain in girlclass.rpy) ──
        def has_trait(self, name):
            return self.girl._has_trait_impl(name)
        def has_perk(self, name):
            return self.girl._has_perk_impl(name)
        def add_trait(self, trait, _pos=None, forced=False, no_perks=False):
            return self.girl._add_trait_impl(trait, _pos, forced, no_perks)
        def remove_trait(self, trait):
            return self.girl._remove_trait_impl(trait)
        def can_acquire_perk(self, perk, context=None):
            return self.girl.can_acquire_perk(perk, context)
        def update_can_perk(self):
            return self.girl.update_can_perk()
        def acquire_perk(self, perk, forced=False):
            return self.girl.acquire_perk(perk, forced)
        def refund_perks(self, min_level=0):
            return self.girl.refund_perks(min_level)
        def check_combo_perks(self):
            return self.girl.check_combo_perks()
        def has_prerequisites(self, perk):
            return self.girl.has_prerequisites(perk)
        def get_perk(self, perk):
            return self.girl.get_perk(perk)
        def get_perk_level(self, perk):
            return self.girl.get_perk_level(perk)
