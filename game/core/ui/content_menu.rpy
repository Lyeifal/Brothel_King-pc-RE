###### Game settings menu (formerly H content) ######

#### Default values ####

default persistent.fix_pic_balance = fix_pic_balance_variety # Sets weights for the 'get_fix_pic()' Girl method

default persistent.forbidden_tags = []

default persistent.use_stock_pictures_missing = False
default persistent.use_stock_pictures_low = False

default persistent.show_girlpack_rating = None

default persistent.mix_group_pictures = False
default persistent.mix_bis_pictures = False

default persistent.naked_girls_in_slavemarket = False
default persistent.naked_girls_in_town = False

default persistent.fuzzy_tagging_jobs = True
default persistent.fuzzy_tagging_acts = True

default persistent.home_screen_notifications = 0 # 0 = default, 1 = no flashing, 2 = n notification

default persistent.show_girl_status = {"away": True, "farm": True, "rest": True, "scheduled": False, "half-shift": True, "master bedroom": True, "work&whore": True, "not work&whore": False, "naked": True, "not naked": False, "negative fixation": True}

default persistent.badges_on_portraits = False

default persistent.skipped_events = defaultdict(bool)
default persistent.can_skip_reports = False
default persistent.can_skip_night_recap = False

default persistent.keep_firstname = False
default persistent.keep_lastname = False
default persistent.gp_name_customization = False

default persistent.dark_night_UI = False

default persistent.sanity_display = False

default persistent.girls_display_mode = "pages"

define persistent.hover_for_preview_girls = True # Toggles hover preview in all screens using girls
define persistent.hover_for_preview_postings = True # Toggles hover preview in postings


#### Game menu creation ####

init python:
    class HMSetting(object):
        """A basic setting for the H menu"""

        def __init__(self, variable, captions=None, ttips=None, values=(False, True), range=2, special=False):
            self.variable = variable
            self.captions = captions or [__("OFF"), __("ON")]
            self.ttips = ttips or [__("OFF"), __("ON")]
            self.values = values
            self.range = range
            self.special = special

        def toggle(self):
            idx = self.get_index()

            if idx < self.range-1:
                setattr(persistent, self.variable, self.values[idx+1])
            else:
                setattr(persistent, self.variable, self.values[0])

        def get(self):
            return getattr(persistent, self.variable)

        def get_index(self):
            return self.values.index(self.get())

        def caption(self):
            return self.captions[self.get_index()]

        def tooltip(self):
            return self.ttips[self.get_index()]



default hm_sections = ["content", "pictures", "UI", "misc"]
default hm_section_titles = {"content": __("Content settings"), "pictures": __("Picture settings"), "UI": __("UI settings"), "misc": __("Other")}

# HM settings will be displayed in order for each section
# 说明文字与选项/提示文本在定义处包裹 __()：显示处经 _(变量) 运行时再查表，字面量必须先进入翻译表
# Descriptions/captions/tooltips are wrapped at definition with __(): display sites re-translate via _(var), so literals must be registered first
default hm_settings = {
    "content" : [
            __("Activate or deactivate objectionable content (won't affect story scenes)."),
            HMSetting("forbidden_tags", special=True),
        ],
        "pictures" : [
            __("Choose what to do when a girlpack is missing pictures with a given tag."),
            HMSetting("use_stock_pictures_missing", captions=[__("Use another picture from the girl pack"), __("Use default pictures")], ttips=[__("The game will pick a picture from the same girlpack with the closest possible tag (e.g. 'service' instead of 'handjob')."), __("The game will pick a default picture with the proper tag.")]),

            __("Choose what to do when a girlpack has low picture variety on a given tag (less than %s).") % stock_picture_threshold,
            HMSetting("use_stock_pictures_low", captions=[__("Only use girl pack pictures"), __("Mix default and girl pack pictures")], ttips=[__("The game will use only the girlpack pictures that are in the pool, at the risk of repetition."), __("The game will add some default pictures to the pool for variety.")]),

            __("Choose the priorities when generating pictures for advanced training."),
            HMSetting("fix_pic_balance", [__("Variety over accuracy"), __("Accuracy over variety")], ttips=[__("The game will prioritize picture variety over accurate tagging."), __("The game will prioritize accurate tagging over picture variety.")], values=[fix_pic_balance_variety, fix_pic_balance_accuracy]),

            __("Choose the behavior of group and bisexual pictures"),
            HMSetting("mix_group_pictures", [__("Group sex: Only use group pictures"), __("Mix group pictures with regular pictures")], ttips=[__("The game will only pick pictures featuring a group."), __("The game will sometimes pick normal pictures for variety.")]),
            HMSetting("mix_bis_pictures", [__("Bisexual sex: Only use bisexual pictures"), __("Mix bisexual pictures with regular pictures")], ttips=[__("The game will only pick pictures featuring a group."), __("The game will sometimes pick normal pictures for variety.")]),

            __("Choose the behavior of profile pictures outside of the 'Girls' tab."),
            HMSetting("naked_girls_in_slavemarket", [__("Slavemarket: No naked pictures."), __("Slavemarket: Allow naked pictures.")], ttips=[__("The slavemarket may not display naked profile pictures."), __("The slavemarket may display naked pictures.")]),
            HMSetting("naked_girls_in_town", [__("City: No naked pictures."), __("City: Allow naked pictures.")], ttips=[__("Free girls may not display naked profile pictures."), __("Free girls may display naked pictures ('Naturist' trait).")]),

            __("Allow extended tags for jobs and sex acts."),
            HMSetting("fuzzy_tagging_jobs", [__("Jobs: Narrow tagging"), __("Jobs: Extended tagging")], ttips=[__("Job pictures will only look for accurate tags (e.g. 'masseuse' for masseuse)."), __("Job pictures will extend the search to 'close enough' tags (e.g. 'swimsuit' for masseuse).")]),
            HMSetting("fuzzy_tagging_acts", [__("Sex acts: Narrow tagging"), __("Sex acts: Extended tagging")], ttips=[__("Sex pictures will only look for accurate tags (e.g. 'toy' for fetish)."), __("Job pictures will extend the search to 'close enough' tags (e.g. 'machine' for fetish).")]),
        ], 
        "UI" : [
            __("Display 'news' notifications next the home screen's buttons."),
            HMSetting("home_screen_notifications", [__("Flashing notifications"), __("Static notifications"), __("No notifications")], ttips=[__("Display a flashing notification until you hover the mouse over it (default)."), __("Display a static notification."), __("Display no notification.")], range=3, values=range(3)),

            __("Use a scrollable screen or numbered tabs to browse the 'Girls' screen (tabs may improve performance)."),
            HMSetting("girls_display_mode", [__("Scroll girls"), __("Use tabs")], ttips=[__("Display girls on a signle scrollable screen (legacy mode: may decrease performance)."), __("Display girls with numbered tabs (may improve performance).")], range=2, values=["vp", "pages"]),

            __("Display girlpack rating on girl profiles"),
            HMSetting("show_girlpack_rating", [__("Never"), __("In slavemarket"), __("In slavemarket/City"), __("Everywhere")], ttips=[__("Never display girlpack rating on profile."), __("Display rating on profile in slavemarket only."), __("Display rating on profile in slavemarket and city."), __("Always display rating on profile.")], values = [None, "In slavemarket", "In market and city", "Everywhere"], range=4),

            __("Preview when hovering"),
            HMSetting("hover_for_preview_girls", [__("Do not preview girls"), __("Preview girls")], ttips=[__("You will not see a girl's profile when hovering over her button."), __("You will see a girl's profile when hovering over her button.")]),
            HMSetting("hover_for_preview_postings", [__("Do not preview quests/classes"), __("Preview quests/classes")], ttips=[__("You will not see a class or quest's profile when hovering over its button."), __("You will see a class or quest's profile when hovering over its button.")]),

            __("Display optional status icons on girl portraits."),
            HMSetting("show_girl_status", special=True),

            __("Display sanity with a girl's mood."),
            HMSetting("sanity_display", [__("In farm only"), __("Everywhere")], ttips=[__("Sanity will only display when a girl is at the farm."), __("Sanity will be displayed on the 'Mood' recap.")]),

            __("Choose how to edit badge settings for your girls."),
            HMSetting("badges_on_portraits", [__("On profile only"), __("On profile and portrait")], [__("Click on a badge in the girl's profile to change it."), __("Click on a badge in the girl's profile or portrait to change it.")]),

            __("Hide events during the 'End Day' loop."),
            HMSetting("skipped_events", special=True),

            __("Allow skipping during the 'End Day' loop."),
            HMSetting("can_skip_reports", [__("Reports: Not skippable"), __("Reports: Skippable")], ttips=[__("Skipping matchmaking and satisfaction reports with 'Ctrl' is not possible."), __("Skipping matchmaking and satisfaction reports with 'Ctrl' is possible.")]),
            HMSetting("can_skip_night_recap", [__("Nightly recap: Not skippable"), __("Nightly recap: Skippable")], ttips=[__("Skipping the nightly recap with 'Ctrl' is not possible."), __("Skipping the nightly recap with 'Ctrl' is possible.")]),

            __("Choose display mode for 'End Day' events (WIP)."),
            HMSetting("dark_night_UI", [__("Light mode"), __("Dark mode")], ttips=[__("End day events are presented in light mode."), __("End day events are presented in dark mode.")]),


        ],
        "misc" : [
            __("Define naming options for non-original girls ('clones')."),
            HMSetting("keep_firstname", [__("Randomize first name"), __("Keep first name")], ttips=[__("First name will be randomized for non-original girls."), __("First name will be remain the same as the original for non-original girls.")]),
            HMSetting("keep_lastname", [__("Randomize last name"), __("Keep last name")], ttips=[__("Last name will be randomized for non-original girls."), __("Last name will be remain the same as the original for non-original girls.")]),
            HMSetting("gp_name_customization", [__("Prioritize girlpack settings"), __("Prioritize in-game settings")], ttips=[__("The girlpack's _BK.ini settings will take precedence over the settings above."), __("The settings above will take precedence over the girlpack's _BK.ini settings.")]),
        ]
        }

default hm_tag_captions = {"beast" : __("Bestiality"), "monster" : __("Monsters/Tentacles"), "machine" : __("Machines")}

default hm_girl_status_list = [("away", "away.webp", __("Away on a class or quest.")), ("farm", "farm.webp", __("Training/Resting at the farm.")), ("rest", "rest.webp", __("Resting")), ("scheduled", "scheduled.webp", __("Scheduled to rest.")), ("half-shift", "half.webp", __("On a half-shift.")), ("master bedroom", "master.webp", __("Training in the Master's bedroom.")), ("negative fixation", "negfix.webp", __("Negative fixation discovered.")), ("naked", "naked.webp", __("Currently naked.")), ("not naked", "not_naked.webp", __("Currently not naked.")), ("work&whore", "ww.webp", __("Set to work and whore.")), ("not work&whore", "not_ww.webp", __("Not set to work and whore"))]

# 元组为 (内部key, 按钮显示文本, 提示文本)：key 必须保持英文，因 persistent.skipped_events 与 endday/events_dispatcher 以这些 key 索引
# Tuples are (internal key, button label, tooltip): keys must stay English (persistent.skipped_events indexed by them in endday/events_dispatcher)
default hm_night_events = [("Normal", __("Normal"), __("Normal events")), ("Matchmaking", __("Matchmaking"), __("Matchmaking reports")), ("Customer", __("Customer"), __("Customer special events")), ("Level/Job/Rank up", __("Level/Job/Rank up"), __("Level up, Job up and Rank up notifications")), ("Health/Security", __("Health/Security"), __("Health and security events")), ("Satisfaction", __("Satisfaction"), __("Customer satisfaction report")), ("Farm", __("Farm"), __("Farm events")), ("Rest", __("Rest"), __("Resting events"))]

#### Game Settings Screen ####

screen hm_forbidden_tags():
    hbox:
        for _tag in ("beast", "monster", "machine"):
            if _tag in persistent.forbidden_tags:
                $ text1 = __("OFF")
            else:
                $ text1 = __("ON")

            textbutton _("%s: %s") % (hm_tag_captions[_tag], text1):
                style "hm_button2"
                size_group "forbidden_tags"
                xpadding xres(18)
                xsize xres(190)

                if _tag in persistent.forbidden_tags:
                    action (RemoveFromSet(persistent.forbidden_tags, _tag), SelectedIf(False))
                    tooltip _("The game will attempt not to display such pictures (Warning: This may not be 100% successful and doesn't change story events that use these fetishes.)")
                else:
                    action (AddToSet(persistent.forbidden_tags, _tag), SelectedIf(True))
                    tooltip _("The game will display such pictures.")

screen hm_girl_statuses():
    default current_status = ""

    hbox spacing xres(12):
        hbox box_wrap True spacing xres(6):
            style_group None
            for status, pic, ttip in hm_girl_status_list:
                button action ToggleDict(persistent.show_girl_status, status) tooltip ttip:
                    if persistent.show_girl_status[status]:
                        background Frame("lightblue_button", borders=gui.button_borders)
                        add ProportionalScale("resources/ui/status/" + pic, *res_tb(30))

                    else:
                        background Frame("lightgrey_button", borders=gui.button_borders)
                        add ProportionalScale("resources/ui/status/" + pic, *res_tb(30), matrixcolor=SaturationMatrix(0))

screen hm_skip_night_events():
    hbox box_wrap True:
        for ev_key, ev_label, ttip in hm_night_events:
            textbutton _(ev_label) style "hm_button2" text_size res_font(16) xalign 0.0 action (ToggleDict(persistent.skipped_events, ev_key), SelectedIf(not persistent.skipped_events[ev_key])) tooltip ttip + {False: __(" will be shown."), True: __(" will be hidden.")}[persistent.skipped_events[ev_key]]


screen h_content(): # H preferences and various game settings

    tag menu

    use game_menu(_("Game settings"), scroll="viewport"):

        frame xfill True style "pref_frame":
            has vbox xfill True
            style_group "hm"

            for section in hm_sections:
                label _(hm_section_titles[section]) text_bold True

                for setting in hm_settings[section]:
                    if is_string(setting):
                        text _("\n%s") % setting
                    elif setting.special: # Custom buttons that do not behave as toggleable objects
                        # Forbidden_tags
                        if setting.variable == "forbidden_tags":
                            use hm_forbidden_tags()
                        elif setting.variable == "show_girl_status":
                            use hm_girl_statuses()
                        elif setting.variable == "skipped_events":
                            use hm_skip_night_events()
                    else:
                        textbutton _(setting.caption()) action (Function(setting.toggle), SelectedIf(setting.get_index())) tooltip _(setting.tooltip()) xsize 0.5

                null height yres(20)
    
    use adv_tooltip()
                

#### HM styles ####

style hm_button:
    selected_background Frame("lightblue_button", borders=gui.button_borders)

style hm_text color c_brown italic True size res_font(16)

style hm_button2 is hm_button:
    idle_background Frame("lightgrey_button", borders=gui.button_borders)
    selected_idle_background Frame("darkorange_button", borders=gui.button_borders)
    # selected_foreground "tb empty"

style hm_button_text size res_font(18)

style hm_button2_text is hm_button_text:
    idle_color c_darkgrey
    selected_color c_white
    xalign 0.0


#### Depreciated ###

# screen h_content_old(): # H preferences and various player settings

#     tag menu

#     use game_menu(_("Game settings"), scroll="viewport"):

#         frame xfill True style "pref_frame":
#             has vbox xfill True

#             label _("Content settings") text_bold True

#             # Objectionable content

#             text "\nActivate or deactivate objectionable content (won't affect story scenes)" color c_brown italic True size res_font(16)

#             if "beast" in persistent.forbidden_tags:
#                 $ text1 = "OFF"
#             else:
#                 $ text1 = "ON"

#             textbutton _("Bestiality: " + text1) text_size res_font(18) xalign 0.0 xsize 0.8 xfill True:
#                 if "beast" in persistent.forbidden_tags:
#                     action RemoveFromSet(persistent.forbidden_tags, "beast")
#                 else:
#                     action AddToSet(persistent.forbidden_tags, "beast")

#             if "monster" in persistent.forbidden_tags:
#                 $ text1 = "OFF"
#             else:
#                 $ text1 = "ON"

#             textbutton _("Monsters/Tentacles: " + text1) text_size res_font(18) xalign 0.0 xsize 0.8 xfill True:
#                 if "monster" in persistent.forbidden_tags:
#                     action RemoveFromSet(persistent.forbidden_tags, "monster")
#                 else:
#                     action AddToSet(persistent.forbidden_tags, "monster")

#             if "machine" in persistent.forbidden_tags:
#                 $ text1 = "OFF"
#             else:
#                 $ text1 = "ON"

#             textbutton _("Machines: " + text1) text_size res_font(18) xalign 0.0 xsize 0.8 xfill True:
#                 if "machine" in persistent.forbidden_tags:
#                     action RemoveFromSet(persistent.forbidden_tags, "machine")
#                 else:
#                     action AddToSet(persistent.forbidden_tags, "machine")

#             text ""

#             label _("Picture settings") text_bold True

#             # Missing Picture algorithm

#             text "\nChoose the behavior of stock (default) pictures and girl pack pictures" color c_brown italic True size res_font(16)

#             if persistent.use_stock_pictures["missing"]:
#                 $ text1 = "When a picture is missing:\nUse stock pictures"
#             else:
#                 $ text1 = "When a picture is missing:\nUse another picture from the girl pack"

#             if persistent.use_stock_pictures["low"]:
#                 $ text2 = "When the picture count is low:\nMix stock and girl pack pictures"
#             else:
#                 $ text2 = "When the picture count is low:\nOnly use girl pack pictures"

#             textbutton text1 text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleDict(persistent.use_stock_pictures, "missing")
#             textbutton text2 text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleDict(persistent.use_stock_pictures, "low")

#             # Advanced Picture algorithm

#             text "\nChoose the behavior of advanced training pictures" color c_brown italic True size res_font(16)
#             if persistent.fix_pic_balance == fix_pic_balance_variety:
#                 textbutton "Advanced training pictures: Better variety" text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action SetField(persistent, "fix_pic_balance", fix_pic_balance_accuracy)
#             else:
#                 textbutton "Advanced training pictures: Better accuracy" text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action SetField(persistent, "fix_pic_balance", fix_pic_balance_variety)

#             # Group/Bis Picture algorithm

#             text "\nChoose the behavior of group and bisexual pictures" color c_brown italic True size res_font(16)
#             textbutton {True: "Group sex: Mix group pictures with regular pictures", False: "Group sex: Only use group sex pictures"}[persistent.mix_group_pictures] text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleField(persistent, "mix_group_pictures")
#             textbutton {True: "Bisexual sex: Mix bisexual pictures with regular pictures", False: "Bisexual sex: Only use bisexual pictures"}[persistent.mix_bis_pictures] text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleField(persistent, "mix_bis_pictures")

#             # Naked girls' settings


#             text "\nChoose the behavior of slavemarket girls' pictures" color c_brown italic True size res_font(16)
#             textbutton {True: "Allow naked pictures in the slavemarket", False: "No naked pictures in the market"}[persistent.naked_girls_in_slavemarket] text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleField(persistent, "naked_girls_in_slavemarket")

#             text "\nChoose the behavior of free girls' pictures" color c_brown italic True size res_font(16)
#             textbutton {True: "Allow naked pictures in the city (naturist trait)", False: "No naked pictures in the city"}[persistent.naked_girls_in_town] text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleField(persistent, "naked_girls_in_town")

#             # Fuzzy tagging
#             text "\nAllow 'close enough' tags to be used (e.g. 'swimsuit' for masseuse events)" color c_brown italic True size res_font(16)

#             hbox xalign 0.0 xsize 0.8:
#                 textbutton "For jobs: %s" % ({True: "ON", False: "OFF"}[persistent.fuzzy_tagging_jobs]) text_size res_font(18) xsize xres(312) action ToggleField(persistent, "fuzzy_tagging_jobs")
#                 textbutton "For sex acts: %s" % {True: "ON", False: "OFF"}[persistent.fuzzy_tagging_acts] text_size res_font(18) xsize xres(312) action ToggleField(persistent, "fuzzy_tagging_acts")

#             text ""

#             label _("UI settings") text_bold True

#             # Pack ratings

#             text "\nDisplay pack rating on girl profiles" color c_brown italic True size res_font(16)

#             if persistent.show_girlpack_rating:
#                 $ text1 = persistent.show_girlpack_rating
#             else:
#                 $ text1 = "OFF"

#             textbutton "Show Girl Pack Rating: [text1]" text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action SetField(persistent, "show_girlpack_rating", get_next([None, "In slavemarket", "In market and city", "Everywhere"], persistent.show_girlpack_rating, loop=True))

#             # Use flashing notifications

#             text "\nDisplay notifications next to buttons on the home screen" color c_brown italic True size res_font(16)

#             default notif_state = {0: "Flashing notifications (default)", 1: "Static notifications", 2: "No notifications"}

#             textbutton notif_state[persistent.home_screen_notifications] text_size res_font(18) xalign 0.0 xsize 0.8 xfill True: #?
#                 if persistent.home_screen_notifications <= 1:
#                     action SetField(persistent, "home_screen_notifications", persistent.home_screen_notifications+1)
#                 else:
#                     action SetField(persistent, "home_screen_notifications", 0)

#             # Show/Hide girl status

#             text "\nDisplay girl status icons" color c_brown italic True size res_font(16)

#             default current_status = ""

#             hbox spacing xres(12):
#                 hbox box_wrap True spacing xres(6):
#                     style_group None
#                     for status in [("away", "away.webp"), ("farm", "farm.webp"), ("rest", "rest.webp"), ("scheduled", "scheduled.webp"), ("half-shift", "half.webp"), ("master bedroom", "master.webp"), ("work&whore", "ww.webp"), ("naked", "naked.webp"), ("negative fixation", "negfix.webp"), ("not naked", "not_naked.webp"), ("not work&whore", "not_ww.webp")]:

#                         if status:
#                             button action ToggleDict(persistent.show_girl_status, status[0]) hovered SetScreenVariable("current_status", status[0]) unhovered SetScreenVariable("current_status", ""):
#                                 if persistent.show_girl_status[status[0]]:
#                                     background Frame("lightblue_button", borders=gui.button_borders)
#                                     add ProportionalScale("resources/ui/status/" + status[1], *res_tb(30))

#                                 else:
#                                     add ProportionalScale("resources/ui/status/" + status[1], *res_tb(30), matrixcolor=SaturationMatrix(0))

#                 if current_status:
#                     text "%s\n(%s)" % (current_status.capitalize(), {True : "active", False : "inactive"}[persistent.show_girl_status[current_status]]) bold True size res_font(14) color c_prune yalign 0.5

#             # Badge settings

#             text "\nYour preferences for setting girl badges" color c_brown italic True size res_font(16)
#             textbutton {True: "Badges can be modified directly on girls' portraits", False: "Badges can only be modified on a girl's profile"}[persistent.badges_on_portraits] text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleField(persistent, "badges_on_portraits")

#             # Night events settings

#             text "\nShow/Skip night events" color c_brown italic True size res_font(16)

#             for ev_type in ["Normal", "Matchmaking", "Customer", "Level/Job/Rank up", "Health/Security", "Satisfaction report", "Farm", "Rest"]:

#                 $ text1 = ev_type

#                 if ev_type != "Satisfaction report":
#                     $ text1 += " events"

#                 if persistent.skipped_events[ev_type]:
#                    $ text1 += ": OFF"
#                 else:
#                    $ text1 += ": ON"

#                 textbutton _(text1) text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleDict(persistent.skipped_events, ev_type)

#             textbutton "Block skipping on night reports: " + {True: "OFF", False: "ON"}[persistent.can_skip_reports] text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleField(persistent, "can_skip_reports")
#             textbutton "Block skipping on final recap: " + {True: "OFF", False: "ON"}[persistent.can_skip_night_recap] text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleField(persistent, "can_skip_night_recap")

#             text ""

#             label _("Misc") text_bold True

#             # Naming options for clones

#             text "\nChoose naming options for non-original girls" color c_brown italic True size res_font(16)

#             $ switch_caption = {True: "YES", False: "NO"}

#             textbutton "Keep First Name: %s" % switch_caption[persistent.keep_firstname] text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleField(persistent, "keep_firstname")
#             textbutton "Keep Last Name: %s" % switch_caption[persistent.keep_lastname] text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleField(persistent, "keep_lastname")
#             textbutton "Prioritize _BK.ini clone name settings (when available): %s" % switch_caption[persistent.gp_name_customization] text_size res_font(18) xalign 0.0 xsize 0.8 xfill True action ToggleField(persistent, "gp_name_customization")

            # End of menu