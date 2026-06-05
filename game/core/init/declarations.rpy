####            CHARACTER AND IMAGE DECLARATIONS                ####
##      All BKing character, image and transition declarations    ##
##              Includes the code for the CG Gallery              ##
####                                                            ####

## Removing black or white background from jpg with paint.net (so I don't forget):
## Select black or white area, delete, use Object / 'old feather' or feather effect then Photo / Sharpen effect

####                            ####
##      CHARACTER DECLARATION     ##
####                            ####

# Declare characters used by this game.

#### INTRO ####

## SYSTEM ##

define wl_padding = int(config.screen_height*0.21)
define bk_error = Character(_("ERROR"), color=c_red)

# Special emoji characters not supported by the new font
define emo_heart = "{font=resources/fonts/DejaVuSans.ttf}❤{/font}"
define emo_broken_heart = "💔"
define emo_lightning = "{font=resources/fonts/DejaVuSans.ttf}⚡{/font}"
define emo_yang = "{font=resources/fonts/DejaVuSans.ttf}☯{/font}"

## MC ##
define you = DynamicCharacter("MC.name", color=c_main)


## SILL ##
define sill = DynamicCharacter("sill_name", color=c_hotpink, image = "sill", window_left_padding=wl_padding) #show_two_window=True,


## KUROHIME ##
define kuro = DynamicCharacter("kuro_name", color = c_lightprune, image = "kuro", window_left_padding=wl_padding)
define kurohime = kuro


## MAID ##
define maid = DynamicCharacter("maid_name", color = c_softpurple, image = "maid", window_left_padding=wl_padding)


## GIO ##
define gio = Character(_("Gio"), color = c_orange, image = "gio", window_left_padding=wl_padding)


## MISC ##
define guard = Character(_("Guard"), color= c_yellow, image = "guard", window_left_padding=wl_padding)
define thug1 = Character(_("Thug"), color= c_lightgreen, image = "thug1", window_left_padding=wl_padding)
define thug2 = Character(_("Thug"), color= c_red, image = "thug2", window_left_padding=wl_padding)
define thug3 = Character(_("Thug"), color= c_lightred, image = "thug", window_left_padding=wl_padding)
define drogon = Character(_("Drogon"), color= c_darkred, image = "drogon", window_left_padding=wl_padding)
define security = Character(_("Security"), color= c_white, image = "security", window_left_padding=wl_padding)
define security_breach = Character(_("Security"), color= c_red, image = "security_breach", window_left_padding=wl_padding)
define programmer = Character(_("BK Programmer"), color = c_lightblue, image="crying_man", window_left_padding=wl_padding)


#### SCREEN CHARACTERS ####

define slavegirl1 = Character(_("Slave girl"), color = c_crimson, image = "slavegirl1", window_left_padding=wl_padding)
define slavegirl2 = Character(_("Slave girl"), color = c_violet, image = "slavegirl2", window_left_padding=wl_padding)
define shopgirl = Character(_("Merchant"), color = c_pink, image = "shopgirl", window_left_padding=wl_padding)
define jobgirl = DynamicCharacter("jobgirl_name", color = c_firered, image = "jobgirl", window_left_padding=wl_padding)
define bast = DynamicCharacter("bast_name", color = c_copper, image = "bast", window_left_padding=wl_padding)
define banker = DynamicCharacter("banker_name", color=c_turquoise, image = "banker", window_left_padding=wl_padding)
define taxgirl = DynamicCharacter("taxgirl_name", color=c_turquoise, image = "taxgirl", window_left_padding=wl_padding)


#### FARM AND MERCHANT CHARACTERS ####

# Gizel
define gizel = DynamicCharacter("gizel_name", color=c_magenta, image = "gizel", window_left_padding=wl_padding)

# City merchants (Characters are also defined as NPCs in 'BKstart')
define stella = DynamicCharacter("stella_name", color=c_lightmagenta, image="stella", window_left_padding=wl_padding)
define goldie = DynamicCharacter("goldie_name", color=c_yellow, image="goldie", window_left_padding=wl_padding)
define willow = DynamicCharacter("willow_name", color=c_copper, image="willow", window_left_padding=wl_padding)
define gina = DynamicCharacter("gina_name", color=c_softpurple, image="gina", window_left_padding=wl_padding)

define riche = DynamicCharacter("riche_name", color=c_azure, image="riche", window_left_padding=wl_padding)
define ramias = DynamicCharacter("ramias_name", color=c_lightgrey, image="ramias", window_left_padding=wl_padding)
define giftgirl = Character(_("Gift Shop Girl"), color=c_hotpink, image="giftgirl", window_left_padding=wl_padding)
define gurigura = DynamicCharacter("gurigura_name", color=c_yellow, image="gurigura", window_left_padding=wl_padding)
define katryn = DynamicCharacter("katryn_name", color=c_lightgreen, image="katryn", window_left_padding=wl_padding)
define today = DynamicCharacter("today_name", color=c_turquoise, image="today", window_left_padding=wl_padding)
define yesterday = DynamicCharacter("yesterday_name", color=c_turquoise, image="yesterday", window_left_padding=wl_padding)

# Extras
define templar = Character(_("Knight templar"), color=c_lightgrey, image="templar", window_left_padding=wl_padding)
define initiate = Character(_("Initiate"), color=c_white, image="initiate", window_left_padding=wl_padding)
define initiate1 = Character(_("First initiate"), color=c_lightblue, image="initiate", window_left_padding=wl_padding)
define initiate2 = Character(_("Second initiate"), color=c_lightred, image="initiate", window_left_padding=wl_padding)
define spirit = Character(_("Dark spirit"), color=c_white, image="spirit", window_left_padding=wl_padding)
define milkmaid = Character(_("Milkmaid"), color=c_pink, image="milkmaid", window_left_padding=wl_padding)
define relative = Character(_("Willow's relative"), color=c_copper)
define blood1 = Character(_("Blonde officer"), color=c_yellow, image="blood1", window_left_padding=wl_padding)
define blood2 = Character(_("Auburn officer"), color=c_copper, image="blood2", window_left_padding=wl_padding)

#### STORY (Chapter 1) ####

define character.kosmo = DynamicCharacter("kosmo_name", color=c_gold, image = "kosmo", window_left_padding=wl_padding)
define sergeant = DynamicCharacter("sergeant_name", color=c_copper, image = "sergeant", window_left_padding=wl_padding)
define maya = DynamicCharacter("maya_name", color=c_firered, image = "maya", window_left_padding=wl_padding)
define roz = Character(_("Roz"), color=c_firered, image = "roz", window_left_padding=wl_padding)
define lieutenant = DynamicCharacter("lieutenant_name", color = "#C06A45", image = "lieutenant", window_left_padding=wl_padding)
define renza = DynamicCharacter("renza_name", color=c_orange_pink, image = "renza", window_left_padding=wl_padding)
define satella = DynamicCharacter("satella_name", color=c_copper, image = "satella", window_left_padding=wl_padding)
define captain = DynamicCharacter("captain_name", color=c_emerald, image = "captain", window_left_padding=wl_padding)


#### STORY (Chapter 2) ####

define shalia = DynamicCharacter("shalia_name", color=c_softpurple, image = "shalia", window_left_padding=wl_padding)
define carpenter = DynamicCharacter("carpenter_name", color=c_firered, image = "carpenter", window_left_padding=wl_padding)
define kenshin = DynamicCharacter("kenshin_name", color=c_copper, image = "kenshin", window_left_padding=wl_padding)
define homura = DynamicCharacter("homura_name", color=c_purple, image = "homura", window_left_padding=wl_padding)
define suzume = DynamicCharacter("suzume_name", color=c_lightblue, image = "suzume", window_left_padding=wl_padding)
define narika = DynamicCharacter("narika_name", color=c_hotpink, image = "narika", window_left_padding=wl_padding)
define mizuki = DynamicCharacter("mizuki_name", color=c_azure, image = "mizuki", window_left_padding=wl_padding)
define haruka = DynamicCharacter("haruka_name", color=c_yellow, image = "haruka", window_left_padding=wl_padding)
define kunoichi = Character(_("Kunoichi"), color=c_red, image = "kunoichi", window_left_padding=wl_padding)
define papa_apprentice = Character(_("Apprentice"), color=c_softpurple, image = "papa_apprentice", window_left_padding=wl_padding)
define papa = Character(_("Papa Freak"), color=c_lightblue, image = "papa", window_left_padding=wl_padding)
define mask = DynamicCharacter("mask_name", color=c_copper, image = "mask", window_left_padding=wl_padding)
define hokoma_warrior = Character(_("Fierce Woman"), color=c_prune, image = "hokoma_warrior")
define magical_girl = Character(_("Strange Girl"), color=c_emerald, image = "magical_girl")
define girl_scientist = Character(_("Nerdy Girl"), color=c_firered, image = "girl_scientist")

#### STORY (Chapter 3) ####
define chaos = DynamicCharacter("chaos_name", color=c_lightmagenta, image = "chaos", window_left_padding=wl_padding)
define scribe = Character(_("Kenshin's Scribe"), color=c_grey_blue, image = "scribe", window_left_padding=wl_padding)
define warden = Character(_("Prison Warden"), color=c_firered, image = "warden", window_left_padding=wl_padding)
define hound_knight = Character(_("Knight leader"), color=c_darkred, image = "hound_leader", window_left_padding=wl_padding)
define noroi_leader = Character(_("Noroi leader"), color=c_darkred, image = "noroi_leader", window_left_padding=wl_padding)
define subaru = Character(_("Subaru"), color=c_lavender, image = "subaru", window_left_padding=wl_padding)
define receptionist = Character(_("MagicU Representative"), color=c_lavender, image = "receptionist", window_left_padding=wl_padding)
define shizuka = DynamicCharacter("shizuka_name", color=c_emerald, image = "shizuka", window_left_padding=wl_padding)
define golem = Character(_("Golem guard"), color=c_firered, image = "golem", window_left_padding=wl_padding)

#### MISC. CHARACTERS ####

## GENERIC EVENT CHARACTERS ##

define ev_girl1 = Character(_("Girl"), color= c_pink)
define ev_girl2 = Character(_("Girl"), color= c_gold)
define ev_girl3 = Character(_("Girl"), color= c_lightblue)
define ev_girl4 = Character(_("Girl"), color= c_white)
define woman = Character(_("Woman"), color= c_violet)
define slave = Character(_("Slave girl"), color= c_softpurple)
define warrior = Character(_("Warrior"), color= c_firered)
define yuna = Character(_("Yuna"), color= c_lightgrey)
define man = Character(_("Man"), color= c_cream)
define man2 = Character(_("Other Man"), color= c_lightgrey)
define customer = Character(_("Customer"), color= c_lightbrown)
define passerby = Character(_("Passerby"), color = c_lightblue)
define demonette = Character(_("Demonette"), color = c_softpurple, image = "demonette", window_left_padding=res_portrait_size)
define demon = Character(_("Demon"), color=c_lightred, image = "red_demon", window_left_padding=res_portrait_size)
define hanny = Character(_("Hanny"), color=c_lightbrown, image = "hanny", window_left_padding=res_portrait_size)

## STORY EXTRAS ##

define hmas_girl = Character(_("Mysterious girl"), color = c_emerald, image = "hmas", window_left_padding=wl_padding)
define sewer_woman = Character(_("Woman"), color=c_grey_blue, image = "sewer_woman", window_left_padding=wl_padding)

define mthug = Character(_("Masked thug"), color=c_white)
define captain_voice = Character(_("Captain's voice"), color=c_emerald)
define judge = Character(_("Judge"), color=c_lightgreen, image = "judge", window_left_padding=wl_padding)
define knight = Character(_("Knight"), color=c_softpurple, image = "knight", window_left_padding=wl_padding)
define lost_soldier = Character(_("Soldier"), color=c_copper, image = "lost_soldier", window_left_padding=wl_padding)

define raccoon = Character(_("Raccoon"), color=c_yellow, image = "raccoon", window_left_padding=wl_padding)
define akuma = Character(_("Akuma"), color=c_steel, image = "blue_demon", window_left_padding=wl_padding)
define gouki = Character(_("Gouki"), color=c_lightred, image = "red_demon", window_left_padding=wl_padding)
define rodrigo = Character(_("Rodrigo"), color=c_lightgrey, image = "skeleton", window_left_padding=wl_padding)

define receptionist = Character(_("MagicU Receptionist"), color=c_lightgrey, image = "receptionist", window_left_padding=wl_padding)


## CONTRACT CHARACTERS ##

define young_sailor = Character(_("Sailor"), color=c_copper, image = "sailor", window_left_padding=wl_padding)
define party_girl = Character(_("Party girl"), color=c_lightred, image = "party_girl", window_left_padding=wl_padding)
define nun = Character(_("Nun"), color=c_grey_blue, image = "nun", window_left_padding=wl_padding)
define kimono_lady = Character(_("Festival lady"), color=c_softpurple, image = "kimono_lady", window_left_padding=wl_padding)
define young_maid = Character(_("Young maid"), color=c_yellow, image = "young_maid", window_left_padding=wl_padding)
define diplomat = Character(_("Lady diplomat"), color=c_orange_pink, image = "diplomat", window_left_padding=wl_padding)
define sorceress = Character(_("Sorceress"), color=c_lightgrey, image = "sorceress", window_left_padding=wl_padding)
define naked_lady = Character(_("Naked lady"), color=c_cream, image = "naked_lady", window_left_padding=wl_padding)


####                            ####
##      IMAGES AND TRANSITIONS    ##
####                            ####


init -2 python:

## Images are declared using an auto-generating function

    def declare(name, img, method=None, x=config.screen_width, y=config.screen_height, wide=False, gallery=True, unlock=False, color_list=None, bw=False, sepia=False, flip=False): # img is the complete image path (from the game folder root)

        _properties = {}
        if bw:
            # bw only implemented for the 's', 'p', 'f', 'pf' and 'tall/med/small' methods for now.
            _properties["matrixcolor"] = SaturationMatrix(0)

        if sepia:
            _properties["matrixcolor"] = SepiaMatrix()

        if flip:
            _properties["xzoom"] = -1.0

        if wide: # Only matters for 4:3 resolution
            if not screen_is_wide:
                y = int(y*0.8)

        if is_videofile(img):
            renpy.image(name, Movie(img, play=img, size=(x, y)))

        elif method == "s": # Scale method (image will fit the exact target dimensions - not proportional)
            renpy.image(name, Transform(img, size=(x, y), **_properties))

        elif method == "p": # ProportionalScale method (image will fit the target dimensions while preserving its aspect ratio)
            #renpy.image(name, ProportionalScale(img, x, y))
            renpy.image(name, ProportionalScale(img, x, y, **_properties))

        elif method == "f": # Factor Scale (image dimensions will change proportionately to float numbers x and y)

            # Foolproofing
            if x == config.screen_width:
                x = 1.0
            if y == config.screen_height:
                y = 1.0

            x *= new_res_ratio
            y *= new_res_ratio

            renpy.image(name, Transform(img, xzoom=x, yzoom=y), **_properties)

        elif method in ("tall", "med", "small"): # Tailor-made adjustments for character bodies
            y_ratio = {"tall" : 0.85, "med" : 0.72, "small" : 0.6}[method]
            renpy.image(name, ProportionalScale(img, None, y_ratio*config.screen_height, **_properties))

        elif method == "pf": # Combines ProportionalScale method and Factor Scale method (based on screen resolution)
            renpy.image(name, ProportionalScale(img, int(x*config.screen_width), int(y*config.screen_height), **_properties))

        elif method == "c": # Colorize image
            if not color_list:
                raise AssertionError("No color list provided for the 'colorize' declaration method")
            for _prefix, _color in color_list:
                renpy.image(_prefix + name, ProportionalScale(img, x, y, matrixcolor=ColorizeMatrix(_color, c_white)))
                # print("declared " + _prefix + name)
            return None # Colorized images are not stored in the gallery

        else: # No change to the original image
            renpy.image(name, img)

        if unlock:
            unlock_pic(name, silent=True)

        if gallery: # Returns image name if the image is to be stored in a gallery
            return name
        else:
            return None

    def declare_multiple(base_name, base_img, method=None, start=0, finish=0, series=None, x=config.screen_width, y=config.screen_height, wide=False, gallery=True, unlock=False, loud=False):
        r = []

        if not series:
            series = range(start, finish+1)

        for nb in series:
            name, img = base_name % str(nb), base_img % str(nb)

            r.append(declare(name, img, method=method, x=x, y=y, wide=wide, gallery=gallery, unlock=unlock))

        return r # Python 2.7 won't allow me to unpack it. Darn.


#### IMAGE DECLARATIONS ####

# These dicts are used for generating CG galleries. Pictures will be displayed in the order they appear. Pictures with 'gallery' set to False will not appear in galleries.
# Each key is a separate button
# If every picture is 'gallery' set to False, it must be put in the 'unused' subdictionary.

    game_image_dict = {}

    ## UI images

    UI_elements_colors = [("lightblue", c_lightblue), ("orange", c_orange), ("darkorange", c_darkorange), ("lightorange", c_lightorange), ("lightcontrast", c_ui_light_solid), ("lightgrey", c_lightgrey), ("prune", c_prune)]

    declare("_button", "resources/gui/button/button.webp", "c", color_list = UI_elements_colors)
    declare("_bar_left", "resources/gui/bar/cryslider_full.webp", "c", color_list = UI_elements_colors + [("red", c_crimson), ("green", c_emerald)])
    declare("_bar_right", "resources/gui/bar/cryslider_empty.webp", "c", color_list = UI_elements_colors)

    for col in ["purple", "red", "yellow", "blue", "green"]:
        for i in range(5):
            declare("%s canister %i" % (col, i), "resources/ui/powers/%s canister%i.webp" % (col, i), "s")

    ## BACKGROUNDS ##

    game_image_dict["Backgrounds"] = {


                                        "sky" : [
                                                declare("bg sky day", "resources/backgrounds/sky day.webp", "s", wide=True),
                                                declare("bg sky dusk", "resources/backgrounds/sky dusk.webp", "s", wide=True),
                                                declare("bg sky night", "resources/backgrounds/sky night.webp", "s", wide=True),
                                                declare("bg valley dusk", "resources/backgrounds/valley dusk.webp", "s", wide=True),
                                                declare('bg stars', 'resources/backgrounds/stars.webp', 's', wide=True),
                                                declare('bg full_moon', 'resources/backgrounds/full moon.webp', 'p'),
                                                ],

                                        "outside" : [
                                                declare("bg outer wall", "resources/backgrounds/castle night.webp", "s", wide=True),
                                                declare("bg outer gate", "resources/backgrounds/gate night.webp", "s", wide=True),
                                                declare("bg battleground", "resources/backgrounds/battleground.webp", "s", wide=True),
                                                declare("bg caravan", "resources/backgrounds/caravan.webp", "s", wide=True, gallery="bg"),
                                                declare("bg dark street", "resources/backgrounds/dark street.webp", "s"),
                                                declare('bg farmland', 'resources/backgrounds/farmland.webp', 's'),
                                                declare('bg farmland dusk', 'resources/backgrounds/farmland dusk.webp', 's'),
                                                declare('bg farmland night', 'resources/backgrounds/farmland night.webp', 's'),
                                                declare('bg farmland night tall', 'resources/backgrounds/farmland night tall.webp', 'p', y=9999),
                                                declare('bg forest', 'resources/backgrounds/forest.webp', 's'),
                                                declare('bg forest night', 'resources/backgrounds/forest night.webp', 's'),
                                                declare('bg clearing', 'resources/backgrounds/clearing.webp', 's'),
                                                declare('bg farm outside', 'resources/backgrounds/farm outside.webp', 's'),
                                                declare('bg haunted_farm', 'resources/backgrounds/haunted farm.webp', 's', wide=True),
                                                declare('bg ambush1', 'resources/backgrounds/ambush.webp', 's', wide=True),
                                                declare('bg ambush2', "resources/backgrounds/ambush.webp", 's', flip=True, gallery=False),
                                                declare('bg mansion night', 'resources/backgrounds/mansion night.webp', 's', wide=True),
                                                declare('bg camp night', 'resources/backgrounds/camp night.webp', 's', wide=True),
                                                declare('bg street', 'resources/backgrounds/street.webp', 's', wide=True),
                                                declare('bg street night', 'resources/backgrounds/street night.webp', 's'),
                                                declare('bg execution_plaza', 'resources/backgrounds/execution plaza.webp', 's'),
                                                declare('bg castle', 'resources/backgrounds/castle.webp', 's'),
                                                declare('bg carriage', 'resources/backgrounds/carriage.webp', 'p'),
                                                declare('bg arena_front', 'resources/backgrounds/arena front.webp', 'p'),
                                                declare('bg dock', 'resources/backgrounds/dock.webp', 'p'),
                                                declare('bg rooftop', 'resources/backgrounds/rooftop.webp', 'p'),
                                                declare('bg rooftop night', 'resources/backgrounds/rooftop night.webp', 'p'),
                                                declare('bg dojo night', 'resources/backgrounds/dojo night.webp', 'p'),
                                                declare('bg asylum', 'resources/backgrounds/asylum.webp', 'p'),
                                                declare('bg prison entrance', 'resources/backgrounds/prison entrance.webp', 's'),
                                                declare("bg magicU", 'resources/backgrounds/magicU.webp', 'p', y=9999),
                                                declare("bg magicU explosion", 'resources/backgrounds/magicU explosion.webp', 's'),
                                                declare("bg floating island", 'resources/backgrounds/floating island.webp', 's', wide=True),
                                                declare("bg karkyr", 'resources/backgrounds/karkyr.webp', 's', wide=True),
                                                declare("bg shalia_tower", 'resources/backgrounds/shalia tower.webp', 's', wide=True),
                                                declare("bg westmarch", 'resources/backgrounds/westmarch.webp', 's', wide=True),
                                                declare("bg westmarch palace", 'resources/backgrounds/westmarch palace.webp', 's', wide=True),
                                                declare('bg moonlit_pond', 'resources/backgrounds/moonlit pond.webp', 's', wide=True),
                                                declare('bg cave entrance', 'resources/backgrounds/cave entrance.webp', 's', wide=True),
                                                declare('bg fire outside', 'resources/backgrounds/fire outside.webp', 's', wide=True),
                                                ],

                                        "inside" : [
                                                declare("bg palace", "resources/backgrounds/palace.webp", "s", wide=True),
                                                declare("bg desk", "resources/backgrounds/front desk.webp", "s"),
                                                declare("bg office", "resources/backgrounds/office.webp", "s", wide=True),
                                                declare("bg room", "resources/backgrounds/room.webp", "p", wide=True),
                                                declare("bg pen", "resources/brothels/farm/pen.webp", "p"),
                                                declare("bg throne room day", "resources/backgrounds/throne room day.webp", "s", wide=True),
                                                declare("bg throne room night", "resources/backgrounds/throne room night.webp", "s", wide=True),
                                                declare('bg gizel_room', 'resources/backgrounds/gizel room.webp', 's', wide=True),
                                                declare('bg master room', 'resources/backgrounds/master room.webp', 's', wide=True),
                                                declare('bg guard_office', 'resources/backgrounds/guard office.webp', 's', wide=True),
                                                declare('bg inner_sewers', 'resources/characters/npc/encounters/secret empty3.webp', 's', wide=True),
                                                declare('bg cell', 'resources/characters/npc/encounters/secret room.webp', 's', wide=True),
                                                declare('bg thieves_guild inside', 'resources/backgrounds/thieves guild hall.webp', 's'),
                                                declare('bg thieves_guild corridor', 'resources/backgrounds/thieves guild corridor.webp', 's', wide=True),
                                                declare('bg thieves_guild room', 'resources/backgrounds/thieves guild room.webp', 's', wide=True),
                                                declare('bg captain_office', 'resources/backgrounds/rich room.webp', 's', wide=True),
                                                declare('bg vault', 'resources/backgrounds/vault.webp', 's', wide=True),
                                                declare('bg palace room', 'resources/backgrounds/palace room.webp', 's', wide=True),
                                                declare('bg palace corridor', 'resources/backgrounds/palace corridor.webp', 's', wide=True),
                                                declare('bg palace corridor2', 'resources/backgrounds/palace corridor.webp', 's', wide=True, flip=True, gallery=False),
                                                declare('bg palace reception', 'resources/backgrounds/reception.webp', 's', wide=True),
                                                declare('bg shalia_temple', 'resources/backgrounds/shalia temple.webp', 's', wide=True),
                                                declare('bg other dimension', 'resources/backgrounds/other dimension.webp', 's'),
                                                declare('bg cave', 'resources/characters/npc/Encounters/secret empty2.webp', 's'),
                                                declare('bg empty_mansion', 'resources/backgrounds/mansion empty.webp', 's', wide=True),
                                                declare('bg mansion inside', 'resources/backgrounds/mansion inside.webp', 's', wide=True),
                                                declare('bg mansion inside2', 'resources/backgrounds/mansion inside2.webp', 's', wide=True),
                                                declare('bg mansion fire', 'resources/backgrounds/fire inside.webp', 's', wide=True),
                                                declare('bg dark_underground', 'resources/backgrounds/dark underground.webp', 's', wide=True),
                                                declare('bg magic_cellar', 'resources/backgrounds/magic cellar.webp', 's'),
                                                declare('bg lab', 'resources/backgrounds/lab.webp', 's'),
                                                declare('bg prison office', 'resources/backgrounds/prison office.webp', 's', wide=True),
                                                declare('bg jail', 'resources/backgrounds/jail.webp', 's'),
                                                declare('bg bedroom', 'resources/brothels/rooms/basic room2.webp', 's'),
                                                declare('bg magic_office', 'resources/backgrounds/magic office.webp', 's'),
                                                declare('bg classroom', 'resources/backgrounds/magical class.webp', 's', wide=True),
                                                declare('bg magic_vault', 'resources/backgrounds/magic vault.webp', 's'),
                                                declare('bg magic_vault_inside', 'resources/backgrounds/magic vault inside.webp', 's'),
                                                declare('bg archives', 'resources/backgrounds/archives.webp', 's', wide=True),
                                                declare("bg crystal_room", 'resources/backgrounds/crystal room.webp', 's', wide=True),
                                                ],

                                        "slavemarket" : [declare("bg slave market", "resources/backgrounds/slave market12.webp", "p"),] +
                                                        declare_multiple("bg slave market%s", "resources/backgrounds/slave market%s.webp", "p", start=1, finish=5) +
                                                        declare_multiple("bg slave market%s", "resources/backgrounds/slave market%s.webp", "p", y = int(config.screen_height*0.8), start=6, finish=7) +
                                                        declare_multiple("bg slave market%s", "resources/backgrounds/slave market%s.webp", "p", start=8, finish=11),


                                        "districts" : [
                                                declare("bg town", "resources/backgrounds/town.webp", "p"),
                                                declare('bg zan', 'resources/backgrounds/zan.webp', 's', wide=True),
                                                declare('bg rich district', 'resources/backgrounds/rich district.webp', 'p', wide=True),
                                                declare('bg poor district', 'resources/backgrounds/poor district.webp', 'p', wide=True),
                                                declare('bg slum district', 'resources/districts/slums.webp', 'p', wide=True),
                                                ],

                                        "locations" : list_imgfiles(path="resources/districts/locations/") + [
                                                    declare('bg spice_market', 'resources/districts/locations/spice market.webp', 's', wide=True, gallery=False),
                                                    declare('bg sewers', 'resources/districts/locations/sewers.webp', 's', wide=True, gallery=False),
                                                    declare('bg junkyard', 'resources/districts/locations/junkyard.webp', 's', gallery=False),
                                                    declare('bg harbor', 'resources/districts/locations/harbor.webp', 's', gallery=False),
                                                    declare('bg thieves_guild', 'resources/districts/locations/thieves guild.webp', 'p', gallery=False),
                                                    declare('bg watchtower', 'resources/districts/locations/watchtower.webp', 's', wide=True, gallery=False),
                                                    declare('bg gallows', 'resources/districts/locations/gallows.webp', 's', gallery=False),
                                                    declare('bg market', 'resources/districts/locations/market.webp', 's', gallery=False),
                                                    declare('bg exotic_emporium', 'resources/districts/locations/Exotic emporium.webp', 's', gallery=False),
                                                    declare('bg hanging_gardens', 'resources/districts/locations/Hanging gardens.webp', 'p', gallery=False),
                                                    declare('bg botanical_garden', 'resources/districts/locations/Botanical garden.webp', 'p', gallery=False),
                                                    declare('bg pilgrim_road', 'resources/districts/locations/Pilgrim road.webp', 's', gallery=False, wide=True),
                                                    declare('bg courtyard', 'resources/districts/locations/Courtyard.webp', 'p', gallery=False),
                                                    declare('bg ruins', 'resources/districts/locations/Ruins.webp', 'p', gallery=False),
                                                    declare('bg plaza', 'resources/districts/locations/plaza.webp', 'p', gallery=False),
                                                    declare('bg arena', 'resources/districts/locations/Arena.webp', 'p', gallery=False),
                                                    declare('bg prison', 'resources/districts/locations/prison.webp', 'p', gallery=False),
                                                    declare('bg seafront', 'resources/districts/locations/Seafront.webp', 'p', gallery=False),
                                                    # declare('bg library', 'resources/districts/locations/library.webp', 'p', gallery=False), # Replaced by MagicU
                                                    declare('bg magic_university', 'resources/districts/locations/magic_university.webp', 'p', gallery=False),
                                                    declare('bg banking_quarter', 'resources/districts/locations/Banking quarter.webp', 'p', gallery=False),
                                                ],

                                        "brothels" : [
                                                declare("bg brothel1", "resources/brothels/" + brothel_pics[1], "s", unlock=True),
                                                declare("bg brothel1 bw", "resources/brothels/" + brothel_pics[1], "s", bw=True, wide=True, gallery=False),
                                                declare("bg brothel2", "resources/brothels/" + brothel_pics[2], "p", wide=True),
                                                declare("bg brothel3", "resources/brothels/" + brothel_pics[3], "p"),
                                                declare("bg brothel4", "resources/brothels/" + brothel_pics[4], "p", wide=True),
                                                declare("bg brothel5", "resources/brothels/" + brothel_pics[5], "p", wide=True),
                                                declare("bg brothel6", "resources/brothels/" + brothel_pics[6], "s"),
                                                declare("bg brothel7", "resources/brothels/" + brothel_pics[7], "p"),
                                                ],

                                        "rooms" : list_imgfiles(path="resources/brothels/rooms/") + [
                                            declare('bg armory', 'resources/brothels/rooms/armory.webp', 'p', gallery=False),
                                            declare('bg wagon', 'resources/brothels/rooms/wagon.webp', 'p', wide=True, gallery=False),
                                            declare('bg onsen', 'resources/brothels/rooms/onsen.webp', 'p', gallery=False),
                                            declare('bg onsen dusty', 'resources/brothels/rooms/onsen_dusty.webp', 'p', gallery=False),
                                            declare('bg onsen dirty', 'resources/brothels/rooms/onsen_dirty.webp', 'p', gallery=False),
                                            declare('bg onsen verydirty', 'resources/brothels/rooms/onsen_verydirty.webp', 'p', gallery=False),
                                            declare('bg tavern', 'resources/brothels/rooms/tavern.webp', 'p', gallery=False),
                                            declare('bg tavern dusty', 'resources/brothels/rooms/tavern_dusty.webp', 'p', gallery=False),
                                            declare('bg tavern dirty', 'resources/brothels/rooms/tavern_dirty.webp', 'p', gallery=False),
                                            declare('bg tavern verydirty', 'resources/brothels/rooms/tavern_verydirty.webp', 'p', gallery=False),
                                            declare('bg okiya', 'resources/brothels/rooms/okiya.webp', 'p', gallery=False),
                                            declare('bg okiya dusty', 'resources/brothels/rooms/okiya_dusty.webp', 'p', gallery=False),
                                            declare('bg okiya dirty', 'resources/brothels/rooms/okiya_dirty.webp', 'p', gallery=False),
                                            declare('bg okiya verydirty', 'resources/brothels/rooms/okiya_verydirty.webp', 'p', gallery=False),
                                            declare('bg strip club', 'resources/brothels/rooms/strip club.webp', 'p', gallery=False),
                                            declare('bg strip club dusty', 'resources/brothels/rooms/strip club_dusty.webp', 'p', gallery=False),
                                            declare('bg strip club dirty', 'resources/brothels/rooms/strip club_dirty.webp', 'p', gallery=False),
                                            declare('bg strip club verydirty', 'resources/brothels/rooms/strip club_verydirty.webp', 'p', gallery=False),
                                            declare('bg club', 'resources/brothels/rooms/strip club.webp', 'p', gallery=False),
                                            ],

                                        "farm" : list_imgfiles(path="resources/brothels/farm/") + [
                                                declare('bg farm', 'resources/brothels/farm/farm.webp', 'p', wide=True),
                                                declare('bg farm tall', 'resources/brothels/farm/farm.webp', 's', gallery=False),
                                                declare('bg farm_stables', 'resources/brothels/farm/stables.webp', 's', gallery=False),
                                                declare('bg farm_pig_stall', 'resources/brothels/farm/pig stall.webp', 's', gallery=False),
                                                declare('bg farm_monster_den', 'resources/brothels/farm/monster den.webp', 's', gallery=False),
                                                declare('bg farm_workshop', 'resources/brothels/farm/workshop.webp', 's', gallery=False),
                                                ],

                                        }

    ## STORY ##

    game_image_dict["Story"] = {


                                "maid sex" : declare_multiple("bg gioblow%s", "resources/characters/npc/Maid/blow%s.webp", "p", start=1, finish=3) +
                                        declare_multiple("bg giofuck%s", "resources/characters/npc/Maid/fuck%s.webp", "p", start=1, finish=7),

                                "intro" : [
                                        declare('gknight fucked', 'resources/characters/npc/Misc/knight fucked.webp'),
                                        declare('princess1 fucked', 'resources/characters/npc/Misc/princess1 fucked.webp'),
                                        declare('princess2 fucked', 'resources/characters/npc/Misc/princess2 fucked.webp'),
                                        declare('priest fucked', 'resources/characters/npc/Misc/priest fucked.webp'),
                                        declare('mage fucked', 'resources/characters/npc/Misc/mage fucked.webp'),
                                        ],

                                "sill soft" : [declare('bg sill_hold', 'resources/characters/npc/Sill/hold.webp', 'p'), declare('bg sill_floor_naked', 'resources/characters/npc/Sill/floor naked.webp', 'p')],

                                "sill gio_fuck" : [declare('bg giofuck8', 'resources/characters/npc/Sill/gio fuck.webp', 'p')],

                                "sill sex1" :
                                        declare_multiple("bg nogiofuck%s", "resources/characters/npc/Sill/sex%s.webp", "p", start=1, finish=4) +
                                        declare_multiple("bg nogiofuck%s", "resources/characters/npc/Sill/sex%s.webp", "p", start=5, finish=6),

                                "sill glasses":
                                    declare_multiple("bg sill glasses%s", "resources/characters/npc/Sill/glasses (%s).webp", "p", start=1, finish=12),

                                "sill intro" : [
                                        declare('bg sill sold', 'resources/characters/npc/Sill/sill sold.webp', 'p'),
                                        declare('bg sill finger', 'resources/characters/npc/Sill/sill fingering.webp', 'p'),
                                        declare('bg sill sex', 'resources/characters/npc/Sill/sill sex.webp', 'p'),
                                        declare('bg sill bj', 'resources/characters/npc/Sill/sill sucking.webp', 'p'),
                                        declare('bg sill fetish', 'resources/characters/npc/Sill/sill fetish.webp', 'p'),
                                        ],

                                "hmas" : [
                                        declare('bg hmas1', 'resources/characters/npc/Hmas/xmas1.webp', 's', wide=True),
                                        declare('bg hmas2', 'resources/characters/npc/Hmas/xmas2.webp', 's', wide=True),
                                        declare('bg hmas sex1', 'resources/characters/npc/Hmas/sex1.webp', 's', wide=True),
                                        declare('bg hmas sex2', 'resources/characters/npc/Hmas/sex2.webp', 's', wide=True),
                                        declare('bg hmas anal1', 'resources/characters/npc/Hmas/anal1.webp', 's', wide=True),
                                        declare('bg hmas anal2', 'resources/characters/npc/Hmas/anal2.webp', 's', wide=True),
                                        ],

                                "renza sex" :
                                        [declare('bg renza_onsen', 'resources/characters/npc/Renza/onsen.webp', 's', wide=True)] +
                                        declare_multiple("bg renza_sex%s", "resources/characters/npc/Renza/sex%s.webp", "s", start=1, finish=6, wide=True),

                                "sewer rape" : declare_multiple('bg sewers_rape%s', 'resources/characters/npc/Sewer girl/sex%s.webp', 's', start=1, finish=3),

                                "lieutenant sex" : declare_multiple('bg lieutenant sex%s', 'resources/characters/npc/lieutenant/sex%s.webp', 'p', start=1, finish=2),

                                "captain sex" : [
                                        declare('captain sex1', 'resources/characters/npc/captain/sex1.webp', 's', wide=True),
                                        declare('captain sex2', 'resources/characters/npc/captain/sex2.webp', 's', wide=True),
                                        declare('bg captain sex3', 'resources/characters/npc/captain/sex3.webp', 's', wide=True),
                                        declare('bg captain sex4', 'resources/characters/npc/captain/sex4.webp', 's', wide=True),
                                        ],

                                "sergeant sex" : declare_multiple('bg sergeant sex%s', 'resources/characters/npc/sergeant/sex%s.webp', 'p', start=1, finish=3, wide=True),

                                "maya sex" : declare_multiple('bg maya sex%s', 'resources/characters/npc/maya/sex%s.webp', 'p', start=1, finish=3),

                                "satella soft1" : [
                                        declare('bg satella_intro', 'resources/characters/npc/satella/satella intro.webp', 'p', wide=True),
                                        declare('bg satella casting', 'resources/characters/npc/satella/casting.webp', 'p'),
                                        declare('bg satella dragon', 'resources/characters/npc/satella/dragon.webp', 'p'),
                                        ],

                                "satella soft2" : declare_multiple('bg satella sit%s', 'resources/characters/npc/satella/sitting (%s).webp', 'p', start=1, finish=3),

                                "satella soft3" : declare_multiple('bg satella stunned%s', 'resources/characters/npc/satella/stunned (%s).webp', 'p', start=1, finish=7),

                                "satella sex1" : declare_multiple('bg satella sex1_%s', 'resources/characters/npc/satella/sex1 (%s).webp', 'p', start=1, finish=3),

                                "satella sex2" : declare_multiple('bg satella sex2_%s', 'resources/characters/npc/satella/sex2 (%s).webp', 'p', start=1, finish=5),

                                "satella sex3" : declare_multiple('bg satella sex3_%s', 'resources/characters/npc/satella/sex3 (%s).webp', 'p', start=1, finish=5, wide=True),

                                "goldie soft" : [
                                        declare('bg goldie_hug', 'resources/characters/npc/Goldie/hug.webp', 'p'),
                                        declare('bg goldie_promise1', 'resources/characters/npc/Goldie/promise1.webp', 'p'),
                                        declare('bg goldie_promise2', 'resources/characters/npc/Goldie/promise2.webp', 'p'),
                                        ],

                                "gizel rape" : declare_multiple("bg gizel_rape%s", "resources/characters/npc/gizel/group (%s).webp", "p", start=1, finish=7),



                                "gizel soft" : declare_multiple("bg gizel_attack%s", "resources/characters/npc/gizel/attack (%s).webp", "p", start=1, finish=4),



                                "gizel sex1" : declare_multiple("bg gizel_big1_%s", "resources/characters/npc/gizel/big1 (%s).webp", "p", start=1, finish=5),




                                "gizel sex2" : declare_multiple("bg gizel_toad%s", "resources/characters/npc/gizel/beast (%s).webp", "p", start=1, finish=6),



                                "gizel sex3" : declare_multiple("bg gizel_machine%s", "resources/characters/npc/gizel/machine (%s).webp", "p", start=1, finish=6),



                                "gizel sex4" : declare_multiple("bg gizel_monster1_%s", "resources/characters/npc/gizel/monster (%s).webp", "p", start=1, finish=7),



                                "gizel sex5" : declare_multiple("bg gizel_monster2_%s", "resources/characters/npc/gizel/monster2 (%s).webp", "p", start=1, finish=6),


                                "gizel sex6" : declare_multiple("bg gizel_big2_%s", "resources/characters/npc/gizel/big2 (%s).webp", "p", start=1, finish=5),

                                "gizel sex7" : declare_multiple("bg gizel_sex1_%s", "resources/characters/npc/gizel/sex1 (%s).webp", "p", start=1, finish=5), #!

                                "gizel sex8" : declare_multiple("bg gizel_sex2_%s", "resources/characters/npc/gizel/sex2 (%s).webp", "p", start=1, finish=5), #!

                                "gizel sex9" : declare_multiple("bg gizel_sex3_%s", "resources/characters/npc/gizel/sex3 (%s).webp", "p", start=1, finish=5), #!

                                "goldie sex1" : declare_multiple("bg goldie_strip%s", "resources/characters/npc/Goldie/strip%s.webp", "p", start=1, finish=2),

                                "goldie sex2" : declare_multiple("bg goldie_titjob%s", "resources/characters/npc/Goldie/titjob%s.webp", "p", start=1, finish=2), #! Update to 1-4 after repeatable event

                                "goldie sex3" : declare_multiple("bg goldie_sex%s", "resources/characters/npc/Goldie/sex%s.webp", "p", start=1, finish=3),

                                "willow soft" : [
                                        declare('bg willow_cast', 'resources/characters/npc/Willow/cast.webp', 'p'),
                                        declare('bg willow_fire', 'resources/characters/npc/Willow/fire.webp', 'p'),
                                        declare('bg willow upskirt', 'resources/characters/npc/Willow/upskirt.webp', 'p'),
                                        declare('bg willow on_top', 'resources/characters/npc/Willow/on top.webp', 'p'),
                                        declare('bg willow tea', 'resources/characters/npc/Willow/tea.webp', 'p'),
                                        ],

                                "willow blowjob" : declare_multiple("bg willow bj%s", "resources/characters/npc/Willow/bj (%s).webp", "p", start=1, finish=4),

                                "willow fuck" : [declare('bg willow fuck', 'resources/characters/npc/Willow/sex.webp', 'p'), declare('bg willow sex', 'resources/characters/npc/Willow/sex.webp', 'p')],

                                "willow rape" : [declare('bg willow rape', 'resources/characters/npc/Willow/rape.webp', 'p')],

                                "willow relative" : declare_multiple("bg willow relative%s", "resources/characters/npc/Willow/rel (%s).webp", "p", start=1, finish=4),

                                "gina soft" : [
                                        declare('bg gina_standing', 'resources/characters/npc/Gina/stand.webp', 'p'),
                                        declare('bg gina_falling', 'resources/characters/npc/Gina/falling.webp', 's'),
                                        declare('bg gina_jump', 'resources/characters/npc/Gina/jump.webp', 'p', wide=True),
                                        # declare('bg gina_flying', 'resources/characters/npc/Gina/flying.webp', 's'),
                                        declare('bg gina_fallen1', 'resources/characters/npc/Gina/fall1.webp', 's'),
                                        declare('bg gina_fallen2', 'resources/characters/npc/Gina/fall2.webp', 's'),
                                        ],

                                "gina research" : declare_multiple("bg gina research%s", "resources/characters/npc/Gina/research%s.webp", "p", start=1, finish=2),

                                "stella soft" : [
                                        declare('bg mare_orgasm', 'resources/characters/npc/Stella/mare orgasm.webp', 's'),
                                        declare('bg mare_attack', 'resources/characters/npc/Stella/mare attack.webp', 's'),
                                        ],

                                "stella service" : declare_multiple("bg stella handjob%s", "resources/characters/npc/Stella/service (%s).webp", "p", start=1, finish=6),

                                "stella sex" : declare_multiple("bg stella sex%s", "resources/characters/npc/Stella/sex (%s).webp", "p", start=1, finish=7),

                                "stella wall" : declare_multiple("bg stella_wall%s", "resources/characters/npc/Stella/wall (%s).webp", "p", start=1, finish=5),

                                "blood1 bj" : declare_multiple("bg ka%s", "resources/characters/npc/Stella/ka (%s).webp", "p", start=1, finish=6),

                                "blood2 tj" : declare_multiple("bg zee%s", "resources/characters/npc/Stella/zee (%s).webp", "p", start=1, finish=5),

                                "stella bj" : declare_multiple("bg stella_bj%s", "resources/characters/npc/Stella/bj (%s).webp", "p", start=1, finish=4),

                                "treasure sex1" : declare_multiple("bg treasure_blonde sex%s", "resources/events/treasure_blonde_sex (%s).webp", "p", start=1, finish=6),

                                "treasure sex2" : declare_multiple("bg treasure_pink sex%s", "resources/events/treasure_pink_sex (%s).webp", "p", start=1, finish=4),

                                "sewer girl sex" : [
                                        declare('bg sewer_girl_sex1', 'resources/characters/npc/Sewer girl/sex4.webp', 'p'),
                                        declare('bg sewer_girl_sex2', 'resources/characters/npc/Sewer girl/sex5.webp', 'p'),
                                        declare('bg sewer_girl_sex3', 'resources/characters/npc/Sewer girl/sex6.webp', 'p'),
                                        ],

                                "shalia soft" : declare_multiple('bg shalia%s', 'resources/characters/npc/shalia/shalia (%s).webp', 'p', start=1, finish=5),

                                "shalia fj" : declare_multiple('bg shalia fj%s', 'resources/characters/npc/shalia/fj (%s).webp', 'p', start=1, finish=4),

                                "banker titjob" : declare_multiple('bg banker titjob%s', 'resources/characters/npc/banker/titjob (%s).webp', 'p', start=1, finish=3, wide=True),

                                "banker sex" : declare_multiple('bg banker sex%s', 'resources/characters/npc/banker/sex (%s).webp', 'p', start=1, finish=3, wide=True),

                                "taxgirl sex" : declare_multiple('bg taxgirl sex%s', 'resources/characters/npc/taxgirl/sex (%s).webp', 'p', start=1, finish=5, wide=True),

                                "taxgirl anal" : declare_multiple('bg taxgirl anal%s', 'resources/characters/npc/taxgirl/anal (%s).webp', 'p', start=1, finish=4, wide=True),

                                "jobgirl magic sex" : declare_multiple('bg jobgirl magic sex%s', 'resources/characters/npc/jobgirl/magic sex (%s).webp', 'p', start=1, finish=4, wide=True),

                                "bast sex" : declare_multiple('bg bast sex%s', 'resources/characters/npc/bast/sex (%s).webp', 'p', start=1, finish=6, wide=True),

                                "bast titjob" : declare_multiple('bg bast titjob%s', 'resources/characters/npc/bast/titjob (%s).webp', 'p', start=0, finish=5, wide=True),

                                "kenshin meet" : declare_multiple('bg kenshin_meet%s', 'resources/characters/npc/kenshin/meet%s.webp', 'p', start=1, finish=4),
                                "kenshin pendant" : declare_multiple('bg kenshin_pendant%s', 'resources/backgrounds/pendant%s.webp', 'f', x=0.25, y=0.25, start=1, finish=2),

                                "kenshin soft" : [declare('bg kenshin secret', 'resources/characters/npc/kenshin/secret meeting.webp', 'p'), declare('kenshin showdown', 'resources/characters/npc/kenshin/showdown.webp', 'p')],

                                "suzume soft" : [declare('bg suzume_roof', 'resources/characters/npc/suzume/roof.webp', 'p')],

                                "suzume forest" : declare_multiple('bg suzume_forest%s', 'resources/characters/npc/suzume/sex forest (%s).webp', 'p', start=1, finish=8),

                                "suzume brothel" : declare_multiple('bg suzume_brothel%s', 'resources/characters/npc/suzume/brothel (%s).webp', 'p', start=1, finish=5),

                                "suzume visit" : [
                                                declare('bg suzume_onsen', 'resources/characters/npc/suzume/onsen.webp', 'p'),
                                                declare('bg suzume_69', 'resources/characters/npc/suzume/69.webp', 'p'),
                                                declare('bg suzume_piledriver', 'resources/characters/npc/suzume/piledriver.webp', 'p'),
                                                ],

                                "homura okiya" : [
                                                declare('bg homura_okiya happy', 'resources/characters/npc/homura/okiya happy.webp', 'p'),
                                                declare('bg homura_okiya sad', 'resources/characters/npc/homura/okiya sad.webp', 'p'),
                                                declare('bg homura_okiya serious', 'resources/characters/npc/homura/okiya serious.webp', 'p'),
                                                declare('bg homura_okiya angry', 'resources/characters/npc/homura/okiya angry.webp', 'p'),
                                                ],

                                "homura naked" : declare_multiple('bg homura_naked%s', 'resources/characters/npc/homura/naked (%s).webp', 'p', start=1, finish=3),

                                "homura mast" : declare_multiple('bg homura_mast%s', 'resources/characters/npc/homura/mast%s.webp', 'p', start=1, finish=5),

                                "homura bj" : declare_multiple('bg homura_bj%s', 'resources/characters/npc/homura/bj%s.webp', 'p', start=1, finish=5),

                                "homura 69" : declare_multiple('bg homura_69_%s', 'resources/characters/npc/homura/sixty-nine (%s).webp', 'p', start=1, finish=6),

                                "homura sex" : declare_multiple('bg homura_sex%s', 'resources/characters/npc/homura/sex (%s).webp', 'p', start=1, finish=5),

                                "homura cowgirl" : declare_multiple('bg homura_cowgirl%s', 'resources/characters/npc/homura/cowgirl (%s).webp', 'p', start=1, finish=4),

                                "homura waterfall" : declare_multiple('bg homura_water%s', 'resources/characters/npc/homura/waterfall (%s).webp', 'p', start=1, finish=8),

                                "homura anal" : declare_multiple('bg homura_anal%s', 'resources/characters/npc/homura/anal (%s).webp', 'p', start=1, finish=5),

                                "homura rest" : declare_multiple('bg homura_rest%s', 'resources/characters/npc/homura/rest (%s).webp', 'p', start=1, finish=4),

                                "homura ninja" : [declare('homura showdown', 'resources/characters/npc/homura/showdown.webp', 'p'), declare('bg homura fire', 'resources/characters/npc/homura/fire.webp', 'p')],

                                "homura tryst" : declare_multiple('bg homura_tryst%s', 'resources/characters/npc/homura/tryst (%s).webp', 'p', start=1, finish=4),

                                "homura capture" : declare_multiple('bg homura_capture%s', 'resources/characters/npc/homura/capture (%s).webp', 'p', start=1, finish=5),

                                "homura farm" : declare_multiple('bg homura_farm%s', 'resources/characters/npc/homura/farm (%s).webp', 'p', start=1, finish=6),

                                "homura group" : declare_multiple('bg homura_group%s', 'resources/characters/npc/homura/group (%s).webp', 'p', start=1, finish=4),

                                "homura grass" : declare_multiple('bg homura_grass%s', 'resources/characters/npc/homura/grass (%s).webp', 'p', start=1, finish=4),

                                "narika soft" : [declare('bg narika intro', 'resources/characters/npc/kunoichi/narika/intro.webp', 'p'),
                                                declare('narika showdown', 'resources/characters/npc/kunoichi/narika/showdown.webp', 'p'),
                                                ],

                                "narika mast" : declare_multiple("bg narika_mast%s", "resources/characters/npc/kunoichi/narika/mast (%s).webp", "p", start=1, finish=11),

                                "narika tiny" : declare_multiple("bg narika_tiny%s", "resources/characters/npc/kunoichi/narika/tiny (%s).webp", "p", start=1, finish=6),

                                "narika capture" : declare_multiple("bg narika_capture%s", "resources/characters/npc/kunoichi/narika/capture (%s).webp", "p", start=1, finish=16),

                                "narika waitress" : declare_multiple("bg narika_waitress%s", "resources/characters/npc/kunoichi/narika/waitress (%s).webp", "p", start=1, finish=7),

                                "narika dancer" : declare_multiple("bg narika_dancer%s", "resources/characters/npc/kunoichi/narika/dancer (%s).webp", "p", start=1, finish=20),

                                "narika masseuse" : declare_multiple("bg narika_masseuse%s", "resources/characters/npc/kunoichi/narika/masseuse (%s).webp", "p", start=1, finish=10),

                                "narika geisha" : declare_multiple("bg narika_geisha%s", "resources/characters/npc/kunoichi/narika/geisha (%s).webp", "p", start=1, finish=12),

                                "narika sex" : declare_multiple("bg narika_sex%s", "resources/characters/npc/kunoichi/narika/sex (%s).webp", "p", start=1, finish=10),

                                "narika broken" : declare_multiple("bg narika_broken%s", "resources/characters/npc/kunoichi/narika/broken (%s).webp", "p", start=1, finish=7),

                                "mizuki soft" : [
                                                # declare('bg mizuki react', 'resources/characters/npc/kunoichi/mizuki/react.webp', 'p'),
                                                declare('bg mizuki intro', 'resources/characters/npc/kunoichi/mizuki/intro.webp', 'p'),
                                                declare('bg mizuki intro1', 'resources/characters/npc/kunoichi/mizuki/intro1.webp', 'p'),
                                                declare('bg mizuki intro2', 'resources/characters/npc/kunoichi/mizuki/intro2.webp', 'p'),
                                                declare('bg mizuki combat', 'resources/characters/npc/kunoichi/mizuki/combat.webp', 'p'),
                                                declare('bg mizuki poison', 'resources/characters/npc/kunoichi/mizuki/poison.webp', 'p'),
                                                # declare('bg mizuki magic', 'resources/characters/npc/kunoichi/mizuki/ice magic.webp', 'p'),
                                                declare('bg mizuki defeat', 'resources/characters/npc/kunoichi/mizuki/defeat.webp', 'p'),
                                                declare('mizuki showdown', 'resources/characters/npc/kunoichi/mizuki/showdown.webp', 'p'),
                                                ] + declare_multiple("bg mizuki family%s", "resources/characters/npc/kunoichi/mizuki/family (%s).webp", "p", start=1, finish=2) + declare_multiple("bg mizuki yukata%s", "resources/characters/npc/kunoichi/mizuki/yukata (%s).webp", "p", start=1, finish=2) + declare_multiple("bg mizuki death%s", "resources/characters/npc/kunoichi/mizuki/death (%s).webp", "p", start=1, finish=3),


                                "mizuki honeymoon" : declare_multiple("bg mizuki honeymoon%s", "resources/characters/npc/kunoichi/mizuki/honeymoon (%s).webp", "p", start=1, finish=9),

                                "mizuki footjob" : declare_multiple("bg mizuki footjob%s", "resources/characters/npc/kunoichi/mizuki/footjob (%s).webp", "p", start=1, finish=3),

                                "mizuki rough" : declare_multiple("bg mizuki rough%s", "resources/characters/npc/kunoichi/mizuki/rough (%s).webp", "p", start=1, finish=4),

                                "mizuki betrayal" : declare_multiple("bg mizuki betrayal%s", "resources/characters/npc/kunoichi/mizuki/betrayal (%s).webp", "p", start=1, finish=8),

                                "mizuki onsen" : declare_multiple("bg mizuki_onsen%s", "resources/characters/npc/kunoichi/mizuki/onsen (%s).webp", "p", start=1, finish=4),

                                "mizuki goodbye" : declare_multiple("bg mizuki sex%s", "resources/characters/npc/kunoichi/mizuki/sex (%s).webp", "p", start=1, finish=6) + declare_multiple("bg mizuki goodbye%s", "resources/characters/npc/kunoichi/mizuki/disappear (%s).webp", "p", start=1, finish=3),

                                "mizuki brothel" : declare_multiple("bg mizuki brothel service%s", "resources/characters/npc/kunoichi/mizuki/brothel service (%s).webp", "p", start=1, finish=3) +  declare_multiple("bg mizuki brothel sex%s", "resources/characters/npc/kunoichi/mizuki/brothel sex (%s).webp", "p", start=1, finish=5) +
                                declare_multiple("bg mizuki brothel anal%s", "resources/characters/npc/kunoichi/mizuki/brothel anal (%s).webp", "p", start=1, finish=5) +
                                declare_multiple("bg mizuki brothel fetish%s", "resources/characters/npc/kunoichi/mizuki/brothel fetish (%s).webp", "p", start=1, finish=4) +
                                declare_multiple("bg mizuki brothel final%s", "resources/characters/npc/kunoichi/mizuki/brothel final (%s).webp", "p", start=1, finish=3),

                                "mizuki capture" : declare_multiple("bg mizuki capture%s", "resources/characters/npc/kunoichi/mizuki/capture (%s).webp", "p", start=1, finish=3),

                                "haruka soft" : [declare('bg haruka intro', 'resources/characters/npc/kunoichi/haruka/intro.webp', 'p'), declare('haruka showdown', 'resources/characters/npc/kunoichi/haruka/showdown.webp', 'p')] +
                                                declare_multiple("bg haruka defeat%s", "resources/characters/npc/kunoichi/haruka/defeat (%s).webp", "p", start=1, finish=3),

                                "haruka pillory" : declare_multiple("bg haruka pillory%s", "resources/characters/npc/kunoichi/haruka/pillory (%s).webp", "p", start=1, finish=9),

                                "haruka bondage" : declare_multiple("bg haruka bondage%s", "resources/characters/npc/kunoichi/haruka/bondage (%s).webp", "p", start=1, finish=12),

                                "haruka fondle" : declare_multiple("bg haruka fondle%s", "resources/characters/npc/kunoichi/haruka/fondle (%s).webp", "p", start=1, finish=5),

                                "haruka big" : declare_multiple("bg haruka big%s", "resources/characters/npc/kunoichi/haruka/big (%s).webp", "p", start=1, finish=13),

                                "haruka beast" : declare_multiple("bg haruka beast%s", "resources/characters/npc/kunoichi/haruka/beast (%s).webp", "p", start=1, finish=13),

                                "haruka monster" : declare_multiple("bg haruka monster%s", "resources/characters/npc/kunoichi/haruka/monster (%s).webp", "p", start=1, finish=6),

                                "haruka machine" : declare_multiple("bg haruka machine%s", "resources/characters/npc/kunoichi/haruka/machine (%s).webp", "p", start=1, finish=6),

                                "haruka cowgirl" : declare_multiple("bg haruka cowgirl%s", "resources/characters/npc/kunoichi/haruka/cowgirl (%s).webp", "p", start=1, finish=6),

                                "haruka massage" : declare_multiple("bg haruka massage%s", "resources/characters/npc/kunoichi/haruka/massage (%s).webp", "p", start=1, finish=21),

                                "carpenter sex" : declare_multiple("bg iulia_sex%s", "resources/characters/npc/carpenter/sex%s.webp", "p", start=1, finish=6),

                                "papa freak" : [declare('bg papa_freak', 'resources/characters/npc/misc/freak.webp', 'p', wide=True)],

                                "shizuka bed" : declare_multiple("bg shizuka bed%s", "resources/characters/npc/shizuka/bed (%s).webp", "p", start=1, finish=2),

                                "MU monster" : declare_multiple("bg MU_monster%s", "resources/characters/npc/kunoichi/guests/MU monster (%s).webp", "p", start=1, finish=6),

                                "MU wall" : declare_multiple("bg MU_wall%s", "resources/characters/npc/kunoichi/guests/MU wall (%s).webp", "p", start=1, finish=6),

                                "witches" : declare_multiple('bg witches%s', 'resources/characters/npc/encounters/witches (%s).webp', 'p', start=1, finish=3, wide=True),

                                "ninja guests" : declare_multiple('bg guest1_sex%s', 'resources/characters/npc/kunoichi/guests/guest1 sex (%s).webp', 'p', start=1, finish=7) +
                                declare_multiple('bg guest2_sex%s', 'resources/characters/npc/kunoichi/guests/guest2 sex (%s).webp', 'p', start=1, finish=6) +
                                declare_multiple('bg guest3_sex%s', 'resources/characters/npc/kunoichi/guests/guest3 sex (%s).webp', 'p', start=1, finish=9),

                                "subaru prison" : [declare('bg subaru prison', 'resources/characters/npc/kunoichi/subaru/prison.webp', 'p', wide=True)] + declare_multiple('bg subaru fondle%s', 'resources/characters/npc/kunoichi/subaru/fondle (%s).webp', 'p', start=1, finish=6),

                                "subaru sex" : declare_multiple('bg subaru sex%s', 'resources/characters/npc/kunoichi/subaru/sex (%s).webp', 'p', start=1, finish=5) + declare_multiple('bg subaru anal%s', 'resources/characters/npc/kunoichi/subaru/anal (%s).webp', 'p', start=1, finish=5),

                                "subaru titjob" : declare_multiple('bg subaru titjob%s', 'resources/characters/npc/kunoichi/subaru/titjob (%s).webp', 'p', start=1, finish=7) + declare_multiple('bg subaru bondage titjob%s', 'resources/characters/npc/kunoichi/subaru/bondage titjob (%s).webp', 'p', start=1, finish=10), #!

                                "subaru demon" : declare_multiple('bg subaru_demon%s', 'resources/characters/npc/kunoichi/subaru/demon (%s).webp', 'p', start=1, finish=7),

                                "chaos" : [declare('bg chaos chained', 'resources/characters/npc/Chaos/bg chained.webp', 's'),
                                            declare('bg chaos no girl', 'resources/characters/npc/Chaos/bg no girl.webp', 'p'),
                                            declare('bg chaos girls', 'resources/characters/npc/Chaos/bg girls.webp', 'p'),
                                            declare('bg chaos virgin', 'resources/characters/npc/Chaos/bg virgin.webp', 'p')],
                                }


    ## CHARACTERS ##

    game_image_dict["Characters"] = OrderedDict([

                                ("sill", [
                                        declare('sill', 'resources/characters/npc/Sill/body.webp', "tall"),

                                        declare('sill past', 'resources/characters/npc/Sill/body_old.webp', "tall"),
                                        declare('sill normal', 'resources/characters/npc/Sill/body.webp', "tall", gallery=False),
                                        declare('sill happy', 'resources/characters/npc/Sill/body.webp', "tall", gallery=False),
                                        declare('sill sad', 'resources/characters/npc/Sill/body1.webp', "tall"),
                                        declare('sill drogon', 'resources/characters/npc/Sill/sill and drogon2.webp', "tall"),
                                        declare('sill naked', 'resources/characters/npc/Sill/body2.webp', "tall"),
                                        declare('sill glasses', 'resources/characters/npc/Sill/body glasses.webp', "tall"),

                                        declare('side sill', 'resources/characters/npc/Sill/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side sill normal', 'resources/characters/npc/Sill/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side sill unknown', 'resources/characters/npc/Sill/portrait_unknown.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side sill happy', 'resources/characters/npc/Sill/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side sill sad', 'resources/characters/npc/Sill/portrait1.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side sill naked', 'resources/characters/npc/Sill/portrait2.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side sill past', 'resources/characters/npc/Sill/portrait_old.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side sill drogon', 'resources/characters/npc/Sill/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side drogon', 'resources/characters/npc/Misc/drogon.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side sill glasses', 'resources/characters/npc/Sill/portrait glasses.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("kurohime", [
                                        declare('kuro', 'resources/characters/npc/Kurohime/body.webp', "tall"),
                                        declare('side kuro', 'resources/characters/npc/Kurohime/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("maid", [
                                        declare('maid normal', 'resources/characters/npc/Maid/normal.webp', "tall"),
                                        declare('maid blush', 'resources/characters/npc/Maid/blush.webp', "tall"),

                                        declare('side maid normal', 'resources/characters/npc/Maid/portrait.webp', 's', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side maid blush', 'resources/characters/npc/Maid/portrait blush.webp', 's', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("gio", [
                                        declare('gio', 'resources/characters/npc/Gio/body.webp', "med"),
                                        declare('gio normal', 'resources/characters/npc/Gio/body.webp', "med", gallery=False),
                                        declare('gio incognito', 'resources/characters/npc/Gio/body.webp', "med", gallery=False),
                                        declare('side gio', 'resources/characters/npc/Gio/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side gio normal', 'resources/characters/npc/Gio/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side gio incognito', 'resources/characters/npc/Gio/portrait incognito.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("jobgirl", [
                                        declare('jobgirl', 'resources/characters/npc/Jobgirl/body.webp', "tall"),
                                        declare('jobgirl normal', 'resources/characters/npc/Jobgirl/body.webp', "tall", gallery=False),
                                        declare('jobgirl magic', 'resources/characters/npc/Jobgirl/body magic.webp', "tall"),
                                        declare('jobgirl magic normal', 'resources/characters/npc/Jobgirl/body magic.webp', "tall", gallery=False),
                                        declare('jobgirl magic blush', 'resources/characters/npc/Jobgirl/body magic blush.webp', "tall"),
                                        declare('side jobgirl', 'resources/characters/npc/Jobgirl/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("shopgirl", [declare("bg shop", "resources/backgrounds/shop.webp", "p"), declare('bg shop bath', 'resources/backgrounds/shop2.webp', 'p'),]),

                                ("sergeant", [
                                        declare('sergeant', 'resources/characters/npc/Sergeant/body.webp', "tall"),
                                        declare('side sergeant', 'resources/characters/npc/Sergeant/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("maya", [
                                        declare('maya', 'resources/characters/npc/Maya/body.webp', "p"),
                                        declare('maya disarmed', 'resources/characters/npc/Maya/disarmed.webp', "p"),
                                        declare('maya disarmed flip', "resources/characters/npc/Maya/disarmed.webp", "p", flip=True, gallery=False),
                                        declare('side maya', 'resources/characters/npc/Maya/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("lieutenant", [
                                        declare('lieutenant', 'resources/characters/npc/Lieutenant/body.webp', "tall"),
                                        declare('lieutenant attack', 'resources/characters/npc/Lieutenant/body attack.webp', "tall"),
                                        declare('side lieutenant', 'resources/characters/npc/Lieutenant/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("sewer woman", [
                                        declare('sewer_woman dressed', 'resources/characters/npc/Sewer girl/body.webp', "tall"),
                                        declare('sewer_woman naked', 'resources/characters/npc/Sewer girl/naked.webp', "tall"),
                                        declare('side sewer_woman', 'resources/characters/npc/Sewer girl/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side sewer_woman naked', 'resources/characters/npc/Sewer girl/portrait naked.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),


                                ("renza", [
                                        declare('renza', 'resources/characters/npc/Renza/body.webp', "med"),
                                        declare('side renza', 'resources/characters/npc/Renza/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("satella", [
                                        declare('satella', 'resources/characters/npc/Satella/body1.webp', "tall"),
                                        declare('satella happy', 'resources/characters/npc/Satella/body1.webp', "tall", gallery=False),
                                        declare('satella angry', 'resources/characters/npc/Satella/body1.webp', "tall", gallery=False),
                                        declare('satella_standing', 'resources/characters/npc/Satella/body2.webp', "tall"),
                                        declare('side satella', 'resources/characters/npc/Satella/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side satella angry', 'resources/characters/npc/Satella/portrait2.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('satella naked', 'resources/characters/npc/Satella/body3.webp', "tall"),
                                        declare('side satella naked', 'resources/characters/npc/Satella/portrait3.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("captain", [
                                        declare('captain', 'resources/characters/npc/Captain/body.webp', "tall"),
                                        declare('side captain', 'resources/characters/npc/Captain/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("gizel", [
                                        declare('gizel', 'resources/characters/npc/Gizel/body.webp', 'tall'),
                                        declare('gizel normal', 'resources/characters/npc/Gizel/body.webp', 'tall', gallery=False),
                                        declare('gizel soft', 'resources/characters/npc/Gizel/body soft.webp', 'tall'),
                                        declare('gizel surprise', 'resources/characters/npc/Gizel/body surprise.webp', 'tall'),
                                        declare('gizel shy', 'resources/characters/npc/Gizel/body shy.webp', 'tall'),
                                        declare('gizel blush', 'resources/characters/npc/Gizel/body blush.webp', 'tall'),
                                        declare('gizel smirk', 'resources/characters/npc/Gizel/body smirk.webp', 'tall'),
                                        declare('gizel upset', 'resources/characters/npc/Gizel/body upset.webp', 'tall'),
                                        declare('gizel angry', 'resources/characters/npc/Gizel/body angry.webp', 'tall'),

                                        declare('gizel whip angry', 'resources/characters/npc/Gizel/whip1.webp', 'tall'),
                                        declare('gizel whip happy', 'resources/characters/npc/Gizel/whip2.webp', 'tall'),
                                        declare('gizel whip struggling', 'resources/characters/npc/Gizel/whip3.webp', 'tall'),

                                        declare('side gizel', 'resources/characters/npc/Gizel/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side gizel normal', 'resources/characters/npc/Gizel/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side gizel soft', 'resources/characters/npc/Gizel/portrait soft.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side gizel surprise', 'resources/characters/npc/Gizel/portrait surprise.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side gizel shy', 'resources/characters/npc/Gizel/portrait shy.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side gizel blush', 'resources/characters/npc/Gizel/portrait blush.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side gizel smirk', 'resources/characters/npc/Gizel/portrait smirk.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side gizel upset', 'resources/characters/npc/Gizel/portrait upset.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side gizel angry', 'resources/characters/npc/Gizel/portrait angry.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("goldie", [
                                        declare('goldie', 'resources/characters/npc/Goldie/body.webp', "tall"),
                                        declare('side goldie', 'resources/characters/npc/Goldie/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
            #                            declare('goldie_swimsuit', 'resources/characters/npc/Goldie/body swimsuit.webp'),
                                        #declare('side goldie_swimsuit', 'resources/characters/npc/Goldie/portrait swimsuit.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("willow", [
                                        declare('willow', 'resources/characters/npc/Willow/body.webp', "med"),
                                        declare('side willow', 'resources/characters/npc/Willow/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("gina", [
                                        declare('gina', 'resources/characters/npc/Gina/body.webp', "med"),
                                        declare('side gina', 'resources/characters/npc/Gina/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("stella", [
                                        declare('stella', 'resources/characters/npc/Stella/body1.webp', "pf", 1.4, 1.4), # Must be shown with yoffset
                                        declare('stella normal', 'resources/characters/npc/Stella/body1.webp', "pf", 1.4, 1.4, gallery=False), # Must be shown with yoffset
                                        declare('stella crossed', 'resources/characters/npc/Stella/body2.webp', "pf", 1.4, 1.4), # Must be shown with yoffset
                                        declare('stella uniform', 'resources/characters/npc/Stella/body3.webp', "p"),
                                        declare('side stella', 'resources/characters/npc/Stella/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side stella normal', 'resources/characters/npc/Stella/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side stella uniform', 'resources/characters/npc/Stella/portrait2.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("blood island officers", [
                                        declare('blood1', 'resources/characters/npc/Stella/ka body.webp', 'p'),
                                        declare('side blood1', 'resources/characters/npc/Stella/ka portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('blood2', 'resources/characters/npc/Stella/zee body.webp', 'p'),
                                        declare('side blood2', 'resources/characters/npc/Stella/zee portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),


                                ("milkmaid", [
                                        declare('milkmaid', 'resources/characters/npc/Misc/milkmaid.webp', "tall"),
                                        declare('side milkmaid', 'resources/characters/npc/Misc/milkmaid portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("kosmo", [
                                        declare('kosmo happy', 'resources/characters/npc/Kosmo/body1.webp', "tall"),
                                        declare('kosmo angry', 'resources/characters/npc/Kosmo/body2.webp', "tall"),
                                        declare('kosmo happy bw', 'resources/characters/npc/Kosmo/body1.webp', "tall", bw=True, gallery=False),
                                        declare('kosmo angry bw', 'resources/characters/npc/Kosmo/body2.webp', "tall", bw=True, gallery=False),
                                        declare('kosmo laughing', 'resources/characters/npc/Kosmo/body3.webp', "tall"),
                                        declare('side kosmo', 'resources/characters/npc/Kosmo/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side kosmo angry', 'resources/characters/npc/Kosmo/portrait2.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side kosmo bw', 'resources/characters/npc/Kosmo/portrait.webp', 'p', bw=True, x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side kosmo angry bw', 'resources/characters/npc/Kosmo/portrait2.webp', 'p', bw=True, x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('kosmo', 'resources/characters/npc/Kosmo/body1.webp', "tall", gallery=False),
                                        declare('kosmo bw', 'resources/characters/npc/Kosmo/body1.webp', "tall", bw=True, gallery=False),
                                        ]),

                                ("kosmo girls", [
                                        declare('kosmo_girl_scientist', 'resources/characters/npc/Kosmo/girl1.webp', "tall"),
                                        declare('kosmo_girl_ninja', 'resources/characters/npc/Kosmo/girl2.webp', "tall"),
                                        declare('kosmo_girl_daughter', 'resources/characters/npc/Kosmo/girl3.webp', "tall"),
                                        declare('kosmo_girl_magic', 'resources/characters/npc/Kosmo/girl4.webp', "tall"),
                                        declare('kosmo_girl_wife', 'resources/characters/npc/Kosmo/girl5.webp', "tall"),
                                        declare('kosmo_girl_captive', 'resources/characters/npc/Kosmo/girl6.webp', "tall"),
                                        declare('kosmo_girl_rogue', 'resources/characters/npc/Kosmo/girl7.webp', "tall"),
                                        declare('kosmo_girl_pirate', 'resources/characters/npc/Kosmo/girl8.webp', "tall"),
                                        declare('kosmo_girl_noble', 'resources/characters/npc/Kosmo/girl9.webp', "tall"),
                                        declare('kosmo_girl_machine', 'resources/characters/npc/Kosmo/girl10.webp', "tall"),
                                        declare('kosmo_girl_machine2', 'resources/characters/npc/Kosmo/girl11.webp', "tall"),
                                        declare('kosmo_twins', 'resources/characters/npc/Kosmo/twins.webp', "tall"),
                                        ]),


                                ("shalia", [
                                        declare('shalia', 'resources/characters/npc/shalia/body (1).webp', "tall"),
                                        declare('shalia2', 'resources/characters/npc/shalia/body (2).webp', "tall"),
                                        declare('shalia3', 'resources/characters/npc/shalia/body (3).webp', "tall"),
                                        declare('shalia4', 'resources/characters/npc/shalia/body (4).webp', "tall"),
                                        declare('shalia5', 'resources/characters/npc/shalia/body (5).webp', "tall"),
                                        declare('shalia6', 'resources/characters/npc/shalia/body (6).webp', "tall"),
                                        declare('side shalia', 'resources/characters/npc/shalia/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("roz", [
                                        declare("roz", "resources/characters/npc/Roz/body.webp", "tall"),
                                        declare("side roz", "resources/characters/npc/Roz/portrait.webp", 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare("roz party", Composite(
                                            (yres(860), yres(768)),
                                            (0, yres(60)), ProportionalScale("resources/characters/npc/Roz/body.webp"),
                                            (yres(520), yres(15)), im.Scale("resources/characters/npc/Misc/Party hat.webp", yres(210), yres(210)),
                                            ))
                                        ]),

                                ("carpenter", [
                                        declare('carpenter', 'resources/characters/npc/carpenter/body.webp', "tall"),
                                        declare('carpenter normal', 'resources/characters/npc/carpenter/body.webp', "tall", gallery=False),
                                        declare('carpenter attack', 'resources/characters/npc/carpenter/attack.webp', "tall"),
                                        declare('carpenter attack2', 'resources/characters/npc/carpenter/attack2.webp', "med"),
                                        declare('carpenter lingerie', 'resources/characters/npc/carpenter/body lingerie.webp', "tall"),
                                        declare('side carpenter', 'resources/characters/npc/carpenter/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("bast", [
                                        declare('bast', 'resources/characters/npc/bast/body.webp', "tall"),
                                        declare('side bast', 'resources/characters/npc/bast/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("banker", [
                                        declare('banker', 'resources/characters/npc/banker/body.webp', "tall"),
                                        declare('banker normal', 'resources/characters/npc/banker/body.webp', "tall", gallery=False),
                                        declare('banker appears happy', 'resources/characters/npc/banker/appear happy.webp', "tall"),
                                        declare('banker appears mad', 'resources/characters/npc/banker/appear mad.webp', "tall"),
                                        declare('banker cheerleader', 'resources/characters/npc/banker/cheerleader.webp', "tall"),
                                        declare('side banker', 'resources/characters/npc/banker/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("taxgirl", [
                                        declare('taxgirl', 'resources/characters/npc/taxgirl/body.webp', "tall"),
                                        declare('side taxgirl', 'resources/characters/npc/taxgirl/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("riche", [
                                        declare('riche', 'resources/characters/npc/riche/body.webp', "tall"),
                                        declare('side riche', 'resources/characters/npc/riche/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("ramias", [
                                        declare('ramias', 'resources/characters/npc/ramias/body.webp', "tall"),
                                        declare('ramias attack', 'resources/characters/npc/ramias/body3.webp', "tall"),
                                        declare('side ramias', 'resources/characters/npc/ramias/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("gurigura", [
                                        declare('gurigura', 'resources/characters/npc/gurigura/body.webp', "tall"),
                                        declare('gurigura attack', 'resources/characters/npc/gurigura/body3.webp', "tall"),
                                        declare('gurigura_attack', 'resources/characters/npc/gurigura/attack.webp', 'p', wide=True),
                                        declare('side gurigura', 'resources/characters/npc/gurigura/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("katryn", [
                                        declare('katryn', 'resources/characters/npc/katryn/body.webp', "tall"),
                                        declare('side katryn', 'resources/characters/npc/katryn/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("giftgirl", [
                                        declare('giftgirl', 'resources/characters/npc/gift girl/body.webp', "tall"),
                                        declare('side giftgirl', 'resources/characters/npc/gift girl/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("today", [
                                        declare('today', 'resources/characters/npc/twins/body.webp', "med"),
                                        declare('side today', 'resources/characters/npc/twins/today portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('bg twins', 'resources/characters/npc/twins/bg.webp', "p"),
                                        ]),

                                ("yesterday", [
                                        declare('yesterday', 'resources/characters/npc/twins/body.webp', "med"),
                                        declare('side yesterday', 'resources/characters/npc/twins/yesterday portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("kenshin", [
                                        declare('kenshin', 'resources/characters/npc/kenshin/body.webp', "tall"),
                                        declare('kenshin normal', 'resources/characters/npc/kenshin/body.webp', "tall", gallery=False),
                                        declare('kenshin blush', 'resources/characters/npc/kenshin/body.webp', "tall", gallery=False),
                                        declare('kenshin annoyed', 'resources/characters/npc/kenshin/body.webp', "tall", gallery=False),
                                        declare('side kenshin', 'resources/characters/npc/kenshin/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side kenshin normal', 'resources/characters/npc/kenshin/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side kenshin blush', 'resources/characters/npc/kenshin/portrait blush.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side kenshin annoyed', 'resources/characters/npc/kenshin/portrait annoyed.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("homura", [
                                        declare('homura', 'resources/characters/npc/homura/body.webp', "p"),
                                        declare('homura normal', 'resources/characters/npc/homura/body.webp', "p", gallery=False),
                                        declare('homura blush', 'resources/characters/npc/homura/body blush.webp', "p"),
                                        declare('homura surprise', 'resources/characters/npc/homura/body surprise.webp', "p"),
                                        declare('homura sad', 'resources/characters/npc/homura/body sad.webp', "p"),
                                        declare('homura naked', 'resources/characters/npc/homura/body naked.webp', "p"),
                                        declare('homura ninja', 'resources/characters/npc/homura/body ninja.webp', "p"),
                                        declare('homura attack', 'resources/characters/npc/homura/body attack.webp', "p"),
                                        declare('side homura', 'resources/characters/npc/homura/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side homura normal', 'resources/characters/npc/homura/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side homura blush', 'resources/characters/npc/homura/portrait blush.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side homura surprise', 'resources/characters/npc/homura/portrait surprise.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side homura sad', 'resources/characters/npc/homura/portrait sad.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side homura naked', 'resources/characters/npc/homura/portrait naked.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side homura ninja', 'resources/characters/npc/homura/portrait ninja.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side homura sepia', 'resources/characters/npc/homura/portrait ninja.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False, sepia=True),
                                        declare('side homura attack', 'resources/characters/npc/homura/portrait ninja.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False, sepia=True),
                                        ]),

                                ("suzume", [
                                        declare('suzume', 'resources/characters/npc/suzume/body.webp', "tall"),
                                        declare('suzume normal', 'resources/characters/npc/suzume/body.webp', "tall", gallery=False),
                                        declare('suzume doubt', 'resources/characters/npc/suzume/body.webp', "tall", gallery=False),
                                        declare('suzume bend', 'resources/characters/npc/suzume/body bend.webp', "tall"),
                                        declare('suzume naked', 'resources/characters/npc/suzume/body naked.webp', "tall"),
                                        declare('suzume naked2', 'resources/characters/npc/suzume/body naked2.webp', "tall"),
                                        declare('suzume shrewd', 'resources/characters/npc/suzume/body.webp', "tall", gallery=False),
                                        declare('suzume ninja', 'resources/characters/npc/suzume/attack.webp', "tall"),
                                        declare('side suzume', 'resources/characters/npc/suzume/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side suzume normal', 'resources/characters/npc/suzume/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side suzume doubt', 'resources/characters/npc/suzume/portrait doubt.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side suzume bend', 'resources/characters/npc/suzume/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side suzume naked', 'resources/characters/npc/suzume/portrait shrewd.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side suzume naked2', 'resources/characters/npc/suzume/portrait naked2.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side suzume shrewd', 'resources/characters/npc/suzume/portrait shrewd.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("kunoichi", [
                                        declare('haruka', 'resources/characters/npc/kunoichi/haruka/body.webp', "tall"),
                                        declare('haruka_humble', 'resources/characters/npc/kunoichi/haruka/body2.webp', "tall"),
                                        declare('haruka_swimsuit', 'resources/characters/npc/kunoichi/haruka/body3.webp', "tall"),
                                        declare('haruka normal', 'resources/characters/npc/kunoichi/haruka/body.webp', "tall", gallery=False),
                                        declare('haruka surprise', 'resources/characters/npc/kunoichi/haruka/body.webp', "tall", gallery=False),
                                        declare('haruka angry', 'resources/characters/npc/kunoichi/haruka/body.webp', "tall", gallery=False),
                                        declare('haruka happy', 'resources/characters/npc/kunoichi/haruka/body.webp', "tall", gallery=False),
                                        declare('haruka sad', 'resources/characters/npc/kunoichi/haruka/body.webp', "tall", gallery=False),
                                        declare('haruka blush', 'resources/characters/npc/kunoichi/haruka/body.webp', "tall", gallery=False),
                                        declare('haruka defiant', 'resources/characters/npc/kunoichi/haruka/body.webp', "tall", gallery=False),
                                        declare('side haruka', 'resources/characters/npc/kunoichi/haruka/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side haruka normal', 'resources/characters/npc/kunoichi/haruka/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side haruka ninja', 'resources/characters/npc/kunoichi/haruka/portrait ninja.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side haruka surprise', 'resources/characters/npc/kunoichi/haruka/portrait surprise.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side haruka angry', 'resources/characters/npc/kunoichi/haruka/portrait angry.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side haruka happy', 'resources/characters/npc/kunoichi/haruka/portrait happy.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side haruka sad', 'resources/characters/npc/kunoichi/haruka/portrait sad.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side haruka blush', 'resources/characters/npc/kunoichi/haruka/portrait blush.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side haruka defiant', 'resources/characters/npc/kunoichi/haruka/portrait defiant.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('haruka_defeated', 'resources/characters/npc/kunoichi/haruka/defeat.webp', "p"),

                                        declare('subaru', 'resources/characters/npc/kunoichi/subaru/subaru.webp', "tall"),
                                        declare('subaru2', 'resources/characters/npc/kunoichi/subaru/subaru2.webp', "tall"),
                                        declare('subaru evil hidden', 'resources/characters/npc/kunoichi/subaru/evil1.webp', "tall"),
                                        declare('subaru evil', 'resources/characters/npc/kunoichi/subaru/evil2.webp', "tall"),
                                        declare('side subaru', 'resources/characters/npc/kunoichi/subaru/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side subaru evil', 'resources/characters/npc/kunoichi/subaru/portrait evil.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),

                                        declare('narika', 'resources/characters/npc/kunoichi/narika/body.webp', "tall"),
                                        declare('narika normal', 'resources/characters/npc/kunoichi/narika/body.webp', "tall", gallery=False),
                                        declare('narika shy', 'resources/characters/npc/kunoichi/narika/body.webp', "tall", gallery=False),
                                        declare('narika angry', 'resources/characters/npc/kunoichi/narika/body.webp', "tall", gallery=False),
                                        declare('narika happy', 'resources/characters/npc/kunoichi/narika/body.webp', "tall", gallery=False),
                                        declare('narika sad', 'resources/characters/npc/kunoichi/narika/body.webp', "tall", gallery=False),
                                        declare('narika blush', 'resources/characters/npc/kunoichi/narika/body.webp', "tall", gallery=False),
                                        declare('narika ninja', 'resources/characters/npc/kunoichi/narika/attack.webp', "tall"),
                                        declare('narika school', 'resources/characters/npc/kunoichi/narika/body school.webp', "tall"),
                                        declare('side narika', 'resources/characters/npc/kunoichi/narika/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side narika normal', 'resources/characters/npc/kunoichi/narika/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side narika ninja', 'resources/characters/npc/kunoichi/narika/portrait ninja.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side narika shy', 'resources/characters/npc/kunoichi/narika/portrait shy.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side narika angry', 'resources/characters/npc/kunoichi/narika/portrait angry.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side narika happy', 'resources/characters/npc/kunoichi/narika/portrait happy.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side narika sad', 'resources/characters/npc/kunoichi/narika/portrait sad.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side narika blush', 'resources/characters/npc/kunoichi/narika/portrait blush.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),

                                        declare('mizuki', 'resources/characters/npc/kunoichi/mizuki/body.webp', "p"),
                                        declare('mizuki_rest', 'resources/characters/npc/kunoichi/mizuki/body rest.webp', "p"),
                                        declare('mizuki normal', 'resources/characters/npc/kunoichi/mizuki/body.webp', "p", gallery=False),
                                        declare('mizuki naked', 'resources/characters/npc/kunoichi/mizuki/body naked.webp', "p"),
                                        declare('mizuki happy', 'resources/characters/npc/kunoichi/mizuki/body.webp', "p", gallery=False),
                                        declare('mizuki sad', 'resources/characters/npc/kunoichi/mizuki/body.webp', "p", gallery=False),
                                        declare('mizuki angry', 'resources/characters/npc/kunoichi/mizuki/body.webp', "p", gallery=False),
                                        declare('side mizuki', 'resources/characters/npc/kunoichi/mizuki/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side mizuki normal', 'resources/characters/npc/kunoichi/mizuki/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side mizuki ninja', 'resources/characters/npc/kunoichi/mizuki/portrait ninja.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side mizuki happy', 'resources/characters/npc/kunoichi/mizuki/portrait happy.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side mizuki sad', 'resources/characters/npc/kunoichi/mizuki/portrait sad.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side mizuki angry', 'resources/characters/npc/kunoichi/mizuki/portrait angry.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side mizuki naked', 'resources/characters/npc/kunoichi/mizuki/portrait naked.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),

                                        declare('kunoichi', 'resources/characters/npc/kunoichi/kunoichi.webp', "tall", gallery=False),
                                        declare('kunoichi reversed', 'resources/characters/npc/kunoichi/kunoichi.webp', "tall", flip=True, gallery=False),
                                        declare('side kunoichi', 'resources/characters/npc/kunoichi/kunoichi portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("receptionist", [
                                        declare('receptionist', 'resources/characters/npc/receptionist/body.webp', "tall"),
                                        declare('receptionist normal', 'resources/characters/npc/receptionist/body.webp', "tall", gallery=False),
                                        declare('receptionist glasses', 'resources/characters/npc/receptionist/body glasses.webp', "tall"),
                                        declare('side receptionist', 'resources/characters/npc/receptionist/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side receptionist normal', 'resources/characters/npc/receptionist/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side receptionist glasses', 'resources/characters/npc/receptionist/portrait glasses.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("shizuka", [
                                        declare('shizuka', 'resources/characters/npc/shizuka/body.webp', "tall"),
                                        # declare('shizuka normal', 'resources/characters/npc/shizuka/body.webp', "tall", gallery=False),
                                        # declare('shizuka jaded', 'resources/characters/npc/shizuka/body2.webp', "tall"),
                                        # declare('shizuka surprise', 'resources/characters/npc/shizuka/body3.webp', "tall"),
                                        # declare('shizuka smile', 'resources/characters/npc/shizuka/body4.webp', "tall"),
                                        declare('side shizuka', 'resources/characters/npc/shizuka/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                            # Extras
                                ('gknight', [declare('gknight', 'resources/characters/npc/Misc/girl_knight.webp', "small"),]),
                                ('princess1', [declare('princess1', 'resources/characters/npc/Misc/princess1.webp', "small"),]),
                                ('princess2', [declare('princess2', 'resources/characters/npc/Misc/princess2.webp', "small"),]),
                                ('priest', [declare('priest', 'resources/characters/npc/Misc/priest.webp', "small"),]),
                                ('mage', [declare('mage', 'resources/characters/npc/Misc/mage.webp', "small"),]),
                                ('bm1', [declare('bm1', 'resources/characters/npc/Misc/bm1.webp', "small"),]),
                                ('bm2', [declare('bm2', 'resources/characters/npc/Misc/bm2.webp', "small"),]),
                                ('king', [declare('king', 'resources/characters/npc/Misc/king2.webp', "med"),]),
                                ('hood', [declare('hood', 'resources/characters/npc/Misc/hood.webp', "small"),]),
                                ('old elf', [declare('old_elf', 'resources/characters/npc/Misc/old elf.webp', "small"),]),
                                ('hermit', [declare('hermit', 'resources/characters/npc/Misc/hermit.webp', "tall"),]),
                                ('clerk', [declare('clerk', 'resources/characters/npc/Misc/clerk.webp', "med"),]),

                                ("guard", [
                                        declare('guard', 'resources/characters/npc/Misc/guard.webp', "p"),
                                        declare('side guard', 'resources/characters/npc/Misc/guard portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare("guard party", im.Composite(
                                            (yres(315), yres(768)),
                                            (0, 0), im.Scale("resources/characters/npc/Misc/guard.webp", yres(315), yres(768)),
                                            (yres(140), yres(75)), im.Scale("resources/characters/npc/Misc/Party hat.webp", yres(125), yres(125)),
                                            )), "p",
                                        ]),

                                ("thugs", [
                                        declare('side thug', 'resources/ui/customers/thug.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),

                                        declare('thug1', 'resources/characters/npc/Misc/thug1.webp', "tall"),
                                        declare('thug1 attack', 'resources/characters/npc/Misc/thug1 attack.webp', "tall"),
                                        declare('side thug1', 'resources/characters/npc/Misc/thug1 portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),

                                        declare('thug2', 'resources/characters/npc/Misc/thug2.webp', "tall"),
                                        declare('thug2 attack', 'resources/characters/npc/Misc/thug2 attack.webp', "tall"),
                                        declare('side thug2', 'resources/characters/npc/Misc/thug2 portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('thug2 burnt', 'resources/characters/npc/Misc/burnt.webp', "tall"),

                                        declare('thugs attack', 'resources/characters/npc/Misc/thugs attack.webp', "tall"),
                                        ]),


                                ("henchman", [declare('henchman', 'resources/characters/npc/Misc/henchman.webp', "tall")]),
                                ("masked thug", [declare('masked_thug', 'resources/characters/npc/Misc/masked thug.webp', "tall")]),
                                ("stranger", [declare('stranger', 'resources/characters/npc/Misc/stranger.webp', "tall")]),
                                ("sewer rapist", [declare('sewer_rapist', 'resources/characters/npc/Misc/sewer rapist.webp', "tall")]),
                                ("judge", [declare('judge', 'resources/characters/npc/Misc/judge.webp', "tall"), declare('side judge', 'resources/characters/npc/Misc/judge portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),]),
                                ("warden", [declare('warden', 'resources/characters/npc/Misc/warden.webp', "tall"), declare('side warden', 'resources/characters/npc/Misc/warden portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),]),
                                ("knight", [declare('knight', 'resources/characters/npc/Misc/knight.webp', "tall"), declare('side knight', 'resources/characters/npc/Misc/knight portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),]),
                                ("hound knight", [declare('hound_knight', 'resources/characters/npc/Misc/hound knight.webp', "tall"), declare('side hound_knight', 'resources/characters/npc/Misc/knight portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),]),
                                ("hound leader", [declare('hound_leader', 'resources/characters/npc/Misc/hound leader.webp', "tall"), declare('side hound_leader', 'resources/characters/npc/Misc/hound leader portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),]),
                                ("noroi", [declare('noroi', 'resources/characters/npc/Misc/noroi.webp', "tall"), declare('side noroi', 'resources/characters/npc/Misc/noroi portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),]),
                                ("noroi leader", [declare('noroi_leader', 'resources/characters/npc/Misc/noroi captain.webp', "tall"), declare('side noroi_leader', 'resources/characters/npc/Misc/noroi captain portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),]),


                                ("templars", [
                                        declare('templar', 'resources/characters/npc/Misc/templar.webp', "tall"),
                                        declare('initiate', 'resources/characters/npc/Misc/initiate.webp', "tall"),
                                        declare('side templar', 'resources/characters/npc/Misc/knight portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side initiate', 'resources/characters/npc/Misc/soldier portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ('lost soldier', [declare('lost_soldier', 'resources/characters/npc/Misc/lost soldier.webp', "med"),]),

                                ("monsters", [
                                        declare('spirit', 'resources/characters/npc/Misc/spirit.webp', 'p', wide=True),
                                        declare('side spirit', 'resources/characters/npc/Misc/spirit portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('sewer_monster', 'resources/characters/npc/Misc/sewer monster.webp', "small"),
                                        declare('sewer_monster happy', 'resources/characters/npc/Misc/sewer monster friendly.webp', "small"),
                                        declare('tentacle_monster', 'resources/characters/npc/Misc/tentacle_monster.webp', "med"),
                                        ]),

                                ("mare", [
                                        declare('mare', 'resources/characters/npc/Misc/mare.webp', "tall"),
                                        ]),

                                ("demons", [
                                        declare('blue_demon', 'resources/characters/npc/Misc/blue demon.webp', "tall"),
                                        declare('side blue_demon', 'resources/characters/npc/Misc/blue demon portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('red_demon', 'resources/characters/npc/Misc/red demon.webp', "tall"),
                                        declare('side red_demon', 'resources/characters/npc/Misc/red demon portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("skeleton", [
                                        declare('skeleton', 'resources/characters/npc/Misc/skeleton.webp', "med"),
                                        declare('side skeleton', 'resources/characters/npc/Misc/skeleton portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ]),

                                ("golem", [declare('golem', 'resources/characters/npc/Misc/golem.webp', "p"), declare('side golem', 'resources/characters/npc/Misc/golem portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),]),

                                ("ogres", [declare('ogre', 'resources/characters/npc/Misc/ogre.webp', "p")]),

                                ("mask", [declare('mask', 'resources/characters/npc/The Mask/body.webp', "tall"),
                                        declare('mask blind', 'resources/characters/npc/The Mask/body blind.webp', "tall"),
                                        declare('mask attack', 'resources/characters/npc/The Mask/attack.webp', "tall"),
                                        declare('mask blind attack', 'resources/characters/npc/The Mask/blind attack.webp', "tall"),
                                        declare('side mask unknown', 'resources/characters/npc/Misc/killer.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side mask', 'resources/characters/npc/The Mask/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side mask blind', 'resources/characters/npc/The Mask/portrait blind.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side mask normal', 'resources/characters/npc/The Mask/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False)]),

                                ("ninja guests", [declare('hokoma_warrior', 'resources/characters/npc/kunoichi/guests/guest1.webp', "tall"), declare('magical_girl', 'resources/characters/npc/kunoichi/guests/guest2.webp', "tall"), declare('girl_scientist', 'resources/characters/npc/kunoichi/guests/guest3.webp', "tall")]),

                            ])

    game_image_dict["unused"] = {

                                "unused for gallery (stand-alone portraits)" : [
                                        declare('side slavegirl1', 'resources/characters/npc/Misc/slave1.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side slavegirl2', 'resources/characters/npc/Misc/slave2.webp', 's', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side shopgirl', 'resources/characters/npc/Misc/shop_girl.webp', 's', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side hmas', 'resources/characters/npc/Hmas/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side raccoon', 'resources/characters/npc/Misc/raccoon.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side sailor', 'resources/characters/npc/Misc/sailor.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side party_girl', 'resources/characters/npc/Misc/party girl.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side nun', 'resources/characters/npc/Misc/nun.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side kimono_lady', 'resources/characters/npc/Misc/kimono lady.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side young_maid', 'resources/characters/npc/Misc/maid.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side diplomat', 'resources/characters/npc/Misc/diplomat.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side sorceress', 'resources/characters/npc/Misc/sorceress.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side naked_lady', 'resources/characters/npc/Misc/naked lady.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('judge_head', 'resources/characters/npc/Misc/judge head.webp', "small"),
                                        declare('panties', 'resources/items/accessory/lace panties.webp', "small"),
                                        declare_multiple('house%s', 'resources/minigame/house%s.webp', 'p', x=xres(90), start=1, finish=8),
                                        declare_multiple('passerby%s', 'resources/minigame/passerby%s.webp', 'p', x=xres(80), start=1, finish=9),
                                        declare_multiple('ninja%s', 'resources/minigame/ninja%s.webp', 'p', x=xres(80), start=0, finish=3),
                                        declare_multiple('guest%s', 'resources/minigame/guest%s.webp', 'p', x=xres(80), start=1, finish=3),
                                        declare('toy hammer', 'resources/items/Weapons/toy hammer.png', 'p', x=xres(32), y=yres(32), gallery=False),
                                        declare('side papa', 'resources/characters/npc/Misc/freak portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side papa_apprentice', 'resources/characters/npc/Misc/freak apprentice.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side demonette', 'resources/characters/npc/Misc/demonette.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side hanny', 'resources/characters/npc/Misc/hanny.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side crying_man', 'resources/characters/npc/Misc/crying man.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side chaos', 'resources/characters/npc/Chaos/portrait.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        declare('side scribe', 'resources/characters/npc/Misc/scribe.webp', 'p', x=res_portrait_size, y=res_portrait_size, gallery=False),
                                        ],

                                "UI elements" : [
                                        declare('success', "resources/ui/challenges/success.webp", 's', gallery=False),
                                        declare('failure', "resources/ui/challenges/failure.webp", 's', gallery=False)

                                ],

                            }

    ## MISC PICTURES ##

    game_image_dict["Misc"] = {

                                "title" : [declare("bg title", "ui/theme.webp", "p", wide=True, unlock=True)],

                                "night" : ["resources/events/" + p for p in night_pics + no_girls_pics],

                                "advertising" : ["resources/events/" + p for p in advertising_pics[1]], # Update when more advertising levels are available

                                "pony" : ["resources/events/" + p for p in pony_pics],

                                "security" : ["resources/events/" + p for p in sum((security_pics.values()), [])] + [declare('side security', 'resources/ui/shield.webp', 's', x=res_portrait_size, y=res_portrait_size, gallery=False),]+ [declare('side security_breach', 'resources/ui/broken shield.webp', 's', x=res_portrait_size, y=res_portrait_size, gallery=False),],

                                "arson" : ["resources/events/" + p for p in arson_pics],

                                "violent" : ["resources/events/" + p for p in violent_pics] + [
                                        declare('bg murder', 'resources/backgrounds/murder.webp', 'p'),
                                        ],

                                "treasure" : ["resources/events/" + p for p in sum((treasure_pics.values()), [])],

                                "jobs" : [
                                        declare('bg waitress', 'resources/backgrounds/waitress.webp', 'p', wide=True, unlock=True),
                                        declare('bg stripper', 'resources/backgrounds/stripper.webp', 'p', wide=True, unlock=True),
                                        declare('bg masseuse', 'resources/backgrounds/masseuse.webp', 'p', wide=True, unlock=True),
                                        declare('bg geisha', 'resources/backgrounds/geisha.webp', 'p', wide=True, unlock=True),
                                        declare('bg whore', 'resources/backgrounds/whore.webp', 'p', wide=True, unlock=True),
                                        declare('bg rest', 'resources/backgrounds/rest.webp', 'p', wide=True, unlock=True),
                                        ],
                                "zodiac" : [declare('bg zodiac', 'resources/backgrounds/zodiac.webp', 'p'),],

                                "tavern" : [
                                        declare('bg tavern_man', 'resources/characters/npc/Misc/tavern_man.webp', 'p'),
                                        declare('symbol', 'resources/backgrounds/thief symbol.webp'),
                                        ],

                                "elves" : [declare('bg elves', 'resources/backgrounds/elves.webp', 'p')],

                                "mages" : [declare('bg magicU_students', 'resources/backgrounds/magic students.webp', 'p')],

                                "mask events" : [declare('bg mask escape', 'resources/characters/npc/The Mask/escape.webp', 'p')] + [declare('bg mask driver1', 'resources/characters/npc/The Mask/driver1.webp', "p"), declare('bg mask driver2', 'resources/characters/npc/The Mask/driver2.webp', "p"),] + [declare('mask showdown', 'resources/characters/npc/The Mask/showdown.webp', 'p')] + declare_multiple("bg mask_duel%s", "resources/characters/npc/The Mask/fire duel%s.webp", "p", start=1, finish=2) + declare_multiple("bg mask_duel%s blind", "resources/characters/npc/The Mask/fire duel blind%s.webp", "p", start=1, finish=2),

                                "mask flashbacks" : declare_multiple("bg c3_flashback%s", "resources/characters/npc/The Mask/flashback%s.webp", "p", start=0, finish=10) + [declare('bg mask rooftop', 'resources/characters/npc/Homura/rooftop.webp', 'p'), declare('bg mask duo', 'resources/characters/npc/Homura/duo.webp', 'p')],

                                "c3 showdown" : [declare('bg showdown all', 'resources/characters/npc/kunoichi/showdown all.webp', 'p')],

                                "c3 kosmo" : declare_multiple("bg kosmo fall%s", "resources/characters/npc/Kosmo/rail%s.webp", "p", start=1, finish=2),

                                "succubi" : declare_multiple('bg succubi%s', 'resources/events/succubi (%s).webp', 'p', start=1, finish=6),

                                "oni" : declare_multiple('bg oni%s', 'resources/events/oni (%s).webp', 'p', start=1, finish=3),

                                "hannies" : declare_multiple('bg hannies%s', 'resources/events/hannies (%s).webp', 'p', start=1, finish=5),

                                "pets" : declare_multiple('bg pet%s', 'resources/characters/npc/misc/pets/bg pet (%s).webp', 'p', start=1, finish=4),

                                "demon service" : declare_multiple('demon service%s', 'resources/events/demon service (%s).webm', 'p', start=1, finish=4, wide=True),

                                "demon sex" : declare_multiple('demon sex%s', 'resources/events/demon sex (%s).webm', 'p', start=1, finish=6, wide=True),

                                "subaru kill" : [declare('bg subaru kill', 'resources/characters/npc/kunoichi/subaru/kill.webp', 'p')],

                                "old_general" : [declare('bg old_general', 'resources/characters/npc/Misc/old general.webp', 'p', wide=True)],

                                "arios" : [declare('bg arios', 'resources/characters/npc/Misc/arios.webp', 'p', wide=True), declare('bg arios_evil', 'resources/characters/npc/Misc/arios evil.webp', 'p'),],

                                "misc" : [declare('bg letter', 'resources/backgrounds/letter.webp', 'p', gallery=False)],

                            }


#### GALLERY CREATION ####

    ## Game event Gallery layout ##

    # Lists all tabs and keys/buttons in the Game CG gallery as (tab, buttons) tuples

    ev_gallery_list = ["Characters", "Story", "Backgrounds", "Misc"]

#     ev_gallery_list = [
#                        ("Characters", ["sill", "kurohime", "maid", "gio", "kosmo", "kosmo girls", "gizel",
#                                        "maya", "roz", "lieutenant", "sergeant", "renza", "satella", "shalia", "captain", "sewer woman",
#                                        "goldie", "willow", "gina", "stella", "shopgirl", "jobgirl", "carpenter", "banker",
#                                        "guard", "thugs", "king", "princess1", "princess2", "gknight", "priest", "mage", "bm1", "bm2", "hood", "henchman",
#                                        "masked thug", "stranger", "sewer rapist", "judge", "templars", "milkmaid", "mare", "monsters",
#                                        "demons", "skeleton", ]),
#                        ("Story", ["intro", "sill intro", "sill sex1", "sill gio_fuck", "maid sex", "renza sex", "satella soft1", "satella soft2", "satella soft3", "satella sex1", "satella sex2", "satella sex3", "shalia soft", "shalia fj", "hmas",
#                                   "gizel soft", "gizel rape", "gizel sex1", "gizel sex2", "gizel sex3", "gizel sex4", "gizel sex5", "gizel sex6",
#                                   "goldie soft", "goldie sex1", "goldie sex2", "goldie sex3", "willow soft", "gina soft", "stella soft",
#                                   "sewer rape", "sewer girl sex", "treasure sex1", "treasure sex2", "banker titjob", "banker sex"]),
#                        ("Backgrounds", ["sky", "inside", "outside", "slavemarket", "districts", "locations", "brothels", "rooms", "farm", ]),
#                        ("Misc.", ["title", "jobs", "zodiac", "night", "pony", "security", "violent", "arson", "treasure", "tavern", "elves"]),
#                       ]

    ## Gallery init ##

    def init_galleries():

        lock = ProportionalScale("resources/ui/lock.webp", 100, 100)

        global ev_gallery
        global gp_gallery

        ## Game event gallery

        ev_gallery = defaultdict(str)

        # Gallery options

        for g in ev_gallery_list:
            ev_gallery[g] = Gallery()
            ev_gallery[g].slideshow_delay = 1.0
            ev_gallery[g].navigation=True
            ev_gallery[g].locked_button=lock
            ev_gallery[g].unlocked_advance=True
            ev_gallery[g].blist = [] # Not a native attribute for the Gallery object
            ev_gallery[g].pics = {} # Not a native attribute for the Gallery object

        # Gallery buttons

            for b in game_image_dict[g].keys():
                pics = game_image_dict[g][b]
                if pics:
                    ev_gallery[g].blist.append(b)
                    ev_gallery[g].button(b)
                    for p in pics:
                        if p:
                            ev_gallery[g].image(p)
                            ev_gallery[g].condition("was_seen('" + p + "')")

        # Auto girl pack galleries

        gp_gallery = defaultdict(str)

        for pack in GirlFilesDict.get_paths():
            path = GirlFilesDict.get_path_dict()[pack]

            gp_gallery[pack] = Gallery()
            gp_gallery[pack].blist = []

            gp_gallery[pack].slideshow_delay = 1.0
            gp_gallery[pack].navigation=True
            gp_gallery[pack].span_buttons=True
            gp_gallery[pack].unlocked_advance=False # Unfortunately, unlocked advance is broken as of now.
            gp_gallery[pack].locked_button=lock

            for file in [f for f in renpy.list_files() if f.startswith(path) and is_imgfile(f, video=False)]:
                gp_gallery[pack].button(file)
                gp_gallery[pack].condition("was_seen('" + file + "')")
                gp_gallery[pack].image(ProportionalScale(file, config.screen_width, config.screen_height)) # file
                gp_gallery[pack].blist.append(file)


#### CUSTOM TRANSITIONS ####

image white = "#FFF"

image noise1 = im.Scale("resources/transitions/noise1.png", config.screen_width, config.screen_height)
image noise2 = im.Scale("resources/transitions/noise2.png", config.screen_width, config.screen_height)
image noise3 = im.Scale("resources/transitions/noise3.png", config.screen_width, config.screen_height)
image noise4 = im.Scale("resources/transitions/noise4.png", config.screen_width, config.screen_height)

define circleout = ImageDissolve(im.Scale("resources/transitions/id_circleiris.webp", config.screen_width, config.screen_height), 2.0)

define circlein = ImageDissolve(im.Scale("resources/transitions/id_circleiris.webp", config.screen_width, config.screen_height), 2.0, reverse = True)

define burn_it = ImageDissolve(im.Scale("resources/transitions/shear.png", config.screen_width, config.screen_height), 1.2)

define dream = ImageDissolve(im.Scale("resources/transitions/imagedissolve dream.png", config.screen_width, config.screen_height), 2.0, 64)

define satella_blink = ImageDissolve(im.Scale("resources/characters/npc/Satella/body2.webp", config.screen_width, config.screen_height), 2.0, reverse = True) # AlphaDissolve("resources/characters/npc/Satella/body2.webp", delay=1.0, alpha=True, reverse=False)

# From the 'Utsukushii Effects' renpy tutorial
define flashbackin = ImageDissolve(im.Scale("resources/transitions/zigzag.webp", config.screen_width, config.screen_height), 1.5, 50)
define flashbackout = ImageDissolve(im.Scale("resources/transitions/zigzag.webp", config.screen_width, config.screen_height), 1.5, 50, reverse=True)
##

define flash = Fade(0.1, 0.0, 0.5, color="#fff")

define doubleflash = MultipleTransition([True, Fade(0.1, 0.0, 0.5, color="#fff"), True, Fade(0.1, 0.0, 0.5, color="#fff"), True])

define fastdissolve = Dissolve(0.1)
define fastfade = Fade(0.15, 0.0, 0.15)

#### CUSTOM TRANSFORMS ####

transform sepia:
    align (0.5, 0.0)
    matrixcolor SepiaMatrix()

transform top_color:
    align (0.5, 0.0)
    matrixcolor IdentityMatrix()

transform desaturate:
    matrixcolor SaturationMatrix(0)

transform red_saturate:
    matrixcolor TintMatrix("#a00")

transform alpha_transform:
    alpha 0.7
    on hover:
        linear 0.15 alpha 1.0
    on idle:
        linear 0.15 alpha 0.7
    on selected_hover:
        linear 0.15 alpha 1.0
    on selected_idle:
        linear 0.15 alpha 0.7

#### CG GALLERY ####

init -3 python:

    def was_seen(pic): # Where pic is a String, either a file path or a renpy image name

        if pic:
            if is_imgfile(pic, video=False): # Disables videos until we can find a way to make them show in CG gallery
                if pic in persistent.seen_list:
                    return True

            elif renpy.seen_image(pic) or pic in persistent.seen_list: # These are renpy images and not filenames
                if not is_videofile(pic):
                    return True

        return False

    def get_gallery_unlock_rate(gal_type, gal, name):
        if gal_type == "ev":
            r = 0
            t = 0

            for b in gal.blist:
                r += sum(1 for pic in game_image_dict[name][b] if was_seen(pic))
                t += sum(1 for pic in game_image_dict[name][b] if pic)

            return r * 100/t

        elif gal_type == "gp":
            return sum(1 for pic in gal.blist if was_seen(pic)) * 100/len(gal.blist)

    def get_button_unlock_rate(but, name):
        return str(sum(1 for pic in game_image_dict[name][but] if was_seen(pic))) + "/" + str(sum(1 for pic in game_image_dict[name][but] if pic))

    def unlock_pic(pic, silent=False):
        if not pic:
            return
        elif is_string(pic):
            path=pic
        elif isinstance(pic, Picture):
            path=pic.path
        elif isinstance(pic, ProportionalScale):
            path=pic.imgname
        else:
            raise AssertionError("Unlock picture: %s not recognized as a string or picture object." % pic)

        if path not in persistent.seen_list:
            persistent.seen_list.append(path)
            if not silent:
                debug_notify("Unlocking " + path)

    def get_gallery_pic(pics):
        for pic in pics:
            if "gallery" in pic:
                return pic



screen galleries():

    tag menu

    key "mouseup_3" action Return()
    key "K_ESCAPE" action Return()

    add "black"
    add "bg title" yalign 0.5

    frame xalign 0.5 yalign 0.5:
        has vbox spacing 10 box_wrap True

        textbutton _("CG - Game") action (ShowMenu("gallery", gal_type="ev"), SetVariable("gallery_type", "ev")) text_size res_font(24) xsize int(config.screen_width*0.1851)

        textbutton _("CG - Girl packs") action (ShowMenu("gallery", gal_type="gp"), SetVariable("gallery_type", "gp")) text_size res_font(24) xsize int(config.screen_width*0.1851)

        # textbutton "Achievements" action ShowMenu("achievements") text_size res_font(24) xsize int(config.screen_width*0.1851)

        textbutton _("Main Menu") action Function(renpy.full_restart) text_size res_font(24) xsize int(config.screen_width*0.1851)


screen gallery_left_menu(gal_type, gal):
    viewport xsize int(config.screen_width*0.1851) mousewheel True draggable True scrollbars "vertical" ysize 0.98 yalign 0.5:
        # add "#000"

        vbox:
            if gal_type == "ev":
                for g in ev_gallery_list:
                    textbutton g action (SetScreenVariable("name", g), SetScreenVariable("gal", ev_gallery[g]), SetScreenVariable("page", 0), SelectedIf(gal==ev_gallery[g])) xsize int(config.screen_width*0.1851) text_size int(config.screen_height*0.025)

            elif gal_type == "gp":
                for pack in GirlFilesDict.get_paths():
                    $ n = get_name(pack, full=True)
                    textbutton n action (SetScreenVariable("name", n), SetScreenVariable("gal", gp_gallery[pack]), SetScreenVariable("page", 0), SelectedIf(gal==gp_gallery[pack])) xsize int(config.screen_width*0.1851) text_size int(config.screen_height*0.025)




screen gallery(gal_type="ev"): # The Gallery object must have a pics variable (a list of renpy displaybles or image files)

    tag menu

    default page=0
    default shown_pics = 12

    default but_sizes = {6 : (360, 300), 12 : (250, 200), 30 : (175, 120), 48 : (130, 100), 80 : (100, 75), 120 : (85, 60)}

    $ but_w = yres(but_sizes[shown_pics][0])
    $ but_h = yres(but_sizes[shown_pics][1])

    if gal_type == "ev":
        default name = "Characters"
        default gal = ev_gallery["Characters"]
    elif gal_type == "gp":
        $ first_pack = GirlFilesDict.get_paths()[0]
        default name = get_name(first_pack, full=True)
        default gal = gp_gallery[first_pack]

    key "mouseup_3" action ShowMenu("galleries")
    key "K_ESCAPE" action ShowMenu("galleries")

    add "#000"
#    add "" xalign 0.5 yalign 0.5

    hbox spacing 10:
        use gallery_left_menu(gal_type, gal)

        vbox spacing 10:

            text name + " (" + str_int(get_gallery_unlock_rate(gal_type, gal, name)) + "%)"

            frame background None:

                id "gallery"

                xsize 1.0
                ysize 0.85

                has hbox box_wrap True spacing 6

                $ index = page*shown_pics

                for i in range(shown_pics):

                    if index+i < len(gal.blist):
                        $ but = gal.blist[index+i]

                        if gal_type == "ev":
                            $ unlocked_pics = [p for p in game_image_dict[name][but] if was_seen(p)]

                            if unlocked_pics:
                                $ first_pic = unlocked_pics[0]
                            else:
                                $ first_pic = "resources/backgrounds/not_found.webp"

                            if is_imgfile(first_pic, video=False):
                                $ pic = first_pic
                            else:
                                $ pic = renpy.get_registered_image(first_pic)

                        else:
                            $ pic = but

                        # if gal_type == "ev":
                        #     if is_imgfile(game_image_dict[name][but][0], video=False):
                        #         $ pic = ProportionalScale(game_image_dict[name][but][0], 240, 180)
                        #     elif game_image_dict[name][but][0]:
                        #         $ pic = ProportionalScale(ImageReference(game_image_dict[name][but][0]), 240, 180)

                        # else:
                        #     $ pic = ProportionalScale(but, 240, 180)

                        frame background None xsize but_w ysize but_h ymargin 6 yalign 0.5:
                            add gal.make_button(but, pic, xpadding=3, ypadding=3, xalign=0.5, yalign=0.5, background=None) hover_alpha 1.0 idle_alpha 0.8 fit "contain"
                            # text str(but)
                            if gal_type == "ev":
                                frame background "#00000055" xalign 0.5 yalign 1.0 ypadding 1:
                                    text get_button_unlock_rate(but, name) size int(config.screen_height*0.02)
                            else:
                                if pic in persistent.pic_ignore_list:
                                    text _("IGNORED") align (0.5, 0.5) color c_red size res_font(16) drop_shadow (2, 2)
                                if persistent.debug_pic_counter and gal_type == "gp":
                                    text _("Used %s times" % persistent.debug_pic_counter_dict[pic]) align (0.5, 1.0) size int(config.screen_height*0.02) #?


            $ max_page = (len(gal.blist)-1) // shown_pics

            text "Page " + str(page+1) + "/" + str(max_page+1) size int(config.screen_height*0.02)

            frame background None xsize 0.8 xalign 1.0:
    #            textbutton "Start Slideshow" action gal.ToggleSlideshow()

                has hbox:

                    textbutton _("Show less"):
                        if shown_pics > list(but_sizes.keys())[0]:
                            action SetScreenVariable("shown_pics", cycle_list(list(but_sizes.keys()), shown_pics, -1))
                    textbutton _("Show more"):
                        if shown_pics < list(but_sizes.keys())[-1]:
                            action SetScreenVariable("shown_pics", cycle_list(list(but_sizes.keys()), shown_pics))

                    if page > 0:
                        key ["K_LEFT", "repeat_K_LEFT", "mousedown_4"]  action SetScreenVariable("page", page-1)
                        textbutton _("Previous") action SetScreenVariable("page", page-1) xalign 0.05
                    if page < max_page:
                        key ["K_RIGHT", "repeat_K_RIGHT", "mousedown_5"] action SetScreenVariable("page", page+1)
                        textbutton _("Next") action SetScreenVariable("page", page+1) xalign 0.9
                    if page < max_page - 10:
                        key "K_PAGEDOWN" action SetScreenVariable("page", page+10)
                    else:
                        key "K_PAGEDOWN" action SetScreenVariable("page", max_page)

                    if page > 10:
                        key "K_PAGEUP" action SetScreenVariable("page", page-10)
                    else:
                        key "K_PAGEUP" action SetScreenVariable("page", 0)

                    key "K_HOME" action SetScreenVariable("page", 0)
                    key "K_END" action SetScreenVariable("page", max_page)

                    textbutton _("Return") action ShowMenu("galleries") xalign 0.5


screen _gallery:

    if locked:
        add "#000"
        text _("Image [index] of [count] locked.") align (0.5, 0.5)
    else:
        add "#000"

        for d in displayables:
            add d xalign 0.5 yalign 1.0 fit "contain"

            if gallery_type == "gp" and d.child.children[0].imgname in persistent.pic_ignore_list:
                text _("IGNORED") align (0.5, 0.5) color c_red size res_font(48) drop_shadow (4, 4)

    if gallery.slideshow:
        timer gallery.slideshow_delay action Return("next") repeat True

    key "game_menu" action gallery.Return()

    if gallery.navigation:
        use gallery_navigation

screen gallery_navigation:
    hbox:
        spacing 20

        style_group "gallery"
        align (.98, .98)

        key "mouseup_3" action gallery.Return()
        key "K_ESCAPE" action gallery.Return()

        if gallery_type == "ev":
            key "K_LEFT" action gallery.Previous(unlocked=True)
            key "repeat_K_LEFT" action gallery.Previous(unlocked=True)
            key 'K_BACKSPACE' action gallery.Previous(unlocked=True)
            key "K_RIGHT" action gallery.Next(unlocked=True)
            key "repeat_K_RIGHT" action gallery.Next(unlocked=True)
            key 'K_SPACE' action gallery.Next(unlocked=True)
            key "K_RETURN" action gallery.ToggleSlideshow()
            key "K_SCROLLOCK" action gallery.ToggleSlideshow()
        else:
            key "mouseup_1" action NullAction() # Blocks mouse clicks for girlpack galleries
            key ['K_DELETE'] action Function(toggle_ignore_pic, d.child.children[0])

        if gallery_type == "ev":
            textbutton _("prev") action gallery.Previous(unlocked=True)
            textbutton _("next") action gallery.Next(unlocked=True)
            textbutton _("slideshow") action gallery.ToggleSlideshow()
        else:
            text str(d.child.children[0].imgname) size res_font(14)
        textbutton _("return") action gallery.Return()

    python:
        style.gallery = Style(style.default)
        style.gallery_button.background = None
        style.gallery_button_text.color = "#666"
        style.gallery_button_text.hover_color = "#fff"
        style.gallery_button_text.selected_color = "#fff"
        style.gallery_button_text.size = int(config.screen_height*0.0148)

#### Pet summons ####

init python:
    for i in range(50):
        renpy.image("weird_pet%i" % i, ConditionSwitch(
            "explode_pet[%i]" % i, "explode",
            "pets_on_fire > %i" % i, "resources/characters/npc/Misc/Pets/pet%i.webp" % renpy.random.randint(2, 3),
            "True", "resources/characters/npc/Misc/Pets/pet1.webp"))

    def small_lightning(trans, st, at):
        global pets_on_fire
        renpy.play(s_fire, "sound")
        pets_on_fire += 1

    def big_lightning(trans, st, at):
        global pets_on_fire
        renpy.play(s_thunder, "sound2")
        pets_on_fire += 2

image evil_lightning:
    zoom 3.0
    yalign 0.0
    choice:
        "resources/minigame/rain/lightning.webp"
        alpha  0.0
        1.2

    choice:
        "resources/minigame/rain/lightning.webp" with vpunch
        xalign 0.0
        alpha  0.0
        linear 0.6 alpha  1.0
        linear 0.6 alpha  0.0
        function small_lightning

    choice:
        "rev_lightning" with vpunch
        xalign 1.0
        alpha  0.0
        linear 0.6 alpha  1.0
        linear 0.6 alpha  0.0
        function big_lightning

    repeat

image explode:
    "resources/characters/npc/Misc/Pets/frame_1.webp"
    pause 0.14
    "resources/characters/npc/Misc/Pets/frame_2.webp"
    pause 0.14
    "resources/characters/npc/Misc/Pets/frame_3.webp"
    pause 0.14
    "resources/characters/npc/Misc/Pets/frame_4.webp"
    pause 0.14
    "resources/characters/npc/Misc/Pets/frame_5.webp"
    pause 0.14
    "resources/characters/npc/Misc/Pets/frame_6.webp"
    pause 0.14
    "resources/characters/npc/Misc/Pets/frame_7.webp"
    pause 0.14
    "resources/characters/npc/Misc/Pets/frame_8.webp"
    pause 0.14

transform falling_pet(x = renpy.random.random(), sz=renpy.random.randint(1, 3)):
    # fall_time cannot be passed as an argument, causes a glitch

    subpixel True

    zpos (3-sz)/3 # Doesn't seem to work

    xalign x
    yalign -0.2
    zoom 0.5 * sz

    parallel:
        linear fall_time * 2.0 yalign 1.4

    parallel:
        choice:
            rotate 0
            linear fall_time / 4 rotate 360
            repeat
        choice:
            rotate 0
            linear fall_time / 4 rotate -360
            repeat
        choice:
            rotate 25
        choice:
            rotate -25


transform falling_pet_die(x = renpy.random.random(), sz=renpy.random.randint(1, 3)):

    subpixel True

    zpos (3-sz)/3 # Doesn't seem to work

    xalign x
    yalign -0.2
    zoom 0.5 * sz

    parallel:
        linear fall_time yalign 0.61 - 0.32*x + 0.075*(1-x)*sz + 0.125 * renpy.random.random() # Causes the best distribution of dead bodies on the bg picture. Trust me, I did a lot of tests!

    parallel:
        choice:
            rotate 0
            linear fall_time / 4 rotate 360
            repeat
        choice:
            rotate 0
            linear fall_time / 4 rotate -360
            repeat
        choice:
            rotate 25
        choice:
            rotate -25

    time fall_time
    rotate 0


screen make_it_rain(finish_em = False): # 50 falling pets

    layer "master"

    default i = 0 # Must be a local variable, otherwise causes glitches
    default t = 1.5 # Pets will appear every t seconds

    if i < 50:
        if finish_em:
            timer t action (Show("falling_pet_die", _tag="falling_pet%i" % i, i=i), SetLocalVariable("i", i+1), SetVariable("fall_time", 1.0 + renpy.random.random()*0.5)) repeat True
        else:
            timer t action (Show("falling_pet", _tag="falling_pet%i" % i, i=i), SetLocalVariable("i", i+1), SetVariable("fall_time", 1.0 + renpy.random.random()*1.5)) repeat True

screen falling_pet(i): # Falls down through the screen

    layer "master"

    add "weird_pet%i" % i at falling_pet

    timer fall_time*2 action Hide()


screen falling_pet_die(i): # Falls down on the ground

    layer "master"

    add "weird_pet%i" % i at falling_pet_die

    timer fall_time action (SetDict(explode_pet, i, True), Play("sound", s_splat))

image micro_transac_rain = SnowBlossom("img_gold_24", count=500)


#### END OF BK declarations ####
