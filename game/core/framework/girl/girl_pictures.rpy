#### GirlPictures — Image selection and management component ####
# Phase 2.1: Extracted from girlclass.rpy (~500 lines of image logic).
# Handles: portrait/profile selection, picture refresh, pack evaluation,
# tag-based picture search, CG unlocking, and AutoRepair checks.

init -2 python:

    class GirlPictures(object):
        """Image selection and management for a Girl.

        All methods receive a `girl` reference for access to girl state
        (naked status, job, location, path, etc.).
        """

        def __init__(self, girl):
            self.girl = girl

        # ── Pack evaluation ──

        def evaluate_girlpack(self):
            """Evaluate girl pack metrics for the pack rating system (A-F)."""
            start = datetime.datetime.now()
            g = self.girl
            main_cover_score, main_div_score, op_cover_score, op_div_score = 0.0, 0.0, 0.0, 0.0

            # Check pictures with 'Main' tags (including naked variations)
            for tag in normal_tags:
                currentList = get_pic_list(g, [tag], not_tags=["naked"], weighted=False)
                if len(currentList): main_cover_score += 1
                main_div_score += min(10, len(currentList))

                currentList = get_pic_list(g, [tag], and_tags=["naked"], weighted=False)
                if len(currentList): main_cover_score += 1
                main_div_score += min(10, len(currentList))

            for tag in all_sex_acts:
                currentList = get_pic_list(g, [tag], not_tags=["group", "bisexual", "machine", "beast", "monster"], weighted=False)
                if len(currentList): main_cover_score += 1
                main_div_score += min(10, len(currentList))

                for tag2 in ("group", "bisexual"):
                    currentList = get_pic_list(g, [tag2], and_tags=[tag], not_tags=["machine", "beast", "monster"], weighted=False)
                    if len(currentList): main_cover_score += 1
                    main_div_score += min(10, len(currentList))

            main_cover_score_total = len(normal_tags) * 2 + len(all_sex_acts) * 3

            # Check optional tags (farm + fixations)
            extended_sex_acts_tuples = [make_list(tag) for tag in extended_sex_acts]
            for tag in all_farm_tags:
                unfiltered = get_pic_list(g, [tag], weighted=False)
                for tag2 in extended_sex_acts_tuples:
                    currentList = list(filter(lambda pic: pic.has_tag(tag2), unfiltered))
                    if len(currentList): op_cover_score += 1
                    op_div_score += min(5, len(currentList))

            for fix in fix_dict.values():
                unfiltered = get_pic_list(g, fix.tag_list[0], and_tags=[], not_tags=fix.not_list, weighted=False)
                for atag in fix.acts:
                    atagTuple = make_list(atag)
                    currentList = list(filter(lambda pic: pic.has_tags(atagTuple), unfiltered))
                    if len(currentList): op_cover_score += 1
                    op_div_score += min(5, len(currentList))

            op_cover_score_total = len(all_farm_tags) * len(extended_sex_acts) + sum(len(fix.acts) for fix in fix_dict.values())

            main_av_pics = main_div_score / main_cover_score if main_cover_score else 0
            op_av_pics = op_div_score / op_cover_score if op_cover_score else 0

            return {
                "main cover score": main_cover_score / main_cover_score_total,
                "main diversity average": main_av_pics,
                "optional cover score": op_cover_score / op_cover_score_total,
                "optional diversity average": op_av_pics,
            }

        # ── Picture refresh ──

        def refresh_pictures(self, force_default=False, silent=False):
            """Assign portrait and profile pictures based on girl's context."""
            g = self.girl

            # Phase 0.4: Invalidate picture cache for this girl on refresh
            PictureCache.evict(g)

            if force_default:
                g.portrait = get_pic(game, "portrait", "profile")
                g.profile = get_pic(game, "profile", "portrait", vertical=True)

            elif g in slavemarket.girls:
                g.portrait = g.get_pic("portrait", "profile", naked_filter=True, and_priority=False, soft=True)
                if g.naked:
                    g.profile = g.get_pic("market", "profile", "portrait", and_tags=["naked"], and_priority=False, not_tags=["beach", "nature", "date", "strip"], soft=True, vertical=True)
                elif persistent.naked_girls_in_slavemarket:
                    g.profile = g.get_pic("market", "profile", "portrait", not_tags=["beach", "nature", "date"], soft=True, vertical=True)
                else:
                    g.profile = g.get_pic("market", "profile", "portrait", not_tags=["naked", "beach", "nature", "date"], soft=True, vertical=True)

            elif g in game.free_girls:
                if persistent.naked_girls_in_town and g.naked:
                    _and_tags = ["naked"]
                    _not_tags = ["masseuse", "waitress", "dancer", "strip"]
                else:
                    _and_tags = []
                    _not_tags = ["naked", "masseuse", "waitress", "dancer"]

                g.portrait = g.get_pic("portrait", "profile", and_tags=_and_tags, not_tags=_not_tags, and_priority=False, soft=True)
                if g.location.lower() in town_locations:
                    g.profile = g.get_pic("profile", "portrait", and_tags=_and_tags + ["town"], not_tags=_not_tags + ["beach", "nature"], soft=True, vertical=True)
                elif g.location.lower() in beach_locations:
                    g.profile = g.get_pic("profile", "portrait", and_tags=_and_tags + ["beach"], not_tags=_not_tags + ["town", "nature"], soft=True, vertical=True)
                elif g.location.lower() in nature_locations:
                    g.profile = g.get_pic("profile", "portrait", and_tags=_and_tags + ["nature"], not_tags=_not_tags + ["town", "beach"], soft=True, vertical=True)
                elif g.location.lower() in court_locations:
                    g.profile = g.get_pic("date", "geisha", "profile", and_tags=_and_tags + ["profile"], not_tags=_not_tags + ["beach", "nature"], soft=True, vertical=True)
                else:
                    g.profile = g.get_pic("profile", "portrait", and_tags=_and_tags, not_tags=_not_tags, soft=True)

            else:  # Brothel girls
                not_tags = ["rest", "wet", "beach", "public"] + [j for j in all_jobs if j != g.job]
                g.portrait = g.get_pic("portrait", "profile", naked_filter=True, and_priority=False, soft=True)
                g.profile = g.get_pic("profile", "portrait", not_tags=not_tags, naked_filter=True, soft=True, vertical=True)

            if not g.profile:
                renpy.say("", __("{color=[c_bad]}No profile or portrait picture could be found for the following girl: %s.{/color}\nPlease rename at least one of her pictures to include the words 'profile' or 'portrait'\n(e.g.: 'profile3.webp')\nAlternatively, completely delete her directory, restart the game and then go to the Help Menu and 'Repair Girl/MC Pictures' to remove her.") % g.path)
                g.profile = Picture(path="resources/backgrounds/not_found.webp")

            if not g.portrait:
                g.portrait = Picture(path="resources/backgrounds/not_found.webp")

            # Auto-unlock CGs for gallery
            unlock_pic(g.portrait.path, silent=True)
            unlock_pic(g.profile.path, silent=True)

            g.create_char()

        # ── AutoRepair ──

        def check_pictures(self):
            """Verify portrait and profile still exist. Refresh if not."""
            g = self.girl
            if g.portrait is None or not GirlFilesDict.contains_file(g.path, g.portrait.path):
                self.refresh_pictures(silent=True)
            elif g.profile is None or not GirlFilesDict.contains_file(g.path, g.profile.path):
                self.refresh_pictures(silent=True)

        # ── Character creation ──

        def create_char(self):
            """Create the Ren'Py Character for dialogue display."""
            g = self.girl
            if g.init_dict.get("identity/game_character"):
                g.char = g.init_dict["identity/game_character"]
            elif g.portrait is not None:
                g.char = Character(g.name, color=c_pink, window_left_padding=wl_padding, show_side_image=g.portrait.get(side=True))
            else:
                g.char = Character(g.name, color=c_pink)

        # ── Picture lookup helpers ──

        @staticmethod
        def _get_pic_by_name(girl, filename):
            """Find a picture by filename in the girl's pack."""
            return GirlFilesDict.get_pic_by_name(girl.path, filename)

        @staticmethod
        def load_pics():
            """No-op: picture loading moved to GirlFilesDict."""
            pass

        # ── Picture lookup (delegated from Girl) ──

        def get_pic_by_name(self, filename):
            return GirlFilesDict.get_pic_by_name(self.girl.path, filename)

        def get_fix_pic(self, act=None, fix=None, and_tags=None, not_tags=None, hide_farm=True, naked_filter=False, pref_filter=True, attempts=0, allow_lesbian=False, always_stock=False, strict=False):
            """Find a picture matching a fixation + sex act combination."""
            g = self.girl

            if is_string(fix):
                fix = fix_dict[fix]

            if not fix:
                raise AssertionError("No fixation provided for picture.")

            # Prepare tags
            if and_tags:
                and_tags = make_list(and_tags)
            else:
                and_tags = []
            if not_tags:
                not_tags = make_list(not_tags)
            else:
                not_tags = []

            if hide_farm:
                not_tags += farm_hardcore_acts
                if not persistent.fuzzy_tagging_acts:
                    not_tags.append("big")
                    not_tags.append("machine")
                elif act != "fetish":
                    not_tags.append("machine")

            if act not in ("bisexual", "group"):
                not_tags += ["bisexual", "group"]
            elif act == "bisexual":
                not_tags.append("group")

            if act == "naked":
                not_tags += all_sex_acts

            if not allow_lesbian and act not in ("bisexual", "group") and "lesbian" not in (and_tags + not_tags):
                not_tags.append("lesbian")

            not_tags.extend(ntag for ntag in fix.not_list if ntag not in not_tags)

            # Build search settings
            and_not_settings = []
            if act:
                and_not_settings.append(["act-based", list(and_tags) + [act], list(not_tags)])
                if fix.name != "public acts":
                    and_not_settings.append(["generic", list(and_tags), list(not_tags) + opposite_sex_acts[act]])
            else:
                and_not_settings.append(["generic", list(and_tags), list(not_tags)])

            pics = []
            pics_second = []

            for _context, _and_tags, _not_tags in and_not_settings:
                for tags in fix.tag_list:
                    _tags = make_list(tags)
                    pic = g.get_pic(_tags, and_tags=_and_tags, not_tags=_not_tags, strict=True, naked_filter=naked_filter, pref_filter=pref_filter, always_stock=always_stock)
                    if pic:
                        pics.append((pic, pic.get_weight(_context)))
                        break
                else:
                    for tags in fix.tag_list:
                        attempts += 1
                        pic = g.get_pic(tags, and_tags=_and_tags, not_tags=_not_tags, attempts=attempts, naked_filter=naked_filter, pref_filter=pref_filter, always_stock=always_stock)
                        if pic:
                            pics_second.append((pic, pic.get_weight()))

            attempts = game.last_pic["attempts"]

            if pics:
                return weighted_choice(pics)
            elif strict:
                return None
            elif pics_second:
                return weighted_choice(pics_second)
            elif act:
                if act in extended_sex_acts and fix.name != "cosplay":
                    pic = g.get_pic(act, "naked", "profile", and_tags=and_tags, not_tags=not_tags, attempts=attempts, naked_filter=False, pref_filter=pref_filter, always_stock=always_stock)
                else:
                    pic = g.get_pic(act, "profile", and_tags=and_tags, not_tags=not_tags, attempts=attempts, naked_filter=naked_filter, pref_filter=pref_filter, always_stock=always_stock)
                if pic:
                    return pic

            return g.get_pic("profile", and_tags=and_tags, not_tags=not_tags, attempts=attempts, naked_filter=naked_filter)

        # ── 标签搜索 | Tag-based picture search ──

        def get_pic(self, tags, alt_tags1=None, alt_tags2=None, alt_tags3=None, and_tags=None, not_tags=None, strict=False, and_priority=True, naked_filter=False, attempts=0, soft=False, hide_farm=False, pref_filter=False, allow_lesbian=False, always_stock=False, horizontal=False, vertical=False):
            '''按标签查找图片 | Find a picture by tags (tries alt_tags in order; and/not_tags dropped in reverse priority order)'''
            g = self.girl

            # First looks for a pic with 'tags', then 'alt_tags1' if no pic is found, then 'alt_tags2'...
            # The 'and' and 'not_tags' apply to every set of tags.
            # NEW: and_tags and not_tags should be listed from the most important to the least important (they will be dropped in reverse order)
            # If 'strict' is on, a False value is returned if no picture can be found with the and/not_tags conditions
            # If 'and_priority' is on, the 'and' and 'not' clause will only be dropped after the search list has been exhausted
            # allow_lesbian is overridden by bisexual/group or using lesbian tag

            tags = make_list(tags)
            if and_tags:
                and_tags = make_list(and_tags)
            else:
                and_tags = []
            if not_tags:
                not_tags = make_list(not_tags)
            else:
                not_tags = []

            ## 优先级过滤器：优先于传入的 not_tags，重要性递增 | Priority filters: take precedence over provided not_tags, in ascending order of importance

            # 'naked_filter' 自动加入 naked 标签（仅用于 profile/rest/work 图，慎用于性事件）| 'naked_filter' automatically adds the naked tag (use only with profile, rest, or work pics)

            if naked_filter and "naked" not in (tags + and_tags + not_tags): # 直接标签指令优先于 naked_filter | Direct tag orders take precedence over naked_filter
                if g.naked:
                    and_tags.append("naked")
                elif not g.naked:
                    not_tags.insert(0, "naked") # 将 "naked" 置于 not_tags 开头 | Places "naked" at the beginning of the not_tags list

            # 'Soft' 自动排除性标签（不排除 naked/农场标签）| 'Soft' automatically excludes sexual tags (keeps naked/farm tags without sexual tags)

            if soft: # 将 soft 过滤器插入 not_tags 开头 | Inserts soft filters at the beginning of the not_tags list
                not_tags = [ntag for ntag in (all_sex_acts + ["group", "bisexual", "cumshot"]) if ntag not in not_tags] + not_tags

            # 除非明确请求或上下文为 bisexual/group，否则排除 lesbian 图 | Lesbian pics excluded unless explicitly requested or context is bisexual/group

            if not allow_lesbian and "lesbian" not in (tags + and_tags + not_tags) and "bisexual" not in (tags + and_tags) and "group" not in (tags + and_tags):
                not_tags.insert(0, "lesbian") # 将 "lesbian" 置于 not_tags 开头 | Places "lesbian" at the beginning of the not_tags list

            # 处女女孩不显示性行为图片，除非明确为 'sex' 或 'group' | 'Virgin' girls never have sex pics shown unless the act is explicitly 'sex' or 'group'

            if g.has_trait("Virgin"):
                if not "sex" in (tags + and_tags + not_tags) and not "group" in (tags + and_tags):
                    not_tags.insert(0, "sex") # 将 "sex" 置于 not_tags 开头 | Places "sex" at the beginning of the not_tags list

            # 'Hide_farm' 排除硬核农场行为，优先级最高 | 'Hide_farm' excludes hardcore farm acts, takes precedence over everything else
            if hide_farm:
                if not persistent.fuzzy_tagging_acts: # 非农场搜索禁用 machine 和 big | Disables machine and big for all non farm picture search
                    not_tags.insert(0, "machine") # 将 "machine" 置于 not_tags 开头 | Places "machine" at the beginning of the not_tags list
                    not_tags.append("big")
                elif "fetish" not in (tags + and_tags):
                    not_tags.insert(0, "machine") # 将 "machine" 置于 not_tags 开头 | Places "machine" at the beginning of the not_tags list
                not_tags = farm_hardcore_acts + not_tags

            ## 非优先级过滤器（追加到 not_tags 末尾）| Non-priority filters (added at the end of the not_tags list)

            # 'portrait' 仅在明确请求时显示 | 'portrait' may not show unless specifically requested

            if "portrait" not in (tags + and_tags + not_tags):
                not_tags.append("portrait")

            # 'pref_filter' 过滤掉女孩不感兴趣的行为标签 | 'pref_filter' filters out sex acts she isn't at least indifferent to

            if pref_filter:
                not_tags += [a for a in all_sex_acts if (not a in (tags + and_tags + not_tags) and not compare_preference(g, a, "indifferent"))]

            # 附加过滤器（欲望/心情）| Additional filters (libido/mood)

            if g.get_stat("libido") < 75 and "libido" not in (tags + and_tags + not_tags): # 欲望过低不出 libido 标签 | Libido tags won't happen if girl's libido is too low
                not_tags.append("libido")
            if g.mood > 0 and g.get_love() - g.get_fear() > 0 and "sad" not in not_tags: # 开心且被爱时不出现 sad 标签 | Sad tags won't happen if girl is happy and loving
                not_tags.append("sad")
            if g.mood < 0 or g.get_love() - g.get_fear() < 0 and "happy" not in not_tags: # 悲伤或恐惧时不出现 happy 标签 | Happy tags won't happen if girl is sad or in fear
                not_tags.append("happy")
            if g.mood >= 15 or g.mood <= -15 or g.get_love() - g.get_fear() >= 15 or g.get_love() - g.get_fear() <= -15: # 情绪激烈时不出现 neutral 标签 | Neutral tags won't happen on strong emotions
                if "neutral" not in not_tags:
                    not_tags.append("neutral")

            # 调用全局 get_pic 执行实际搜索 | Call the global get_pic to perform the actual search
            return get_pic(g, tags=tags, alt_tags1=alt_tags1, alt_tags2=alt_tags2, alt_tags3=alt_tags3, and_tags=and_tags, not_tags=not_tags, strict=strict, and_priority=and_priority, attempts=attempts, always_stock=always_stock, horizontal=horizontal, vertical=vertical)

        def get_pic_not_tags(self, tags, alt_tags1=None, alt_tags2=None, alt_tags3=None, and_tags=None, not_tags=None, strict=False, and_priority=True, naked_filter=False, attempts=0, soft=False, hide_farm=False, pref_filter=False, allow_lesbian=False, always_stock=False):
            '''按标签排除查找图片（get_pic 的 not_tags 变体）| Find a picture by tags (not_tags variant of get_pic)'''
            g = self.girl

            # First looks for a pic with 'tags', then 'alt_tags1' if no pic is found, then 'alt_tags2'...
            # The 'and' and 'not_tags' apply to every set of tags.
            # NEW: and_tags and not_tags should be listed from the most important to the least important (they will be dropped in reverse order)
            # If 'strict' is on, a False value is returned if no picture can be found with the and/not_tags conditions
            # If 'and_priority' is on, the 'and' and 'not' clause will only be dropped after the search list has been exhausted
            # allow_lesbian is overridden by bisexual/group or using lesbian tag

            tags = make_list(tags)
            if and_tags:
                and_tags = make_list(and_tags)
            else:
                and_tags = []
            if not_tags:
                not_tags = make_list(not_tags)
            else:
                not_tags = []

            ## 优先级过滤器：优先于传入的 not_tags，重要性递增 | Priority filters: take precedence over provided not_tags, in ascending order of importance

            # 'naked_filter' 自动加入 naked 标签（仅用于 profile/rest/work 图，慎用于性事件）| 'naked_filter' automatically adds the naked tag (use only with profile, rest, or work pics)

            if naked_filter and "naked" not in (tags + and_tags + not_tags): # 直接标签指令优先于 naked_filter | Direct tag orders take precedence over naked_filter
                if g.naked:
                    and_tags.append("naked")
                elif not g.naked:
                    not_tags.insert(0, "naked") # 将 "naked" 置于 not_tags 开头 | Places "naked" at the begining of the not_tags list

            # 'Soft' 自动排除性标签（不排除 naked/农场标签）| 'Soft' automatically excludes sexual tags (keeps naked/farm tags without sexual tags)

            if soft: # 将 soft 过滤器插入 not_tags 开头 | Inserts soft filters at the beginning of the not_tags list
                not_tags = [ntag for ntag in (all_sex_acts + ["group", "bisexual", "cumshot"]) if ntag not in not_tags] + not_tags

            # 除非明确请求或上下文为 bisexual/group，否则排除 lesbian 图 | Lesbian pics excluded unless explicitly requested or context is bisexual/group

            if not allow_lesbian and "lesbian" not in (tags + and_tags + not_tags) and "bisexual" not in (tags + and_tags) and "group" not in (tags + and_tags):
                not_tags.insert(0, "lesbian") # 将 "lesbian" 置于 not_tags 开头 | Places "lesbian" at the beginning of the not_tags list

            # 处女女孩不显示性行为图片，除非明确为 'sex' 或 'group' | 'Virgin' girls never have sex pics shown unless the act is explicitly 'sex' or 'group'

            if g.has_trait("Virgin"):
                if not "sex" in (tags + and_tags + not_tags) and not "group" in (tags + and_tags):
                    not_tags.insert(0, "sex") # 将 "sex" 置于 not_tags 开头 | Places "sex" at the beginning of the not_tags list

            # 'Hide_farm' 排除硬核农场行为，优先级最高 | 'Hide_farm' excludes hardcore farm acts, takes precedence over everything else
            if hide_farm:
                if not persistent.fuzzy_tagging_acts: # 非农场搜索禁用 machine 和 big | Disables machine and big for all non farm picture search
                    not_tags.insert(0, "machine") # 将 "machine" 置于 not_tags 开头 | Places "machine" at the beginning of the not_tags list
                    not_tags.append("big")
                elif "fetish" not in (tags + and_tags):
                    not_tags.insert(0, "machine") # 将 "machine" 置于 not_tags 开头 | Places "machine" at the beginning of the not_tags list
                not_tags = farm_hardcore_acts + not_tags

            ## 非优先级过滤器（追加到 not_tags 末尾）| Non-priority filters (added at the end of the not_tags list)

            # 'portrait' 仅在明确请求时显示 | 'portrait' may not show unless specifically requested

            if "portrait" not in (tags + and_tags + not_tags):
                not_tags.append("portrait")

            # 'pref_filter' 过滤掉女孩不感兴趣的行为标签 | 'pref_filter' filters out sex acts she isn't at least indifferent to

            if pref_filter:
                not_tags += [a for a in all_sex_acts if (not a in (tags + and_tags + not_tags) and not compare_preference(g, a, "indifferent"))]

            # 附加过滤器（欲望/心情）| Additional filters (libido/mood)

            if g.get_stat("libido") < 75 and "libido" not in (tags + and_tags + not_tags): # 欲望过低不出 libido 标签 | Libido tags won't happen if girl's libido is too low
                not_tags.append("libido")
            if g.mood > 0 and g.get_love() - g.get_fear() > 0 and "sad" not in not_tags: # 开心且被爱时不出现 sad 标签 | Sad tags won't happen if girl is happy and loving
                not_tags.append("sad")
            if g.mood < 0 or g.get_love() - g.get_fear() < 0 and "happy" not in not_tags: # 悲伤或恐惧时不出现 happy 标签 | Happy tags won't happen if girl is sad or in fear
                not_tags.append("happy")
            if g.mood >= 15 or g.mood <= -15 or g.get_love() - g.get_fear() >= 15 or g.get_love() - g.get_fear() <= -15: # 情绪激烈时不出现 neutral 标签 | Neutral tags won't happen on strong emotions
                if "neutral" not in not_tags:
                    not_tags.append("neutral")

            return and_text(not_tags)
