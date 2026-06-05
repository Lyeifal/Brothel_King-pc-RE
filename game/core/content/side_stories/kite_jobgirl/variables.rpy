############ JOBGIRL EVENTS VARIABLES ############


init -3 python:

# Goldo: These lines won't work as 'init' because they will be reset everytime the player starts the game.
# I moved them to the beginning of the first event.

#     jobgirl_romance = 0
#     jobgirl_corruption = 0
#     anika_sex = False


## sounds

    ## part 1 : riddle
    m_jobgirl_1_suspence = m_short_suspense

    ## part 2 : beach
    s_moans_friend = s_moans_mature_quiet

## characters

init 1 define anika = Character("Anika", image="anika", window_left_padding=int(wl_padding))
image anika = ProportionalScale("resources/characters/npc/Jobgirl/beach/anika body.webp")
image side anika = ProportionalScale("resources/characters/npc/Jobgirl/beach/anika portrait.webp", res_portrait_size, res_portrait_size)

# define elflady = Character("Insert-Name", image="elflady")
# image elflady = "resources/characters/npc/Jobgirl/elf house/lady body.gif"
# image side elflady = "resources/characters/npc/Jobgirl/elf house/lady portrait.webp"



## images

    ## part 1 : riddle

image jobgirl_riddle = ProportionalScale("resources/characters/npc/Jobgirl/special_riddle.webp", config.screen_width, config.screen_height)
image teasing_cleavage = ProportionalScale("resources/characters/npc/Jobgirl/teasing cleavage.webp", config.screen_height, config.screen_width)

    ## part 2 : beach

image bg beach = im.Scale("resources/backgrounds/beach.webp", config.screen_width, config.screen_height)
image beach_arrival = ProportionalScale("resources/characters/npc/Jobgirl/beach/beach arrival.webp", config.screen_width, config.screen_height)
image jobgirl_bikini = ProportionalScale("resources/characters/npc/Jobgirl/beach/beach bikini.webp", config.screen_width, config.screen_height)
image beach_friend_1 = ProportionalScale("resources/characters/npc/Jobgirl/beach/beach friend 1.webp", config.screen_width, config.screen_height)
image beach_friend_2 = ProportionalScale("resources/characters/npc/Jobgirl/beach/beach friend 2.webp", config.screen_width, config.screen_height)
image beach_friend_3 = ProportionalScale("resources/characters/npc/Jobgirl/beach/beach friend 3.webp", config.screen_width, config.screen_height)
image beach_sit = ProportionalScale("resources/characters/npc/Jobgirl/beach/beach sit.webp", config.screen_width, config.screen_height)
image beach_stand_1 = ProportionalScale("resources/characters/npc/Jobgirl/beach/beach stand1.webp", config.screen_width, config.screen_height)
image beach_stand_2 = ProportionalScale("resources/characters/npc/Jobgirl/beach/beach stand2.webp", config.screen_width, config.screen_height)
# image beach_sunscreen = "resources/characters/npc/Jobgirl/beach/beach sunscreen.webp"
image beach_surprised = ProportionalScale("resources/characters/npc/Jobgirl/beach/beach surprised.webp", config.screen_width, config.screen_height)
# image beach_teasing = "resources/characters/npc/Jobgirl/beach/beach teasing.webp"
# image beach_teasing_butt = "resources/characters/npc/Jobgirl/beach/beach teasing butt.webp"
# image beach_teasing_naked = "resources/characters/npc/Jobgirl/beach/beach teasing naked.webp"
image beach_topless = ProportionalScale("resources/characters/npc/Jobgirl/beach/beach topless.webp", config.screen_width, config.screen_height)
image beach_lay_down = ProportionalScale("resources/characters/npc/Jobgirl/beach/beach lay down.webp", config.screen_width, config.screen_height)
# image special_beach = "resources/characters/npc/Jobgirl/special beach.webp"

image friend_sunbathing = ProportionalScale("resources/characters/npc/Jobgirl/beach/friend sunbathing.webp", config.screen_width, config.screen_height)
image friend_teasing1 = ProportionalScale ("resources/characters/npc/Jobgirl/beach/friend teasing1.webp", config.screen_width, config.screen_height)
image friend_teasing2 = ProportionalScale ("resources/characters/npc/Jobgirl/beach/friend teasing2.webp", config.screen_width, config.screen_height)
image friend_boobs = ProportionalScale("resources/characters/npc/Jobgirl/beach/friend boobs.webp", config.screen_width, config.screen_height)
image friend_cum_body1 = ProportionalScale("resources/characters/npc/Jobgirl/beach/friend cum body1.webp", config.screen_width, config.screen_height)
image friend_cum_body2 = ProportionalScale("resources/characters/npc/Jobgirl/beach/friend cum body2.webp", config.screen_width, config.screen_height)
image friend_orgasm = ProportionalScale("resources/characters/npc/Jobgirl/beach/friend orgasm.webp", config.screen_width, config.screen_height)
image friend_stand1 = ProportionalScale("resources/characters/npc/Jobgirl/beach/friend stand1.webp", config.screen_width, config.screen_height)
image friend_shower = ProportionalScale("resources/characters/npc/Jobgirl/beach/friend shower.webp", config.screen_width, config.screen_height)
image friend_doggy = ProportionalScale("resources/characters/npc/Jobgirl/beach/friend doggy.webp", config.screen_width, config.screen_height)

    ## part 3 : elf house

# image elf_house_hall = "resources/characters/npc/Jobgirl/elf house/hallroom.webp"
# image elf_house_inner = "resources/characters/npc/Jobgirl/elf house/inside.webp"

# image elf_lady_1 = "resources/characters/npc/Jobgirl/elf house/lady 1.webp"
# image elf_lady_2 = "resources/characters/npc/Jobgirl/elf house/lady 2.webp"
# image elf_lady_3 = "resources/characters/npc/Jobgirl/elf house/lady 3.webp"
# image elf_lady_4 = "resources/characters/npc/Jobgirl/elf house/lady 4.webp"
# image elf_lady_5 = "resources/characters/npc/Jobgirl/elf house/lady 5.webp"
# image elf_lady_6 = "resources/characters/npc/Jobgirl/elf house/lady 6.webp"
