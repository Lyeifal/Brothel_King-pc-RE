#### Effects functions ####

init -3 python:
    def get_effect(thing, type, target, custom_scale=("factor", 0), change_cap=False, iterate=False, randomize=True):
        ## Will return the cumulated value of all applicable effects if test is passed
        # custom_scale is a tuple ('factor name', 'value') which is used for specific perks
        # change_cap=True will only return Effects with the change_cap attribute as True (which means it affects stat min and max)
        # Boost effects are now additive. Let's hope nothing blows up.
        # Special effects return their value (if found), 0 if not found

        # Choose result type

        if type == "special":
            result = 0

        elif type in ("boost"):
            # result is a % expressed as a float. 1.0 (100%) means no positive or negative effect occur.
            result = 1.0
        else:
            # result is a number expressed as int or float. 0 means no positive or negative effect occur.
            result = 0

        # Checks a dictionary to optimize performance (the dictionary is updated through the update_effects function)
        if iterate: # For single items only
            effect_list = [eff for eff in thing.effects if type.lower() == eff.type.lower() and target.lower() == eff.target.lower()]
        else: # Includes world-scope effects
            effect_list = thing.effect_dict[(type.lower(), target.lower())] + game.world_effect_dict[(type.lower(), target.lower())]

        for effect in effect_list:

            # Out of scope effects will be ignored to avoid double proc

            if (effect.scope == "world" and thing not in (brothel, farm, game)) or (effect.scope == "brothel" and thing != brothel) or (effect.scope == "farm" and thing != farm) or (effect.scope == "city" and thing != game):
                continue # Jumps to the next effect in the for loop

            #### APPLIES SCALING EFFECTS ####

            if effect.scales_with:
                if effect.source: # This is used for scoped effects to track the original source and scale accordingly
                    factor = get_scale_factor(effect.source, effect.scales_with, custom_scale=custom_scale)
                else:
                    factor = get_scale_factor(thing, effect.scales_with, custom_scale=custom_scale)
            else:
                factor = 1

            #### TESTING EFFECT PROC CHANCE ####

            chance = effect.chance

            if target != "effect chance": # Applies boost to effect chance if there is one
                if chance < 0.5: # Hard-coded: Effect_chance boost is capped at 50%
                    chance *= (1 + get_effect(thing, "special", "effect chance", iterate=iterate, randomize=randomize)) # Why special and not boost? Description related?
                    if chance > 0.5:
                        chance = 0.5
                chance *= get_effect(thing, "boost", target + " chance", iterate=iterate, randomize=randomize)

            if chance < 1:
                game.chance_log = chance
                if renpy.random.random() > chance or not randomize:
                    continue # Jumps to the next effect in the for loop

            if change_cap and not effect.change_cap:
                continue # Jumps to the next effect in the for loop

            #### ADDING EFFECT VALUE TO RESULT ####

            if effect.dice: # Adds the value of a dice with 'effect.value' faces
                if factor and randomize: # Warning: Factor affects the number of faces the dice has. It should never be a fraction in that case.
                    try:
                        result += dice(effect.value * factor, effect.dice) # New: dice property can be an integer
                    except:
                        result += dice(effect.value * factor)
                else:
                    result += effect.value * factor/2

            else:
                try:
                    result += effect.value * factor
                except:
                    result = effect.value # For special effects that do not use numeric values. Only one active effect returns its value. For now, this type of effects must be checked for with 'raw' activated.

        if type in ("boost") and result < 0:
            # Boost results can never go negative to avoid unintended behavior
            return 0.0

        return result

    def add_effects(thing, effects, apply_boost=False, spillover=False, expires=False):
        ## This function adds effects to a target (thing)

        effects = make_list(effects, obj_type = Effect)
        c = None
        scope_list = [] # Stores affected scope to optimize recourse to update_effect()

        for effect in effects:

            # If the effect will affect dress and equipment effects, the equipment is removed BEFORE applying the effect to be equipped back after.

            if effect.type == "boost" and effect.target in all_equipement_types:
                it_list = []

                # Removes items first
                for it in thing.equipped:

                    if it.type.name.lower() == effect.target:
                        it_list.append(it)
                        thing.unequip(it)

            # Applies effect

            #### GAIN AND INSTANTS ####
            ## Gain and Instant effects are applied immediately and not added to active effects. They cannot expire.
            ## Gained value is returned (note: will not work properly if there are more than one effects)
            ## Gain effects affect a character's stats or attributes. Instant effects affect the world or the brothel. They work the same and are mostly hardcoded.

            if effect.type in ("gain", "instant"):

                if effect.scope == "brothel":
                    for girl in MC.girls:
                        c = effect.gain(girl, apply_boost=apply_boost, spillover=spillover)
                elif effect.scope == "farm":
                    for girl in farm.girls:
                        c = effect.gain(girl, apply_boost=apply_boost, spillover=spillover)
                elif effect.scope == "city":
                    for girl in game.free_girls:
                        c = effect.gain(girl, apply_boost=apply_boost, spillover=spillover)
                elif effect.scope == "world":
                    for girl in MC.girls + farm.girls + game.free_girls:
                        c = effect.gain(girl, apply_boost=apply_boost, spillover=spillover)
                else:
                    c = effect.gain(thing, apply_boost=apply_boost, spillover=spillover)

            #### PERSONALITY EFFECTS ####
            ## This forces a personality on a girl (mostly associated with traits). This cannot override the .ini file 'Always' and 'Never' settings.
            ## Personality effects are permanent and are not added to active effects.

            elif effect.type == "personality":
                thing.generate_personality(effect.target)
                c = effect.target


            #### OTHER EFFECTS ####

            else:
                thing.effects.append(effect)
                thing.effect_dict[(effect.type, effect.target)].append(effect) # Stores active effects in a dictionary for faster access
                if effect.scope:
                    scope_list.append(effect.scope)

                if effect.type == "special":
                    # Naturist effect
                    if effect.target == "naked":
                        if thing not in game.free_girls: # Free girls will not reveal their naturist streak immediately
                            thing.naked = True

            # Re-equip items AFTER the boost effect has been applied
            if effect.type == "boost" and effect.target in all_equipement_types:
                for it in it_list:
                    thing.equip(it)

        if expires:
            calendar.set_alarm(expires, StoryEvent(label = "effect_expired", call_args = [thing, effects]))

        if scope_list:
            update_effects(scope_list)

        return c


    def remove_effects(thing, effects):
        ## This function removes effects from a target (thing)

        effects = make_list(effects, obj_type = Effect)
        scope_list = [] # Stores affected scope to optimize recourse to update_effect()

        for effect in effects:

            #### REMOVE EQUIPMENT BOOST ####
            ## If the effect will affect dress and equipment effects, the equipment is removed BEFORE applying the effect to be equipped back after.

            if effect.type == "boost" and effect.target in all_equipement_types:
                it_list = []

                # Removes items first
                for it in thing.equipped:

                    if it.type.name.lower() == effect.target:
                        it_list.append(it)
                        thing.unequip(it)

            # Remove effect

            if effect in thing.effects:
                thing.effects.remove(effect)
            if effect in thing.effect_dict[(effect.type, effect.target)]:
                thing.effect_dict[(effect.type, effect.target)].remove(effect)
            if effect.scope:
                scope_list.append(effect.scope)

            if effect.type == "boost" and effect.target in all_equipement_types:
                # Re-equip items
                for it in it_list:
                    thing.equip(it)

        if scope_list:
            update_effects(scope_list)


    def get_scale_factor(thing, scales_with, custom_scale=("factor", 0), raw=False):

        if scales_with in ("strength", "spirit", "charisma", "speed"):
            factor = MC.get_stat(scales_with, raw=raw)
        elif scales_with == "defense":
            factor = thing.get_defense()
        elif scales_with in ("rep", "reputation"):
            factor = thing.rep
        elif scales_with == "rank":
            factor = thing.rank
        elif scales_with == "equipped": # Counts every piece of equipment
            factor = len(thing.equipped)
        elif scales_with == "chapter":
            factor = game.chapter
        elif scales_with == "district":
            factor = district.rank
        elif scales_with == custom_scale[0]: # Custom scale
            factor = custom_scale[1]
        else:
            factor = 0 # 'scales_with' effects will be ignored if no scale factor is found (avoids unwarranted bonuses)

        return factor

    def update_effects(scope_list=("world", "brothel", "farm", "city")): # Updates all world-affecting effects.

        if "world" in scope_list:
            game.world_effect_dict = defaultdict(list)

            for source in ([g for g in (MC.girls + farm.girls) if not (g.away or g.hurt or g.exhausted)] + [f for f in brothel.furniture if f.active] + [MC, MC.current_trainer, calendar.moon]):
                if source:
                    for effect in source.effects:
                        if effect.scope == "world":
                            game.world_effect_dict[effect.type, effect.target].append(effect)
                            effect.source = source # Tracks source (sometimes useful for applying scaling effects)

        if "brothel" in scope_list:
            brothel.effect_dict = defaultdict(list)

            for source in ([g for g in MC.girls if not (g.away or g.hurt or g.exhausted)] + [f for f in brothel.furniture if f.active] + [MC, MC.current_trainer, calendar.moon]):
                if source:
                    for effect in source.effects:
                        if effect.scope == "brothel":
                            brothel.effect_dict[effect.type, effect.target].append(effect)
                            effect.source = source # Tracks source (sometimes useful for applying scaling effects)

        if "farm" in scope_list:
            farm.effect_dict = defaultdict(list)

            for source in ([g for g in farm.girls if not (g.away or g.hurt or g.exhausted)] + [f for f in brothel.furniture if f.active] + [MC, MC.current_trainer, calendar.moon]):
                if source:
                    for effect in source.effects:
                        if effect.scope == "farm":
                            farm.effect_dict[effect.type, effect.target].append(effect)
                            effect.source = source # Tracks source (sometimes useful for applying scaling effects)

        if "city" in scope_list:
            game.effect_dict = defaultdict(list)

            for source in ([f for f in brothel.furniture if f.active] + [MC, MC.current_trainer, calendar.moon]):
                if source:
                    for effect in source.effects:
                        if effect.scope == "city":
                            game.effect_dict[effect.type, effect.target].append(effect)
                            effect.source = source # Tracks source (sometimes useful for applying scaling effects)

        # brothel.effect_dict = defaultdict(list)
        # farm.effect_dict = defaultdict(list)
        # game.effect_dict = defaultdict(list)
        #
        # for source in ([g for g in MC.girls if not (g.away or g.hurt or g.exhausted)] + [f for f in brothel.furniture if f.active] + [MC, MC.current_trainer, calendar.moon]):
        #     if source:
        #         for effect in source.effects:
        #             if effect.scope == "brothel" or effect.scope == "world":
        #                 brothel.effect_dict[effect.type, effect.target].append(effect)
        #                 effect.source = source # Tracks source (sometimes useful for applying scaling effects)
        #             elif effect.scope == "farm" or effect.scope == "world":
        #                 farm.effect_dict[effect.type, effect.target].append(effect)
        #                 effect.source = source # Tracks source (sometimes useful for applying scaling effects)
        #             elif effect.scope == "city" or effect.scope == "world":
        #                 game.effect_dict[effect.type, effect.target].append(effect)
        #                 effect.source = source # Tracks source (sometimes useful for applying scaling effects)


    def get_pic_list(thing, tags, and_tags = None, not_tags = None, weighted=True, horizontal=False, vertical=False): # For performance reasons, get_pic_list should always receive lists as arguments

        # Phase 0.4: Check the picture cache first to avoid repeated linear scans
        if weighted:
            cached = PictureCache.get(thing, tags, and_tags, not_tags)
            if cached is not None:
                return cached

        # not_tags will be trimmed if they contradict search_tags or and_tags
        not_tags = make_list(not_tags)
        _not_tags = list(not_tags) # Local copy of not_tags to avoid changing mutable list

        if _not_tags:
#            not_tags = make_tuple(not_tags)
            for tag in tags:
                if tag in _not_tags:
                    _not_tags.remove(tag)

            if and_tags:
                for tag in and_tags:
                    if tag in _not_tags:
                        _not_tags.remove(tag)

        #<Chris12 PackState>
        # Use the new GirlFilesDict
        # Shows unrecognized files based on user settings.
        if weighted:
            if isinstance(thing, Girl):
                show_unrecognized = preferences.packstate_unrecognized != "Hide"
                result = [(pic, pic.get_weight()) for pic in GirlFilesDict.get_pics(thing.path) if not pic.is_trash and (not pic.is_unrecognized or show_unrecognized) and pic.has_tags(tags, and_tags, _not_tags, horizontal=horizontal, vertical=vertical)]
                # Phase 0.4: Cache the result for future lookups
                PictureCache.put(thing, tags, and_tags, not_tags, result)
                return result
            #</Chris12 PackState>
            return [(pic, pic.get_weight()) for pic in thing.pics if pic.has_tags(tags, and_tags, _not_tags, horizontal=horizontal, vertical=vertical)]

        else:
            if isinstance(thing, Girl):
                show_unrecognized = preferences.packstate_unrecognized != "Hide"
                return [pic for pic in GirlFilesDict.get_pics(thing.path) if not pic.is_trash and (not pic.is_unrecognized or show_unrecognized) and pic.has_tags(tags, and_tags, _not_tags, horizontal=horizontal, vertical=vertical)]
            #</Chris12 PackState>
            return [pic for pic in thing.pics if pic.has_tags(tags, and_tags, _not_tags, horizontal=horizontal, vertical=vertical)]


    def get_pic(thing, tags, alt_tags1 = None, alt_tags2 = None, alt_tags3 = None, and_tags = None, not_tags = None, strict = False, and_priority=True, attempts=0, always_stock=False, horizontal=False, vertical=False):

        # First looks for a pic with one of 'tags'
        # If stock pictures are deactivated: the search will move to 'alt_tags1' if no pic is found, then 'alt_tags2', then 'alt_tag3'
        # If stock pictures are activated: the search will move to the default pictures
        # The 'and' and 'not_tags' apply to every set of tags.
        # If 'strict' is on, a False value is returned if no picture can be found with the and/not_tags conditions
        # If 'and_priority' is on, the 'and' and 'not' clauses will only be dropped after the search list has been exhausted
        # If 'always_stock' is on, a default pic will always be provided if it is missing, regardless of the stock_picture setting

        piclist = []

        tags = make_list(tags)
        alt_tags1 = make_list(alt_tags1)
        alt_tags2 = make_list(alt_tags2)
        alt_tags3 = make_list(alt_tags3)
        if and_tags:
            and_tags = make_list(and_tags)
        else:
            and_tags = []
        if not_tags:
            not_tags = make_list(not_tags)
        else:
            not_tags = []

        # Tags will be searched in that order
        if persistent.use_stock_pictures_missing or always_stock:
            search_list = [(thing, tags), (game, tags), (thing, alt_tags1), (game, alt_tags1), (thing, alt_tags2),  (game, alt_tags2), (thing, alt_tags3),  (game, alt_tags3)]
        else:
            search_list = [(thing, tags), (thing, alt_tags1), (thing, alt_tags2), (thing, alt_tags3)]

        for target, search_tags in search_list:

            ## Look for pictures matching ALL requirements
            attempts += 1

            piclist = get_pic_list(target, search_tags, and_tags, not_tags, horizontal=horizontal, vertical=vertical)

            # Drop the horizontal/vertical clause if none found
            if piclist == []:
                piclist +=  get_pic_list(target, search_tags, and_tags, not_tags)

            # Mix with stock pictures if the number of pictures found is too low and the option has been activated in the H menu
            if persistent.use_stock_pictures_low and len(piclist) < stock_picture_threshold and target != game:
                piclist += get_pic_list(game, search_tags, and_tags, not_tags, horizontal=horizontal, vertical=vertical)

            if piclist != []:
#                renpy.say("", str(len(piclist)) + " pictures found: " + and_text([p.filename for p in piclist]))

                pic = weighted_choice(piclist)

#                renpy.say("", "Returning: " + pic.filename)

                game.last_pic = {"tags": search_tags, "and_tags": and_tags, "not_tags": not_tags, "attempts": attempts}

                if persistent.debug_pic_counter:
                    persistent.debug_pic_counter_dict[pic.path] += 1

                return pic

            ## Without and_priority
            # If nothing is found, drop the 'and' clauses (and_priority = False). not_tags clause is dropped last.

            if not and_priority and not strict:

                for i in range(len(and_tags)):
                    attempts += 1

                    _and_tags = and_tags[:-i-1] # Removes and_tags one by one, starting from the last one

                    piclist = get_pic_list(target, search_tags, and_tags=_and_tags, not_tags=not_tags)

                    # Mix with stock pictures if the number of pictures found is too low and the option has been activated in the H menu
                    if persistent.use_stock_pictures_low and len(piclist) < stock_picture_threshold and target != game:
                        piclist += get_pic_list(game, search_tags, and_tags=_and_tags, not_tags=not_tags, horizontal=horizontal, vertical=vertical)

                    if piclist != []:
                        pic = weighted_choice(piclist)
                        game.last_pic = {"tags": search_tags, "and_tags": and_tags, "not_tags": not_tags, "attempts": attempts}

                        if persistent.debug_pic_counter:
                            persistent.debug_pic_counter_dict[pic.path] += 1

                        return pic

                # If this is not enough, removes 'not_tags'
                for i in range(len(not_tags)):
                    attempts += 1

                    _not_tags = not_tags[:-i-1] # Removes not_tags one by one, starting from the last one

                    piclist = get_pic_list(target, search_tags, not_tags=_not_tags)

                    # Mix with stock pictures if the number of pictures found is too low and the option has been activated in the H menu
                    if persistent.use_stock_pictures_low and len(piclist) < stock_picture_threshold and target != game:
                        piclist += get_pic_list(game, search_tags, not_tags=_not_tags, horizontal=horizontal, vertical=vertical)

                    if piclist != []:
                        pic = weighted_choice(piclist)
                        game.last_pic = {"tags": search_tags, "and_tags": and_tags, "not_tags": not_tags, "attempts": attempts}

                        if persistent.debug_pic_counter:
                            persistent.debug_pic_counter_dict[pic.path] += 1

                        return pic

        # If nothing is found, drop the 'and' clauses (and_priority = True). not_tags clause is dropped last.

#        renpy.say("", "No matching pictures found.")


        ## With and_priority
        if and_priority and not strict:

            for i in range(len(and_tags)):
                _and_tags = and_tags[:-i-1] # Removes and_tags one by one, starting from the last one

                for target, search_tags in search_list:

                    attempts += 1

                    piclist = get_pic_list(target, search_tags, and_tags=_and_tags, not_tags=not_tags)

                    # Mix with stock pictures if the number of pictures found is too low and the option has been activated in the H menu
                    if persistent.use_stock_pictures_low and len(piclist) < stock_picture_threshold and target != game:
                        piclist += get_pic_list(game, search_tags, and_tags=_and_tags, not_tags=not_tags)

                    if piclist != []:
                        pic = weighted_choice(piclist)

                        game.last_pic = {"tags": search_tags, "and_tags": and_tags, "not_tags": not_tags, "attempts": attempts}

                        if persistent.debug_pic_counter:
                            persistent.debug_pic_counter_dict[pic.path] += 1

                        return pic

            for i in range(len(not_tags)):
                _not_tags = not_tags[:-i-1] # Removes not_tags one by one, starting from the last one

                for target, search_tags in search_list:

                    attempts += 1

                    piclist = get_pic_list(target, search_tags, not_tags=_not_tags)

                    # Mix with stock pictures if the number of pictures found is too low and the option has been activated in the H menu
                    if persistent.use_stock_pictures_low and len(piclist) < stock_picture_threshold and target != game:
                        piclist += get_pic_list(game, search_tags, not_tags=_not_tags)

                    if piclist != []:
                        pic = weighted_choice(piclist)

                        game.last_pic = {"tags": search_tags, "and_tags": and_tags, "not_tags": not_tags, "attempts": attempts}

                        if persistent.debug_pic_counter:
                            persistent.debug_pic_counter_dict[pic.path] += 1

                        return pic

        game.last_pic = {"tags": search_tags, "and_tags": and_tags, "not_tags": not_tags, "attempts": attempts}

        return None


