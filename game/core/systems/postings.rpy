#### BK QUESTS AND CLASSES ####
## Labels are used instead of Functions to make sure we are using global variables

# EN: Resolvers used by Quest.from_dict() when loading JSON quest/class templates.
# ZH: 加载 JSON 任务/课程模板时，Quest.from_dict() 使用的解析函数。
#     放在 init 1 python 中，确保 s_sigh 等音频变量和 all_jobs 已初始化。
init 1 python:
    _sound_map = {"sigh": s_sigh, "aaha": s_aaha, "mmmh": s_mmmh, "aah": s_aah, "scream": s_scream}

    def _resolve_sound(name):
        return _sound_map.get(name, s_sigh)

    def _resolve_jp_type(val):
        if val == "all_jobs":
            return all_jobs
        return val

label init_postings():
    python:
        ## EN: Load quest and class templates from JSON (BK Evolution), fallback to hardcoded.
        ## ZH: 从 JSON 加载任务和课程模板（BK Evolution），否则使用硬编码。

        _qt_json = DataLoader.load_quest_templates()
        if _qt_json:
            quest_templates = [Quest.from_dict(q, sound_resolver=_resolve_sound, jp_type_resolver=_resolve_jp_type) for q in _qt_json.get("quest_templates", [])]
            class_templates = [Quest.from_dict(q, sound_resolver=_resolve_sound, jp_type_resolver=_resolve_jp_type) for q in _qt_json.get("class_templates", [])]
        else:
            # Fallback: hardcoded quest and class templates
            quest_templates = [
                            Quest("quest", name = __('Model needed'), main_stat = 'Beauty', second_stat = 'Libido', other_stats = ("Body", "Charm", "Refinement"), tags = 'model', description = __("I'm an artist, an artist I tell thee! I need a muse. Clothing unnecessary."), sound = s_sigh),
                            Quest("quest", name = __('Private dance'), main_stat = 'Body', second_stat = 'Constitution', other_stats = ("Body", "Charm", "Refinement"), tags = 'dance', description = __("Looking for a private, intimate dance...."), sound = s_sigh),
                            Quest("quest", name = __('Entertain my guests'), main_stat = 'Charm', second_stat = 'Obedience', other_stats = ("Beauty", "Body", "Refinement"), tags = 'waitress', description = __("My guests are arriving soon, and nothing is ready! This is a disaster! I need your help!"), sound = s_sigh),
                            Quest("quest", name = __('Escort needed'), main_stat = 'Refinement', second_stat = 'Sensitivity', other_stats = ("Beauty", "Body", "Charm"), tags = 'geisha', description = __("I have an important guild meeting, and I need to show them I'm not just anyone. Looking for an elite companion to impress those snobs."), sound = s_sigh),
                            Quest("quest", name = __('Make me feel young again'), main_stat = 'Libido', second_stat = 'Sensitivity', other_stats = ("Beauty", "Body", "Refinement"), tags = 'sex', description = __("It's been many a moon since lil' willy's gone to sleep. I need a girl to help me remember what it was like in the old days..."), sound = s_aaha),
                            Quest("quest", name = __('Setting a record'), main_stat = 'Constitution', second_stat = 'Libido', other_stats = ("Body", "Charm", "Refinement"), tags = 'anal', description = __("I aim to break the record set by Long Dick Silver, and this will take long hours of practice... Help me get harder and stronger so that I can succeed!"), sound = s_aaha),
                            Quest("quest", name = __('Girlfriend needed'), main_stat = 'Sensitivity', second_stat = 'Obedience', other_stats = ("Beauty", "Charm", "Refinement"), tags = 'service', description = __("I feel lonely... Will you help me forget my troubles?"), sound = s_aaha),
                            Quest("quest", name = __('Hiring help'), main_stat = 'Obedience', second_stat = 'Constitution', other_stats = ("Beauty", "Body", "Charm"), tags = 'maid', description = __("I need an extra maid to help out in the mansion. There is a very specific uniform..."), sound = s_aaha),
                            Quest("quest", name = __('Please teach my son'), main_stat = 'Service', second_stat = 'Sex', other_stats = ("Libido", "Constitution", "Obedience", "Sensitivity"), tags = 'service', description = __("My son is already 21, and not yet married. He's a big oaf when it comes to women... Can you help him come out of his shell?"), sound = s_mmmh),
                            Quest("quest", name = __('Bored in Zan'), main_stat = 'Sex', second_stat = 'Anal', other_stats = ("Libido", "Constitution", "Obedience", "Sensitivity"), tags = 'sex', description = __("I'm stranded here, drinking ale all day at the local inn. I'm bored out of my mind. Please send me some 'entertainment'."), sound = s_mmmh),
                            Quest("quest", name = __('Back door man'), main_stat = 'Anal', second_stat = 'Fetish', other_stats = ("Libido", "Constitution", "Obedience", "Sensitivity"), tags = 'anal', description = __("The men don't know, but the little girls understand..."), sound = s_mmmh),
                            Quest("quest", name = __('Night at the dungeon'), main_stat = 'Fetish', second_stat = 'Service', other_stats = ("Libido", "Constitution", "Obedience", "Sensitivity"), tags = 'fetish', description = __("Looking for partners to help us test our new contraption. C'mon! It will be fun!"), sound = s_mmmh),
                            Quest("quest", name = __('Private party'), main_stat = 'Constitution', second_stat = 'Libido', other_stats = ("Body", "Charm", "Refinement"), tags = 'group', description = __("Hosting a large delegation at my house. We need girls to entertain our guests in every way possible..."), sound = s_aah),
                            Quest("quest", name = __('Ladies night'), main_stat = 'Service', second_stat = 'Sex', other_stats = ("Libido", "Constitution", "Obedience", "Sensitivity"), tags = 'group', description = __("We are holding our traditional 'ladies night' at our local guild hall. Looking for a girl to play with a friend in front of the audience..."), sound = s_aah),
                            ]

            class_templates = [
                                Quest("class", name = __('Modeling'), main_stat = 'Beauty', second_stat = 'Libido', other_stats = ("Body", "Charm", "Refinement"), jp_type = all_jobs, tags = 'model', description = __("Learn the secrets to looking fabulous and have perfect hair at all times! Who wants to look natural anyway?"), sound = s_sigh),
                                
                                Quest("class", name = __('Dancing'), main_stat = 'Body', second_stat = 'Constitution', other_stats = ("Beauty", "Charm", "Refinement"), jp_type = ["dancer"], tags = 'dance', description = __("Zomba! Bodyfighting! Aqua reggeaton!\nHurry before we make up even more silly names!"), sound = s_sigh),
                                
                                Quest("class", name = __('Waitress'), main_stat = 'Charm', second_stat = 'Obedience', other_stats = ("Beauty", "Body", "Refinement"), jp_type = ["waitress"], tags = 'waitress', description = __("Learn the basics of working tables... You'll never spill a glass on a customer's crotch again, unless you want to!"), sound = s_sigh),
                                
                                Quest("class", name = __('Geisha'), main_stat = 'Refinement', second_stat = 'Sensitivity', other_stats = ("Beauty", "Body", "Charm"), jp_type = ["geisha"], tags = 'geisha', description = __("Master all Zanic traditional arts, including the exact science of tea ceremony trigonometry. Don't look like an ass because your tea cup is off 5 degrees to the left!"), sound = s_sigh),
                                
                                Quest("class", name = __('Massage'), main_stat = 'Libido', second_stat = 'Sensitivity', other_stats = ("Beauty", "Body", "Refinement"), jp_type = ["masseuse"], tags = 'masseuse', description = __("Spend a relaxing few days at the spa with us. It will be awesome! As for the teaching... Wait, what teaching?"), sound = s_aaha),
                                
                                Quest("class", name = __('Swimming'), main_stat = 'Constitution', second_stat = 'Libido', other_stats = ("Body", "Charm", "Refinement"), jp_type = ["masseuse"], tags = 'swim', description = __("The sun shining on exposed bodies... Water running along voluptuous curves... Tanning oil on glistening skin... And swimming, of course. Erm."), sound = s_aaha),
                                
                                Quest("class", name = __('Singing'), main_stat = 'Sensitivity', second_stat = 'Obedience', other_stats = ("Beauty", "Charm", "Refinement"), jp_type = ["dancer", "geisha"], tags = 'sing', description = __("'Sing properly dammit, or I'll rip off your head and shove manure down your neck!'. How bad can a singing class be? Oh, you'll see..."), sound = s_aaha),
                                
                                Quest("class", name = __('Maid'), main_stat = 'Obedience', second_stat = 'Constitution', other_stats = ("Beauty", "Body", "Charm"), jp_type = ["waitress"], tags = 'maid', description = __("'If you want to clean up properly, you have to bend forward a lot more! More... More... Hmm, that's better.'"), sound = s_aaha),
                                
                                Quest("class", name = __('XXX{#1}'), main_stat = 'Service', second_stat = 'Sex', other_stats = ("Libido", "Constitution", "Obedience", "Sensitivity"), jp_type = ["service", "sex"], tags = 'XXX', description = __("Learn to pleasure a man... Or a woman, if you're so inclined. Why not learn both?{#1}"), sound = s_aah),
                                
                                Quest("class", name = __('XXX'), main_stat = 'Sex', second_stat = 'Anal', other_stats = ("Libido", "Constitution", "Obedience", "Sensitivity"), jp_type = ["anal", "sex"], tags = 'XXX', description = __("Learn to pleasure a man... Or a woman, if you're so inclined. Why not learn both?"), sound = s_aah),
                                
                                Quest("class", name = __('Hardcore{#1}'), main_stat = 'Anal', second_stat = 'Fetish', other_stats = ("Libido", "Constitution", "Obedience", "Sensitivity"), jp_type = ["anal", "fetish"], tags = 'hardcore', description = __("We've got more tools than a hardware store, more beasts than the palace zoo... And by the time we're finished, they're all gonna fit inside of her!{#1}"), sound = s_scream),
                                
                                Quest("class", name = __('Hardcore'), main_stat = 'Fetish', second_stat = 'Service', other_stats = ("Libido", "Constitution", "Obedience", "Sensitivity"), jp_type = ["service", "fetish"], tags = 'hardcore', description = __("We've got more tools than a hardware store, more beasts than the palace zoo... And by the time we're finished, they're all gonna fit inside of her!"), sound = s_scream),
                                ]

    return

#### END OF BK POSTINGS FILE ####
