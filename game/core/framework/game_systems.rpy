#### Game Systems functions ####

init -3 python:
    def update_slaves():

        nb = dice(6)+5

        slavemarket.girls = [] # Empties slavemarket to get another chance at generating an original girl
        slavemarket.girls = get_girls(nb)

        for girl in slavemarket.girls: girl.refresh_pictures()

        slavemarket.updated = True

        return


    def update_free_girls(): # Generates a list of girls that will cycle around the city. Note: Girls restricted to a location may not be visible

        # Removes girls that haven't been talked to for 8 weeks
        # Randomly removes girls that haven't been met by the player on a roll of 1 on a d4

        for girl in game.free_girls:
            if (not girl.MC_interact and dice(4) == 1) or (girl.MC_interact and girl.talked_to_date < calendar.time - 56):
                game.free_girls.remove(girl)

        # game.free_girls = [girl for girl in game.free_girls if (not girl.MC_interact and dice(4) > 1) or (girl.MC_interact and girl.talked_to_date >= calendar.time - 56)]

        # game.free_girls = [girl for girl in game.free_girls if (girl.talked_to_date and girl.talked_to_date >= calendar.time - 56) or not girl.talked_to_date]
        #
        # game.free_girls = [girl for girl in game.free_girls if girl.MC_interact or (dice(6) > 1)]

        # Adds new girls as necessary to fill up the city streets
        if district.rank == 1:
            nb = free_girls_per_district

        elif district.rank == 2:
            nb = free_girls_per_district * 3

        elif district.rank == 3:
            nb = free_girls_per_district * 5

        else:
            nb = free_girls_per_district * 6

        if len(game.free_girls) < nb:
            game.free_girls += get_girls(nb - len(game.free_girls), free=True)

        return


    def refresh_available_locations():

        """ This creates 3 free girl slots for every location available to the player """

        game.location_slots = []

        loc_list = game.get_available_locations()

        for loc in loc_list:
            game.location_slots += [loc.name]*3

    def reset_girl_jobs():

        for girl in MC.girls and farm.girls:
            if girl.job in all_jobs:
                if not brothel.can_have(girl.job):
                    girl.set_job(None)
                    notify(girl.fullname + __(" was set to rest."), pic=girl.portrait, col="a little bad")

        return


    def cycle_free_girls():

        renpy.random.shuffle(game.free_girls)
        renpy.random.shuffle(game.location_slots)

        for loc in game.get_available_locations():
            loc.girls = []

        available_girls = list(game.free_girls) # copy of game.free_girls

        for slot in game.location_slots: # Reminder: game.location_slots contains location names (strings)
            for girl in available_girls:
                 # Girls that have interacted with MC will cycle unless move_after_meeting is set to False
                if (girl.MC_interact and girl.init_dict["background story/move_after_meeting"]) or can_spawn(girl, location=location_dict[slot]):
                    girl.location = slot
                    location_dict[slot].girls.append(girl)
                    available_girls.remove(girl) # This is okay because of break
                    break

        return

    def update_market():
        calendar.discounted = []
        calendar.scarce = []

        d = dice(100)

        if d >= 98: # Everything is cheap this week
            calendar.discounted = build_resources
        elif d >= 95:
            calendar.discounted = ["marble", "ore", "silk"]
        elif d >= 91:
            calendar.discounted = ["wood", "leather", "dye"]
        elif d <= 2: # Everything is expensive
            calendar.scarce = build_resources
        elif d <= 5:
            calendar.scarce = ["marble", "ore", "silk"]
        elif d <= 9:
            calendar.scarce = ["wood", "leather", "dye"]
        else:
            calendar.discounted = [rand_choice(build_resources)]
            calendar.scarce = [rand_choice(build_resources)]

            if calendar.discounted == calendar.scarce:
                calendar.discounted = []
                calendar.scarce = []

        return


    def update_shops():

        # All shops (BK Evolution: data-driven restock)

        for merc in all_shops:
            merc.restock(once_a_day=False)

        return

    def weekly_updates(change_district=False):

        game.update_max_girl_level()
        update_slaves()
        refresh_available_locations()
        update_free_girls()
        cycle_free_girls()
        update_shops()
        if not change_district:
            update_market()
            update_quests()
        update_NPC_items(NPC_renza)
        update_NPC_items(NPC_captain)
        evpower_deck.update()

        return

    def update_mods(): #! Replace messages

        global mod_traceback

        mod_traceback += __("Updating mods... ")

        # Checks if existing/active mods have been disabled

        undetected_mods = []

        for name in persistent.mods.keys():
            if name not in detected_mods.keys():
                undetected_mods.append(name)

        for name in undetected_mods:
            del persistent.mods[name]

            renpy.notify(__("Mod: %s has been removed.") % name)
            mod_traceback += "\n" + __("Mod: %s has been removed.") % name

        # Checks new mods or new mod versions

        for name, mod in detected_mods.items():

            # Finding new mod

            if name not in persistent.mods.keys():
                register_mod(mod)
                renpy.notify(_("%s has been added.") % mod.full_name)

                mod_traceback += "\n" + __("Mod: %s has been added.") % name

            # Finding new version (basic checks: version number and events lenght)

            elif mod.check_for_updates():
#                renpy.call_screen("OK_screen", title = mod.name + ": new version found", message = "A different version of this mod: " + mod.name + " has been found ([[mod.version]]). The mod has been reset.")
                register_mod(mod)
                renpy.notify(_("%s has been updated.") % mod.full_name)
                mod.active = True
                mod_traceback += "\n" + __("Mod: %s has been updated.") % name

            # Activating mod if it exists

            elif persistent.mods[name]["active"]:
                mod.active = True
#                if debug_mode:
#                    renpy.notify(mod.full_name + " has been activated.")
                mod_traceback += "\n" + __("Mod: %s has been activated.") % name

        # persistent.mods should now be updated to reflect all currently available mods

    def register_mod(mod):

        global mod_traceback

        persistent.mods[mod.name] = {"version" : mod.version, "check" : mod.get_check(), "active" : mod.active}

        mod_traceback += "\n" + "Mod: " + mod.name + " has been registered."

#     def reset_mod(mod): # No longer required

#         if renpy.call_screen("yes_no", mod.full_name + " will be reset. Are you sure you want to proceed?\n\n{b}Warning{/b}: The mod will be reset, this might impact your saved games."):

#             mod.deactivate()
#             if detected_mods[mod.name]:
#                 # persistent.mods[mod.name] = detected_mods[mod.name]
#                 renpy.notify(mod.full_name + " has been reset.")
#             else:
#                 renpy.call_screen("OK_screen", title="Mod Not Found", message=event_color["bad"] % (mod.full_name + ": This mod couldn't be found among installed mods."))

    def reset_updated_games():

        global updated_games

        updated_games = defaultdict(bool)


    def load_quest_pics(): ## Loads quests and class pics

        quest_board.pics = []

        # Looking for picture in quests directory

        imgfiles = [file for file in renpy.list_files() if file.startswith("resources/quests/") and is_imgfile(file)]

        # Attaching each picture to the list with appropriate tags

        for file in imgfiles:

            file_name = file.split("/")[-1]

            quest_board.pics.append(Picture(file_name, file))


    def update_quests():

        quest_board.quests = []
        quest_board.classes = []

        quest_nb = 2 + dice(6)

        class_nb = 2 + dice(6)

        for i in range(quest_nb):

            q = copy.copy(rand_choice(quest_templates))

            d = dice(6)

            if district.rank <= 1 or d >= 4:
                q.randomize(district.rank)
            elif district.rank <= 2 or d >= 2:
                q.randomize(district.rank-1)
            else:
                q.randomize(dice(district.rank-2))

            quest_board.quests.append(q)

        for i in range(class_nb):

            c = copy.copy(rand_choice(class_templates))

            d = dice(6)

            if district.rank <= 1 or d >= 4:
                c.randomize(district.rank)
            elif district.rank <= 2 or d >= 2:
                c.randomize(district.rank-1)
            else:
                c.randomize(dice(district.rank-2))

            quest_board.classes.append(c)

        quest_board.updated = True


    def refresh_quest_girls(girl, quest):

        if not quest:
            available_girls = [g for g in MC.girls if not (g.away or g.hurt > 0 or g.exhausted)]

        else:
            available_girls = [g for g in MC.girls if quest.test_eligibility(g)[0]]
        
        # elif quest.type == "quest":
        #     available_girls = [g for g in MC.girls if quest.test_eligibility(g)[0]]

        # else:
        #     available_girls = [g for g in MC.girls if not (g.away or g.hurt > 0 or g.exhausted)]

        if girl not in available_girls:
            try:
                girl = available_girls[0]
            except:
                pass # girl = MC.girls[0]

        return girl, available_girls


    def add_event(lbl, chapter=0, date=0, year=0, month=0, day=0, chance = 1.0, type="day", location = None, locations = None, min_gold = -99999, condition = None, not_condition = None, condition_func = None, call_args=None, once = True, AP_cost = 1, order = 0, weight = 1, room = None, modes=None):

        # Lower order = procs first
        # Type can be: "city", "day" (plays on main screen), "night" (plays upon ending day), "morning" (plays after night events)
        # Warning: Base type is "day"

        new_event = StoryEvent(label=lbl, chapter=chapter, date=date, year=year, month=month, day=day, chance=chance, type=type, location=location, locations = locations, min_gold=min_gold, condition=condition, not_condition=not_condition, condition_func=condition_func, call_args=call_args, once=once, AP_cost=AP_cost, order=order, weight=weight, room=room, modes=modes)

        if not _event_mode_allowed(new_event):
            return

        if type == "city":
            city_events.append(new_event)
            EventBridge.sync_to_engine(new_event, "city")  # Phase 1.3
        elif type in ("any", "day", "night", "morning"):
            daily_events.append(new_event)
            EventBridge.sync_to_engine(new_event, type)  # Phase 1.3

    def story_add_event(lbl, type="city", duplicates=True):

        # Warning: Base type is "city"

        ev = event_dict[lbl]
        if not _event_mode_allowed(ev):
            return

        if type == "city" or ev.location:
            if duplicates or ev not in city_events: # Avoids creating duplicate events if duplicates is set to False
                city_events.append(ev)
                city_events.sort(key=lambda x: x.order)
                EventBridge.sync_to_engine(ev, "city")  # Phase 1.3

        else:
            if duplicates or ev not in daily_events: # Avoids creating duplicate events if duplicates is set to False
                daily_events.append(ev)
                daily_events.sort(key=lambda x: x.order)
                EventBridge.sync_to_engine(ev, type)  # Phase 1.3

        return

    def story_remove_event(lbl, type="city"):

        if type == "city":
            try:
                city_events.remove(event_dict[lbl])
            except (KeyError, ValueError):
                debug_notify("Couldn't remove city event as it doesn't exist: " + lbl)
                return False

        else:
            try:
                daily_events.remove(event_dict[lbl])
            except (KeyError, ValueError):
                debug_notify("Couldn't remove daily event as it doesn't exist: " + lbl)
                return False

        return True

    def clear_event(lbl): # Removes all occurences of the given label in existing events, slower but more thorough/convenient

        r = 0

        for ev in list(city_events):
            if ev.label == lbl:
                city_events.remove(ev)
                r += 1

        if r:
            debug_notify("%i events removed from city events." % r)

        r = 0

        for ev in list(daily_events):
            if ev.label == lbl:
                daily_events.remove(ev)
                r += 1

        if r:
            debug_notify("%i events removed from daily events." % r)

    def story_set_condition(name, value=True):
        story_flags[name] = value
        return

    def get_events(type="any", _time=None):

        event_list = []

        if not _time:
            _time = calendar.time

        for ev in daily_events:
            if ev.happens(type):
                event_list.append(ev)

        return event_list


    def toggle_skip(ev_type):
        if persistent.skipped_events[ev_type]:
            persistent.skipped_events[ev_type] = False
        else:
            persistent.skipped_events[ev_type] = True

    def get_vp_bounds(girl, girl_list):

        if selected_view_mode == "x40" or (selected_view_mode=="Auto" and len(girl_list)>24):
            h = girl_but_ysize["x40"]
            col = 4
            lines = 10
        elif selected_view_mode == "x24" or (selected_view_mode=="Auto" and len(girl_list)>12):
            h = girl_but_ysize["x24"]
            col = 3
            lines = 8
        elif selected_view_mode == "x12" or (selected_view_mode=="Auto" and len(girl_list)>4):
            h = girl_but_ysize["x12"]
            col = 2
            lines = 6
        else:
            h = girl_but_ysize["x4"]
            col = 1
            lines = 4

        if girl in girl_list:
            top_position = girl_list.index(girl)//col * h
            bottom_position = (girl_list.index(girl)//col-(lines-1)) * h

            top_bound = top_position - (lines-1) * h
            bottom_bound = bottom_position + (lines-1) * h

            return top_bound, bottom_bound

        else:
            return 0,0

    def focus_vp(girl_list):

        # This adjusts the viewport to show the selected girl

        if selected_girl in girl_list:
            top_bound, bottom_bound = get_vp_bounds(selected_girl, girl_list)

            if vp_adj.value < top_bound:
                vp_adj.change(top_bound)

            elif vp_adj.value > bottom_bound:
                vp_adj.change(bottom_bound)

        else:
            vp_adj.change(0)

        renpy.restart_interaction()

        return


    def select_previous_girl(girl_list, loop=True, pace=1):

        global selected_girl

        # if selected_girl and selected_girl in girl_list:
        #     previousindex = girl_list.index(selected_girl) - pace
        # else:
        #     previousindex = 0
        #
        # if previousindex < 0:
        #     if loop:
        #         previousindex = len(girl_list) -1
        #     else:
        #         previousindex = girl_list.index(selected_girl)
        #
        # selected_girl = girl_list[previousindex]

        selected_girl = get_previous(girl_list, selected_girl, loop, pace)

        focus_vp(girl_list)

        return

    def get_previous(mylist, current, loop=False, pace=1, avoid=None):

        mylist = [it for it in mylist if it != avoid]

        if mylist:
            if current in mylist:
                previousindex = mylist.index(current) - pace
            else:
                previousindex = 0

            if previousindex < 0:
                if loop:
                    previousindex = len(mylist) -1
                else:
                    previousindex = mylist.index(current)

            return mylist[previousindex]
        return current # Fallback

    def get_next(mylist, current, loop=False, pace=1, avoid=None):

        mylist = [it for it in mylist if it != avoid]

        if mylist:
            if current in mylist:
                nextindex = mylist.index(current) + pace
            else:
                nextindex = 0

            if nextindex > len(mylist) -1:
                if loop:
                    nextindex = 0
                else:
                    nextindex = len(mylist) -1

            return mylist[nextindex]
        return current # Fallback

    def select_next_girl(girl_list, loop=True, pace=1):

        global selected_girl

        # if selected_girl and selected_girl in girl_list:
        #     nextindex = girl_list.index(selected_girl) + pace
        # else:
        #     nextindex = 0
        #
        # if nextindex > len(girl_list) -1:
        #     if loop:
        #         nextindex = 0
        #     else:
        #         nextindex = girl_list.index(selected_girl)

        selected_girl = get_next(girl_list, selected_girl, loop, pace)

#        renpy.notify("Selected girl is " + selected_girl.name)

        focus_vp(girl_list)

        return

    def can_interact(girl, type = None, slave = True, silent=True): # Antiquated, to be replaced by the GirlInteractionTopic method

        if not girl in MC.girls and slave:
            return False

        if MC.interactions < 1:
            return False

        if type:
            if type == "train" and girl.MC_interact_counters[type] >= 1:
                if not silent:
                    renpy.say("", __("You cannot train a girl more than once per day."))
                return False

            elif type in ("present", "money", "offer") and girl.MC_interact_counters[type] >= 1:
                return False

            elif type == "offer" and len(MC.girls) >= brothel.bedrooms:
                return False

            elif girl.MC_interact_counters[type] >= 3:
                if not silent:
                    renpy.say("", __("You cannot do the same things more than 3 times a day with a girl."))
                return False

        return True

    def get_act_menu(prompt=None, extended=True, girl=None, conditions=True):
        if extended:
            acts = extended_sex_acts
        else:
            acts = all_sex_acts

        menu_list = []

        if prompt:
            menu_list.append((prompt, None))

        for act in acts:
            text1 = long_act_description["action " + act]

            if girl and conditions and training_test_dict[act]: # Tests thresholds for training girls

                condition_met = False

                for cond, pref in training_test_dict[act]:
                    if compare_preference(girl, cond, pref):
#                            renpy.say("", "Can display " + act + " because " + cond + " is " + pref + " or more.")
                        condition_met=True
                        break
            else:
                condition_met = True

            if girl:
                if girl.personality_unlock[act]:
                    if act in girl.pos_acts and act in girl.neg_acts:
                        text1 = __(text1) + " (%s)" % emo_yang
                    elif act in girl.pos_acts:
                        text1 = __(text1) + " (%s)" % emo_heart
                    elif act in girl.neg_acts:
                        text1 = __(text1) + " (%s)" % emo_lightning
                else:
                    text1 = __(text1) + " (?)"

            if condition_met:
                menu_list.append((text1, act))

        menu_list.append(("Go back", "back"))

        return menu_list



    def get_fix_menu(act, step = "all", girl = None):

        menu_list = []#[(prompt, None),]

        fix_list = get_fix_list(act, step)

        if girl:
            pos_fix = [f.name for f in girl.pos_fixations]
            neg_fix = [f.name for f in girl.neg_fixations]

        for fix in fix_list:
            text1 = fix_description[fix.name + " action"]

            if girl:
                if girl.personality_unlock[fix.name]:
                    if fix.name in pos_fix:
                        text1 = __(text1) + " (%s)" % emo_heart
                    elif fix.name in neg_fix:
                        text1 = __(text1) + " (%s)" % emo_lightning
                else:
                    text1 = __(text1) + " (?)"

            menu_list.append((text1, fix))

        menu_list.append(("Nothing special", "no fix"))

        return menu_list

    def get_fix_list(act, step = "all"):

        if step == "all":
            return [fix for fix in fix_dict.values() if act in fix.acts]

        else:
            return [fix for fix in fix_dict.values() if act in fix.acts and step == fix.step]


    def multiple_choice_menu(prompt, menu_list, limit=9, nb=1): # Returns a list of nb choices, or the "back" string if cancelled

        _selected = []
        menu_list = list(menu_list) # Copying to avoid issues

        for _ in range(nb):
            _selected.append(long_menu(prompt + __(" (%i/%i)") % (len(_selected), nb), menu_list, limit))

            if _selected[-1] == "back":
                return "back"

            for it in menu_list:
                if it[1] == _selected[-1]: # Compares returned value with last selected choice
                    menu_list.remove(it) # Removing from list is okay because of break
                    break

        return _selected


    def long_menu(prompt, menu_list, limit=9): # Creates a menu with next/previous commands if menu has many items

        if len(menu_list) <= limit:
            return menu([(prompt, None)] + menu_list)

        idx = 0
        limit -= 2

        while True:
            end = idx + limit

            if end > len(menu_list):
                end = len(menu_list)

            if prompt:
                part_menu = [(prompt, None)] + menu_list[idx:end]
            else:
                part_menu = menu_list[idx:end]

            if idx > 0:
                part_menu += [(__("{i}Previous{/i}"), "previous")]
            else:
                part_menu += [(__("{color=#AAA}{i}Previous{/i}"), "previous")]

            if end < len(menu_list):
                part_menu += [(__("{i}Next{/i}"), "next")]
            else:
                part_menu += [(__("{color=#AAA}{i}Next{/i}"), "next")]

            r = menu(part_menu)

            if r == "next":
                if end < len(menu_list):
                    idx += limit

            elif r == "previous":
                if idx > 0:
                    idx -= limit

            else:
                return r

    def shake_mouse(amplitude=150):

        amplitude = yres(amplitude)

        renpy.set_mouse_pos(renpy.get_mouse_pos()[0] + renpy.random.randint(0, amplitude) - xres(75), renpy.get_mouse_pos()[1] + (renpy.random.randint(yres(50), amplitude) * renpy.random.choice((-1, 1))), 0.1)

        return

    def commit_start_settings():
        for s in NGP_settings:
            s.record()

        # Gold/Resources
        MC.gold = int(starting_gold + NGP_settings_dict["starting gold"].get())

        for rk, nb in [(i+2, NGP_settings_dict["starting resources"].values[i+1]) for i in range(NGP_settings_dict["starting resources"].index)]:
            for res in build_resources:
                if resource_dict[res].rank == rk:
                    MC.gain_resource(res, nb, message=False)

        if NGP_settings_dict["extractors Mk I"].get():
            for _ in range(NGP_settings_dict["extractors Mk I"].get()):
                MC.add_item(extractor_items["extractor1"].get_instance(), use_sound=False)

        if NGP_settings_dict["extractors Mk II"].get():
            for _ in range(NGP_settings_dict["extractors Mk II"].get()):
                MC.add_item(extractor_items["extractor2"].get_instance(), use_sound=False)

        # Init girlpack mix
        game.init_mixes()

        # Adjust MC stats and spells
        if NGP_settings_dict["good alignment"].get():
            MC.good += 10
        if NGP_settings_dict["evil alignment"].get():
            MC.evil += 10

        for stat in all_MC_stats:
            if NGP_settings_dict[stat].get():
                pic = {"strength" : "bear.webp", "spirit" : "sorcerer.webp", "charisma" : "ghost.webp", "speed" : "speed.webp"}[stat]
                MC.learn(Spell(NGP_settings_dict[stat].label, pic, type="passive", level=1, effects=[Effect("gain", stat, NGP_settings_dict[stat].get()), Effect("change", stat + " max", NGP_settings_dict[stat].get())], description=__("Gain %i to MC's %s and %s maximum.") % (NGP_settings_dict[stat].get(), stat.capitalize(), stat.capitalize())))
                # MC.change_stat(stat, NGP_settings_dict[stat].get(), False, ignore_ceil=True)

        if NGP_settings_dict["love generation"].get():
            MC.learn(Spell(NGP_settings_dict["love generation"].label, 'love.webp', type="passive", level=1, effects=[Effect("boost", "love gains", NGP_settings_dict["love generation"].get(), scope="brothel")], description=__("Boosts love gains by %i per cent (NewGame+ effect).") % (100*NGP_settings_dict["love generation"].get())))

        if NGP_settings_dict["fear generation"].get():
            MC.learn(Spell(NGP_settings_dict["fear generation"].label, 'doll_.webp', type="passive", level=1, effects=[Effect("boost", "fear gains", NGP_settings_dict["fear generation"].get(), scope="brothel")], description=__("Boosts fear gains by %i per cent (NewGame+ effect).") % (100*NGP_settings_dict["fear generation"].get())))

        if NGP_settings_dict["xp generation"].get():
            MC.learn(Spell(NGP_settings_dict["xp generation"].label, 'enhanced.webp', type="passive", level=1, effects=[Effect("boost", "xp gains", NGP_settings_dict["xp generation"].get(), scope="brothel")], description=__("Boosts your girl's XP gains by %i per cent (NewGame+ effect).") % (100*NGP_settings_dict["xp generation"].get())))

        if NGP_settings_dict["jp generation"].get():
            MC.learn(Spell(NGP_settings_dict["jp generation"].label, 'hand.webp', type="passive", level=1, effects=[Effect("boost", "all jp gains", NGP_settings_dict["jp generation"].get(), scope="brothel")], description=__("Boosts your girl's JP gains by %i per cent (NewGame+ effect).") % (100*NGP_settings_dict["jp generation"].get())))

        if NGP_settings_dict["prestige generation"].get():
            MC.learn(Spell(NGP_settings_dict["prestige generation"].label, 'fame.webp', type="passive", level=1, effects=[Effect("boost", "prestige", NGP_settings_dict["prestige generation"].get())], description=__("Boosts your prestige gains by %i per cent (NewGame+ effect).") % (100*NGP_settings_dict["prestige generation"].get())))

        if NGP_settings_dict["training efficiency"].get():
            MC.learn(Spell(NGP_settings_dict["training efficiency"].label, 'discipline.webp', type="passive", level=1, effects=[Effect("boost", "MC training", NGP_settings_dict["training efficiency"].get())], description=__("Boosts your girls' gains from your personal training by %i per cent (NewGame+ effect).") % (100*NGP_settings_dict["training efficiency"].get())))

        if NGP_settings_dict["tax reduction"].get():
            MC.learn(Spell(NGP_settings_dict["tax reduction"].label, 'haggler.webp', type="passive", level=1, effects=[Effect("boost", "taxes", -NGP_settings_dict["tax reduction"].get())], description=__("Reduces your total taxes by %i per cent (NewGame+ effect).") % (100*NGP_settings_dict["tax reduction"].get())))

        # Item dispensers
        if NGP_settings_dict["free girl"].get():
            if NGP_settings_dict["free girl"].get() == "once":
                MC.add_item(seduction_potion.get_instance(), use_sound=False)
            else:
                Furniture(NGP_settings_dict["free girl"].label + " kit", type='NewGame+', pic='wine cases.webp', rank=0, chapter=0, cost=[], duration=0, effects=[Effect("event", "dispense_item", "free girl")], hidden_effect=True, base_description=__("Receive a %s Potion of Seduction.") % NGP_settings_dict["free girl"].get()).build()

        if NGP_settings_dict["virginity"].get():
            if NGP_settings_dict["virginity"].get() == "once":
                MC.add_item(restoration_balm.get_instance(), use_sound=False)
            else:
                Furniture(NGP_settings_dict["virginity"].label + " kit", type='NewGame+', pic='platinum statue.webp', rank=0, chapter=0, cost=[], duration=0, effects=[Effect("event", "dispense_item", "virginity")], hidden_effect=True, base_description=__("Receive a %s Balm of Restoration.") % NGP_settings_dict["virginity"].get()).build()

        if NGP_settings_dict["sanity"].get():
            if NGP_settings_dict["sanity"].get() == "once":
                MC.add_item(bliss_incense.get_instance(), use_sound=False)
            else:
                Furniture(NGP_settings_dict["sanity"].label + " kit", type='NewGame+', pic='sofa2.webp', rank=0, chapter=0, cost=[], duration=0, effects=[Effect("event", "dispense_item", "sanity")], hidden_effect=True, base_description=__("Receive a %s Incense of Bliss.") % NGP_settings_dict["sanity"].get()).build()

        if NGP_settings_dict["interactions"].get():
            if NGP_settings_dict["interactions"].get() == "once":
                MC.add_item(magic_powder.get_instance(), use_sound=False)
            else:
                Furniture(NGP_settings_dict["interactions"].label + " kit", type='NewGame+', pic='explosive traps.webp', rank=0, chapter=0, cost=[], duration=0, effects=[Effect("event", "dispense_item", "interactions")], hidden_effect=True, base_description=__("Receive a %s Magic Powder.") % NGP_settings_dict["interactions"].get()).build()

        if NGP_settings_dict["perks"].get():
            if NGP_settings_dict["perks"].get() == "once":
                MC.add_item(wyvern_egg.get_instance(), use_sound=False)
            else:
                Furniture(NGP_settings_dict["perks"].label, type='NewGame+', pic='wine cases.webp', rank=0, chapter=0, cost=[], duration=0, effects=[Effect("event", "dispense_item", "perks")], hidden_effect=True, base_description=__("Receive a %s Wyvern egg.") % NGP_settings_dict["perks"].get()).build()

        if NGP_settings_dict["autorest"].get():
            vitals_scanner.description += __(" Allows autorest to be set up from the Schedule screen.")
            vitals_scanner.build()

        if NGP_settings_dict["girl"].get():
            rank = NGP_settings_dict["girl"].get()
            level = 1 + (rank-1)*5

            girl = get_girl(free=False, level_range=[level, level])
            MC.girls.append(girl)
            girl.init_after_acquire()
            notify(__("You have received %s as a starting slave!") % girl.fullname, pic=girl.portrait)

        if NGP_settings_dict["free girl challenge"].get():
            calendar.set_alarm(1, StoryEvent("free_girl_challenge", type="morning"))
            slavemarket.active = False
            MC.learn(Spell(NGP_settings_dict["free girl challenge"].label, 'girl.webp', type="passive", level=1, description=__("Slavemarket is disabled. You receive a new girl at the start of each month. (NewGame+ effect).")))

        if NGP_settings_dict["training challenge"].get():
            MC.training = False
            MC.learn(Spell(NGP_settings_dict["training challenge"].label, 'militia.webp', type="passive", level=1, effects=[Effect("boost", "farm training", 1.0)], description=__("The Farm becomes much more efficient, but you can no longer personally train your girls. (NewGame+ effect).")))

        # naturist frequency is handled in BKgirlclass.rpy generate_traits()

        MC.reset_interactions()


    def unlocking_extras():
        global unlocked_shops
        global gizel_name
        global carpenter_name
        global goldie_name
        global willow_name
        global gina_name
        global stella_name
        global gurigura_name
        global ramias_name
        global katryn_name
        global riche_name


        # if game.starting_gold:
        #     if int(game.starting_gold) > starting_gold:
        #         game.achievements = False
        #         # renpy.notify("gold")

        # if starting_chapter > 1 or [x for x in extras_dict.values() if x]:
        #     # game.achievements = False
        #     # renpy.notify("chapter")

        #     if starting_chapter > 1:
        #         story_flags["c1_path"] = c1_path

        # starting_chapter is handled in BKstart.rpy

        # Unlock farm
        if NGP_settings_dict["farm"].get() or debug_mode or not game.is_story_mode():
            # game.achievements = False

            farm.activate()
            farm_firstvisit = False
            gizel_name = "Gizel"

            ## EN: Also queue the rancher shop unlock and merchant meetings
            ##     that the story chain normally adds (farm_gizel_introduction).
            ##     Without this, NG+/debug farm unlocks permanently miss
            ##     Goldie's shop and the Stella/Willow/Gina meetings.
            ##     Duplicate-safe: unlocking_extras() runs at every chapter
            ##     change, so only add events that never fired and are absent.
            ## ZH: 顺带补入剧情链（farm_gizel_introduction）才会添加的牧场
            ##     商店解锁与商人相遇事件，否则 NG+/调试 解锁农场会永久
            ##     错过 Goldie 商店及 Stella/Willow/Gina 相遇。去重保护：
            ##     本函数每次换章都会运行，只补未触发且不在列表中的事件。
            if globals().get("event_dict") is not None:
                for _farm_lbl in ("farm_activate_goldie", "farm_meet_stella", "farm_meet_willow", "farm_meet_gina"):
                    _farm_ev = event_dict.get(_farm_lbl)
                    if _farm_ev is not None and not _farm_ev.happened and _farm_ev not in city_events:
                        story_add_event(_farm_lbl)

        # Unlock Carpenter's Wagon
        if NGP_settings_dict["carpenter"].get() or debug_mode or (game.chapter >= 2 and not game.is_story_mode()):
            # game.achievements = False

            NPC_carpenter.active = True
            story_flags["found wagon"] = True
            story_flags["met carpenter"] = True
            carpenter_name = "Iulia"

        # if extras_dict["locations"]:
        #     game.achievements = False
        #     if final:
        #         thieves_guild.secret = False
        #         thieves_guild.action = True

        # Unlock Minion merchants (BK Evolution: data-driven by unlock_batch)
        if NGP_settings_dict["minion merchants"].get() or debug_mode or not game.is_story_mode():

            unlock("farmland")
            sewers.action = True
            junkyard.action = True
            goldie_name = "Goldie"
            willow_name = "Willow"
            gina_name = "Gina"
            _batch = [s for s in all_shops if getattr(s, 'unlock_batch', None) == "minion_early"]
            if not _batch:
                _batch = [NPC_goldie, NPC_willow, NPC_gina]
            unlocked_shops += [m for m in _batch if m not in unlocked_shops]

        if NGP_settings_dict["minion merchants"].get() or debug_mode or (game.chapter >= 2 and not game.is_story_mode()):

            harbor.action = True
            stella_name = "Stella"
            _batch = [s for s in all_shops if getattr(s, 'unlock_batch', None) == "minion_late"]
            if not _batch:
                _batch = [NPC_stella]
            for m in _batch:
                if m not in unlocked_shops:
                    unlocked_shops.append(m)

        # Unlock Item merchants (BK Evolution: data-driven by unlock_batch)
        if NGP_settings_dict["item merchants"].get() or debug_mode or (game.chapter >= 2 and not game.is_story_mode()):

            arena.action = True
            prison.action = True
            exotic_emporium.action = True
            market.action = True
            gurigura_name = "Gurigura"
            ramias_name = "Ramias"
            _batch = [s for s in all_shops if getattr(s, 'unlock_batch', None) == "item_early"]
            if not _batch:
                _batch = [NPC_ramias, NPC_gurigura, NPC_giftgirl]
            unlocked_shops += [m for m in _batch if m not in unlocked_shops]

        if NGP_settings_dict["item merchants"].get() or debug_mode or (game.chapter >= 4 and not game.is_story_mode()):

            botanical_garden.action = True
            magic_university.action = True
            pilgrim_road.action = True
            katryn_name = "Katryn"
            riche_name = "Riche"
            _batch = [s for s in all_shops if getattr(s, 'unlock_batch', None) == "item_late"]
            if not _batch:
                _batch = [NPC_riche, NPC_katryn, NPC_twins]
            unlocked_shops += [m for m in _batch if m not in unlocked_shops]

        # Unlock Trainers
        if NGP_settings_dict["all trainers"].get() or debug_mode or not game.is_story_mode():
            # game.achievements = False
            for t in game.trainers:
                if t not in MC.trainers:
                    MC.trainers.append(t)

        # Debugging
        if debug_mode:
            shipyard.action = True # Wood
            stables.action = True # Leather
            beach.action = True # Dye
            old_ruins.action = True # Stone
            hanging_gardens.action = True # Silk
            guild_quarter.action = True # Ore
            falls.action = True # Diamond


        # if extras_dict["shops"]:
        #     game.achievements = False
        #     if final:
        #         farm.action = True
        #         sewers.action = True
        #         junkyard.action = True
        #         unlocked_shops += [m for m in [NPC_goldie, NPC_willow, NPC_gina] if m not in unlocked_shops]

        #         if extras_dict["shops"] >= 2:
        #             harbor.action = True
        #             arena.action = True
        #             prison.action = True
        #             exotic_emporium.action = True
        #             market.action = True
        #             unlocked_shops += [m for m in [NPC_stella, NPC_ramias, NPC_gurigura, NPC_giftgirl] if m not in unlocked_shops]

        #         if extras_dict["shops"] >= 4:
        #             botanical_garden.action = True
        #             library.action = True
        #             pilgrim_road.action = True
        #             unlocked_shops += [m for m in [NPC_riche, NPC_katryn, NPC_twins] if m not in unlocked_shops]

        # if extras_dict["resources"]:
        #     game.achievements = False
        #     if final:
        #         if extras_dict["resources"] >= 2:
        #             shipyard.action = True
        #             stables.action = True
        #             beach.action = True
        #         if extras_dict["resources"] >= 4:
        #             old_ruins.action = True
        #             hanging_gardens.action = True
        #             guild_quarter.action = True
        #         if extras_dict["resources"] >= 6:
        #             falls.action = True
        #     # renpy.notify("resources")

    def update_available_mixes():
        available_mixes = persistent.girl_mix.keys()

        for mix in persistent.game_mixes:
            if mix not in available_mixes:
                renpy.notify(__("Removing %s from game mixes") % mix)
                persistent.game_mixes.remove(mix)

        if len(available_mixes) == 1 or len(persistent.game_mixes) == 0:
            persistent.game_mixes = ["default"]

        return list(available_mixes)

    def get_day_report(_log):
        # Phase 0.2: All report strings now use __() for I18N.
        # The plural() function is language-aware — returns "" for CJK locales.

        gold_str = __("gold")

        if _log.net >= 0:
            msg = __("You made %s last night.\n") % (event_color["good"] % (str(round_int(_log.net)) + " " + gold_str),)
        else:
            msg = __("You lost %s last night.\n") % (event_color["bad"] % (str(round_int(_log.net)) + " " + gold_str),)

        msg += "{size=-2}" + __("- Gold made: + %s\n") % (event_color["good"] % str(round_int(_log.gold_made)),)
        msg += __("- Girls upkeep: - %s\n") % (event_color["bad"] % str(round_int(_log.upkeep)),)
        msg += __("- Brothel costs: - %s\n{/size}\n") % (event_color["bad"] % str(round_int(_log.costs)),)

        msg += __("%s customer%s came to the brothel.\n") % (str(_log.cust), plural(_log.cust))
        msg += "{size=-2}" + __("- Customer%s served (job): %s/%s\n") % (plural(_log.check("served")), event_color["good"] % str(_log.check("served")), str(_log.cust))
        msg += __("- Customer%s entertained (job): %s/%s\n") % (plural(_log.check("entertained")), event_color["good"] % str(_log.check("entertained")), str(_log.check("served")))
        msg += __("- Customer%s served (sex): %s/%s\n") % (plural(_log.check("laid")), event_color["good"] % str(_log.check("laid")), str(_log.cust))
        msg += __("- Customer%s satisfied (sex): %s/%s\n{/size}\n") % (plural(_log.check("satisfied")), event_color["good"] % str(_log.check("satisfied")), str(_log.check("laid")))

        msg += __("%s girl%s worked in the brothel. ") % (str(_log.check("work_days")), plural(_log.check("work_days")))

        if _log.check("strike_days"):
            msg += event_color["bad"] % __("%s girl%s went on strike. ") % (str(_log.check("strike_days")), plural(_log.check("strike_days")))
        if _log.check("run_away"):
            msg += event_color["bad"] % __("%s girl%s ran away from the brothel.") % (str(_log.check("run_away")), plural(_log.check("run_away")))

        msg += __("\n{size=-2}- Waitress: %s\n") % (event_color["good"] % str(_log.check("waitress_days")),)
        msg += __("- Dancer: %s\n") % (event_color["good"] % str(_log.check("dancer_days")),)
        msg += __("- Masseuse: %s\n") % (event_color["good"] % str(_log.check("masseuse_days")),)
        msg += __("- Geisha: %s\n") % (event_color["good"] % str(_log.check("geisha_days")),)
        msg += __("- Whore: %s\n{/size}\n") % (event_color["good"] % str(_log.check("whore_days")),)

        if _log.check("rest_days") > 1:
            msg += __("%s girls were resting at the brothel. ") % str(_log.check("rest_days"))
        elif _log.check("rest_days") > 0:
            msg += __("%s girl was resting at the brothel. ") % str(_log.check("rest_days"))

        if _log.check("hurt_days") > 1:
            msg += event_color["bad"] % __("%s girls were hurt while working. ") % str(_log.check("hurt_days"))
        elif _log.check("hurt_days") > 0:
            msg += event_color["bad"] % __("%s girl was hurt while working. ") % str(_log.check("hurt_days"))

        if _log.check("exhausted"):
            msg += event_color["bad"] % __("%s girl%s became exhausted while working. ") % (str(_log.check("exhausted")), plural(_log.check("exhausted")))

        msg += "\n"

        if farm.active:
            msg += __("%s girls were at the farm last night. ") % str(_log.check("farm_days") + _log.check("farm_rest_days"))

            if _log.check("farm_resisted_training"):
                msg += event_color["bad"] % __("%s girl%s resisted training. ") % (str(_log.check("farm_resisted_training")), plural(_log.check("farm_resisted_training")))

            if _log.check("farm_run_away"):
                msg += event_color["bad"] % __("%s girl%s ran away from the farm.") % (str(_log.check("farm_run_away")), plural(_log.check("farm_run_away")))

            if _log.check("farm_hurt"):
                msg += event_color["bad"] % __("%s girl%s got hurt while resisting.") % (str(_log.check("farm_hurt")), plural(_log.check("farm_hurt")))

            if _log.check("minion_hurt"):
                msg += event_color["bad"] % __("%s minion%s got hurt in the fighting.") % (str(_log.check("minion_hurt")), plural(_log.check("minion_hurt")))

            msg += "\n{size=-2}" + __("- In training: %s\n") % (event_color["good"] % str(_log.check("farm_training_days")),)
            msg += __("- In holding: %s{/size}\n") % (event_color["good"] % str(_log.check("farm_holding_days")),)

            if _log.check("farm_rest_days") > 1:
                msg += __("%s girls were resting at the farm. ") % str(_log.check("farm_rest_days"))
            elif _log.check("farm_rest_days") > 0:
                msg += __("%s girl was resting at the farm. ") % str(_log.check("farm_rest_days"))

        return msg

    def get_next_day_report(): # Compiles Yesterday's report for the Brothel screen

        n = len(MC.girls)
        msg = __("You have %s girl%s in your brothel (max %s).\n\n") % (n, plural(n), brothel.bedrooms)

        working_girls = sum(1 for girl in MC.girls if girl.works_today(check_autorest=True))
        waitresses = sum(1 for girl in MC.girls if girl.works_today(check_autorest=True) and girl.job == "waitress")
        dancers = sum(1 for girl in MC.girls if girl.works_today(check_autorest=True) and girl.job == "dancer")
        masseuses = sum(1 for girl in MC.girls if girl.works_today(check_autorest=True) and girl.job == "masseuse")
        geishas = sum(1 for girl in MC.girls if girl.works_today(check_autorest=True) and girl.job == "geisha")
        whores = sum(1 for girl in MC.girls if girl.works_today(check_autorest=True) and girl.job == "whore")
        away = sum(1 for girl in MC.girls if girl.away)
        resting = sum(1 for girl in MC.girls if not girl.works_today(check_autorest=True) and not girl.away)

        msg += __("%s girl%s will be working tonight.") % (working_girls, plural(working_girls))

        msg += __("\n{size=-2}- Waitress: %s\n") % (event_color["good"] % str(waitresses))
        msg += __("- Dancer: %s\n") % (event_color["good"] % str(dancers))
        msg += __("- Masseuse: %s\n") % (event_color["good"] % str(masseuses))
        msg += __("- Geisha: %s\n") % (event_color["good"] % str(geishas))
        msg += __("- Whore: %s\n{/size}\n") % (event_color["good"] % str(whores))

        if away > 1:
            msg += __("%s are away on a quest or class.\n\n") % away
        elif away > 0:
            msg += __("%s is away on a quest or class.\n\n") % away

        msg += __("%s girl%s will be resting at the brothel tonight.\n\n") % (resting, plural(resting))

        if farm.active:
            farm_training = sum(1 for girl in farm.girls if farm.programs[girl].target != "no training")
            farm_holding = sum(1 for girl in farm.girls if farm.programs[girl].target == "no training" and farm.programs[girl].holding != "rest")
            farm_resting = sum(1 for girl in farm.girls if farm.programs[girl].target == "no training" and farm.programs[girl].holding == "rest")

            msg += __("%s girl%s will be at the farm tonight.") % (len(farm.girls), plural(len(farm.girls)))

            msg += __("\n{size=-2}- In training: %s\n") % (event_color["good"] % str(farm_training))
            msg += __("- In holding: %s\n{/size}\n") % (event_color["good"] % str(farm_holding))

            msg += __("%s girl%s will be resting at the farm tonight.") % (farm_resting, plural(farm_resting))

        return msg


    def get_warnings():

        msg = ""

        # Escaped girls

        for girl in MC.escaped_girls:
            msg += event_color["bad"] % (girl.fullname + " has escaped the brothel and has yet to return.\n")

        # Grumbling girls

        for girl in MC.girls:
            if girl.run_away_check():
                msg += event_color["a little bad contrast"] % (__("Warning! %s is grumbling about running away.\n") % girl.fullname)

        # Tired and hurt girls

        for girl in MC.girls:
            if girl.tired_check():
                msg += event_color["a little bad contrast"] % (girl.fullname + " is getting tired.\n")

            if girl.exhausted:
                msg += event_color["bad"] % (girl.fullname + " is exhausted and cannot work until she is fully rested.\n")

            if girl.hurt:
                msg += event_color["bad"] % (girl.fullname + " is hurt and cannot work until she is fully rested.\n")

        # News

        msg += "\n"

#         if game.token > 0:
#             msg += event_color["special"] % "You are ready to move to a new district.\n\n"

        if MC.skill_points > 0:
            msg += event_color["good"] % "You are ready to level up.\n"

        ready_to_level = sum(1 for girl in MC.girls if girl.upgrade_points >= 1)
        ready_to_perk = sum(1 for girl in MC.girls if girl.perk_points > 0)

        if ready_to_level > 1:
            msg += event_color["good"] % (str(ready_to_level) + " girls have unspent skill points.\n")
        elif ready_to_level > 0:
            msg += event_color["good"] % (str(ready_to_level) + " girl has unspent skill points.\n")

        if ready_to_perk > 1:
            msg += event_color["good"] % (str(ready_to_perk) + " girls have unspent perk points.\n")
        elif ready_to_perk > 0:
            msg += event_color["good"] % (str(ready_to_perk) + " girl has unspent perk points.\n")

        if shop.updated:
            msg += __("The Shop has received new items.\n\n")

        if slavemarket.active and slavemarket.updated:
            msg += __("The Slave Market has received new girls.\n\n")

        if quest_board.updated:
            msg += __("There are new Classes and Quests available in town.\n\n")

        return msg


    def get_resting_girls():
        return [g for g in MC.girls if (not g.job or g.job == "rest" or g.resting or g.workdays[calendar.get_weekday()] == 0) and not (g.away or g.hurt > 0 or g.exhausted)]

    def get_known_free_girls(min_relationship_level=0):
        return [g for g in game.free_girls if g.MC_interact and g.MC_relationship_level >= min_relationship_level]

    def compile_girl_log(girl): # Used to store girl log calculations in a dictionary and avoid refreshing it with every tick
        log_dict = defaultdict(dict)

        log_dict["age"] = calendar.time - girl.get_log("acquired")

        for days in (1, 7, 28, 0):
            log_dict["total_gold"][days] = girl.get_log("total_gold", days)
            log_dict["quest_gold"][days] = girl.get_log("quest_gold", days)
            log_dict["upkeep"][days] = girl.get_log("upkeep", days)
            log_dict["total_xp"][days] = girl.get_log("total_xp", days)
            log_dict["total_jp"][days] = girl.get_log("total_jp", days)
            log_dict["total_rep"][days] = girl.get_log("total_rep", days)
            log_dict["waitress_days"][days] = girl.get_log("waitress_days", days)
            log_dict["dancer_days"][days] = girl.get_log("dancer_days", days)
            log_dict["masseuse_days"][days] = girl.get_log("masseuse_days", days)
            log_dict["geisha_days"][days] = girl.get_log("geisha_days", days)
            log_dict["whore_days"][days] = girl.get_log("whore_days", days)
            log_dict["work_whore_days"][days] = girl.get_log("work_whore_days", days)
            log_dict["work_days"][days] = girl.get_log("work_days", days)
            log_dict["rest_days"][days] = girl.get_log("rest_days", days)
            log_dict["away_days"][days] = girl.get_log("away_days", days)
            log_dict["farm_days"][days] = girl.get_log("farm_days", days)
            log_dict["strike_days"][days] = girl.get_log("strike_days", days)
            log_dict["hurt_days"][days] = girl.get_log("hurt_days", days)
            log_dict["sick_days"][days] = girl.get_log("sick_days", days)

            for job in all_jobs + ["whore"] + all_sex_acts:
                log_dict[job + "_cust"][days] = girl.get_log(job + "_cust", days)
                log_dict[job + "_gold"][days] = girl.get_log(job + "_gold", days)
                log_dict[job + "_xp"][days] = girl.get_log(job + "_xp", days)
                log_dict[job + "_jp"][days] = girl.get_log(job + "_jp", days)
                log_dict[job + "_rep"][days] = girl.get_log(job + "_rep", days)
                log_dict[job + "_perf"][days] = girl.get_average_performance(job, days)

        return log_dict

    def set_girls_workdays():
        for girl in MC.girls:
            girl.set_workdays()

    def change_district(chosen_district, free=False, start=False): # Change district

        global district

        if not start:
            game.blocked_districts.append(district)

        district = chosen_district

        if not (free or start):
            MC.gold -= blist[game.chapter].cost
            renpy.play(s_gold, "sound")

    def get_starting_furniture(chapter): # lower chapter furniture is built from the beginning
        for furn in all_furniture:
            if furn.chapter < chapter:
                furn.build(message=False)

    def build_all_furniture(chapter=7):
        global all_furniture

        for furn in all_furniture:
            if chapter >= furn.chapter:
                furn.build(message=False)
        all_furniture.append(vitals_scanner)
        all_furniture.append(billboard)

#### END OF BK FUNCTIONS FILE ####
    def create_enemy_brothels(): ### To simulate brothel ranking

        en_brothels = []

        for c in range(7):
            if c+1 == 7:
                total_levels = 7
            else:
                total_levels = 5
            for lvl in range(total_levels):
                en_brothels.append(EnemyBrothel(c+1, lvl+1))

        # Special brothels

        bro1 = EnemyBrothel(7, 5)
        bro1.name = "{font=resources/fonts/DejaVuSans.ttf}HʘʘKERS™{/font}"
        bro1.pic = "resources/backgrounds/slave market8.webp"
        bro1.base_income = 2500000
        en_brothels.append(bro1)

        bro2 = EnemyBrothel(7, 5)
        bro2.name = __("Cloud's Palace")
        bro2.pic = "resources/backgrounds/slave market5.webp"
        bro2.base_income = 5000000
        en_brothels.append(bro2)

        return en_brothels

    def list_stat_changes(stat_dict): # stat_dict should have the following format: {stat_name : value}
        text1 = ""

        for s, v in stat_dict.items():
            if v:
                if s.endswith("preference"):
                    text1 += "\n" + __(s.capitalize()) + ": " + get_plus_rating(v, "pref")
                elif s in stat_increase_dict.keys():
                    text1 += stat_increase_dict[s] % v
                elif v > 0:
                    text1 += stat_increase_dict["stat"] % (__(s.capitalize()), v)
                elif v < 0:
                    text1 += stat_increase_dict["stat_neg"] % (__(s.capitalize()), v)

        return text1

    def MU_jobgirl_event_test():
        if NPC_jobgirl.love >= 10 or NPC_jobgirl.corruption >= 10:
            return True
        return False

    def farm_can_perform_act(girl, act): # Returns bool and tooltip in case of failure
        if act in ("bisexual", "group"): # Can only choose bis / group if some of sexual acts are accepted
            base_acts_number = sum(1 for a in all_sex_acts if girl.will_do_farm_act(a, mode="tough"))
            if act == "bisexual" and base_acts_number < 1:
                return False, __("She must be open to at least one sex act before choosing 'Bisexual'.")
            if act == "group" and base_acts_number < 2:
                return False, __("She must be open to at least two sex acts before choosing 'Group'.")
        if act == "group" and farm.count_minions() < 2: # checks if farm has 2+ healthy minions
            return False, __("Requires 2 or 3 free minions in the farm.")
        return True, ''

