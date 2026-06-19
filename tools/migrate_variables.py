#!/usr/bin/env python3
"""
Migrate stats, personalities, ranks from hardcoded variables.rpy to JSON.
ZH: 将 variables.rpy 中的硬编码 stats/personalities/ranks 迁移到 JSON。
"""

import re
from pathlib import Path

VARIABLES_RPY = Path("game/core/init/variables.rpy")
text = VARIABLES_RPY.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# 1. Replace stats block
# ---------------------------------------------------------------------------
old_stats = '''    ## STAT NAMES (SKILLS) ##


    gstats_main = [
        __("Charm"),
        __("Beauty"),
        __("Body"),
        __("Refinement"),
        __("Sensitivity"),
        __("Libido"),
        __("Constitution"),
        __("Obedience"),
        ]

    gstats_sex = [
        __("Service"),
        __("Sex"),
        __("Anal"),
        __("Fetish")
        ]

    all_skills = [s.lower() for s in gstats_main + gstats_sex]


    ## STAT DESCRIPTION ##

    gstats_dict = {
                    "Beauty" : __("How beautiful she looks. Affects work as a {b}masseuse{/b} and regular {b}sex{/b}. Current masseuse capacity: {b}%s{/b} customer%s."),
                    "Body" : __("How well-shaped and firm her body is. Affects work as a {b}dancer{/b} and {b}anal{/b} sex. Current dancer capacity: {b}%s{/b} customer%s."),
                    "Charm" : __("Her personality and presence. Affects work as a {b}waitress{/b} and sexual {b}service{/b}. Current waitress capacity: {b}%s{/b} customer%s."),
                    "Refinement" : __("How intelligent and worldly she is. Affects work as a {b}geisha{/b} and {b}fetish{/b} sex acts. Current geisha capacity: {b}%s{/b} customer%s."),
                    "Libido" : __("How eager for sex she is. Affects {b}dancer{/b}, {b}sex{/b} and max {b}whoring{/b} customers. Current whore capacity: {b}%s{/b} customer%s."),
                    "Sensitivity" : __("How sensitive she is to her body and her partners. Affects {b}masseuse{/b}, {b}service{/b} and improves customer {b}satisfaction{/b}."),
                    "Constitution" : __("Her stamina. Affects {b}waitress{/b}, {b}anal{/b} sex, improves her maximum {b}energy{/b} and allows her to serve {b}more customers{/b}."),
                    "Obedience" : __("How receptive she is to orders and servitude. Affects {b}geisha{/b}, {b}fetish{/b} sexual acts and chances of accepting {b}work{/b} or {b}training{/b}."),
                    "Service" : __("How good she is with handjobs, blowjobs and other sexual services."),
                    "Sex" : __("How good she is at regular sex."),
                    "Anal" : __("How good she is at anal sex."),
                    "Fetish" : __("How good she is at BDSM and other unusual requests.")
                }

    gstats_descript = {
                    "beauty" : __("a beautiful girl"),
                    "body" : __("a girl with a hot body"),
                    "charm" : __("a charming girl"),
                    "refinement" : __("a refined girl"),
                    }

    gstat_job_skill = {
                    "Beauty" : __("masseuse"),
                    "Body" : __("dancer"),
                    "Charm" : __("waitress"),
                    "Refinement" : __("geisha"),
                    "Libido" : __("whore"),
                    }

    MC_stat_color = {
                    "strength" : __("{color=[c_darkred]}%s{/color}"),
                    "defense" : __("{color=[c_darkred]}%s{/color}"),
                    "spirit" : __("{color=[c_darkblue]}%s{/color}"),
                    "charisma" : __("{color=[c_emerald]}%s{/color}"),
                    "speed" : __("{color=[c_lightblue]}%s{/color}"),
                    }

    preference_color = {
                "refuses" : __("{color=#F70000}%s{/color}"),
#                 "extremely reluctant" : __("{color=#FF2626}%s{/color}"),
                "very reluctant" : __("{color=#FF5353}%s{/color}"),
                "reluctant" : __("{color=#FF8E8E}%s{/color}"),
                "a little reluctant" : __("{color=#FFB5B5}%s{/color}"),
                "indifferent" : __("{color=[c_white]}%s{/color}"),
                "a little interested" : __("{color=#BDF4CB}%s{/color}"),
                "interested" : __("{color=#7CEB98}%s{/color}"),
                "very interested" : __("{color=#1FCB4A}%s{/color}"),
                "fascinated" : __("{color=[c_orange]}%s{/color}"),
                None: __("%s"),
                }'''

new_stats = '''    ## STAT NAMES (SKILLS) — JSON-driven (BK Evolution) ##
    import json as _json, os as _os
    _stats_path = _os.path.join(renpy.config.gamedir, "custom", "data", "stats", "stats.json")
    _stats_data = {}
    if _os.path.exists(_stats_path):
        with open(_stats_path, 'r', encoding='utf-8') as _f:
            _stats_data = _json.load(_f)

    gstats_main = [__(s) for s in _stats_data.get("main_stats", ["Charm", "Beauty", "Body", "Refinement", "Sensitivity", "Libido", "Constitution", "Obedience"])]
    gstats_sex = [__(s) for s in _stats_data.get("sex_stats", ["Service", "Sex", "Anal", "Fetish"])]
    all_skills = [s.lower() for s in gstats_main + gstats_sex]

    ## STAT DESCRIPTION ##
    _sd = _stats_data.get("stat_descriptions", {})
    gstats_dict = {k: __(v) for k, v in _sd.items()}

    _ssd = _stats_data.get("stat_short_descriptions", {})
    gstats_descript = {k: __(v) for k, v in _ssd.items()}

    _sjs = _stats_data.get("stat_job_skills", {})
    gstat_job_skill = {k: __(v) for k, v in _sjs.items()}

    _msc = _stats_data.get("mc_stat_colors", {})
    MC_stat_color = {k: v for k, v in _msc.items()}

    _pc = _stats_data.get("preference_colors", {})
    preference_color = {k: v for k, v in _pc.items()}
    preference_color[None] = _pc.get(None, "%s")'''

if old_stats in text:
    text = text.replace(old_stats, new_stats)
    print("[OK] Stats block replaced")
else:
    print("[WARN] Stats block not found (may have been modified)")

# ---------------------------------------------------------------------------
# 2. Replace personalities block
# ---------------------------------------------------------------------------
old_personalities = '''    gpersonalities = {
                        "pervert" : Personality(name="pervert", attributes=("very extravert", "very lewd"), description="Wild and 'no limit' kind of girl. Curious about all sorts of sexual acts, the more perverted the better. She doesn't care for romance."),
                        "rebel" : Personality(name="rebel", attributes=("very extravert", "very dom"), often_stories = ["slave_story5"], description="Always fighting and contradicting others, fiercely independent. She must do things of her own free will."),
                        "cold" : Personality(name="cold", attributes=("very materialist", "very introvert"), description="Cold and detached, she doesn't show her feelings easily. She seems strangely unconcerned about what goes on around her, and uninterested in the fate of others."),
                        "nerd" : Personality(name="nerd", attributes=("very introvert", "very idealist"), often_stories = ["slave_story8"], description="Quiet and bookish. Rather light-headed. Always curious. She doesn't like parties, noise, and physical effort."),
                        "masochist" : Personality(name="masochist", attributes=("very introvert", "very sub"), description="The lower the better. She likes to be at the bottom and secretly enjoys being mistreated. Gifts and loving gestures annoy her, she feels she doesn't deserve them."),
                        "bimbo" : Personality(name="bimbo", attributes=("very materialist", "very lewd"), description="Vain, attention-craved, she cares about status and wealth. Loves presents and compliments. She has no qualms about using her body to get these things, too."),
                        "meek" : Personality(name="meek", attributes=("very modest", "very sub"), often_stories = ["slave_story4"], rarely_stories = ["slave_story5","slave_story8"], description="Shy, easily swayed, will cry rather than resist. Doesn't like conflict."),
#                         "heartless" : Personality(name="heartless", attributes=("very materialist", "very dom"), description="Cold, calculating, domineering and selfish. Will always try to benefit at the expense of others."),
                        "sweet" : Personality(name="sweet", attributes=("very idealist", "very extravert"), description="Lovely and sunny personality, always positive, and rather romantic. She doesn't like negativity."),

                        "superficial" : Personality(name="superficial", attributes=("very extravert", "very materialist"), description="Ever the socialite, she cares about being seen, preferably in the most outstanding outfit and expensive jewelry. Some call her needy and craving for attention, but she knows they're just jealous of her new shoes..."),
                        "holy" : Personality(name="holy", attributes=("very extravert", "very modest"), never_stories = ["slave_story7","slave_story8"], description="A firebrand promoter of religion and morality, she prays every night for the salvation of her soul and tries to convert others to her beliefs. With little success so far, but she won't give up."),
                        "helper" : Personality(name="helper", attributes=("very extravert", "very sub"), description="Always ready to help her friends, places herself after others. Can be a bit nosy sometimes."),
                        "creep" : Personality(name="creep", attributes=("very introvert", "very lewd"), description="Shy and awkward around people, she is obsessed about all sorts of naughty topics that she researches in her own time. Get complaints for stalking - a lot."),
                        "repressed" : Personality(name="repressed", attributes=("very introvert", "very modest"), description="Raised in a very strict environment, she lives in fear of her own impulses and tries her hardest to suppress them."),
                        "schemer" : Personality(name="schemer", attributes=("very introvert", "very dom"), description="She likes nothing more than to scheme and make grand plans, ready to assert her dominance over all living beings... Some day. In the meantime, if she has to suck a dick... So be it."),
                        "prude" : Personality(name="prude", attributes=("very materialist", "very modest"), rarely_stories = ["slave_story7","slave_story8"], description="She behaves like a good, Arios-fearing girl at all times. She frowns on frivolity and amoral behavior. Some think she has dirty thoughts in secret, but if so, she hides them well."),
                        "princess" : Personality(name="princess", attributes=("very dom", "very materialist"), often_stories = ["slave_story6"], rarely_stories = ["slave_story1","slave_story2","slave_story3","slave_story5","slave_story7","slave_story8"], never_stories = ["slave_story4"], description="A figurative princess (or is she?), she thinks everyone ought to be at her feet and deliver on her every whim. Her behavior can be cruel, but mostly she's naive."),
                        "pet" : Personality(name="pet", attributes=("very materialist", "very sub"), rarely_stories = ["slave_story5","slave_story8"], description="The teacher's pet. Always ready to please her master, she likes nothing more than to live in comfort at his feet. Some despise her servility, calling her unpleasant names behind her back."),
                        "easy" : Personality(name="easy", attributes=("very lewd", "very idealist"), description="It's not her fault, she has always attracted men, and never had the heart to turn them down. Although many call her easy, her sole purpose is to spread joy. Hopefully not STDs."),
                        "class president" : Personality(name="class president", attributes=("very modest", "very idealist"), often_stories = ["slave_story8"], description="She must always be on top, she strives to be exemplary and despises every kind of misconduct. The high expectations she has of others mirror the harsh discipline whe puts herself through."),
                        "tsundere" : Personality(name="tsundere", attributes=("very idealist", "very dom"), description="Easy to anger, hard to please, she has a secret soft spot. She will put herself at risk to help others, then kick their butts for needing help in the first place."),
                        "loyal" : Personality(name="loyal", attributes=("very idealist", "very sub"), often_stories = ["slave_story2"], description="She always follows orders, out of a sense of duty more than fear. She believes everyone must know their place, and do their best to excel at whatever task they are given. Even whores."),
                        "yandere" : Personality(name="yandere", attributes=("very lewd", "very dom"), rarely_stories = ["slave_story3","slave_story7"], description="Very high on the hot yet neurotic scale. Loving and devoted, but also firebatshit crazy. She's ready to do anything to get her man and snuff out the competition, including... actually snuffing them."),
                        "masochist2" : Personality(name="masochist", attributes=("very lewd", "very sub"), description="The lower the better. She likes to be at the bottom and secretly enjoys being mistreated. Gifts and loving gestures annoy her, she feels she doesn't deserve them."),
                        "stubborn" : Personality(name="stubborn", attributes=("very modest", "very dom"), description="She doesn't like people who don't share her strict principles and moral values, and she doesn't take contradiction well either. A lot of fun at parties, if you like parties that end with a tavern brawl."),
                    }

    reserved_personality_names = gpersonalities.keys()'''

new_personalities = '''    ## GIRL PERSONALITIES — JSON-driven (BK Evolution) ##
    _pers_path = _os.path.join(renpy.config.gamedir, "custom", "data", "personalities", "personalities.json")
    _pers_data = []
    if _os.path.exists(_pers_path):
        with open(_pers_path, 'r', encoding='utf-8') as _f:
            _pers_data = _json.load(_f)

    gpersonalities = {}
    for _p in _pers_data:
        _pid = _p.get("id")
        if not _pid:
            continue
        gpersonalities[_pid] = Personality(
            name=_p.get("name", _pid),
            attributes=tuple(_p.get("attributes", [])),
            description=__(_p.get("description", "")),
            often_stories=_p.get("often_stories", []),
            rarely_stories=_p.get("rarely_stories", []),
            never_stories=_p.get("never_stories", []),
            dialogue_personality_weight=_p.get("dialogue_personality_weight", 3),
            dialogue_attribute_weight=_p.get("dialogue_attribute_weight", 1),
        )

    reserved_personality_names = gpersonalities.keys()'''

if old_personalities in text:
    text = text.replace(old_personalities, new_personalities)
    print("[OK] Personalities block replaced")
else:
    print("[WARN] Personalities block not found (may have been modified)")

# ---------------------------------------------------------------------------
# 3. Replace ranks block
# ---------------------------------------------------------------------------
old_ranks = '''    rank_name = {
                    1 : __("C"), #"{color=[c_white]}C{/color}",
                    2 : __("B"), #"{color=[c_yellow]}B{/color}",
                    3 : __("A"), #"{color=[c_lightblue]}A{/color}",
                    4 : __("S"), #"{color=[c_purple]}S{/color}",
                    5 : __("X"), #"{color=[c_gold]}X{/color}",
                    "waitress0": __("Unskilled"),
                    "waitress1": __("Beginner Waitress"),
                    "waitress2": __("Competent Waitress"),
                    "waitress3": __("Skilled Barmaid"),
                    "waitress4": __("Expert Barmaid"),
                    "waitress5": __("Tavern Queen"),
                    "dancer0": __("Unskilled"),
                    "dancer1": __("Beginner Dancer"),
                    "dancer2": __("Competent Dancer"),
                    "dancer3": __("Skilled Stripper"),
                    "dancer4": __("Expert Stripper"),
                    "dancer5": __("Poledance Queen"),
                    "masseuse0": __("Unskilled"),
                    "masseuse1": __("Beginner Masseuse"),
                    "masseuse2": __("Competent Masseuse"),
                    "masseuse3": __("Skilled Massage girl"),
                    "masseuse4": __("Expert Massage girl"),
                    "masseuse5": __("Soapy Queen"),
                    "geisha0": __("Unskilled"),
                    "geisha1": __("Beginner Maiko"),
                    "geisha2": __("Competent Maiko"),
                    "geisha3": __("Skilled Geisha"),
                    "geisha4": __("Expert Geisha"),
                    "geisha5": __("Courtesan Queen"),
                    "sex0" : __("Unskilled"),
                    "sex1" : __("Beginner Prostitute"),
                    "sex2" : __("Competent Prostitute"),
                    "sex3" : __("Skilled Whore"),
                    "sex4" : __("Expert Whore"),
                    "sex5" : __("Brothel Queen"),
                    "service0" : __("Unskilled"),
                    "service1" : __("Beginner Wanker"),
                    "service2" : __("Competent Wanker"),
                    "service3" : __("Skilled Cocksucker"),
                    "service4" : __("Expert Cocksucker"),
                    "service5" : __("Blowjob Queen"),
                    "anal0" : __("Unskilled"),
                    "anal1" : __("Beginner Anal Slut"),
                    "anal2" : __("Competent Anal Slut"),
                    "anal3" : __("Skilled Butt Lover"),
                    "anal4" : __("Expert Butt Lover"),
                    "anal5" : __("Anal Queen"),
                    "fetish0" : __("Unskilled"),
                    "fetish1" : __("Beginner Servant"),
                    "fetish2" : __("Competent Servant"),
                    "fetish3" : __("Skilled Escort"),
                    "fetish4" : __("Expert Escort"),
                    "fetish5" : __("Bondage Queen"),
                }


    jp_to_level = {
                    -1 : 0,
                    0 : 50,
                    1 : 125,
                    2 : 250,
                    3 : 425,
                    4 : 650,
                }

    job_up_dict = {
                    "waitress" : ("charm", "constitution", "beauty", "body"),
                    "dancer" : ("body", "libido", "charm", "refinement"),
                    "masseuse" : ("beauty", "sensitivity", "body", "refinement"),
                    "geisha" : ("refinement", "obedience", "charm", "beauty"),
                    "service" : ("service", "sensitivity", "charm", "fetish"),
                    "sex" : ("sex", "libido", "beauty", "service"),
                    "anal" : ("anal", "constitution", "body", "sex"),
                    "fetish" : ("fetish", "obedience", "refinement", "anal"),
                }

    job_up_change = {
                    1 : (5, 5, 0),
                    2 : (10, 5, 0),
                    3 : (15, 10, 5),
                    4 : (25, 15, 10),
                    5 : (40, 25, 15),
                }

    rep_to_rank = {
                    0 : 0,
                    1 : 10,
                    2 : 25,
                    3 : 50,
                    4 : 100,
                    5 : 1000,
                }

    rep_gains_dict = { # Read as: For a given girl rank - 'cust.rank relative to girl.rank (e.g: __('\'higher\') = The customer has a higher rank) : must get a result >= X to earn rep'
                    1 : {"higher" : __("bad"), "same" : __("average")},
                    2 : {"higher" : __("bad"), "same" : __("average"), "lower" : __("good")},
                    3 : {"higher" : __("average"), "same" : __("good"), "lower" : __("very good")},
                    4 : {"higher" : __("average"), "same" : __("good"), "lower" : __("very good")},
                    5 : {"same" : __("good"), "lower" : __("perfect")}, # Made easier for now
                }

    rep_loss_dict = { # Read as: __('\'must get a result < X to lose rep\'). Being < to very bad is actually impossible
                    1 : {"higher" : __("very bad"), "same" : __("bad")},
                    2 : {"higher" : __("very bad"), "same" : __("bad"), "lower" : __("average")},
                    3 : {"higher" : __("bad"), "same" : __("average"), "lower" : __("good")},
                    4 : {"higher" : __("bad"), "same" : __("average"), "lower" : __("good")},
                    5 : {"same" : __("average"), "lower" : __("very good")}, # Made easier for now
                }'''

new_ranks = '''    ## RANKS / JOB POINTS — JSON-driven (BK Evolution) ##
    _ranks_path = _os.path.join(renpy.config.gamedir, "custom", "data", "ranks", "ranks.json")
    _ranks_data = {}
    if _os.path.exists(_ranks_path):
        with open(_ranks_path, 'r', encoding='utf-8') as _f:
            _ranks_data = _json.load(_f)

    _rn = _ranks_data.get("rank_names", {})
    rank_name = {int(k) if k.isdigit() else k: __(v) for k, v in _rn.items()}

    _jtl = _ranks_data.get("jp_to_level", {})
    jp_to_level = {int(k): v for k, v in _jtl.items()}

    _jud = _ranks_data.get("job_up_dict", {})
    job_up_dict = {k: tuple(v) for k, v in _jud.items()}

    _juc = _ranks_data.get("job_up_change", {})
    job_up_change = {int(k): tuple(v) for k, v in _juc.items()}

    _rtr = _ranks_data.get("rep_to_rank", {})
    rep_to_rank = {int(k): v for k, v in _rtr.items()}

    _rgd = _ranks_data.get("rep_gains_dict", {})
    rep_gains_dict = {int(k): {sk: __(sv) for sk, sv in svdict.items()} for k, svdict in _rgd.items()}

    _rld = _ranks_data.get("rep_loss_dict", {})
    rep_loss_dict = {int(k): {sk: __(sv) for sk, sv in svdict.items()} for k, svdict in _rld.items()}'''

if old_ranks in text:
    text = text.replace(old_ranks, new_ranks)
    print("[OK] Ranks block replaced")
else:
    print("[WARN] Ranks block not found (may have been modified)")

# Write back
VARIABLES_RPY.write_text(text, encoding="utf-8")
print("\nDone. File saved:", VARIABLES_RPY)
