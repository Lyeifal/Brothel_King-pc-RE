#### Dialogue functions ####

init -3 python:
    def say_name(it):
        if it:
            return it.name
        else:
            return __("None")


#    def list_items(rank = 1):

#        district.items = defaultdict(list)

#        district.items["junk"] += game.items[rank - 1]
#        district.items["common"] += game.items[rank]
#        district.items["rare"] += game.items[rank + 1]
#        district.items["exceptional"] += game.items[rank + 2]

#        return


    def get_description(basetext, effects, separator="\n", final_dot=True):

        text1 = "{i}" + __(basetext) + "{/i}"
        begin = True

        for effect in effects:
            d = effect.get_description()

            if begin and d:

                if basetext:
                    text1 += separator
                else:
                    text1 = ""

                text1 += __(capitalize(d))
                begin = False

            elif not begin and d:
                text1 += ", " + d

        if final_dot:
            if len(text1) > 0 and text1[-1] not in (".", "!", "?"): # Makes sure punctuation is added last.
                text1 += "."

        return text1


    def get_log_changes(girl, change_log, changes, act): ## Where 'change_log' is a NightChangeLog object and 'changes' lists tuples with (stat_name, nb) - Used for perform()

        change_log.add("")

        for c in changes:

            stat, nb = c

            if stat in ("rep", "reputation"):
                change_log.add(__("Reputation: %i/%i (%s)") % (girl.rep, girl.get_stat_max("rep"), plus_text(int(nb), "rep")))

            elif stat == "gold":
                change_log.add(__("Gold: {image=img_gold} %s") % plus_text(int(nb), "gold"))

            else:
                change_log.add("%s: %i/%i (%s)" % ((__(stat.capitalize()), girl.get_stat(stat), girl.get_stat_max(stat), plus_text(nb, "stat", decimals=2))), ttip = describe_leveled_stats(act), ttip_title = __("%s skill changes") % __(act.capitalize()))

        return change_log

    def describe_leveled_stats(act):
        desc = ""
        for stat, _, chg in perform_job_dict[act + "_changes"]:
            desc += __(stat_name_dict[stat[0].capitalize()]) + ": "
            if chg > 1:
                desc += event_color["good"] % "++"
            elif chg == 1:
                desc += event_color["good"] % "+"
            elif chg < 0:
                desc += event_color["a little bad"] % "-"
            desc += "\n"
        return desc

    def get_change_text(changes): ## Where 'changes' lists tuples with (stat_name, nb)

        text_changes = ""

        for c in changes:

            stat, nb = c

            if nb:
                if stat in ("rep", "reputation"):
                    text_changes += __("Girl reputation: %s") % plus_text(nb, color_scheme="rep", decimals=1)

                elif stat == "gold":
                    text_changes += __("Gold: {image=img_gold} %s") % plus_text(round_int(nb), color_scheme="gold")

                else:
                    text_changes += __("%s: %s") % (__(stat.capitalize()), plus_text(round_int(nb), color_scheme="standard"))

            text_changes += "\n"

        return text_changes


    def help(screen):
        target = "help"
        renpy.call(target, screen)

        return


    def get_gossip():

        # Generic gossip is always on
        # Chapter gossip is active only during a given chapter
        # District gossip is specific to the visited district
        # Story gossip is added by the story, permanently
        # Temp gossip is added by the story, and removed at the end of each chapter

        try:
            return rand_choice(generic_gossip + chapter_gossip[game.chapter] + district_gossip[selected_district.name] + story_gossip + temp_gossip)
        except:
            return rand_choice(generic_gossip)

    # def acquire_girl(girl, free = False, target=MC):
    #
    #     target.girls.append(girl)
    #
    #     if free:
    #         game.free_girls.remove(girl)
    #         game.track("free girl acquired")
    #
    #     girl.location = None
    #     girl.set_job(None)
    #     girl.set_workdays()
    #     girl.refresh_pictures()
    #
    #     girl.log["acquired"] = calendar.time
    #     girl.track_event("acquired", arg=girl.name)
    #     test_achievements(["free girl acquired", "originals", "slaves", "naked", "rank B", "rank A", "rank S", "rank X"])

    def relinquish_girl(girl): # Not exactly symetrical with acquire_girl, to clean up later

        girl.set_job(None)
        brothel.master_bedroom.remove_girl(girl)

        if girl in MC.girls:
            MC.girls.remove(girl)

        if girl in farm.girls:
            farm.girls.remove(girl)

        if girl.items: # Unequip all items before selling
            for it in list(girl.items): # shallow copy of list since deleting from girl.items
                if it.equipped:
                    girl.unequip(it)
                MC.take(girl, it)
                notify((girl.fullname + __(" has lost ") + it.name), pic=girl.portrait)
                renpy.pause(0.5)

    def have_fight(attacker, defender, att_bonus=0, def_bonus=0, advantage = "defender"): # Returns True if attacker won, False otherwise

        attack = attacker.get_defense(fight = True) + dice(6) + att_bonus
        defense = defender.get_defense(fight = True) + dice(6) + def_bonus

        if attack > defense:
            return True

        elif defense > attack:
            return False

        elif attack == defense and advantage == "attacker":
            return True

        elif attack == defense and advantage == "defender":
            return False

        else:
            return "tie"

    def compare_preference(girl, act, pref, bonus=0): # Returns True if a girl's preference is better or equal to Pref
        if preference_modifier[girl.get_preference(act, bonus)] <= preference_modifier[pref]:
            return True
        return False

    def get_preference_limit(act, pref):
        return base_reluctance[act] * preference_limit[pref]

    def get_act_weakness_symbol(girl, act):

        if girl.personality_unlock[act]:
            if act in girl.pos_acts and act in girl.neg_acts:
                return " (%s)" % emo_yang
            elif act in girl.pos_acts:
                return " (%s)" % emo_heart
            elif act in girl.neg_acts:
                return " (%s)" % emo_lightning
            else:
                return ""
        else:
            return " (?)"

    def get_fix_weakness_symbol(girl, fix_name):

        if girl.personality_unlock[fix_name]:
            if fix_name in [fix.name for fix in girl.pos_fixations]:
                return " (%s)" % emo_heart
            elif fix_name in [fix.name for fix in girl.neg_fixations]:
                return " (%s)" % emo_lightning
            else:
                return ""
        else:
            return " (?)"

    def this_is_a_hentai_game_so_why_are_you_trying_to_act_classy_all_of_a_sudden():

        global shake_count

        shake_count +=1

        if shake_count == 1:

            renpy.say(you, __("I mean, I could just..."), interact=False)

        elif shake_count == 2:

            renpy.say(you, __("You know, just five seconds..."), interact=False)

        elif shake_count == 3:

            renpy.say(you, __("It wouldn't hurt anybody..."), interact=False)

        elif shake_count == 4:

            renpy.say(you, __("What's... happening to me..."), interact=False)

        elif shake_count == 5:

            renpy.say(you, __("I... I can't control myself..."), interact=False)

            shake_count = 0

        shake_mouse()

        return

    def get_rand_minion(type, nb):

        minions = []

        for i in range(nb):
            level = dice(district.rank) - 1
            minions.append(Minion(type, level))

        return minions

    # def generate_template_items(items):
    #
    #     #Generate variable quality items
    #
    #     new_items = []
    #
    #     for it in items:
    #
    #         for i in range(0,7):
    #
    #             if it.min_rank <= i <= it.max_rank:
    #
    #                 new_it = it.generate_new_item(i)
    #
    #                 new_items.append(new_it)
    #
    #     return new_items


    def can_use_minion_item():

        if MC.get_items(target="minion", name="Healing powder") and farm.get_hurt_minions():
            return True
        if MC.get_items(target="minion", effect_type="gain"):
            for it in MC.get_items(target="minion", effect_type="gain"):
                for eff in it.effects:
                    if eff.target[:-3] in all_minion_types: # This checks if the target effect starts with a minion type, then check if this type of minion exists in the farm (dirty)
                        if farm.get_minions(eff.target[:-3]):
                            return True
        return False

    def return_ddict_list():
        return defaultdict(list)

    def add_mix():
        new_mix = renpy.input(_("Enter the name of the mix you want to create"))

        if new_mix in (persistent.girl_mix.keys()):
            renpy.notify(_("{color=[c_red]}%s already exists.{/color}") % new_mix)
        else:
            persistent.girl_mix[new_mix] = []
            persistent.active_mix = new_mix
        return

    def add_all_to_mix(mix):
        persistent.girl_mix[mix] = list(persistent.girl_packs)

    def remove_all_from_mix(mix):
        persistent.girl_mix[mix] = []

    def delete_mix(mix):
        if mix == "default":
            renpy.notify(__("Can't delete the 'default' mix."))
        elif mix in persistent.girl_mix.keys() and renpy.call_screen("yes_no", __("Are you sure you want to delete this girl mix?")):
            del persistent.girl_mix[mix]
            if persistent.active_mix == mix:
                persistent.active_mix = "default"

    def prepare_not_tags(girl, act, fix_list=None, farm=False):

        if fix_list == None: fix_list = []

        not_tags = ["swimsuit", "fight", "profile", "date", "rest"] # Avoids showing profile and other inappropriate pics (unless the not clause is dropped)

        if act == "naked":
            not_tags += all_sex_acts
            if "masturbation" in fix_list:
                not_tags.remove("service")

        if act != "group" and not farm:
            not_tags.append("group")
        if act != "bisexual" and not farm:
            not_tags.append("bisexual")

        if "public acts" not in fix_list:
            not_tags.append("public")
        if "cosplay" not in fix_list and "roleplay" not in fix_list: # Disable improper job pics unless cosplay/roleplay is on
            not_tags += [j for j in all_jobs if girl.job != j]
            not_tags.append("cosplay")

        return not_tags


    def parse_dice_formula(formula):
        def factor(f):
            g = f.split('d')
            if len(g)==1:
                return int(f)
            return sum(random.randint(1, int(g[1]) if g[1] else 6) for i in range(int(g[0]) if g[0] else 1))

        def term(t):
            p = t.split('*')
            return factor(p[0]) if len(p)==1 else factor(p[0])*factor(p[1])

        return sum(term(x) for x in formula.split('+'))

    def plus_minus(value): # Returns a string value with a + or - sign (no sign if = 0)
        return plus_text(float(value))

    def is_censored(tag):
        if tag in (persistent.forbidden_tags + forbidden_tags):
            return True
        return False

    def load_girl_status(girls): # Stores statuses in a dictionary that is refreshed every interaction
        s_dict = {}

        for girl in girls:
            update_girl_status(s_dict, girl)

        return s_dict

    def update_girl_status(s_dict, girl):
        s_dict[girl] = girl.get_status()
        s_dict[girl, "summary"] = girl.get_status_summary()

    def change_autorest(girl="default", direction="+"): # girl set to "default" is a special case: the default value

        if direction == "+" and autorest_limit[girl] < 200:
            autorest_limit[girl] += 5
        elif direction == "-" and autorest_limit[girl] > 0:
            autorest_limit[girl] -= 5

    def reset_autorest(): # Overwrites all custom autorest limits to the default value.
        for k in autorest_limit.keys():
            if k != "default":
                autorest_limit[k] = autorest_limit["default"]

    def get_opposite_attribute(attr):
        prfx = ""
        opp = ""

        if attr.startswith("very "):
            prfx = "very "
            attr = attr[5:]

        for a1, a2 in personality_attributes:
            if attr == a1:
                opp = a2
                break
            elif attr == a2:
                opp = a1
                break

        return prfx + opp

    def print_ignore_list():
        ignore_text = list_text(sorted(persistent.pic_ignore_list), "", if_none="No pictures have been set to ignore.")
        if persistent.pic_ignore_list:
            ignore_text = __("%i picture%s currently ignored (pictures will be updated after restart):\n") % (len(persistent.pic_ignore_list), plural(len(persistent.pic_ignore_list))) + ignore_text

        with open((config.gamedir + "\\ignored_pictures.txt"), "wt") as ignore_file: #? Check that it works if file doesn't exist
            ignore_file.write(ignore_text)

        notify(__("List printed to: ") + config.gamedir + "\\ignored_pictures.txt")

    def toggle_ignore_pic(pic): # path overrides pic if provided

        if is_string(pic):
            path=pic
        elif isinstance(pic, Picture):
            path=pic.path
        elif isinstance(pic, ProportionalScale):
            path=event_pic.imgname

        if path in persistent.pic_ignore_list:
            persistent.pic_ignore_list.remove(path)
            priority_notify(__("Removed from the 'IGNORE' list: %s") % path, col=c_lightgreen)
        else:
            if not persistent.seen_ignore_intro:
                renpy.call_in_new_context("ignore_introduction")
            persistent.pic_ignore_list.append(path)
            priority_notify(__("Added to the 'IGNORE' list: %s") % path, col=c_red)

    def _event_mode_allowed(event):
        """EN: Check if a StoryEvent is allowed in the current game mode.
           ZH: 检查 StoryEvent 是否允许在当前游戏模式下运行。"""
        if event.modes is None:
            return True
        if not hasattr(game, 'game_mode') or game.game_mode is None:
            return True
        current_mode = game.game_mode.mode_id if hasattr(game.game_mode, 'mode_id') else game.game_mode
        if is_string(event.modes):
            return event.modes == current_mode
        return current_mode in event.modes

