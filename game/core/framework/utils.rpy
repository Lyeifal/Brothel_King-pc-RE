#### Utils functions ####

init -3 python:
    def xres(_size=None): # Some custom resolutions may work better with a different xy ratio
        if _size is None:
            return config.screen_width
        try:
            return res_dict["x", _size]
        except:
            res_dict["x", _size] = int(_size*config.screen_width*res_xy_ratio/RES_BASE_X)
            return res_dict["x", _size]

    def yres(_size=None):
        if _size is None:
            return config.screen_height
        try:
            return res_dict["y", _size]
        except:
            res_dict["y", _size] = int(_size*config.screen_height/RES_BASE_Y)
            return res_dict["y", _size]

    def res_font(_size):
        return yres(_size)

    def res_tb(_size): # Always returns square dimensions. This function returns a tuple - unpack it with * if needed
        return (yres(_size),)*2

#<Chris12 PredictImages> Disabled, was causing problems as Renpy doesn't support multithreading (Goldo)
    # # Threading is necessary, because otherwise the screen only shows AFTER ALL images have been loaded.
    # # That would actually make things slower. With threading, the images load in the background as intended.
    # # This function seems to work only if called from BKscreens. Probably got something to do with interactions. Maybe I'm just misunderstanding, though.
    # def predict_images(girls, predict_portraits = True, predict_profiles = True):
    #     def predict_images_helper():
    #         try:
    #             # Predict all portraits first since they are needed immediately.
    #             for girl in girls:
    #                 if predict_portraits and girl.portrait is not None : renpy.predict(girl.portrait.get(side=True))
    #
    #             # After that, begin loading the profile images
    #             for girl in girls:
    #                 if predict_profiles and girl.profile is not None : renpy.predict(girl.profile.get(profile=True))
    #         except: pass
    #     if girls is not None and len(girls) > 0:
    #         t = threading.Thread(target=predict_images_helper)
    #         t.daemon = True
    #         t.start()

    def fast_portrait(path, x, y):
        for pic in GirlFilesDict.get_pics(path):
            if pic.has_tag("portrait") and not pic.has_tag("naked"):
                return pic.get(x, y)
        for pic in GirlFilesDict.get_pics(path):
            if pic.has_tag("portrait"):
                return pic.get(x, y)
        for pic in GirlFilesDict.get_pics(path):
            if pic.has_tag("profile"):
                return pic.get(x, y)
        return Picture(path="resources/backgrounds/not_found.webp").get(x, y)

    def predict_next_img(event_queues): # use renpy.predict() to cache image(s) from current first event of first non-empty queue

        # Including DougTheC's fix #

        for queue in event_queues :
            if queue and isinstance(queue[0], Event):
                if queue[0].pic is not None:
                    if isinstance(queue[0].pic, Picture):
                        renpy.predict(queue[0].pic.get(res_event_width, res_event_height))
                    else:
                        renpy.predict(queue[0].pic)    # image may be described by unicode string, especially for farm
                if queue[0].background is not None:
                    if isinstance(queue[0].background, Picture):
                        renpy.predict(queue[0].background.get(res_event_width, res_event_height))
                    else:
                        renpy.predict(queue[0].background)    # image may be described by unicode string, especially for farm

                break

#</Chris12 PredictImages>


    def dice(sides, number = 1):
        """Randomly generates a number of dices with a result from 1 to sides"""

        return sum(renpy.random.randint(1, sides) for i in range(number))


    def rand_choice(li, nb = None): # returns False for an empty list or invalid nb

        li = list(li)

        if li:
            if nb == None: # Returns a single object if nb is None (default value)
                return renpy.random.choice(li)
            elif nb > 0: # Returns a list if nb is provided. May return less than the number of items requested if len(li) < nb
                try:
                    return renpy.random.sample(li, k=int(nb))
                except:
                    return li

        return False


    def weighted_choice(li, nb=None, duplicates=False): # Where li is a list of tuples with item, weight, and nb is the number of choices drawn

        # Returns a single item according to a random weighted choice if nb is not provided
        # Returns several items as part of a list if nb is provided
        # Returns False or an empty list if no choices are available

        r = []

        if nb:
            choice_nb = nb
        else:
            choice_nb = 1

        if li:
            if len(li) <= choice_nb and not duplicates: # Returns the whole choice list if duplicates is inactive and the number of choices is equal or in excess of choice list length, to avoid infinite loops
                r = [x for x, w in li]

            else:
                copy_list = [(x, w) for x, w in li]
                weightsum = sum(w for x, w in copy_list)

                # Main loop

                while len(r) < choice_nb:

                    rand = renpy.random.random() * weightsum # Random returns a number between 0.0 and 1.0

                    currentWeight = 0

                    for x, w in copy_list:
                        currentWeight += w
                        if currentWeight >= rand :
                            r.append(x)
                            break

                    else : # Just to be safe against potential rounding problems
                        x, w = copy_list[-1]
                        r.append(x)

                    if not duplicates:
                        copy_list = [(x, w) for x, w in copy_list if x not in r]
                        weightsum = sum(w for x, w in copy_list)

        if nb == None:
            if len(r) >= 1: # Checks both the intended number and the result list before returning a single item
                return r[0]
            else:
                return False # Returns False if no list was provided
        else:
            return r

    def round_int(x): # Rounds to the nearest decimal number (remember to force a float when dividing two integers, python is a dick about that)

        x = float(x)

        return int(round(x))

    def str_int(x): # Returns a string of an integer
        return str(round_int(x))

    def str_dec(nb, decimals=2): # Returns a string of either an integer or a float, depending on the nb of decimals available
        return ((("%." + str(decimals) + "f") % nb).rstrip("0")).rstrip(".")

    def round_down(x): # Home-made version of math.floor
        return int(x)

    def round_up(x): # Home-made version of math.ceil
        if int(x) < x:
            return int(x) + 1
        else:
            return int(x)

    def round_best(x, decimals=1):

        for d in range(decimals):
            if not (x * 10 ** (d)) % 1:
                if d == 0:
                    return int(x)
                else:
                    return round(x, d)

        return round(x, decimals)


    def mean(values, integer=False): # Can be fed a generator as well
        n = 0
        s = 0
        for v in values:
            s += v
            n += 1

        r = float(s) / n # Without float, this would round down to an integer when all values are integers

        if not integer:
            return r
        else:
            return round_int(r)


    def mean_int(values):
        return mean(values, True)

    def clamp(val, _min, _max): # Clamps value between min and max (included)
        return max(min(val, _max), _min)


    def get_change_min_max(val, chg, _min, _max=10**18, enforce_boundaries=True): # Returns change to value after applying min and max. DOES NOT RETURN THE NEW VALUE.

        # If enforce_boundaries is True, a value outside the min-max range will be forced back to min or max

        if not enforce_boundaries:
            if val < _min or val > _max: # Change will be ignored if the value is outside of range
                return 0

        if _min <= val+chg <= _max:
            return chg

        elif val+chg < _min:
            return _min - val

        elif val+chg > _max:
            return _max - val


    def is_string(it):
        if isinstance(it, basestring):
            return True
        else:
            return False

    def make_list(it, obj_type = None): # Will automatically make a list of a single string, integer or float. Specify object type to list otherwise.

        if not it:
            return []

        if is_string(it) or isinstance(it, int) or isinstance(it, float):
            return list([it])

        if obj_type:
            if isinstance(it, obj_type):
                return list([it])

        return list(it)



    def reverse_if(boost, chg): ## Reverses boost if a stat is decreasing

        if chg < 0:
            boost = 1/float(boost)

        return boost

    def plus_text(nb, color_scheme=None, pos_marker="+", neg_marker="", decimals=2): # Returns number as text with +/- sign and color scheme. Use decimals to specify the max length of a float (0 to force integer)

        pos_color, neg_color = {"standard": ("a little good", "a little bad"), "normal": ("good", "bad"), "gold": ("gold", "bad"), "stat": ("good", "bad"), "xp": ("xp", "bad"), "jp": ("jp", "bad"), "rep": ("rep", "bad"), None: (None, None)}[color_scheme]

        if nb == 0:  # Use to catch exact zeros before next check
            return "0"
        elif not decimals:
            nb_txt = '{:,}'.format(int(nb))
        else:
            nb_txt = str_dec(nb, decimals)

        if nb > 0:
            return event_color[pos_color] % (pos_marker + nb_txt)
        elif nb < 0:
            return event_color[neg_color] % (neg_marker + nb_txt)

    def gold_text(nb, pos_marker=""):
        return plus_text(nb, "gold", pos_marker=pos_marker, decimals=False)

    def and_text(li, txt=None, prune_empty=True, if_none=event_color["bad"] % "#ERROR# No list", separator=", "): # prune_empty removes empty entries from the list

        if txt is None:
            txt = __(" and ")

        if prune_empty:
            li = [x for x in li if x]

        if not li:
            return if_none

        if len(li) == 1:
            return li[0]

        elif len(li) > 1:
            return separator.join(li[:-1]) + txt + li[-1]

        else:
            return if_none

    def list_text(li, txt="* ", prune_empty=True, if_none=event_color["bad"] % "#ERROR# No list"): # prune_empty removes empty entries from the list

        if prune_empty:
            li = [x for x in li if x]

        if not li:
            return if_none

        return txt + ("\n" + txt).join(li)

    # ── i18n-safe plural & article ──────────────────────────────────────
    # Phase 0.1: These are now language-aware.
    #
    # pluralize() is the recommended replacement for plural().
    #   - English: pluralize(1, "file", "files") → "file"
    #              pluralize(3, "file", "files") → "files"
    #   - Chinese/Japanese/Korean: always returns singular form.
    #
    # article() is retained for compatibility but returns "" for non-English
    # locales (CJK languages do not use articles).

    def _is_english_locale():
        """True when the active language has no plural/article grammar."""
        lang = getattr(renpy.game.preferences, 'language', None)
        return lang is None  # None = English, all others = no plural/article suffixes

    def pluralize(nb, singular_form, plural_form=None):
        """Return the correct singular or plural form for the current language.

        For English: uses CLDR-style nplurals=2 (n != 1). If plural_form is
        omitted, defaults to singular_form + 's'.
        For CJK/Korean: always returns singular_form (no grammatical number).
        """
        if not _is_english_locale():
            return singular_form
        if abs(nb) == 1:
            return singular_form
        if plural_form is not None:
            return plural_form
        return singular_form + "s"

    def plural(nb, ending="s", singular=""):
        """DEPRECATED: use pluralize() instead.

        Kept for backward compatibility. Now language-aware:
        - English: returns *ending* if nb != 1, otherwise *singular*.
        - CJK/Korean: always returns "" (no plural suffix needed).
        """
        if not _is_english_locale():
            return ""
        if abs(nb) == 1:
            return singular
        return ending

    def article(noun, definite=False):
        """DEPRECATED: use __() with full noun phrases instead.

        Kept for backward compatibility. Now language-aware:
        - English: returns "a "/"an "/"the " + noun.
        - CJK/Korean: returns noun unchanged (no articles).
        """
        if not _is_english_locale():
            return noun
        if definite:
            return __("the ") + noun
        elif noun[0].lower() in ("a", "i", "e", "o"):
            return __("an ") + noun
        else:
            return __("a ") + noun

    def season_text(d): # Where d is a dictionary containing text for all 4 seasons
        return d[calendar.get_season()]

    def capitalize(s): # This is different from the string capitalize method as it doesn't alter subsequent caps after the first char.
        return s[:1].upper() + s[1:]

    def uncapitalize(s):
        return s[:1].lower() + s[1:]

    def cycle_list(mylist, item, number=1):

        if item not in mylist:
            raise AssertionError("Item not in list")

        idx = (mylist.index(item) + number) % len(mylist)

        return mylist[idx]

    def move_up_list(mylist, item):
        idx = mylist.index(item)
        if idx > 0:
            mylist.insert(idx-1, mylist.pop(idx))

    def move_down_list(mylist, item):
        idx = mylist.index(item)
        if idx < len(mylist):
            mylist.insert(idx+1, mylist.pop(idx))

    def is_imgfile(file, video=True):
        if is_string(file):
            if (file[-4:].lower() in IMGFORMATS or file[-5:].lower() in IMGFORMATS):
                return True
            if video and is_videofile(file):
                return True
        return False

    def is_videofile(file):
        if is_string(file):
            if (file[-4:].lower() in VIDEOFORMATS or file[-5:].lower() in VIDEOFORMATS):
                return True
        return False

    def list_imgfiles(path, strict=True): # Returns a list of all image files in the given folder (and sub-folders if strict is set to False)

        if strict:
            return [f for f in renpy.list_files() if f.startswith(path) and is_imgfile(f) and f.count("/") == path.count("/")]

        else:
            return [f for f in renpy.list_files() if f.startswith(path) and is_imgfile(f)]

    def get_current_folder():
        foldername, ignored1, ignored2 = renpy.game.context().current

        # Trim "game/" and the current file from the folder path
        foldername = foldername[len("game/"):foldername.rfind("/")+1]
        return foldername

    def count_lines(s, char_per_line):

    # Kills unwanted format characters to avoid artificial character count (rough)
        s = s.replace("{b}", "")
        s = s.replace("{/b}", "")
        s = s.replace("{i}", "")
        s = s.replace("{/i}", "")
        s = s.replace("{color=", "")
        s = s.replace("{/color}", "")

        lines = s.split("\n")

        total = len(lines)

        for line in lines:
            total += len(line) // char_per_line

        if s.endswith("\n"):
            total -= 1

        return total

    def girl_object_count():
        return sum(1 for obj in gc.get_referrers(Girl) if obj.__class__ is Girl)

    def girl_gc():
        glist = game.get_all_girls()
        dlist = []

        for g in gc.get_referrers(Girl):
            if g.__class__ is Girl:
                if g not in glist:
                    dlist.append(g)

        nb = len(dlist)

        while dlist:
            del dlist[0]

        gc.collect()

        return __("%i girls deleted. Remaining: %i") % (nb, girl_object_count())


    def debug_sorting_girls():

        MC.girls = slavemarket.girls

        for girl in MC.girls:
            girl.level = dice(10)
            girl.rank = dice(4)
            girl.set_job(rand_choice(all_jobs))

    def is_renpy_8_1():
        if renpy.version_tuple[0] > 8 or (renpy.version_tuple[0] == 8 and renpy.version_tuple[1] >= 1):
            return True
        return False

    def norollback():
        if debug_mode:
            renpy.block_rollback()

    def are_different(_list):
        # Check if different items are mixed
        if len(_list) < 2:
            return False

        different = [it for it in _list[1:] if it != _list[0]]

        if different:
            return True
        return False

init -3 python:

    def roll_result(crit_success = 95, crit_fail = 5 ): # This rolls a dice to randomize the result a little

        r = dice(100)

        if r <= crit_fail:
            return __("critical failure")

        elif r <= 25:
            return __("failure")

        elif r <= 75:
            return __("neutral")

        elif r <= crit_success:
            return __("success")

        elif r <= 100:
            return __("critical success")



    def show_tt(pos="top_right"):

        tt = Tooltip("")

        if pos == "center":
            renpy.show_screen("tool", x = 0.5, y = 0.5, w = 300, h = 150)

        elif pos == "right":
            renpy.show_screen("tool", x = 1.0, y = 0.7, w = 215, h = 150)

        elif pos == "top_right":
            renpy.show_screen("tool", x = 0.93, y = 0.0, w = 0.32, h = 0.075, bg = False)

        elif pos == "hide":
            renpy.hide_screen("tool")

        return tt



    def percent_text(value, use_plus=True):
        percentage = round_int(value * 100)

        if use_plus:
            return "%s%%" % plus_minus(percentage)
        else:
            return "%s%%" % str(percentage)

