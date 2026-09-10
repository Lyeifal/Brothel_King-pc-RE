#### Girl Factory functions ####

init -3 python:
    def get_girl_path(file): # Returns girlpack name (the folder name), girlpack_path, file_name - Or None, None, None if the file is not a valid girl pack picture

        if is_imgfile(file) or file.endswith("_BK.ini"):
            for gdir in girl_directories:
                if file.startswith(gdir):

                    #!
                    # if gdir != "custom/girls/":
                    #     print(file + " was found!")

                    if gdir.endswith("/"):
                        gdir_len = len(gdir.split("/")) - 1 # The split actually includes an empty string at the end so len is 1 higher than expected
                    else:
                        gdir_len = len(gdir.split("/"))

                    file_parts = file.split("/")

                    if len(file_parts) > gdir_len + 1: # Skips files inside the root 'girls' directory to avoid problems
                        girlpack_name = ""
                        mix_name = ""
                        mix_list = []

                        for part in file_parts[gdir_len:-1]:
                            if part.startswith("_"): # Folders starting with an underscore will be completely ignored (such as a story pics-only directory)
                                return None, None, None

                            elif part.startswith("#"): # Folders starting with '#' will be identified as 'container folders' and a new mix will be created
                                if girlpack_name: # containers will be ignored if inside a girl pack (likely a mistake)
                                    return None, None, None
                                mix_name += part + " "
                                mix_list.append(mix_name)

                            else: # the first 'normal' folder will become the girlpack name
                                if not girlpack_name:
                                    girlpack_name = part
                                    girlpack_path = "/".join(file_parts[:file_parts.index(part)+1])

                        if not girlpack_name:
                            return None, None, None

                        # Creates mixes automatically

                        if mix_list:
                            for mix_name in mix_list:
                                if mix_name in persistent.girl_mix.keys():
                                    if girlpack_name not in persistent.girl_mix[mix_name]:
                                        persistent.girl_mix[mix_name].append(girlpack_name)
                                else:
                                    persistent.girl_mix[mix_name] = [girlpack_name]

                        return girlpack_name, girlpack_path, file_parts[-1]

        return None, None, None


    # def list_girl_packs(): # Returns a list of girl pack names. Used for CG gallery
    #
    #     pack_dir = {}
    #
    #     for file in renpy.list_files():
    #         girlpack_name, girlpack_path, file_name = get_girl_path(file)
    #         if girlpack_name: # Because get_girl_path can return None values
    #             if not pack_dir[girlpack_name]:
    #                 pack_dir[girlpack_name] = girlpack_path
    #
    #             elif pack_dir[girlpack_name] != girlpack_path: # Detects if a girlpack folder was found in two different locations for error handling.
    #                 raise AssertionError("Two girl packs with the name '%s' were found:\n%s\n%s\nRename one to avoid conflicts." % (girlpack_name, pack_dir[girlpack_name], girlpack_path))
    #                 renpy.say("", __("Exiting Ren'Py...{w=1}{nw}"))
    #                 renpy.quit()
    #
    #             if (girlpack_name, girlpack_path) not in pack_dir.items():
    #                 pack_dir[girlpack_name] = girlpack_path
    #
    #     return pack_dir

    def get_selected_girlpacks(mix_list): # Avoids duplicating girl packs if several mixes are selected with the exact same packs
        girlpacks = []

        for mix in mix_list:
            girlpacks += [gp for gp in persistent.girl_mix[mix] if gp not in girlpacks]

        return girlpacks

    def change_template(girl): # Used for debugging saved games that have different girl packs
        new_girl_pack = rand_choice(get_selected_girlpacks(game.mixes))
        girl.pack_name = new_girl_pack
        girl.path = new_girl_pack
        girl.load_ini()
        girl.generate_personality()
        girl.generate_background()
        girl.refresh_pictures()
        girl.create_char()

    def generate_girls():
        #<Chris12 PackState>
        global read_ini_log
        read_ini_log = ""

        # Use the new GirlFilesDict when generating new girls
        glist = list()

        ## CHECKING ACTIVE GAME MIXES ##

        available_girlpacks = get_selected_girlpacks(game.mixes)

        ## TAKING NAMES ##

        for girlpack_name in available_girlpacks:
            newGirl = Girl()
            newGirl.pack_name = girlpack_name
            newGirl.path = girlpack_name
            glist.append(newGirl)
        #</Chris12 PackState>

        ## SHOWING BUTTS ##

        for girl in glist:
            girl.load_ini()

        if not glist:
            renpy.say("", event_color["bad"] % __("The game couldn't find a girl pack in the current girl mix.") + __("\nHave you downloaded and installed girl packs?\nVisit [URL] to get your first girl packs."))
#            raise AssertionError("No girls found! Did you download a girl pack?")
            renpy.say("", __("Exiting Ren'Py...{w=1}{nw}"))
            renpy.quit()

        return glist

    def create_girl(pack_name, free=False, force_original=False, level=1, personality=None): # Create a single girl from pack_name (must be a valid pack name)
        girl = Girl()
        girl.pack_name = pack_name
        girl.path = pack_name
        girl.load_ini()
        girl.id = game.girl_id_generated
        game.girl_id_generated += 1
        girl.randomize(free=free, force_original=force_original, level=level, personality=personality)

        return girl

    def get_name(dir, full=False):

        """ Breaks down a dir name into a first name/last name """

        ## Only works with formats like "name", "name surname" or "name_surname". The "_" operator takes precedence over " ",
        ## which could be useful for composed first names

        dir_parts = dir.split("/")

        if not dir_parts[-1]: # split will sometimes return an empty string at the end
            dir_parts = dir_parts[:-1]

        dir = dir_parts[-1]

        if dir.count("_") == 1:
            char = dir.find("_")

            first_name = dir[:char]
            last_name = dir[char+1:]

        elif dir.count(" ") >= 1:
            char = dir.find(" ")

            first_name = dir[:char]
            last_name = dir[char+1:]

        else:
            first_name = dir
            last_name = ""

        if full:
            return first_name + " " + last_name

        else:
            return first_name, last_name

    def get_girl(free=False, p_traits=None, n_trait=None, perks=None, level_range=None, prefer_original = None): # This will return a single new girl, if possible using different templates and checking for duplicates
        return get_girls(1, free, p_traits, n_trait, perks, level_range, prefer_original)[0]

    def get_girls(nb, free=False, p_traits=None, n_trait=None, perks=None, level_range=None, prefer_original = None): # This will return a list of new girls, if possible using different templates and checking for duplicates

        # If level_range is provided as a tuple of integers (min, max), girls will generate at a random level in range
        # Never set level range below 1 or above 25 to avoid problems

        # prefer_original prioritizes the creation of original girls. They will take the top spots in glist. The game will fall back to non-original if necessary
        if prefer_original is None:
            prefer_original=prefer_original_girls

        t1 = time.perf_counter()

        if p_traits == None: p_traits = []
        if perks == None: perks = []

        template_girls = [g for g in generate_girls() if can_generate(g, free)] # Must be separate from available_templates to avoid creating new girl objects with every loop

        t2 = time.perf_counter()

        available_templates = []
        glist = []
        final_list = []

        while len(glist) < nb:
            if available_templates == []:
                available_templates = list(template_girls) # list() is necessary to make a true copy of template_girls
                renpy.random.shuffle(available_templates) # places girl templates in random order

            # First looks for girls that haven't been generated at all

            for girl in available_templates:
                if girl not in glist and girl.count_occurences("all") == 0:
                    glist.append(girl)
                    available_templates.remove(girl) # removing within the for loop is okay because of 'break'
                    if girl.is_unique(): # Removes unique girls from the template pool if they are unique
                        template_girls.remove(girl)
                    break
            else: # 'for' loop failed
                # Next looks for girls that aren't owned by player and have less than 3 occurences elsewhere

                available_templates = [g for g in available_templates if not g.is_unique()] # This clears unique girls from the list (shouldn't be needed)

                if not available_templates:
                    raise AssertionError("Not enough girl templates available - Check your girlpack configuration (all set to 'unique'?)")

                for girl in available_templates:
                    if girl not in glist and girl.count_occurences("player") == 0 and girl.count_occurences("all") <= 3:
                        glist.append(girl)
                        available_templates.remove(girl) # removing within the for loop is okay because of 'break'
                        break

                # Finally, looks for girls with the least occurrences anywhere

                else:
                    if not available_templates:
                        raise AssertionError("Not enough girl templates available - Check your girlpack configuration")

                    found = False
                    i = 1
                    while not found:
                        i += 1

                        if i > 250:
                            raise AssertionError("Error chasing duplicates - Possible infinite loop detected")

                        for girl in available_templates:
                            if girl.count_occurences("all") < i:
                                glist.append(girl)
                                available_templates.remove(girl) # removing within the for loop is okay because of 'break'
                                found = True
                                break

        t3 = time.perf_counter()

        for template in glist:
            girl = copy.deepcopy(template)
            girl.id = game.girl_id_generated
            game.girl_id_generated += 1

            if level_range:
                lvl = renpy.random.randint(level_range[0], level_range[1])

            else: # Will pick a randomized level based on chapter
                lvl = randomize_girl_level()

            # <Chris12 - prefer_original>
            girl.randomize(free=free, p_traits=p_traits, n_trait=n_trait, perks=perks, level=lvl, force_original=(prefer_original and girl.count_occurences("all", original=True, add_list=final_list) == 0), temp_list=final_list) # final_list is checked to avoid multiple original generation
            # </Chris12 - prefer_original>

            final_list.append(girl)

            if girl.init_dict["background story/init_function"]:
                try:
                    globals()[girl.init_dict["background story/init_function"]](girl)
                except:
                    raise AssertionError("Function " + girl.init_dict["background story/init_function"] + " in " + girl.path + "/_BK.ini doesn't exist or failed.")

            # 通知 Mod: 女孩已完整生成（randomize 与 init_function 之后） | Notify mods: girl fully generated (after randomize and init_function)
            mod_api_v2.execute_hook(mod_api_v2.HOOK_GIRL_GENERATED, girl=girl)

        t4 = time.perf_counter()

        try:
            game.func_time_log += "\ntotal time: %s" % (t4 - t1)
        except:
            pass

        return final_list



### RANDOM AND NUMBERS FUNCTIONS ###

    def read_init_file_generate_as(file):
        if file:
            v = read_init_file_field(file, "background story", "generate_as", _default="all", skip_checks=True)
            return v
        return "all"

    def read_init_file_field(file, _key, _value, _default="default", skip_checks=False):
        if file:
            field = read_init_file(file, search_for = {_key : [_value]}, skip_checks=skip_checks)[_key + "/" + _value]
            if field:
                return field
        return _default

    ## To add a new _BK.ini value:
    #  1. Edit _BK.ini template and define variable type and possible values
    #  2. Update the search_for dictionary below
    #  3. Add sanity checks as necessary
    #  4. Define cloning behavior
    #  5. Update relevant parts of girl generation

    def read_init_file(file, search_for = None, skip_checks=False): ## This compiles a dictionary of values contained in a _BK.ini file. The dictionary acts as a buffer to account for the possibility of user mistakes.

        global read_ini_log

        input_dict = defaultdict(list)

        ## Read file

        parser = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))

        try:
            parser.read(config.gamedir + "/" + file)
        except UnicodeDecodeError:
            raise AssertionError("Error reading file: " + config.gamedir + "/" + file + ". Please make sure that special characters in the _BK.ini file are encoded in Unicode.")
        except:
            raise AssertionError("Error reading file: " + config.gamedir + "/" + file + ". Please verify _BK.ini file integrity.")

        ## list sections and values to search for in the .ini file (update this when the .ini format is updated)

        if not search_for:
            search_for = {
                          "identity" : ["first_name", "last_name", "inverted_name", "creator", "version", "description", "unique", "keep_first_name", "keep_last_name", "keep_inverted", "game_character"],
                          "base skills" : gstats_main + ["keep_skills"],
                          "base positive traits" : ["always", "often", "rarely", "never", "keep_traits"],
                          "base negative traits" : ["always", "often", "rarely", "never", "keep_traits"],
                          "base personality" : ["always", "often", "rarely", "never", "keep_personality"],
                          "custom personality" : ["custom_personality", "name", "personality_name", "attributes", "personality_dialogue_only", "dialogue_personality_weight", "dialogue_attribute_weight", "description", "custom_dialogue_label"],
                          "tastes" : ["favorite_color", "favorite_food", "favorite_drink", "disliked_color", "disliked_food", "disliked_drink", "hobbies"],
                          "sexual preferences" : ["favorite_acts", "disliked_acts", "favorite_fixations", "always_fixations", "always_negative_fixations", "disliked_fixations", "never_fixations", "never_negative_fixations", "sexual_experience", "farm_weakness", "keep_sex"],
                          "background story" : ["generate_as", "generate_in", "move_after_meeting", "origin", "origin_description", "always_slave_story", "often_slave_story", "rarely_slave_story", "never_slave_story", "init_function", "city_label", "story_label", "night_label", "interact_prompt", "keep_generate_as", "keep_init", "keep_background", "keep_interactions"],
                          "cloning options" : ["unique", "keep_first_name", "keep_last_name", "keep_inverted", "keep_skills", "keep_traits", "keep_personality", "keep_sex", "keep_generate_as", "keep_init", "keep_background", "keep_interactions"],
                          "custom tags" : [],
                          "custom dialogue" : []
                          }

        for k, v in search_for.items():
            for thing in v:
                try:
                    input_dict[k + "/" + thing] = ast.literal_eval(parser.get(k, thing.lower()))
                except:
                    read_ini_log += "\nAn error has been found parsing " + k + "/" + thing + " in " + file + ", or it has been intentionally left out."

        # Parse dynamic sections where any key is valid
        for section in ("custom tags", "custom dialogue"):
            if parser.has_section(section):
                for option in parser.options(section):
                    try:
                        input_dict[section + "/" + option] = ast.literal_eval(parser.get(section, option))
                    except:
                        read_ini_log += "\nAn error has been found parsing " + section + "/" + option + " in " + file + ", or it has been intentionally left out."

        if skip_checks:
            return input_dict

        ## Sanity checks

        # Game character

        if input_dict["identity/game_character"]:
            try:
                gc = globals()[input_dict["identity/game_character"]] # checks that a variable with the given string name exists in the global store
            except:
                gc = None

            input_dict["identity/game_character"] = gc

            if not isinstance(gc, ADVCharacter):
                read_ini_log += "\n%s is not a declared game character." % input_dict["identity/game_character"]

        # Skills

        for key in gstats_main: # Makes sure all values are between 0 and 5
            try:
                input_dict["base skills/" + key] = max(min(input_dict["base skills/" + key], 5), 0)
            except:
                input_dict["base skills/" + key] = 0

        # Traits and Personalities

        for key in ["always", "often", "rarely", "never"]:
            input_dict["base positive traits/" + key] = [t.capitalize() for t in input_dict["base positive traits/" + key]]
            input_dict["base negative traits/" + key] = [t.capitalize() for t in input_dict["base negative traits/" + key]]

            for trait in input_dict["base positive traits/" + key]:
                if trait not in trait_dict.keys():
                    input_dict["base positive traits/" + key].remove(trait)

                    if trait in renamed_traits.keys(): # Updates trait name for backwards compatibility
                        input_dict["base positive traits/" + key].append(renamed_traits[trait])
                    else:
                        renpy.say(__("{color=[c_red]}{b}Error parsing %s{/b}{/color}") % file, __("{color=[c_red]}%s{/color} is not a valid trait.\nCheck the correct use of brackets and quotes.") % trait)

            for trait in input_dict["base negative traits/" + key]:
                if trait not in trait_dict.keys():
                    input_dict["base negative traits/" + key].remove(trait)

                    if trait in renamed_traits.keys(): # Updates trait name for backwards compatibility
                        input_dict["base negative traits/" + key].append(renamed_traits[trait])
                    else:
                        renpy.say(__("{color=[c_red]}{b}Error parsing %s{/b}{/color}") % file, __("{color=[c_red]}%s{/color} is not a valid trait.\nCheck the correct use of brackets and quotes.") % trait)

            input_dict["base personality/" + key] = [p.lower() for p in input_dict["base personality/" + key]]

            for pers in input_dict["base personality/" + key]:
                if pers not in gpersonalities.keys():
                    renpy.say(__("{color=[c_red]}{b}Error parsing %s{/b}{/color}") % file, __("{color=[c_red]}%s{/color} is not a valid personality.\nCheck the correct use of brackets and quotes.") % pers)

        # Custom personality (for backwards compatibility)

        if input_dict["custom personality/name"] and not input_dict["custom personality/personality_name"]:
            input_dict["custom personality/personality_name"] = input_dict["custom personality/name"]

        # Tastes

        for tas in search_for["tastes"]:
            if tas == "hobbies":
                if input_dict["tastes/" + tas]:
                    input_dict["tastes/" + tas] = make_list(input_dict["tastes/" + tas]) # Makes sure entry is a list
                    if len(input_dict["tastes/" + tas]) > 2: # Limits number of hobbies to two
                        input_dict["tastes/" + tas] = input_dict["tastes/" + tas][:2]

            else:
                if input_dict["tastes/" + tas]:
                    if is_string(input_dict["tastes/" + tas]):
                        input_dict["tastes/" + tas] = input_dict["tastes/" + tas].lower()
                    else:
                        input_dict["tastes/" + tas] = None

        # Preferences

        for key in ["favorite_acts", "disliked_acts"]:
            input_dict["sexual preferences/" + key] = [p.lower() for p in input_dict["sexual preferences/" + key]]

            for act in input_dict["sexual preferences/" + key]:
                if act not in extended_sex_acts:
                    renpy.say(__("{color=[c_red]}{b}Error parsing %s{/b}{/color}") % file, __("{color=[c_red]}%s{/color} is not a valid sex act.\nCheck the correct use of brackets and quotes.") % act)

        # Fixations

        for key in ["always_fixations", "always_negative_fixations", "favorite_fixations", "disliked_fixations", "never_fixations", "never_negative_fixations"]:
            input_dict["sexual preferences/" + key] = [p.lower() for p in input_dict["sexual preferences/" + key]]

            for fix in input_dict["sexual preferences/" + key]:
                if fix not in fix_dict.keys():
                    renpy.say(__("{color=[c_red]}{b}Error parsing %s{/b}{/color}") % file, __("{color=[c_red]}%s{/color} is not a valid fixation.\nCheck the correct use of brackets and quotes.") % fix)

        # Prior sexual experience

        if input_dict["sexual preferences/sexual_experience"]:
            input_dict["sexual preferences/sexual_experience"] = input_dict["sexual preferences/sexual_experience"].lower()

            if input_dict["sexual preferences/sexual_experience"].lower() not in list(sexual_training_value.keys()) + ["random"]:
                renpy.say(__("{color=[c_red]}{b}Error parsing %s{/b}{/color}") % file, __("{color=[c_red]}%s{/color} is not a valid setting.\nAccepted values are \"very experienced\", \"experienced\",  \"average\", \"inexperienced\", \"very inexperienced\", \"random\".") % input_dict["sexual preferences/sexual_experience"])

        # Farm

        if input_dict["sexual preferences/farm_weakness"]:
            input_dict["sexual preferences/farm_weakness"] = input_dict["sexual preferences/farm_weakness"].lower()

            if input_dict["sexual preferences/farm_weakness"] not in all_minion_types + ["random"]:
                renpy.say(__("{color=[c_red]}{b}Error parsing %s{/b}{/color}") % file, __("{color=[c_red]}%s{/color} is not a valid farm weakness.\nAccepted values are \"stallion\", \"beast\", \"monster\", \"machine\", \"random\".") % input_dict["sexual preferences/farm_weakness"])

        # Back story

        if input_dict["background story/generate_as"]:
            input_dict["background story/generate_as"] = input_dict["background story/generate_as"].lower()
            if input_dict["background story/generate_as"] not in ("slave", "free", "story", "all"):
                raise AssertionError("_BK.ini error with girlpack: %s. 'background story/generate_as' should be set to 'all', 'slave', 'free' or 'story'." % file)
        else:
            input_dict["background story/generate_as"] = "all"

        if input_dict["background story/generate_in"]:
            if input_dict["background story/generate_in"] != "all":

                if is_string(input_dict["background story/generate_in"]): # For single entries
                    input_dict["background story/generate_in"] = [input_dict["background story/generate_in"]] # Creates a list


                # Converts every entry to lower case
                try:
                    input_dict["background story/generate_in"] = [loc.lower() for loc in input_dict["background story/generate_in"]]
                except:
                    raise AssertionError("_BK.ini error with girlpack: %s. 'background story/generate_in' should be set to 'all' OR a list of valid district or location names, spelled exactly as in-game. Don't forget the article for districts (e.g. 'The Slums')." % file)

                # Replace old 'library' location with 'magic university
                if "library" in input_dict["background story/generate_in"]:
                    input_dict["background story/generate_in"].remove("library")
                    input_dict["background story/generate_in"].append("magic university")

                # Confirms location exists
                for loc in input_dict["background story/generate_in"]:
                    if loc not in ["all"] + [d.name.lower() for d in all_districts] + [l.name.lower() for l in all_locations]:
                        raise AssertionError("_BK.ini error with girlpack: %s. Wrong location: %s. 'background story/generate_in' should be set to 'all' OR a list of valid district or location names, spelled exactly as in-game. Don't forget the article for districts (e.g. 'The Slums')." % (file, loc))

        else:
            input_dict["background story/generate_in"] = "all"

        if input_dict["background story/move_after_meeting"] != False:
            input_dict["background story/move_after_meeting"] = True

        return input_dict

    def register_custom_tags_for_pack(girlpack_name, custom_tags):
        """
        Register custom tags from a girl pack's _BK.ini into the global tag system
        and re-tag all pictures for that pack.
        """
        if not custom_tags:
            return

        for tag_name, synonyms in custom_tags.items():
            tag_registry.register_tag(tag_name, synonyms, tag_list=synonyms)

        # Update static sorted lists to include new tags
        global sorted_tag_dict_keys, sorted_tags_with_separator
        sorted_tag_dict_keys = sorted(tag_dict.keys(), key=lambda x: len(x), reverse=True)
        sorted_tags_with_separator = [tag for tag in sorted_tag_dict_keys if " " in tag]

        # Re-tag pictures for this pack so new tags are recognized
        for pic in GirlFilesDict.get_pics(girlpack_name):
            pic.make_tags_from_filename()

    def register_custom_dialogue_for_pack(girlpack_name, custom_dialogue):
        """
        Register custom dialogue lines from a girl pack's _BK.ini into the global dialogue system.
        Duplicate lines for the same pack/topic are skipped.
        """
        if not custom_dialogue:
            return

        for topic, lines in custom_dialogue.items():
            existing_lines = [d.line for d in dialogue_dict[topic].get(girlpack_name, [])]
            for line in lines:
                if line not in existing_lines:
                    add_dialogue(topic, girlpack_name, line)

    def clone_init_dict(input_dict):

        global read_ini_log

        ## Support for new _BK.ini format (cloning options no longer a sub-section)
        for section, klist in [("identity", ["unique", "keep_first_name", "keep_last_name", "keep_inverted"]), ("base skills", ["keep_skills"]), ("base positive traits", ["keep_traits"]), ("base negative traits", ["keep_traits"]), ("base personality", ["keep_personality"]), ("sexual preferences", ["keep_sex"]), ("background story", ["keep_generate_as", "keep_init", "keep_background", "keep_interactions"])]:
            for k in klist:
                if input_dict[section + "/" + k]:
                    if k == "keep_traits":
                        if input_dict["base positive traits/keep_traits"] != input_dict["base negative traits/keep_traits"]:
                            read_ini_log += "\nConflict with {b}%s{/b} key in positive and negative traits: overwritten by True setting." % k
                            input_dict["base positive traits/keep_traits"] = input_dict["base negative traits/keep_traits"] = True
                    if input_dict["cloning options/" + k]:
                        read_ini_log += "\nConflict with {b}%s{/b} key: %s overwritten by %s setting." % (k, "cloning options/" + k, section + "/" + k)
                    input_dict["cloning options/" + k] = input_dict[section + "/" + k]

        ## Cloning default settings

        if not input_dict["cloning options/keep_first_name"]:
            if not persistent.keep_firstname:
                input_dict["identity/first_name"] = "?rand"
        if not input_dict["cloning options/keep_last_name"]:
            if not persistent.keep_lastname:
                input_dict["identity/last_name"] = "?rand"
        if not input_dict["cloning options/keep_inverted"]:
            input_dict["identity/inverted_name"] = False
        if not input_dict["cloning options/keep_skills"]:
            for skill in gstats_main:
                input_dict["base skills/" + skill] = 0
        if not input_dict["cloning options/keep_traits"]:
            for key in ["always", "often", "rarely", "never"]:
                input_dict["base positive traits/" + key] = []
                input_dict["base negative traits/" + key] = []
        if not input_dict["cloning options/keep_personality"]:
            for key in ["always", "often", "rarely", "never"]:
                input_dict["base personality/" + key] = []
            input_dict["custom personality/custom_personality"] = False
            for key in ["favorite_color", "favorite_food", "favorite_drink", "disliked_color", "disliked_food", "disliked_drink", "hobbies"]:
                input_dict["base personality/" + key] = None
        if not input_dict["cloning options/keep_sex"]:
            for key in ["favorite_acts", "disliked_acts", "favorite_fixations", "disliked_fixations", "always_fixations", "always_negative_fixations", "never_fixations", "never_negative_fixations"]:
                input_dict["sexual preferences/" + key] = []
            input_dict["sexual preferences/sexual_experience"] = "random"
            input_dict["sexual preferences/farm_weakness"] = "random"
        if not input_dict["cloning options/keep_generate_as"]:
            input_dict["background story/generate_as"] = "all"
            input_dict["background story/generate_in"] = "all"
        if not input_dict["cloning options/keep_init"]:
            input_dict["background story/init_function"] = None
        if not input_dict["cloning options/keep_background"]:
            input_dict["background story/origin"] = "random"
            input_dict["background story/origin_description"] = None
            for key in ["always_slave_story", "often_slave_story", "rarely_slave_story", "never_slave_story"]:
                input_dict["background story/" + key] = []
            input_dict["background story/story_label"] = None
        if not input_dict["cloning options/keep_interactions"]:
            input_dict["background story/city_label"] = None
            input_dict["background story/night_label"] = None
            input_dict["background story/interact_prompt"] = None

        return input_dict


    # Checks if a girl can be generated as a free girl or slave with the 'get_girls' function
    def can_generate(girl, free=False, add_list=None): # add_list is an additional list of girls that will be checked as part of the 'count_occurences' function

        # Slaves cannot generate in the city
        if free and girl.init_dict["background story/generate_as"] == "slave":
            return False

        # Free girls cannot generate in the market
        elif not free and girl.init_dict["background story/generate_as"] == "free":
            return False

        # Story girls cannot generate anywhere (use 'create_girl' to add a story girl to the game)
        elif girl.init_dict["background story/generate_as"] == "story":
            return False

        # Unique girls may only generate if none other already exists
        if girl.is_unique(): # No other girl can generate after the first one
            if girl.count_occurences("all", add_list=add_list) > 0: # count_occurences does not include self
                return False

        return True


    def can_spawn(girl, location): # Location is an object

        if not isinstance(location, Location):
            raise AssertionError(str(location) + " is not a valid Location object.")

        if girl.init_dict["background story/generate_in"] and girl.init_dict["background story/generate_in"] != "all":
            # girl.init_dict["background story/generate_in"] is either "all" or a list of district or location names in lower case

            if location.name.lower() not in girl.init_dict["background story/generate_in"] and location.get_district().name.lower() not in girl.init_dict["background story/generate_in"]:
                return False

        return True



    # #  <DougTheC> Take advantage of "and" being short-circuit operator to speed process
    # #  Also avoid unique girls being improperly included by irrelevant "cloning options/keep_generate_as" value
    # def can_generate(girl, free=False, context="game", location=None): # Context can be 'game' or 'mix'. Location is an object
    #     if context == "game":

    #         # Unique girls may only generate if none other exists
    #         if girl.init_dict["cloning options/unique"]: # No other girl can generate after the first one
    #             #  Unique girl need not check for "cloning options/keep_generate_as", as there are no clones
    #             if free and girl.init_dict["background story/generate_as"] == "slave":
    #                 return False
    #             elif not free and girl.init_dict["background story/generate_as"] == "free":
    #                 return False
    #             elif location:
    #                 if girl.init_dict["background story/generate_in"] and girl.init_dict["background story/generate_in"] != "all":
    #                     for place in girl.init_dict["background story/generate_in"]:
    #                         if location.get_district().name.lower() not in girl.init_dict["background story/generate_in"] and location.name.lower() not in girl.init_dict["background story/generate_in"]:
    #                             return False
    #             #  Uses count_occurences last, only when absolutely necessary; significant time consumption
    #             if girl.count_occurences("all") > 1:
    #                 return False

    #         #  Check other girls
    #         else: # elif girl.init_dict["cloning options/keep_generate_as"]
    #             if free and girl.init_dict["background story/generate_as"] == "slave":
    #                 return False
    #             elif not free and girl.init_dict["background story/generate_as"] == "free":
    #                 return False
    #             elif location:
    #                 if girl.init_dict["background story/generate_in"] and girl.init_dict["background story/generate_in"] != "all":
    #                     for place in girl.init_dict["background story/generate_in"]:
    #                         if location.get_district().name.lower() not in girl.init_dict["background story/generate_in"] and location.name.lower() not in girl.init_dict["background story/generate_in"]:
    #                             return False

    #     elif context == "mix":
    #         if girl.init_dict["background story/generate_as"] == "story": # story-only girls are not included in the mix UI
    #             return False

    #     return True
    # #  </DougTheC>


    def get_girlpack_rating(girl=None, path=None, forced=False):

        if path:
            girl = Girl()
            girl.path = path

        if rating_dict[girl.path] and not forced:
            d = rating_dict[girl.path]
        else:
#            renpy.say("", "Evaluate " + path)
            d = girl.evaluate_girlpack()
            rating_dict[girl.path] = d

        score = d["main cover score"] * 5 + d["optional cover score"] * 2

        if score >= 6:
            rating = "A"
            col = "special"
        elif score >= 5:
            rating = "B"
            col = "good"
        elif score >= 4:
            rating = "C"
            col = "a little good"
        elif score >= 3:
            rating = "D"
            col = "average"
        elif score >= 2:
            rating = "E"
            col = "a little bad"
        else:
            rating = "F"
            col = "bad"

        if d["main diversity average"] > 5:
            rating += "+"
        elif d["main diversity average"] < 3:
            rating += "-"

        ttip = "Girlpack rating: %s, " % rating
        #<Chris12 PackState>
        #ttip += "\nPictures: " + str(len(girl.pics))
        ttip += "Pictures: " + str(len(GirlFilesDict.get_pics(girl.path)))
        #</Chris12 PackState>
        ttip += "\nMain tags score: " + str(round_int(d["main cover score"]*100)) + "% (" + str(round(d["main diversity average"], 1)) + " picture/existing tag)"
        ttip += "\nOptional tags score: " + str(round_int(d["optional cover score"]*100)) + "% (" + str(round(d["optional diversity average"], 1)) + " picture/existing tag)"

        return event_color[col] % rating, ttip


    def get_plus_rating(chg, type="stat"):

        if type == "stat":
            if chg > 3:
                r = "+++"
            elif chg > 1:
                r = "++"
            elif chg > 0.2:
                r = "+"
            elif chg >= -0.2:
                r = "="
            elif chg >= -1:
                r = "-"
            elif chg >= -3:
                r = "--"
            else:
                r = "---"

        elif type == "pref":
            if chg > 250:
                r = "+++"
            elif chg > 100:
                r = "++"
            elif chg > 5:
                r = "+"
            elif chg > -5:
                r = "="
            elif chg >= -100:
                r = "-"
            elif chg >= -250:
                r = "--"
            else:
                r = "---"

        return "{color=" + color_dict[r] + "}" + r + "{/color}"

    def randomize_girl_level(): # Picks a level for a randomly generated girl, based on Chapter

        weighted_list = []
        rank = 0

        # Chance to generate at lower rank is halved every step

        for i in range(game.max_girl_rank): # Chance gets higher with every rank
            rank += 1
            weighted_list.append([rank, 1.25**rank]) #? Test how it behaves

        girl_rank = weighted_choice(weighted_list)

        if girl_rank < 2:
            return renpy.random.randint(1, int(game.max_girl_level))
        else:
            return renpy.random.randint((girl_rank-1) * 5, int(game.max_girl_level))

init -3 python:

    def generate_name(type):
        if type == "stallion":
            return rand_choice(minion_name_dict["consonants"]).capitalize() + rand_choice(minion_name_dict["vowels"]) + rand_choice(minion_name_dict["consonants"])
        elif type == "beast":
#            return rand_choice(minion_name_dict["consonants"]) + rand_choice(minion_name_dict["vowels"]) + rand_choice(minion_name_dict["consonants"]) + rand_choice(minion_name_dict["vowels"])
            cons = rand_choice(minion_name_dict["consonants"])
            return cons.capitalize() + rand_choice(minion_name_dict["vowels"]) + cons + rand_choice(minion_name_dict["vowels"])
        elif type == "monster":
            return rand_choice(minion_name_dict["monster1"]).capitalize() + rand_choice(minion_name_dict["vowels"]) + rand_choice(minion_name_dict["monster2"])
        elif type == "machine":
            return rand_choice(minion_name_dict["consonants"] + minion_name_dict["vowels"]).capitalize() + rand_choice(minion_name_dict["consonants"] + minion_name_dict["vowels"]).capitalize() + "-" + str(99 + dice(900))
        elif type == "girl":
            first_name = ""

            syllabs = dice(3)

            if syllabs == 1:
                first_name += rand_choice(girl_name_dict["syllabs"]) + rand_choice(girl_name_dict["enders"])

            elif syllabs == 2:
                first_name += rand_choice(girl_name_dict["syllabs"]) + rand_choice(girl_name_dict["fillers"]) + rand_choice(girl_name_dict["syllabs"])

            elif syllabs == 3:
                first_name += rand_choice(girl_name_dict["syllabs"]) + rand_choice(girl_name_dict["syllabs"]) + rand_choice(girl_name_dict["enders"])

            syllabs = dice(4)

            last_name = ""

            if syllabs == 1:
                last_name = rand_choice(girl_name_dict["last_syllabs"]) + rand_choice(girl_name_dict["enders"])
            else:
                for i in range(syllabs):
                    last_name += rand_choice(girl_name_dict["last_syllabs"])

            return first_name.capitalize(), last_name.capitalize()

