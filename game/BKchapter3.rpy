#### CHAPTER 3 EVENTS ####

## Suzume events & NPC hints ##

label c3_suzume_hint(): # Happens after all three kunoichi hunts have been locked, or after the first summon of Homura

    scene black with fade
    show expression bg_bro at top with dissolve
    show suzume with dissolve

    if story_flags["homura summoned"]:
        suzume bend "Sooo... Did you learn anything interesting from your posh little girlfriend?"

        you "Do you mean... Homura? Are you stalking me, or something?"

        suzume doubt "Stalking? No way! I just watch you have sex from time to time, is all."

        you "Watch me have... THIS IS WORSE THAN STALKING!" with vpunch

        suzume "Hey, what can I say... It turns me on."

        you "Why you... Grrr..."

        you "Hang on, I just thought of something. Can you bend forward?"

        show suzume bend with dissolve

        suzume bend "Bend forward? Like this?"

        you "Ah, yes... Just what I thought."

        you "I'm horny. Come here."

    else:
        suzume doubt "Well... We seem to be well and truly stuck."

        you "What do you mean?"

        suzume "We have hunted all three kunoichi across the city... But now they are all beyond our reach."

        you "Their ninja powers are messing with us. There has to be a way to circumvent them."

        suzume normal "We should ask around for hints. You've made a few contacts through the city, haven't you? Why not ask them for clues?"

        you "I don't know. Most of them are freaks and dullards. Some are hot girls, though."

        suzume bend "What about this noble little lady you've been dating? Perhaps she knows something we don't?"

        you "Hey! We're not da-"

        you "Why am I justifying myself to you?" with vpunch

        suzume "Fufufu, don't get the wrong idea. I'm not the jealous type..."

        suzume "But just so you know, I could use a little boning. I am getting rusty, you know!"

        you "It's only been-"

        you "Wait. Actually, it's been a while. Come here."

    scene black with fade

    play sound s_moans_short

    "A while later..."

    play sound s_orgasm_fast
    show bg suzume_piledriver at top with flash

    suzume naked2 "AAAAAAAH!!!"

    with doubleflash

    suzume "Oh my... Look at the mess you've made..."

    "She looks at you straight in the eye in an obscene pose as your cum drips down her holes and belly."

    suzume "You didn't even spare my ass this time! Looks like we've found a new way to have fun..."

    play sound s_mmh
    $ MC.change_prestige(3)

    scene black with fade
    show expression bg_bro at top with dissolve
    show suzume naked with dissolve

    suzume "Aaah... That's better! [emo_heart]"

    you "Yes. But this doesn't bring us any closer to catching those pesky ninjas."

    suzume "Well, like I said, you can investigate with your contacts in the city. Or you can hit your noble girlfriend."

    you "For lack of better ideas... Okay."

    "You can now {b}visit your contacts{/b} by talking to suzume on the {b}city{/b} screen."

    if story_flags["homura summoned"]:
        "You could also ask Homura for more hints, by summoning her from the {b}Plaza{/b}."
    else:
        "Homura also mentioned that she can help you if you tie her ribbon to a pole in the {b}Plaza{/b}, but you'll need an okiya first."

    $ story_flags["suzume hint seen"] = True
    $ suzume_hints_active = True

    return


label c3_update_hint_goals():
    python:
        for nin, channel, desc in [(NPC_haruka, "story", "The Earth Kunoichi"), (NPC_mizuki, "story2", "The Water Kunoichi"), (NPC_narika, "story3", "The Void Kunoichi")]:
            # Unlocks hint recap with Suzume
            if nin.flags["hints"] >= 3:
                if nin.flags["locked"]: # First call
                    game.set_task(desc + ": Talk to Suzume again about %s." % nin.name, channel, blocking=True)
                nin.flags["locked"] = False

            # Init hints
            else:
                if nin.flags["hints"] is False:
                    nin.flags["hints"] = 0
                game.set_task(desc + ": Collect 3 hints on " + nin.name + " (%s/3)." % str(nin.flags["hints"]), channel, blocking=True)

    return

label c3_interrogate_contacts():

    hide screen districts

    scene black
    show bg zan at top
    # with fastfade

    show screen overlay

    call c3_update_hint_goals() from _call_c3_update_hint_goals

    $ suzume("So, who would you like to question among your contacts in the city?", interact=False)

    $ contact_list =  [("side suzume", "Suzume, the Air Kunoichi", NPC_suzume),
                        ("side sill", "Sill, your trusty Slave Girl", NPC_sill),
                        ("side papa", "Papa Freak, the Weird Old Man", NPC_freak),
                        ("side jobgirl", "[jobgirl_name], the Quest Giver", NPC_jobgirl),
                        ("side satella", "Satella, the Night Mistress", NPC_satella),
                        ]

    if NPC_bast.met:
        $ contact_list.append(("side bast", "Bast, the Quartermaster", NPC_bast))
    if farm.active:
        $ contact_list.append(("side gizel", "Gizel, the White Witch", NPC_gizel))
    if story_flags["met carpenter"]:
        $ contact_list.append(("side carpenter", "Iulia, the Carpenter", NPC_carpenter))
    if thieves_guild.action:
        $ contact_list.append(("side renza", "Renza, the Thief", NPC_renza))
    if not NPC_kenshin.flags["dead"]:
        $ contact_list.append(("side kenshin", "Kenshin, the Knight Commander", NPC_kenshin))
    else:
        $ contact_list.append(("side knight", "The Royal Knights", NPC_knight))
    if watchtower.action:
        $ contact_list.append(("side sergeant", "Kashiv, the grim Guard Sergeant", NPC_sergeant))
        $ contact_list.append(("side captain", "Farah, the naughty Guard Captain", NPC_captain))
    if story_flags["c1_path"] == "neutral":
        $ contact_list.append(("side lieutenant", "Lydie, the cunning Guard Captain", NPC_lieutenant))
    if story_flags["c1_path"] == "good":
        $ contact_list.append(("side maya", "Maya, the righteous Guard Captain", NPC_maya))
        $ contact_list.append(("side roz", "Roz, the zealous Guard Lieutenant", NPC_roz))
    if harbor.action:
        $ contact_list.append(("side stella", "Stella, the Blood Isles's Slaver", NPC_stella))
    if farmland.action:
        $ contact_list.append(("side goldie", "Goldie, the Farmhand", NPC_goldie))
    if sewers.action:
        $ contact_list.append(("side willow", "Willow, the Monster Catcher", NPC_willow))
    if junkyard.action:
        $ contact_list.append(("side gina", "Gina, the Mad Scientist", NPC_gina))
    if prison.action:
        $ contact_list.append(("side gurigura", "Gurigura, the Toy Merchant", NPC_gurigura))
    if arena.action:
        $ contact_list.append(("side ramias", "Ramias, the Weapon Merchant", NPC_ramias))

    call screen suzume_hints(contact_list)
    $ npc = _return

    if not npc:
        jump districts

    if not isinstance(npc, NPC):
        jump c3_interrogate_contacts

    # General tips / unlock story (Suzume)

    if npc == NPC_suzume:

        if not (NPC_narika.flags["locked"] or NPC_narika.flags["c3 path"]) or not (NPC_mizuki.flags["locked"] or NPC_mizuki.flags["c3 path"]) or not (NPC_haruka.flags["locked"] or NPC_haruka.flags["c3 path"]):
            menu:
                "I found hints about Narika" if not (NPC_narika.flags["locked"] or NPC_narika.flags["c3 path"]):
                    hide overlay
                    scene black with fade
                    call c3_unlock_narika from _call_c3_unlock_narika
                "I found hints about Mizuki" if not (NPC_mizuki.flags["locked"] or NPC_mizuki.flags["c3 path"]):
                    hide overlay
                    scene black with fade
                    call c3_unlock_mizuki from _call_c3_unlock_mizuki
                "I found hints about Haruka" if not (NPC_haruka.flags["locked"] or NPC_haruka.flags["c3 path"]):
                    hide overlay
                    scene black with fade
                    call c3_unlock_haruka from _call_c3_unlock_haruka

            jump districts

        suzume doubt "Well, I've told you everything I know, I think..."

        suzume normal "I don't have specific hints about individual Kunoichi, but I'm sure other people will."

        suzume "If you can collect {b}three hints{/b} about one of them, talk to me again. We should be able to devise a plan."

        "Talk to Suzume after you've gathered {b}three hints{/b} on a Kunoichi."

        jump c3_interrogate_contacts

    menu:
        "Who do you want to ask [npc.name] about?"

        "Ask about Narika, the Void Kunoichi" if NPC_narika.flags["locked"] or not MC.has_item(void_rune.name) or debug_mode:
            "You tell [npc.name] about {b}Narika{/b}, the Kunoichi you are looking for, and what she's been up to."
            $ nin = NPC_narika

        "Ask about Mizuki, the Water Kunoichi" if NPC_mizuki.flags["locked"] or not MC.has_item(water_rune.name) or debug_mode:
            "You tell [npc.name] about {b}Mizuki{/b}, the Kunoichi you are looking for, and what she's been up to."
            $ nin = NPC_mizuki

        "Ask about Haruka, the Earth Kunoichi" if NPC_haruka.flags["locked"] or not MC.has_item(earth_rune.name) or debug_mode:
            "You tell [npc.name] about {b}Haruka{/b}, the Kunoichi you are looking for, and what she's been up to."
            $ nin = NPC_haruka

        "Ask about the elemental-proof cells" if npc == NPC_freak and NPC_freak.flags["holding info"]:
            "You talk to {b}Papa Freak{/b} about the secret magic-proof cells in your building again."
            call c3_papa_cells from _call_c3_papa_cells

            jump c3_interrogate_contacts

        "Never mind":
            jump c3_interrogate_contacts

    # Individual tips

    $ MC.interactions -= 1

    $ hint_list = {
                    NPC_narika : (NPC_jobgirl, NPC_bast, NPC_gurigura, NPC_gina, NPC_roz, NPC_renza, NPC_captain),
                    NPC_mizuki : (NPC_sill, NPC_satella, NPC_freak, NPC_gizel, NPC_stella),
                    NPC_haruka : (NPC_kenshin, NPC_carpenter, NPC_ramias, NPC_goldie, NPC_maya, NPC_lieutenant, NPC_sergeant)
                }

    if npc in hint_list[nin]:

        call c3_hint(npc, nin) from _call_c3_hint
        scene black
        show bg zan at top
        with fastdissolve

        if _return != "cancel":
            call c3_update_hint_goals() from _call_c3_update_hint_goals_1

    else:
        python:
            no_hint = {
                    NPC_jobgirl : "Err, sorry, I don't know anything about such a person.",
                    NPC_bast : "Look, I'm busy, and this doesn't ring a bell, sorry.",
                    NPC_gurigura : "Teeheehee! I didn't understand a single thing you said, but you're funny, Mister.",
                    NPC_gina : "Sorry, but I don't know anything about such a person. Now, I have an important paper to write, so...",
                    NPC_roz : "Err, never heard about that chick, sorry.",
                    NPC_renza : "Hmm... I don't know this person. She probably operates outside of my turf.",
                    NPC_captain : "Never heard of her. Now, if you'll excuse me, I have a legal {i}and{/i} a criminal empire to run, so kindly fuck off.",
                    NPC_sill : "Oh, I'm sorry, Master... I really don't know anything about such a person.",
                    NPC_satella : "Why, it's funny you should mention it, I had a pet raccoon called just like that... But I just realized I forgot to feed it. Poor thing, it's been six months! It must be hungry.",
                    NPC_freak : "Thank you for visiting me, my boy.... But I have no idea who you're babbling on about.",
                    NPC_gizel : "Don't know, don't care. Look, human females are fun to run experiments on, but I haven't got much interest in their indiviual characteristics otherwise.",
                    NPC_stella : "Look, I don't give information for free. But I don't have any information about this person anyway.",
                    NPC_kenshin : "Is this a person of interest in your investigation? I haven't heard anything worth mentioning about such a person.",
                    NPC_knight : "We don't know anything about this individual. Now move along, citizen.",
                    NPC_carpenter : "Boss, I'm just a carpenter. I build things. This cloak and dagger stuff doesn't concern me.",
                    NPC_ramias : "I'm sorry, I'm sure it was all terribly interesting, but ever since an orc banged his mace on my helmet, I blank out sometimes. I'm afraid I can't help you.",
                    NPC_goldie : "Oh, " + MC.name + ", I would love nothing more than to help you... But I really don't know anything.",
                    NPC_maya : "Sorry, I haven't heard of such a criminal. Maybe ask Roz, he's the one who still patrols the streets. I mostly handle paperwork now... *sigh*",
                    NPC_lieutenant : "No, I must say I haven't heard of her. Maybe Renza knows, I handle the more 'official' business these days.",
                    NPC_willow : "Is she a monster? Because that's what I deal with, monsters. I give most humans a wide berth.",
                    NPC_sergeant : "I have nothing to say to you. Leave.",
                    }

        $ renpy.say(npc.char, no_hint[npc])

    if npc == NPC_willow:
        if story_flags["fire rune"]:
            willow "Sorry friend. You already bought that fire rune from me. (Damn, I knew I should have asked 100 gold for it...)"
        else:
            if not NPC_willow.flags["introduce fire rune"]:
                $ NPC_willow.flags["introduce fire rune"] = True

                willow "Hey, [MC.name], wanna see something cool?"

                you "Depends. Does it involve going into the sewers again? Because I hate going down in the sewers. Washing the smell away takes days..."

                willow "Nope, it's a fire rune. You can engrave it on a weapon, and fight fire with fire. Isn't it cool?"

                you "Yeah I guess... But none of the ninjas I'm hunting for use fire."

                willow "But you could get it, you know, just in case? For 100,000 gold?"

                you "100,000 GOLD!!!" with vpunch

                willow "Alright, sheesh, don't yell... 10,000 gold then?"

                you "10,000 GOLD!!!" with vpunch

                you "..."

                you "Wait. Did you just give me a 90 per cent rebate right off the bat? Why?"

                willow "Gee, you're impossible!"

                willow "Fine, Mister Negotiator, you can have it for 1,000 gold! But that's final!"

                you "You just went down from 100,000 gold to 1,000 gold in the blink of an eye."

                willow "Yes. I'm great at bargaining, don't you think? Because I think I rock!"

                you "Well, it's, err, important that you believe in yourself... If no one else will?"

                you "So can I have it for 1,000 gold?"

                willow "Yes, that's my final price. Because if you lower the price more than twice, it brings bad luck and your fluffy ears fall off. Everybody knows that."

                you "I don't think that {i}anybody{/i} actually knows that..."

                willow "Anyway, you want it, or what?"

            else:
                willow "Say, you wouldn't be interested in that piping hot fire rune, would you? 1,000 gold, as we negotiated last time?"

            if MC.gold >= 1000:
                menu:
                    _("Sure (pay 1,000 gold)"):                        you "Sure okay, give it to me."

                        play sound s_gold
                        $ MC.gold -= 1000
                        $ story_flags["fire rune"] = True

                        call receive_item(fire_rune) from _call_receive_item_19

                    "No":
                        you "1,000 gold for a trinket I'll never use? No thanks."

            else:
                you "I don't have that kind of money right now."

                willow "Fine, I'll hang on to this a little longer. Let me know if you want it."

    elif npc == NPC_freak and not NPC_freak.flags["holding info"]:

        $ NPC_freak.flags["holding info"] = True

        papa_apprentice "Hey, Papa, aren't you forgetting something? You said you'd tell him?"

        papa "Uh? Oh, that's right..."

        papa "Sorry, young man, I wanted to tell you about that house you just got off my hands."

        you "I knew it!!! It was all a scam, isn't it? It's going to crumble within a week? It's built on an ancient graveyard? It's haunted by malevolent vampire rabbits?"

        papa "No..."

        you "So it's even worse, then! Cockroaches?!?" with vpunch

        papa "No, no, let me speak..."

        papa "You remember, I told you the building has elemental resonance?"

        you "Yes..."

        papa "It's especially strong in the foundations, where the holding cells used to be."

        you "Holding cells? First time I'm hearing about this."

        papa "Yes, they're condemned."

        you "Why talk about it now, then?"

        papa "Well, you told us you're hunting for ninjas with elemental powers, correct?"

        you "Yes..."

        papa_apprentice "Then holding cells that cancel elemental magic could be very useful to you!"

        you "Indeed... If I could get those Kunoichi captured in the first place."

        papa "I'll leave that bit to you. But my apprentice and I, we could rebuild the holding cells... For a price."

        you "How much?"

        papa "You know we don't need money, right?"

        you "So... What is it you want?"

        papa_apprentice "Oh, I think you know... *grin*"

        papa "Girls, of course!"

        you "Can you be more specific?"

        papa "All right..."

        $ NPC_freak.flags["cells built"] = 0

        call c3_papa_cells() from _call_c3_papa_cells_1
        show screen overlay

        if not NPC_freak.location:
            $ NPC_freak.location = location_dict[papa_location[district.name]]
        $ NPC_freak.location.action = True

    if MC.interactions:
        jump c3_interrogate_contacts
    else:
        jump districts

label c3_hint(npc, ninja):

    scene black
    show expression npc.get_bg() at top
    if npc != NPC_stella:
        show expression npc.char.image_tag
    else:
        show stella at center:
            yoffset yres(350)

    with fade

    ## Narika tips

    if ninja == NPC_narika:
        if npc == NPC_jobgirl: # disguise, upper city
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True
            if event_dict["c2_narika_H1"].happened:
                $ ninja.flags["school hint"] = True
                $ ninja.flags["upper city hint"] = True
                jobgirl "A student in uniform, you say?"

                jobgirl "Well, none of the classes that I know of require uniforms. Must be something from the upper city."

                jobgirl "Must be a fancy school for sure... Reserved for blue bloods, no doubt."

            else:
                $ ninja.flags["school hint"] = True
                jobgirl "Wait a minute, this does ring a bell..."

                jobgirl "Sometimes ago, I was taking an adventuring class and someone asked me if I heard about an ambitious heist being organized in the city."

                jobgirl "They asked me if I was worried about our safety. I was confused, until they said the target was going to be a school."

                jobgirl "Hahaha, can you imagine that? A bank or a guild, maybe, but a school? Who in Xeros thinks robbing a school is a good idea?"

                # jobgirl "I've heard of an ambitious heist being planned in the upper city. Something about a locked-down place, with tight security and all... A bank maybe?"
                #
                # jobgirl "I'll tell you what, no one can take over such targets by storm, they're too well-defended... If it was me, I'd go with infiltration. Get them from within."

            suzume "Hmm, that's a hint we could use... It narrows down our target, I guess."

            play sound s_spell

        elif npc == NPC_bast: # magical item
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True
                $ ninja.flags["magic hint"] = True
            bast "Stolen goods? You're asking me, the official market quartermaster, if I know who is moving stolen goods?"

            you "Well..."

            bast "Of course I do!" with vpunch

            bast "I wouldn't be a very good trader if I didn't know about the black market, now, would I?"

            bast "Turns out, I've heard something recently. Someone inquiring in advance about how to sell a single item of high value."

            bast "The interesting thing, though? It's supposed to be a magical item. Not easy to find a taker for these, but they fetch sky-high prices if you do."

            bast "Can't say if it's related to your girl, but worth checking out, wouldn't you say?"

            play sound s_spell

        elif npc == NPC_gurigura: # disguise
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True
            if event_dict["c2_narika_H1"].happened:

                show expression npc.char.image_tag at left with move
                show katryn at right with dissolve

                gurigura "A student in uniform? And you're asking me... Because I look young?"

                you "Well..."

                gurigura "I {i}am{/i} young, but I never went to no school, teeheehee..."

                katryn "Why, obviously. You might as well ask a kitty about theoretical physics."

                gurigura "Theophysical ethics, what's that? And what's a kitty?"

                katryn "My point."

                you "This is all a big waste of time..."

                katryn "Wait. All of this goes way over poor Gurigura's head, obviously, but {i}I{/i} can help."

                you "Really?"

                katryn "Of course. There's one place where girls wear the exact kind of uniforms you described. The Magic University."

                suzume "The Magic University! That's an important clue, [MC.name]!"

                play sound s_spell
                $ ninja.flags["school hint"] = True
                $ ninja.flags["magic hint"] = True

            else:
                gurigura "You know the funny thing, I met a young girl like that the other day, same clothing and all."

                gurigura "She looked about my age, and she smelled funny, so I followed her around. The smell of fluffy trees."

                you "Fluffy trees? Like Sakura?"

                gurigura "Sakura? Isn't that a stripper's name?"

                you "*sigh*"

                gurigura "So I followed her. I figured we could be playmates, you know?"

                you "Hmm... Do you always stalk random people like that?"

                gurigura "Of course not! Only when they smell funny."

                you "I... Don't even wanna know. Go on."

                gurigura "I followed her as she entered a big building through a back door."

                gurigura "I peeked through the keyhole, and she was in her undies!"

                you "Uh?"

                gurigura "She quickly stashed her fighting clothes behind a loose stone, and put on some kind of uniform."

                you "A uniform?!?"

                suzume "Whatever she is doing, she must be in a place where uniforms are worn. This is an important clue!"

                play sound s_spell
                $ ninja.flags["uniform hint"] = True

        elif npc == NPC_roz: # upper city, lined-up buyer / Good c1 ending
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True
                $ ninja.flags["upper city hint"] = True
            $ wrong_name = ''.join(random.sample(MC.name,len(MC.name))).capitalize()

            roz "Oy! [wrong_name], long time no see."

            you "Actually, it's [MC.name]."

            roz "Yes! [wrong_name], that's what I just said."

            you "*long explanation*"

            you "Anyway... Can you help me?"

            roz "You know, I've heard something. Sometimes when I beat up a petty thief, they start spilling out some interesting information."

            you "I see, sometimes you have to beat them up when they resist arrest."

            roz "When they resist arrest? Oh, yeah... That too."

            roz "Anyway, word on the street is that a heist is being prepared, but this is nowhere in the league of the common riff-raff I deal with in the Slums."

            roz "They're aiming for a top-tier target, and sparing no resources to prepare for it. That's the only way they could afford hiring professionals like your ninja babe."

            roz "We're talking about the upper city, of course. Top security, difficult infiltration and escape, buyer lined-up for the goods. This kind of things."

            you "You know, that's actually helpful information. Color me impressed."

            roz "Uh? Impressed? Sorry pal, I don't have a pencil of that color."

            you "I take that back. *cringe*"

            play sound s_spell

        elif npc == NPC_renza: # Magical item, lined-up buyer / Neutral c1 ending

            renza "Interesting... If anyone else told me such a story, I wouldn't believe a word of it. But you and I have a history."

            you "So... Can you help me?"

            if npc.flags["seen ninja hint"]:
                renza "I already agreed to help you, didn't I?"

            elif NPC_renza.flags["story4"]:
                renza "Of course I can. Anything for you, sweetheart."

            else:
                renza "Well, information has a price. Perhaps you could donate some of your resources to the guild, hmm?"

                if not (MC.has_resource("wood", 10) or MC.has_resource("leather", 10) or MC.has_resource("dye", 10)):
                    renza "Bring me at least ten resources such as {b}wood, leather or dye{/b}. Then we'll talk."
                    return

                menu:
                    extend ""
                    "Give her 10 {image=tb wood}" if MC.has_resource("wood", 10):
                        $ MC.spend_resource("wood", 10)

                    "Give her 10 {image=tb leather}" if MC.has_resource("leather", 10):
                        $ MC.spend_resource("leather", 10)

                    "Give her 10 {image=tb dye}" if MC.has_resource("dye", 10):
                        $ MC.spend_resource("dye", 10)

                    "Don't give her":
                        you "Sorry, maybe next time."
                        return

                renza "Thanks! That will do."

            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True
                $ ninja.flags["magic hint"] = True
                $ ninja.flags["upper city hint"] = True

            renza "I've been approached by someone, maybe 3 or 4 months ago. They wanted help to steal a certain item from the upper city."

            you "Nothing unusual in your line of work..."

            renza "Except I had to turn them down. This was out of reach, even for me."

            you "What do you mean?"

            renza "They wanted to lay their hands on a unique magic item, with top-notch protection spells. I'm not sure where it was being held, they wouldn't tell me until I accepted the job."

            you "You turned it down?"

            renza "There's one thing about me: I'd rather be alive and poor than rich but burnt to a crisp by a magic ward."

            renza "A Kunoichi, though... They just might pull it off."

            you "And who was it that approached you?"

            renza "I have no idea. It was a woman, for sure, but her disguise was nearly perfect. I understood she had high-level backers."

            renza "We chatted for a while about how to overcome some of the more mundane defenses. Her questions were quite good and to-the-point, I have to say. A true professional."

            you "What happened after that?"

            renza "Nothing. Once she figured I wouldn't take the job, she thanked me and I never heard from her again."

            renza "But I'm willing to bet she's the one who's bankrolling your mysterious Kunoichi."

            you "Well, that's certainly something..."

            play sound s_spell

        elif npc == NPC_captain: # Upper city, uniforms / evil c1 ending
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True
                $ ninja.flags["upper city hint"] = True
            captain "A thief? In my city? Haha! Now that'd be a first..."

            you "Don't jest. She's not just any thief, she's a well-trained ninja."

            captain "Look, [MC.name], your naivety is part of your charm, but you could do with using your brain a little more. Do you think someone would hire a very expensive ninja to steal something in the Slums?"

            you "I guess not..."

            captain "Obviously if it was happening on my turf, I'd know about it. And I'd get my cut. The target must be in the upper city, where it's none of my concern."

            you "Makes sense."

            captain "In fact, I've heard they've really buffed security in some of the iconic landmarks... The Royal Palace, the Cathedra, the Magic University..."

            captain "It could be related to the murders, but it could also be linked to this alleged heist?"

            suzume doubt "She could be right... The little brat must be targeting one of those places."

            play sound s_spell

        elif npc == NPC_gina: # Void rune
            if story_flags["void rune"]:
                gina "I'm sorry, I already sold you the time-bending rune. Wait, are you a time-traveller from the past who hasn't bought the rune yet? I need to make some calculations..."
            else:
                if not NPC_gina.flags["introduce void rune"]:
                    $ NPC_gina.flags["introduce void rune"] = True

                    gina "What on earth are you babbling on about? Murders? Ninjas? Toy hammers?"

                    gina "I don't have time for this! I'm on the brink of a major discovery!"

                    you "If you say so..."

                    gina "Why, you don't believe me? Let me walk you through a few differential equations..."

                    you "No no, it's fine, I believe you!"

                    gina "You see, the Cimerians were so advanced that they had ways to manipulate the spacetime fabric itself."

                    you "The spacetime fabric? You mean like... Cloth?"

                    gina "Exactly. Every scientist knows that space and time are made of black thread, which is woven together by Chaos Fairies."

                    gina "Do you never wonder why the skies looks black at night?"

                    you "Because... They're made of the black thread space and time thingy?"

                    gina "Precisely! A fellow scholar, I see. We call them the Woven Threads of Fate."

                    gina "As you must know, science has shown that time is composed of smaller elemental particles, called timicrons. A moment, for instance, can hold as many as 1,532,875 timicrons. While an instant is more like 75,584 timicrons.  But feel free to check my maths."

                    you "No thanks."

                    gina "Now, timicrons can be charged positively, of course, so that they go faster, or negatively, so that they go slower."

                    gina "It has been proven that some activities, such as having fun, charge timicrons positively, while other activities charge timicrons negatively. This is how science explains that an hour at the dentist always seems to drag on much longer than an hour at the brothel."

                    gina "Now, look at this Cimerian runic stone: by generating a field with the Woven Threads of Fate, the Old Ones were able to charge it negatively and alter time in various ways."

                    gina "This WTF field could then be deployed with the press of a rune, slowing down all of the timicrons within a reasonably large area, such as a ballroom."

                    you "Wait a minute, let's see if I can make sense of your mumbo-jumbo... Are you saying this stone can slow down time?"

                    gina "Not at all, silly... It just slows down timicrons so that time {i}seems{/i} to flow slower in a given referential."

                    you "What if I put a super fast ninja in this referential-thingy? Could this stone hold her in place?"

                    gina "Well... Technically speaking... Yes? Maybe. I don't know. Maybe not."

                    you "Thank you for giving me an actionable and informed scientific opinion."

                    you "Anyway, I may actually need something like this."

                    gina "Really? I could sell it to you. It's true that I'm always in need of additional funds for my research..."

                    gina "I guess I could part with it for 1,000 denars."

                    you "1,000 denars? That's a lot for a small rock..."

                    gina "Well, I suppose if you have a couple of pieces of Cimerian scrap, that would do too."

                else:
                    gina "Want the time-warping runic stone? The price is still 1,000 gold, or two Cimerian scraps."

                if MC.gold >= 1000 or len(MC.get_items(name="Cimerian scrap")) >= 2 or MC.get_items(name="Cimerian artefact"):
                    menu:
                        _("Okay (pay 1,000 gold)"):                            $ NPC_gina.flags["research"] += 2
                            you "Fine, I'll take it."

                            play sound s_gold
                            $ MC.change_gold(-1000)
                            gina "Thanks! This will help with my research."

                            $ story_flags["void rune"] = True
                            call receive_item(void_rune) from _call_receive_item_20

                        "Okay (give 2 Cimerian scrap)" if len(MC.get_items(name="Cimerian scrap")) >= 2:
                            $ NPC_gina.flags["research"] += 2
                            call remove_item(MC.get_items(name="Cimerian scrap")[0]) from _call_remove_item_2
                            call remove_item(MC.get_items(name="Cimerian scrap")[0]) from _call_remove_item_3
                            gina "Thanks! This will help with my research."
                            $ story_flags["void rune"] = True
                            call receive_item(void_rune) from _call_receive_item_45

                        "What about this? (give Cimerian artefact)" if MC.get_items(name="Cimerian artefact"):
                            $ NPC_gina.flags["research"] += 5
                            $ MC.remove_item(MC.get_items(name="Cimerian artefact")[0])
                            gina "Whoah, amazing find!!! This will help a lot with my research, thank you. Here, take this."
                            $ MC.change_gold(500)
                            $ story_flags["void rune"] = True
                            call receive_item(void_rune) from _call_receive_item_46

                        "Maybe later":
                            you "1,000 gold for a piece of rubble? I'll pass."

                            gina "Suit yourself. Come back if you change your mind."

                else:
                    you "I don't have the money."

                    gina "How disappointing. Come back if you change your mind."

    elif ninja == NPC_mizuki:
        if npc == NPC_sill: # Various types of magic, ghost
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True

            sill sad "R-Really, Master? You want my opinion?"

            sill "(What should I do, what should I do... This never happens...)"

            you "Yes. If I remember right, you were trained in magic as a child before your family fell out of grace, correct?"

            sill happy "Well, it's true! My teachers said I had great potential."

            sill sad "And now, look at me, doing laundry... *sniff*"

            you "I know, right! What a waste of your natural talent for housekeeping it would have been."

            sill "Aw..."

            you "Anyway, is there anything you can tell me about the water Kunoichi?"

            sill happy "Ahem, let's see. So you say this woman can appear and disappear at will?"

            you "Yes, and yet it doesn't seem to be regular magic... She just vanishes into thin air, like a ghost. I'm sure her mana was depleted."

            sill "Hmm... Like a ghost, you said?"

            you "Yeah."

            sill "One thing I learnt is that speaking broadly, there are two kinds of magic. The one we use is called academic magic, which is centered around formulas, scepters, runes or other conduits that we have to learn and master in order to cast spells."

            you "Okay..."

            sill "But there is another form of magic, called 'innate magic'. It's the kind used by dragons, the fairy people, demons..."

            you "Hmm... Even though she's a she-devil, I don't think she's a demon. Or a dragon, or an elf, for that matter."

            sill "... and the undead."

            you "What?"

            sill "Ghosts. The undead. They can use innate magic. Even without any external conduits, or mana. Their immortal soul is the conduit."

            you "Wait a minute. You're not seriously suggesting she's a ghost?"

            if NPC_mizuki.flags["onsen"]:
                you "I've seen her from up close and... She is very much alive! *blush*"

            sill "Well, if she in't a ghost, maybe she found a way to harvest the afterlife's energy, then."

            you "As far-fetched as this sounds... This could be a lead. Let's see where it takes us."

            play sound s_spell

        elif npc == NPC_satella: # Various types of magic, link to Shalia, Karkyr story
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True

            play music m_satella fadein 3.0

            satella happy "Teehee, look what the raccoon dragged in! So... You didn't come here to play a game?"

            you "N-No, not this time..."

            satella angry "Well, you're damn right you didn't, because I didn't send you a bloody invitation, did I!" with vpunch

            you "N-No!!! I'm sorry to disturb you.... Maybe this wasn't a good idea-"

            satella happy "I mean, it's perfectly fine for you to drop by and ask idle questions."

            you "Phew..."

            satella angry "BUT GAMES, THOUGH? GAMES ARE INVITE-ONLY! I MIGHT TURN YOU INTO A MAGGOT PILE IF YOU DARED!!!" with vpunch

            you "*gulp*"

            you "I'm definitely not here for a game... Just idle questions about ninjas you may or may not know anything about, I swear."

            satella happy "Fine, then. I'm glad to see you value my time."

            satella angry "My {i}game{/i} time." with vpunch

            you "So... Know anything about this person? Or her magic?"

            satella happy "Let me tell you something about wizards, sorcerers, mages, witches and all of their ilk..."

            you "What?"

            satella "They're all a bunch of hopeless losers!" with vpunch

            if MC.playerclass == "Wizard":
                you "Well... Thanks."
            else:
                you "Ha! That's what I think, too."

            satella "And you know why?"

            you "I'm going to go with... No?"

            satella "Because they're nerds, that's why!" with vpunch

            you "Uh?"

            satella "They spend spend studying, poring over dusty old books, peeking into other dimensions and begging for scraps of knowledge from bored demons..."

            play sound s_evil_laugh

            satella "Looooooo-sers!!!" with vpunch

            you "..."

            satella "You see, {i}I{/i} weave far better magic than any of these sorry dorks, and did I have to work hard to learn it?"

            satella "Not a single day in my life! Can you believe it?" with vpunch

            you "Oh, I believe it."

            satella "It's because I have good genes! {i}Dragon genes{/i}! It all comes naturally to me!"

            you "Well... Okay."

            satella "So here are my two denars: Your mysterious black magic woman may be a natural, like me. If so, then she doesn't need mana to cast spells, or scrolls, or materia, or whatever it is kids use these days."

            you "Really? Could she just cast any spell?"

            satella "Well, spells within her area of affinity, anyway. Not gonna lie, invisibility, disappearing at will... Sounds right up Shalia's alley."

            you "So she could be a natural magic user, and a Shaliaite... Hmm."

            satella "There's a Shalia covent in Karkyr that studies unorthodox magic. Who knows, maybe they've heard of her."

            you "Karkyr, uh..."

            play sound s_spell

        elif npc == NPC_freak: # Westmarch story, ghost, Karkyr story
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True

            play music m_freak fadein 3.0

            papa "Hey, yo, [MC.name]! Waddup, my [MC.playerclass]?"

            you "Uh? What are you doing?"

            papa "I, err, I'm sorry, son... I was trying to sound 'cool', in the parlance of young people of our era..."

            papa "But I'm old... Hopelessly old..."

            you "Yeah, well, that's kind of the reason I'm asking you this. This lady Mizuki is supposed to be really old... Like you."

            you "(Although I must say she's in much better shape...)"

            papa "We'll see how you are when you get to 323! I'm sure your mighty dick may not be so hardy by then, heh!"

            you "Focus, Papa. Leave my dick out of this. Please."

            papa "So... This lady wears a lavish blue kimono, and she is of great beauty, would you say?"

            you "I would say..."

            papa "And does she have big puppies?"

            you "Puppies? I don't follow..."

            papa "I mean jugs? Mellons? Honkers, ta-tas, knockers, gitchi gitchi yaya dada?"

            you "I think you're laboriously trying to say... 'boobs'."

            papa "Ah, yes, boobies! That's what I'm talking about, dog!"

            you "Stop it."

            papa "Sorry..."

            you "But yeah, now that you mention it, she is remarkable in that area, too..."

            papa "Funny, it reminds me of one such lady, back in Westmarch when I was still... Well."

            papa "She was a highborn princess, from one of the oldest families in Karkyr. She always wore that beautiful blue kimono."

            papa "But it can't be her. It's impossible. That was almost 200 years ago, and..."

            you "She could be 200 for all we know. You lived to the ripe old age of 300, so why not?"

            papa "It's not that easy, and besides..."

            you "No, wait! She has powerful magic! She probably..."

            papa "Listen to me! The lady I'm talking about. It's not her. She took her own life."

            you "She... What?" with vpunch

            papa "Everyone in the city at the time knew her. Lovely young woman. She came from Karkyr and married a prince in Westmarch, they had a grandiose wedding."

            papa "But soon after that, she took her own life."

            you "Whaaat!?!" with vpunch

            papa "It was a shock to everyone in the Western Kingdoms, as Westmarch was known at the time."

            papa "In fact, this sorry event may have started the great struggle for power that lasted 50 years and ended up with the Four Kingdoms disbanded into a hundred small Principalities."

            papa "So you see, young man, there's no chance that your woman and my big-breasted princess could be one and the same. I'm sorry I misled you."

            you "But still... This seems like too much of a coincidence..."

            play sound s_spell

        elif npc == NPC_gizel: # Westmarch story, link to Shalia
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True

            gizel normal "A mysterious lady who disappears into thin air? Hmm. Interesting."

            you "I thought, you know, maybe you know something, as you're immortal and stuff..."

            gizel "Well, the first thing I can tell you is pretty obvious. Smoke and mirrors, hiding, misdirection, deception..."

            gizel "This reeks of Shalia."

            you "Shalia? The Goddess of Shadows?"

            gizel "Precisely. But I realize this is not a lot to go on..."

            gizel "I have something else for you. Much... Stranger, though."

            you "What do you mean?"

            gizel smirk "The Blue Witch of the West."

            you "I beg your pardon?"

            gizel "You remember the nickname the stupid Arios crusaders gave me? White Witch of the North?"

            you "Yeah..."

            gizel "Unimaginative as they are, when they met an all-powerful female magic user in Westmarch, can you guess what nickname they gave her?"

            you "The... The 'Blue Witch of the West'?"

            gizel upset "Precisely. The big, ignorant oafs."

            gizel normal"Turns out about 200-years ago, there was a huge war in Westmarch. Started with four kingdoms, ended with a hundred Principalities. You could say it never really ended."

            gizel "During that time, while I was monitoring various rumors as I usually do to see if the stupid knights were on my track, I started hearing rumors about a local witch."

            gizel upset "A Shalia assassin, a she-devil that could use magic and appear and disappear at will, and killed her marks in a dozen spectacular ways."

            you "Whoah, really?"

            gizel smirk "She was the bane of one or several of the factions in that war, although I can't be arsed to remember which ones."

            gizel upset "Her description was always the same: A stunning, ice-pale middle-age woman with raven hair, and an elaborate blue silk kimono!"

            you "It definitely matches Mizuki..."

            gizel normal "But she left Westmarch by the end of the war, and I never heard from her again after that. By rights, she should be long-dead..."

            you "Something doesn't add up... But it's a lead."

            gizel upset "Okay, now scram. I have to get up early, feed the minions, milk the slaves... Working on the farm is no picnic, you know!"

            play sound s_spell

        elif npc == NPC_stella: # Water rune

            if story_flags["water rune"]:
                stella "You already have that water rune, so no need to pester me. And no refunds!"

            else:
                if not NPC_stella.flags["introduce water rune"]:
                    $ NPC_stella.flags["introduce water rune"] = True

                    stella "Female ninjas, uh? How terribly interesting. *yawn*"

                    stella "In case you've forgotten, I'm a very busy woman... With very little patience. I have nothing to share for free."

                    you "Okay, I see. Fine, I'll just..."

                    stella "I do, however, have something to sell to you."

                    you "Sell?"

                    "She extends her gloved hand, and shows you a tiny blue pebble."

                    stella "Look at this baby. This is actually a fully operational water rune."

                    you "What does it do?"

                    stella "Used in the right way, it can turn water magic against its wielder. Invaluable for ship defense."

                    you "Water magic? Like the one Mizuki seems to be using?"

                    stella "I paid precious little attention to your tedious story, but yes, if your target is using water magic, this rune could significantly weaken her."

                    you "That seems great..."

                    stella "So, 1,000 gold. No haggling."

                    you "That's a bit steep."

                    stella "Fine, I'll find another buyer."

                    you "Wait!"

                else:
                    stella "Came back for the Water stone, haven't you? I knew you would."

                if MC.gold >= 1000:
                    menu:
                        _("Okay (pay 1,000 gold)"):                            you "Okay, I'll take it."

                            play sound s_gold
                            $ MC.gold -= 1000
                            $ story_flags["water rune"] = True

                            call receive_item(water_rune) from _call_receive_item_21

                        "Maybe later":
                            you "1,000 gold is more than I can afford. Maybe next time."

                            stella "Out of my way, then. I've got actual paying customers to tend to."

                else:
                    you "I don't have the money yet, but..."

                    stella "Oh, come on. Find it."

                    stella "Why don't you do right, like some other men do? Get out of here, get me some money too."

    elif ninja == NPC_haruka:
        if npc == NPC_kenshin: # High security prisoners, Demon-worship
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True

            play sound s_sigh

            kenshin "Still playing amateur detective, are you? *sigh*"

            kenshin "You're wasting your time. Zan's prison, Xotar, is operated by the Knights, and it has the best security conditions in Xeros."

            kenshin "No one comes in or out without my knowledge. And I've never heard this extravagant tale of a one-armed Kunoichi being taken in."

            you "Are you sure? But how can you know all of the prisoners there? It's a huge place, it surely holds over a thousand people..."

            kenshin "Hmph, don't question me! Of course I don't know the names of all the common rabble that rots in the regular prison quarters."

            kenshin "But the maximum security area of the Prison, which would be the only one suitable to hold a trained assassin? I know all of the prisoners there, I handle the paperwork myself."

            kenshin "I make a point of it. These are the most dangerous individuals in Zan."

            if story_flags["c1_path"] != "evil":
                kenshin "Or were..."

                you "What was that?"

                kenshin "Uh? Nothing. I was just thinking about the corrupt guard Captain that you helped captured."

                you "Why? What happened to her?"

                kenshin "A security breach. No need to say more."

                you "Wait. I thought you had the best security? But someone still passed through?"

                kenshin "Those stupid guards took advantage of my knights being away! It should never have happened, and..."

                kenshin "Why am I justifying myself to YOU?" with vpunch

                you "Still, as you can see, some things remain out of your control."

            else:
                you "But something may have slipped past you."

            kenshin "Nonsense! And don't even get me started on those rumors..."

            you "Rumors?"

            "She stiffens and bites her lip. You can tell she told you too much."

            kenshin "Don't..."

            you "Please, I need to know. This could be important for the inquiry. The Princess gave me a task, remember?"

            kenshin "Trust me, this is absolutely trivial. The rumors of demon-worship within the Knights' ranks are disgraceful, and I won't tolerate any of them."

            you "Demon-worship? Wait a second..."

            kenshin "I'm not going to entertain your idle questions anymore! I have important business to attend!"

            you "But Haruka, the Kunoichi... She mentioned a cult of demon-worshippers..."

            "Kenshin gives you an ice-cold look."

            kenshin "This is just a stupid coincidence. Now, instead of insulting the good name of my knights, why don't you take a hike, before I indulge the urge to unsheath my blade?"

            you "There's no need to act like this... We could be frie..."

            kenshin "GET. OUT!!!" with vpunch

            "You retreat before her fury. Still, you learnt a good deal about the Prison."

            play sound s_spell

        elif npc == NPC_knight: # High security prisoners, Demon-worship
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True

            knight "I see now why Lady Kenshin was worried about you snooping around, playing amateur detective."

            knight "You're wasting your time. Zan's prison, Xotar, is operated by the Knights, and it has the best security conditions in Xeros."

            knight "No one comes in or out without our knowledge. And I've never heard this extravagant tale of a one-armed Kunoichi being taken in."

            you "Are you sure? But how can you know all of the prisoners there? It's a huge place, it surely holds over a thousand people..."

            knight "Hmph, don't question me! Of course I don't know the names of all the common rabble that rots in the regular prison quarters."

            knight "But the maximum security area of the Prison, which would be the only one suitable to hold a trained assassin? I know all of the prisoners there, I used to handle all the paperwork for Lady Kenshin to review personally."

            knight "She made a point of it. These are the most dangerous individuals in Zan."

            knight "And don't even get me started on those rumors..."

            you "Rumors?"

            knight "Trifles. The rumors of demon-worship within the Knights' ranks are disgraceful, and we won't tolerate any propagation of this slander."

            you "Demon-worship? Wait a second..."

            knight "I'm not going to entertain your idle questions anymore! Solving Lady Kenshin's death is my number one priority."

            you "But Haruka, the Kunoichi... She mentioned a cult of demon-worshippers..."

            "He heaves a exasperated sigh and points at the door."

            knight "Sod off!"

            "You retreat before he sends his guards to manhandle you. Still, you learnt some things about the Prison."

            play sound s_spell

        elif npc == NPC_carpenter: # prison secrets, prisoner fake identity
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True

            carpenter "Oh, hey, Boss! Nice of you to come here and chat."

            carpenter "Not sure I know anything about that yellow-clad missus, 'm afraid."

            carpenter "I know plenty about the Prison, though..."

            you "Really? You do? Were you in jail?"

            carpenter "Oh no, lordy Ariossy, no!"

            carpenter "But that gig I had a while back, when we met, remember?"

            carpenter "I had been working a lot in and around the Prison. There's always work for a carpenter in there, although my so-called 'Master' took it way too far..."

            carpenter "I usually just went in to do some repairs, doors, beds, support beams... Wood gets damaged quickly; the whole place is damp as fuck, especially in the basement where they have the worst criminals."

            you "The worst criminals? Like who?"

            carpenter "Well, I'm not sure, Boss... When the knights talk between themselves, they use nicknames. 'Long ears', 'Butcher', 'Cindirella', that sort of thing."

            carpenter "One of 'em knights took a fancy to me, got loose-lipped while trying to get me drunk."

            carpenter "Said they gave fake names to the special VIP prisoners, especially when they're people the King hisself wants there... They even fake the paperwork, too."

            you "Interesting... Anything else you can tell me about the Prison?"

            carpenter "Well, sure... Get this: the Xotar Prison was not always a jail. In fact, it's built on top of a much, much older building."

            "Really? What kind of building?"

            "She spits."

            carpenter "No one knows that, Boss. The place is real {i}ancient{/i}. Summerians built it, or sumethin'."

            you "The Cimerians?"

            carpenter "Yeah, whatever. Fucking elves, or dwarves, or gnolls, hell if I can tell the difference."

            carpenter "That's where that weird name, 'Xotar', comes from. Means 'the Hub' or sumethin', in their Arios-forsaken language."

            carpenter "But one thing's pretty clear: That building was no prison. Too many ways in and out. In fact there are some paths even the Knights don't know about."

            you "And you know about them?"

            carpenter "Err... Not really. I've seen some old plans, not accurate enough to pinpoint anything."

            carpenter "But I remember there are hidden pathways, to the Sewers especially..."

            you "Oh, the Sewers. Lovely. I was just itching to go back down there..."

            carpenter "Well, whatever floats your junk, Boss."

            "You thank Iulia for her information. There's surely something useful here."

            play sound s_spell

        elif npc == NPC_ramias: # Demon-worship, High security prisoners
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True

            ramias "I don't know anything about that girl, but the Prison? Might have heard a thing or two."

            you "You have? When?"

            ramias "From the Knights themselves, oddly enough. They're not a talkative bunch, but the circumstances were special. I was applying for a job."

            you "A job? At the Prison?"

            ramias "Well, that wasn't my original intention. I wanted to see if the Knights needed another sword arm at the castle, but the snooty bastards took issues with me not being a blue blood."

            ramias "Instead they offered me a low-level guard job at the Prison... I should have said no from the start, but I was damn broke."

            you "What did they tell you?"

            ramias "Well, there are several areas in the Prison. The largest is on the ground floor, easily the size of a village. It holds the common criminals, where they live in incredible squalor."

            ramias "Seasoned murderers cohabit with infortunate plebs who stole a load of bread, and that goes as well as you can expect."

            ramias "The upper floors are for well-connected prisoners, or simply paying ones. They get access to better cells, sometimes single, and guaranteed food and drinks on most days."

            ramias "Have their own bathing area too, so they get shanked a lot less."

            ramias "Finally, there's the basement floor, or floors. It's the maximum security area. Who knows what goes on in there."

            ramias "Regular guards aren't allowed to pry."

            you "And where did you want to work?"

            ramias "Turns out, nowhere. I'm a fighter, but I'm not one for lording over orphans and widows that fight for scraps of bread."

            ramias "The privileged assholes upstairs would really get to me. Never cared for pandering to rich or highborn crybabies, and I've seen more than my share among the brass in the army."

            ramias "That leaves the maximum security prison... I thought about it at first, because there was an air of danger about it that appealed to me."

            ramias "Told me they lost a couple of guards just a week before, sounded more exciting than the rest."

            you "That's, uh... One way to see it."

            you "Still, you turned them down?"

            ramias "Sure did. Before I said yes, I did a bit of research by hitting the taverns. What I learnt, I didn't like one bit."

            you "What was that?"

            ramias "There were many disturbing rumors about the place, but that's to be expected. The King and his knights are not really famous for their leniency with criminals or political opponents alike."

            ramias "But the demon-worshipping stuff? Arios no, I may forget to go to church more often than not, but I ain't going near that with a ten-foot spear."

            you "Demon-worship?"

            ramias "Yup. Too much noise on the street about strange noises and lights at night, forbidden rituals... Most of the max security prison guard is corrupted, or so I heard."

            ramias "I have no doubt when the time was right, they would have tried to enlist me in their unholy schemes."

            ramias "Then I might have had to gut them, and all of that was a lot more trouble than I was asking for. I'd rather keep going with the weapon seller gig, thank you very much."

            you "This talk of demons and conspiracy sounds a little far-fetched, if you ask me."

            ramias "Mayhaps, can't say for sure. But I've found time and again that there's more truth in the divagations of drunkards than in the honey-tongued lies of the powers-that-be."

            you "Thanks for the intel, anyway. I hope it can bring me closer to catching my mark."

            play sound s_spell

        elif npc == NPC_maya: # C1 good / prison secrets, prisoner fake identity
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True

            maya "Kunoichi, uh? Woah, you're really doing a great job at keeping yourself in trouble."

            you "I do what I can."

            maya "You know, it's funny you should mention the Prison. I've been putting old Captain Farah's books in order lately, and some things struck me as odd."

            you "You mean... Beyond her habit of spending half the city taxes on designer lingerie?"

            maya "Yup. See, we have a register of all the criminals that were transferred to the Prison. There's a few of those each month."

            you "And?"

            maya "Well, there's at least two dozen names in there that I've never heard of. They don't match any other records. And I pride myself on knowing most if not all of our detainees."

            you "What does it mean?"

            maya "My best guess is, they were prisoners in transit, coming from outside the city. But such prisoners are usually fully registered when they come in, those were not."

            maya "And their names are the kind of usual drivel lazy spooks would use to forge records."

            maya "'Dick Puncher'? 'Bobobobo Bobobo'? 'Wolf Blitzer'?"

            maya "Obviously made up. They really didn't put in any effort."

            you "So who {i}were{/i} those prisoners?"

            maya "Beats me, but they were all bound to the maximum security part of the Prison."

            maya "I know the old Captain would sometimes send out those secret transfer convoys. But the Palace has yet to ask me to do the same."

            you "Secret convoys?"

            maya "Yeah. Always leaving at night, those. Single prisoner, heavily armed escort."

            maya "I was never chosen for escort duty, Farah preferred to send her lapdog, Sergeant Kashiv. I always suspected something was fishy."

            you "Anything else you can tell me?"

            maya "Well, it's not a lot to go on about, but... Kashiv, when she came back from such errands, she always smelled like a sewer. Arios knows where she had been."

            you "Like the Sewers, uh? Could it be she accessed the Prison that way?"

            maya "Who knows? But this kind of experience makes you hate barracks and sharing bunk beds."

            "You thank Maya for the information."

            play sound s_spell

        elif npc == NPC_lieutenant: # c1 neutral / prison secrets, prisoner fake identity
            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True

            lieutenant "Oh, my dear [MC.name]. It's been a while. We had a good time, last time, uh?"

            "You remember the night you spent together."

            you "Hmmm... We sure did."

            lieutenant "But I understand you're here on business. My pride is hurt, but only a little."

            you "Well..."

            lieutenant "Let's cut to the chase. You mentioned a certain wounded Kunoichi, and how she was sent to Xotar Prison. I think I know something about that."

            you "Really?"

            lieutenant "Yes. You see, our old Captain used to take some hefty bribes to organize prisoner convoys of a certain kind, all with the utmost discretion, which was unusual for her."

            you "What kind of prisoner convoys?"

            lieutenant "Lone prisoners, two at most, under secret identities. The guards would come in from the road at night, load the prisoner in a box that was almost like a casket, and carry them to the Prison with an escort of guards and knights hidden in civilian clothes."

            lieutenant "Sergeant Kashiv always carried out the Captain's dirty deeds, so she was usually in charge of the escort."

            lieutenant "They'd go down into the Sewers, where I hear there are secret passages that lead into old parts of the Prison. You'd never hear from the poor sods again."

            you "How do you know about that?"

            lieutenant "I did some spying on account of Renza on such convoys, to see if they were hiding anything valuable. One night, I caught a glimpse of the prisoner as they were locking her in the box."

            lieutenant "Even though the light was low, one thing stood out... The lady only had one arm."

            you "I see! So they took her into the Sewers?"

            lieutenant "Yes. And that's the last anyone will probably hear from the poor lass, Shalia embrace her."

            "You thank the Lieutenant for the information and head back to the city, lost in your thoughts."

            play sound s_spell

        elif npc == NPC_sergeant: # c1 evil / prison secrets, prisoner fake identity

            if npc.flags["interrogation"] in ("beaten", "raped"):
                sergeant "You..."

                "Her face whitens with fear. She remembers what you did to her."

                sergeant "Get away from me! One more step and I'll kill you, you bastard!"

                "You quickly leave before she recovers from her shock and stabs you."

                return

            else:
                sergeant "I'd be damned... You dare to show your face here? Don't think I forgot the last time we met..."

                you "Call us even then. You tried to get me killed."

                you "And don't forget our mutual friend the good Captain Farah... I'm sure she would take issue with you fighting me over an old grudge."

                sergeant "Grr..."

                play sound s_sigh

                sergeant "You are correct. *sigh*"

                sergeant "Fine, I'll tell you what I know about the Prison, if it gets you out of my sight faster."

                sergeant "While there's nothing special about the Prison on the surface, the special convoys are noteworthy."

                you "Special convoys?"

                sergeant "Yup. When the Prison gets a 'VIP' prisoner, courtesy of the King, they sometimes arrives in a special convoy. Means no traces are left in the system."

                sergeant "When the Guard was involved, which was rare because no one is usually interested in VIP prisoners coming from outside the walls, I was one of those trusted with the package."

                you "The package?"

                sergeant "More like a sedan chair, really, except it's a chained metal one, and it's damn heavy."

                sergeant "No one involved in the convoy knows who we're escorting. They give him or her a fake name, and the Knights warn you in no uncertain terms than any attempt at peaking inside will end with your head on a pike."

                sergeant "As if all of that wasn't enough, they have us enter through a secret passage in the Sewers. Can't allow anyone to see who's coming in and out of the maximum security prison."

                you "And where might I find this secret doorway, exactly?"

                sergeant "Hell if I know. It's in the Sewers, but they blindfolded us as soon as we were there and had us follow the Knight's voice to move on."

                sergeant "I hated every minute of it. The blindfold makes you notice the smell a lot more, and I nearly stumbled into the waste stream a dozen times."

                sergeant "Anyway, that's all I know. Scram now, will you?"

                "You reflect on what she told you. Could this help with your chase?"

            if not npc.flags["seen ninja hint"]:
                $ ninja.flags["hints"] += 1
                $ npc.flags["seen ninja hint"] = True

            play sound s_spell

        elif npc == NPC_goldie: # Earth rune
            if story_flags["earth rune"]:
                goldie "I'm sorry, [MC.name], I'm afraid I can't help you further. I only had the one rune I gave you."

            else:

                if not NPC_goldie.flags["introduce earth rune"]:
                    $ NPC_goldie.flags["introduce earth rune"] = True

                    goldie "Ninja women with a dark and terrible past? Wow, [MC.name]! What an exciting and glamorous life you're living..."

                    you "Yeah, well, I hope this isn't the kind of adventure that ends with me taking a shuriken to the back of the head."

                    goldie "Oh, don't say that, [MC.name]! If anything happened to you, I would be unconsolable..."

                    "She looks genuinely worried about you."

                    goldie "You know, I think I have just the thing. It's been in my family for generations, my Pa' used to say it would bring us good luck."

                    goldie "It's a runic stone, the kind that shamans of old used to fashion in the way the Cimerians did. Or so they said."

                    goldie "This one has the Earth symbol, so it's appropriate if you're after an Earth ninja. Maybe. I don't really know anything about ninjas, except from novels."

                    you "Thank you... This looks expensive, are you sure I can have it?"

                    goldie "Well... It's true that I don't have a lot to go on these days, but if it's you... *blush*"

                    you "(This would probably fetch hundreds of denars on the market... What should I do?)"

                else:
                    goldie "Oh, [MC.name], you(re back. I assume this is about the Earth stone?"

                label c2_goldie_buy_rune():
                    menu:
                        "What will you do?"

                        _("Grab the stone for free"):                            you "(This offer is too good to pass.)"

                            you "Thank you Goldie, I'll have the stone, then."

                            "She gives a last look at the stone, and you can see some anguish in her eyes. But she steels her resolve, and gives it to you."

                            $ MC.good -= 1

                        "Give her 500 gold for it":
                            if MC.gold < 500:
                                "You don't have enough money."
                                jump c2_goldie_buy_rune

                            "You give her the minimum price you think such a stone could be worth."

                            you "Here, please take this gold as compensation. I wouldn't feel right depriving you of such a valuable object when you're struggling."

                            goldie "Oh, thank you... You didn't have to..."

                            you "You're welcome."

                            $ MC.neutral += 1
                            $ NPC_goldie.love += 1

                            play sound s_gold
                            $ MC.gold -= 500

                        "Give her 1,000 gold for it":
                            if MC.gold < 1000:
                                "You don't have enough money."
                                jump c2_goldie_buy_rune

                            "You give her a good price for what you think the stone is worth."

                            you "Here, I don't want to cheat you of such a valuable object in yout time of need."

                            goldie "Oh, thank you! This is too much!"

                            you "No, please, have it. It's my pleasure."

                            goldie "Thank you so much!"

                            "She gives you a grateful kiss."

                            $ MC.good += 1
                            $ NPC_goldie.love += 1

                            play sound s_gold
                            $ MC.gold -= 1000

                        "Come back later":
                            you "Thank you for your offer, but I can't accept just yet. I will be back."
                            return

                    $ story_flags["earth rune"] = True

                    call receive_item(earth_rune) from _call_receive_item_22

                    goldie "May it protect you from harm, dear [MC.name]."

                    you "Thank you sweetie."

    $ unlock_achievement("suzume hint")

    return


## Unlocking ninjas ##

label c3_unlock_narika():

    hide screen districts

    play music m_suspense fadein 3.0

    show bg narika intro at sepia with dissolve

    if NPC_narika.flags["hint recap"]:
        menu:
            suzume "So, I think we've gathered enough intel about the Void ninja! What do you want to do?"

            "Can you recap the intel again?":
                pass

            "Visit the Magic University":
                if NPC_narika.flags["magicu failed"]:
                    you "Yeah, after what happened I don't think I can show my face around there for some time."
                else:
                    call c3_narika_MU_visit() from _call_c3_narika_MU_visit
                return

            "Try to catch her again":
                if story_flags["ninja hunt"] == calendar.time:
                    "You can only attempt to catch a ninja once a day."
                    return

                hide screen overlay
                scene black with fade
                show bg rooftop at top with dissolve
                call ninja_game(NPC_narika) from _call_ninja_game_3
                return

            "Look for her later in the city":
                return

    else:

        suzume normal "I think now we have a pretty good idea of what that little brat is up to!"

        you "Have we? Can you recap?"

    suzume "Sure. Here's what we've gathered so far."

    suzume "Narika is organizing a heist of some sorts. She may have a powerful backer."

    if NPC_narika.flags["upper city hint"]:
        suzume "It's clear her mark is in the upper city. That's beyond our current reach, but we can probably get a safe-conduct from the Princess."

    if NPC_narika.flags["uniform hint"]:
        suzume "We also know it's a place where they wear uniforms. That's an important clue."

    if NPC_narika.flags["school hint"]:
        suzume "And the mark is a school. That narrows it down significantly."

    if NPC_narika.flags["magic hint"]:
        suzume "Finally, she's going after a magical artefact! There are only a few places where such important magical items could be found."

    suzume "Which means..."

    you "The Magic University."

    suzume "Of course. See, it wasn't hard."

    suzume "Void ninjas don't rely on magic to be effective, so they are better suited to taking on a target with magical protection. It must have been important to whoever recruited her."

    you "Fine. Now, we know what she's after. But how do we get to her?"

    suzume "Well, I see a couple of ways to go about this."

    you "Tell me."

    suzume "First, you could report your findings to the Dean of Magic U."

    suzume "They would be able to thwart the heist, and probably have the means to lock the Void ninja up."

    suzume "In doing so, we would be gaining a useful ally, as well as fulfilling the Princess's mandate."

    you "I see. Anything else?"

    suzume doubt "There's another option. It's a little unorthodox, even for you... But hear me out."

    suzume normal "What if we {i}helped{/i} her steal that artefact?"

    you "Whaaat?" with vpunch

    suzume "Think about it. We could split the proceeds of the heist, and make her an ally. Then we'd get her to spill the beans about her backer."

    you "Err, I don't know if the Princess would like us to do that."

    suzume "Aha, but think about it this way: there's no love lost between the Royals and the Mages."

    you "There isn't?"

    suzume "Nope. The Zanic Magic Guild remained neutral during the change of dynasty 25 years ago. They waited until power was well into the hands of the Pharo dynasty to begrudgingly declare allegiance."

    if MC.playerclass == "Wizard":
        you "It's nothing personal, wizards are not supposed to meddle in regime change. Too many bad precedents."
    else:
        you "An abundance of caution, eh? So much for scheming wizards."

    suzume "Anyway, King Pharo always keeps the Magic Guild at arm's length, knowing they are unreliable allies."

    suzume "If you can get Narika to leave Zan's nobility in peace, the Princess might just turn a blind eye to you messing with the Magic University."

    you "Hmmm..."

    $ NPC_narika.flags["hint recap"] = True
    $ NPC_narika.flags["hunt stage"] = 3
    $ NPC_narika.location = spice_market

    if MC.has_item(void_rune.name):
        suzume "I can think of something else. Remember that Cimerian device you bought?"

        you "The Void Rune? It's supposed to slow down time?"

        suzume "Yes. I can see how that could mess with her powers. If you can catch her again in the city, maybe we could beat her this time."

        if NPC_freak.flags["holding info"]:
            suzume "And put her in one of the Cimerian-built cells the perverted old man mentioned."

            you "So you know about that, uh."

            suzume "Yup."

        else:
            suzume "But you lack the means to hold her. We would have to deliver her to the Princess quickly and get it over with."

            suzume "Unless you can figure out a way to keep her locked up."

        you "Capturing her, hmmm..."

    jump c3_unlock_narika

label c3_unlock_haruka():

    # Hints: High security prisoners, Demon-worship, prison secret passage, prisoner fake identity

    hide screen districts
    play music m_suspense fadein 3.0

    show bg haruka defeat1 at sepia with dissolve

    if NPC_haruka.flags["hint recap"]:
        menu:
            suzume "So, I think we've gathered enough intel about the Earth ninja! What do you want to do?"

            "Can you recap the intel again?":
                pass

            "Let's negotiate with her":
                call ninja_game(NPC_haruka) from _call_ninja_game_5
                # call c3_haruka_final_intercept() from _call_c3_haruka_final_intercept
                return

            "Let's warn the guards she's coming" if not story_flags["haruka told guards"]:
                hide screen overlay
                call c3_haruka_guards() from _call_c3_haruka_guards
                return

            "Look for her later in the city":
                return

    else:
        suzume normal "I think we've gathered enough intel about that stuck-up Earth ninja and her scheme!"

        you "Did we? Let's do a recap."

    suzume "Well, it's obvious that she is trying to rescue her former mentor, Subaru."

    suzume "She was captured in the destruction of their temple, far away from here."

    show bg prison at sepia with dissolve

    suzume "And Haruka believes Subaru is being kept in the city's Prison. If she is, she must be in the basement, where the {b}maximum security quarters{/b} are located."

    you "But there is no record of her ever being there."

    suzume "True, but it does not necessarily mean she isn't. As we've learnt, sometimes they bring secret convoys to the Prison, {b}registering captives under fake names{/b}."

    you "Kenshin leads the Royal Knights, and she told us that she knows all about the high-security prisoners. She didn't mention Subaru."

    suzume doubt "Well, maybe she got sloppy. Or..."

    suzume "Kenshin may be in on the plot. You should be careful around her."

    suzume "Regardless, they go to great lengths to avoid scrutiny, even bringing in the captives through a {b}secret passage in the Sewers{/b}."

    you "Shady stuff..."

    suzume "That's right. That leads us to the most concerning piece of the puzzle..."

    you "Which is?"

    suzume "{b}Demon-worshippers{/b}. Some of our contacts have mentioned rumors, and they're the ones who abducted Subaru in the first place."

    suzume doubt "If there is any chance demon-worshippers are being involved, we should be extra careful."

    you "*gulp*" with vpunch

    suzume shrewd "That's a lot to take in."

    you "Sure, but... How does it help us catch Haruka? That's our goal, remember?"

    suzume doubt "Well, the way I see it, you have a few options."

    you "I do?"

    suzume "All the information we've gathered could prove valuable to Haruka. Maybe we can strike a deal with her."

    suzume "We just want her to stop murdering people in the city. The sooner she frees Subaru, the faster she'll get out of our hair."

    you "What if in freeing her, she murders a bunch of people?"

    suzume shrewd "Well... As long as they're not rich and famous, I don't think the Princess would care much."

    you "What other options do I have?"

    suzume doubt "We could go to the prison guards and warn them, in exchange for their help catching her."

    you "That sounds sensible... But what if they're as corrupt as the guard in the Slums? I don't see why they wouldn't be."

    suzume "Then we can attempt to turn that to our advantage, maybe strike a deal with them or something."

    you "Hmm..."

    $ NPC_haruka.flags["hint recap"] = True
    $ NPC_haruka.flags["hunt stage"] = 3
    $ NPC_haruka.location = prison

    if MC.has_item(earth_rune.name):
        suzume "And finally, there's that magic stone you found."

        you "The Earth Rune? Would that work on her?"

        suzume "The only way to know is to try it. If you can catch her again in the city, maybe we can pass her defenses this time."

        you "Then I could capture her on my own..."

        if NPC_freak.flags["holding info"]:
            suzume "And maybe throw her in one of the magic-proof cells the perverted old man mentioned."

            you "Maybe. Wait a- Do you just follow me everywhere?"

            suzume "Sure."

            you "{i}Everywhere{/i}?" with vpunch

            suzume "Yup."

            you "..."
        else:
            suzume "Sure. But if you have no way to hold her, you will have to turn her in for a reward."

    jump c3_unlock_haruka


## Papa Freak events ##

label c3_papa_cells():

    hide screen overlay
    scene black
    show bg papa_freak at top
    with dissolve

    if NPC_freak.flags["cells built"] >= 4:
        papa "I have built everything I could for you, young lad. It's nice of you to visit, though."

    elif not NPC_freak.flags["requirements"]:
        if not NPC_freak.flags["cells built"]:
            papa "So, for starters... I'm looking for a great cocksucker."

            papa_apprentice "Papa likes it wet and nice, uh..."

            you "I don't need details. Please."

            papa "Bring us a whore that offers great service, is beautiful and perverted, and we'll build you a cell."

            "Bring a whore to Papa with at least {b}75 in Service, Beauty and Libido{/b}."

            $ game.set_task("Bring a whore to Papa with at least 75 in Service, Beauty and Libido.", "papa", blocking=False)
            $ NPC_freak.flags["requirements"] = [("service", 75), ("beauty", 75), ("libido", 75)]

        elif NPC_freak.flags["cells built"] == 1:

            papa "Now Papa wants to reward his apprentice. He's been working hard, lately."

            papa_apprentice "Oooh, thank you, Papa!"

            papa "But we'll take turns, of course. Can't let you have all the fun."

            papa_apprentice "Ew, I knew there was a trick."

            papa "What kind of girl would you like, my boy?"

            papa_apprentice "Well, good at sex, of course... With a good personality, and a sensitive body... Hmmm. *drool*"

            "Bring a whore to Papa with at least {b}75 in Sex, Charm and Sensitivity{/b}."

            $ game.set_task("Bring a whore to Papa with at least 75 in Sex, Charm and Sensitivity.", "papa", blocking=False)
            $ NPC_freak.flags["requirements"] = [("sex", 75), ("charm", 75), ("sensitivity", 75)]

        elif NPC_freak.flags["cells built"] == 2:

            papa "Did you like that last one, my boy?"

            papa_apprentice "I did... I had such a great time."

            papa "But you wanted more, didn't you? Can't hide it from Papa..."

            papa_apprentice "Well... It's true. I wish I could have fucked her ass."

            papa "Anal? You kinky little rascal."

            papa "All right, our next order is: an anal whore! She must have a good body, of course, and be obedient."

            "Bring a whore to Papa with at least {b}75 in Anal, Body and Obedience{/b}."

            $ game.set_task("Bring a whore to Papa with at least 75 in Anal, Body and Obedience.", "papa", blocking=False)
            $ NPC_freak.flags["requirements"] = [("anal", 75), ("body", 75), ("obedience", 75)]

        elif NPC_freak.flags["cells built"] == 3:

            papa "This one must be special. I have this list of fantasies I have yet to achieve..."

            papa_apprentice "Papa wants to get frea-kyyyy~..."

            you "Please. Don't do that. "

            extend "Ever. "

            extend "Again."

            papa "Bring me a whore with kinky tastes, who is both refined and physically resilient. This is our last order! Let's make her count!"

            "Bring a whore to Papa with at least {b}75 in Fetish, Refinement and Constitution{/b}."

            $ game.set_task("Bring a whore to Papa with at least 75 in Fetish, Refinement and Constitution.", "papa", blocking=False)
            $ NPC_freak.flags["requirements"] = [("fetish", 75), ("refinement", 75), ("constitution", 75)]

        scene black with fade

        return


    else:
        $ req_skills = tuple(sk.capitalize() for sk, v in NPC_freak.flags["requirements"])
        $ req_val = NPC_freak.flags["requirements"][0][1] # Cannot handle separate skill requirements for now
        $ req = and_text(req_skills)

        if MC.girls:
            "Choose a girl from your brothel to bring with you (reminder: she must have at least [req_val] in [req], and be open to whoring)"
            $ girl = long_menu("Choose a girl", [(g.fullname + " (%s %i, %s %i, %s %i)" % (req_skills[0], g.get_stat(req_skills[0]), req_skills[1], g.get_stat(req_skills[1]), req_skills[2], g.get_stat(req_skills[2])), g) for g in MC.girls])
        else:
            "You cannot satisfy Papa Freak's requests, as you have no girls in your brothel."
            return

        scene black with fade
        show bg papa_freak at top with dissolve

        papa "So, my young friend, have you brought me a suitable whore?"

        you "Yes, Papa. I would like you to meet [girl.name]."

        call dialogue(girl, "girl introduction") from _call_dialogue_252

        papa_apprentice "She's hot! I like her."

        papa "Let me see..."

        python:
            for stat, val in NPC_freak.flags["requirements"]:
                if girl.get_stat(stat) < val:
                    failed_stat = capitalize(stat)
                    break
            else:
                failed_stat = None

        if debug_mode:
            menu:
                "Force success"

                _("Yes"):                    $ failed_stat = None

                "No":
                    pass

        if failed_stat:
            papa "No, that won't do, that won't do at all... I'm sorry, young lady. Come back when you've had more training."

            "You need a girl with higher {b}[failed_stat]{/b} to satisfy Papa Freak's request."

            return

        papa "She looks perfect... Come now, my pretty, Papa and his young apprentice have been waiting for you..."

        girl.char "What is it about, Master?"

        "You explain what she needs to do."

        $ sex_act = NPC_freak.flags["requirements"][0][0]
        $ forced = False

        if debug_mode:
            menu:
                "Force success"

                _("Yes"):                    $ forced = True

                "No":
                    pass

        if not girl.will_do_sex_act(sex_act) and not forced:
            play sound s_surprise
            if sex_act == "service":
                girl.char "Suck that old man's junk? No way! Don't make me!"
            elif sex_act == "sex":
                girl.char "Sleep with those guys? No! I don't want to!"
            elif sex_act == "anal":
                girl.char "Take it in the ass, from them? No!!!"
            elif sex_act == "fetish":
                girl.char "Ew, but I don't want to do kinky things with those two! No way!!!"

            papa "I see. Boy, isn't that a sad turn of events..."

            papa "But I won't force anybody. Please come back when she's more open-minded about [sex_act]."

            "The girl needs to agree to {b}[sex_act]{/b} acts before you can satisfy Papa Freak's request."

        else:

            girl.char "I understand, Master [MC.name]. I will do my best."

            papa "That's the spirit! Now, come here, I would like to see those titties up close... Fuhahahaha!"

            scene black with fade

            play sound s_moans_short

            show screen show_img(girl.get_pic(sex_act, "naked", hide_farm=True))
            with dissolve

            girl.char "Oh, aaah, oooh!!!"

            papa "Yes! Yes! Just like this!!!"

            show screen show_img(girl.get_pic(sex_act, "service", "naked", and_tags="cumshot", hide_farm=True))
            with flash

            play sound s_orgasm_fast

            girl.char "Aaaah!!!"

            with doubleflash

            hide screen show_img
            scene black
            with fade

            show bg papa_freak at top with dissolve

            papa "Oh boy... She's really something. Can I get another go?"

            you "Yes. But you must build me a cell, first."

            papa "You got it. What will it be?"

            menu:
                extend ""

                "Build me a cell with a Void ward" if not story_flags["void ward"]:
                    $ target = "void"

                    papa "This is a complex element, if it is an element at all... Fortunately, the old Cimerians knew a thing or two about manipulating time and space."

                "Build me a cell with a Water ward" if not story_flags["water ward"]:
                    $ target = "water"

                    papa "Ah, water... I've this special desiccant technology I've been experimenting with. I thought it was only good for preserving cookies, but I might find a use for it after all"

                "Build me a cell with an Earth ward" if not story_flags["earth ward"]:
                    $ target = "earth"

                    papa "This is straightforward enough. Metal blocks most Earth magic. A cell made entirely of steel would do the trick."

                "Build me the cell with a ward against Air and Fire" if (story_flags["void ward"] and story_flags["water ward"] and story_flags["earth ward"]):
                    $ target = "air and fire"
                    $ story_flags["air ward"] = True
                    $ story_flags["fire ward"] = True

                    papa "Two elements of swift movement and destruction... Earth blocks most of their effects, so we'll take the cell that's deeper underground. And those runic stabilizers should do the rest."

            $ story_flags[target + " ward"] = True

            scene black with fade

            play sound s_saw

            pause 0.3

            play sound2 s_clash

            pause 0.3

            play sound s_vibro

            papa_apprentice "Phew... *pant* *pant*"

            papa_apprentice "Everything is in place, Papa, just like you instructed."

            papa "Perfect! Here you go, young man, just as we agreed. You now have a nice holding cell that will ward against [target] powers."

            $ NPC_freak.flags["cells built"] += 1
            $ NPC_freak.flags["requirements"] = None

            $ renpy.block_rollback()

            if (story_flags["void ward"] and story_flags["water ward"] and story_flags["earth ward"] and story_flags["fire ward"]):
                papa "This was the last one. Your basement is now fit to capture a small army of elemental ninjas."

                you "I was going to install a game room, but that works too."

                papa "See you around soon, my boy!"

                $ NPC_freak.location.action = False
                $ game.set_task(None, "papa")

                you "Sure."

            elif NPC_freak.flags["cells built"] < 3:
                you "Can you build me any more holding cells?"

                papa "Can I? Sure. But will I? There needs to be something in it for me..."

                you "All right. Name your poison."

            elif NPC_freak.flags["cells built"] < 4:
                you "So this is it, then?"

                papa "Well... There is one more elemental cell I could restore, but you didn't ask me about it..."

                you "Which one?"

                papa "The Air and Fire ward room. It blocks not one but two elements. Nice, isn't it?"

                you "Yeah... But I have no need to imprison someone with one of those elements."

                papa "Not now you don't, but if the eventuality presented itself, wouldn't it be nice to have a cell ready?"

                you "*sigh* What do you want for it?"

            jump c3_papa_cells

    scene black with fade

    return


## Homura city events ##

label c3_contact_homura():

    "You remember what Homura told you about tying her ribbon to a pole at the Plaza to summon her."

    if NPC_homura.flags["is summoned"]:
        you "I already tied the ribbon to summon her. She will come to me, eventually?"

    elif brothel.has_room("okiya"):
        you "Here, let's see if that does the trick."

        if blue_ribbon in MC.items:
            $ MC.items.remove(blue_ribbon)
            $ plaza.action = False

        $ calendar.set_alarm(calendar.time, StoryEvent(label = "c3_homura_visit", type = "night"))

        $ NPC_homura.flags["is summoned"] = True

    else:
        you "She did mention I needed to build an okiya first... No point in summoning her now."

        "You must buy the {b}Okiya{/b} before you can contact Homura again."

    return

label c3_homura_visit(): # Happens after tying the ribbon in the plaza

    # Doesn't happen if the final confrontation is done
    if story_flags["c3 ending"]:
        return

    scene black with fade
    show bg okiya at top with dissolve

    play music m_palace fadein 3.0

    "That night, you keep an eye out for Lady Homura. Sure enough, it isn't long before you spot her entering the Okiya, bowing politely to your staff."

    $ NPC_homura.flags["is summoned"] = False

    show bg homura_okiya happy at top with dissolve

    if not story_flags["homura summoned"]: # first visit
        $ story_flags["homura summoned"] = True

        homura normal "[MC.name]! I thought you'd never contact me again."

        homura blush "I was a bit scared, to be honest. *frown*"

        you "Why would I let you down?"

        homura "Well, I thought, because we had, hem... You know..."

        homura "I thought maybe a man in your occupation might just care about... *blush*"

        menu:
            _("Tell her you're not like that"):                $ norollback()
                you "I'm not like that, you know."

                if MC.get_alignment() == "good":
                    homura normal "I know. You're a good person."

                    homura "I'm just surprised that... You do this."

                    you "It's just a job. Besides, if this trade was only left to the bad guys, it would be bad, wouldn't it?"

                    play sound s_laugh
                    homura "You make a good point!"

                    $ NPC_homura.love += 2

                elif MC.get_alignment() == "neutral":
                    homura "Well... So you say. But I don't know if your actions match your words."

                    you "Well, I try my best..."

                    $ NPC_homura.love -= 1

                elif MC.get_alignment() == "evil":
                    homura sad "I find that hard to believe. I've heard stories about how you treat people, you know."

                    you "Uh? Who rated me out? I'll smash their..."

                    play sound s_sigh
                    homura "See? This is what I'm talking about."

                    $ NPC_homura.love -= 2

            "Tell her she's different": # For neutral characters
                $ norollback()
                you "In other circumstances, you would be right. But there's something special about you."

                homura blush "Hmmm..."

                if MC.get_alignment() == "neutral":
                    homura normal "Haha, I knew it! Well, I guess I should count myself lucky then..."

                    $ NPC_homura.love += 1

                elif MC.get_alignment() == "good":
                    homura sad "Really? That's a litle cold, coming from you. I thought you were a more caring person."

                    you "Well, maybe I should have put it differently..."

                    $ NPC_homura.love -= 1

                elif MC.get_alignment() == "evil":
                    play sound s_sigh
                    homura sad "You say I'm different, but how do I know that you don't say that to all girls? I know your kind."

                    you "Well..."

                    $ NPC_homura.love -= 1

            "Tell her you still need her": # For evil characters
                $ norollback()
                you "I'll be blunt. I'm not one for commitment. But right now, I still need you."

                if MC.get_alignment() == "evil":
                    homura blush "I expected as much... But thanks for giving to me straight."

                    homura "I'm an adult just like you... I make my choices."

                    you "It's good that we understand each other."

                    $ NPC_homura.love += 2

                elif MC.get_alignment() == "neutral":
                    homura "Okay... I see. I don't know what I was expecting. ."

                    you "Sorry about that."

                    homura "Yeah."

                    $ NPC_homura.love -= 1

                elif MC.get_alignment() == "good":
                    homura sad "Really? But Iheard such good things about you... I thought..."

                    you "Err, sorry. I mean, I care for you, but..."

                    play sound s_sigh
                    homura "Save it. It's off your chest, at least."

                    $ NPC_homura.love -= 2

        homura normal "Anyway. So, this is your new house? It's nice. The okiya looks good."

        homura sad "My ears are ringing, though... There's something odd about this place."

        if MC.playerclass == "Wizard":
            you "Ah yes, you noticed. The walls are infused with ancient magic."

            you "It normally only affects people with elemental affinity, though. You may be experiencing some kind of magic resonance. Do you have magical affinity?"

        else:
            you "Well, the previous owner mentioned something about magic wards, messing with spells or whatever."

            you "Why, are you a magic user?"

        play sound s_laugh
        homura normal "Oh, absolutely not! The less I am around magic the better. I just don't trust magic."

        you "Isn't your father a mage, though?"

        homura "Well, uh... Yes, I guess he is."

        you "You never wanted to follow into his footsteps?"

        homura "Uh... Oh, no."

        homura "He wouldn't have allowed me, anyway. Wizards think magic is better left to men."

        you "Really? But there are many women sorceresses..."

        homura "Let's just not discuss my father's views on women. He's a typical male, thinking they should use brooms to clean up the kitchen instead of flying."

        menu:
            extend ""

            "He's wrong, of course":
                $ MC.good += 1

                you "That's just wrong. Women are just as capable as men... They can do great things..."

                homura "Oh, really? Look at you, making money from whoring girl slaves out... Quite the feminist."

                you "Ouch..."

                if NPC_homura.love >= 5:
                    homura sad "Sorry, that was uncalled for."

                    you "It's all right..."

                    $ NPC_homura.love += 1

            "He's got a point":
                $ MC.evil += 1

                you "Look, he's not wrong. Women are less capable than men, it's obvious."

                you "It's only right that you should serve us..."

                play sound s_surprise
                homura surprise "What? Are you out of your mind?"

                homura "That's a new low, even for you!"

                you "Hehe, you're cute when you're angry..."

                homura "Shut up! And remove your hand!"

                $ NPC_homura.love -= 3

            "There are much more interesting things to do with women":
                $ MC.neutral += 1
                you "Such a sad lack of imagination. Women are wonderful, everywhere... Especially..."

                homura blush "S-Shut up, I know what you're going to say..."

                you "We're compatible, men and women, that's all I'm saying. *wink*"

                homura "Err, stop it..."

                homura "..."

                homura "It's kind of sexy when you talk like that, though."

        homura normal "Back on topic. You wanted to see me?"

        you "Yeah."

    else:
        homura "Hello, [MC.name]! I'm glad you called me again."

        you "Glad to see you, too."

    homura "So. Is it business, or pleasure?"

    menu:
        extend ""

        "Business":
            you "Business, I'm afraid. You remember about the task that the Princess gave me?"

            if NPC_homura.flags["divulged assignment"]:
                homura "Yes, of course. You're hunting those weird women ninjas, the kuno... Something."

                you "Right. I was wondering if you could help me figure out my options."

                homura "I'm going to do my best! Shoot!"

                call c3_homura_menu_business() from _call_c3_homura_menu_business

            else:
                homura "Of course... Are you ready to tell me more about it? I can help you!"

                menu:
                    you "Well..."

                    "Yes":
                        $ NPC_homura.flags["divulged assignment"] = True

                        you "Yes. I need help, and I don't think I can manage this alone."

                        homura "Awesome! Now tell me! I'm so curious..."

                        with fade

                        "You spend a long time telling her about your assignment and the Kunoichi."

                        with fade

                        homura "Secret female ninjas terrorizing the city... This is even better than the illegal picture books I buy at the Spice Market!"

                        homura "So, what can I help you with?"

                        call c3_homura_menu_business() from _call_c3_homura_menu_business_1

                    "No":
                        you "No, sorry."

                        homura "..."

                        you "It's really a secret. I can't talk about it."

                        homura sad "I see... But, then, I can't help you..."

                        you "Err... I guess not..."

                        homura "Such a waste of time..."

            if NPC_homura.love + dice(6) > 10:
                with fade
                homura blush "Say, [MC.name]..."

                "Homura has had a few drinks, and she now leans close to you. You can feel her hair brush against your neck."

                homura "I know you called me for a serious discussion, but... Perhaps we could take this elsewhere?"

                menu:
                    extend ""
                    "Let's go to the bedroom":
                        $ NPC_homura.love += 0.5

                        you "Of course, Lady Henso... Follow... Hey!"

                        "She's already grabbing your hand, pulling you towards the stairs."

                        call c3_homura_menu_pleasure() from _call_c3_homura_menu_pleasure

                    "Perhaps another time":
                        $ NPC_homura.love -= 0.5

                        you "I would love to, Homura, but I'm really busy right now..."

                        homura sad "Oh, I see."

        "Pleasure":
            you "Pleasure, of course."

            call c3_homura_menu_pleasure() from _call_c3_homura_menu_pleasure_1

    scene black with fade
    show bg okiya at top with dissolve
    show homura normal with dissolve

    homura "I'll be going, then. Here, take my ribbon, in case you need to contact me again."

    you "Thank you..."

    call receive_item(blue_ribbon, use_article=False) from _call_receive_item_23
    $ plaza.action = True

    return

label c3_homura_menu_business():

    menu:
        "Tell her about Narika, the Void Kunoichi" if NPC_narika.flags["locked"]:
            with fade
            "You spend a long time explaining about the Void Kunoichi and the details of your encounter."

            homura normal "I see... So she's preparing a heist, you think?"

            you "Yes. It would be good if I could figure out her target."

            homura "You need to talk to someone from the criminal world, then... Or perhaps to someone from the law, but with underground connections?"

            homura "Perhaps you can also figure out where she plans to sell her loot?"

            you "Those are all good ideas."

            homura "Anything else you can tell me about her?"

            if NPC_narika.flags["spied masturbating"]: # if event_dict["c2_narika_H1"].happened:
                you "Well... We could get a glimpse of her using a magic crystal..."

                you "She was wearing a school uniform."

                homura "Really? She's a student? That doesn't make sense!"

                homura "It must be a cover for her hit job, whatever it is..."

                homura "Perhaps ask someone who might know the city's schools?"

                you "Err, do I know anyone like that?"

        "Tell her about Mizuki, the Water Kunoichi" if NPC_mizuki.flags["locked"]:
            with fade

            "You spend a long time explaining about the Water Kunoichi and the details of your encounter."

            homura normal "A lady who doesn't age, and disappears at will... This stinks to high heaven of powerful magic."

            you "Indeed. But it's beyond the abilities of most mages I've ever seen, and yet she doesn't seem like a fully trained sorceress."

            homura "I would start with interrogating magic-users, preferably unconventional ones."

            homura "And if she's really lived for as long as she claims, perhaps ask some old-timers about her? They might know some stories."

            you "You're right."

        "Tell her about Haruka, the Earth Kunoichi" if NPC_haruka.flags["locked"]:
            with fade

            "You spend a long time explaining about the Earth Kunoichi and the details of your encounter."

            homura normal "This one looks tough-as-nails... I'm impressed."

            homura "So she's after a prisoner, you say? You need to talk to someone from law enforcement who knows the security arrangements around the prison."

            homura "They might even know where this Subaru woman is being held."

            you "Makes sense. I'll start with them."

    homura "I'm afraid that's all I got for now. I can't stay much longer..."

    you "It's alright. Thank you very much for your help."

    scene black with fade

    if story_flags["suzume hint seen"]:
        "Talk to Suzume on the {b}City{/b} screen to pay a visit to your contacts in Zan."

    return

label c3_homura_menu_pleasure():

    stop music fadeout 3.0

    # Unlocks new sex acts as the story progresses (except anal - unlocked through story)

    $ ninja_lock_count = sum(1 for x in [NPC_narika, NPC_mizuki, NPC_haruka] if x.flags["locked"])

    if ninja_lock_count >= 3 and NPC_homura.flags["H level"] == 3:
        homura normal "Pleasure! Yay!"

        homura "You know what, we still have a few hours of daylight. Why don't we go outside for a stroll?"

        you "A stroll? Not quite what I had in mind..."

        homura "Oh, come on! It will be fun!"

        call homura_river() from _call_homura_river
        $ NPC_homura.love += 1
        $ NPC_homura.flags["H level"] += 1

        return

    homura blush "I see... Let's take it upstairs, then."

    you "Come."

    scene black with fade
    show expression brothel.master_bedroom.get_pic() at top
    with dissolve

    show homura blush with dissolve

    if ninja_lock_count and NPC_homura.flags["H level"] == 1:
        call homura_69() from _call_homura_69
        $ NPC_homura.love += 1
        $ NPC_homura.flags["H level"] += 1

    elif ninja_lock_count >= 2 and NPC_homura.flags["H level"] == 2:
        call homura_cowgirl() from _call_homura_cowgirl
        $ NPC_homura.love += 1
        $ NPC_homura.flags["H level"] += 1

    else:
        homura "So. What do you want to do?"

        menu:
            extend ""

            "I want to see you masturbate":
                call homura_mast(False) from _call_homura_mast_1

                scene black with fade
                show expression brothel.master_bedroom.get_pic() at top
                with dissolve

                show homura naked with dissolve

                homura "Did I give you a good show? But... It felt lonely..."

                $ NPC_homura.love += 0.25

            "I want a blowjob":
                call homura_bj(False) from _call_homura_bj_1

                scene black with fade
                show expression brothel.master_bedroom.get_pic() at top
                with dissolve

                show homura naked with dissolve

                homura "Well, someone looks like he enjoyed himself... But what about me?"

                $ NPC_homura.love += 0.25

            "Let's do 69" if NPC_homura.flags["H level"] >= 2:
                call homura_69(False) from _call_homura_69_1

                scene black with fade
                show bg homura_rest1 at top with dissolve

                homura "Wow... Was it as good for you as it was for me?"

                $ NPC_homura.love += 0.5

            "Let's have sex (missionary)":
                call homura_sex(False) from _call_homura_sex

                scene black with fade
                show bg homura_rest1 at top with dissolve

                homura "It's always good when you're inside me..."

                $ NPC_homura.love += 0.5

            "Let's have sex (cowgirl)" if NPC_homura.flags["H level"] >= 3:
                call homura_cowgirl(False) from _call_homura_cowgirl_1

                scene black with fade
                show bg homura_rest1 at top with dissolve

                homura "I like being on top, it's an intoxicating feeling..."

                $ NPC_homura.love += 0.5

            "Let's go outside" if NPC_homura.flags["H level"] >= 4:
                call homura_river(False) from _call_homura_river_1

                show bg forest at top with fade
                show homura naked with dissolve

                homura naked "Wow, having sex outside is so much fun... It always feels as if someone could catch us at any moment. [emo_heart]"

                $ NPC_homura.love += 0.5

            "Let me do your ass" if NPC_homura.flags["H level"] >= 4:

                if NPC_homura.flags["H level"] == 4:
                    "You lean down and whisper in her ear. She blushes bright red."

                    homura "Oh!"

                    homura "You want to... Erm..."

                    you "So?"

                    "Homura remains silent, but she takes your hand. You lead her slowly towards the bedroom."

                    call homura_anal() from _call_homura_anal_1

                    $ NPC_homura.flags["H level"] += 1
                    $ NPC_homura.love += 1

                else:
                    call homura_anal(False) from _call_homura_anal

                scene black with fade

                if NPC_homura.love > 10:
                    show bg homura_rest4 at top with dissolve

                    play sound s_mmmh
                    homura naked "That was rough... But I loved it. [emo_heart]"
                    $ NPC_homura.love += 0.5
                elif NPC_homura.love <= 5:
                    show bg homura_rest3 at top with dissolve

                    homura naked "Oh, that was too rough..."
                    $ NPC_homura.love -= 1

            "Nothing":
                you "Sorry, I changed my mind."

                play sound s_surprise
                homura surprise "Whaaat? Aw, are you toying with my feelings? *frown*"

                $ NPC_homura.love -= 0.5

                return

    return

label homura_69(first=True):

    scene black with fade

    if first:
        show bg homura_naked1 at top with dissolve

        homura naked "So... What should we do now..."

        you " Let's see. Last time you made me feel good with your mouth... Can you do it again?"

        show bg homura_naked2 at top with dissolve
        play sound s_surprise

        homura "B-But... I want to enjoy myself too!"

        you "Okay then, I know what to do..."

    show bg homura_69_1 at top with dissolve

    play sound s_sucking

    homura "Mmh, nggh, hmmm..."

    you "That's it, work it nicely..."

    homura "Like thish? Hmmm..."

    "She looks very concetrated as she licks your shaft up and down, squeezing the base with her small hand."

    "Spreading her pussy lips open with your fingers, you can see she is already moist."

    you "Does this turn you on?"

    homura "Shhh... Shtop it... You know it does... Mmmh... *lick*"

    "She gently cups your balls in her hand, licking them."

    you "Your technique is improving fast... Hmmm..."

    homura "I am a fasht learner... *kiss*"

    you "I can see that... Hmm."

    "After teasing her with your fingers, you bring your face very close to her slit, breathing hard."

    show bg homura_69_2 at top with dissolve

    homura "Oh, I can feel... Oh..."

    "Juice is already running out of her pussy when you put your tongue to work. She gasps as you push it inside her."

    homura "Oh! Aaaah!!! [emo_heart]"

    "Your dick is getting slippery with her saliva as she increases her pace. At the same time, you lick her clit and pussy lips, careful to keep her on the edge."

    homura "This is too good, oh, ohh..."

    "She furiously grinds her pussy in your face, losing all self-control. You respond by burying your tongue deep inside her, still rubbing her clit with your fingers."

    homura "I'm... I'm..."

    show bg homura_69_3 at top with flash

    homura "Cummmiiiing!!!"

    with doubleflash

    play sound s_orgasm_young

    homura "AAAH, AAAAH!!!"

    show bg homura_69_4 at top with flash

    "She trembles with pleasure as an orgasm wave rocks her. Her wet juice is covering your face, dripping on your chin."

    you "Hmmm..."

    homura "Oooh... That was so good... Let me return the favor."

    show bg homura_69_5 at top with dissolve

    play sound s_sucking

    "In spite of the situation, Homura doesn't miss a beat. She immediately takes your cock deep in her mouth."

    homura "Nggh, Ngh..."

    "You find yourself moving your hips in sync with her blowjob, hitting the sides of her mouth. She sucks hard on your shaft."

    homura "Ngggh... Hmmm..."

    "Not really thinking straight, you find yourself licking the juice from her gaping pussy again."

    "Her clit is very sensitive now, so you take care to tease it softly. She still reacts with moans of pleasure."

    play sound s_moans_quiet

    homura "Ohhh... Hmmm..."

    "Determined to make you cum, she goes faster and faster, taking your cock deeper inside her mouth."

    "Feeling close to your limit, you lose all control, sucking on her clit as you finger her, rubbing the inner walls of her pussy."

    homura "S-Shtop, if you do that..."

    show bg homura_69_4 at top with dissolve

    homura "AAAAAH!!!!" with vpunch

    show bg homura_69_6 at top with doubleflash

    "Your cock pops out of her mouth and she cums again, trembling, as you let it all out on her face."

    "*spurt* *spurt*" with flash

    "She squeezes your cock in her small hand without thinking, making you cum every last drop on her erotic face."

    "Her love juice is all over your face."

    homura "So intense... Ahhh..."

    if first:
        scene black with fade
        show expression brothel.master_bedroom.get_pic() at top
        with dissolve

        show homura naked with dissolve

        homura "So this is what a '69' is, uh? That was so fun..."

        you "Is it your first time doing this?"

        "She blushes."

        homura "S-Sure... I have experience, but not that much..."

        homura "I like this, though. Let's do it again some time."

        you "Of course... And there are many more things I could show you!"

        homura "Oh..."

        $ MC.change_prestige(3)

    return

label homura_cowgirl(first=True):

    scene black with fade

    if first:
        show bg homura_naked1 at top with dissolve

        homura naked "So... Are we going to have sex?"

        you "Of course... If you want to."

        homura "I do! But this time... I'll be on top!"

    "Homura pushes you back with surprising strength, and straddles across you."

    show bg homura_cowgirl1 at top with dissolve

    homura naked "Now, where is my big boy... Oh!"

    "Guiding your cock to the entrance of her slit with one hand, she puts your hands on her breasts with the other."

    homura "Here. Touch me!"

    "You start rubbing her nipples and gently cupping her tits."

    homura "Play with them harder! Don't hold back!"

    you "You're so forward today..."

    homura "Shut up... And get to it! *blush*"

    with vpunch

    play sound s_moans_quiet

    "Obeying her command, you knead her tits harder while she lowers herself on your cock."

    homura "Oh! It's so deep... It hurts..."

    you "Slow down..."

    homura "It's... Aw... Fine..."

    "Your cock slowly finds its way inside her tight pussy, and you briefly pause to let her adjust to the feeling."

    you "You okay?"

    homura "S-Sure. You can move now..."

    "Sure enough, as you start carefully moving your hips, you feel the wetness of her love juice begin to ease your cock in and out."

    homura "Hmmm..."

    "Homura closes her eyes and concentrates on the feeling of your cock inside her, and your hands playing with her tits and nipples."

    homura "Oooh..."

    "Unconsciously, she starts to move her hips in sync with yours. Soon, your dick is making sloppy noises as it repeatedly slides in and out of her pussy."

    "Turning your attention to her boobs, you again notice how well-shaped they are for such a petite girl. She hasn't got an ounce of fat on her, but her breasts are really something."

    homura "W-What are you looking at?"

    you "Your tits. They're just the right size for my hands... I love them."

    "You give her a good squeeze as you say that."

    show bg homura_cowgirl2 at top with dissolve

    homura "Haaa!!!"

    "Visibly turned on, she increases the pace of her hip movements furiously."

    "You lay back and let her do most of the work, enjoying the view, and the feeling of her pussy gripping you tighter and tighter."

    homura "It's going deep... Deep..."

    "You can feel your cock hitting her womb every time it slams deep inside. Her love juice is splashing on your crotch now."

    homura "I'm... I'm close..."

    you "Me too... Ohh..."

    if calendar.day > 18:
        homura "Today is a safe day... Let it all in!"

    else:
        homura "Today is dangerous... Please do it outside..."

    "As she says that, she grips you even tighter, driving you crazy. You feel the surge as you bounce her up one more time."

    menu:
        you "OHHH..."

        "Cum inside":
            with flash

            homura "Aaaah!!!"

            show bg homura_cowgirl3 at top with dissolve

            "*spurt* *spurt*"

            "You cum hard inside her, filling her pussy to the brim with warm semen."

            if calendar.day <= 18:
                homura "You stupid idiot! I told you today wasn't a safe day!!!"
                $ NPC_homura.love -= 2

                "She's really mad."

                homura "And now I'll have to get herbs from the alchemist, and feel sick for two days... Ugh!"

            else:
                homura "I can feel it! Aaaah! Aaah!!!"

                with flash

                "You feel the walls of her pussy pulsating around you as she has an orgasm of her own."

                homura "I came... Ohh..."

        "Cum outside":
            with flash

            you "Uhhhh!!!"

            show bg homura_cowgirl4 at top with dissolve

            "Taking your cock out just in time, you bust your load all over her white belly."

            homura "Oh my... Look at this... It's all over my breasts..."

            with flash

            "You look at her body appreciatively, dripping with your sticky cum."

            if calendar.day > 18:
                homura "I told you to cum inside, though... Why didn't you?"

                "She looks cross with you."

                $ NPC_homura.love -= 0.5

            else:
                homura "You came outside, like I said. You're a good boy... Hmmm..."

                "She kisses you deeply."

    if first:
        $ MC.change_prestige(3)

    return

label homura_river(first=True):

    scene black with fade

    play music m_nature fadein 3.0

    if first:
        show bg clearing at top with dissolve

        show homura with dissolve

        homura "Aaah... The forest. I love it here..."

        you "Aren't we straying too far from the city?"

        homura "Don't be silly. I come here all the time. I know these woods like the back of my hand."

        you "That's strange for a noble girl. I thought your father was keeping you locked up?"

        homura "He only {i}tries{/i} to keep me locked up. And you've seen how successful he is."

        homura "I've always liked walking in nature. I've got fond memories of these woods. I even..."

        play sound s_sigh

        homura "*sigh*"

        you "What was that?"

        homura "Oh, nothing. Come, there's something I want to show you."

        you "..."

    scene black with fade

    show bg farm outside at top with dissolve

    if first:

        homura "Look! Pretty, isn't it?"

        menu:
            extend ""

            "Amazing":
                you "Wonderful! This place feels out of time..."

                homura "Right? I come here every chance I get."

                homura "I'm happy I get to share it with someone, for once..."

                $ NPC_homura.love += 1

            "It's alright":
                you "Yeah, it's fine, I guess."

                homura surprise "You guess? Come on! It's great, admit it!"

            "I've seen better":
                you "Well, it's nothing compared to this waterfall in the Arik Mountains. I hear it falls from a mile high..."

                homura sad "Aw, do you have to spoil this moment? I took you here for us to be together..."

                $ NPC_homura.love -= 1

        you "It's nice. Homura, we..."

        play sound s_dress

        you "Homura?"

    play sound s_splash
    with vpunch

    homura naked "Woohoo!!!"

    show bg homura_water1 at top with dissolve

    if first:

        homura "Aaaah, it's so good!"

        you "Homura... Really? There could be people around, you know... That farmhouse..."

        homura "Oh, don't be so prudish! I never saw anyone here. Come, join me!"

        you "Are you sure? I feel like we're being watched, and, err..."

        play sound s_laugh

        homura "You worry too much!"

    homura "Come, the water's good!"

    play sound s_dress

    show bg homura_water2 at top with dissolve

    "Taking off your clothes, you waddle in the water. It is not deep, and you feel a strange tingling sensation being naked in the open."

    if first:

        homura "Take that! Teeheehee!"

        play sound s_splash

        "Homura throws water at you like a child, and you answer in kind."

        play sound s_laugh

        "At some point, your assaults drive her right under the waterfall."

        play sound2 s_splash
        pause 0.2
        play sound s_surprise

        homura "Uwaaah!!!" with vpunch

    show bg homura_water3 at top with dissolve

    if first:

        homura "Look what you've done! Because of you, I'm all wet now..."

        you "Well... That wouldn't be a first."

        homura "Y-You silly... *blush*"

    "Watching her standing naked in the water, her skin glistening in the sun, you cannot help but get hard."

    "Homura also cannot help but notice. She motions for you to move closer."

    homura "Come on, give me a rub."

    if first:

        you "A rub... On your back?"

        homura "Yes, on my back, silly! I feel tense. I need to unwind."

        you "I don't know... Don't you think it's time to go?"

        show bg homura_water4 at top with dissolve

        homura "No it's not! Don't spoil the mood now, give me a massage!"

        you "Well..."

    "As she braces herself against a rock wall, you start massaging her shoulders, slowly moving down to her back."

    show bg homura_water1 at top with dissolve

    homura "Oh, that's the spot... More... Do it stronger..."

    "You keep massaging her back, helping relax her muscles."

    if first:

        you "You're awfully tense for someone who lives at court..."

        show bg homura_water2 at top with dissolve

        homura "Well, I do try to keep in shape... Plus climbing down my Dad's palace walls isn't exactly a picnic."

        you "I believe you, you've got the body of an athlete, and... Uh?" with hpunch

    show bg homura_water5 at top with dissolve

    "Homura bends over backwards, touching your cock with her buttcheeks."

    homura "My, look at that... It's hard as a rock, already."

    you "Well, massaging cute naked women does that to a man..."

    homura "Hmmm... I think I'm in the mood for more than a massage..."

    "She keeps brushing against your cock. You see some wetness on her slit that is definitely not water."

    "She holds her breath as you move behind her, bringing your cock up to the entrance of her pussy."

    homura "Do... Do me, [MC.name]..."

    show bg homura_water6 at top with dissolve

    play sound s_aah

    homura "Aaaah!" with hpunch

    "Pushing back against the wall, she makes your cock enter her tight pussy as you grab her from behind."

    homura "Oh, it's coming in!" with hpunch

    "She starts moaning erotically, moving her hips back and forth."

    play sound s_moans

    homura "I can feel you..."

    "You let her do the work for a while, as her pussy loosens and welcomes your dick deeper in."

    homura "C-Come on... Don't leave me hanging..."

    homura "Aaaah! [emo_heart]" with hpunch

    "Deciding to join in the fun, you start responding by slamming your cock inside with every thrust. You both start getting into a rhythm."

    show bg homura_water7 at top with dissolve

    homura "Oh yes... Aaaah!" with hpunch

    "Her love juices are flowing now, and she forgets herself as she moves to impale herself on your hard cock."

    homura "Oh yes! F-Fuck me harder!" with hpunch

    you "What did you just say? My, is this really Lady Henso I am speaking to?"

    homura "S-Shut up... Aaaah!!! [emo_heart]" with hpunch

    you "You know, we are out here in the open, where anyone could see us, fucking like wild animals in the river..."

    "Your words only seem to turn her on, and you can feel her body tensing up as she pushes against you with her strong thighs."

    homura "Oh... Aaah... Aaaah..." with hpunch

    "Her pussy walls close in on you, squeezing your dick hard as you hit the entrance of her womb."

    homura "I'm... Ohhh... I'm..." with hpunch

    play sound s_scream
    show bg homura_water8 at top with flash

    homura "CUMIIIIIING!!!!" with hpunch

    play sound s_orgasm_young
    with doubleflash

    "You both cum hard under the waterfall."

    with flash

    "Your cum inside her, then spurt some out on her pretty white ass. Water from the waterfall washes a mix of cum and love juice down her thighs."

    homura "Aaaah... It was so good... My head is spinning..."

    "You give her a gentle rub from behind. You stay inside her for a moment, then she reluctantly lets you go."

    show bg homura_water5 at top with dissolve

    you "The sun is getting low. We have to get back now..."

    homura "Aw... I was in the mood for more..."

    you "Next time..."

    if first:
        you "Uh?"

        "You could swear you saw something move in the bushes. Something... Colorful?"

        you "Hmm... Was that pink hair?"

        $ MC.change_prestige(3)

    return

label homura_anal(first=True):

    scene black with fade

    if first:
        show bg homura_naked1 at top with dissolve

        homura naked "So... How do we do this? *nervous*"

        you "Relax... We're going to take it slow."

        homura "I don't... Normally do this kind of things, you know..."

        you "What do you mean? I can remember doing a lot of kinky stuff with you."

        show bg homura_naked2 at top with dissolve

        play sound s_surprise
        homura "S-Stop it! You know what I mean. I don't normally do... What we're about to do."

        you "Are you saying this is your first time?"

        show bg homura_naked3 at top with dissolve

        homura "I'm saying... Yes. Yes, this is my first time."

        you "Wow... I'm a lucky man, then."

        homura "I don't know about that..."

        you "Come here."

        "You move over on the bed and kiss her. She closes her eyes..."

        scene black with fade

    show bg homura_anal1 at top with dissolve # ask msg (x+a) 1p/sham

    if first:
        homura naked "What... What are you doing?"

    "As you spread her legs open, Homura almost goes in a panic."

    homura naked "Aaaah..."

    "She is already visibly wet, though. You can tell whe was waiting in anticipation for what comes next."

    you "Rushing into it won't do. Let me help ease you up a little."

    play sound s_sucking

    "Going down between her thighs, you start licking her clit, her pussy lips, all the way down to her asshole. She moans uncontrollably."

    homura "Oh nooooo... What are you doing to me..."

    you "Well, you seem to like it... *lick*"

    "Her love juices are running thick, now, and she shivers under your tongue."

    "She gasps as you introduce a finger inside her ass."

    play sound s_surprise

    homura "Aaah!!! Don't..."

    you "Just relax, dear. If you can't take a finger, you won't be able to handle what comes next."

    play sound s_moans_quiet

    "She clenches her teeth and endures, as you start massaging her asshole from the inside."

    "While pushing your tongue inside her wet slit to tease her, you eagerly suck on her erect clit."

    homura "What's this... I've never felt like this... Ohhhh..."

    you "Is this too much for you already?"

    if first:
        homura "No, but..."

        "She looks at you with intensity."

        homura "[MC.name]... Fuck me please."

        you "Now? I don't think you are ready..."

        homura "My pussy. Now!!!" with vpunch

        show bg homura_anal2 at top with dissolve # ask msg (x+a) 1x

        "Not daring to disobey, you move your cock between her legs, easily slipping it inside her wet, gaping pussy."

        homura "Oh yes!!! Oh..."

        "Your warm-up technique has really put her in the mood, and she welcomes you deeper inside her as she lifts her hips to give you a better angle."

        homura "It's so good... I feel dizzy..."

        you "You like it?"

        homura "Yes... Do it, harder!" with vpunch

        "There is nothing lady-like about the horny girl before you, begging you for a good fuck. This puts you in a playful mood."

        you "My my, dear honorable Lady Henso, are you saying you want me to fuck you like a slut?" with vpunch

        "She seems turned on by the dirty talk."

        homura "I'm a bad... I'm a bad bitch... I need to be punished for my sins..." with vpunch

        you "Very well..."

        "With that angle, it's very easy to pile down on her and drive your cock all the way in."

        homura "Oh, aah, AAAH!!!" with vpunch

        "She moans and gasps as you pound her mercilessly."

        you "You like this, Homura? Do you like to be fucked like a vulgar streetgirl?"

        homura "That's... All... I deserve... Fuck me harder! Fill me up with dirty cum!" with vpunch

        "This little game is a big turn-on for the both of you, and you quickly reach your limits."

        you "I can't hold it any longer..." with vpunch

        homura "Me neither... I'm... I'm..."

        show bg homura_anal3 at top with flash # ask msg (x+a) 1cin/cob(on nos)

        you "UWAH!" with vpunch

        play sound s_orgasm_fast
        with doubleflash

        homura "CUMIIIIIING!!!"

        with flash

        "You shoot a massive load of cum all over her body, and she reaches orgasm at exactly the same time."

        homura "Oh... I came like crazy..."

        you "Me too..."

        homura "I'm all sticky... You even got some on my face!"

        "You both start laughing."

        with fade

        homura "You're still hard..."

        you "You got me incredibly turned on... We are not finished."

        homura "Right... I made a promise..."

        "The nervousness is back in her voice, but her body is now a lot more relaxed."

        "Bringing your cock up to her asshole, you use a mix of cum and her own love juice to lubricate the entrance."

        homura "It's dirty..."

        you "It's not, don't worry..."

    else:
        homura "No... I can take it..."

        "Not missing a bit, you slip a second finger inside her asshole, having lubricated it with her love juice."

        homura "Aaaah..."

        "Her ass is more loose now than when you first fucked her, and she has learnt to relax her body. Soon, you are able to slip a third finger inside."

        homura "Oh, aaah, ah!"

        you "You are getting nicely wet... Does having fingers up your butt turn you on?"

        homura "S-Stop it... *blush*"

        "Her weak denying tells you all you need to know. Still licking her slit, you play with her ass from the inside."

        homura "E-Enough... I'm... I'm ready..."

        you "Great..."

        "Your cock has been rock-hard for a while. You bring it up to her ass."

        homura "I-It's big..."

        you "Yes, but don't worry... We already know it will fit."

    "Spitting in her crack, you use your cock to push some saliva inside her. Her asshole is becoming loose."

    you "Shall we?"

    play sound s_mmh
    homura "Hmmm... Yes..."

    show bg homura_anal4 at top with dissolve # ask msg (x+a) 1a

    play sound s_scream

    homura "AAAAH!" with vpunch

    if first:
        "Being fucked in the ass for the first time, she is very sensitive. You stop mid-way to give her a chance of recovery."

        you "Are you alright?"

        play sound s_ahaa

        homura "Aaah... I-I feel strange... But I can handle it..."

    "Your cock seems massively too big for her little asshole, but you slowly push it in."

    play sound s_moans

    homura "AH, AAAH, AHAAA!" with vpunch

    you "Try to relax. Your body will adjust in a moment."

    homura "Aaaah..."

    "She seems almost ready to faint, hiding her face as you start slowly fucking her ass. Still, she nods at you to continue."

    "You use one hand to rub her clit and pussy, getting more love juice down on your cock."

    play sound s_aah

    homura "Ah, aah!" with vpunch

    "The familiar stimulation of her lower regions helps drive Homura's attention away from the cock in her ass. She eases up a little."

    homura "Oh, hmmm..."

    if first:
        you "This will feel weird at first, but you will learn to love it in time."

        homura "..."

        homura "Teach me."

    "You bend forward to kiss her. You keep stimulating her body, and moving in and out of her asshole becomes easier."

    homura "Aah, Ohh, Ohhh!!!" with vpunch

    "Little by little, you increase your pace. Her asshole looks more and more dilated, but is adjusting nicely."

    homura "Oh... I'm making love with my butt... I can't believe I'm doing this..." with vpunch

    "It looks like she is geeting in the mood. She's now peeking at the place where both of your bodies connect."

    homura "I, aah... Can't believe... This huge thing is... In my butt..." with vpunch

    "You are moving at a good pace now, still rubbing and pinching her clit as you pound her butthole."

    play sound s_scream

    homura "Oh, ah, aah..." with vpunch

    "Concentrating on the feeling, she hugs you close. You can feel her body tensing up."

    homura "Ohh... Ohhh!" with vpunch

    if first:
        "Fucking her virgin ass and watching her cute reaction becomes too much for you. You can't help but reach your limit."

        you "OHH..."

    show bg homura_anal5 at top with flash # 1cin

    play sound s_screams

    homura "AAAH!!!" with vpunch

    with doubleflash

    "You mind goes blank as you shoot your load right into her asshole. She is surprised at the feeling of warm cum erupting inside her."

    with flash

    if first:

        play sound s_sexy_sigh
        homura "Oh no... Doing it in the butt... I'm so depraved..."

        you "Hmm... But didn't you enjoy it?"

        homura "I... I did... I was close to cuming again..."

        homura "I think it's true that I'm a dirty slut, I can't deny it."

        you "Who said that? I was only joking..."

        homura "It's not you, it's... Never mind."

        "She hugs you close, kissing your mouth passionately."

        $ MC.change_prestige(3)

    else:
        play sound s_orgasm_young
        homura "AAAAH!!!" with vpunch

        "She cums as soon as you unload, burying her fingers in your back."

        homura "I came... From my butt... Aaaah..."

        you "You did... I'm proud of you..."

        homura "Hahaha... Don't be..."

    return


## Narika story line ##

label c3_narika_MU_visit():

    $ renpy.block_rollback()

    play music m_magicu fadein 3.0

    scene black with fade
    show bg magicU at top with dissolve:
        yalign 0.0

    $ renpy.pause(0.25, hard=True)

    show bg magicU at top with dissolve:
        linear 1.25 yalign 1.0

    $ renpy.pause(1.25, hard=True)

    if story_flags["MU seen intro"]:
        show receptionist with dissolve

        "You returned to the Magic University to register as a student."

        call c3_narika_MU_pay_fee() from _call_c3_narika_MU_pay_fee
        return

    show sill with dissolve

    sill "Wow! So this is the Magic University, the highlight of the Magic Guild quarter, renowned around Xeros as a place of deep knowledge and wondrous experimentation!"

    sill "I'm so honored and excited to be here!"

    sill "Right, Master? Master?"

    you "Hmmm... Most of the students and faculty are chicks, and they're hot as fuck..."

    hide sill
    show bg magicU_students at top with dissolve

    "Professor" "So now that we've successfully neutralized the undead, let's dissect it to see how it works..."

    "Students" "Yay!!!"

    you "Hot chicks... *drool*"

    show bg magicU at top:
        yalign 1.0
    show sill
    with dissolve

    sill "Ew, necromancy? Are they even allowed to do that?!?"

    "Girl voice" "Of course. Our charter with the city is very clear that what happens at Magic University, stays at Magic University."

    show sill at right with move
    show receptionist at totheleft with dissolve

    you "Oh, really? And who are might you be?"

    receptionist "I'm the P.R. representative for Magic University."

    sill "P.R. representative? Never heard of that before. What does it entail?"

    play sound s_sigh

    receptionist "It means I have to deal with people from the outside... *sigh* Most mages can't be bothered handling the profane."

    receptionist "So I handle the reception of outsiders, register students, file complaints from their families... I even operate the gift shop."

    receptionist "And answer questions from busybodies, of course."

    sill sad "Oh..."

    receptionist "I was informed by the Dean that an agent of the Court was visiting, so I came to greet you."

    receptionist "It's.. What was it again? Ah, yes: Nice to meet you."

    "Her voice sounds completely indifferent. She doesn't sound at all like she means it."

    you "Who told you we worked for the Court? We're not here on any kind of official business... "

    receptionist "Official, unofficial, it's all the same to the Guild really."

    receptionist "Mages welcome the Crown's scrutiny. Provided it remains in line with our Charter, of course."

    receptionist "Now, I assume you have questions, so please ask them... So that you be on your way and tend to whatever important paperwork you have to fill in."

    you "How helpful..."

    label MU_questions_menu():

        menu:
            _("Tell me more about you"):
                you "So... You're the public face of the University, so to speak?"

                receptionist "Nothing that fancy. It's just that I am more of a people person than most mages."

                "She looks bored and unexpressive."

                you "(If you're the people person, I wonder what the others are like...)"

                receptionist "Also, it's a sad fact that I am quite hopeless at working spells. Can't even cast a minor fireball."

                receptionist "So our Dean, Masou-sama, figured I would be better suited to this task."

                you "Wait, didn't you say you were a mage?"

                receptionist "Oh, I am."

                sill "You're a trained mage but you don't know magic???" with vpunch

                receptionist "I {i}know{/i} magic, sort of, I mean I've read the textbooks... I'm just not good at wielding it."

                "She sighs deeply."

                receptionist "Look, if you must know, my father is a high Lord from the nearby country. He paid a hefty sum for me to study here."

                receptionist "As I'm not really fit for the mundane world, I've been content to stay here for the past five years. Eventually, I'll figure it out... Maybe."

                you "Five years and no progress? Why does the University even keep you?"

                "She looks puzzled by your question."

                receptionist "Why, my dad pays a hefty tuition, of course!"

                receptionist "Did you seriously think a prestigious institution like ours operated on merit?"

                sill "Unbelieveable..."

                you "So you got, err, promoted to handling strangers, is that it?"

                receptionist "Yeah. Like I said, it suits me. Studying for more than an hour at a time gives me headaches."

                receptionist "Most days no one shows up. Other times, just some rich parents trying to offload their useless kid."

                sill "(Is she speaking about herself?)"

                receptionist "I handle the families an application form to fill, cash their tuition fee, and then they leave quickly."

                receptionist "I wish most days were that easy..."

                "She looks at you two reproachfully."

                jump MU_questions_menu

            "Tell me about the university":

                you "I want to know more about the Magic University. What do you do here?"

                play sound s_sigh

                receptionist "*sigh*"

                receptionist "The Magic University, or MagicU as it is known, was created a little over 90 years ago by our current Dean, Masou-sama, who was at that time the top ranking graduate of Karkyr university."

                you "(Over 90 years ago, uh? That Dean's an old-timer.)"

                receptionist "The Dean proceeded to make MagicU one of the most elite institution in Xeros."

                receptionist "Our faculty is top tier, and our facilities are second to none. Our students can enjoy living here full-time with high-class amenities and focus on their training."

                receptionist "Here at MagicU, we strive to teach them all possible schools of magic at the highest level, even some of the more unorthodox topics such as necromancy, demonology, and card tricks."

                receptionist "We also encourage our graduates and faculty to advance the magic arts by engaging in cutting research. Sometimes the research {i}actually{/i} cuts. And bites. And claws."

                receptionist "In short, MagicU is the best place for a gentle-man or woman to learn magic in a comfortable and magic-friendly environment. We give even the elite schools in Karkyr a run for their mana."

                "During her whole pitch, her voice has remained as cold and bored as ever."

                receptionist "Would you like to know more? Perhaps I can interest you in a brochure, or some books about the history of our prestigious establishment?"

                you "Err, not really..."

                receptionist "*not listening* Here, let's me look for the right chronicle..."

                play sound s_spell
                show receptionist glasses with flash

                receptionist "Here, this one is an abridged version, just shy of 2,000 pages long."

                sill normal "Whoah! Your glasses just materialized out of thin air!" with vpunch

                receptionist "Of course. I am farsighted, so I need my glasses to read books..."

                sill "So you do know some magic, after all!"

                play sound s_sigh

                receptionist "*looking annoyed* I don't. It's the glasses that are magic."

                you "Magic glasses?"

                receptionist "Naturally. Among the fruits of our research, we have developed a large number of magical prosthetics, from the mundane such as these to the miraculous."

                sill "Really?"

                receptionist "Some of our magic artifacts can replace limbs, cure ailments and infirmities..."

                receptionist "And even prop up the impotent. But if you need help in that department, I'm afraid our most powerful items are under magical lock and key in the University's vault."

                you "N-No, I don't..."

                receptionist "Sure, sure. They all say that."

                play sound s_spell
                show receptionist with flash

                sill "(Magic glasses, hmm?)"

                jump MU_questions_menu

            "Why did you call me a Court agent?":

                receptionist "Look, I don't care what business you have with the Court, and which faction you're working for."

                receptionist "The Dean said you'd come, and you came, so this much was right."

                you "Did the Dean mention us specifically? You could have mistaken us with someone else..."

                $ desc = {"Warrior": "A big dullard with a large sword, battered armor and a vacant stare, displaying the grace and sense of a drunken troll.",
                            "Wizard": "A snooty know-it-all in a tattered robe adorned with rough patches and stains of questionable origin. You will struggle and fail not to roll your eyes at him when he speaks.",
                            "Trader": "A shifty scoundrel with the subtlety of a horny alley cat, more likely to break into drunken slumber than into a vault full of gold."
                            }[MC.playerclass]

                receptionist "No, she mentioned you precisely. '[desc]' He is followed by a pink-haired slave girl who smells of cleaning products."

                receptionist "That describes you, doesn't it?"

                you "It does not!"

                sill "It kind of does..."

                play sound s_punch

                sill sad "*OUCH*" with vpunch

                receptionist "Don't be naive. The Dean likes to keep informed of what goes on at Court, just like your people spy on our affairs."

                receptionist "The Charter doesn't prohibit that, as long as it remains within reason."

                receptionist "No doubt the Dean knows more about your mission, but I don't need to know."

                receptionist "Which is a good thing too, because Gods know I wouldn't care."

                jump MU_questions_menu

            "What is this charter you speak of?":

                receptionist "*sigh* You don't know that? Maybe it's true that you're not a Court agent after all..."

                receptionist "The Charter is the treaty that recognizes the Magic Guild's fealty to the Pharo dynasty, and thus covers MagicU as well."

                sill happy "I seem to recall there was some friction at the beginning of the King's reign..."

                receptionist "Not really. It's just that the Guild has lived through four different dynasties since it settled in Zan, and one Republic."

                receptionist "The Pharo dynasty began on shaky ground, twenty-five years ago."

                receptionist "So the mages withheld their approval of the new king until a satisfactory deal was reached."

                receptionist "Some at Court are still bitter about this, but if you ask me, they're fools."

                you "For the record, I didn't ask."

                sill "What does the Charter say?"

                receptionist "Well, it gives us perpetual lease on this part of the city, not just the University grounds but the whole Magic Guild's district."

                receptionist "We can arrange our own affairs, and the Crown can only intervene if we request it. Their troops and agents like yourselves are barred from entering Guild and University buildings without invitation. We also do not pay royal taxes."

                you "I can see why that would rub some folks at the Palace the wrong way."

                receptionist "Some think the King got a raw deal. But he was able to consolidate his power in the end, so all is well that ends well, right?"

                receptionist "The problem is more with the personal animosity the King has developed for magic users."

                you "Personal?"

                receptionist "Yup. That the King actively hates mages is famous all over Zan."

                receptionist "Only a few magic-users are allowed at Court, such as the Astronomer Lord Henso, and they have cut ties with our Guild a long time ago."

                sill sad "Has somebody in the Guild wronged King Pharo in any way?"

                receptionist "I suppose this has to do with one assassination plot or another. Or the Dean's refusal to participate in the war effort. Meaningless politics. *shrug*"

                receptionist "If you ask me, a King should have thicker skin than that, and not get upset over some petty squabble."

                you "Again, I didn't ask..."

                receptionist "Anyway, we're quite content with the King avoiding us if it means we stay out of each other's business."

                receptionist "As the Charter would have us."

                jump MU_questions_menu

            "Tell me about the students":
                you "So you said you handle student registration?"

                receptionist "Unfortunately, I do."

                sill "You must have lots of students from the nobility within your ranks."

                receptionist "Of course. Our students only come from the elite layers of society, as they should."

                you "Even from within the Royal family?"

                "She gives you a strange look."

                receptionist "Of course not, why do you even ask?"

                you "Uh? Why not?"

                receptionist "Because King Pharo forbids it, of course."

                sill "He does?"

                receptionist "Yes. Some grudge he has against mages, in spite of the Charter we signed twenty-five years ago."

                you "Anyway, do you know a girl student that fits this description?"

                receptionist "I like to think I'm able to forget someone's face as soon as they leave the registration office. It is a skill I have refined over many years."

                sill sad "(Is this really a skill, though?)"

                "You proceed to describe Narika in as much detail as possible."

                receptionist "A spolied, whiny kid? That describes {i}all of the students{/i} we get at the University."

                you "But do you remember her?"

                receptionist "I don't. Just like I hope I'll have forgotten all about you by the time you step out of here."

                you "Wow, you really have a way with people. I can see why they made you the P.R. representative..."

                receptionist "Thanks."

                "She doesn't even seem to register your sarcasm."

                jump MU_questions_menu

            "Tell me about the Dean":
                you "So your Dean sounds like an interesting character..."

                receptionist "Sure thing. Masou-sama is over a century old, and has lead the Guild and the University for nearly as long."

                receptionist "She was a prodigy, a once-in-a-generation phenomenon. Graduated Karkyr at only fifteen."

                you "So the Dean is a 'she'?"

                receptionist "Sure. But don't get any ideas. She's many planes of existence out of your league, and anyway, she's celibate. Her only interest is devoting herself to magic."

                you "Haha, you're deluded, I'm not going to fall for some old crone. Not my kink."

                sill "What does Masou-sama do, exactly?"

                receptionist "Well, on the one hand, she's the Dean here so she keeps the faculty and researchers under control, which is no small thing. I don't think there's a higher concentration of inflated egos anywhere else in Xeros."

                receptionist "On the other hand, as she is also the Guild's Grandmaster, she has to handle a whole lot of politics. I understand she loathes that, but someone has to do it."

                receptionist "She has precious little time for anything else, including her magical research. This is in spite of using several alternate timelines to multiply her output."

                you "Can we meet her?"

                receptionist "Oh, sure. Did you miss the part where I said her time is precious and shouldn't be wasted?"

                you "It is important. We come with an urgent warning."

                receptionist "What's so urgent that you must disturb..."

                receptionist "Oh, blast, it's not like I'm paid, well, anything to stop you, so go right ahead."

                receptionist "She's better at dealing with your type than I am, anyway."

                you "'My' type?"

                sill "(Come Master, let's not waste this chance to talk to the Dean...)"

                play sound s_thunder

                with flash

                "The receptionist fumbles with something inside her pouch and a shimering blue portal fizzles into existence next to you."

                receptionist "Here you go. I'll see you on your way out."

                receptionist "(Shouldn't be long...)"

                call c3_narika_dean_visit from _call_c3_narika_dean_visit

                show bg magicU at top with flash:
                    yalign 1.0

                show receptionist with dissolve

                receptionist "So you're back. Yay."

                receptionist "That was an exceptionally long interview. The Dean must like you."

                you "Yeah, not really."

                receptionist "Oh? Well, don't worry about it. She doesn't like anybody."

                receptionist "What did she say?"

                "She's asking out of boredom rather than genuine interest."

                sill "Well, she told us that we shouldn't ever..."

                you "*interrupting* That we shouldn't ever worry about a thing!"

                you "She said we're welcome to investigate at our leisure. She'll cover for us by giving you fake instructions, because our mission is so secret than you can't know about it, you see."

                receptionist "..."

                "She stares at you blankly for a few seconds."

                receptionist "Fine, what do I care."

                you "So, can we visit the University now?"

                receptionist "Absolutely not."

                you "Whaaaat?" with vpunch

                receptionist "Only students and faculty are allowed on school grounds. Certainly not Crown agents."

                you "I assure you, I am not a Crown agent."

                receptionist "Maybe, but you're not a student either."

                you "Can I register to be a student, then?"

                receptionist "No! I mean, you..."

                "She struggles to find a reason to deny your request for some time. You can see from the deep frown on her face that she isn't coming up with anything."

                receptionist "Do you even have any magical affinity?"

                if MC.playerclass == "Wizard" or MC.spirit >= 5:

                    if MC.playerclass == "Wizard":

                        you "Of course! I'm a trained wizard. I'm far above your puny level."

                        receptionist "You don't have to rub it in my face..."

                    else:
                        you "Well, I'm no wizard, but I trained quite a few spells in my days. I'm able to handle the entry class, at least."

                        receptionist "Ok, fine, I guess I can register you for "

                    receptionist "Fine, I can register you for a class, but you need to pay the tuition."

                    you "And how much is that?"

                    receptionist "Oh, the usual rate is 10,000 denars per year. But since you're from outside of the Upper City, that would be 15,000."

                    you "WHAAAAT??? That's crazy!" with vpunch

                    receptionist "Hmph, as I thought, you don't have the means to study here..."

                    you "I don't need a year of classes anyway... Don't you have anything... Cheaper?"

                    receptionist "Well, I guess I can sign you up for a seven-day trial."

                    you "How much is that?"

                    $ price = story_flags["magicU price"] = 750

                    receptionist "That would be [price] gold."

                else:

                    you "Well, not really, but..."

                    "She looks relieved."

                    receptionist "Here you are, then! You can't get in."

                    you "Wait a moment... You don't have any magical ability either!"

                    receptionist "I do! Sort of..."

                    you "Your dad just paid your way in, didn't he?"

                    receptionist "Hmph, yes, but I don't suppose you have his kind of wealth..."

                    you "Come one, we can make a deal. I just need access to the University for a short time."

                    receptionist "Well..."

                    you "I'll pay cash, of course. Directly to you. No need for any paperwork..."

                    receptionist "You're going to get me in trouble..."

                    receptionist "..."

                    receptionist "Fine, 1,500 denars, and you get access to the University for a week."

                    you "1,500 denars? That's steep!"

                    call challenge("bluff", 4) from _call_challenge_67

                    if _return:
                        receptionist "Hmph, fine, 1,000 denars then. But it's final."

                        $ price = story_flags["magicU price"] = 1000

                    else:
                        receptionist "Take it or leave it, pinchpenny."

                        $ price = story_flags["magicU price"] = 1500

                you "[price] gold for two weeks, uh..."

                call c3_narika_MU_pay_fee() from _call_c3_narika_MU_pay_fee_1

                $ story_flags["MU seen intro"] = True

    return

label c3_narika_MU_pay_fee():

    $ price = story_flags["magicU price"]

    receptionist "[price] gold, and you get in for seven class days. What do you say?"

    if MC.gold < price:
        you "I don't have the money right now."

        receptionist "Yeah, I didn't think you did."

    else:

        menu:
            _("Yes"):                $ MC.change_gold(-price)
                $ NPC_narika.flags["c3 path"] = "MagicU"
                $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_narika)] = True
                $ renpy.block_rollback()

                you "Fine, here you are."

                "The girl swiftly grabs the pouch of gold, conspicuously hiding it in her bosom rather than stowing it in the registration desk."

                call receive_item(MU_entry_scroll, use_article=False) from _call_receive_item_15

                receptionist "Good, I'll give you a registration scroll valid for a week."

                receptionist "The school is open every day, so you can start coming tomorrow."

                you "The scroll doesn't mention my name... It's for one 'Lord Fakelot McFakeface'?"

                receptionist "Is it now? Well, think of it as insurance, in case the Dean looks at the student record."

                receptionist "If she found out I let you in, you might get caught, and {i}I{/i} may get in trouble."

                receptionist "I don't care about you turning into a slug, but I don't want to be yelled at."

                scene black with fade

                "You will attend school every weekday for the next week."

                $ story_flags["MU class days"] = 0
                $ story_add_event("c3_narika_MU_class", "daily")
                $ game.set_task("The Void Kunoichi: Attend class for a week at MagicU", "story3", 3)
                return

            "No":
                you "I still need to think it over."

                receptionist "Oh, fine, just waste more of my time then."

    scene black with fade

    "Talk to {b}suzume{/b} to go back to the University once you have the funds."

    return

label c3_narika_dean_visit():

    play sound s_mystery
    scene black with fade
    scene bg magic_office with doubleflash

    "You step into the portal and suddenly find yourself inside a fancy office, filled with various old tomes and magical oddities."

    you "So, this is the Dean's office..."

    show shizuka with dissolve

    shizuka "Yes? What is it?"

    you "(Oh, good, her assistant.)"

    you "Hello there young lady. Could you fetch your mistress please? I have urgent business with her."

    shizuka "Uh? My mistress?"

    you "Sure, sure, now go, shoo. Bring me the old lady."

    sill sad "Master..."

    you "Stop interrupting, Sill."

    "The young woman doesn't move, looking at you, amused."

    you "Gee, still here? Come one, I haven't got all day! Go tell the Dean I'm here!"

    sill "But Master..."

    you "What is it with the help these days? Shut up, Sill. You're in over your head."

    shizuka "Ahem."

    you "What?"

    shizuka "The Dean..."

    $ interject = {"Arios": "Arios", "Shalia": "Shalia", None: "Daemons"}[MC.god]

    you "Yes, go get her, isn't that what I asked for? ([interject], that assistant is cute, but not very bright...)"

    you "Or is that Dean so senile she can't even bring her old bones to the office anymore?"

    sill "Master! This woman! She {i}is{/i} the Dean!" with vpunch

    shizuka "*nods* I {i}am{/i} the Dean."

    you "You {i}are{/i} the Dean? Oh, very funny. Everyone knows the Dean is a decrepit crone who's over a century old."

    sill "Master, you're making it worse..."

    $ shizuka_name = "Dean Shizuka"

    shizuka "Your slave has more sense than you. You barge into my office and start calling out a lady about her age?"

    shizuka "I have half a mind to send you on a one-way trip to an Eldritch dimension right now."

    you "Wait, you're really the Dean?" with vpunch

    shizuka "Of course I am. I'm one of the Master Mages from Karkyr, and you think I couldn't overcome something as petty as aging?"

    you "Ah, err, hem, I'm sorry my lady, I didn't know... *mumble*"

    shizuka "So you're an idiot on top of being a sexual harasser. Charming."

    you "I'm sorry, what? A sexual harasser?"

    shizuka "Of course! Remember that time you tried to sneak naked into my room?"

    you "Uh? I never... Sill?"

    sill "Err, sorry Master, I don't know what she's talking about either..."

    shizuka "Wait, was that in the past, or in the future?"

    shizuka "I'm following too many different timelines at once, I might have gotten them confused."

    shizuka "Demons, there's just too much work these days. My mind wanders."

    you "..."

    shizuka "Yeah, yeah, we'll see how you handle things when you're my age. A decrepit crone, you said? Ha!"

    you "S-Sorry, we got off on the wrong foot here. I've come to warn you about imminent danger to your institution."

    shizuka "But of course. I am really {i}moved{/i} by the Court's concern for our safety."

    you "Look, I don't work for the Court... I mean I do, but, it's not the reason I'm here... I mean it is, but..."

    shizuka "He blabbers again... *sigh*"

    shizuka "Look, this is all terribly entertaining, I have never seen a Crown agent embarrass himself that much in so little time, but I have a thousand other things to do before the day is over."

    you "Wait! I don't think you realize the danger you're in. A trained assassin is after something valuable at the University, and they'll stop at nothing to get it."

    shizuka "Are they now? And what is this valuable thing they're after?"

    you "I... Have no idea, yet, but I was hoping..."

    play sound s_laugh

    shizuka "You {i}are{/i} clueless, aren't you?"

    shizuka "Look, we get attempted break-ins all the time, and our defensive measures are top-notch."

    shizuka "No one in their right mind wants to face our magical traps. I have a jar full of slugs in the back who used to be burglars."

    shizuka "They provide me with a source of slime, and the students with entertainment during study breaks, gambling on slug races."

    you "But listen. The attacker is a Kunoichi, a prodigy with natural resistance to magic. She could take on your defenses, I'm sure."

    shizuka "Hmph. I designed most of those traps myself, so I strongly doubt that."

    shizuka "Now, let me lay down the rules."

    shizuka "This meeting is over, and you are not to bother me ever again. I will give that airhead receptionist clearer instructions this time."

    shizuka "If I find out you are causing trouble at my quiet little private institution, you will soon join my slug collection."

    shizuka "Do I make myself clear?"

    you "Well yeah, but..."

    shizuka "Good."

    play sound s_spell
    scene black with flash

    "She snaps her fingers, and the room goes blank."

    return

label c3_narika_failed_summon():
    play sound s_scream_loud

    ev_girl2 "Nooooo!!!" with vpunch

    play sound s_tentacle
    show bg MU_monster2 at top with dissolve

    "Not content with fondling her, the monster pushes his pulsating red cock into her panties, burying the fabric in her pussy."

    ev_girl2 "Stop... I summoned thee... Thou shalt obey me..."

    play sound s_scream

    ev_girl2 "Aaaaah!" with vpunch

    play sound s_tentacle

    show bg MU_monster3 at top with dissolve

    "Ignoring her feeble attempts at regaining control, the demon pushes his cock harder and harder until her panties give way."

    "*RIP*" with vpunch

    "In an instant, the large demon cock fills her pussy, all the way to her womb."

    play sound s_screams

    ev_girl2 "No, no, let me go, aahaaah!" with vpunch

    "The girl screams, unable to take the feeling of the demon fucking her raw."

    play sound s_roar

    pause 0.3

    play sound2 s_tentacle

    "With a sickening gooey sound, the tentacles agglutinate into a monstrous shape, still probing at the poor girl's holes"

    ev_girl2 "Nooo-"

    show bg MU_monster4 at top with dissolve

    play sound s_mystery

    ev_girl2 "Hmmmh!!!" with vpunch

    play sound s_sucking

    "Shutting her up with another one of his tentacle cocks, the demon lets out an outworldly groan."

    ev_girl2 "Nggh... Ngh..." with vpunch

    "The beast is fucking her in rhythm, now, and she seems to have lost any will to fight back."

    ev_girl2 "Hmmh... Nggh!" with vpunch

    "Her body is like a broken doll, bouncing on demonic dicks with obscene wet sounds."

    play sound s_mmh

    ev_girl2 "Hmmmh..."

    "The demon's tentacles begin to swell, apparently gorging with unholy semen. It seems it is about to shoot its load inside the hapless girl."

    play sound s_roar

    "*GROAR*" with vpunch

    show bg MU_monster5 at top with flash

    "Suddenly, thick monstrous cum beetween to erupt at both ends of the demon' dicks, shooting inside her mouth and pussy."

    with doubleflash

    ev_girl2 "Ngh, nggh, ngggggggh!!!"

    show bg MU_monster6 at top with flash

    "The girl can't do anything but take it all in, almost losing her mind as her womb fills up with wad after wad of demonic cum."

    play sound s_evil_laugh

    "Beaming with an unholy glow, the demon seems to bask into the mess it's made."

    return

label c3_narika_MU_class():


    play music m_magicu fadein 3.0

    if not story_flags["MU class days"]:
        $ story_flags["MU class days"] = 0
    $ story_flags["MU class days"] += 1

    if debug_mode:
        $ story_flags["MU class days"] = int(renpy.input("Choose day number"))

    $ renpy.block_rollback()

    scene black with fade
    show bg magicU at top with dissolve:
        yalign 0.0

    $ renpy.pause(0.25, hard=True)

    show bg magicU at top:
        linear 1.25 yalign 1.0


    if story_flags["MU class days"] == 1: # Day 1 - Sill intro

        you "Finally here! Magic University, here I come!"

        "???" "Wait, wait! *pant*..."

        you "Uh? Who's this?"

        play sound s_steps
        show sill glasses at totheright with easeinright

        "???" "Oh... I finally caught up with you!"

        you "I'm sorry, your face looks kind of familiar, but... Have we met?"

        $ sill_name = "Familiar girl"

        sill "Master! It's me!"

        you "*squint*"

        you "*{b}squint harder{/b}*"

        sill "Master!"

        you "Sill! Is that you?"

        $ sill_name = "Sill"

        sill "Of course it's me! Gee, Master, is my disguise really so effective?"

        you "It's... Mesmerizing."

        sill "It's the glasses! Seeing that receptionist girl conjuring up her glasses yesterday made me think of this trick..."

        you "Really? Take them off just for a second?"

        sill "Okay..."

        show sill glasses:
            zoom 1.0
            yalign 1.0
            ease 0.5 zoom 1.75 yanchor 0.5

        pause 0.5

        play sound s_spell
        show sill happy with dissolve:
            zoom 1.0
            yalign 1.0

        sill "Like that?"

        you "Amazing. It's  like a completely different person."

        play sound2 s_spell
        show sill glasses with dissolve:
            zoom 1.75
            yanchor 0.5
            pause 0.5
            ease 0.5 zoom 1.0 yalign 1.0

        you "What about your registration scroll?"

        sill "I forged one from using yours. I simply had to cast..."

        you "Not interested, forget I asked."

        sill "Hehe, this way I can accompany you to class, Master [MC.name]!"

        sill "(Oh, my heart is beating fast! It's like we're two highschool sweethearts who just...)"

        you "Good idea, let's split up, we'll cover more ground that way."

        sill "B-But..."

        sill "(Oh no...)"

        sill "(Well, at least I will get to do something other than housework.)"

        you "Move it, Sill, we ain't got all day! Let's see, you can go there... Your next class is... 'Cleaning up magical equipment 101'."

        sill "Aargh..." with vpunch

        scene black with fade

        if MC.playerclass == "Wizard":
            you "Phew, I almost died of boredom in there... I had forgotten how much non-Euclydian geometry and linguistics of the Great old ones you need to cram before you can summon a simple eldritch hamster."

        else:
            you "I have a pain in my neck from nodding to the teacher even though I didn't understand a single word."

        you "More importantly, I didn't catch a single glimpse of our target... It's harder than I thought. This place is huge."

        show bg magicU at top with dissolve:
            yalign 1.0

        show sill glasses with dissolve

        sill glasses "Master! Finally, I am done... *pant*"

        sill "They made us clean up the whole magic lab, this wasn't really like a class at all... And I..."

        you "Nice, nice, good to know you were having fun, but what about that pesky ninja?"

        sill "I didn't see her anywhere..."

        you "[MC.swear()], we'll have to look harder tomorrow..."

        show bg magicU at top with dissolve:
            yalign 1.0
            matrixcolor SaturationMatrix(0.4)

        "A large shadow suddenly glides over you."

        show bg floating island at top with dissolve:
            matrixcolor None

        you "UWAAAAH!!! What the fuck is THAT???" with vpunch

        you "Sill! There's a, there's a..."

        sill "A floating island?"

        you "Yes!" with vpunch

        sill "Did you just notice it? It's been floating around ever since we came here."

        you "I was so focused on keeping my ear to the ground looking for Narika that I didn't even notice..."

        sill "They call it the Sky Isle, and it's been here in Zan forever. It seems to always hang high above the Magic University."

        sill "Although I heard it was already floating around long before they built the University. It seems to be attracted to places of power."

        you "What's up there?"

        sill "No one knows. Oddly, teleportation spells won't work on it and the terrible wind up there does not allow flying."

        sill "Some say it's a piece of the legendary Goliath Kingdom, ripped apart in the cataclysm that destroyed that land..."

        you "Yeah well, I'm sure it's just a big dumb piece of rock that happen to defy the laws of physics. Let's not get sidetracked and focus on the important stuff. Which is..."

        you "That I'm STARVING!!! It's almost dinner time, and you need to get to the kitchen fast!" with vpunch

        sill "Oww... *panic*"

    elif story_flags["MU class days"] == 2: # Day 2 - Sill H

        you "(Day Two of infiltrating the university...)"

        you "(I better get a lead on this girl ninja today, no time to screw around.)"

        show sill glasses at totheright with easeinright

        sill "Wait for meeee!!!"

        you "What, you're coming along today too?"

        sill "Of course! It's been my dream to go back to studying..."

        you "You're weird... No one likes studying. At least I didn't, so that means no one does, right?"

        sill "I'm so excited! After doing the chores yesterday I stayed up all night to study my old textbooks."

        sill "I need to dust off some of what I learned in the past, and..."

        scene black with flashbackout
        sill glasses "(...and see if I could still figure out how to cast that old enchant...)"

        show bg sill sold at sepia
        with flashbackin

        sill glasses "(...the one I used when I met Master [MC.name]...)"

        hide bg
        show bg sill sold
        with flashbackin

        sill past "Oh no, what's going to happen to me???"

        sill "My life is over... Father wants to sell me off to some stranger at the slavemarket..."

        sill "All these men are giving me dirty looks... They're old and disgusting... Everywhere I look, I just feel sick..."

        you "Hello Sir, is this horse for sale?"

        play sound s_surprise

        sill "!!!" with vpunch

        sill "(This man, talking to my father! He's...)"

        sill "(He's actually quite dashing!)"

        $ MC.rand_say(["wa: My old one got his head blown off by a trebuchet. Nasty business.", "tr: My old one got hurt playing with my pet dragon. Turns out horse hair is surprisingly flammable.", "wi: I lost my old one. Turns out you can't dry a horse using a microwave spell. Who would have thought?"])

        sill "(In fact... He's really handsome... Just looking at him gives me strange tingling sensations all over...)"

        you "May I look it in the mouth? Let's see..."

        sill "(If I'm going to be a slave to anyone, this man...)" with vpunch

        you "Oh, would you look at that! There's a girl next to the horse."

        sill "(He saw me!!!)"

        you "She's cute actually. Is she also for sale?"

        sill "(And he said I'm cute!!! [emo_heart])" with vpunch

        "Sill's father starts bartering with [MC.name]."

        sill "(Quick, Sill, get your act together!)"

        sill "(Find that enchantment! The one you were saving for your one true love...)"

        sill "(This enchantment will make anyone fall for me. It has to work... Arios, please!)"

        you "Ouch, man, that's steep. But you know what, throw in the girl and I'll take the horse. It's all the coin I've got, but she's my type. Here you go."

        play sound s_gold

        sill "(I can't believe it! He bought me! The enchantment worked!)"

        $ MC.rand_say(["gd: Hi there, cutie. Don't be afraid. I'm [MC.name].", "ne: Hello. I'm your new master. My name is [MC.name].", "ev: Get up, slave. You're mine now, and don't you forget it. The name's [MC.name]."])

        sill "H-Hello Master..."

        sill "Master [MC.name]..."

        scene black
        show bg magicU at top:
            yalign 1.0
        show sill glasses:
            xalign 0.5
            ypos 1.15
            yanchor 1.0
        with flashbackout

        play sound s_ahaa

        sill "Master [MC.name]... Aaah... [emo_heart]"

        you "Yes, that's my name... Why are you swooning like a fool?"

        sill "Oh, erm, sorry. How are you today, Master [MC.name]? *blush*"

        sill "(I was hard at work all night on these enchanted glasses...)"

        sill "(If I got the spell right, it should rekindle the flame between Master and me...)"

        you "What are you acting so strange?"

        sill "Have you noticed anything today, Master? Anything at all?"

        you "Nope."

        show sill glasses:
            ease 1.0 ypos 1.5 zoom 1.5 subpixel True

        "Sill gets closer."

        sill "But look! What about my glasses? Do you like them?"

        you "They're okay, I guess. Why are you acting all weird?"

        show sill glasses:
            ease 1.0 ypos 2.25 zoom 2.5 subpixel True

        "Sill gets even closer."

        sill "How about now? *blush*"

        you "*look*"

        you "*look intently*"

        show sill glasses:
            ease 1.0 ypos 1.5 zoom 1.5 subpixel True

        you "(Is it me, or is it getting hot all of a sudden?)"

        you "You know... You know what they say about girls in glasses, right?"

        sill "That they're... Really smart?"

        you "Nope."

        stop music fadeout 3.0

        scene black with fade
        show bg sill glasses1 with dissolve

        play music m_suzume fadein 3.0

        "Grabbing Sill's hand, you pull her into the bushes and swiftly pull her clothing out of the way."

        play sound s_mmh

        sill glasses "Oh, Master! [emo_heart]" with vpunch

        you "No underwear, uh? That's my Sill..."

        sill "(Whoah... Looks like my enchantment worked a little too well...)"

        show bg sill glasses2 with dissolve

        sill "Master! We're in public! What are you doing..."

        you "I know we're in public! That's why you're already wet, isn't it?"

        "You stick two fingers inside her pussy, and they immediately become sticky with thick juice."

        play sound s_aaah

        sill "Aaah!" with vpunch

        sill "But anyone could see us... The faculty... The students..."

        you "That's part of the fun!"

        "Pulling out your hard cock, you place it right between her pussy lips, enjoying her moistness on the tip or your manhood."

        show bg sill glasses3 with dissolve

        stop music fadeout 3.0
        play sound s_surprise

        sill "No, Master, wait!" with vpunch

        you "What? You don't want me to fuck you senseless?"

        sill "It's... It's not that..."

        sill "But I need to know... Are you doing this to me because of my glasses?"

        you "Uh? What are you rambling on about?"

        sill "It's my glasses that turn you on, isn't it?"

        sill "(It's just because of the enchantment...)"

        you "..."

        you "Nonsense."

        "You remove her glasses and fling them to the side."

        sill naked "Uh? M-Master?"

        you "Glasses are just an accessory, I don't care about that."

        sill naked "Really?"

        "She looks at you with big, shiny puppy eyes."

        you "Of course, your true beauty is inside..."

        play sound s_sigh

        sill "Aw... Master... It's so nice of you to say so... [emo_heart]"

        you "...inside that tight pussy of yours! Let's FUCK!" with vpunch

        play sound s_scream

        sill "Aaaah!!!" with vpunch

        scene black with fade

        sill naked "(Master likes me even without the enchantment... I'm glad... [emo_heart])"

        sill "Wait, Master, wait!" with vpunch

        you "What, again? Your constant interruptions are going to ruin the mood, Sill..."

        sill "No, Master, don't get me wrong."

        sill "I want to make love. But let me be on top."

        you "Uh? What's gotten into you today?"

        show bg sill glasses4 with dissolve

        sill "Come on Master! I want to ride your dick!" with vpunch

        you "Whoah, you're wild today!"

        sill "(Master will be in love with me, I'm sure... I'm going to show him a good time!)"

        "Sill starts grinding her lower body against you, coating your shaft with her juice."

        you "We're laying down in the middle of the alley... Anyone could come..."

        sill "Like you said, it's part of the fun!"

        show bg sill glasses5 with dissolve

        play sound s_ahaa

        sill "Ahaaaah..." with vpunch

        "Sill lowers herself onto your cock, sliding it deep into her drenched pussy."

        play sound s_moans

        sill "Oh Master, you're so thick! Oh!"

        play sound s_moans

        "Sill starts rocking her hips, massaging your dick between the tight folds of her pussy."

        "She shakes her boobs at you, enjoying your gaze."

        show bg sill glasses6 with dissolve

        sill "Do you like it, Master? Aaaah! [emo_heart]" with vpunch

        you "Oh, you're squeezing me... Sill, your technique's got better..."

        sill "The girls have been giving me tips! Look, how's this?"

        show bg sill glasses7 with dissolve

        play sound s_dodge

        sill "Banzai!" with vpunch

        "Squeezing you tighter between her thighs, she buries your cock deeper inside her, increasing the sensations even further."

        you "Whoah! Amazing!" with vpunch

        play sound s_mmh

        sill "See, Master? I've gotten good, haven't I? Hmmmh..."

        "She keeps bouncing off your dick faster and faster, almost popping it out on the way up, only to impale herself on it all the way down."

        play sound s_aah

        sill "Ooh... Aaaaah..." with vpunch

        you "I can't... Ooooh..."

        show bg sill glasses8 with dissolve

        sill "You're close, aren't you? I know your body like the back of my hand, you know..."

        sill "Let me make you cum, Master [MC.name]. Let your slave fuck your brains out today..."

        sill "Hmmm, ooh, aaaah..." with vpunch

        "Sill keeps upping the pace, squeezing your dick with all her strength."

        show bg sill glasses9 with dissolve

        play sound s_scream

        sill "Aaaah!" with vpunch

        sill "Oh my, I'm so close too! Fuck me, Master! Fuck my dirty pussy!"

        "*squeeze*"

        play sound s_ahaa

        sill "You hear that, Master [MC.name]?"

        "Your bodies make dirty wet noises as Sill's juice splash around your crotch. You feel your orgasm building up inexorably."

        sill "That is the sound of inevitability."

        play sound s_scream_loud

        sill "AAAAAH!!!" with vpunch

        show bg sill glasses10 with flash

        "Suddenly, it all becomes too much for you. As Sill descends on your dick one last time, you shoot a huge load of cum straight at her womb."

        play sound s_aaah

        sill "Oh, you're so deep, oooh..." with doubleflash

        play sound s_orgasm_fast

        sill "I'm, I'm... AAAAAAAH!!!"

        with flash

        "Sill cums hard too, her hips arching back as she convulses in orgasm with your cock deep inside her."

        sill "It's so warm inside, aaaah..."

        show bg sill glasses11 with fade

        sill "See, Master [MC.name]? You're not so tough, after all, aren't you?"

        sill "Maybe {i}I{/i} can call the shots from now on... You could be {i}my{/i} slave, doing my bidding..."

        sill "In exchange, I'll let you be my {i}slave boyfriend{/i}."

        sill "Don't worry, I'd still fuck you every day, and after that you'll give me a nice massage, make some tea, then do the chores for me... Hehehehe...."

        you "Sill..."

        play sound s_laugh

        sill "Ho ho ho ho, I can already see it! 'Yes, Mistress Sill', 'Of course Mister sill', 'What part of your body needs relief, Mistress Sill?'..."

        you "Sill."

        sill "And then you'd get on your knees, and..."

        you "SILL!!!" with vpunch

        show bg sill glasses12 with dissolve

        "Sill suddenly snaps out of her revery."

        sill "Oh, uh, ah, s-s-sorry Master!!!"

        you "Are you quite finished?"

        sill "*mumbles incoherent excuses*"

        menu:
            _("Humor her"):                $ MC.good += 1
                $ NPC_sill.love += 5

                "You soften your voice and smile."

                you "You know, perhaps we can do that one day. As {i}roleplaying{/i}."

                sill "R-Really? You'd do it? You're not... Mad at me, Master?"

                you "Mad at you? Of course not, we just had great sex. I like it when you're so forward."

                you "So maybe we'll do that again, eh? One day."

                sill "Oh, thank you, Master... [emo_heart]"

                you "But not anytime soon. First I need to recover from this."

                sill "O-Of course..."

            "Let it slide":
                $ MC.neutral += 1
                $ NPC_sill.love += 2

                "You roll your eyes."

                you "What nonsense was that?"

                sill "I-I'm sorry, I don't know what came over me, Master... It's that time of the month, maybe, and..."

                you  "Quit your babbling, Sill."

                you "I'll let your impertinence slide this once. After all, it's understandable in the heat of the moment."

                you "It {i}was{/i} a great fuck..."

                sill "T-Thank you, Master..."

                you "But don't let that get to your head, you hear? "

                sill "N-No, sorry Master. I'll be good."


            "Punish her":
                $ MC.evil += 1
                $ NPC_sill.love -= 2

                you "I don't think I heard you correctly. Did you call me... {i}Your slave{/i}?"

                sill "I-Im so sorry, Master... I was just..."

                you "[MC.swear()], you have the gall to tell me that, you impudent wench? I should have you flogged!"

                sill "No! Master [MC.name], nooo! I'm sorry, I'll never do it again!"

                you "I'll see to it that you will not! I'll give you double the chores this week, and you'll sleep on the kitchen floor!"

                sill "Aaw... I'm sorry, Master..."

        "Suddenly, you hear the laughs of a large group of students nearby."

        "You both become painfully self-conscious, lying naked and covered in bodily fluids in the middle of the alley."

        scene black with fade

        play sound s_dress

        "Hurryingly, you fix your clothes and head back towards the main building."

        play sound s_spell

        "As you walk back, you notice the time on the magic clock up on the main building's tower."

        sill glasses "Oh no! Classes are over already!"

        you "No way! We missed our chance to hunt the ninja because of your naughty shenanigans! *mad*"

        play sound s_punch

        sill "But, Master, it's you... Ouch!!!" with vpunch

        $ MC.change_prestige(3)

        "You didn't make any progress on the hunt for Narika today. Better luck tomorrow?"

    elif story_flags["MU class days"] == 3: # Day 3 - Narika glimpse

        you "Okay, today I locked Sill up in her room. No more interruptions, this time I'm going to find that pesky ninja!"

        you "Let's check a bunch of different classrooms. She's bound to be {i}somewhere{/i}."

        show black with fade

        "You spend the next hour poking your head into various classrooms."

        you "[MC.swear()], this place is so darn big... Wait, what's this one? 'Arcane items of Xeros: A long history.'"

        "You catch a whiff of sakura flower perfume as you peer into the classroom."

        scene black with fade
        show bg classroom at top with dissolve

        "Professor" "So, did you like the lecture, Miss?"

        show narika school with dissolve

        narika "Oh yes, Professor... You are {i}so{/i} interesting, you know... I come here every day just to hear {i}you{/i}..."

        "The girl bats her eyes exageratedly while the Professor basks in her adoration."

        "Professor" "It's so nice of you to say so, my child..."

        "The old teacher starts patting the girl on the lower back, inching his hand down to her skirt. She evades at the last moment in a swift elegant move, still managing to look natural."

        you "(This girl...)"

        narika "Professor [emo_heart], did you remember my request?"

        "Professor" "Child, it's not easy to sate your curiosity... I can't tell you such things, there are rules and the Dean would be very cross if she..."

        narika "Ow, Prof-chan, don't be a meanie... You do remember my promise, don't you?"

        "Professor" "You promised to... *gulp*"

        narika "Yes? *teasing*"

        "Professor" "To give me your used panties... If I..."

        narika "That's right! [emo_heart]"

        narika "But in exchange I just want you to share some knowledge... For my thesis... Pretty please?"

        "She bats her eyes so fast she almost gives the old guy a seizure."

        "Professor" "*sigh* All right, you're such a sweet girl, there's really no harm in that..."

        "Professor" "I know of the item you asked about. It's one fine piece of magic engineering, based on ancient Cimerian principles... They used mithril to..."

        narika "*growing impatient* Cut to the chase, old man, where is it?" with vpunch

        "The Professor stops, startled, Narika catches herself and immediately reverts to her schoolgirl act."

        narika "*in character* Pretty please, Prof-chan?"

        "Professor" "Well, uhm... It's here in the Dean's vault, the most secure place in the whole University. Building it was an early feat for the Dean and we keep it away from the public, as it is priceless."

        narika "Of course, of course... And this vault is completely unbreachable, isn't it?"

        "Professor" "Quite so! One would have to be a master at evading magical traps to even make it past the entrance to the vault, but then..."

        narika "Yes? *eager*"

        "Professor" "There's a final piece of security that no thief could ever work around..."

        narika "What is it?" with vpunch

        "Professor" "It is, er... *lowers his voice*"

        "You can't quite make out what the Professor is saying. Narika raises an eyebrow."

        narika "Really? I see..."

        "Professor" "So, that's all I know about it. Now, will you give me my... present?"

        narika "You know what, I have to go now, but I'll drop by next week and I'll give it to you for sure!"

        play sound s_steps
        hide narika with easeoutright

        "Professor" "Wait, young lady! I-"

        "Professor" "She's gone..."

        scene black with fade

        "You ponder what you just saw."

        you "She's definitely out to get a magical item from the Vault."

        you "It's not quite enough information to unravel her plan yet. I need to keep investigating."

    elif story_flags["MU class days"] == 4: # Day 4 - Monster H

        "You are back to Magic U. today, again touring the different classrooms looking for Narika."

        you "Day Four already. I only have one week. I need to make progress."

        "You hear some yelling coming from one of the halls."

        "Professor Emeritus" "Search again, damnit! It must be around somewhere! Masou will have my hide if she finds out I lost it!"

        "You catch a glimpse of half a dozen servants running around the vast and expensive lab, before one of them spots you and slams the door shut."

        "Intrigued, you keep exploring, when you suddenly hear something."

        play sound s_surprise
        ev_girl2 "Oh no! Help!" with vpunch

        "The cry comes from one of the student rooms."

        scene black with fade
        show bg MU_monster1 at top with dissolve

        play sound s_scream

        ev_girl2 "Aaaah!!!" with vpunch

        ev_girl2 "I completely messed up the magic formula... The Demon is not obeying any of my orders!"

        "You peek inside the room and see a student in the middle of a sticky situation."

        menu:
            "What do you do?"

            _("Help her"):                $ MC.good += 1

                # Challenge
                $ chal = renpy.call_screen("challenge_menu", challenges=[("Attack", "fight", selected_district.rank), ("Dispell", "control", selected_district.rank)])

                if chal == "fight":
                    $ norollback()

                    play sound s_sheath

                    "Unsheathing your weapon, you leap inside the room and starts hacking at the creature."

                elif chal == "control":
                    $ norollback()

                    "Stepping inside the room, you try to think fast and figure out the demon's type and weakness before it can fully take form in the material world."

                play sound s_scream_loud
                ev_girl2 "Eeek!!! Help me!" with vpunch

                call challenge(chal, 3) from _call_challenge_68 # result is stored in the _return variable
                $ r = _return

                if r:
                    if chal == "fight":
                        play sound s_sheath
                        pause 0.3
                        play sound2 s_sheath
                        with flash

                        "You slice off most of the monster's appendages."

                        play sound s_roar

                        "With a roar of pain, the demon withdraws and his body shines briefly before disappearing into thin air."

                    elif chal == "control":
                        you "POYE POLOMI!!!" with vpunch

                        play sound s_lightning
                        with flash
                        "Your fingers blast arcane lightning at the thing, searing his mind through the interdimensional veil. The creature withdraws in pain."

                        play sound s_roar

                    ev_girl2 "Oh, thank you so much!"

                    ev_girl2 "It's gone back to where it came from, it didn't have time to fully materialize!"

                    scene black with fade

                    "The girl is really grateful. She gives you something for your trouble."

                    $ MC.change_prestige(3)
                    call receive_item(item_dict["Lucky charm"]) from _call_receive_item_26

                else:
                    play sound s_roar

                    "The creature notices you, and a wrigling mass of tentacles spurts towards you."

                    "You fall back in disgust, trying to fence off the attacks as best as you can."

                    play sound s_punch

                    you "OUCH!!!" with vpunch

                    "Alas, you hit your head hard on a shelf, and a dozen large and heavy magic tomes rain down on you."

                    "You are knocked out; fortunately the beast is content with leaving you alone and focussing its attention back on the hapless girl."

                    call c3_narika_failed_summon() from _call_c3_narika_failed_summon

                    scene black with fade

                    "When you come back to your senses, the demon and the girl are nowhere to be seen."

                    "Defeated, you head back home, with your stamina spent and a nasty headache."

                    $ MC.interactions -= MC.interactions

            "Just watch":
                $ MC.evil += 1
                you "(I shouldn't get involved, but I'll keep an eye on it. You know, just in case...)"

                call c3_narika_failed_summon() from _call_c3_narika_failed_summon_1

                scene black with fade

                "Once the beast is sated, it goes into a half-asleep state. The girl finally begins to stir and motions to free herself."

                "You decide not to stick around and retreat before anyone sees you."

    elif story_flags["MU class days"] == 5: # Day 5 - Shizuka run-in
        you "Today is the fifth day of class... This time I will find that little minx."

        show sill glasses with dissolve

        sill "Master... You're sure about this?"

        you "Yes. Today, I will check the Dean's floor. Narika's probably been snooping around Shizuka's office."

        if MC.playerclass == "Wizard":
            play sound s_spell

            "You cast a discretion spell on yourself. You'll try poking your nose inside the dean's office to see if there is anything fishy."

        else:
            you "Your magic will help me. You have studied that discretion spell all night, as I commanded you?"

            sill "Yes... I didn't get any sleep... *sob*"

            you "Good, good. What are you waiting for? Cast it!"

            play sound s_spell

            "Sill does her best to shield your aura from magic detection."

        sill "B-But Master, Masou-sama is an archmage... Surely she won't be tricked by a simple sneak spell?"

        play sound s_punch

        sill "Ow!" with vpunch

        $ MC.rand_say("wi: Nonsense, do you doubt the extent of my magical abilities?", "Stop whining! If you did your job correctly, I'll have nothing to worry about.")

        you "Now, let's see what that sexy old lady has to hide..."

        scene black with fade
        show bg magic_office at top with dissolve

        you "No one seems to be here... Good, let's look around."

        "Being careful not to touch anything that could trigger a magic trap, you explore the room."

        "It seems no mage can ever resist filling their office with scores of gizmos, potions and dusty old tomes."

        "Nevertheless, for a mage's office, the Dean's is a lot more orderly than what you are used to."

        you "Nothing here seems really noteworthy..."

        "Suddenly, you catch a whiff of a familiar smell... Sakura flowers."

        you "Wait! That's Narika's smell... She has been here not so long ago."

        "Following the faint smell, you reach a large cabinet at the back of the room, and stop dead in your tracks. Something is off, after all."

        you "Well well well... There's a safe inside the cabinet, and it's been busted open. Took a fair bit of skill, from the look of it."

        "You don't doubt there was one or more magic wards protecting it, but they were bypassed. The safe sits empty, its door dangling open."

        you "Someone's just been here. It must have been our little friend. But what did she take?"

        "You turn to the last place you didn't check, an ornate door in the back of the room."

        you "Maybe I'll check this place next..."

        "You risk a quick peek through a crack in the door."

        stop music fadeout 3.0

        show bg shizuka bed1 at top with dissolve

        you "*gulp*"

        "Shizuka is lying on her bed, only wearing a simple white blouse with light blue panties."

        you "(Whoah, nice butt... That anti-aging spell sure works wonders...)"

        play sound s_sigh

        shizuka "Uh? Who's there?" with vpunch

        "You freeze in your steps. Shizuka has noticed you, from the other side of the door!"

        you "(Oh, shit...)"

        shizuka "It's faint, but I can feel your presence, student. I must admit that skulking spell of yours is surprisingly good."

        shizuka "But if you know what's good for you, you will leave my office this instant. Don't make me come out of here and report you."

        "Being in the other room, it seems she believes that you are merely a nosy student. You should definitely make a run for it."

        shizuka "I'll give you to the count of three to get the heck out of here. Unless you want to spend the rest of the month eating flies as a toadling..."

        menu:
            "What do you do?"

            _("Join her in bed"):                $ renpy.block_rollback()
                $ NPC_narika.flags["c3 path"] = None
                $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_narika)] = False
                $ NPC_narika.flags["magicu failed"] = True
                $ game.set_task("Find another way to stop the Void Kunoichi.", "story3")

                you "(Obviously, she's joking. She looks lonely all by herself. She clearly needs a man.)"

                you "(Otherwise, why would she lay here, half-naked and vulnerable, while there's an intruder in her office?)"

                play sound s_dress

                you "(It's time to show her a good time...) *unzip*"

                scene black with fade

                you "Here I come, Deany baby! Daddy's home~~~"

                play sound s_thunder

                show bg shizuka bed2 with flash

                "*ZAP*"

                play sound s_wscream

                you "AAAAARGH!!!" with vpunch

                "As soon as you enter the room, a massive bolt of lightning hits you right in the dick. Shizuka did not so much as move a muscle."

                "You fall flat on your face, as the smell of grilled pork fills the air."

                shizuka "Oh, it's you? I knew you were a pervert."

                you "*sizzle*"

                shizuka "You have overstepped your bounds, royal agent. I'll have you thrown out immediately, and make sure spells are in place so that you will not come back."

                play sound s_spell
                scene black with flash

                "*snap*"

                $ MC.interactions -= MC.interactions
                $ story_remove_event("c3_narika_MU_class", "daily")
                call remove_item(MU_entry_scroll, use_article=False) from _call_remove_item_4

                "When you recover from the shock, you are lying in the gutter outside the University's walls, with your pants all but burnt out to a crisp. The walk home puts your sneaking abilities through a hell of a test."

                you "I can't show my face again at the University until things cool off... I'll need to find another way to get to Narika."

            "Get the hell out":
                play sound s_steps
                scene black with fade
                show bg palace corridor

                "You don't need to be told twice, and you take off before she has a chance to catch you."

                "As you turn around the corridor, you hear Shizuka's yell behind you."

                shizuka "WHO THE HELL MESSED WITH MY CABINET? COME BACK HERE, RIGHT THIS INSTANT!!!" with vpunch

                "You run down the stairs and exit through the back, doing your best to stay well hidden until you reach the safety of the outside district."

                scene black with fade

                you "Damn, that was close. What did Narika steal from the Dean, I wonder?"


    elif story_flags["MU class days"] == 6: # Day 6 - Wall H
        you "Okay, the week is almost over... I need to find out what Narika is up to."

        show bg palace corridor2 at top with dissolve

        "You decide to try your luck in a section of the school you haven't yet explored."

        you "I think I've been to almost every class by now... Where could she be..."

        play sound s_steps

        "Suddenly, you hear fast footsteps coming from around the corner."

        you "Uh?"

        play sound s_crash

        "*BUMP*" with vpunch

        play sound s_surprise

        "???" "Hey, watch it!!!"

        "Someone running fast around the bend of the corridor slammed right into you, making you both fall to the ground."

        "You try to grab onto something for balance, but it turns out to be something squishy."

        play sound s_scream

        "Girl" "Eeek! It's my butt, you pervert!" with vpunch

        "You let go, getting ready to apologize."

        you "Err, erm, I'm sorry, Miss..."

        show narika school with dissolve

        narika "..."

        you "..."

        "Both at the same time" "It's YOU!!!" with vpunch

        play sound s_steps

        hide narika with easeoutleft

        "Narika immediately bolts in the opposite direction."

        you "Come back here! I need to talk to you!" with vpunch

        play sound s_shatter

        "Not listening, Narika leaps right through a window."

        you "It's the third floor! [MC.swear()]..."

        "Running to the window, you take a look outside. The girl has landed in a bush, and is already back up, running away at full speed."

        you "Damn, I'll never be able to catch her..."

        "Looking back down the hall, you notice a door gaping open in the corridor where she came from."

        you "She looked like she was in a hurry to leave... Let's see what she was running from."

        stop music fadeout 3.0

        scene black with fade

        play sound s_scream

        "Woman's voice" "Help me! Help!!!" with vpunch

        show bg MU_wall1 at top with dissolve

        you "Uh? What's going on here?"

        "It takes a little bit of time for you to process what your eyes are seeing."

        "It's a woman's butt, protruding out of a cement wall."

        you "What the..."

        play sound s_surprise

        "Woman's voice" "Is there anyone here? Help!" with vpunch

        show bg MU_wall2 at top with dissolve

        "The voice is coming from the other side of the wall."

        you "What... Who are you? what happened?"

        "Woman's voice" "I'm Professor Suza, I-I teach the teleporting class..."

        you "You {i}teach{/i} teleporting? Is that how you ended up here?"

        "Suza" "No, it's not that! I was a victim of a student prank..."

        "Suza" "It's that girl! She's trouble, I should have known something was off when she failed to cast the simplest telekinesy spell..."

        "Suza" "She wooed some of the boy students and convinced them to help her carry out this prank."

        "Suza" "They used a magic scroll to teleport me into the wall, and now I'm stuck here! I can't move, and I can't cast spells with my hands blocked!"

        you "Well, I guess it's a good thing the wall gave in instead of you..."

        "Suza" "This is no jape, Sir! That girl, she stole my... The..."

        you "Your what?"

        "Suza" "I-I can't say... But that's besides the point! Can you please help me?"

        you "Hmmm..."

        menu:
            extend ""

            "Help her":
                $ MC.good += 1

                you "Well, here, let me help you..."

                scene black with fade

                "With great effort, you manage to get the teacher unstuck."

                "Suza" "Thank you so much, Sir!"

                you "You're welcome."

                "Suza" "Now, to catch that little minx..."

                "You take a look inside the classroom. Drawers are dangling open, obviously someone has gone through them all while the teacher was incapacitated."

                you "It's risky to blow her cover like that in front of a teacher... To be so bold, she must be getting close to her goal."

            "Tease her":
                $ MC.good -= 1
                you "First, I would like you to tell me what it is she took from you."

                "Suza" "Uh? I'm sorry, Sir, it's confidential school information."

                you "Oh, really?"

                "Suza" "I hope you understand, I can't..."

                play sound s_dress

                "Suza" "Sir, what are you doing? Sir?"

                play sound s_scream

                show bg MU_wall3 at top with dissolve

                "In one fell swoop, you remove her pants. You start teasing her private parts with a piece of chalk."

                play sound s_scream_loud

                "Suza" "Sir, no, it feels ticklish! What's going on???"

                you "You know, we can play a game to jog your memory."

                "Suza" "I-I don't understand... Let me go..."

                you "I'm going to keep teasing you on this side of the wall... Until you tell me what that girl took from you."

                "You start tugging at her panties."

                play sound s_scream_loud

                "Suza" "Aaaah!!!" with vpunch

                "Suza" "It's not something important, I swear! You shouldn't concern yourself with this..."

                you "I guess I do feel concerned."

                play sound s_dress

                "You pull harder on her panties, rubbing the piece of chalk against her sensitive clit."

                play sound s_screams

                "Suza" "Aaaah, aah, aaaah!!!" with vpunch

                you "Oh, whoah, look at that! The teacher is getting wet."

                "You rub your palm against her crotch, feeling her moistness through her panties."

                "Suza" "N-no! Stop it already!" with vpunch

                you "Tell you what, if you don't tell me soon, I will consider this an invitation to fuck you..."

                "You start pulling her panties out of the way."

                play sound s_scream

                "Suza" "No! S-Stop! I will tell you, just stop it!"

                "You pause for an instant, giving her a little time to collect herself."

                "Suza" "Fine, fine, Arios, please stop this!"

                "Suza" "She took the key..."

                you "What key?"

                "Suza" "The archmage's key. The one Masou-sama gave me for safekeeping."

                you "What is this key for?"

                "Suza" "I-I just know I need to hang on to it. Masou-sama can't find out, or I will be fired!"

                you "Fired? That doesn't sound so bad..."

                "Suza" "Out of a glass cannon! Into hellfire!"

                you "Oh. And what does that key do?"

                "Suza" "It's one of the key to the vault... Oh, I'm in so much trouble..."

                you "The vault? One of the keys?"

                "Suza" "That alone won't open the vault, thank Arios..."

                "Suza" "Will you let me go now?"

                menu:
                    extend ""

                    "Yes":
                        you "Sure. Or rather, someone else will. Just hang in there, I'll tell the janitor on my way out."

                        "Suza" "H-Hey! Come back!" with vpunch

                    "No":
                        $ MC.evil += 3

                        you "I don't think so. We really only got started on the fun part."

                        "Suza" "S-Sir!!! Please stop this jest right away..."

                        play sound s_dress

                        show bg MU_wall4 at top with dissolve

                        play sound s_surprise

                        "Suza" "S-Something's touching me down here!"

                        "Suza" "Is it your... Finger?"

                        you "Nope."

                        "Suza" "Don't tell me it's your d-"

                        play sound s_scream_loud

                        show bg MU_wall5 at top with hpunch

                        "Suza" "Eeeek!!!"

                        "Pushing your hips forward, you enter her all in one go."

                        play sound s_ahaa

                        "Suza" "Ahaaa!"

                        "Although Suza's pussy is wet enough, she was ill-prepared to take your whole length."

                        "You enjoy the feeling of her snug pussy struggling to accomodate your cock."

                        you "Hang in there, teach'. This will get easier in a moment."

                        "Suza" "D-Don't move... I..."

                        play sound s_scream

                        "Suza" "Aaaah!" with hpunch

                        "Unable to resist, you start moving your hips, slowly at first."

                        play sound s_moans

                        "Suza" "Oh, ah, aaah..." with hpunch

                        "She moans softly as you fuck her, unable to gather her wits and keep talking."

                        "Her body is placed at a perfect angle for you thanks to the wall holding her. You put your hands behind your head, thrusting deeper inside her."

                        play sound s_aah

                        "Suza" "Aaaah! Oh, aah... [emo_heart]" with hpunch

                        "You can feel it's getting easier to move inside her now."

                        "Your balls are hitting her crotch with every move, making a lewd slapping sound."

                        "Suza" "N-No..."

                        you "Are you feeling this, teach'? I'm getting close."

                        play sound s_ahaa

                        "Suza" "N-No... Don't do it inside..."

                        play sound s_moans

                        "Suza" "Aaah, aaaaah, aaaaah!"

                        "With her legs spread wide, she can't move at all."

                        "You sink your fingers in the flesh of her ass, pulling her towards you."

                        "Suza" "I can't take any more... Ngh... Aaaaah!!!"

                        with flash

                        "Jamming your dick inside her up to the hilt, you cum in torrents, filling her womb with your semen."

                        play sound s_screams

                        "Suza" "Nooooo!!! Aaaah!!!!" with doubleflash

                        show bg MU_wall6 at top with flash

                        "Taking your cock out, you take a satisfied look at Suza, your cum flowing out of her pussy."

                        you "Well, that was fun. You'd better clean up before the next class starts..."

                        you "Oh, that's right, I forgot... You're stuck! Well, I'm sure the students will help you out. Muhahahaha..."

                "You leave, having found out new information about Narika's plan."


    elif story_flags["MU class days"] == 7: # Day 7 - Confrontation w/ Narika
        "The final day of class has arrived. It is time to confront Narika."

        you "I stayed up all night poring over plans of the school and the locations of my run-ins with Narika..."

        you "Today I am going to find her. And then we'll put an end to this!"

        scene black with fade
        show bg palace corridor at top with dissolve

        you "I am going to stand around this corner. If my calculations are correct, she is bound to go through here at least once today."

        you "Now let's wait..."

        with fade

        you "..."

        you "(Damn... I've been standing here for over an hour, and she isn't anywhere to be seen.)"

        "Groups of students pass you by, chatting and laughing, but you see no trace of Narika anywhere."

        you "(I guess I'll have to look elsewhere...)"

        play sound s_sheathe

        "The hissing sound of metal against metal startles you, and you feel something cold pressing against your throat."

        "It's the business end of a kunai. Although its wielder stands behind you, it's not hard to guess who it is."

        you "*gulp* Ahem, Narika-chan, why don't we talk this through..."

        narika school "You again! I'm not going to let you get in my way this time..."

        narika "You've been really annoying, stalking me like this! Are you in love with me, or something?"

        menu:
            extend ""

            "Yes, that's it":
                $ renpy.block_rollback()

                you "Well, I... Err... Sure. I am quite taken with you Narika..."

                you "You are, erm, the epitome of cuteness... And your ass..."

                narika "What?!?" with vpunch

                you "... your AS-tounding features are the stuff of... nice dreams..."

                "Narika's voice softens. she lowers her shuriken."

                narika "Oof, that was awful. But at least you seem sincere... *flattered*"

                "Her eyes sparkle."

                narika "Fine, I shan't kill one of my biggest fans."

                $ NPC_narika.love += 1

                you "Phew..."

            "Ew, no...":
                $ renpy.block_rollback()

                you "What? No way!"

                narika angry "What do you mean, no way?!? Am I not good enough for you?"

                you "Well, you're a deadly assassin, not exactly my type... I mean, there's Suzume, but she's got a massive rack..."

                narika "What the hell are you on about! My chest is still growing, okay! It's bigger than it looks!"

                you "Really?"

                "Unable to move your neck very much because of the blade, you still manage to try to eye her boobies."

                narika "Eek! Don't look!"

                "Narika steps back and tries to hide in embarrassment, withdrawing her blade."

                you "Phew."

                $ NPC_narika.love += 2

                narika "(Damn it, why isn't this boy looking at me like the others do? Is he gay, or something? Hmph!)"

            "You need me":
                $ renpy.block_rollback()

                you "You need my help..."

                narika "Hmph, you think I can't handle myself? I, the greatest Kunoichi of this continent, and the next?"

                "Her voice grows angry."

                you "N-No..."

                $ NPC_narika.love -= 1

                narika "Why am I even wasting my time with you... Speak, what do you want?"

                "To your relief, she lets you go, but she doesn't let her blade down."

            "Spare me!":
                $ renpy.block_rollback()

                you "D-Don't kill me, please. I have mouths to feed..."

                narika "Really? You have kids?"

                you "Uh... G-girls. Lots of girls. They call me 'daddy'..."

                narika "Oh, that's adorable..."

                narika "But that doesn't have anything to do with me. *cold*"

                $ NPC_narika.love -= 2

        you "Look, I know you've been collecting keys from the Dean and head teachers."

        you "I could help you reach your goal, if you'd just share your plan."

        narika "Oh really! Do you take me for a fool? Why should I trust you?"

        you "Well..."

        menu:
            you "You can trust me, because..."

            "Tell her the truth":
                $ renpy.block_rollback()
                you "I work for... Princess Kurohime. I am looking into some murders for her."

                you "The Court is at odds with the Mage's Guild. That's why I'm here incognito."

                narika "Hmmm... It's true that I don't see you fitting in with these stuck-up mages..."

                you "If helping you causes trouble for the Mages, I'm in."

                narika "Well, you have come to me, instead of ratting me out to the Dean. I suppose that makes you neutral."

                "Narika considers your offer."

                if NPC_narika.love >= 5:
                    narika "(I keep running into this boy... Maybe it's a sign? Destiny? Hmmm...)"

                    narika sad "Fine, I will allow you to lend me your aid, feeble as it may be."

                    narika angry "But don't get cocky! I run this show."

                    $ NPC_narika.flags["shared plan"] = True

                else:
                    narika "(I don't know this man, and I have a bad feeling about him.)"

                    narika sad "I don't really need any help. There's a minor hurdle to my plan, but it's nothing I can't handle with a few more days of preparation."

                    narika "Now, to dispose of the interloper..."

                    $ NPC_narika.flags["shared plan"] = False

            "Lie":
                $ renpy.block_rollback()
                you "I, err... Hate this school... They give me bad grades, and the tuition fees are horrendous..."

                you "And the school cafeteria sucks! I've seen roaches there."

                you "So I'm ready to help you with whatever your plan is. Please tell me what it is, with plenty of details."

                you "Make sure to include the exact extent of your involvement with the murders in the city..."

                you "And if you can put it in writing, that would be best."

                narika "Oh come on, hold it right there!"

                narika "Do you think you could fool me with such a stupid, bold-faced lie???" with vpunch

                you "..."

                narika "The school cafeteria is GREAT! They make a mean matcha tiramisu!!!"

                narika "So what if there are a few roaches... I like tiramisu!" with vpunch

                $ NPC_narika.flags["shared plan"] = False

        if NPC_narika.flags["shared plan"]:

            narika shy "So. I guess you'll do. I could make it worth your while."

            you "S-Sure."

            show narika school with dissolve

            narika "I'm going to break into the Archmage's vault, and recover a very specific item."

            narika "It takes four keys to open the vault, all operated by a separate individual. And I have collected all of them."

            you "So you need four people to get in?"

            narika "Ha! The Dean thinks this makes the vault foolproof against a single attacker, but she's naive."

            narika "With my super speed, I can activate all four keys at the same time, no sweat."

            you "Woah, that's amazing!"

            narika "It sure is! *beaming*"

            you "So... What do you need me to do, then?"

            narika "That old pervert professor told me about one more security contraption I need to deal with."

            you "What is it?"

            narika "It's not only that you need keys. The vault is magically trapped. It must be disabled from the outside."

            narika "I can't use super speed with that. I need someone outside the vault to do it."

            you "That would be me?"

            narika "I was thinking of hiring help, but I really don't want anyone else to blow my cover. Since you're here, you'll do."

            "You stop and think for a moment."

            "This could be a good opportunity to make an ally... Although the Mages' Guild will be pissed."

            "But this could also be an opportunity for a set-up... You could get Narika trapped in the vault."

            narika "So, are you in, or should I spill your guts on the floor right this moment?"

            you "I'm in, I'm in. *attempt to smile*"

            narika "Good! Let's wait until classes are over. Meet me inside the Dean's building."

            scene black with fade

            "You hide until classes are over and all students are on their way home."

            show bg empty_mansion at top with dissolve

            you "(I wonder if this is a good idea... If anyone sees me, I'm going to be in trouble...)"

            "???" "Hey."

            you "Uwaaah!!!" with vpunch

            show narika with dissolve

            narika "Shhh! It's me, silly."

            you "Damn, you Kunoichi are always so silent..."

            narika "Come, let's not waste any time. The Dean is studying in her chambers. This is the right time to strike."

            scene black with fade
            show bg magic_vault at top with dissolve

            show narika with dissolve

            you "So... This magic vault. What's in it?"

            narika "All of the most precious magical devices that the Dean has accumulated over the years. But only one of them interests me right now."

            you "You're not planning on taking everything?"

            narika "No way! Half these items are probably terribly cursed. And I don't like magic one bit. It creeps me out."

            narika "No, the plan is simple: get in, grab the item, get out."

            you "What's the item? Who wants it?"

            narika "*sigh* You don't need to know that. Just focus on your task, it's very simple: once the door is open, pull on this candelabra and keep it down until I'm done. This will disable the traps."

            you "Are you sure about this?"

            narika "I, uh, well... It had better work, or I'd make that old goat swallow the panties I gave him!"

            you "Wait. You gave him your panties?"

            narika angry "*blush* Ah, err, no, I mean... It's not..."

            narika "Anyway! Shut up, and grab that candelabra! Let's get to work!" with vpunch

            play sound s_dodge

            hide narika

            show ninja0:
                xalign 0.825 yalign 0.5
            with blinds

            "*WOOSH*"

            show ninja0:
                ease 0.25 xalign 0.475 yalign 0.4

            play sound2 s_dodge

            pause 0.3

            show ninja0:
                ease 0.15 xalign 0.825
                yalign 0.4

            play sound3 s_dodge

            pause 0.25

            show ninja0:
                ease 0.2 xalign 0.475 yalign 0.5

            play sound s_dodge

            pause 0.1

            play sound2 s_open

            "With amazing speed, Narika leaps from lock to lock, turning all four keys in a single instant."

            you "Wow!"

            play sound s_crash

            "The vault door slams opens, making way more noise than you'd like."

            hide ninja0 with dissolve

            narika "Pull that candelabra down to disable the traps! I'm going in!"

            "You pull the candelabra down and feel a tingling sensation as magical energy flows from the vault and into it, temporarily disabling the traps."

            show bg magic_vault_inside at top with dissolve

            "The vault is filled with magic contraptions and containers of various shape and sizes."

            narika "I'm in! Finally, I can reach it..."

            show narika with dissolve

            "Narika beelines towards a locked case."

            "She jumps with excitement as she sees a plaque. From where you stand, you can't read what it says."

            "Wasting no time, Narika begins to pick the lock expertly with the point of her kunai."

            narika "Finally, the Oculus Mask is within reach!"

            "She's too busy to pay attention to you. This could be the right time to strike."

            menu:
                "What do you do?"

                _("Keep the traps disabled"):                    $ renpy.block_rollback()

                    $ NPC_narika.flags["c3 path"] = "ally"
                    $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_narika)] = True

                    "You hold the candelabra in place, keeping Narika from being harmed by the magical traps."

                    play sound s_creak

                    "The case slowly creaks opens. Strangely, even though most items in this vault seem to have been left untouched for years, no dust flies off."

                    narika "We did it! All these weeks of preparation will finally pay off... The Oculus Mask is mine!"

                    play sound s_surprise

                    narika "Uh???"

                    narika "WHAT THE FUCK!!!" with vpunch

                    you "What is it?"

                    narika "It's... It's empty!"

                    you "What?"

                    narika "The Mask! It's not here! We've been duped!"

                    you "Are you sure you've looked in the right place?"

                    narika "It could only be here! The plaque said so, as well as my intel..."

                    play sound s_horn
                    pause 0.5
                    play sound2 s_horn

                    "An alarm starts ringing."

                    play music m_danger

                    narika "Damn it! We must run!"

                    you "What's going on?"

                    narika "I don't know! Someone set us up!"

                    play sound s_gust

                    "A gust of wind passes you by. It's Narika, fleeing at top speed."

                    you "Hey, wait for me!!!"

                    "You hear a commotion in the corridor outside. The mages have quickly scrambled some security and are getting ready to storm the place."

                    you "This is not looking good... How are we getting out of here???"

                    narika "Step back."

                    you "Uh? Why... What's that thing you're holding?"

                    narika "I said, step back."

                    "Deciding not to argue, you step behind her, just in time."

                    play sound s_vibro
                    pause 0.2
                    play sound2 s_fire

                    scene black with fade
                    show bg castle with dissolve

                    play sound s_spell

                    "Bird" "*chirp chirp chirp*"

                    "Bird" "Chirp?"

                    play sound s_lightning

                    show bg magicU explosion with flash

                    play sound s_wscream

                    you "AAAAAAAAAAAAAAH!!!"

                    "The wall is blast open. Effortlessly, Narika lifts you in her arms, jumping though the gaping hole opened by the explosion."

                    "Everything becomes a blur as she leaps from rooftop to rooftop, carrying you in her arms. It feels as if you were flying."

                    show bg rooftop at top with dissolve
                    show narika with dissolve

                    "After running at top speed for several minutes, Narika finally comes to a stop. You are amazed to see the Magic University already miles in the distance."

                    narika "Phew... That was close..."

                    you "[MC.swear()], you're faster than a charging griffin..."

                    "You both suddenly stop and realize that she is still holding you in her arms. What's more, her hand is resting on your ass."

                    you "Ahem..."

                    play sound s_crash
                    with vpunch

                    "Narika drops you down like an anvil."

                    narika blush "Ew! Get off me!"

                    you "You were the one copping a feel!"

                    narika "I absolutely was not! And I just saved your ass!" with vpunch

                    you "Yeah, and you were also getting a handful!"

                    narika "Aaaaaah!!!" with vpunch

                    "Narika's eyes spark with confusion and fury. Suddenly, something completely unexpected happens."

                    narika "Uwaaah!!! *burst into tears*"

                    you "Narika... Narika?"

                    narika "All these efforts... All this hard work... And it was all in vain..."

                    you "Calm down... Please."

                    "You give her your handkerchief. She grabs it and noisily blows her nose."

                    you "Listen, you need to tell me everything, and I'll see if I can help you."

                    you "But not here. I know just the place where you can lie low..."

                    scene black with fade

                    "Going through the side streets, you take Narika to [brothel.name]."

                    you "Here, you can take some rest. We'll talk tonight."

                    "Wait until tonight and debrief with Narika."

                    $ calendar.set_alarm(calendar.time, StoryEvent("c3_narika_debriefing", type = "night"))


                "Unleash the traps":
                    $ renpy.block_rollback()

                    you "It's now or never..."

                    play sound s_spell

                    "Releasing your grip on the candelabra, you feel the wave of magical energy ebbing back to the vault."

                    "A faint green halo starts glowing around Narika. When she notices it, it is too late."

                    play sound s_fizzle

                    show narika:
                        ease 0.5 zoom 0.2 ypos 0.8 yanchor 1.0 xalign 0.45

                    narika "W-What!!! The room has become gigantic!!!"

                    you "No, I don't think it has..."

                    "Narika stares back at you, astonished."

                    narika "You have become a giant too? What just..."

                    "Realization comes too late."

                    narika "The candelabra! You let it go!"

                    narika "You betrayed ME! I'll KILL you for this!" with vpunch

                    "Her voice has taken on a mouse-like pitch, which makes her threats all the funnier."

                    you "What was that? I thought I heard a rodent..."

                    play sound s_sheathe

                    "Furious, Narika flings her tiny shuriken at you. It sadly falls on the floor with a clang a mere few feet away from her."

                    narika "My strength is depleted too... What's this damned magic!"

                    shizuka "Why, it's only one of my many security layers, designed to stop hapless thieves like you, of course."

                    show narika with move:
                        xalign 0.25
                    show shizuka at right with dissolve

                    "Shizuka takes in the scene then looks at you, raising an eyebrow."

                    shizuka "Well, if it isn't our Royal agent... So this is the thief you were telling me about? I was expecting someone taller."

                    you "Sure. I tricked her. I did it as a, err, favor to you and the Guild..."

                    shizuka "Really? Well, I suppose thanks are in order then. Although I'm not sure I trust your motives."

                    "Shizuka strolls into the vault, and casually flicks the item case open, not even straining as she disable multiple intricate magic locks."

                    shizuka "Good to know the mask is still safely in... Uh?"

                    "Shizuka suddenly frowns."

                    shizuka "WHERE is the mask? My magical prototype! WHERE IS IT!!!" with vpunch

                    "She slams the case closed. You think you can see a tiny piece of paper flying away."

                    you "A prototype? What does it do?"

                    shizuka "It has the power of spectral sight, but that besides the point!"

                    shizuka "You!" with vpunch

                    "Shizuka looms over Narika, giving her a threatening look."

                    narika "I-I didn't take it, I swear! You stopped me before I could open it..."

                    "Shizuka then looks at you."

                    you "I didn't even step in the vault..."

                    "Even though she's seething, Shizuka understands that you are not lying."

                    shizuka "I will have to deal with that. Let me call the guards, they'll take that rat away."

                    you "Wait! I want to interrogate the prisoner first."

                    shizuka "She doesn't know who took the mask. For all I know, it might have been gone for months..."

                    you "But I need information for a different purpose. Court business..."

                    shizuka "*shrug* I suppose you can, then. Use one of the detention cells. But I'll give you an hour, no more."

                    "She snaps a finger, opening up a portal."

                    narika "Hey! First let me go back to my normal size!" with vpunch

                    "Shizuka scoffs."

                    shizuka "Not a chance. You'll stay like this until it no longer entertains me."

                    narika "*squeaking and vociferating*"

                    shizuka "That could take a while..."

                    call c3_narika_interrogation() from _call_c3_narika_interrogation

        else:
            $ NPC_narika.flags["c3 path"] = None
            $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_narika)] = False
            $ NPC_narika.flags["magicu failed"] = True
            $ game.set_task("Find another way to stop the Void Kunoichi.", "story3")

            play sound s_sheathe
            "*HISS*"

            you "W-Wait! I'll go away, and I won't bother you in this school ever again!" with vpunch

            narika "Hmph, you won't bother me again if you're dead..."

            play sound s_wscream

            you "Aaaaaah!"

            narika "*sigh* But fine, I don't want to get blood everywhere and blow my cover. Just get out of here, and never come back."

            you "I-I can go? Really?"

            narika "Yes. Now fuck off, before I change my mind."

            scene black with fade

            "Discretion being the best part of valor, you retreat promptly, leaving the school's premises."

            you "I lost this battle, but not the war... I must find another way to get to Narika."

        $ story_remove_event("c3_narika_MU_class", "daily")
        call remove_item(MU_entry_scroll, use_article=False) from _call_remove_item_5

    stop music fadeout 3.0
    scene black with fade

    return

label c3_narika_debriefing():

    scene black with fade
    show expression brothel.master_bedroom.get_pic() at top
    with dissolve

    "Later that night, you return to your quarters. You find Narika pacing around, brooding, while Suzume tries to comfort her."

    show narika at right with dissolve

    narika angry "Months of planning! And for what! I hate the fucking magic university! I hate magic!" with vpunch

    show suzume at left with dissolve

    suzume "Chill, sis'. [MC.name] is here, maybe he can help you sort out this mess."

    narika "Mister Pervert over here? Ha!"

    "You wonder when she took to calling you Mister Pervert, but you guess working in a brothel doesn't help your case."

    narika sad "Nothing can salvage this wreck... The money is one thing... But my reputation..."

    you "Calm down. Tell us the whole thing from the beginning."

    narika "Well..."

    "She hesitates for a moment, but shrugs."

    narika shy "I guess you already know a lot about the situation, so I might as well fill you in. It's not like any of this information is going to be useful to either of us."

    narika "I was personally hired by Stee V the Wondrous, a famous bard from Westmarch. As you must know, he's one of the most talented musicians in Xeros."

    narika "But he is also afflicted by a terrible infirmity. He is blind."

    narika "So when he heard that the Magic University in Zan had developed magical prototypes to help with various disabilities, he got interested."

    you "I see..."

    narika "But he couldn't, so he got in negotiations with the Dean, tried to get her to sell the prototype. But the price she was asking for could buy you a small principality in Westmarch. It was too much, even for him."

    narika normal "So he took the next logical step: he decided to {i}steal{/i} it."

    $ MC.rand_say("ar: That's not very honorable...", "wa: That's not very honorable...", "gd: That's not very honorable...", "tr: Yup, that makes sense.", "sh: Yup, that makes sense.", "ne: Yup, that makes sense.", "Steal it?")

    narika "Naturally. And so he hired the best Kunoichi money can get!"

    menu:
        extend ""

        "You're the best":
            you "It's you, isn't it?"
            $ MC.evil -= 1

            narika shy "It goes without saying. Although after today..."

            narika angry "Damn you, Mister Pervert, why did you have to remind me? *angry*"

            $ NPC_narika.love -= 1

            "Your flattery is only twisting the knife. Narika bows her head in shame."

        "Others are better":
            you "I know a couple others who are at least as good as you. Haruka, the Earth Kunoichi. Mizuki, the weird Ice lady."
            $ MC.neutral += 1

            narika sad "Pfff, normally, I would not even consider them competition..."

            narika "But what if they complete their assignment before I do? People will think I'm not worthy of my reputation!"

            "Narika lets these dark thoughts discourage her."

        "You're the worst":
            $ MC.good -= 1

            you "The best Kunoichi? Give me a break! You couldn't even manage a little burglary."

            "Narika blushes bright red."

            narika angry "You... You..." with vpunch

            "Suddenly, the unexpected happen. Tears start streaming from her eyes."

            narika sad "You're right, Mister Pervert... I completely failed... I am worthless..."

            "She sobs like a little girl. You are completely taken aback."

            suzume doubt "Well done, you big oaf..."

    "You change the subject, hoping to avoid a scene."

    you "Ahem... So this blind bard... Came all the way over to hire you?"

    narika "Of course not. He sent one of his henchmen, or should I say henchwomen."

    you "A woman?"

    narika "Yes, and a dangerous one at that. She was under a disguise, but I could sense her power... Not one to be trifled with."

    you "Could it be that she set you up?"

    "Narika broods, her mood somber."

    narika "Maybe... Why would she though? Why me?"

    you "Anyway, someone got there first. And stole that item. Correct?"

    narika "It must be! They replaced the mask with that stupid note."

    you "Wait, a note? What did it say?"

    narika "Uh? I don't know! I threw it on the ground as soon as we were out of there!"

    you "You WHAT?" with vpunch

    suzume normal "Yeah, she did throw it... But I picked it up."

    you "Phew... At least one of you has sense."

    suzume doubt "There's only a single sentence though."

    suzume "'Now Haku will have his revenge.'"

    you "Haku? Who the fuck is Haku?"

    narika "That's not a Kunoichi's name."

    suzume "It's a male name. Sounds like a Zanic name."

    you "Wait a minute- this item, the mask..."

    narika "The Oculus Mask."

    scene black with fade
    show bg mask escape at desaturate with dissolve

    you "Is it made of a silver-like metal? In the shape of a demon's eyes?"

    narika "It's Cimerian mithril, but yes! Have you seen it?"

    "Narika jumps to her feet, suddenly full of hope."

    you "Yes we have. Let me fill you in on the details..."

    scene black with fade

    "You tell Narika about the masked man who's been terrorizing Zan's upper class."

    show expression brothel.master_bedroom.get_pic() at top
    show narika at right
    show suzume at left
    with dissolve

    narika "It must be him, then! How did he manage to steal the mask in the first place? I was barely able to get to it, and I'm the best-"

    you "Let's not have this conversation again, shall we?"

    suzume "Listen, [MC.name]! We just got a major clue... That guy's name is Haku! And he's blind! If we-"

    you "Well, lot of big ifs and buts... And don't get me wrong, I like big butts and I cannot lie. But..."

    suzume "Do you have a better lead?"

    you "I suppose not..."

    suzume "We are closing in on this guy. A good day's work."

    you "And I can finally stop going to school every day like in that recurring nightmare where I forget my pants."

    narika "Hey, wait! What about me? I didn't get anything out of this!"

    you "Well... If you help us catch that guy, you can have the mask."

    narika "Really? Then I'm in!"

    show suzume bend with dissolve

    suzume "It's nice to have a new ally. Even if you're a bit... Young."

    narika blush "I may not be an old hag with saggy boobs like you, but I have twice the skill! Just watch me."

    suzume "I'm sure you don't have to worry about saggy boobs, being flat-chested and all..."

    narika angry "I'm still {i}growing{/i}, okay? Grrrr..." with vpunch

    you "Girls, girls... To the task at hand."

    suzume "Yes, boss!"

    play sound s_dodge
    hide suzume with blinds

    narika normal "Okay, Mister Pervert!"

    play sound s_dodge
    hide narika with blinds

    $ unlock_achievement("narika ally")
    call c3_end_story(NPC_narika) from _call_c3_end_story

    scene black with fade

    "And just like that, they're gone. You wonder if it will stop creeping you out one day."

    return

label c3_narika_interrogation():

    hide shizuka with flash
    show narika with move:
        xalign 0.45

    "Shizuka disappears into the portal, leaving you alone with Narika."

    narika angry "Let me go! I haven't done anything to you! I have nothing to tell you!"

    you "I'll be the judge of that."

    narika "Listen, if you help me escape..."

    you "Hush, I have questions first."

    you "What's your connection to the murders in the city, and the other Kunoichi?"

    narika "None, none whatsoever!"

    you "Then who do you work for?"

    narika "I can't say! Now, let me go!"

    you "At least tell me what that mask is..."

    narika "It's just a magical prosthetic, it gives the sense of sight to blind people."

    you "Who sent you to retrieve it?"

    narika shy "Uhn uhn. *shakes her tiny head* Not until you let me go!"

    you "I was hoping you'd be more helpful..."

    menu:
        "What do you do with Narika?"

        _("Agree to help her"):            $ renpy.block_rollback()

            you "Okay, I will help you escape. But it's going to damage my reputation with the Dean by a lot, so you better tell me all that you know!"

            narika shy "Fine, fine, I will tell you."

            narika "I was hired by a famous artist in Westmarch, who is blind."

            narika "He wanted me to recover the Oculus Mask to cure him."

            you "Hmm. That doesn't sound related to our case."

            narika "I told you, I can't help you. I'm as shocked as that stupid Dean that the mask was already stolen."

            narika "Now, you need to help me get out of here!"

            menu:
                extend ""

                "Sure":
                    $ NPC_narika.flags["c3 path"] = "neutral"
                    $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_narika)] = True
                    $ MC.good += 2

                    you "A promise is a promise, I suppose. But I need to get you past the guards."

                    narika normal "I'm super small now, so that should be easy!"

                    play sound s_dress

                    you "Here, you can hide in my pants."

                    narika "Sure, I can hide in your-"

                    play sound s_surprise

                    narika angry "PANTS???" with vpunch

                    you "Sure. If there is a bulge under my shirt, the guards may get be suspicious. In my pants, on the other hand, it's business as usual."

                    narika "But... But... I... No!"

                    "Eventually, seeing no alternative, Narika begrudgingly climbs inside your pants."

                    hide narika with dissolve

                    you "Heheh, your hair tickles."

                    narika "Shut up, and get moving! I can't breathe in here!"

                    scene black with fade
                    show bg empty_mansion at top with dissolve

                    "Making sure no one is watching, you leave the cell, walking past the guards that are watching over the vault room."

                    narika "*muffled* W-What's this? Something is taking all the room in here, and it's growing!"

                    you "It's your fault, if you keep wiggling like this, it stimulates my..."

                    narika "Uwaaah! Let me out!!!" with vpunch

                    show narika:
                        xalign 0.45
                        ypos 0.8
                        yanchor 1.0
                        zoom 0.2
                    with dissolve

                    "Finally, Narika tumbles down your leg and frees herself from your pants."

                    narika "That was HORRIBLE! Hair from your leg even got in my mouth! *spits*"

                    you "You hope it's from the leg..."

                    narika "Ew!" with vpunch

                    "Narika sighs, exasperated."

                    narika sad "Still, you held your part of the bargain I suppose. So I guess you can have this."

                    "She holds a small piece of paper in her tiny hand, handing it over to you."

                    you "What's that?"

                    narika "It's from the case in the vault. I grabbed it before that bitchy Dean could notice."

                    you "A note? It's a single sentence. Let's see..."

                    you "'Now Haku will have his revenge.' Who or what is Haku?"

                    narika "I don't know. But that sounds like a man's name."

                    you "Thank you, that could be a precious clue..."

                    you "You're free to leave, now. What are you gonna do?"

                    narika angry "Are you kidding? I need to find a way to grow back to my normal size, before I get eaten by a small dog!"

                    narika "It would be better if our paths never crossed again... I have many other scores to settle first, but don't think I forgot that you betrayed me in the vault!"

                    you "Tall words for such a tiny woman... Let's go our separate ways, then. I need to continue my investigation."

                "Nah":
                    $ NPC_narika.flags["c3 path"] = "banished"
                    $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_narika)] = True
                    $ MC.evil += 1

                    you "Nah, I was lying. You can stay here and enjoy the Dean's hospitality."

                    narika angry "WHAT???" with vpunch

                    you "You're entirely too trusting for a ninja, you know that? See ya!"

                    "You ignore her squeals of anguish as you step out of the cell."

                    $ unlock_achievement("narika arrested")

        "Leave her to her fate":
            $ NPC_narika.flags["c3 path"] = "banished"
            $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_narika)] = True
            $ MC.good -= 1

            you "I can see you're not being reasonable. I'll just leave you to rot in the Archmage's cells, then."

            narika angry "Wait! Wait!"

            you "Well, good bye then."

            "You ignore her squeals of anguish as you step out of the cell, knowing she will be dealt with by the Archmage."

            $ unlock_achievement("narika arrested")

        "Rape some sense into her":
            $ NPC_narika.flags["c3 path"] = "raped"
            $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_narika)] = True
            $ MC.evil += 5

            you "I don't think you understand the situation you're in, Narika."

            "Narika senses the threat in your tone."

            narika angry "What, you're thinking of beating me up, or something?"

            you "Oh no, no, I would never pick on someone so small..."

            narika "Fuck you!" with vpunch

            you "That, on the other hand, can be arranged..."

            narika "What do you-"

            scene black with fade

            play sound s_scream

            narika blush "AAAAAH!!!"

            play sound s_dress

            "*riiip*"

            show bg narika_tiny1 at top with dissolve

            narika "EEEEK! Get away from me, pig!" with vpunch

            you "It's interesting to have a real-life doll-sized girl to play with..."

            you "Even your nipples are so tiny... *rub*"

            play sound s_scream_loud

            narika "AAAAH!!! D-Don't touch me!!!" with vpunch

            you "Cute little pussy you have here... Even though it's so small, I can all the little details..."

            you "You look like the action figures I used to have as a child... But I didn't know it was going to be this type of action."

            narika "Let me GOOO!!! You fucking pervert!!!" with vpunch

            you "We'll need to get you well lubricated for the next part... *spit*"

            "She flinches in horror as you cover her lower body with saliva."

            play sound s_screams

            narika "What next part? No! Leave me alone!!! Heeeelp!!!" with vpunch

            you "This part."

            show bg narika_tiny2 at top with dissolve

            narika "Aaaah!!! Get that thing away from me!!!" with vpunch

            you "Hahaha, my dick is as tall as you now! I can rub it over your entire body in one go!"

            play sound s_scream_loud

            narika "Disgusting! Heelp, someone, heeeelp!!!" with vpunch

            "Mercilessly, you continue, using your spit as lubricant to slide up and down her tiny exposed body."

            narika "What's... What's happening to me... This is a nightmare..."

            "Grinding against her, you increase the pressure on her crotch, forcibly keeping her legs open."

            you "I hear the Kunoichi are very flexible. Why don't we test that theory?"

            narika "What do you... Aaaaaah!!!" with vpunch

            show bg narika_tiny3 at top with dissolve

            "You place your dick near her lower entrance."

            narika "No, no, wait, WAIT!!! This is impossible!"

            narika "You can't do this, it will br-"

            play sound s_splat

            show bg narika_tiny4 at top with dissolve

            narika "AAAAARGH!!!" with vpunch

            "Ignoring her, you push your dick inside her tiny doll-like body. At first, it looks like there is no way this will ever work, but slowly you force your way inside, stretching her to her limits."

            "Narika cries out in pain and bewilderment."

            play sound s_scream_loud
            narika "AAAAAAH!!!" with vpunch

            you "Look at that, it's like you're pregnant with my dick!"

            narika "STOOOOOP!!! STOP!!!" with vpunch

            "A lesser woman would have passed out or died, but Narika had years of intense training, allowing her to surpass the limits of the human body."

            "Still, she hangs on only by a thread."

            play sound s_screams

            narika "NGYAAARH! AAARH! AAAAH!!!" with vpunch

            "Her body is grossly deformed as you start fucking her."

            you "Hahaha, I like tight pussy, but this is something else!"

            narika "I'm going to die, stop!!! *sobs*"

            you "You're the perfect onahole for me. Muhahahaha!"

            narika "Noooo..."

            "You only laugh and increase your pace, making her jerk her head back and scream like an animal."

            show bg narika_tiny5 at top with dissolve

            play sound s_screams

            narika "AAH, AAAH, AAAAAAAH!!!" with vpunch

            "Enjoying yourself at her expense, you keep messing up her insides mercilessly, ruining her tiny body."

            narika "AAH, NGGH, AAARH... S-Stop... *sob*" with vpunch

            you "Don't worry, it's not going to last much longer."

            "Her eyes widen, as she wonders what you mean. She doesn't have to wonder for long."

            with flash

            you "Ughhh..."

            show bg narika_tiny6 at top with doubleflash

            "Suddenly, you start cumming, filling her belly to the brim with semen."

            play sound s_scream_loud
            narika "UWAAAGH!!!" with vpunch

            with flash

            "You pull out and spray the rest of your cum all over her tiny body. She howls in pain as your dick pops out."

            you "Hehehe, I might have gone a little overboard this time... But that was fun for me, at least."

            "Narika is looking down at her gaping hole, horrified. You have ravaged her body from head to toe."

            "She is left speechless, in a completely state of shock."

            you "That was fun. Now, will you tell me about your secret-"

            narika "*drool*"

            you "Narika? Narika?"

            "Narika is completely unresponsive, her face inexpressive. Her mind is gone. She is alive, but barely."

            "You try to talk to her, but she ignores you. She is completely gone."

            you "Looks like I broke another one of my toys... Oh well."

            $ MC.change_prestige(3)

            scene black with fade

            "Shrugging, you ditch her limp body on the ground where she lands with a thud, barely breathing amidst a pool of cum."

            "You step out of the vault, hoping to get out of here before anyone asks too many questions."

            "Fortunately, no one interferes, and soon you are out of the Magic University for good."

            $ MC.change_prestige(3)
            $ unlock_achievement("narika raped")

    call c3_end_story(NPC_narika) from _call_c3_end_story_1

    scene black with fade
    # show bg magic_university at top with dissolve

    "You think back about what you've learned."

    you "A magical all-seeing mask has disappeared, and soon after this masked man appears and starts murdering people in the city... Quite the coincidence."

    you "If it is indeed the same person, our culprit was a blind man... I guess that narrows down the possibilities."

    return

label c3_narika_final_intercept(): # Called from ninja_game
    play music m_narika fadein 3.0

    scene black with fade
    show bg narika intro at top with dissolve

    narika ninja "You are trying my patience! Don't you understand I'm way out of your league?"

    if MC.has_item(void_rune.name):
        "You can feel dark energy flowing from the void rune into the warhammer where you inserted it."

        you "Bring it on!"

        "Narika starts running, but she is much slower than before."

        narika "Khhh! *sweat*"

        narika "(What's happening... It feels like every movement is a slog?)" with vpunch

        stop music fadeout 3.0

        $ story_flags["ninja hunt"] = calendar.time

        call run_ninja_game(njgame) from _call_run_ninja_game_1

        return _return

        # results are in BKchapter2 - label intercept_narika()

    else:
        suzume "Damn, she's slippery as always... Boss, I don't think we can catch her."

        play sound s_gust
        hide bg with dissolve

        "Narika moves faster than your eyes can see, and before you have a chance to react she is already leaping from rooftop to rooftop in the distance. You know better than to run after her."

        scene black with fade

        you "Damn, if only I had a counter to her super speed..."

    return

label c3_narika_captured():

    "That night, you join Gizel in the cellar of [brothel.name] to visit your new captive."

    scene black with fade
    show bg narika_capture1 at top with dissolve

    narika blush "You! What have you done to me! My powers won't work here!" with vpunch

    gizel smirk "Hmph. Mind your tone, little girl."

    gizel "I just set you up to be comfortable for what's coming."

    narika "What's coming? W-What do you mean? And why am I naked!!!"

    gizel "Ah, [MC.name], here you are. I was waiting for you to begin the lesson."

    narika "Lesson? What do you sick people want with me??? *scared*" with vpunch

    you "I have brought you here so that you will join my fine establishment."

    narika "What? What are you talking about? What establishment?"

    you "Well, it is, let's say, a 'house of carnal pleasure'."

    narika "A house of carnival what?"

    gizel "It's a brothel. For whores. Hookers. Prostitutes."

    play sound s_surprise

    narika "What!!! Are you out of your mind??? I'm not even... Err..." with vpunch

    gizel "Silence!" with vpunch

    show bg narika_capture2 at top with dissolve

    play sound s_punch

    "*WHIP*" with vpunch

    show bg narika_capture3 at top with dissolve

    play sound s_scream

    narika "OUCH!!!"

    gizel "I told you to change your tone. You will mind your manners, or else..."

    narika "B-But... But... You guys..."

    "Gizel has a dangerous glint in her eyes."

    gizel "Mistress Gizel. And you will refer to [MC.name] as Master."

    narika "Whaaat?" with vpunch

    narika "You can't seriously suggest I call you that?"

    play sound s_punch
    pause 0.2
    play sound2 s_punch

    "*WHIP* *WHIP*" with vpunch

    show bg narika_capture4 at top with dissolve

    play sound s_scream

    narika "AW!!! STOP!!!" with vpunch

    gizel "Ask me nicely!"

    play sound s_punch

    "*WHIP*" with vpunch

    narika "S-Stop... M-M-Mistress..."

    gizel "That-a-girl!"

    you "Gizel, there is no need for such violence."

    gizel "Who said there's a need? I just wanted to do it."

    you "Anyway. Narika, look at the situation you're in. You've lost your powers, you've lost your reputation."

    you "It would be better for you to cooperate."

    narika "B-B-But... I am not a whore!!!"

    gizel "Who are you talking to???" with vpunch

    play sound s_punch
    pause 0.2
    play sound2 s_punch

    "*WHIP* *WHIP*" with vpunch

    show bg narika_capture5 with dissolve

    narika "AW! OW! OUCH!!!" with vpunch

    show bg narika_capture4 with dissolve

    narika "M-Master [MC.name]... I mean... I am not..."

    gizel "You are not a whore... {i}Yet{/i}."

    you "No one said you have to be a whore... You can tend to the customers in other ways: You can wait tables, dance for them..."

    narika "D-Dance? Only dance?"

    you "Well, at first..."

    narika "What do you mean, at first?!?" with vpunch

    you "Well, you can take things at your own pace."

    gizel "Or you can take things at our pace. *snark*"

    narika "B-But... You don't understand... I'm..."

    gizel "Spit it out!" with vpunch

    play sound2 s_punch

    "*WHIP*" with vpunch

    show bg narika_capture5 at top with dissolve

    play sound s_scream

    narika "AAAW!!!"

    show bg narika_capture4 at top with dissolve

    narika "STOP, STOP! I'M A VIRGIN, OKAY???" with vpunch

    gizel "A virgin? Ha..."

    play sound s_evil_laugh
    gizel "HAHAHAHAHAHA!!! That little slut is a virgin..."

    "Tears well up in Narika's eyes."

    narika sad "It's true! I have saved my virginity... For... For the right person..."

    "Gizel laughs cruelly."

    gizel "Yeah yeah, sure, we believe that. *snark*"

    you "Suzume told me how you keep flirting with boys wherever you go..."

    gizel "But deep down, you were always scared to take the plunge."

    "Narika looks away, not answering."

    gizel "Little scaredy scaredy cat..."

    narika "Grrr... *clench teeth*"

    gizel "It can't be helped, then. You'd just be dead weight in a whorehouse."

    gizel "I'm just going to have to feed you to the pigs..."

    narika angry "Pigs? W-Wait!" with vpunch

    gizel "Say goodbye, sweetheart..."

    show bg narika_capture5 at top with dissolve

    play sound s_scream_loud

    narika "NOOOOO!!!" with vpunch

    narika "I DON'T WANT TO DIE A VIRGIN!!!" with vpunch

    "The three of you stand for a moment in stunned silent. Narika can hardly believe she blurted it out loud."

    show bg narika_capture5 at top with dissolve

    narika "*sob*"

    gizel "So? I'm sure [MC.name] will be happy to help you with that..."

    play sound s_surprise
    show bg narika_capture6 at top with dissolve

    if NPC_narika.love >= 5:
        narika "(T-That boy? If it's him, then... Could it be?)"

    elif NPC_narika.love >= 1:
        narika "(Wait, what? Am I going to do it with that random guy???)"

    else:
        narika "(Oh no!!! Not that jerk!!!)"

    narika "M-Mistresss, wait, I can't..."

    play sound s_clang

    "Ignoring Narika's muffled complaints, Gizel yanks on her chains, lifting her body up in the air."

    scene black with fade
    show bg narika_capture7 at top with dissolve

    "Narika is hanging from her chains with her legs spread apart and her body exposed."

    "Narika blushes bright red. Instead of protesting, however, she has fallen strangely silent."

    narika "W-What... What are you going to do to me?"

    "Her tone is strangely quiet. It's almost as if there was as much curiosity as fear in her voice."

    $ _min = rand_choice(farm.get_minions("machine"))

    if not _min:
        $ _min = "R2D2"
    else:
        $ _min = _min.name

    gizel "First, I'm going to introduce to one of my minions... [_min]."

    play sound s_vibro

    show bg narika_capture8 at top with dissolve

    narika "W-Wait!!! What the heck is that???" with vpunch

    play sound s_vibro

    "[_min]" "*tickle* *tickle*"

    show bg narika_capture9 at top with dissolve
    play sound s_laugh

    narika "Heeheehee!!! Stop it!!!"

    show bg narika_capture10 at top with dissolve

    narika blush "It feels strange... The robot... It vibrates..."

    gizel "It's a massage bot. Trust me, it will feel good... Nothing to worry about."

    show bg narika_capture11 at top with dissolve

    play sound s_ahaa

    narika "Ahaa!" with vpunch

    play sound s_vibro
    "The robot hands move to massage Narika's petite boobs, eliciting soft moans from her as they move in circles."

    play sound s_vibro

    play sound s_mmh

    narika "Hmmm..."

    gizel "Looks like your tits are small, but sensitive... Like mine..."

    show bg narika_capture12 at top with dissolve

    play sound s_vibro

    "*BZZZ*" with vpunch

    play sound s_moans_short

    narika "Ah, aah, aaaah!!!"

    gizel "Haha, look at that, [MC.name]! She's enjoying herself."

    narika "N-No... I just feel... Weird..."

    play sound s_aaah

    narika "Aaaaah!" with vpunch

    "In spite of herself, Narika is being turned on by the vibrating bot."

    gizel "Fufufufu..."

    "After playing with her for a little while, Gizel suddenly stops the apparatus."

    show bg narika_capture11 at top with dissolve

    narika "*pant* *pant*"

    narika "Is it... Over?"

    play sound s_evil_laugh

    gizel "Oh, no! [MC.name], come forward."

    narika "W-W..."

    play sound s_dress

    narika "*gasp*"

    "You remove your pants. Narika is stunned to see your dick for the first time, rock-hard and standing for attention."

    narika "*gulp* This can't possibly..."

    show bg narika_capture13 at top with dissolve

    play sound s_scream_loud

    narika "AAAAAH!!!" with hpunch

    "Narika scream as you enter without warning, helped by the love juice that has started to drip from her pussy."

    gizel "Oooooh, it looks like she was a virgin after all!"

    "Narika whimpers as you stretch her pussy with your thick rod."

    "It takes a while for her to adjust to the foreign presence, but she controls her breathing and remains remarkably calm."

    gizel "As expected from a Kunoichi, a little pain is nothing to her. I'd even wager she likes it."

    narika "N-No... It's just... I..."

    play sound s_scream

    narika "Aaaaah!" with hpunch

    "You start moving, overriding Narika's senses as she feels her pussy stretch wider."

    gizel "That girl is a little bit of a masochist, I can tell."

    "You move your hips closer to Narika's body, your balls brushing against her crotch."

    play sound s_mmh

    narika "Hmm..."

    gizel "Look! She's already getting used to it!"

    narika "N-No, it just feels... Wrong..."

    gizel "What a liar. I know you've been wondering about sex for a long time. Maybe [_min] here can make you honest."

    show bg narika_capture14 at top with dissolve

    play sound s_vibro

    "BZZZZ" with hpunch

    play sound s_screams

    narika "Aaaah! Aaaah!" with hpunch

    gizel "Haha, look at that! Her boobs are so sensitive, she's already shaking!"

    gizel "I think she needs a good pounding. [MC.name], it's time to work your magic."

    play sound s_moans

    "Not waiting for Gizel to egg you on, you increase your pace, sliding more and more easily inside and out of her, until you almost match the robot's pace."

    narika "Noooooo!!! I'm losing my mind!!!" with hpunch

    "Narika loses control of her voice, her moans are loud and unrestrained."

    gizel "She's clinging on for dear life, but she loves it! That girl is a natural!"

    narika "No! Please, stop! I can't take it anymore!!!" with hpunch

    gizel "Oh, I bet you can! How about I give you some help?"

    play sound s_clang

    "Gizel pulls on Narika's chains, forcing her body into an even more spread out position."

    narika "Ughn, aaah, aaah!" with hpunch

    "This new position allows you to bang her even deeper. You slowly feel your climax approaching."

    "Her pussy is squeezing you harder and harder, until you are ready to burst."

    gizel "She's already close, too! Haha!"

    play sound s_aah

    narika "Close to, hmmm... Close to... What?"

    gizel smirk "This!" with vpunch

    show bg narika_capture15 at top with flash

    "Gizel suddenly puts a well-manicured finger inside your asshole, sending you over the edge."

    with doubleflash

    you "Hey!"

    play sound s_scream_loud

    narika "AAAAAAAAH!!! AAAAH!!!" with hpunch

    play sound s_orgasm

    "You fill Narika up with your cum, causing her to orgasm at the same time."

    show bg narika_capture16 at top with flash

    gizel "Hahaha! That was so much fun!"

    narika sad "Aaaaah... Did I die? I'm seeing stars..."

    "Narika's eyes are unfocused, and her breathing is labored. A thin line of drool leaks from her mouth."

    gizel "Fufufu, you're okay, kid. I might not feed you to the pigs, after all."

    gizel "Anyway, off we go! I'm going to take good care of you at the farm..."

    narika angry "Wait, what? No!!! I don't want to go to your weird farm!"

    "She looks at you and Gizel in turn with pleading eyes."

    gizel "What??? You're coming with me, right now, and the first thing I'll do is to whip the impertinence out of your sorry husk! *annoyed*"

    $ dim = MC.name[:3]

    narika "Noooo, no, wait!!! [dim]... Master [MC.name]! Don't leave me with that crazy w-witch!"

    narika "I'll work as a waitress or, or I'll dance, or something... Just don't let her take me!"

    you "Well. If you're willing to work, I guess I can..."

    play sound s_surprise

    gizel surprise "What?!? No you won't! She's mine! I'm going to break her!" with vpunch

    narika "I'll be good, I promise! Just... Keep me away from her!"

    you "Fine, fine, you can stay and work at [brothel.name], then. Gizel, leave her be."

    gizel angry "W-What! This is unacceptable! I-" with vpunch

    "You harden your tone."

    you "Back off, Gizel. I've taken my decision."

    gizel upset "Hmph... Fine, whatever, have it your way. I don't care about that slut!"

    narika sad "Aw, th-thanks..."

    you "Oh, and Gizel?"

    gizel "Yes? What?"

    you "Take your finger out of my asshole. It's kind of undermining my authority when I speak."

    gizel shy "Oops, sorry!" with vpunch

    scene black with fade

    "Narika has agreed to help in the brothel. She will perform different jobs outside of whoring, but you won't be able to control her directly until her training is complete."

    "Make sure you have {b}every type of jobs available{/b} at the brothel for this."

    $ MC.change_prestige(3)

    call remove_item(void_rune, definite_article=True) from _call_remove_item_6

    # INIT BREAKING COUNTER
    $ NPC_narika.flags["waitress counter"] = 0
    $ NPC_narika.flags["dancer counter"] = 0
    $ NPC_narika.flags["masseuse counter"] = 0
    $ NPC_narika.flags["geisha counter"] = 0

    $ story_add_event("narika_break_test", "daily")

    $ NPC_narika.flags["c3 path"] = "captured"
    $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_narika)] = True
    call c3_end_story(NPC_narika) from _call_c3_end_story_2

    return

label narika_break_test():

    # Step 0: Proc job event

    python:
        job_event=None
        for job in all_jobs:
            if job == "dancer":
                if NPC_narika.flags["waitress counter"] >= 5 and NPC_narika.flags["geisha counter"] >= 5 and NPC_narika.flags["masseuse counter"] >= 5 and NPC_narika.flags["dancer counter"] == 4: # Happens after all job training has been completed.
                    job_event = "narika_" + job
                    NPC_narika.flags[job + " counter"] += 1 # Avoids job event proccing more than one time
                    break
            else:
                if NPC_narika.flags[job + " counter"] == 4:
                    job_event = "narika_" + job
                    NPC_narika.flags[job + " counter"] += 1 # Avoids job event proccing more than one time
                    break

    if NPC_narika.flags["waitress counter"] >= 5 and NPC_narika.flags["geisha counter"] >= 5 and NPC_narika.flags["masseuse counter"] >= 5 and NPC_narika.flags["dancer counter"] >= 5:
        $ story_remove_event("narika_break_test", "daily")
        # $ calendar.set_alarm(calendar.day + 1, StoryEvent(label="narika_broken"))

    if job_event:
        $ renpy.call(job_event)
        $ MC.change_prestige(3)
        $ notify("Narika has now trained sufficiently as a %s." % job)
        return

    # Step 1: Find an available job

    python:
        for girl in job_girls: # job_girls should be initialized in End day
            if girl.job in all_jobs:
                if NPC_narika.flags[girl.job + " counter"] < 4:
                    break
        else:
            girl = None

    # Step 2: Train

    if girl and girl.job in all_jobs:

        if not NPC_narika.flags["jobs intro"]: # Intro to jobs
            $ NPC_narika.flags["jobs intro"] = True

            show expression bg_bro at top with dissolve

            narika sad "(So this is it... What on earth am I supposed to do?)"

            sill "Oh, hi! You're the new girl, right?"

            narika "The new... Yes. I guess so."

            sill "Well, it's a pleasure to meet you! I'm Sill, by the way."

            narika shy "Erm, okay. Hi."

            sill "There are many things to learn, but I'm sure you'll manage. And don't forget, if you have any question, I'll always be here for you!"

            narika "How..."

            sill "Yes?"

            narika angry "How can you be so perky and carefree!!!" with vpunch

            sill "Uh?"

            narika "This is a {i}whorehouse{/i}!!! People come here and have sex!" with vpunch

            sill "Well... Yeah, of course. That's what a whorehouse is."

            narika "Aren't you bothered by it???" with vpunch

            sill "*thinking* Well, there are a lot of chores... A lot of bed sheets to clean up... And Master [MC.name] often scolds me, but..."

            narika "That's not what I mean!!! The SEX!!! It's wrong!!!" with vpunch

            sill "The sex is wrong? Why?"

            narika shy "Because, uh... Well..."

            sill "I see. Maybe you don't like it because you've had bad lovers in the past."

            sill "But Master [MC.name] can help you. He personally trains most of the girls."

            narika blush "That's not what I mean!!!" with vpunch

            narika shy "I already saw his, err, training..."

            sill sad "Oh, so you had sex with him already? What did he do? He's not in love with you, is he? *anxious*"

            narika "I, err, uhm... It was weird, okay? I didn't want to do it! It felt... Wrong!"

            sill happy "Oh, okay. You're not made for each other then! It's fine."

            narika "Does, erm... Does [MC.name] have sex with everyone around here?"

            sill "Well... Pretty much, yes."

            narika "Does it mean that... Err... He'll do it again with me?"

            sill sad "Well, that's probably his intention..."

            sill happy "But you know what, I'll tell him to leave you alone."

            narika "N-No, that won't be necessary..."

            sill "Oh don't worry, he'll listen to me for sure! I think. I'm his number 1 confidant and advisor, so... Hehe."

            narika angry "I said don't!" with vpunch

            sill sad "Whoah!"

            narika shy "It's just that, erm... I don't want any favors, okay..."

            narika "(What am I doing?)"

            sill normal "Well, erm... Okay, then. Today, you'll follow [girl.name] around. She'll show you the ropes."
            scene black with fade

        if NPC_narika.flags[girl.job + " counter"] == 0:
            show expression ("bg " + job_room_dict[girl.job]) at top with dissolve

            if girl.is_("dom"):
                girl.char "Look who's here... Another newbie."

                narika shy "Well... Yes. What do you do here?"

                girl.char "Today I'm working as a [girl.job]. Follow me, kiddo, and try to keep up."

                narika "Hmph, of course!"

            else:
                girl.char "Oh, welcome, Miss. You are...?"

                narika shy "Narika. I'm the new girl. I guess."

                girl.char "S-Sorry, right! Sill told me."

                girl.char "I'm working as a [girl.job] today. Would you care to help me?"

                narika "Sure, okay..."

            if girl.job == "waitress":

                girl.char "Our main job is to serve customers with food and drinks, and to chat with them as we go."

                girl.char "Tipsy customers often get handsy, but you'll get used to it."

                narika "Can I chop their hands off?"

                girl.char "What??? No!!!" with vpunch

                girl.char "Just play along, you'll get better tips this way."

                play sound s_sigh

                narika "(This stuff is complicated...) *sigh*"

            elif girl.job == "dancer":

                girl.char "As dancers, we put on a hot show for our audience, we got all kinds of fun costumes..."

                narika "Wait, this one is damaged! There are holes everywhere..."

                girl.char "Oh, no, that's intended."

                narika "But it doesn't even cover the..."

                girl.char "Teeheehee, that's the best part!"

                narika "(Oh my...)"

            elif girl.job == "masseuse":

                girl.char "We give massages to the customers, so that they can get in the mood for the rest."

                narika "Massages? I guess I know how to give massages!"

                girl.char "You do? Actually, my shoulders are sore. Show me!"

                narika "Sure thing. Get ready..."

                girl.char "Is that... A fighting stance?"

                play sound s_punch
                pause 0.5
                play sound2 s_punch
                pause 0.3
                play sound3 s_punch
                pause 0.2
                play sound s_punch

                narika "ATTACK OF THE 10,000 NEEDLES!!! TAHTAHTAHTAHTAHTAHTAAAAAH!!!!" with vpunch

                play sound s_scream_loud

                girl.char "AAAAAAARGH!!!" with vpunch

                with fade

                girl.char "Aaaaw... I can't feel my body from the waist up..."

                narika "Erm, sorry... I think I overdid it a little..."

                girl.char "Actually, that was good... The pain is gone..."

                girl.char "But please be more gentle with customers, okay? We want them relaxed, not dead."

                narika "S-Sorry..."

            elif girl.job == "geisha":

                girl.char "As a geisha, you must bewitch customers with your wits and artistic talents, and display respect proper etiquette."

                narika blush "*loud belch* Yeah, yeah, how hard can it be."

                girl.char "Err..."

                girl.char "Let's see. Do you know how to sing?"

                narika "No."

                girl.char "Play music?"

                narika "No."

                girl.char "Make tea?"

                narika "Nope."

                girl.char "Do you know how to recite poems? Arrange flowers? Do your make-up? Put on an Obi? Hold your hair up with chopsticks?"

                narika angry "No, no, no and no!!!" with vpunch

                narika "What good are any of these things??? I know a hundred-and-one ways to skewer a man so that he bleeds and dies silently! Will that do?"

                girl.char "Oh dear..."

                girl.char "Look, let me help you put this kimono on. You just stand pretty, and whatever you do, don't open your Arios-damned mouth."

                narika "Hmph, fine..."

                narika "(What could be so hard about this geisha job anyway?)"

        $ NPC_narika.flags[girl.job + " counter"] += 1

        $ renpy.block_rollback()

        with fade

        if girl.job == "dancer" and NPC_narika.flags[girl.job + " counter"] == 4:
            $ notify("Narika has now trained sufficiently as a dancer.")

        if NPC_narika.flags[girl.job + " counter"] <= 4:
            $ notify("Narika trained with %s as a %s (%i/4)." % (girl.name, girl.job, NPC_narika.flags[girl.job + " counter"]), pic="side narika blush")

    else:
        $ notify("Narika couldn't help any girls in the brothel with their job.", pic="side narika blush", col=c_lightred)

    return

label narika_waitress():
    scene black with fade

    "Hearing some noise in the kitchen, you take a peek."

    you "Well, if it isn't Narika working in the kitchen... I can hardly believe you went from a murderous Kunoichi to baking cookies, hehe."

    narika blush "S-Shut up... I just have a lot to do for customers..."

    you "And I want to thank you for being pleasant to our customers. I see you've even adopted our 'no bra' policy."

    show bg narika_waitress1 at top with dissolve

    play sound s_surprise

    narika "S-Stop fooling around! I just don't usually wear bras..."

    you "Oh yes, I've noticed... I guess with your small boobs, you don't need them."

    narika "My boobs are not small!!! Grrr..." with vpunch

    you "Let me see... Hmmm, it's just as I remembered, they're smallish but fit in my hands nicely!"

    play sound s_dress

    "You squeeze them to illustrate your point."

    play sound s_ahaa

    narika "Ah, aah, stop it..."

    you "But your nipples are really perky. They stand at attention whenever I touch you... It's nice."

    play sound s_scream

    narika "Aaaaah!"

    you "And they're so sensitive..."

    "You gently rub her nipples between your fingers, eliciting more moans from Narika."

    narika "I've got... Aaaah... Food to prepare..."

    "Ignoring her, you rub your bulge against her ass."

    you "And yet, you're not stopping me. What gives?"

    show bg narika_waitress2 at top with dissolve

    play sound s_hmm

    narika "I... Hmmm, idiot, I can't think straight when you... Aaah... Touch me like that..."

    "You continue groping Narika's tits and ass. She could easily push you back, but instead she waits for what comes next, like a deer frozen in the headlights of a yet-to-be-invented mechanical contraption."

    you "Narika, just resume your cooking. We don't want to keep the customers waiting."

    show bg narika_waitress3 at top with dissolve

    narika blush "You're not going to do... Anything else, are you?"

    you "Oh, don't mind me... I'm just going to touch you a little."

    "Narika resumes her cooking with shaking hands, blushing and moaning softly as you caress her body."

    play sound s_aaah

    narika "Aaah... [emo_heart]" with vpunch

    "Narika pretends to ignore you, but you can tell she is getting turned on."

    you "Stay focused on the food, will you? Don't enjoy yourself too much."

    narika "O-Of course! I'm not feeling this one bit. With my elite training, I can concentrate on whatever task is at hand regardless of your pointless distractions."

    you "Oh good, then by all means, ignore this."

    "You slip your hands inside her panties, slowly taking them off sending shivers down her spine."

    narika "Just let me work. I'm not going to be-"

    show bg narika_waitress4 at top with dissolve

    play sound s_scream

    narika "Aaah!!!" with vpunch

    "Narika's eyes open wide as you lift her leg up without warning."

    you "Just ignore me, Narika! Nothing to see here."

    narika "I-Idiot, I told you to leave me alone... Your thing is touching..."

    you "Hmmm... I know."

    with vpunch

    play sound s_scream_loud

    narika "AAAAH!!!"

    play sound s_splat

    "You enter her with a single thrust."

    play sound s_moans

    narika "Ah, aaah, aaaaaah..."

    "Narika pants and moans as she struggles to adjust to the size of your dick. But once again, she doesn't resist."

    you "Hmm, feels nice and tight. More than a little wet, too."

    show bg narika_waitress5 at top with dissolve

    narika "It's your fault... You're making me feel weird..."

    with vpunch

    narika "Ah, aah, aah! S-Stop moving, you idiot! I have to finish this!"

    "Narika tries to resume her cooking, but her legs are shaking so much, she is having trouble just standing up."

    you "Don't worry, just let me take care of everything. It's going to be fine."

    show bg narika_waitress4 at top with dissolve

    narika "AAAH!" with vpunch

    "You start moving your hips, slowly at first, then faster."

    "Narika is helpless as you slide in and out of her, her pussy squeezing you harder with each thrust."

    play sound s_moans_short

    narika "Ah, ah, ah!" with vpunch

    "You keep playing with her tit too, tugging on her sensitive nipple."

    play sound s_ahaa

    narika "Ah, aah, ahaaaah!!!" with vpunch

    "Narika's breathing is labored and irregular, she has completely forgotten the task at hand, her resolve is slowly crumbling."

    you "It's really easy to move inside you now... Like your body welcomes me."

    play sound s_scream

    narika "AAAAAH!!! Don't say such embarrassing things!!!" with vpunch

    play sound s_moans

    "In spite of herself, Narika starts moving her hips back, matching your pace."

    you "Oh, you're getting into it! That's nice."

    "You increase your pace, pounding her more forcefully."

    "The table shakes with every thrust, flour spilling everywhere. You don't care, and renew your assault."

    narika "Aaaaah, AAAAAAH!!!" with vpunch

    "Narika is moaning feverishly. You can tell she's about to climax."

    you "Let's take a break, shall we?"

    "An inch from cumming, you suddenly stop moving with your dick still stuck deep inside her."

    play sound s_surprise

    narika "W-What? Why did you stop?!" with vpunch

    narika "I was about to, err..."

    "Narika blushes even more, her ass slowly wriggling against your crotch."

    you "..."

    you "Just kidding."

    you "Haaa!" with vpunch

    show bg narika_waitress6 at top with flash

    "Surprising her, you slam your cock deep inside her one last time, sending both of you over the edge."

    with doubleflash

    play sound s_orgasm

    "Narika screams as you both climax at the same time."

    with flash

    narika "Aaah... Arrh... You really came inside..."

    "Narika looks defeated as she tries to catch her breath."

    you "Hey, that was pretty fun! I'd say you have a future as a naked chef."

    play sound s_sigh

    show bg narika_waitress7 at top with dissolve

    "Narika heaves a deep sigh, avoiding eye contact as you exit her sensitive pussy."

    narika "You... You're the worst..."

    "Is she really angry at you, or...?"

    scene black with fade

    $ MC.change_prestige(3)
    "Keep training Narika in different jobs until she is ready to join your brothel."

    return

label narika_masseuse():
    scene black with fade

    you "Looks like Narika is working as a masseuse today... Let's see how she's doing."

    play sound s_surprise

    show bg narika_masseuse1 at top with fade

    narika "M-Master [MC.name]? You're not supposed to be in this area... It's for customers..."

    you "Why, as the owner, I need to make sure everything is ready to welcome our dear customers! Think of it as quality control."

    narika "Quality... What?"

    you "For instance, what's that you're wearing? A one-piece swimsuit? It's not the most customer-friendly outfit..."

    narika "B-But, I had nothing else appropriate to wear..."

    you "I mean, at least you could show a little skin. Customers won't pay if they think you're just a girl in a school swimsuit."

    you "I mean, they will totally pay for that, but you can make it more interesting..."

    narika "I don't get it..."

    you "Tss... Like that, see?"

    show bg narika_masseuse2 at top with dissolve

    play sound s_scream

    narika "Eeek!" with vpunch

    you "Now, that's better! A lot more sexy, that way."

    narika blush "B-B-But... Everyone can see my... My..."

    you "Your what?"

    show bg narika_masseuse3 at top with dissolve

    play sound s_scream_loud

    narika "AAAAH!" with vpunch

    you "Haha, it's fun, the fabric is nearly disappearing in your slit! It really shows off the shape of your labia!"

    play sound s_ahaa

    narika "I-I don't know what, aaahaa, what that means!" with vpunch

    play sound s_moans_quiet

    you "It means you're beautiful down there."

    show bg narika_masseuse4 at top with dissolve

    narika "R-Really?"

    you "Sure. I have seen lots of pussies, and let me tell you, yours looks amazing."

    play sound s_aah

    narika "Is that even a compliment... Aahaa!" with vpunch

    you "Let's go inside... We can continue the lesson before the customers arrive."

    narika "..."

    play sound s_dress

    show bg narika_masseuse5 at top with fade

    $ m = MC.name[0]

    narika blush "[m]-[MC.name]... It's... So big... Can it really...?"

    you "Only one way to find out!"

    show bg narika_masseuse6 at top with dissolve

    play sound s_scream

    narika "Aaaah! [emo_heart]" with vpunch

    "Peeling her swimsuit aside, you expose her snatch, pushing the tip of your cock inside."

    you "Hmmm... You're nice and tight, just the way I remembered."

    play sound s_mmh

    show bg narika_masseuse7 at top with dissolve

    narika "You're out of control... Mmmh..."

    you "Are you going to stop me?"

    narika "..."

    you "I didn't think so."

    show bg narika_masseuse6 at top with dissolve

    play sound s_surprise

    narika "AAAAH!" with vpunch

    "You start rocking your hips, slowly sliding your dick in and out of her."

    play sound s_moans_short

    narika "Ah, ah, ahh... Mmmmh..."

    "Narika is breathing heavily, trying to adjust to your size."

    narika "Is it... All in...?"

    "You can hear curiosity in her voice, in spite of herself."

    you "Oh no, not yet. We're only halfway there."

    narika "N-No way-"

    play sound s_scream_loud

    narika "AAAAAAH!!!" with vpunch

    you "Now, it's all in."

    narika "You're too big... I can't..."

    you "What is it, Narika?"

    "Narika's pussy squeezes your cock tight, but you keep pushing in, stretching her pussy walls from the inside."

    narika "Aaaaaaah!" with vpunch

    you "What, can't take it? Are you too soft?"

    show bg narika_masseuse8 at top with dissolve

    narika "I'm not... Soft..."

    you "Oh yeah? You think you can keep up?"

    narika "I, uhng..."

    "She grits her teeth, but her eyes defy you to go further."

    "You push on, enjoying the way her pussy muscles struggle to expel you as you pump your shaft inside her."

    play sound s_moans

    narika "Ah, ah, ahh, aaah, aaaaaah!" with vpunch

    "In spite of her inexperience, Narika seems determined to keep up. She even starts to rock her hips slightly, slowly matching your rhythm."

    you "Hmmm, that's more like it!"

    "You hear some noise coming from the corridor. It seems some early customers are already beginning to show up."

    you "Hear that? I think some customers may be on the verge of walking in on us."

    show bg narika_masseuse7 at top with dissolve

    play sound s_surprise

    narika "N-No! They can't see me... Like that!"

    you "And why not? I told you it would do you good to show more skin. It's kind of an extreme version of that."

    narika shy "B-B-But... We're... Making love!"

    you "Hahahah, we're just fucking, Narika, it's different."

    narika "F-Fucking?"

    you "Yup."

    narika "B-B-But, isn't it something only lovers do?"

    you "Oh, sweet child... Anyone can fuck anyone, you shouldn't be so uptight about it."

    narika "S-So... We're not... Lovers?"

    you "Of sorts, if you want to call it that... But first and foremost, we're just having fun."

    narika blush "I-I'm not... Aaaah!" with vpunch

    "You pick up the pace, thrusting harder inside Narika."

    play sound s_moans

    narika "Ah, ah, aah!" with vpunch

    "Her pussy is gushing juices now, as she tries to match your pace."

    you "Don't even bother denying it, your body is craving for more."

    narika "..."

    you "You know, the first time I saw you, I knew you were hiding your true feelings behind a cold facade. I knew you had to a lot going on under the surface."

    narika "Ngh..." with vpunch

    "You pound Narika's pussy as you continue your monologue."

    you "I could see you were a girl who was craving for attention, a little princess who wanted to be pampered. But there is another side to you."

    narika "Ah, aah, ahh! Aaaaaaah!" with vpunch

    "You feel Narika's pussy clenching harder, signaling that she's close to climax."

    you "Oh, look, I think the customers are coming in!"

    narika "N-No! I don't want them to see me like that! A-Aaah!" with vpunch

    show bg narika_masseuse6 at top with flash

    "Narika struggles to regain control of herself, but her body betrays her as the mere thought of being found out sends her over the edge."

    show bg narika_masseuse9 at top with doubleflash

    play sound s_orgasm

    "Narika moans loudly, her pussy tightening around your cock in a series of spasms, sending you over the edge as well."

    show bg narika_masseuse10 at top with flash

    you "Bwahaha, just kidding, it was only Sill who's checking if the rooms are clean..."

    narika "Aaaah..."

    sill sad "M-Master??? What are you doing? I just washed that bench less than an hour ago!!!" with vpunch

    you "Well, it's good you got some practice, because you need to do it all over again!"

    you "And on the double. Customers will pour in any minute now."

    sill "And what about her? Is she going to help?"

    you "Narika here? Oh no, she's been through enough for today. Leave her be."

    "You remove your cock from Narika's pussy, gently laying her down on the bench before leaving."

    sill "Eeewww! And now there's cum leaking all over the place!" with vpunch

    scene black with fade

    $ MC.change_prestige(3)

    "Keep training Narika in different jobs until she is ready to join your brothel."

    return

label narika_geisha():
    scene black with fade

    narika shy "Come, Sir, err, I mean, dear customer..."

    narika "Please follow me to the chashitsu, the tea house... The tea ceremony will start shortly."

    "Ruffian" "Oy! I don't care about your stupid ceremony, kid! Shalia spit on it!"

    show bg narika_geisha1 at top with dissolve

    play sound s_dress

    "Ruffian" "Is this a whorehouse or what? Are you just here to serve tea and give flowery speeches?"

    play sound s_surprise

    narika blush "S-Sir, what are you doing??"

    "Ruffian" "What's it look like I'm doing? Checking the quality of the goods, that's what!"

    narika "B-But, I'm just a maiko in training... We have a no-touching policy..."

    "Ruffian" "Yeah, fuck that. You think that means anything in a place like that?"

    narika "But Sir..."

    "Ruffian" "Shut the fuck up, you little slut! You don't want me to hurt your pretty little face, do you?"

    narika "..."

    show bg narika_geisha2 at top with dissolve

    narika "(Damn, I could snap that fool's neck in a split second... But I need to behave, I'm only just starting to find my footing here...)"

    "Ruffian" "Eheheh, I like them small titties..."

    narika "(I just have to endure this for now... At least he's not...)"

    play sound s_dress
    pause 0.2
    play sound2 s_surprise

    show bg narika_geisha3 at top with dissolve

    narika "Ah!" with vpunch

    "Ruffian" "Ah yes, show me more..."

    narika "S-Sir!"

    "The gruffy customer tugs at her kimono, exposing her underwear. His grabby hands resume fondling Narika."

    narika "(This is bad... That guy is trouble...)"

    "Ruffian" "Eheheheh, what's that? Such plain underwear... You sure you're a hooker?"

    show bg narika_geisha4 at top with dissolve

    narika "I-I'm not!!!" with vpunch

    "Ruffian" "Whatev's, girly... I'm enjoying touching your hot body just the same..."

    narika "(W-Why is it that I can't shake that guy's off? I can kill a dozen ninja in a fight, but when big strong hands are on me... I feel powerless to stop it?)"

    "Ruffian" "Your nipples are perking through your bra... Eheh, aren't you a sensitive little kitty?"

    narika "Kkkh..."

    play sound s_dress

    show bg narika_geisha5 at top with dissolve

    "The customer unzips his pants, sliding his erect cock between Narika's legs."

    play sound s_scream

    narika "N-No!!! Sir! That's going too far!!!"

    "Ruffian" "Oh come on, don't be such a buzzkill, Miss! You knew this was coming..."

    narika "(This is really bad... I need to do something before this escalates any further...)"

    "Ruffian" "We gots all the time in the world... I'm 'a make you a real woman."

    narika "(I've always refused to use {i}that kind{/i} of Kunoichi techniques, but... This is a force majeur...)"

    "Slowly, deliberately, Narika contracts her pussy, her lips clenching the ruffian's dick through the panties' fabric."

    "Ruffian" "Ohohohoh!!! What is that! It feels incredible..."

    "Ruffian" "How are you even doing that? I must have underestimated you..."

    narika "(So... My instructor told me I could use this to deliver the finishing blow... It was all just theory, though, I've never even used such a technique...)"

    narika "(Forgive me, Master [MC.name], for what I'm about to do, but I must end this now...)"

    "Narika steels her resolve, and activates the secret technique."

    narika angry "HA!!!" with vpunch

    play sound s_splat

    with flash

    "Ruffian" "OW!!! OHOHOHOHOHOHOH!!!"

    show bg narika_geisha6 at top with doubleflash

    "The customer's dick erupts like a geyser, smearing Narika's legs and panties with thick semen."

    with flash

    "Ruffian" "In-In..."

    "Ruffian" "INCREDIBLE!!!"

    "Ruffian" "I've never felt anything like this! I thought I was about to die, and then it was so good!"

    show bg narika_geisha7 at top with flash

    narika "(Oh no... Did I mess up that technique? Or did I misunderstand the instructor when she told us it would 'finish' him?)"

    "Ruffian" "Ohohoh, I'm in heaven now..."

    narika "D-Dear customer, I'm glad you had your... fun. Now, I need to wash, can you please let me-"

    play sound s_dress

    show bg narika_geisha8 at top with dissolve

    pause 0.2

    play sound s_scream

    narika "AAAAH!!!" with vpunch

    "The customer's callous hands rip off her panties and bra."

    "Ruffian" "Oh no, we're just getting started... You're all mine now! I'm going to enjoy that bewitching pussy night and day from now on!"

    narika "N-No, stop it! I will call my... My boss..."

    if MC.playerclass == "Warrior":
        "Ruffian" "What, that loser, the old washed-up veteran? I can take ten guys like him any day! I bet he's never even been in a real fight."
        $ s = s_punch
    elif MC.playerclass == "Wizard":
        "Ruffian" "That effeminate loser with his robes and his walking stick? You think I'm scared of the tacky magic tricks he uses to impress the simple-minded morons?"
        $ s = s_fire
    elif MC.playerclass == "Trader":
        "Ruffian" "What, that chatty braggart and his pet lizard? He reminds me of a loser kid I was bullying, I pushed him down into the latrines and nailed his pet to the door..."
        $ s = s_roar

    "Ruffian" "If he dares to interrupt, I'll give him the hiding of his life. I'll screw down his head and shit down his neck. I'll-"

    play sound s_whistle

    you "Hey, dickhead." with vpunch

    "Ruffian" "Uh?"

    you "Get your filthy hands of my girl. The sign says 'NO TOUCHING'..."

    if MC.playerclass == "Warrior":
        play sound s_punch
        "*PUNCH*" with vpunch
        "Ruffian" "Ouch!!!"

    elif MC.playerclass == "Wizard":
        play sound s_fire
        "*BLAST*" with flash
        "Ruffian" "Aaaarh!!!"

    elif MC.playerclass == "Trader":
        play sound s_roar
        "*ROAR*" with vpunch
        "Ruffian" "G-G-Get that thing away from me!!!"

    you "... without paying. It says, 'NO TOUCHING {i}without paying{/i}'."

    "Ruffian" "GRRR... So you wanna dance, motherfucker?"

    play sound s_sheath

    "The customer takes out a nasty looking knife from Arios-knows-where."

    you "Narika, please."

    narika "W-With pleasure, Master..."

    play sound s_punch
    pause 0.3
    play sound2 s_punch
    pause 0.2
    play sound3 s_punch
    pause 0.1
    play sound s_punch
    pause 0.1
    play sound2 s_punch
    pause 0.2
    play sound3 s_punch
    pause 0.1
    play sound s_punch
    pause 0.3

    "*punch* *kick* *slap* *slap* *elbow* *roundhouse kick*" with vpunch

    play sound s_wscream

    "Ruffian" "AAAAAAAAaaaaaaaaaaa{size=-4}aaaaaa{size=-4}aaaaaa{size=-4}aaaaaahhh" with vpunch

    "The customer is kicked high above the rooftops, disappearing into the distance until he is just one tiny spot among the night's stars."

    you "Are you okay?"

    narika "..."

    narika "That nasty man... He touched me, he... did his thing... It felt so gross, and weird..."

    narika shy "I... I even peed myself... *voice breaks*"

    you "Oh, honey... It's not pee..."

    "You insert an expert finger inside her exposed snatch, scooping up a bunch of love juice."

    you "I can't believe you... Did being assaulted turn you on, or giving is it beating this guy to a pulp?"

    narika blush "..."

    narika "Both..."

    you "Hahaha, at least you're honest."

    you "I can't really leave you like this, though, can I?"

    narika "..."

    you "Let's make the best of this unexpected foreplay."

    show bg narika_geisha9 at top with fade

    play sound s_mmh

    narika "Oh, Master..."

    you "I think you're getting the hand of this place, Narika."

    narika "B-But... It's all so new to me... The girls, the outfits, the customers... The s-sex..."

    you "And yet look at you, you're moving your hips in rhythm with mine..."

    narika "I c-can't help it, it's like there's this fire inside me... I don't understand it..."

    you "You like sex, Narika, it's only natural. It's the most pleasurable thing in the world. I can guide you down the right path."

    narika "I-Is it like... Kunoichi training?"

    you "Oh, it's a lot more fun than that."

    narika "..."

    "Increasing your pace, you keep fucking her tight pussy, and she hangs onto you for dear life."

    show bg narika_geisha10 at top with dissolve

    play sound s_scream

    narika "Oh! ah! Aaah!" with vpunch

    play sound s_moans

    narika "Oh yes, yes... That's the spot... [emo_heart]"

    "Spreading her legs wider, you find just the right angle, sending shivers down her spine every time you pound into her."

    narika "Aaaaah!!!" with vpunch

    narika "Oh no!!! If you do that, I will..."

    show bg narika_geisha11 at top with flash

    play sound s_screams

    narika "OH!!! AAAAH!!! AAAAAH!!!"

    play sound s_orgasm_fast

    narika "You both cum at the same time, Narika clinging to you as you spurt your warm seed inside her."

    show bg narika_geisha12 at top with flash

    narika "A-Amazing..."

    you "Wow... You're okay?"

    narika "I didn't know... There was such a... feeling..."

    you "This is just the beginning. If you pay attention to my teachings, soon you will..."

    you "Narika? Narika?"

    "It looks like Narika passed out in the middle of your lecture."

    "You are relieved to hear her snore, though. It's just fatigue."

    "Carrying her back to her room, you reflect back on her progress since you brought her here."

    you "I'm surprised how well she's adjusting. She really is a quick learner."

    scene black with fade

    $ MC.change_prestige(3)

    "Keep training Narika in different jobs until she is ready to join your brothel."

    return

label narika_dancer():
    scene black with fade

    play sound s_crowd_cheer

    "Customers" "Whoohoo!!! *Cheers*"

    narika school "Thank you, thank you..."

    man "The show was amazing! Can you do the split once more?"

    man2 "And the cartwheel! With that short skirt of yours, it was just... Hmmm..."

    "The customers really enjoyed Narika's dance show."

    narika "Fufufu, thank you, my adoring fans! *blush*"

    narika "(I really am getting quite popular now...)"

    narika "(I've been here for a while already. I hear there are customers that come just for me...)"

    narika "(Why does it make me feel so... Tingly?)"

    man2 "Here, Narika-chan! I brought you flowers!"

    narika "Flowers? For me? Oh, thank you... *swoons*"

    man "Can I get your autograph?"

    "Third man" "I'll buy your used underwear! Name your price!"

    narika "(Gee, I have never been this popular with boys, not even in school... It's intoxicating...)"

    "Fans" "Narika-chan, we are your biggest fans! *together*"

    narika "Ahaha... Would you like me to give you a tour backstage?"

    "Fans" "YES!!!" with vpunch

    man "A tour with Narika-chan! This is the best day of my life!!!" with vpunch

    narika "(Why are my fans so creepy? But I have to entertain them... That's the price of being an idol I guess.)"

    "Narika led the three guys to the changing room. She didn't know what to make of the growing tingling sensation that was coursing through her body."

    with fade

    man "Narika-chan, can I ask you something?"

    narika "Sure, sure, ask me anything, I'd be nothing without my fans..."

    narika "(Why am I saying these corny idol lines all of a sudden?)"

    man "Can you sign your autograph on my skin? You know, like a tattoo that comes from Narika-chan?"

    narika "Oh, well, why not. Let me find a pen..."

    play sound s_dress

    show bg narika_dancer1 at top with dissolve

    narika blush "W-What are you doing?"

    man "You said you would sign your autograph on my body, right? I want it here."

    "Other men" "Do it, Narika-chan! Do it!"

    narika "B-But... I can't, err... write on it... I mean, it's too soft..."

    man "Oh, right!"

    man "You need to help me get it harder first."

    "The man guides Narika's hand towards his cock. She is surprised at his boldness, but also aroused."

    narika "W-Well, I suppose I can help out a fan..."

    "Narika starts stroking the man's cock, under the watchful eye of the others."

    man2 "Oooooh! I'm so jealous!"

    man "This is so good! Aah!!!" with vpunch

    show bg narika_dancer2 at top with dissolve

    "Acting even more bold, the man pushes his cock in Narika's face, brushing the head against her lips."

    narika "!!!" with vpunch

    man "Please, Narika-chan, lick it a little... It would make me so happy..."

    narika "(This is getting out of hand... Literally...)"

    "In spite of herself, Narika soon finds herself licking the tip of the man's dick, tasting his sweat and pre-cum."

    narika "(W-Why do I allow myself to be debased by these fans? And why does it feel so... hot?)"

    man2 "Look at that!!! Narika-chan is really doing it!"

    "Third man" "Oh no, am I dead? Am I in heaven?"

    man "Oh, Narika-chan, now I can die a happy man... I-"

    with flash

    "Aaaah!!!"

    show bg narika_dancer3 at top with doubleflash

    "As Narika wraps the man's cock with her lips, he cums suddenly, spilling a wad of salty cum in her mouth."

    narika "Hnnng..."

    show bg narika_dancer4 at top with flash

    "Gasping for air, Narika lets a mix of drool and cum drip down from her lips."

    man "T-This is much better than an autograph! Thank you, Narika-chan!"

    narika "Uhn... You're... You're welcome..."

    show bg narika_dancer5 at top with dissolve

    man2 "What about us? It's our turn now!"

    "Third man" "Yes! It wouldn't be fair to do it just for them!"

    narika "(I... I can't be seen playing favorites with my fans, it would be a bad look...)"

    narika "F-Fine... Just wait in line, or something..."

    man2 "Me first!" with vpunch

    "Third man" "No, me!!!" with vpunch

    narika "Gee, calm down, boys... I've got two hands, I'll do my best to help you both..."

    show bg narika_dancer6 at top with dissolve

    narika "Here, happy now?"

    man2 "Oooh, this is good!!!"

    "Third man" "I don't believe it! This is even better than the time I got the special edition calendar of BK48!"

    man "I'm ready to go again! Show me something to get me started."

    play sound s_dress

    show bg narika_dancer7 at top with dissolve

    "The man forcefully lifts Narika's top to reveal her tits, but she is beyond caring. She already started licking the other customers' cocks."

    narika "Please, dear fans... Look at my body... And enjoy yourselves..."

    man2 "Oh, Narika-chan, your tits are beautiful!!!"

    "Third man" "She's licking it! I'll never wash my dick again!!!"

    "The fire in Narika's body is now in full heat, and she doesn't resist the turn of events."

    narika "(Why am I doing this?)"

    narika "(Oh, who am I kidding, it's just so fun...)"

    show bg narika_dancer8 at top with flash

    "As Narika licks and sucks the customers, they release their cum on her face and chest."

    with doubleflash

    man2 "Oh, Narika-chan! You are so beautiful with cum all over your face!!!"

    "Third man" "I could watch this forever! I'll burn my eyes out after they have been so blessed!!!"

    narika "Please don't..."

    man "I can't take it anymore! Narika-chan, I'll..."

    show bg narika_dancer9 with doubleflash

    "The customer cums on Narika's face and hair, splashing her face with his seed."

    "As the cum drips down Narika's body, she feels a sense of liberation, of letting go of her inhibitions."

    show bg narika_dancer10 with dissolve

    narika "(I think Master [MC.name] was right, I needed to be shown the way... But now that I am on the path, I can keep walking it on my own.)"

    "Narika's journey of self-discovery has only begun, and she's ready for more."

    narika "(So far I've used my body for fighting and strength... But it can also bring joy and pleasure, to me and to others.)"

    narika "(Isn't that a better calling?)"

    scene black with fade

    $ MC.change_prestige(3)

    "Narika is now fully trained in all jobs. Please wait for events to unfold."

    $ calendar.set_alarm(calendar.time+1, StoryEvent("narika_broken", type="night"))

    $ calendar.set_alarm(calendar.time+56, StoryEvent("narika_fans_return", type="night"))
    return

label narika_fans_return(): # runs in a loop until the event happens

    python:
        for girl in MC.girls:
            if girl.pack_name == "Narika Shihoudou" and girl.original and girl.job == "dancer":
                break
        else:
            girl=None

    if girl:

        "Narika was just ending her dancing shift when she heard a familiar voice call out her name."

        man "Narikaaaaaa-chan!!!"

        narika school "?"

        man2 "It's us!!! Your biggest fans! Do you remember us?"

        "Narika gives them a blank stare."

        "Third man" "You showed us around backstage! You gave us, erm... Special service!"

        narika "Oh, it was you guys!"

        show bg narika_dancer10 at sepia
        with flashbackin

        narika "(That was the moment... I realized I could do this...)"

        man "It was awesome, Narika-chan! I haven't slept for weeks, daydreaming about this!"

        man2 "I masturbate every day thinking about it! I even made a clay figure of you, and..."

        narika "Enough, enough! (Gee, you idol fans are still as creepy as ever...)"

        "Third man" "Would you show us around backstage today? Pretty please?"

        man "We'll pay extra!"

        narika "Well..."

        "Together" "Narika-chan, we beg you!!! *down on their knees and hands, imploring her*"

        narika "*sigh* All right, fine... Just follow me. But no inappropriate touching, okay?"

        scene black with flashbackout

        show bg narika_dancer9 at top with doubleflash

        narika blush "Eeeek!!! It's in my hair!"

        narika "So much for me saying 'no touching'..."

        $ MC.change_gold(300)

        show bg narika_dancer10 at top with flash

        man "Thank you so much, Narika-chan!!!"

        man2 "Now I can masturbate to this for many more months!"

        "Third man" "But, Narika-chan..."

        narika "What..."

        "Third man" "I heard the idols from BK48, they let their fans go all the way you know..."

        man "It's true! I heard they sometimes treat several of their fans at once!"

        man2 "Friends, don't you dare to compare Narika-chan to these BK48 sows..."

        narika "All the way? Hmph, do they think it makes them better or something? I bet they just lie there like a dead tuna..."

        man "You're right, you don't have to do it to be awesome!"

        man2 "Yes, exactly! You're perfect as you are, even if you can't perform at their level!"

        "Third man" "Sure, I mean... BK48 is something else, it's not a fair comparison..."

        narika angry "HOLD ON A MOMENT!!!" with vpunch

        narika "You lowly worms think I'm not on par with these fat vulgar bitches from BK48?!?" with vpunch

        man "N-N-No..."

        man2 "W-We wouldn't dare..."

        "Third man" "I think we're going to now... (She's scary!!!)"

        narika "YOU THREE STAY RIGHT HERE!!!"

        play sound s_dress

        show bg narika_dancer11 at top with fade

        man "N-Narika-chan, you don't have to force yourself..."

        narika "Hmph. I'm not forcing myself, I'm just doing my duty as an idol. You can't leave here thinking someone else gives better fan service."

        man2 "Narika-chan, you're so cool! [emo_heart]"

        "Third man" "Ooooh, Narika-chan, my heart is going to beat out of my chest!!"

        narika "Please, dear fans, look at me and only me! Your... Queen."

        man "O-Of course..."

        man "Queen Narika!!!"

        man2 "I am so lucky to be in the presence of the divine!!"

        "Third man" "Aaaah, I'm going to faint!"

        show bg narika_dancer12 with dissolve

        "Narika slowly lowers herself on the customer, his cock disappearing inside her wet pussy."

        man2 "OH MY GOD!!!" with vpunch

        "Third man" "I can't believe my eyes! Narika-chan is truly a goddess!!!"

        narika "Ah, ahh! Don't start moving until I tell you to!"

        man "Y-Yes, my Queen! I will obey!"

        narika "That's right, you will obey me! Now thrust your hips! Hard!"

        man "As you wish, Queen Narika!" with vpunch

        play sound s_mmh

        show bg narika_dancer13 with dissolve


        narika "Hmmm, yes..."

        "The man starts pounding Narika who bounces up and down his cock, while the others look at her with fascination."

        narika "(I could get used to this...) Fufufu..."
        man "I'm in heaven... I... Ugnh..."

        show bg narika_dancer14 with doubleflash

        play sound s_scream

        narika "AAAAH!!! [emo_heart]" with vpunch

        "The man cums suddenly, filling Narika's pussy with his seed."

        man2 "It's so hot!!! I can't hold it any longer!"

        "Third man" "Me neither! This is beyond my wildest dreams!!!"

        show bg narika_dancer15 with doubleflash

        man2 "*grunt*"

        "Third man" "Aaaarh!"

        "The men all cum together on Narika's body and face."

        show bg narika_dancer16 with flash

        narika "Aaaaah, you guys came so much!"

        narika "(The smell of men's cum... It's overpowering...)"

        man "Am I dead? I think I'm dead..."

        man "It's okay, I can die happy now... *pass out*"

        man2 "I-I'm spent..."

        "Third man" "But it's not fair! How come he got to cum inside you, when I didn't?"

        narika "Well, he was first in line..."

        "Third man" "But what about me?"

        narika "He's passed out now, you're going to have to wait for him to wake up..."

        narika "His dick is still stuck inside me."

        "Third man" "But I don't want to wait another second! I'm hard as fuck, Queen, it's painful!"

        narika "Then wh-"

        play sound s_splat

        show bg narika_dancer17 with dissolve

        play sound s_scream_loud

        narika "AAAAAAAH!!!" with vpunch

        narika "Y-You bastard... You just put it in my asshole with even asking..."

        "Third man" "I-I'm sorry, I don't know what came over me, Queen..."

        "Third man" "I'll come out right away... This was so inappropriate, I don't know how you can forgive me..."

        narika "Ah, aah..."

        "Narika moans as he tries to remove his dick."

        "Third man" "Q-Queen? I can't remove my dick? It's too tight!"

        show bg narika_dancer18 with dissolve

        narika "That's right. Because I won't let you."

        "Narika is using the muscles of her ass to clench onto the man's dick."

        narika "I have yet to be satisfied, as that other chump came too early."

        narika "So you're going to make me cum now..."

        "Third man" "I-I'll do anything for you, Queen Narika! Just tell me what I can do!"

        narika "I want you to fuck me in the ass. Do it now!"

        "Third man" "Yes, my Queen! As you wish!" with vpunch

        play sound s_mmh

        with vpunch

        "Narika's body rocks back and forth as the customer pushes his cock in and out of her asshole."

        play sound s_aah

        narika "Aaah, yes... [emo_heart]" with vpunch

        play sound s_moans

        "She scoops some cum off her body and licks it off her fingers as she looks back at the customer."

        man2 "A-Amazing!!! This is the power of a true idol!!!"

        "Third man" "O-Of course! No one in the world can compare to Narika-chan!"

        "Third man" "OOOOOOH!!!!" with vpunch

        play sound s_orgasm

        show bg narika_dancer19 with dissolve

        narika "Ooooh!!! YES!!!" with doubleflash

        "The customer cums, releasing his seed inside Narika's ass, while she reaches her climax as well."

        show bg narika_dancer20 with flash

        "Third man" "*pant, pant*"

        "The customers are in shock, looking at her as if she was a goddess."

        "Narika feels a sense of accomplishment, as if she just conquered an impossible challenge."

        narika "(I can please any number of men... Nothing is beyond my power now...)"

        narika "I'll become the best idol ever and I'll make all of my fans happy!!!"

        "Customers" "Yes, my Queen!!!" with vpunch

        $ MC.change_gold(1200)
        $ girl.change_mood(100)
        $ girl.raise_preference("group", 500)
        $ girl.change_rep(5)

        scene black with fade

        man "*waking up* Ugh... Did I miss anything?"

        $ MC.change_prestige(game.chapter)

        $ clear_event("narika_fans_return")

    return

label narika_broken:

    scene black with fade
    show expression brothel.master_bedroom.get_pic() at top
    with dissolve

    show narika normal with dissolve

    narika "Master, you wanted to see me?"

    you "Yes, I wanted to congratulate you on your progress so far. I think you are now ready to join us."

    narika blush "Well, I didn't know what to expect at first... But I think I can hold my own."

    you "You sure can. The girls said you've been good help."

    narika "Well, I've tried all the side jobs... but I can't just be a supporting actress. I need to lead!"

    you "Meaning?"

    narika "There's one last job I haven't tried... The real stuff. You know."

    you "Right."

    menu:
        you "In that case..."

        "I will try you out myself":

            $ renpy.block_rollback()

            you "You're going to welcome me as if I was a customer, and give me the best service you're capable of."

            you "If I am satisfied with you, I will let you join [brothel.name]."

            narika "O-Okay..."

            scene black with fade
            show bg narika_sex1 at top with dissolve

            narika blush "W-Welcome, dear customer..."

            you "Don't be so formal... You can call me... Daddy."

            narika "D-Daddy? Why?"

            you "Many customers ask for this. Don't you know step-relations are all the rage now in smutty dime novels?"

            narika "Alright... Welcome home, Daddy."

            you "Still not wearing a bra... I like that."

            narika "Do you like my titties, Daddy?"

            you "Sure, hehehe..."

            "You pinch her nipples."

            narika "Ah!" with vpunch

            you "Perky as always... Let's check what else you have for me."

            play sound s_dress

            show bg narika_sex2 at top with dissolve

            "You remove her panties, spreading her knees apart to get a good view of her pussy."

            "Her pussy is already wet."

            you "It looks like you've been a naughty daughter..."

            "Narika is embarrassed to be exposed in such a manner, but also feels a sense of excitement."

            narika "S-Sorry, Daddy... I was thinking about you all day, and got turned on..."

            "Narika spreads her legs wider, inviting you to get closer."

            narika "I-If you look at me like this, I'll get even more excited..."

            you "Hehehe, what a dirty daughter. I'm going to have to punish you."

            "You lower your head towards her pussy and start licking it."

            show bg narika_sex3 at top with dissolve

            narika "Aaaaah!!! [emo_heart]" with vpunch

            you "Just as I thought, you're leaking all over the place, you dirty girl!"

            narika "I-I'm sorry, Daddy! It's just... It's my first time..."

            you "Don't lie, Narika, customers won't like that."

            narika "I-I mean, it's my first time... As a... A..."

            you "Yes?"

            narika "Whore..."

            "She lets the word roll off her tongue, as if it had a deeper, almost mystical meaning."

            "As the words come out of her mouth, Narika feels as if she has been reborn."

            you "I like the new you... Let me show you my appreciation."

            show bg narika_sex4 at top with dissolve

            play sound s_aah

            narika "Aaaaah!" with vpunch

            "You resume licking her pussy, while she leans back and grabs the sheets with her hands."

            "Spreading her pussy lips apart, you push your tongue inside, tasting her sweet love juice."

            narika "Daddy! Oh, Daddy!"

            play sound s_ahaa

            "Narika is trembling, close to cumming already."

            narika "Ahhh! I-I'm too sensitive, Daddy!"

            you "Let's not rush to the finish line..."

            "You stop, and she looks at you with a hint of disappointment."

            "Before she can beg you to continue, however, you push her down on the bed."

            show bg narika_sex5 at top with dissolve

            you "I think my slutty daughter's pussy is ready to take my dick..."

            narika "Y-Yes, Daddy! Please use me as you like!"

            play sound s_dress

            "You pull out your cock and it springs to attention."

            you "Make sure to satisfy me fully, and you will have a place of honor among my girls."

            narika "S-Sure, Daddy. I'll do my best."

            "You put your cock between her legs and start thrusting."

            show bg narika_sex6 at top with dissolve

            play sound s_mmh

            narika "Oh, Daddy, Daddy!!!"

            you "Your pussy is so tight, and yet so easy to move into..."

            "You grab her ass, pulling her towards you as you lodge your cock deeper inside."

            show bg narika_sex7 at top with dissolve

            play sound s_aaah

            narika "Oh, Daddy... You're so big..."

            "Her pussy is clenching around you as she bites her lips."

            play sound s_moans

            "Narika is moaning, looking at you as she gets filled up with your dick."

            you "Narika, my slutty daughter... You feel so good!"

            you  "I'm going to have to fuck your pussy now... Don't mind me if I'm being rough."

            narika "Daddy, I want it rough..."

            "You start fucking her in earnest, pushing your cock in and out of her pussy."

            show bg narika_sex8 at top with dissolve

            play sound s_surprise

            narika "Aaaah!!!" with vpunch

            narika "Oh yes, Daddy, just like that!!!"

            "You fuck her hard for some time, but then you slow down your pace."

            narika "(It feels so good, but... Why is he holding back?)"

            "She looks at you and realizes what she has to do."

            narika "Daddy, you're teasing me... Please don't hold back on me..."

            you "You can do better than that... Don't just take it."

            you "You're a whore now, remember? Act like it!"

            "You pick up the pace again, making her moan harder."

            narika "Ah, Daddy!!!" with vpunch

            "She starts rocking her hips back and forth, making your cock hit her deeper regions every time you push into her."

            narika "Take me, Daddy! Fuck me hard!" with vpunch

            "You start feeling the onset of your orgasm."

            you "I'm getting close, Narika. Do you want to be filled by my cum?"

            narika "Yes, Daddy! Please fill me up!"

            you "Then you have to deserve it. Your move."

            "You stop pounding her, waiting with your dick buried halfway in."

            "Narika takes a few moments to collect herself, then starts fucking you on her own."

            play sound s_scream_loud

            narika "AAAAAH!" with vpunch

            "She slams her ass against your crotch, taking your dick deeper every time."

            "She uses all of her muscles to make you feel good. You can feel her pussy walls tightening around your shaft."

            play sound s_scream

            narika "Oh, Daddy! I'm gonna cum!" with vpunch

            with flash

            play sound s_orgasm

            "She orgasms, squeezing your dick with all of her might, sending you over the edge as well."

            you "Here it comes, Narika... Take it all!"

            show bg narika_sex9 at top with doubleflash

            "You spray your seed inside her pussy, reaching her deepest places."

            with flash

            "The sensation of your hot cum makes Narika orgasm again, milking every drop out of you."

            show bg narika_sex10 at top with dissolve

            play sound s_sigh

            narika "I came... Twice..."

            you "On your first day as a whore..."

        "I will summon some customers":

            $ renpy.block_rollback()

            $ cust = rand_choice(get_available_populations()).get_rand_name().capitalize()

            you "Your test will involve real customers. are you ready for it?"

            narika "..."

            narika blush "Yes, I am."

            you "Alright. Let me fetch some."

            scene black with fade

            "You ask Sill to find you two of the ugliest customers in the brothel."

            sill "Okay, Master [MC.name], but... Why?"

            you "I want to make sure that former spoiled little princess is ready to serve anyone."

            you "Plus, I have a feeling she might like some additional humiliation..."

            play sound s_maniacal_laugh
            you "Bwahahaha!!!"

            $ MC.good -= 2

            sill "Err... Okay..."

            show bg narika_broken1 at top with fade

            narika "Ooh, aah, aaah! Mister, you're so rough!!!" with vpunch

            "[cust]" "Osh, I like how you move, you little shlut!"

            narika "(That guy is old, fat and smelly... And he speaks with a slur...)"

            narika "(And he fucks me like I'm a dirty street hooker...)"

            narika "(Why am I getting so turned on by this???)" with vpunch

            "[cust]" "Kish me you bitshh!"

            show bg narika_broken2 at top with dissolve

            "The customer licks the outside of Narika's mouth with his slithering tongue."

            narika "(Oh gosh, his breath smells like cheap alcohol and clove cigarettes... Disgusting...)"

            "Narika leans into the kiss, intertwining her tongue with the customer's, swallowing his dirty saliva."

            "She gets turned on by this humiliating act, and starts rocking her hips back and forth faster."

            "[cust]" "Oh, nishe... I really enjoy when you squeeje my cock like thish..."

            show bg narika_broken3 at top with dissolve

            narika "Ah, aah, ooh!!!" with vpunch

            "The customer grabs her ass, squeezing it hard as he keeps pounding her pussy."

            "She gets more and more aroused as the customer fucks her like a piece of meat."

            "[cust]" "You like the bells I put on your nippies? It jingles every time I shlam my cock into you, hahaha!"

            "Narika's face is red, and she is breathing heavily as he fucks her like a wild animal."

            play sound s_aaah

            narika "Aaah, ohh, aaaah!!!" with vpunch

            "Other customer" "Oy! The big man said I was gonna get a turn too! I'm still waiting!"

            narika "Aah, sorry... Aah..."

            "Other customer"  "I ain't gonna wait forever. Ready or not, here I come!"

            show bg narika_broken4 at top with dissolve

            play sound s_scream

            narika "NGGGH!!!" with vpunch

            "Other customer" "Oy, I'm coming in. don't mind me, eheheheh..."

            "The second man pushes his cock against her asshole, forcing his way inside."

            "The first man doesn't let it stop him, however, as he keeps pounding her pussy."

            narika "(This man is a pig just like the other one... But his dick... is so big...)"

            narika "(They're both so rough with me... I've never had anything like this happen to me before...)"

            "The second man's dick is so large that it struggles to enter her asshole."

            play sound s_splat

            "Finally, it gives way, and Narika is almost torn apart as the large man enters her from behind."

            play sound s_scream_loud

            narika "AAAAAH!!!"

            play sound s_chimes

            "The force of the insertion makes the bells on her nipples ring out loud."

            show bg narika_broken5 at top with dissolve

            play sound s_scream_loud

            narika "Oooh, it hurts!!!" with vpunch

            narika "(I can take pain... But this is so intense... My mind is going blank!)"

            "The two men start thrusting their cocks inside her, one filling up her pussy while the other is pushing its way inside her ass."

            play sound s_moans

            "She can't keep up with the pleasure she is feeling, and her moans of apin and pleasure start filling the air."

            "The first customer grabs her hair, pulling it back and forcing her to look at him."

            "[cust]" "I'm going to fill you up with semen. You could father my child, you lucky shlut! Eheheh..."

            narika "(T-Thank the gods for Sill's contraception magic...)"

            "Other customer" "I'm going to make your ass pregnant too, hahahaha!"

            narika "(Ow... They're as dumb as they are ugly...)"

            narika "(I'm being treated like a broken fucktoy by these disgusting men... And yet...)"

            play sound s_scream

            narika "I'm enjoying this... So much!" with vpunch

            "Other customer" "Unbelievable! Hear that, cousin?"

            "[cust]" "Yesh!!! Time for the big finissh!" with vpunch

            show bg narika_broken6 at top with flash

            "[cust]" "UUUGH!!!"

            "Other customer" "OHOHOH!" with doubleflash

            play sound s_orgasm

            narika "AAAAAH!!!!" with flash

            "Narika climaxes as the two men spray their load inside her pussy and ass."

            "Her orgasm makes her pussy squeeze the dick inside her, making the pig man cum harder."

            "The two men's faces are red from the strain, their smelly breath hot on Narika's neck."

            show bg narika_broken7 at top with dissolve

            narika sad "(Did all of this really happen...)"

            "She can feel their semen leak out of her holes."

            narika "(It's so warm, so disgusting... I love it...)"

            "[cust]" "I've been with a lot of whorjes in my day... In fact, I've only been with whorjes."

            "[cust]" "But you're the real shtuff."

            "Other customer" "Yeah, you're really a natural-born cum dumpster."

            narika "(How rude... But...)"

            narika "(Could it be true?)"

            $ MC.change_gold(400)

    $ MC.change_prestige(3)

    scene black with fade
    show expression brothel.master_bedroom.get_pic() at top
    with dissolve

    show narika normal with dissolve

    you "Congratulations. You passed the test with flying colors."

    narika "I always do, but... It's nothing like Kunoichi training. This one made me feel... Hmmm."

    you "You see, being a whore is not only about having sex with men."

    narika "It's not?"

    you "You were able to adapt to any situation to please a customer. And to find your own joy in doing so."

    you "That's what separates the best whores from the amateurs."

    narika "I see it now..."

    "You see new resolve on her face."

    narika "I always wanted to prove my superiority as a fighter. But the truth is, I wasn't really the best, because my heart wasn't into it..."

    narika "What I always craved was the admiration of others. But killing and stealing couldn't get me that."

    narika "This, on the other hand... It feels like something right and natural."

    narika "Something I could do to get genuine praise..."

    narika "And enjoy myself in the process."

    you "Narika, I am impressed. You're more than ready."

    narika "Of course I am! I shall be the number one whore in all of Xeros!"

    you "Haha, still competitive, I see! That's the spirit!"

    scene black with fade
    "Narika Shihoudou is now ready to join your brothel."

    $ girl = create_girl("Narika Shihoudou", force_original=True, level=10)
    $ girl.pop_virginity("MC")
    $ unlock_achievement("narika captured")

    call acquire_ninja(girl) from _call_acquire_ninja

    return


label c3_narika_arrested():

    "Suzume came back to report."

    show expression bg_bro at top
    with dissolve

    show suzume bend with dissolve

    suzume "Good news; that brat Narika is now in royal custody."

    you "Did the princess say anything?"

    suzume "Her interrogators whisked her away for questioning. From the look of things, I don't think we're likely to hear from her again."

    suzume "The Princess was more worried about the Mages' Guild than that Kunoichi girl, though. I'm not sure Narika was our mark."

    you "Oh well. At least we got a nice reward."

    $ unlock_achievement("narika arrested")
    $ MC.change_gold(2500)
    call receive_item(rep_item) from _call_receive_item_27
    call c3_end_story(NPC_narika) from _call_c3_end_story_3

    scene black with fade

    "You have received a reward for capturing Narika Shihoudou."

    return

## End of Narika  events ##


## Mizuki story line ##

label mizuki_k_go(girl):
    $ NPC_mizuki.flags["quest K"] = "started"

    girl.char "Master? You sent for me?"

    you "Yes, [girl.name]. I want you to travel to Karkyr on an assignment."

    if girl.origin == "Karkyr":
        girl.char "Karkyr? That's where I'm from!"

        you "Good, so you already know the city well."

    you "You're going there to look into a lady that may have lived there two centuries ago. I trust you will use every skill in your arsenal to succeed."

    girl.char "A lady from two centuries ago???"

    you "Suzume will fill you in on the details. Off you go, now."

    $ girl.say("leave for quest")

    "[girl.fullname] has left for Karkyr."

    return

label mizuki_k_back(girl):
    $ NPC_mizuki.flags["quest K"] = "resolved"
    $ NPC_mizuki.location = None
    $ _name = girl.name

    scene black with fade
    show expression bg_bro at top
    with dissolve

    suzume "Master! [girl.fullname] is back from Karkyr."

    "[_name] enters the brothel and sheds her travel cloak. She looks weary from the road, but there's something else as well. She has an air of mystery."

    "You send Sill to fetch some warm tea and wait for [_name] to gather her thoughts. After a little while, she looks rested enough to speak."

    if NPC_mizuki.flags["c3 path"]: # Mizuki storyline was already solved by other means
        call mizuki_quest_check(girl) from _call_mizuki_quest_check
        return

    you "Tell us now, [_name]. What did you learn?"

    girl.char "It was a long journey, Master..."

    play music m_tavern fadein 3.0

    scene black with fade
    show bg karkyr at sepia with dissolve

    girl.char "The trip to Karkyr was long but uneventful, and I was glad to reach the outskirts of the city."

    show bg karkyr at top_color
    with flashbackin

    "The caravan stops by the gates, leaving [_name] to fend for herself."

    girl.char "Karkyr... Here we are."

    girl.char "Can I really find answers for Master [MC.name] here?"

    girl.char "According to Suzume, I'm supposed to enquire about a dead lady from 200 years ago. That isn't much to go on..."

    "[girl.fullname] enters the city of mages, wondering at the sights and sounds of wizardry all around her."

    show bg arena_front with dissolve

    play sound s_punch

    girl.char "Hey, watch it!" with vpunch

    "[_name] barely escapes being crushed by a passing carriage."

    girl.char "(Uh? There's no one in the driver's seat!)"

    "Passing wizard" "That stupid arcane autopilot nearly ran you over! It's nowhere near ready for public launch..."

    "Trying to focus on her assignment, [_name] soon makes her way to a massive building in the heart of the city."

    girl.char "Karkyr's Municipal Archives... If there's anywhere I could find information about centuries-old events, it should be here..."

    play sound s_knock

    show bg archives at top with dissolve

    "A drab municipal employee with boredom written all over his face greets [_name] in the empty hall. He frowns, not too happy about having a visitor."

    show clerk with dissolve

    "Clerk" "Sorry Miss, we're closed. Come back during office hours."

    girl.char "It's mid-afternoon on a week day. Is it not office hours?"

    "She points at the sign behind the desk which reads 'OPEN'."

    "Clerk" "What? No!"

    "The clerk places his back to the wall, trying to hide the sign."

    "Clerk" "It's, erm, impossible for me to open to the public. The... United Wizard Union... mandates that we must be two in the office at all times for... Fire and safety... Thingies..."

    girl.char "Look, I'm only here to..."

    "Clerk" "Oh, oh, I know! Do you have your municipal archive membership card?"

    girl.char "My what?"

    "Clerk" "Aaaaand of course you don't. That's too bad, then."

    girl.char "Wait! How can I get one?"

    "Clerk" "You must fill in a couple of forms... In four copies each..."

    girl.char "Fine. *sigh*"

    "Clerk" "...and wait for 10 to 12 months for us to process your request."

    play sound s_surprise

    girl.char "What???" with vpunch

    "It's clear this hapless public servant is willing to work very hard to avoid doing any work."

    girl.char "(I have to try a new approach...)"

    $ _beauty = girl.get_stat("beauty")
    $ _constitution = girl.get_stat("constitution")
    $ _libido = girl.get_stat("libido")
    $ _def = girl.get_defense() * 5
    $ _naked = girl.compare_preference("naked", "indifferent") and _libido >= 35
    $ _sex = girl.compare_preference("sex", "indifferent") and _libido >= 50 and not girl.has_trait("Virgin")

    $ r = False

    menu:
        _("Attempt to woo him (Beauty: [_beauty])"):
            "[_name] removes her head cover, revealing her face."

            "Batting her eyelashes and playing with her hair, she gives the dorky clerk her best look."

            girl.char "But dear Sir, I only want to browse the archive for information about my poor departed relative..."

            girl.char "It will take no time at all, I swear! [emo_heart]"

            if _beauty >= 50:

                call success() from _call_success

                "The man becomes visibly sweaty and gulps, his eyes riveted on [_name]'s pretty face."

                "Clerk" "Well, if it really won't take too much time, I suppose... *mumbles unintelligibly*"

                "[_name] gives him a bright smile, making him blush even harder."

                girl.char "Oh, thank you, you're such a nice man. *grin*!"

                girl.char "(Creep.)"

                $ r = True

            else:

                call failure() from _call_failure

                "The man's face remains unmoved. It seems [_name] overestimated her charms."

                "Clerk" "Lady, I told you already. This facility is closed to the public. Go. Away."

                "Dejected, [_name] leaves the building empty-handed. It seems this avenue of investigation is a dead end."

        "Physically threaten him (Constitution: [_constitution])":

            girl.char "Safety reasons?"

            girl.char "Pal, I came all the way here from Zan on an important mission. If you don't let me through, it's your safety I'd worry about!" with vpunch

            if _def:
                "[_name] pats the hilt of her defense weapon for good measure."

            if _constitution + _def >= 50:

                call success() from _call_success_1

                "The man's face turns pale, and he immediately folds like a house of cards."

                "Clerk" "O-O-Of course my lady. Silly me, I just realized lunch break is over and it's time to open again... I won't be in your way, I promise... *trembles*"

                "[_name] shrugs."

                $ r = True

            else:

                call failure() from _call_failure_1

                "Clerk" "What??? You threaten me, a value member of the municipal union? I'll call the golem guards on you!"

                "Realizing her bluff is not going to work, [_name] quickly backs away, followed all the way to the street by the angry clerk's imprecations."

        "Flash your boobs" if _naked:

            girl.char "Well, how about I show you this membership card?"

            show screen show_event(girl.get_pic("strip", "naked", "profile", soft=True))
            with dissolve

            "[_name] flashes her titties to the bewildered clerk, whose jaw suddenly drops."

            girl.char "What do you think, old man? Are these in order?"

            "Clerk" "I... You... We... Errr..."

            "The man gulps hard, unable to look away."

            call success() from _call_success_2

            "Clerk" "F-F-Follow me... I guess I'll let you in for a spell... *gulp*"

            hide screen show_event
            with dissolve

            $ r = True

        "Offer him sex" if _sex:

            "[_name] walks all the way up to the stubborn man, close enough to smell his foul breath."

            "Ignoring his poor body hygiene, she leans towards him, whispering in his ear."

            girl.char "How about this: you let me in there, and I'll let you... in here."

            "She grabs his hand, bringing it in contact with her crotch."

            call success() from _call_success_3

            "The man gasps, left speechless. But he doesn't take his hand away."

            scene black with fade

            show screen show_event(girl.get_pic("sex", not_tags="group", hide_farm=True))
            with dissolve

            play sound s_hmm

            girl.char "Hmmm, at least there's one part of you that can work with zeal..."

            play sound s_moans_quiet

            "The man keeps his thoughts to himself as fucks her raw, enjoying the feeling of her soft pussy walls."

            "Clerk" "*grunt*" with vpunch

            "His eyes are half-closed, and he is breathing heavily, as if he is trying not to wake up from a dream."

            girl.char "I bet it beats pushing pencils for the higher-ups while waiting for retirement, doesn't it?"

            "He moans, unable to answer her question. Instead, he grabs her tits, massaging them roughly."

            play sound s_ahaa
            girl.char "Yes, yes, that's right! Fuck me like a powerless constituent!" with vpunch

            "Her goading him only seems to make him fuck her harder, which she enjoys a lot."


            "The clerk slams his cock into her even more aggressively."

            play sound s_scream_loud

            girl.char "NGGHH!!! YES!!!" with vpunch

            "The man is close to cumming. He holds on a few moments more, trying to prolong his pleasure."

            menu:
                _("Let him cum inside"):                    girl.char "Go ahead, don't be shy, fill me up like you'd fill a form with red ink!"

                    show screen show_event(girl.get_pic("cin", "creampie", "cumshot", and_tags="sex", not_tags="group", hide_farm=True))
                    with doubleflash

                    "The man gives one last thrust, spraying his hot seed inside her pussy."

                    "She can feel his cum rush inside her, then leak down her thighs."

                    girl.char "Ah, so you've finally finished. Now you have to hold your end of the bargain."

                "Make him cum outside":
                    girl.char "Don't cum inside now. Don't be shy, you can shoot your load on my body."

                    show screen show_event(girl.get_pic("cob", "cumshot", and_tags="sex", not_tags="group", hide_farm=True))
                    with doubleflash

                    "Clerk" "*groan*" with vpunch

                    "The clerk out of her pussy, grabbing his shaft as he sprays his seed all over her."

                    "[_name] heaves a sigh as she feels his sticky cum coating her body."

                    girl.char "Find me a towel or something to clean up. Then you' ll have to hold on to your part of the deal."

            play sound s_dress
            hide screen show_event
            with dissolve

            "After they both sort their clothes out, the man invites her to enter the archive. He sports a stupid grin on his face, which [_name] does her best to ignore."

            $ r = True

    if r:
        show bg archives at top with dissolve

        "[_name] starts browsing the archives. The clerk does his best to help, which isn't much, but at least [_name] is able to grasp how the index system works."

        girl.char "I don't even know what I'm looking for here... Suzume said that Mizuki woman is probably going by an alias, so finding her real name is going to be a challenge."

        girl.char "... I know more or less the decade when she got married, to a lord from Westmarch... And she was nobility, so I should be able to find out something about their wedding in the almanacs."

        with fade

        "An hour passes. Then two. The petty clerk grumbles and clears his throat incessantly, seeing his hopes of going home early fade away."

        girl.char "Wait a minute... This notice: '{b}Wedding of Lord Mitsuhide from Telago and Lady Kouchi from Karkyr{/b}'... Telago is one the large cities in Westmarch!"

        girl.char "Let's read it!"

        play sound s_dress

        call screen letter(header = _("A Most Auspicious Occasion (1/3)"),
                        message = __("In the twilight hours of yestereve, the City of Karkyr had the distinct pleasure of witnessing a splendid matrimonial union between the esteemed scions of two venerable families: the Mitsuhide from the distant West and the esteemed Kouchi from our very own Karkyr.\n\nThe bride, Lady Sui Kouchi, graced the occasion in a resplendent midnight blue kimono, a testament to the finest craftsmanship."), signature = "...")

        girl.char "A midnight blue kimono? That sounds like her description... Let's keep reading."

        play sound s_dress

        call screen letter(header = _("A Most Auspicious Occasion (2/3)"), message= _("Renowned throughout the realm as the sweetest flower of the Karkyr nobility, Lady Sui captivates all with her generous heart and highborn spirit, extending her kindness even to the most destitute among our citizens.\n\nAs the sole heir of the Kouchi lineage, her dowry encompasses the considerable estates of her family, stretching across Karkyr and its verdant surroundings."),
                        signature = "...")

        $ girl.rand_say("ma: She was loaded, that's a noble all right... But radiant heart and benevolent spirit? Damn, that doesn't sound at all like her.", "id: So she was a kind heart? That's a rare thing among the nobility, especially if she was also rich.")

        play sound s_dress

        call screen letter(header = _("A Most Auspicious Occasion (3/3)"), message= _("Though the Mitsuhide family may not boast the lengthy pedigree of the Kouchi (some ill-mannered souls may even label them as upstarts - but you shall not read such baseless slander from your humble Almanac), the dashing young Lord is rumored to be well-positioned in the ongoing struggle for supremacy over the Western Marches.\n\nEven as the newlyweds retired to their chambers, the festivities continued late into the night, a sumptuous feast laid before the guests featuring chilled monkey brains and snake surprise..."),
                        signature = "The Karkyr Almanac")

        girl.char "All right, that's enough. Could this Sui Kouchi be our mysterious blue Lady? Let's dig deeper about that Kouchi family..."

        "The clerk sighs exasperatedly as [_name] opens yet another dusty tome of the same year..."

        show bg archives at sepia with dissolve

        scene black with fade

        girl.char "That's when I found it. The diary from an old servant of the Kouchi family, who was watching over the young Lady during her wedding."

        you "Really? What was in it?"

        girl.char "The man had some talent as a sketcher, and I found a drawing of the blue lady inside. She looked just like Mizuki."

        you "So it was her! Did you learn anything else?"

        girl.char "There was one record of note. It said this..."

        scene black with fade

        show bg archives at sepia
        show bg archives at top_color with flashbackin

        "Old servant diary" "The wedding was found by all to be a wonderful affair, and I had never seen Lady Sui so happy. She was deeply smitten with the young Lord."

        "Old servant diary" "Alas, poor soul, had I known it would end like it did, I would have thrown myself into the fires of the seven hells rather than let her leave her dear Father with that man."

        "Old servant diary" "Nevertheless, as I passed by the door of the espoused, I could hear them whisper sweet nothings..."

        show bg mizuki honeymoon1 at sepia with fade

        $ mizuki_name = "Lady Sui"

        play sound s_surprise
        show bg mizuki honeymoon1 at top_color with flashbackin

        mizuki happy "M-My lord! This is all so sudden, I, I..."

        "Lord Mitsuhide" "What, Sui? We're husband and wife now. You know what that entails..."

        mizuki "I know, but... I've never been so close with a man before, I... I need a moment."

        "Lord Mitsuhide" "Sure, sure, we'll take our time... *sigh*"

        show bg mizuki honeymoon2 at top with dissolve

        mizuki "Thank you my lord... For being so wonderful to me..."

        scene black with fade

        "Old servant diary" "I should have removed myself from behind the door then and there, but I couldn't help but hear what came next..."

        stop music fadeout 3.0

        show bg mizuki honeymoon3 at top with dissolve

        play sound s_screams

        mizuki naked "Oh, my lord, oh!!! Aaah!!!" with vpunch

        play sound s_sucking

        "Lord Mitsuhide" "Damn, you're tight! So you really are a virgin..."

        mizuki "O-Of course, my lord, how would I not be? You are my first husband..."

        "Lord Mitsuhide" "Haha... So naive, in spite of having such a mature body..."

        play sound s_aaah

        mizuki "I... Nggh... Thank you, my lord... Aaah!" with vpunch

        "Lord Mitsuhide" "*push deeper inside her* You like that, uh?"

        with vpunch

        mizuki "Oh! My lord! It... It hurts..."

        "Lord Mitsuhide" "Yeah, well, you're going to get used to it."

        mizuki "I-I don't know... It's just so overwhelming..."

        show bg mizuki honeymoon4 at top with dissolve

        play sound s_scream

        mizuki "Ahahah!" with vpunch

        "Mitsuhide starts sucking on her nipple, twisting it with his tongue."

        mizuki "This... Oh..."

        "Lord Mitsuhide" "Hmm, seems like I found your weakness..."

        mizuki "It feels, hmmm..."

        "Lord Mitsuhide" "What? *keeps fucking her hard*" with vpunch

        play sound s_scream_loud

        mizuki "AAAH!!!" with vpunch

        mizuki "D-Don't bite..."

        "Lord Mitsuhide" "Can't help it, these titties are so inviting... Eheh."

        "She struggles to match his rhythm."

        play sound s_ahaa

        mizuki "Can we take it, aah, slow? If we pace ourselves, I might..."

        with vpunch

        "Lord Mitsuhide" "AAARRRH! *grunt*"

        play sound s_surprise
        show bg mizuki honeymoon5 at top with flash

        mizuki "Eek!!! W-what's this?!?"

        with doubleflash

        "Lord Mitsuhide" "Oh, damn..."

        with flash

        mizuki "Did you... Did something..."

        "Lord Mitsuhide" "Eheh, it felt great. I couldn't help myself."

        mizuki "I-I see, my lord..."

        mizuki "(So this is what it's like... To be husband and wife... I never knew...)"

        "Lord Mitsuhide" "Arios, I'm spent, I need to lie down now."

        show bg mizuki honeymoon6 at top with fade

        "Lord Mitsuhide" "You did well, Sui, for a beginner."

        mizuki "T-Thank you, my lord."

        "Lord Mitsuhide" "I think I'm going to enjoy our marriage more than I thought I would..."

        play sound s_surprise

        show bg mizuki honeymoon7 at top with dissolve

        mizuki "My lord... What do you mean? Do you not fancy me?"

        "Lord Mitsuhide" "Fancy you? Oh, come on, Sui, you're not so naive as to not know how unions work among the nobility. Our feelings do not count in these matters."

        mizuki "I... I know how such things work, but... You courted me quite gallantly, and I am ashamed to admit that I fell for you at first sight..."

        "Lord Mitsuhide" "Eheh, you did, didn't you? I did go all out..."

        mizuki "*blush* I am serious, my lord... My heart is yours..."

        "Lord Mitsuhide" "Eheh, you're cute."

        mizuki "It wasn't easy to convince father to let you into the family... I don't mean any offense, but... This is not what he wanted..."

        "Lord Mitsuhide" "Hmph, I know the old fart doesn't like me one bit. He thinks my blood isn't the right shade of blue. Just like these dusty old families from the Western Kingdoms!"

        "Lord Mitsuhide" "But I'll show them... You'll see!"

        mizuki "Regardless, we are together now, my lord. Are you... Are you glad?"

        "Lord Mitsuhide" "Glad? Oh, yes, Sui, I'm very, very glad. You and I are going to get along splendidly."

        show bg mizuki honeymoon8 at top with dissolve

        mizuki "Oh, that's a relief!"

        mizuki "Then if you're happy, I'm happy too. I'm going to be the best wife for you, you'll see! I will bear your children..."

        "Lord Mitsuhide" "Of course you will!"

        "Lord Mitsuhide" "Now, let's catch some shuteye. We ride in the morning for the Western Kingdoms, and I don't want to waste any more time here than I need to."

        mizuki "So soon? I-I mean, s-sure, if you have some urgent business..."

        "Mitsuhide is not listening, already half asleep."

        show bg mizuki honeymoon9 at top with dissolve

        mizuki "Good night, dear husband... *blush*"

        "Lord Mitsuhide" "*snore*"

        $ mizuki_name = "Mizuki"

        scene black with fade
        show bg archives at sepia with dissolve

        "Old servant diary" "The next day at dawn, Lady Sui left Karkyr for Westmarch, with no time to say goodbye to her dear Father or us, her loyal servants."

        "Old servant diary" "Little did we know we would never see her again..."

        scene black with fade

        girl.char "That's about all I could gather from the archives."

        $ NPC_mizuki.flags["K1 unlock"] = True

        you "Good. Were you able to learn anything else?"

    else:
        scene black with fade

        girl.char "...so I had to leave, unable to learn anything."

        you "Damn. But you did manage to find some other information, right?"

        $ NPC_mizuki.flags["K1 unlock"] = False

    girl.char "Well, Suzume gave me another hint I had to follow."

    suzume "Yup. I told her Mizuki seems to be under the protection of Shalia."

    girl.char "But it is a long tale... I must rest now, Master, and I will finish my story tomorrow."

    you "Fine, let's finish this story tomorrow then. Get some sleep."

    $ MC.rand_say("gd: You deserve a good rest.", "ne: You will need to recover before you can go back to your duties.", "ev: Because I expect you to be back on the job shortly!")

    $ calendar.set_alarm(calendar.time+1, StoryEvent(label="mizuki_k_back2", type="morning", call_args = (girl, )))

    sill "[girl.fullname] is now back to [brothel.name]. You may want to let her rest before putting her back on the job."

    return


label mizuki_k_back2(girl):

    scene black with fade

    "You summon [girl.fullname] so that she can finish telling you about her time in Karkyr."

    show expression bg_bro at top
    with dissolve

    $ _name = girl.name

    you "So, [_name]. Are you ready to continue your story?"

    girl.char "Yes. So, during my travel, I had heard about a special shrine in Karkyr devoted to Shalia..."

    girl.char "One that was hidden in plain sight, they said."

    show bg arena_front at sepia with dissolve

    $ r = False

    if MC.god == "Shalia":
        girl.char "Thanks to the information you gave me as one of Shalia's followers, I was able to find it."

        girl.char "I followed your advice and found the path, although it was well hidden."

        call success() from _call_success_4

        $ r = True

    elif girl.origin == "Karkyr":
        call success() from _call_success_5

        girl.char "As a native of Karkyr, I knew just where to go. As kids, we used to play 'ghosts and ghouls' in the fog at the foot of the tower..."
        $ r = True

    else:
        girl.char "I talked to many people in the taverns, trying to find my way to that secret location..."

        scene black with fade
        show bg tavern_man at sepia with dissolve

        girl.char "When finally..."

        play music m_tavern fadein 3.0

        play sound s_crowd_laugh

        show bg tavern_man at top_color with flashbackin

        man "The tower of Shalia you say? Nah, you won't find anyone in the city who will lead you there."

        girl.char "Really? And Why not?"

        man "Because the Archmage Council banned all religious followers from the city. Including Shalia's."

        girl.char "All religions, forbidden? Why is that?"

        man "There was another pogrom against mages in Borgo a couple of months ago, and the son of one of the Council's big shots got stoned to death."

        man "The Council 'took a stand against religious intolerance', or so they said, and decreed that the city would from now on only follow the voice of Reason and Magic."

        man "It is now forbidden to visit any of the old places of worship, or you'll be escorted out of the city by unfriendly golems."

        girl.char "So... Fight intolerance with intolerance?"

        man "*shrug* Well, maybe it was the right decision. At least it keeps Arios fanatics at bay."

        man "But the collateral damage is now Shalia followers have to live in hiding as well. Which doesn't change much for us, I guess..."

        girl.char "Wait! You're a Shalia follower?" with vpunch

        man "Hush, lower your voice now, are you nuts?"

        "He looks around nervously."

        man "The people here are friends, but I don't want to be kicked out of the city over some foolish girl's loose tongue..."

        girl.char "But Sir, you must know where Shalia's Tower is located! Please, just tell me how to get there..."

        man "Come on, it's not that simple. There is only one path to get there, and it's well hidden. You would need someone to guide you."

        girl.char "Then could you perhaps..."

        man "Me? Absolutely not!"

        $ _charm= girl.get_stat("charm")
        $ _sensitivity = girl.get_stat("sensitivity")
        $ _libido = girl.get_stat("libido")
        $ _service = girl.compare_preference("service", "indifferent") and _libido >= 35

        menu:
            _("Manipulate him (Charm: [_charm])"):
                girl.char "Oh, come on, Sir, are you afraid to help a lady? I thought you were a real gentleman..."

                if _charm >= 50:

                    call success() from _call_success_6

                    man "Of course I am! That isn't the question..."

                    girl.char "I knew it, you {i}are{/i} brave!"

                    "She puts her hand on his arm."

                    man "I... Ahem..."

                    girl.char "I would be {i}immensely{/i} grateful if you would help me, a poor girl from outside the city..."

                    man "I {i}am{/i} known as fearless, you aren't wrong..."

                    girl.char "Oh, you'd be my knight in shining armor..."

                    man "Oh, don't embarrass me, I... Well..."

                    "She looks at him with big puppy eyes."

                    man "*sigh* Oh, demons, fine, I'll show you the path that leads to the Tower. But that's as far as I'll go, okay? The mages are sure to have eyes on that place."

                    girl.char "Thank you, Sir! I knew you'd come around!"

                    $ r = True

                else:

                    call failure() from _call_failure_2

                    man "Yeah, yeah, save that crap for the bourgeois you whore yourself to."

                    man "I didn't get that far in the underworld by giving any favours. Now scram."

                    "The vibe in the tavern turns hostile almost instantly, and [_name] realizes the man she is talking to is perhaps more important than he seemed."

                    "She is rudely escorted out by goons."

            "Appeal to his good heart (Sensitivity: [_sensitivity])":

                girl.char "Mister, please!"

                "[_name] looks at him with tears in her eyes."

                girl.char "My master will get mad if I don't find it... He might beat me blue... *sob exageratedly*"

                if _sensitivity >= 50:

                    call success() from _call_success_7

                    man "D-Don't cry, kid..."

                    man "(Damn, I could never handle seeing a crying girl...)"

                    man "Okay, fine, I'll show you..."

                    "Through her crocodile tears, [_name] looks up with hope."

                    girl.char "You will?"

                    man "Yes, but only so far as where the path starts! Then you're on your own."

                    girl.char "Oh, thank you!"

                    $ r = True

                else:

                    call failure() from _call_failure_3

                    man "What, you think I'd help you out of pity? *disdainful*"

                    man "Pathetic. Get out of my sight."

                    "He signals for two bouncers to come and [_name] is quickly escorted out of the tavern."


            "Offer him a blowjob" if _service:

                girl.char "Wait... Remember how you told me I had a loose tongue? I can use it for other things..."

                man "W-What do you mean? *sweat*"

                "[_name] makes a show of dropping a spoon off the table."

                play sound s_clang

                girl.char "Oops, silly me! Let me get this."

                "Getting on all four, [_name] goes under the table, only to emerge between the man's legs."

                man "W-What are you doing?!?"

                "She puts her hand on his crotch, feeling the growing bulge inside."

                girl.char "What if I make it worth your while? Will you take me there? *salacious wink*"

                call success() from _call_success_8

                man "I... Err... Fine."

                man "Let's just go somewhere more quiet..."

                girl.char "Lead the way! *grin*"

                play sound s_dress

                scene black with fade

                show screen show_event(girl.get_pic("blowjob", "service", not_tags="group", hide_farm=True))
                with dissolve

                "They move to the back, and [_name] resumes her ministrations as soon as they are alone."

                play sound s_sucking

                girl.char "Ngggh..."

                man "Oooh... Aaah..."

                girl.char "Nggh... Hmmm... Fee'ing good? *mumble*"

                "The man grunts his approval, holding her head as he fucks her mouth more."

                girl.char "Hmmmm..."

                "[_name] does her best to bring him off quickly, licking his shaft and teasing the tip by pushing it against the inside of her cheek."

                man "Urrh..."

                "[_name] increases her pace, taking him deeper, until he is ready to burst. She takes a quick breather, still jerking his cock."

                girl.char "Tell me, mister. Where do you want to finish?"

                menu:
                    _("Inside her mouth"):                        "[_name] takes him back inside her wet, warm mouth, only for him to instantly get off"

                        show screen show_event(girl.get_pic("cim", "cof", "cumshot", and_tags="service", not_tags="group", hide_farm=True))
                        with flash

                        man "*grunt*"

                        with doubleflash

                        girl.char "NGGGH!!"

                        with flash

                        "Pulling her hair, the man lets it all out before he finally releases her."

                        girl.char "*cough* *cough*"

                        "Cum drips down her face as the man tries to gather his thoughts."

                    "Over her face":
                        "[_name] smiles and stands ready to receive his load as he jerks himself off."

                        show screen show_event(girl.get_pic("cof", "cih", "cumshot", and_tags="service", not_tags="group", hide_farm=True))
                        with flash

                        man "*groan*"

                        with doubleflash

                        "The man explodes right over her face and hair, smearing her with sticky white semen. She takes it all in stride."

                        man "Oh, aah, ah... *heavy breathing*"

                hide screen show_event
                with dissolve

                "As she cleans up, she looks at him inquisitively."

                girl.char "Now you'll hold up your part of the bargain, right?"

                man "F-Fine... I'll show you where to go. But you'll have to be quick - I don't want to get caught!"

                $ r = True

    if r:

        stop music fadeout 3.0

        scene black with fade

        show bg shalia_tower at sepia with dissolve

        "After a long trek, [_name] finally reached Shalia tower."

        show bg shalia_tower at top_color with flashbackin

        girl.char "Here it is... Hidden in plain sight atop one of the hills in the city, but invisible from below because of the endless fog..."

        "[_name] shivers."

        girl.char "There are strange lights about, but no one is in sight. This place seems deserted."

        "Cautiously, [_name] climbs the rest of the way to the entrance."

        "She is surprised to find the door isn't locked. Taking a deep breath, she enters the forbidden shrine."

        scene black with fade

        "The tower is a maze of smoke and mirrors, with bizarrely shaped rooms that seem to hide secrets in plain sight, but ultimately resist [_name]'s efforts to understand their true purpose."

        "Eventually, she makes her way to a room at the top of the tower who finally holds her interest."

        show bg crystal_room at top with dissolve

        "A large crystal is floating inside the room, buzzing with purple energy. It seems to animate as [_name] gets closer."

        "Crystal" "Welcome, follower. It has been some time since one of your kind has come to visit."

        "Crystal" "I do hope nothing bad has happened to our congregation..."

        $ q_who = True
        $ q_what = True
        $ q_council = True
        $ q_mizuki = True

        label c3_crystal_menu():

            menu:
                "Who or what are you?" if q_who:
                    girl.char "A talking crystal? Am I dreaming?"

                    girl.char "Who, or what, are you?"

                    "Crystal" "Well. I am the Mentor."

                    girl.char "The what, now?"

                    "Crystal" "The Mentor. Of the local Shalia covent. It is a position held by the eldest, most cunning among us. Usually amounts to the same thing."

                    "Crystal" "At least I {i}am{/i} very old. Maybe not that cunning."

                    girl.char "But isn't that position held, you know, by... people? (As opposed to, say... Talking floating stones?)"

                    "Crystal" "A fair question. I was once made of flesh and blood. Like you."

                    "Crystal" "My knowledge and advice was once found to valuable enough. The first Archmage, Patrik, offered to use Cimerian techniques to preserve my soul. In the crystal shard you see before you."

                    "Crystal" "Perhaps 'offered' isn't the right word. Rather sentenced. Patrik wanted to harness my knowledge of the underworld. For his own purposes."

                    girl.char "And you accepted?"

                    "Crystal" "The alternative was quartering. So yes."

                    "Crystal" "The joke's on him though. Now he's long gone. Most mages have forgotten that I exist. But I remain. I was reclaimed by Shalia and her followers a few centuries ago."

                    girl.char "Centuries ago? Then you might know her..."

                    $ q_who = False

                    jump c3_crystal_menu

                "What do you do?" if q_what:
                    girl.char "What are you doing here?"

                    "Crystal" "I am the covent's Mentor. I answer questions and offer advice to the faithful. And other curious souls like you."

                    "Crystal" "I can also tell people about our history. I was around for five or six centuries, after all."

                    girl.char "Can you make time to answer all these questions?"

                    "Crystal" "You'd think it'd keep me busy. But not many people stop by. Overconfidence is a boon to the youth..."

                    "Crystal" "Until they get shanked in a dark alley."

                    "Crystal" "Now I sit here, and devise haikus. Would you like to hear one?"

                    girl.char "Well... No."

                    $ q_what = False

                    jump c3_crystal_menu

                "Shalia worship is forbidden now" if q_council:
                    girl.char "You should know that Shalia's worship has been banned by the Council! That's why no one has come to the tower for a while."

                    "Crystal" "Oh, again? It's only been a hot minute since the last time."

                    "Crystal" "What was it, like 80 years ago?"

                    "Crystal" "Fret not, youngster. It's a momentary setback. Such bans only last for a few decades, half a century at most."

                    "Crystal" "But that explains why {i}they{/i} are gathering outside..."

                    girl.char "They? Who's they?"

                    "Crystal" "The golems. They've come for you, I'm afraid. You should hurry with your questions."

                    girl.char "Oh, crap."

                    $ q_council = False

                    jump c3_crystal_menu

                "I have questions about a mysterious lady..." if q_mizuki:

                    "[_name] gives the crystal a description of Mizuki."

                    with fade

                    girl.char "And we believe she was a Shalia follower. Would that ring any bell?"

                    "The crystal gives a sort of chuckling noise."

                    "Crystal" "Of course it does. Child, I have known many merciless killers. But Ike Mizuki stands out. She's the most cold-blooded assassin I've ever met."

                    girl.char "Mizuki? So you knew her under her alias?"

                    "Crystal" "I sure did. I gave it to her."

                    girl.char "You... What?"

                    scene black with fade
                    show bg shalia_tower at sepia with dissolve

                    "Crystal" "It happened two centuries ago. I was a dark night..."

                    play sound s_thunder
                    with flash

                    "Shalia follower" "Mentor! Mentor!"

                    show bg crystal_room at sepia with dissolve

                    "Crystal" "Yes, son?"

                    "Men pour into the room, out of breath. They are carrying a body on a stretcher."

                    "Shalia follower" "We found her outside in the snow... She has Shalia's mark on her..."

                    "Crystal" "Alive?"

                    "Shalia follower" "No, Mentor, we checked. Dead as a doornail. But it's not one of us who did her in, I swear."

                    "Crystal" "If she's dead, then... Why is she moving?"

                    play sound s_wscream

                    "Shalia follower" "WHAAAAH!!!" with vpunch

                    "The men drop the stretcher in awe as the cold body stirs."

                    "Shalia follower" "What sorcery is this? She had no pulse! She was gone!"

                    "Crystal" "Shalia saw fit to protect her. A rare honor."

                    scene black with fade

                    "Crystal" "This is how I met her. Mizuki."

                    show bg mizuki intro at sepia with dissolve

                    "Crystal" "When she got to her senses, she wouldn't answer anyone's questions. We nursed her back to a semblance of health, but she was mute for the whole time."

                    "A wave of energy crackles around the crystal. Almost like a shiver."

                    "Crystal" "When she finally spoke, months had passed. I still remember her words, crystal clear *cough*. She said..."

                    show bg mizuki intro at top_color with flashbackin

                    mizuki angry "I need to kill someone. Teach me."

                    "Crystal" "We were all taken aback. She didn't seem the type. Some of the followers even thought she was from a well-to-do family in the city."

                    "Crystal" "I too thought she had a soft side... I misjudged her."

                    "Crystal" "Regardless, she was under Shalia's protection. It was my duty to help."

                    girl.char "What did you do?"

                    "Crystal" "There was a ninja school in the mountains nearby. It was the Water school, which seemed fitting."

                    "Crystal" "I pulled some favors to have her enroll there, under the alias 'Ike Mizuki'. She chose it."

                    "Crystal" "She trained at the ninja school for years. They told me she was exceptionally gifted and hard-working. She would visit us from time to time."

                    girl.char "You didn't ask her who she wanted to kill?"

                    "Crystal" "In such matters, I know better than to pry."

                    "Crystal" "Regardless, we soon found out."

                    "Crystal" "There was a civil war in Westmarch at the time. Something about four kingdoms vying for ultimate power, or such political nonsense."

                    "Crystal" "A large battle was held to breach into one of the capital cities. A young lord died in that fight."

                    "Crystal" "As soon as Mizuki heard the news, she got up and left Karkyr, without a single word."

                    "Crystal" "But the people who met her gaze that day swore they had seen death incarnate."

                    "Crystal" "We thought we would never hear from her again... But we were wrong."

                    girl.char "What happened?"

                    "Crystal" "Back in Westmarch, lords started dying. Brutally."

                    "Crystal" "It didn't matter how much security they had. They were picked off one by one."

                    show bg mizuki combat at sepia with dissolve

                    "Crystal" "For some, it was a blade..."

                    show bg mizuki poison at sepia with dissolve

                    "Crystal" "For others, poison..."

                    show bg mizuki defeat at sepia with dissolve

                    "Crystal" "Others again, magic..."

                    "Crystal" "She dealt death in every possible way. Even..."

                    show bg mizuki footjob1 at sepia with dissolve
                    show bg mizuki footjob1 at top_color with flashbackin

                    "Echoes of a lord's voice" "Ngggh... N-No more... I-It hurts... P-Please let me go..."

                    $ mizuki_name = "Echoes of Mizuki's voice"

                    mizuki ninja "Fufufu... Of course."

                    show bg mizuki footjob2 at top with doubleflash


                    "Echoes of a lord's voice" "M-M-Mercy!!! AAARGH!!!"

                    show bg mizuki footjob3 at top with flash

                    mizuki "Finally, it's my turn to have a good time."

                    mizuki "Time to drop dead, dear father-in-law."

                    play sound s_splat

                    "*twist*"

                    scene black with fade
                    play sound s_wscream

                    "Echoes of a lord's voice" "AAAAARH!!!" with vpunch

                    show bg crystal_room at top with flashbackout

                    "Crystal" "Everyone she marked for death, died."

                    "Crystal" "The Western realms were thrown into chaos, all of their ruling families decimated."

                    "Crystal" "But she didn't stop in Westmarch. The trail of murders continued, and I still hear about it to this day. 200 years later."

                    "Crystal" "Seems I'm not the only one who cheated death."

                    $ mizuki_name = "Mizuki"

                    $ q_mizuki = False

                    jump c3_crystal_menu

                "Leave" if not q_mizuki:
                    "[_name] thanks the Mentor for what he told her, then takes her leave."

                    scene black with fade
                    show bg shalia_tower at top with dissolve

                    "As she exits the tower, [_name] is confronted by a towering figure, a massive golem guard infused with magical energy."

                    show golem at right with dissolve

                    golem "This building if off-limit to the public. You have been found in violation of Council resolution 50E-B512A."

                    golem "You will now be removed from the city perimeter. Any resistance will be met with lethal force."

                    "Unwilling to risk a confrontation, [_name] follows the golem guards quietly to the city's outskirts."

                    scene black with fade
                    show bg karkyr at top with dissolve

                    show golem at right with dissolve

                    golem "Unlawful worshipper. You have been banned from the city for a duration of... One year. Any attempt to enter the city premises again will be met..."

                    girl.char "...with lethal force, yeah, yeah, I get it."

                    $ NPC_mizuki.flags["K2 unlock"] = True

    else: # failure

        scene black with flashbackout

        girl.char "So I looked everywhere for information within the city."

        girl.char "But I could never find out where that cursed tower was. People would just shut me down every time I asked."

        girl.char "Eventually my stipend ran out, I had to come back."

    hide golem
    show bg karkyr at sepia
    with flashbackout

    girl.char "And that's it. After that, I took the next wagon out of the city, and came straight back to you."

    if NPC_mizuki.flags["K1 unlock"] and NPC_mizuki.flags["K2 unlock"]:

        you "Very impressive. You did very well."

        $ girl.change_mood(20)
        $ girl.change_love(2)
        $ girl.change_fear(-2)

        girl.char "Thank you, Master."

    elif NPC_mizuki.flags["K1 unlock"] or NPC_mizuki.flags["K2 unlock"]:

        you "I guess we found at least one hint. I hope we can learn more."

        girl.char "Yes, Master."

    else:

        you "So you were not able to retrieve even a single piece of useful information?"

        girl.char "I'm sorry, Master, I... *look down*"

        menu:
            _("Reassure her"):                you "Well, you did your best. It's on me for giving you an assignment that was too hard."

                girl.char "Sorry..."

                you "Please go get some rest."

                $ girl.change_mood(-5)
                $ girl.change_fear(-1)

            "Scold her":
                you "What a waste of time and money. You will have to work extra hard to make up for that! Out of my sight!"

                girl.char "Aw..."

                $ girl.change_mood(-20)
                $ girl.change_love(-2)
                $ girl.change_fear(2)

        $ NPC_mizuki["failed quest"] = True
        $ NPC_mizuki.location = seafront

        "Suzume looks defeated."

        suzume doubt "[MC.name], I'm afraid this failure means we won't be able to uncover Mizuki's secret. We are missing some important clues..."

    if NPC_mizuki.flags["quest W"] == "resolved" and NPC_mizuki.flags["quest K"] == "resolved" and not NPC_mizuki.flags["failed quest"]:
        $ NPC_mizuki.flags["quest success"] = True
        $ game.set_task("The Water Kunoichi: Talk to Suzume to confront Mizuki about her past.", "story2", 3)
        suzume "I believe we now know enough to expose Mizuki's secret."

        "You can call on Suzume from the {b}Visit city{/b} screen to progress Mizuki's story."

    return

label mizuki_w_go(girl):
    $ NPC_mizuki.flags["quest W"] = "started"

    girl.char "You wanted to see me, Master?"

    you "Yes. I'm going to send you on a secret mission to Westmarch."

    if girl.origin == "Westmarch":
        girl.char "Oh, I'm from Westmarch!"

        you "It's good, because I will need someone who knows the lay of the land."

    you "You will need to investigate some political events that happened there 200 years ago."

    girl.char "200 years ago? Why?"

    you "Suzume will fill you in on the details. You'll leave on the next stagecoach to the West."

    $ girl.say("leave for quest")

    "[girl.fullname] leaves for Westmarch."

    return

label mizuki_quest_check(girl):

    girl.char "Master, I have learned many things from my travels. It is a long and poignant story about Mizuki's past..."

    you "Oh, that? Forget it, that won't be necessary."

    girl.char "Whaaaat???" with vpunch

    suzume "Oh yeah, we got rid of her already!"

    girl.char "B-B-But what about my story?"

    you "Oh, you can tell Sill, she's dying to hear all the details."

    sill sad "What? I, uh, no... I need to clean the attic..."

    girl.char "Wait, where are you all going? Waiiiit!!!"

    stop music fadeout 3.0

    scene black with fade

    "[girl.fullname] is now back to [brothel.name]. You may want to let her rest before putting her back on the job."

    return

label mizuki_w_back(girl):
    $ NPC_mizuki.flags["quest W"] = "resolved"
    $ NPC_mizuki.location = None
    girl.char "[girl.fullname] returns from Westmarch."

    $ _name = girl.name

    suzume "[MC.name], good news! [girl.fullname] just got back from Westmarch."

    "[_name]'s clothes are damp from the constant mist and rain on the road to Westmarch. She looks tired and miserable."

    "You tell Sill to get her a change of fresh clothes before she sits down before you to report."

    if NPC_mizuki.flags["c3 path"]: # Mizuki storyline was already solved by other means
        call mizuki_quest_check(girl) from _call_mizuki_quest_check_1
        return

    you "So, how did your investigation of Mizuki in Westmarch go?"

    stop music fadeout 3.0

    girl.char "It was... Complicated. Even finding the right place was a challenge."

    play music m_knights fadein 3.0

    scene black with fade
    show bg westmarch at sepia with dissolve

    girl.char "Westmarch is comprised of many independent cities. Based on Suzume's information, I targeted the larger ones, but I didn't find what I was looking for until I reached the old royal capital, Telago."

    girl.char "The older people there could remember the Lady in blue, as they called her. She was the wife of a Prince, came from Karkyr, then she died a tragic death."

    suzume "It matches what we know about Mizuki's story."

    girl.char "People were fuzzy on the details, but after some time I heard about someone who could be of help..."

    show bg westmarch at top_color with flashbackin

    woman "...that old coot still lives in the old Mitsuhide Manor. You can find him there at most times, but beware, he isn't the friendly sort."

    girl.char "An old man living alone in an abandoned manor... Thats isn't much to go on, but it's my best lead yet."

    show bg westmarch palace at top with fade

    girl.char "Finally, I found it..."

    girl.char "This isn't a house, it's a palace! Definitely the home of a High Lord..."

    girl.char "Could it really be that only one man lives here?"

    show old_elf with dissolve

    "Old Elf" "Go away!"

    girl.char "Eh?"

    "Old Elf" "Go away! Don't loiter, or I will call the militia!"

    "An old skinny man is barring the way with his diminutive frame, dressed in clothes that were once fancy but are way past their prime."

    play sound s_surprise

    girl.char "S-Sir?" with vpunch

    "[_name] is stunned to see that the man is in fact an elf, a rare sight in Zan. And a male one at that, which is even rarer."

    "Old Elf" "What's the matter with you, wench, are you deaf? Why are you staring at me like this?"

    girl.char "N-Nothing, Sir, I've just never met a male elf before..."

    "She has to remind herself that unlike Zan, the Western principalities are not actually at war with the Elves, although racist sentiment is as prevalent here as anywhere else."

    "Old Elf" "What, you uncough peasant have never seen a city elf? You think all Elves are like these wretches who hide in the forest, munching on roots and drinking plant juice like the degenerates they are?"

    girl.char "N-No..."

    "Old Elf" "Well now you have. Now, go away, shoo."

    girl.char "Wait! Please Sir, do you live here? It's you I've come seeking."

    "Old Elf" "Me? Ha! Preposterous!"

    "Old Elf" "What in Arios's name would a street girl like you have to do with me, a proud servant of the Mitsuhide Clan?"

    girl.char "The Mitsuhide Clan? But... There doesn't seem to be anyone else living here."

    "Old Elf" "*sigh deeply* No, not anymore... But I keep the glorious memory of the Mitsuhide's alive, and I will for the centuries to come, for as long as I draw breath!"

    girl.char "Such loyalty is... Noteworthy? Err, can you tell me about the Mitsuhide family?"

    "The old elf suddenly mellows and starts spewing information at her. [_name] has clearly stumbled upon his favorite topic."

    "Old Elf" "The flamboyant Mitsuhide family, pride of Telago, and beloved champions of Westmarch! Of course, I know all about it!"

    "Old Elf" "There is a reason the name 'Mitsuhide' is revered and feared in equal measure across our lands and beyond... It was the most powerful and enlightenned family to ever grace these parts. There were no other clan like them, and mark my words, there shan't be another!"

    "Old Elf" "They were patrons to warriors, priests and artists alike, and they very nearly united Westmarch as one country, were it not for their untimely demise..."

    girl.char "Really? What happened?"

    "Old Elf" "I was but a young lad with no hair on my chin then... Barely 60 years old... To think such an illustrious clan could stumble and fall, all because of the sins of a cursed woman!"

    girl.char "A cursed woman? Tell me more..."

    "The man clams up all of a sudden."

    "Old Elf" "That vile, evil blue witch! I won't say a word about that wretch. Now, leave me be!"

    "[_name] suddenly panics: she is in danger of losing the plot, this close to succeeding."

    girl.char "(Quick, I must think of something!)"

    $ r  = False

    if girl.origin == "Westmarch":
        girl.char "You know, I grew up in Westmarch with my [girl.story_guardian], in a city pretty far from here, and still I heard about the mighty Mitsuhide family."

        "[_name] is lying through her teeth; she could never be bothered to care about the endless petty power politics cursing her homeland."

        girl.char "I always wondered how such a clearly powerful and morally superior family could meet their downfall... It seems so unfair..."

        call success() from _call_success_9

        "Old Elf" "And it is!"

        "The man starts rambling again."

        $ r = True

    else:

        $ _refinement= girl.get_stat("refinement")
        $ _obedience = girl.get_stat("obedience")
        $ _libido = girl.get_stat("libido")
        $ _anal = girl.compare_preference("anal", "indifferent") and _libido >= 35

        menu:
            _("Appeal to his sophistication (Refinement: [_refinement])"):
                girl.char "Please, Sir, I wasn't expecting to meet someone so... Erudite. I am something of a scholar myself, and am working on a historical treaty of the area."

                if _refinement >= 50:

                    "Old Elf" "A treaty? On Telago's history?"

                    girl.char "Precisely."

                    call success() from _call_success_10

                    "Old Elf" "Well, then, you can't possibly omit the tale of the Mitsuhide family! Oh, there is so much to write! You'd need a whole tome..."

                    girl.char "You know what... I may even write two."

                    "Old Elf" "Oh, yes, yes! Well listen, young woman, because I am the most unbiased and reliable authority on their distinguished history..."

                    girl.char "Undoubtedly... *sigh*"

                    $ r = True

                else:
                    "The old elf looks incredulous."

                    "Old Elf" "You? A writer?"

                    call failure() from _call_failure_4

                    "He bursts out laughing."

                    "Old Elf" "A writer! Do you expect me to believe a street girl knows how to read and write?"

                    "Old Elf" "Just go back to the gutter, where you belong!"

                    "Old Elf" "A writer! Ha! *laugh exageratedly*"

                    play sound s_door_close

                    "He slams the door shut."

            "Offer to do chores for him (Obedience: [_obedience])":

                girl.char "Wait, Sir! I do so respect your knowledge, and would be happy to serve you for the day, if you would care to impart your wisdom..."

                "She bows deeply."

                girl.char "Living alone here, surely you may have some chores you would need help with?"

                if _obedience >= 65:

                    "The man looks torn."

                    "Old Elf" "Well... You look a decent enough sort..."

                    call success() from _call_success_11

                    "Old Elf" "I do have a lot of chores... I haven't dusted the manor in a year... And laundry is piling up..."

                    girl.char "Let me help you, then! *determined*"

                    with fade

                    "[_name] spends a few hours putting the mansion into order."

                    "When she is finally done, she crumbles onto a chair, exhausted. But the old elf looks satisfied."

                    "Old Elf" "Why, it's nice to have everything tidy again! It reminds me of the old days..."

                    "The man seems in the mood to tell stories once more."

                    $ r = True

                else:

                    "The man spits on the ground."

                    "Old Elf" "Help me with chores? Why, you little minx, do you think I'm daft?"

                    call failure() from _call_failure_5

                    "Old Elf" "I know full well the likes of you! You intend to rob this place as soon as I have my back turned, don't you?"

                    "Old Elf" "Stealing from the glorious Mitsuhide family! The nerves!"

                    play sound s_door_close

                    "He slams the gate shut, hurling insults at her until she finally leaves."

            "Offer him sex" if _anal:

                girl.char "Hold off your horses, old man... I can make it worth your while."

                "She pulls on her tunic, hinting suggestively at her shapes. She lewdly caresses her lower belly."

                "Old Elf" "What?!? Mating with a human? Who do you take me for!!!"

                "He looks nervously around him, but doesn't shut the door. He steals glances at [_name]'s lewd body even as he protest."

                "Old Elf" "Arios says it's a sin for different races to mate..."

                girl.char "Well... There's always the back door. This isn't mating, so Arios doesn't mind, does He?"

                "Old Elf" "T-T-The... Back... Door?"

                "His face whitens, and sweat forms on his brow."

                girl.char "Don't play innocent with me, old man... You know what I mean."

                girl.char "Come on, won't you have some fun?"

                "Glancing nervously around him, the old elf grabs her by the shoulder and pulls her in."

                "Old Elf" "Get in, quick... The neighbors mustn't see us!"

                scene black with fade

                show screen show_event(girl.get_pic("anal", hide_farm=True, not_tags="group"))

                play sound s_moans
                girl.char "*moan*"

                "As soon as they are inside, the old elf wastes no time and starts fucking [_name] in the ass with surprising energy."

                "Old Elf" "How dare you, you little slut... Tempt me with your tight sinful asshole..."

                "His rock-hard cock belies his reproachful words."

                girl.char "Oh! You're big for an old man..."

                "Having always believed elves to be weak and fragile creatures, [_name] is surprised by the sheer size of the elf's junk."

                "Old Elf" "Don't you know elves are renowned for their stamina? This is one reason we were prized servants for prestigious households like the Mitsuhide's..."

                "He rams her ass again, stretching her hole even further."

                play sound s_aaah

                girl.char "Ahaha!!! [emo_heart]" with vpunch

                girl.char "(That man is old enough to be... I don't know, my great-great-grandpa, but he's stretching me to my limits...)"

                girl.char "Slow down, gramps..."

                "But the old elf completely ignores her, ravaging her ass even harder without a care in the world."

                "He treats her like a dirty anal whore and she can't help but feel aroused by it."

                "Old Elf" "Oh... I'm getting there..."

                "[_name] endures a little longer, clenching her butt muscles to try to ease him along."

                menu:
                    _("Let him cum inside"):                        "Old Elf" "OHOHOHOH!!!" with flash

                        show screen show_event(girl.get_pic("cin", "creampie", "cumshot", and_tags="anal", not_tags="group", hide_farm=True))
                        with doubleflash

                        "Eventually, the old elf discharges his seed right inside her tight butthole before letting her go, and she sighs as she feels warm semen leak out of her little by little."

                    "Make him cum outside":
                        "Old Elf" "Here is comes..." with flash

                        show screen show_event(girl.get_pic("cin", "creampie", "cumshot", and_tags="anal", not_tags="group", hide_farm=True))
                        with doubleflash

                        "[_name] takes out his cock from her butt with a loud pop, and he immediately starts spraying ropes of cum all over her butt and back."

                "Old Elf" "Oooh... I-I can't..."

                "The old elf is all out of breath and for a moment, [_name] worries about his health."

                hide screen show_event with dissolve

                "When he speaks again, however, he is as obnoxious as ever, and she soon wishes he had fainted."

                "Old Elf" "I can't believe I debased myself with a common slut. I, the last remaining servant of the House of Mitsuhide... What would people say..."

                girl.char "Well, my upper lips, at least, are sealed. Give me the information I came for, and you can forget about me."

                "Old Elf" "Hmph! Such impertinence!"

                "The old elf stops to consider his options, his confidence shaken. He realizes [_name] could damage his reputation if word of their tryst got out."

                call success() from _call_success_12

                "Old Elf" "Damn women... You're all as bad as the blue witch! Fine, ask your questions, and begone from this place!"

                $ r = True

    if r:
        girl.char "So... Did you say the Clan fell because of a woman?"

        "Old Elf" "A woman? More like a she-devil! She put her evil claws into our Prince's heart, and even beyond the grave she came back to haunt us!"

        girl.char "Even after her death, you say?"

        "Old Elf" "Oh, she looked innocent enough at first... The scheming deceiver..."

        hide old_elf
        show bg mizuki family2 at sepia
        with fade

        "Old Elf" "Like all women, I should have known she wasn't to be trusted..."

        show bg mizuki family2 at top_color with flashbackin

        $ mizuki_name = "Lady Sui"

        mizuki happy "Oh, my sweet baby... You're starving again, aren't you? No matter how much milk I give you, you always want more."

        mizuki "But after that, time to go to sleep. It's night time already."

        mizuki "Fear not the shadows, my dear son..."

        mizuki "For the stars are vigils that shall ward thee against the night..."

        "She hums an old nursery rhyme for her son."

        "Lord Mitsuhide" "Hey, Sui! What nonsense are you singing to my son again?"

        show bg mizuki family1 at top with dissolve

        mizuki "Oh! Welcome back, dear husband! The baby and I missed you. You must be exhausted from all this traveling..."

        "Lord Mitsuhide" "Indeed. I spent the whole month on horseback. I see my son has grown, I barely had time to see him since after he was born."

        show bg mizuki family2 at top with dissolve

        mizuki "Yes, he is growing well. He's always hungry! I think he will become a fine young man..."

        "Lord Mitsuhide" "A fine young man? Pah! Women are so unambitious. He's going to be so much more!"

        "Lord Mitsuhide" "As my heir, he will inherit the whole of Westmarch."

        mizuki normal "The whole of Westmarch? But our family is only one of the four Kingdoms..."

        "Lord Mitsuhide" "Not for long! Thanks to your father's gold, I was able to gather quite a sizeable force."

        "Lord Mitsuhide" "Our alliance with the Second Kingdom is fragile, but it will last at least until we topple the other two kings."

        "Lord Mitsuhide" "And then it's just a question of who will betray whom first... I intend to emerge the winner."

        "Lord Mitsuhide" "Mark my words: Our son will be the leader of a dynasty of kings, even emperors! We will build a Kingdom to last a Thousand years!!!" with vpunch

        mizuki "Hmm, okay... I'm sorry, my lord, I understand nothing of politics... I don't keep up with the news, I just take care of our baby all day and night. Without you it's been hard, he doesn't sleep much..."

        "Lord Mitsuhide" "Yes, well, such are the menial tasks that are fit for women. I'm sure you can find a chamber maid to help you."

        "Lord Mitsuhide" "By the way..."

        "He approaches her with a glint in his eye."

        "Lord Mitsuhide" "Put the baby down into his cradle, he's had enough to eat. You'll spoil him."

        mizuki "W-Why, my lord?"

        scene black with fade

        "Lord Mitsuhide" "Because I'm hungry too..."

        show bg mizuki rough1 at top with dissolve

        mizuki "Aaaah! My lord!" with vpunch

        play sound s_scream

        mizuki "It's so sudden... It hurts!"

        "Lord Mitsuhide" "Nonsense... A good wife should always be ready to serve her husband."

        mizuki "S-Sorry..."

        "Lord Mitsuhide" "Look at these... Still dripping milk, aren't they? We shouldn't let it go to waste."

        show bg mizuki rough2 at top with dissolve

        mizuki "Hmmm!!!" with vpunch

        "Lord Mitsuhide" "Here, drink some! Haha, your tits are so big that they actually reach your mouth!"

        mizuki "Ngggh!!!" with vpunch

        "Lord Mitsuhide" "How does it taste? It would be a shame to leave all of it to the kid, wouldn't it?"

        mizuki "Nggh..."

        "Lord Mitsuhide" "Hey, don't drink it all. Give me a taste."

        show bg mizuki rough3 at top with dissolve

        mizuki "Gaaah!!!"

        "Mitsuhide forcibly kisses her, tasting the milk off her mouth."

        "Lord Mitsuhide" "Hahaha, I love to fool around with young mothers!"

        mizuki "Y-Young mothers... You mean you've been with... Others?"

        "Lord Mitsuhide" "Uh? Oh, ahem... It's not like I have a fetish for banging the young wives of my servants, or anything, hahaha. *shrug*"

        mizuki "My lord... My back hurts from carrying the baby... Can we move to the bed..."

        "*SQUEEZE*"

        play sound s_scream_loud

        show bg mizuki rough4 at top with dissolve

        "Ignoring her, Mitsuhide squeezes her breasts with his full strength, making her moan in pain as milk spurts from her nipples."

        mizuki "OUCH!!! Please stop!" with vpunch

        "Lord Mitsuhide" "Keep screaming! Oh yeah, I'll... I'm..."

        play sound s_screams

        mizuki "Oh, ah, aaah!!! It hurts!"

        with flash

        "Lord Mitsuhide" "*loud grunt*"

        with doubleflash

        "He cums hard inside her, roughing up her tits again for good measure."

        mizuki "Aw... *sob*"

        "Lord Mitsuhide" "Phew. That was a good one. After being on the road for a month, I had missed it."

        mizuki "Ow..."

        "Lord Mitsuhide" "Not to mention you left me high and dry after giving birth... You kept saying it was too painful! Women are so weak."

        mizuki "S-Sorry..."

        show bg mizuki yukata1 at top with fade

        mizuki "I hope you are satisfied, husband."

        "Lord Mitsuhide" "Well, not really."

        play sound s_surprise
        show bg mizuki yukata2 at top with dissolve

        mizuki "Uh? Why not, my lord?"

        "Lord Mitsuhide" "I's not about your performance in bed... Although you could certainly improve. It's something of more import to our Clan."

        "Lord Mitsuhide" "You see, there are rumors that you are a Shaliaite. It may end up hurting us with the Arios Church."

        mizuki sad "B-But, husband... Of course, I follow Shalia. You knew that well before we were betrothed... My family are among the oldest Shaliaite families from Karkyr. We never hid it from anyone."

        "Lord Mitsuhide" "Okay, so I did, maybe, but I hadn't considered all of the ramifications. For now it is more expedient for us to say that I didn't know."

        "Lord Mitsuhide" "I trust you won't make a fuss about this at court? And stop singing these stupid rhymes to our son, for fuck's sake?"

        mizuki "B-But, my lord, I'm not even practicing Shalia worship or anything... It is just the traditions of my family; my father kept his faith as a show of respect for our lineage..."

        "Lord Mitsuhide" "Your lineage? Your father's lineage is over, Sui. As you are an only child, and a woman, your family is no more."

        mizuki "N-No, there's our son now... He can keep both of our heritage, and his life will be richer for it..."

        "Lord Mitsuhide" "What? Nonsense! I'm the father, the boy belongs to {i}my{/i} family as a matter of course, he doesn't need any other heritage."

        "Lord Mitsuhide" "And now that I have received all of your father's wealth after his untimely demise, we have no need to be attached to his house anymore."

        mizuki "B-But... We could still keep my father's memory alive... If it's Shalia's worship that worries you, my lord, we don't have to..."

        "Lord Mitsuhide" "Enough!" with vpunch

        "Lord Mitsuhide" "You are in over your head, wife. These are matters of state, not the ludicrous, romantic delusions of women."

        "Lord Mitsuhide" "Let us not speak about this again."

        mizuki "..."

        "Lord Mitsuhide" "I am going to the Second Kingdom for a month or two, we need to organize for the coming campaign."

        mizuki "So soon? But you only just got back! You have barely seen the boy..."

        "Lord Mitsuhide" "Yeah, well, I cannot make time for suckling babes over matters of State. I'll handle his education when he is old enough to hold a sword, as is proper."

        "Lord Mitsuhide" "There is a war coming. But by my estimate, it will be well over before winter."

        mizuki "O-Okay..."

        show bg mizuki yukata2 at sepia with flashbackout

        scene black
        show bg westmarch palace at top
        show old_elf
        with flashbackin

        "Old Elf" "In spite of his careful preparations, the Prince's campaign didn't go as well as he had hoped."

        "Old Elf" "Word had already got out to the Third and Fourth kingdoms that the Mitsuhide Clan was raising an army, and to make matters worse, the Second Kingdom betrayed us as we were assaulting the walls of Caprizio."

        "Old Elf" "Many attributed this bad luck to his heathen wife. A Shalia witch, no less!"

        "He spits in contempt."

        "Old Elf" "To think that wench used to give me candy as a young lad... Laced with what unholy concoctions, Arios knows!"

        "Old Elf" "The Prince used to slap me around, but I can see now it was for my own good, he was just honest and direct."

        "Old Elf" "And he was so good to my dear mother... Always visiting her when he was at the palace, their private conversations in her bedroom could last for hours..."

        "Old Elf" "Anyway, that evil woman was pulling the strings behind the good Prince's back, and our downfall continued."

        "Old Elf" "The real God was angry with the Clan, and it showed when the Arios Church withdrew its support for our plea."

        "Old Elf" "After a couple of years, it was obvious what needed to be done. The voices of reason were telling the Prince to remove this stain on our good name, and he was finally starting to listen."

        "Old Elf" "So it was with great relief that we learnt that he was repudiating her in order to marry a princess from the Fourth Kingdom."

        girl.char "He repudiated the mother of his son?"

        "Old Elf" "A fair and sound decision. To think that she couldn't even manage to give him another heir! That good for nothing succubus."

        girl.char "What happened to her?"

        "Old Elf" "Oh, well, soon after that, she died. She couldn't take the pain from being separated from our good Prince, who had been so good to her in spite of her treachery."

        girl.char "Wait, what? She died? Just like that?" with vpunch

        "Old Elf" "Took her own life in the forest, they said. A fitting end for a heathen..."

        girl.char "..."

        "Old Elf" "And for a few years things were good. We were winning the war, mostly. Lord Mitsuhide was now King, and the young prince was growing into a fine warrior in his stead, in spite of his questionable maternal heritage."

        "Old Elf" "But then disaster struck! The young heir died while storming the wall in the fourth battle of Caprizio. He was only sixteen..."

        "Old Elf" "We had barely finished mourning for him, that the King himself was brutally murdered in his bed by an assassin."

        "Old Elf" "And then his uncle, his brothers, their children, and their in-laws... Nearly all of them were assassinated within the span of a few years!"

        "Old Elf" "The Kingdom started losing the war decisively... But the other realms were hurting as well. Many other highborns died as well at the hand of the fearsome assassin."

        "Old Elf" "And that assassin was none other than..."

        play sound s_thunder
        with flash

        "Old Elf" "The cursed ex-wife's ghost!!!"

        girl.char "That woman killed them all? But she was dead!"

        "Old Elf" "The Blue Witch of the West, we called her."

        "Old Elf" "But I've seen the portraits commissioned by the militia, and I recognized her immediately..."

        "Old Elf" "The evil Kouchi Sui, coming back from the grave! She couldn't harm the virtuous Lord Mitsuhide while she was alive, so she destroyed him and his legacy, in death."

        "The elf looks tired and defeated, the burden of centuries suddenly showing in his wrinkles."

        "Old Elf" "It wasn't long before a good-for-nothing lordling upstart staged a coup, and overthrew the headless Mitsuhide family to take power in Telago."

        "Old Elf" "Things have only gone down from then... Now everyone in the Clan is long dead, or scattered across Xeros to escape the ghost's wrath."

        "Old Elf" "I alone remain in the husk of the palace. But I still have nightmares about the killer ghost in blue..."

        "He shivers, before falling silent."

        $ NPC_mizuki.flags["W1 unlock"] = True
        $ mizuki_name = "Mizuki"

        scene black with flashbackout

        girl.char "And that's all I was able to get from the old man. He showed me out right after that, and was quite rude about it."

        you "That's an important part of the story you've uncovered here, [girl.name]! You did well!"

        suzume "So Mizuki was repudiated, and killed herself... And then she came back a Kunoichi... How does this add up?"

        you "Was there more?"

        girl.char "Yes, there was one last place left for me to check..."
        

    else:
        "[_name] is left alone in the street, no closer to understanding the mysteries of the Mitsuhide Clan."

        scene black with flashbackout

        girl.char "And so I failed to learn more about that highborn family."

        girl.char "But there was one more lead I wanted to follow..."

    stop music fadeout 3.0

    girl.char "But it is a long story, and I need to catch a bit of sleep first."

    $ MC.rand_say("gd: Of course, silly me, you must be exhausted...", "ne: Oh, right, you'll be in better shape to tell the story tomorrow.", "ev: What! No! I want the rest of that story... Well, fine, but report to me as soon as you are done resting.")

    girl.char "Thank you Master. I will finish my story tomorrow."

    girl.char "(Gods, I can't wait to sleep in my bed again...)"

    $ calendar.set_alarm(calendar.time+1, StoryEvent(label="mizuki_w_back2", type="morning", call_args = (girl, )))

    sill "[girl.fullname] is now back to [brothel.name]. You may want to let her rest before putting her back on the job."

    return


label mizuki_w_back2(girl):

    $ _name = girl.name

    scene black with fade
    show expression bg_bro at top with dissolve

    you "So, [_name], are you ready to continue your story?"

    girl.char "Yes boss. So, I had one final place to check..."

    scene black with fade
    show bg forest at sepia with dissolve

    girl.char "One thing everyone I met seemed to agree on is that the 'Lady in blue' died in the forest nearby... So I needed to check it out."

    show bg forest at top_color with flashbackin

    girl.char "How can I possibly find my way in this huge forest? I need a guide before it gets dark..."

    "Voice" "Hey, city girl. What's a cute little birdie like you doing out here?"

    show hermit with dissolve

    "[_name] turns around to see a comely woman dressed in outdoor clothes, carrying a large basket of supplies."

    girl.char "Oh, hello Madam. Do you know this forest well?"

    woman "*chuckle* Oh, I do. that's where ol' Alka lives."

    woman "Alka's the name, by the way."

    girl.char "Oh, well, hello, Mrs Alka."

    woman "It's {i}Miss{/i} Alka, young one. *grin*"

    girl.char "...Miss Alka. I am looking for a certain place, could you perhaps tell me the way?"

    woman "Well, maybe sister. But would you be a dear and first help me carry this load all the way to my hut? It's me supplies for the month."

    "[_name] obliges, carrying some of the load while the woman follows. [_name] can feel her eyes on her back, lingering longer than they should."

    "They finally reach a large mud hut."

    woman "Here we are! Drop that stuff in the kitchen. Want some herbal tea?"

    "The hut looks lived in and cozy, featuring alchemist treaties and opaque vials neatly ordered on numbered shelves. [_name] gathers that her host is a witch doctor of sorts."

    girl.char "Err, no thank you. I'm kind of in a rush."

    woman "Is that so? And where is it that you're headed, sis'?"

    girl.char "I'm looking for a... Historical place. I heard a lady took her own life somewhere around here, 200 years ago."

    "The woman raises an eyebrow."

    woman "Stalking a suicidal wench from 200-years ago? Now that's a wild goose chase to go on, for a cute city girl like you..."

    girl.char "Have you heard about that place? It's supposed to be the last resting place of the Lady in Blue-"

    woman "Wait a jiffy. You're not thinking of offing yourself on her grave as some kind of stupid romantic gesture, are ya?"

    girl.char "N-No, absolutely not! I'm hoping to find..."

    play sound s_sigh

    girl.char "Well, I don't know... *discouraged*"

    girl.char "I mean, after 200 years, there's no chance that anything of interest remains in that place, is there? It's pointless..."

    "The woman puts down the last box and comes close to [_name]."

    woman "Well, were you anywhere but here at Alka's Hut of Wonders, I'd be inclined to say yer' right..."

    girl.char "'Hut of Wonders'?"

    woman "But you've found me. Mayhaps I can fix you."

    girl.char "R-Really? Can you?"

    woman "See, I'm something of a mystic. I have all sorts of potions to expand consciousness and reveal hidden secrets..."

    girl.char "You do?"

    woman "Yup. The folks from the city can't get enough of these remedies. And in return, I grab supplies, allowing me to live life in peace out here, far away from Arios freaks and the like."

    woman "As it happens, I know the ol' blue witch's resting place. It ain't far from here. An' I can cook ye the potion of Claire Voy-Hans, very useful."

    girl.char "You mean Clairvoyance?"

    woman "Uh, yep, that's her! So, ya want Alka's help?"

    girl.char "(Sounds awfully like a scam, but what other choice do I have...)"

    girl.char "All right then. How much do you want for it?"

    woman "How much? *grin* You don't get me, sis', I haven't got much use for coins out here..."

    girl.char "Then what?"

    "The woman gives [_name] an appreciative look from head to toe, and gives her a non-equivocal smile."

    woman "You know why I like living here? Because of the privacy, and the freedom to be who I wanna be... With whom I wanna be."

    "Understanding dawns on [_name]."

    $ r = False

    $ _body= girl.get_stat("body")
    $ _libido = girl.get_stat("libido")
    $ _fetish= girl.compare_preference("fetish", "indifferent") and _libido >= 35
    $ _bisexual= girl.compare_preference("bisexual", "indifferent") and _libido >= 35

    menu:
        _("Flaunt her goods (Body: [_body])"):
            "Hoping to get off easy, [_name] opens up her blouse."

            girl.char "You want to check me out? We can make it work..."

            if _body >= 50:

                call success() from _call_success_13

                "The woman licks her lips as [_name] flaunts her hot body in a suggestive way, stopping just short of undressing."

                woman "By the forest spirits, girl, you have a body to die for... Were I just ten years younger..."

                "She toys with the thought for a little while, but then decides she is happy with what she got."

                $ r = True

            else:

                call failure() from _call_failure_6

                "The woman looks at her, but seems ultimately unimpressed."

                woman "Well, don't take it the wrong way hun', but... Yer' not actually my type."

                woman "I'm sorry, I'm too busy to help ya now. Maybe come back next month, after I harvest some plants?"

                girl.char "Next month? I can't wait that long! I have to go back to Zan!"

                woman "Well, sorry to hear that. But yer' gonna have to sort that out on yer own."

        "Discuss intimate details (Libido: [_libido])":

            girl.char "Wait a... So you're a lesbian, are you? Oh, I have so many questions!"

            "[_name] steers the conversation towards the intimate, partly out of calculation, and partly out of personal curiosity."

            if _libido >= 50:

                call success() from _call_success_14

                "Picking up on her obvious interest, the woman relaxes as she answers [_name]'s many questions."

                woman "Ya know, I've laid with boys for a while, but it really ain't my scene."

                woman "I see plenty of girlfriends in town that are married to jerks... I am clearly a better match for them."

                woman "Maybe one day you'll see the light and join us... Why dontcha?"

                girl.char "Well... Perhaps, one day... *blush*"

                woman "In the meantime, I'm gonna help ya. Hope you'll pay it forward to the next outcast you meet."

                $ r = True

            else:

                call failure() from _call_failure_7

                "The woman sees clearly through her manoeuver, however, and her demeanor turns cold."

                woman "Listen, hun', I don't really enjoy idle talk about my sexual orientation. I can clearly see yer' not interested."

                woman "I'm sorry we can't help each other. But that's how life is, it ain't fair."

                girl.char "B-But, could you help me find..."

                woman "Nah, I changed my mind. Go get yerself a new hobby."


        "Offer to satisfy her fetish" if _fetish:

            girl.char "I see. Well, look, I'm not as familiar with women as I am with men, but..."

            girl.char "If there's something you would like to see... Maybe I can put on a good show for you."

            "The woman licks her lips."

            woman "Now you're talking my language... All right then, let's see what you can do... And I will return the favor."

            scene black with fade

            play sound s_dress

            show screen show_event(girl.get_pic("fetish", "service", and_tags=["bisexual", "lesbian"], not_tags=["sex", "anal"], hide_farm=True, allow_lesbian=True))

            woman "Wow... I didn't expect a young one like you to be so bold..."

            girl.char "I've had good training..."

            woman "So it seems... You're not uncomfortable, are you?"

            girl.char "I'm good... I hope you like it."

            woman "Oh, yes... I hope you don't mind me touching myself?"

            girl.char "Suit yourself..."

            "The woman starts rubbing her clit furiously while watching [_name]."

            play sound s_moans

            woman "*moan softly*"

            girl.char "Oh... It feels hot..."

            woman "You are hot, girlie..."

            "The woman makes dirty wet noises as she fingers herself, her other hand massaging her large tits."

            woman "Yes, keep at it, only a little longer..."

            play sound s_mmmh

            girl.char "Hmmm..."

            woman "Ohhhh..."

            "The woman clenches her teeth, sweating, as she circles her clit to push herself over the edge."

            play sound s_aaah

            woman "AAAH!!!" with flash

            "The woman shakes violently as an orgasm washes over her."

            with flash

            "[_name] bites her lips as she watches, turned on in spite of her discomfort."

            woman "Aaaah... Yer' good, little girlie... I didn't think you were this naughty when I met you..."

            girl.char "I guess I'm full of surprises."

            hide screen show_event with dissolve

            play sound s_dress

            girl.char "Now, remember your promise?"

            woman "Oh, yes, a promise is a promise..."

            woman "Let me grab a glass of water or three. And we can head to the pond."

            $ r = True


        "Offer to have sex with her" if _bisexual:

            girl.char "So, it seems some of our interests are aligned after all... Maybe I can get you to loosen up a little. *wink*"

            woman "Well, whadaya know, maybe you can, my pretty..."

            "Smiling at [_name], he woman opens the door to her bedroom and nods for her to enter."

            scene black with fade

            play sound s_mmmh

            show screen show_event(girl.get_pic("lesbian", "bisexual", hide_farm=True, allow_lesbian=True))

            girl.char "Hmmm..."

            play sound s_moans_mature_quiet

            woman "Aaaah..."

            woman "You do know your way around women..."

            girl.char "Of course. I am one."

            woman "I've laid with plenty of young inexperienced girls in the city... But you're different."

            girl.char "That's because young as I may be, I 'm far from inexperienced."

            woman "Hmmm... I can feel that..."

            "The two women grinds against each other and play for a long time."

            girl.char "Oh... Your... It's touching my..."

            woman "Relax, girlie. I can still show you a thing or two..."

            girl.char "If you do that, I'll..."

            woman "Please do..."

            girl.char "Aaaah... It's... Aaaaaah..."

            woman "*kiss*"

            play sound s_orgasm_young

            girl.char "AAAAAAHHH!!!" with flash

            "The woman expertly brings [_name] to climax, making sure to keep the stimulation going until it has completely washed over her."

            girl.char "P-Please! I'm too sensitive!"

            woman "Fufufu, you sweet child... Your body is like a fiddle, I love to play it."

            girl.char "Ugh... I can't feel my legs..."

            woman "I'll give you a moment to rest. then we'll head out."

            play sound s_sigh

            girl.char "Thanks... *contented sigh*"

            hide screen show_event with dissolve

            $ r = True

    if r:
        scene black with fade

        "The woman rummages through her cupboards, finally emerging with a small dusty vial containing a cerulean-colored liquid."

        woman "I knew I still had some of this elixir somewhere..."

        girl.char "What's that?"

        woman "It's the elixir of Claire Voy-Hans, I told ya. It reveals the unseen to the untrained eye - for a short while."

        girl.char "Will you make me drink it? *suspicious*"

        woman "Yep. But not here..."

        scene black with fade
        show bg full_moon at top with dissolve

        woman "...we must head out to the pond first."

        "Both women exit the hut. Night has fallen, but the forest is brightened with the light of the full moon."

        "Watching her step, [_name] follows the witch doctor down a narrow bushy path."

        girl.char "The pond?"

        woman "Yes. That's where your mysterious Lady took her own life."

        girl.char "What do you know about her?"

        woman "Not much. People have long claimed this forest to be haunted by her ghost."

        girl.char "And do you believe it?"

        woman "Nah. Ain't never seen anything out of the ordinary here. But you can tell her death left a lingering mark on this place. There are stories..."

        girl.char "Like what?"

        woman "That she still be lurking in the darkness, ready to slit your throat or eat your welps... The usual."

        girl.char "Yikes."

        woman "It isn't far now. Watch for prickly shrubs. Some of them are poisonous."

        girl.char "Whoah!"

        "[_name] takes extra care when walking the last few yards, but when she takes her eyes off the ground to look at the spectacle before her, she gasps in amazement."

        show bg moonlit_pond at top with dissolve

        $ girl.rand_say("ma: Whoah! Spooky! Do we really have to be here?", "id: Is this the place? It sure looks haunted... *shiver*")

        woman "This is the place. Where {i}she{/i} died..."

        girl.char "How... How would you know?"

        woman "'Tis the story I've been told by me gran', who got it from her gran', who got it from... Oh, I don't know, but people just know. It's here."

        woman "To this day some spurn lovers still come to this place an' take their own life. That's not what you intend, right, sweetie?"

        girl.char "Of course not. I'm just running an errand for my master."

        if girl.free:
            woman "Your master? Aren't you a free woman? *surprised*"

            girl.char "It's complicated..."

        else:
            woman "Ah, I see, that's the mark I've seen on you..."

        girl.char "Anyway, now that we're here... I don't know what to do? Where to look?"

        woman "We got us a bottle of elixir, remember?"

        "The woman hands her the vial. [girl.name] opens it and sniffs its content with a frown."

        woman "Drink it. It will reveal things to you."

        girl.char "Err... Why don't you drink it? You can tell me what happens afterwards?"

        woman "*chuckle* Who says I don't already know? Some things are to be experienced for yourself. You wouldn't believe everything I've seen anyway, kid."

        "Reluctantly, [girl.name] brings the vial to her lips, trying to focus on not disappointing her master."

        $ girl.rand_say("do: [MC.name]... You owe me one...", "su: I-I have no choice... Master [MC.name] said so...")

        play sound s_bubbling

        "[girl.name] gulps down the content of the vial."

        scene black with dream

        girl.char "Where... Am I?"

        "Ghost" "Where... Am I?"

        girl.char "Who... Who's there???"

        "Ghost" "Who... Who's there???"

        "[girl.name] shudders as she hears an eery voice echo her own in the pitch black of her dream."

        "Lord Mitsuhide" "It's me, Sui. So, this is where you've been hiding."

        girl.char "Sui? Hiding? I don't..."

        "Ghost" "My lord! Oh, I'm so relieved to see you! I-I'm sorry, I had to run into the forest..."

        show bg mizuki death1 at sepia with dream

        "A ghost materializes out of the dream's fog. It's Mizuki."

        show bg mizuki death1 at top_color with flashbackin

        mizuki sad "Something terrible happened... *sob*"

        "Lord Mitsuhide" "Terrible, indeed! I know just what happened, Sui."

        mizuki "Y-You do? *shocked*" with vpunch

        "Lord Mitsuhide" "Yes. You betrayed me, Sui. You consorted with my own kin, no less."

        play sound s_surprise

        mizuki angry "What! This is not at all what happened!" with vpunch

        "Lord Mitsuhide" "Don't you dare talk back, bitch!"

        scene black with fade
        play sound s_punch

        "*SLAP*" with vpunch

        show bg mizuki death2 at top with dissolve

        mizuki "Aw!!!"

        "Lord Mitsuhide" "You filthy, cheating whore... I should have expected as much from a Shalia cultist."

        mizuki "It's not true! *sob*" with vpunch

        girl.char "(What happened? What happened to you, Mizuki?)"

        "To [_name]'s surprise, her mind seems to become attuned with Mizuki's. She could probe her memories if she wanted."

        menu:
            _("Try to learn more"):                "She feels the scene morph before her eyes as Mizuki's memories become her own."
                call c3_mizuki_rape from _call_c3_mizuki_rape

                show bg mizuki death1 at top with dream

                "The vision fades back to the woods."

            "Leave it alone":
                "Whatever happened to Mizuki, [_name] can guess well enough. She focusses on the scene before her instead."

                show bg mizuki death1 at top with dissolve

        "Lord Mitsuhide" "It's over, Sui. I should have taken that decision long ago... You've been nothing but dead weight from the beginning."

        mizuki "B-But, my lord... Our son..."

        "Lord Mitsuhide" "{i}My{/i} son and heir will remain with me, of course. We have more than enough idle maids to take care of him."

        mizuki "You CAN'T! He's {i}my{/i} son too! I cared for him all his life..." with vpunch

        "Lord Mitsuhide" "Well, that ends today! He may cry for a week or two, but later he'll thank me, when I tell him of your treachery."

        play sound s_scream
        show bg mizuki death2 at top with dissolve

        mizuki "No!!! My baby... No! What should I do??? Please!" with vpunch

        "Lord Mitsuhide" "You can stay and live out here in the forest like an animal, for all I care."

        "Lord Mitsuhide" "But if you dare show your face again in {i}my{/i} city, I'll have you flogged and thrown in a cell to rot!" with vpunch

        play sound s_scream_loud
        mizuki "No!!!"

        "Mizuki's cry of anguish echoes through the empty night."

        scene black with fade

        "Time elapses in [_name]'s dream. She is overwhelmed with Mizuki's feelings of loss and betrayal until the vision starts to focus again."

        show bg mizuki death2 at top with dissolve

        mizuki "These monsters... They took everything from me..."

        mizuki "My family... My name... My boy... M-My baby... *shaking*"

        mizuki "There is no way out... No way... Except..."

        "Suddenly, something catches [_name]'s eye at the corner of the vision. Something shiny."

        play sound s_sheathe
        show bg mizuki death3 with dissolve

        "The cold glint of metal shimmers under the moonlight."

        "[_name] wants to scream at Mizuki to stop, but she is unable to make a sound."

        $ girl.rand_say("do: No! You have to fight back!", "id: No... Mizuki! Don't let them win!", "ma: Wait! You can fix this somehow!", "su: Oh no... Mizuki...")

        scene black with fade

        play sound s_sheathe

        pause 0.1

        play sound2 s_splat

        pause 0.3

        play sound s_splash

        show bg full_moon at top with dissolve

        "Something drops into the water. The reflection of the moon in the cold pond slowly becomes tinted with crimson."

        "An inert shape drifts across the pond, blue silk spreading out around it like moth wings."

        girl.char "That's it then... That's how she died."

        play sound s_mystery

        "*chilly wind*"

        girl.char "Uh? What's going on?"

        show bg full_moon at desaturate with dissolve

        "A large shadow passes over the moon, extinguishing the stars. The pond becomes perfectly still. [_name] feels as if the dream itself was becoming thick with dark magical energy."

        scene white with flash

        play sound s_chimes

        "A wave of cold washes over [_name], and she is blinded by white, icy light."

        $ girl.rand_say("mo: W-What is this...", "le: Well, fuck me!")

        play sound s_stone

        scene black with fade
        show bg mizuki intro2 at top with flash

        "Mizuki is now encased in ice that now covers the entirety of the pond. Her eyes are open."

        "[_name] can barely see her between the layers of thick ice, but one thing is unmistakable and sends a shiver down her spine."

        girl.char "That stare!!!"

        scene black with dream
        show expression bg_bro at top with flashbackin

        play sound s_sigh

        girl.char "Her eyes were hard as steel, and cold... The eyes of a killer."

        suzume doubt "And then you woke up?"

        girl.char "Yes. I was still in the forest, but the witch doctor was gone."

        you "Is it possible that it was all a fever-induced dream?"

        suzume "Who knows? Some psychotropes are known to give accurate visions."

        girl.char "Wait... There's more. When I woke up, there was something etched into the bark of the nearby trees. I'm sure it that wasn't there when we got to the pond."

        girl.char "It was like a claw mark. *shivers*\nBut I recognized that symbol."

        you "What was it?"

        girl.char "The mark of Shalia."

        "She crosses herself with the sign of Arios."

        suzume "Shalia... Of course!"

        suzume "Wait, do you think she intervened to protect Mizuki?"

        if MC.god == "Shalia":
            you "The full moon, the dark shadows, the ice... And taking a stand for the downtrodden... Everything points to the Goddess, all right."

        else:
            you "I don't know what sorcery it was that brought her back, but it seems clear that it is linked to Shalia."

        suzume "Let's not forget Mizuki's family were Shalia worshippers... This adds up."

        $ NPC_mizuki.flags["W2 unlock"] = True

    else:
        "The woman unceremoniously escorts her out."

        scene black with flashbackout

        girl.char "And that's as far as I got."

        you "Damn. I was hoping you'd find something about her death..."

        suzume "It was so long ago, though, it was a long shot."

        you "Still..."

    "[_name] seems spent after telling her entire story."

    if NPC_mizuki.flags["W1 unlock"] and NPC_mizuki.flags["W2 unlock"]:
        you "You did well, [_name]. You deserve some rest."

        you "Sill, go prepare a warm bath for her."

        girl.char "Oh, thank you!"

        $ girl.change_mood(20)
        $ girl.change_love(2)
        $ girl.change_fear(-2)

    elif NPC_mizuki.flags["W1 unlock"] or NPC_mizuki.flags["W2 unlock"]:

        you "I would have rather you uncovered the whole story, but that will have to do."

        play sound s_sigh

        girl.char "I did my best..."

        "She leaves you to your thoughts."

    else:

        you "Are you telling me I paid for this whole trip, and you couldn't even uncover a single piece of useful information?"

        girl.char "S-Sorry Master..."

        menu:
            _("Reassure her"):                you "Well, we knew it was a long shot. Still, Mizuki's secrets are probably out of our reach now..."

                girl.char "*fall silent*"

                you "You've had a long trip. Get some rest."

                $ girl.change_mood(-5)
                $ girl.change_fear(-1)

            "Scold her":
                you "Did you think that you were there on vacation? You owe me a great deal for your foolishness! Get ready to work extra!!!"

                girl.char "M-Master... *watery eyes*"

                $ girl.change_mood(-20)
                $ girl.change_love(-2)
                $ girl.change_fear(2)

        "[_name] rushes out and leaves you with your thoughts."

        you "Whatever Mizuki is hiding, I guess we won't be able to find out now..."

        $ NPC_mizuki["failed quest"] = True
        $ NPC_mizuki.location = seafront

    if NPC_mizuki.flags["quest W"] == "resolved" and NPC_mizuki.flags["quest K"] == "resolved" and not NPC_mizuki.flags["failed quest"]:
        $ NPC_mizuki.flags["quest success"] = True
        $ game.set_task("The Water Kunoichi: Talk to Suzume to confront Mizuki about her past.", "story2", 3)

        suzume "I believe we now know enough to expose Mizuki's secret."

        "You can call on Suzume from the {b}Visit city{/b} screen to progress Mizuki's story."

    return

label c3_mizuki_rape():

    scene black with dream
    show bg mizuki betrayal2 at top with flashbackin

    "Earlier that fateful night..."

    play sound s_chimes

    mizuki "Uh? Hello?"

    show bg mizuki betrayal1 at top with dissolve

    mizuki "Oh, it's you! Father-in-law, uncle."

    mizuki "It's quite a late hour for a visit. Forgive me, I didn't know that you were coming."

    mizuki "The baby is sleeping now, with the nanny. I can make you some green tea, if you want?"

    "Mitsuhide senior" "Cut the crap, girl." with vpunch

    show bg mizuki betrayal2 at top with dissolve
    play sound s_surprise

    mizuki "Uh? My lord?"

    "Mitsuhide's uncle" "You! You've been a thorn in our side for long enough."

    mizuki "M-My lords... I don't understand... I've never done anything to wrong you..."

    "Mitsuhide senior" "Oh, but you have! Just having you breathe the air of my son and grand-son's house is enough to shame our family."

    mizuki "M-My lord, please don't say such things... I am your daughter-in-law..."

    "Mitsuhide's uncle" "Not for long!"

    mizuki "What? W-what do you mean?" with vpunch

    "Mitsuhide's uncle" "It took us some time, but we finally found a good match for my nephew. Much better than some second-rate orphan from a forgotten family in Karkyr..."

    "Mitsuhide senior" "A young princess from the Fourth Kingdom agreed to marry my son, which suits our plans just fine. She'll be a fine addition to our family... And {i}she{/i} worships the True God, as is proper."

    mizuki "M-My husband won't stand for this! You can't just repudiate me!"

    "Mitsuhide's uncle" "Shut the fuck up, you stupid cow!" with vpunch

    "Mizuki stands there, stunned speechless."

    "Mitsuhide senior" "You know what, brother, you've got a point. She does look like a cow..."

    "Mitsuhide's uncle" "Yeah... Look at these udders..."

    "Mitsuhide senior" "You need to be put down in your place. Since your husband is not here to discipline you, I will have to do it..."

    play sound s_scream

    mizuki "Get away from me!"

    scene black with fade

    play sound s_punch

    mizuki "No!!!" with vpunch

    show bg mizuki betrayal3 at top with fade

    play sound s_screams
    with vpunch

    "The Mitsuhide elders pin Mizuki pin to the ground, removing her clothing. Even though she resists them at best she can, they simply slap her into submission."

    show bg mizuki betrayal4 at top with dissolve

    "Mitsuhide's uncle" "Stop screaming like that, whore! You'll wake your precious kid up..."

    "Mitsuhide senior" "Not so proud, now, Kouchi?"

    "Mitsuhide senior" "I wish your stuck-up father could see you... He thought our family were lessers, not worthy to marry into their midst. But now look who's on the ground, begging for mercy!"

    mizuki "No, let me go! I am your daughter-in-law!"

    "Mitsuhide senior" "And yet the old fool is dead now, with no heir to his name, his legacy scattered to the winds... While soon, all of Westmarch will bend the knee before the Mitsuhide clan!"

    play sound s_scream_loud

    mizuki "You are mad!!! Let me go!!!"

    play sound s_punch

    "Mitsuhide senior" "What's that? You can't keep your trap shut, can you?" with vpunch

    show bg mizuki betrayal5 at top with dissolve

    play sound s_surprise

    "The old man pinches and twists Mizuki's nipples viciously, causing her to moan in pain."

    "Mitsuhide senior" "Stupid bitch. You would have made a fine whore, but you are not fit to be anyone's wife. Much less my son's."

    mizuki "Stop!!! I-I am the mother of your grand-son!" with vpunch

    "Mitsuhide senior" "Yeah. That's about the only useful thing you ever did for us."

    "Mitsuhide's uncle" "That's right! The only useful thing you ever did was to spread your legs and pussy."

    "Mitsuhide senior" "Oh, by the way..."

    play sound s_screams

    mizuki "No! No!!!" with vpunch

    scene black with fade

    mizuki "NOOOOOOO..." with vpunch

    show bg mizuki betrayal6 at top with fade

    "Mitsuhide senior" "Bwahahaha! Not bad, for a young mother. I thought she'd be looser."

    "Mitsuhide's uncle" "Bro, you're really giving it to her! Serves her right!"

    mizuki "You monsters... Get away from me!" with vpunch

    "Mitsuhide senior" "Still talking? Brother, will you shut her up? You can smack her unconscious..."

    "Mitsuhide's uncle" "Oh, I have a better idea."

    show bg mizuki betrayal7 at top with dissolve

    play sound s_sucking

    mizuki "*muffled cries*"

    "Mitsuhide senior" "Ah, that's better."

    "Mitsuhide's uncle" "Look at her go! It was a shame to leave it all to her husband."

    "Mitsuhide senior" "Yes, we should have done that earlier. My son was dragging his feet to dump her."

    "Mitsuhide's uncle" "The flesh is weak, and she does have a great body. Regardless, after tonight, he's not going to cling onto her any more, is he?"

    "Mitsuhide senior" "Of course not. This should give him the little shove he needs."

    mizuki "HMPHHH!!!" with vpunch

    "Mitsuhide's uncle" "OOOH..."

    with flash

    "Mitsuhide senior" "RAAAH!"

    show bg mizuki betrayal8 at top with doubleflash

    "Both men cum hard, covering Mizuki's used body with their filthy juice."

    mizuki "*gasp* NOOOO..." with vpunch

    "Mitsuhide senior" "Aw, I'm getting too old for that shit! I'm spent!"

    "Both men lay there panting while Mizuki crawls away from them, hugging her clothes."

    "Mitsuhide's uncle" "Yeah, remember when we used to..."

    scene black with flash

    "Mitsuhide's uncle" "Hey, watch out!" with vpunch

    play sound s_sheathe

    mizuki "Get away from me! Get away from me!"

    "Mitsuhide's uncle" "That bitch! She took my knife!"

    "Mitsuhide senior" "Easy, girl..."

    play sound s_scream_loud

    mizuki "GET AWAY FROM ME!!! AAAAH!!!" with vpunch

    show bg okiya at top with dissolve

    play sound s_run

    "Mizuki turns back and run."

    "Mitsuhide senior" "Ha! She bolted..."

    "Mitsuhide's uncle" "Phew. I should have been more careful. Anyway, the kid's here. She won't go very far."

    "Mitsuhide senior" "Let us find my son. After all, it is his job to deal with his unruly wife..."

    "Mitsuhide's uncle" "I think you mean... 'Ex'-wife!"

    play sound s_maniacal_laugh

    "Both men burst into a cruel laugh, before the vision fades."

    scene black with fade

    return


label c3_unlock_mizuki():

    hide screen districts

    play music m_suspense fadein 3.0

    show bg mizuki intro1 at sepia with dissolve

    if NPC_mizuki.flags["quest success"]:
        suzume "You now know enough about Mizuki's past to confront her. Good."

        suzume "I think I know where she is. Do you want me to lead you to her now?"

        menu:
            extend ""
            "Yes":
                you "Sure. Let's see what this 'ghost lady' has to say about her own legend."
                $ NPC_mizuki.flags["hunt stage"] = 4
                scene black with fade
                show bg rooftop at top with dissolve
                call ninja_game(NPC_mizuki)

            "No":
                you "Maybe later."

        return

    if NPC_mizuki.flags["hint recap"]:
        menu:
            suzume normal "I think we've gathered enough intel about the Water ninja! What do you want to do?"

            "Can you recap the intel again?":
                pass

            "Investigate her past" if not NPC_mizuki.flags["failed quest"]:
                suzume "To continue your investigation, you must send someone to Karkyr and Westmarch."

                suzume "In that case, let's assign one of your girls to the appropriate quest."

                suzume "At the minimum you'll want someone who's loyal, but the more skills she has the better."

                if not NPC_mizuki.flags["quest K"]:
                    $ NPC_mizuki.flags["quest K"] = "available"

                if not NPC_mizuki.flags["quest W"]:
                    $ NPC_mizuki.flags["quest W"] = "available"

                $ selected_destination = "postings"

                jump teleport

            "Confront her":
                if story_flags["ninja hunt"] == calendar.time:
                    "You can only attempt to catch a ninja once a day."
                    return

                hide screen overlay
                scene black with fade
                show bg rooftop at top with dissolve
                call ninja_game(NPC_mizuki) from _call_ninja_game_6
                return

            "Look for her later in the city":
                return

    else:

        suzume normal "I think now we have a pretty good idea of what that old witch is up to!"

        you "Have we? Can you recap?"

    suzume "Sure. Here's what we've gathered so far."

    # Mizuki hints:
    # Various types of magic, ghost, link to Shalia, Westmarch story

    suzume "We know that Mizuki doesn't only use regular magic to disappear at will. We suspect she's using innate magic..."

    you "Like a ghost."

    suzume "Like a ghost."

    you "A ghost, and a Kunoichi? How did that happen?"

    suzume "I don't know. But your contacts mentioned Karkyr, and Westmarch. Seems like one of these two locations could hold the key to her secrets."

    you "Karkyr is bloody far, and Westmarch even further. I can't go there, I've got [brothel.name] and the girls to tend to."

    suzume bend "Sure, so someone should go in your stead."

    you "*stare at her*"

    suzume normal "..."

    you "*stare harder*"

    suzume "*inspects her fingernails*"

    you "*stare some more*"

    you "So... You're going, right?"

    suzume "Uh? Me? Hahaha, no way!"

    you "Why not???" with vpunch

    suzume "I am not running errands, and I'm not about to go pore over some old boring chronicles for you! Thanks but no thanks!"

    suzume bend "Besides, the reason I'm hanging around is to get fucked, and who's gonna fuck me if I'm on a road trip halfway through Xeros, hmmm?"

    "She pats your crotch hungrily as she says that."

    suzume normal "Why don't you just send Sill?"

    you "Sill? No way!"

    you "Who's going to iron my socks if she goes? Do you want me to wear unironed socks like a... Like a fucking beast???" with vpunch

    suzume "Send one of your girls then."

    you "One of my girls? Like on a quest?"

    suzume "Sure. Just make sure to send a trustworthy and capable girl. You don't know what skills she will need to succeed."

    you "But then I'd be missing her for weeks... Still, this might be the only way?"

    suzume "Tough choice."

    if MC.has_item(water_rune.name):
        suzume shrewd "Or, you know, you could just catch the bitch."

        suzume "Using that water rune of yours."

        you "The Water Rune? Would that work?"

        suzume doubt "Well, it turns water magic against its user... Perhaps the backlash would be strong enough to neutralize her other powers."

        suzume doubt "Worth a shot, anyway."

        if NPC_freak.flags["holding info"]:
            suzume "And dump the old fox into one of Papa Freak's magic dampening cells."

            you "I don't know, she's a master at escaping..."

            suzume normal "Hey, I'm just throwing shurikens at the wall here, see if they stick..."

        else:
            suzume "But you lack the means to hold her. We would have to deliver her to the Princess quickly and get it over with."

            suzume "Unless you can figure out a way to keep her locked up."

    else:
        suzume "It would be easier to just forget about the background check and catch her... But we'd need something that can neutralize her magic."

    $ NPC_mizuki.flags["hint recap"] = True
    $ NPC_mizuki.flags["hunt stage"] = 3
    $ NPC_mizuki.location = seafront

    jump c3_unlock_mizuki


label c3_mizuki_final_intercept():

    play music m_mizuki fadein 3.0

    scene black with fade
    show bg rooftop at top with dissolve

    show mizuki with dissolve

    mizuki "It's you again? Tsh... You really test my patience."

    if NPC_mizuki.flags["quest K"] == "resolved" or NPC_mizuki.flags["quest W"] == "resolved":
        menu:
            "Confront her about her past" if NPC_mizuki.flags["quest success"]:
                call c3_mizuki_end_investigation() from _call_c3_mizuki_end_investigation

                return "silent"

            "Try and capture her":
                pass

            "Leave for now":
                you "I'd rather not confront her just now."

                mizuki "Wise choice."

                scene black with fade
                stop music fadeout 3.0
                return

    # Attempt capture

    $ ninja = NPC_mizuki
    stop music fadeout 3.0

    if story_flags["ninja hunt"] == calendar.time:
        "You can only attempt to catch a ninja once a day."
        scene black with fade
        return

    if MC.has_item(water_rune.name):

        "You place the Water Rune in the appropriate slot on your toy-hammer, and it instantly melts and seeps inside the weapon. It seems colder to the touch."

        you "All right, Mizuki. Let's dance!"

        mizuki "Hmph. Wielding that big thing around like you've got something to compensate for. You think you can match me?"

        "Her voice stays cold and calculating, but you notice a hint of hesitation in her eyes."

        mizuki "(Damn, why am I feeling so... Cold... I never feel cold!)"

        "Mizuki's movement becomes clumsier, and her magic powers are draining. Time to put an end to this!"

        scene black with fade

        $ story_flags["ninja hunt"] = calendar.time

        call run_ninja_game(njgame) from _call_run_ninja_game_3

        return _return

        # results are in BKchapter2 - label intercept_mizuki()

    else:

        suzume "Her magic is at full capacity... It's useless now. We need to find something to counter it with."

        you "If we could turn her water magic against her, perhaps..."

    scene black with fade
    stop music fadeout 3.0

    return


label c3_mizuki_end_investigation():

    you "Hold it! I want to talk to you."

    scene black with fade
    show bg mizuki intro1 with dissolve

    mizuki "*sigh* It's unfortunate, but I really can't have you stalk me like this all the time."

    play sound s_mystery
    with flash

    "The air goes cold, and a menacing mist starts to form around Mizuki."

    you "Wait, Mizuki! Or should I say... Sui?"

    play sound s_fizzle
    show bg mizuki intro with dissolve

    "The mist dissipates, as Mizuki's shoulders slump ever so slightly."

    mizuki angry "That name... How do you know it?!"

    you "A little bird told me your life story."

    "It seems like she's finally listening."

    mizuki "Oh, really... And what do you think you know?"

label c3_mizuki_investigation_menu():

    if debug_mode:
        $ NPC_mizuki.flags["K1 unlock"] = True
        $ NPC_mizuki.flags["K2 unlock"] = True
        $ NPC_mizuki.flags["W1 unlock"] = True
        $ NPC_mizuki.flags["W2 unlock"] = True

    menu:
        "Talk to Mizuki about..."

        "Her wedding to Lord Mistuhide" if NPC_mizuki.flags["K1 unlock"] and not NPC_mizuki.flags["wedding answer"]:

            $ NPC_mizuki.flags["wedding answer"] = True

            you "I now know your real name: Sui Kouchi. And how you got married in Karkyr, to one Lord Mitsuhide from Westmarch."

            "Although she is usually pale as death, you could swear her face just became whiter."

            "You tell her what you know about her wedding in Karkyr."

            with fade

            mizuki normal "Kouchi Sui... That woman is long dead. She means nothing to me."

            mizuki sad "In fact, she never did mean anything to anyone... Only..."

            "Her voice shakes a little."

            you "But it was you, wasn't it?"

            mizuki normal "Me?"

            mizuki "Is a flamboyant butterfly the same as the ashen caterpillar that came before it? I don't know the answer to that."

            you "I only know bits and pieces of your story. But it seems that you were a nice woman."

            mizuki angry "A {i}nice{/i} woman? Ha! For all the good it did me. *frown*"

            mizuki "If anything, my story should serve as a warning for anyone who thinks being good will get you anywhere - in this life or the next."

            mizuki normal "I was a spoiled noble girl with a heart full of ideals and a head full of air."

            mizuki "I was wooed by the first playboy to show up at my dad's court... And, no surprise, it turned out he was only after my father's money."

            mizuki sad "All I wanted from this life was to be a good daughter, a good wife, and a good mother... And I failed on all counts."

            menu:
                extend ""

                "Don't be so hard on yourself":
                    $ NPC_mizuki.love -= 1

                    you "But you tried to do the right-"

                    mizuki angry "And what for? Every kindness I ever did, was repaid in cruelty." with vpunch

                    mizuki "It's only when I started to wield a blade, that I could begin to make things right."

                "Yes, you were weak":
                    $ NPC_mizuki.love += 2

                    you "You failed because you were too soft."

                    mizuki "Ha! You got that right. How I despise my old self for it."

                    mizuki "I paid dearly for my weakness."

                "Many people make mistakes":
                    you "Many people make mistakes. You couldn't know it would end like this."

                    mizuki "Yes, I was a young fool, and fools are a denar a dozen."

                    mizuki "But I'm old and deadly now. I don't make mistakes anymore."

            mizuki normal "I had to die and be reborn for it. But now, I know the hearts of men and women."

            mizuki "And I know that all most of them deserve is a knife between the shoulders."

            you "You're scary..."

            mizuki normal "Well, at least I'm still on the fence about you, sweetheart. That's why you're still standing."

        "Her family in Westmarch" if NPC_mizuki.flags["W1 unlock"] and not NPC_mizuki.flags["family answer"]:

            $ NPC_mizuki.flags["family answer"] = True

            you "I know you started a new family in Westmarch with your husband. You even had a child, a boy..."

            play sound s_thunder
            show bg mizuki intro1 with flash

            mizuki angry "DON'T MENTION HIM! NOT NOW! NOT EVER!!!" with flash

            play sound s_gust

            "Her voice booms, otherworldly. A gust of icy wind rush by you."

            "You keep your mouth shut. For the first time, she really looks like a spook to you."

            show bg mizuki intro with dissolve

            "Fury flickers in her eyes, then fades. The icy commotion dies down."

            mizuki normal "*sigh* I know you have nothing to do with these Mitsuhide pigs, nor with my son's fate. But his memory is mine to cherish."

            mizuki sad "They took my family from me, my honor, and even my life. But the one sin I will never forgive is, they killed my son."

            you "Didn't he die in battle?"

            mizuki angry "They sent a mere boy to storm a wall, when he had no idea what he was doing! They might as well have held the lance that pierced his gut."

            mizuki "They poisoned his mind with tales of heroism, while they comfortably sat on their ass in the back of every engagement..."

            mizuki "That heartless dog, my so-called 'husband', never lifted a finger to help raise him. But he sure knew how to send him to his death."

            mizuki "But soon, he shall be avenged. I'll make sure the last of their cursed blood is spilled and swallowed by the dark earth."

        "Her betrayal" if NPC_mizuki.flags["W2 unlock"] and not NPC_mizuki.flags["betrayal answer"]:

            $ NPC_mizuki.flags["betrayal answer"] = True

            you "I know how you were betrayed... Your husband repudiated you, chased you away from his city..."

            "She spits her next words angrily."

            mizuki angry "The fucking mongrel! The dirty whoreson! Let me tell you, his death was slow and painful... But everyday I regret not making it ten times worse."

            mizuki "I got all the others, too. His parents, his uncles, his brothers, his mistresses, his bastards... But he was my first kill, and the most satisfying."

            mizuki sad "What they did to me... They took my life away..."

            mizuki "I could have died in my bed 200 years ago, a happy and dumb wife, living only to pop out more heirs for the local lordling..."

            mizuki normal "Now, you and I would consider this kind of life appalling, but it would have been a blessing. I would have suffered much less."

            you "You took your own life..."

            mizuki "Did I really? I'm still standing before you, am I not? Good old Sui was so helpless, she couldn't even off herself."

            mizuki "Don't mistake {i}me{/i} for that hopeless fool. {i}She{/i} died."

        "How she came back from the dead" if NPC_mizuki.flags["K2 unlock"] and not NPC_mizuki.flags["dead answer"]:

            $ NPC_mizuki.flags["dead answer"] = True

            you "You died, didn't you? How did you survive? How did you make your way back to Karkyr?"

            mizuki normal "I haven't the faintest idea... And I don't care."

            mizuki "That old talking crystal at the Tower thought I received Shalia's blessing or some such nonsense. Maybe, maybe not, but that's not my concern."

            mizuki "All I know is that I gained powers. My natural affinity for water magic emerged much stronger, and that I could disappear like a ghost."

            mizuki "I like the power, but I couldn't care less where it comes from. I despise gods and their schemes, and bringing me back to this valley of tears was {i}not{/i} a kindness."

            you "Did it change you?"

            mizuki "Not immediately. When I was reborn, I could feel a rage inside, a white-hot fury I didn't think I was capable of."

            mizuki "I wanted revenge, so I honed my skills as a killer. It's good that the local ninja temple would have me, but I would have sold my body just as well to the first rogue I met, if he'd teach me how not to hold a dagger upside down."

            mizuki "But I was still soft. The more I trained, the more foolish my plans for revenge seemed to be. I dithered. I delayed."

            you "Something put your plans into motion."

            mizuki sad "Yes. As I was pondering whether I was ready to get my revenge for the umpteenth time, words came that my son had died in battle."

            "For the first time, tears start to stream freely down her face. The mighty ghost killer is crying, just before your eyes."

            mizuki "I couldn't believe it. My baby was a child still, barely sixteen."

            mizuki "It was his first battle, a siege. I was told he was the first over the wall."

            mizuki "He wanted to impress his dog of a father, to gain his approval... As if that worthless piece of shit could feel anything over than vanity and envy."

            mizuki normal "I left the temple immediately. Let me tell you, I never again hesitated."

            mizuki "I spent years hunting them all down... The Mitsuhide's, that cursed King whose army slaughtered my son, their relatives and relatives of their relatives..."

            mizuki "They were all oh-so-ambitious, so keen to build their legacy. I made sure their bloodlines were completely extinguished."

            mizuki "As I speak to you, my work on this earth is nearly done..."

        "Why is she really here" if (not NPC_mizuki.flags["K1 unlock"] or NPC_mizuki.flags["wedding answer"]) and (not NPC_mizuki.flags["W1 unlock"] or NPC_mizuki.flags["family answer"]) and (not NPC_mizuki.flags["W2 unlock"] or NPC_mizuki.flags["betrayal answer"]) and (not NPC_mizuki.flags["K2 unlock"] or NPC_mizuki.flags["dead answer"]):

            you "Thank you for telling me your story. I still don't understand how you came back from the dead, but regardless: why are you here now? In Zan?"

            mizuki normal "Hmph. You know my story now, so I might as well indulge you. But if you squeal, you know I won't hesitate to put a dagger in your heart."

            you "That is a given."

            mizuki "I told you I hunted the Mitsuhide's to the last, and I almost did."

            mizuki "But these cockroaches had a way to multiply, what with their dalliances and cousins and whatnot."

            mizuki "One by one I got them, even after they had fled to the four corners of the known world."

            mizuki "But one of them remains. A couple of decades ago, I learnt about a holdover from the Mitsuhide bloodline, the long lost heir to some bastard who fled Westmarch during the war."

            mizuki "When I got to him, he had already been killed, strangely enough. But he has a daughter..."

            you "Daughter? You mean you kill innocent women too?"

            play sound s_evil_laugh

            mizuki "Innocent women? Ha, you're too much!"

            mizuki "No Mitsuhide is innocent, whether it's the dogs, or the bitches. But regardless, this 'innocent woman' is a killer too. Or a soldier, anyway, that's the same thing."

            mizuki "And she's among the most protected in all of Zan."

            you "Why? Who is she?"

            mizuki "Very well, I shall tell you."

            mizuki "Her name is Mitsuhide Kenshin-"

            you "Kenshin??" with vpunch

            mizuki "... but she goes by her mother's name, Uesugi."

            you "Uesugi Kenshin? You want to assassinate the sitting Commander of the royal knights???" with vpunch

            mizuki "Yes. And what of it? Are you going to stop me?"

            you "B-But..."

            mizuki "When I came for her father, she was still a child, and even I have some principles. I gave her a few years."

            mizuki "But now she is an adult, and the head of the knights no less. She needs to meet her fate before she has time to spawn more Mitsuhide cockroaches."

            you "You can't just kill the head of the knights.."

            mizuki "Yes, she's well-protected. But every armor has a flaw."

            you "(She wants to kill Kenshin! What should I do?!?)"

            mizuki "Wait a moment... That long face... You know her, don't you?"

            you "M-Me? N-No, what makes you..."

            mizuki angry "Don't play games with me, kiddo! I can read you as well as an open book! You know her!"

            you "..."

            mizuki normal "What is she to you? A friend, a lover, an associate?"

            you "You're way off..."

            "Mizuki seems dangerously close to leaping at you, but after a fleeting instant, she relaxes with a grin."

            mizuki happy "Oh well, keep your secrets. It's not like anything you do could possibly save her."

            mizuki "In fact, you can tell her I'm coming for her. I always enjoyed sportsmanship."

            you "Erm..."

            mizuki "You know what, it's been nice catching up with you. And I enjoyed the heart-to-heart conversation, even if it was mostly one-sided. But I {i}truly{/i} have bigger fish to fry. You understand."

            mizuki "Bye now..."

            play sound s_stone

            show bg mizuki intro1 at top with flash

            pause 0.2

            show bg mizuki intro2 at top with dissolve

            "Mizuki raises an impenetrable ice barrier, up until you can't even see her through it."

            scene black with fade
            show bg ambush1 at top
            with dissolve

            you "Suzume, did you catch all this?"

            show suzume with dissolve

            suzume "Yes... Seems like the water ghost wants to ice your knight girlfriend, smack in the middle of the royal quarters."

            $ MC.rand_say("gd: We can't allow that to happen! I must warn her!", "ne: If we rescue Kenshin, she could be in our debt...", "ev: Kenshin has been nothing but a thorn in our side... Maybe if she had an 'accident', we could take advantage of the situation.")

            you "Let us speak to Kenshin. Also, she's not my girlfriend."

            suzume bend "She's not your girlfriend... Yet. *wink*"

            you "Wipe that stupid grin off you face, and carry this message to the Castle. Let Kenshin know we need to talk to her."

            suzume "Will do, boss."

            hide suzume with dissolve

            if not NPC_mizuki.flags["c3 path"] == "waiting":
                $ calendar.set_alarm(calendar.time, StoryEvent(label="c3_mizuki_kenshin_warning", type="night"))
            $ NPC_mizuki.location = None
            $ NPC_mizuki.flags["c3 path"] = "waiting"

            $ game.set_task("The Water Kunoichi: Wait for Suzume to get back from the castle.", "story2", 3)

            scene black with fade
            return

    jump c3_mizuki_investigation_menu


label c3_mizuki_kenshin_warning():

    "That night, you receive a courier from the Castle."

    you "It's a letter from Kenshin. Let's see what it says."

    call screen letter(header = _("Meet me at the Watchtower"),
                        message = __(MC.name + ",\n\nI have read your message, and it only confirms my suspicions. Someone has been spying on the castle recently, and I hope you have a good explanation for your involvement. My safety is of no concern to me, but I need to make sure the Princess is safe. Let us meet quietly by the Watchtower. I know a secret route, make sure that you are not being tailed as well. Be ready to explain yourself."), signature = "Kenshin")

    you "Dry and to the point, as usual. Well, let's meet her at the Watchtower then."

    $ game.set_task("The Water Kunoichi: Go to the Watchtower to meet with Kenshin.", "story2", 3)

    "Go to the {b}Watchtower{/b} to meet with Kenshin."

    $ add_event("c3_mizuki_kenshin_confrontation", chance = 1.0, type="city", location = "watchtower", order = -1, once = True, AP_cost = 1)

    return


label c3_mizuki_kenshin_confrontation():

    "Kenshin told you to meet her by the watchtower to discuss Mizuki's Plot, so you go."

    you "She isn't around... Maybe I got the place wrong?"

    you "(But hey, at least there's a cute girl coming my way...)"

    show bg kenshin secret at top with dissolve

    you "*whistle* Hey, babe, is your dad a-"

    you "Kenshin???" with vpunch

    kenshin "Hush, don't be so loud!!! Of course it's me, who did you expect?"

    you "It's just... Without your armor, I... You're..."

    kenshin "I'm what?"

    you "Cute- I mean... Feminine?"

    kenshin blush "W-What??? 'C-C-cute'???" with vpunch

    kenshin "(Arios! He called me 'cute'... Who does he think I am...)"

    kenshin "Ahem..."

    kenshin annoyed "Stop the nonsense already! You said the castle was in danger!"

    you "Well... Not the castle exactly, no. I called you here, because I need to talk to you."

    kenshin "Wait a..."

    kenshin blush "Did you call me here on a... On a date?"

    you "Uh? A date?"

    kenshin "(Oh no... It's a date, isn't it? I didn't prepare for this! What should I do???)"

    you "Of course not! I have grave news!"

    kenshin normal "Uh? So... It's not a date, then?"

    you "Nope."

    kenshin annoyed "Well... Let's hear it, then! What is it? Spit it out!" with vpunch

    you "Okay, okay! Why are you so pissed all of a sudden?"

    kenshin "Nothing! Let's get it over with, already! I have, err, duties to attend to."

    you "You see, there's a hired killer on your trail... "

    you "... a female ninja, all dressed up in a deep blue kimono, with big knockers and, erm..."

    you "I stopped noticing the rest after the big knockers."

    kenshin "A deep blue kimono?"

    kenshin "Like the one that woman is wearing, hiding over there behind the treeline?"

    show bg clearing with dissolve

    you "Oh no..."

    play sound s_gust
    show mizuki with moveinright

    mizuki "Fufufu, you've got a good eye, Lady Commander..."

    "Mizuki steps out from behind the trees."

    mizuki normal "I have to praise you, young woman. You move quietly when out of the castle, proving hard to track, even for me."

    mizuki "It's lucky I ran into your boyfriend here, following him proved much easier. Men are always so predictable."

    kenshin "He's not my boyfriend!" with vpunch

    you "I'm not her boyfriend!" with vpunch

    "You both interject at the same time."

    mizuki "Truly... Well, your relationship status does not interest me."

    mizuki "I have come for you, young woman, the last descendent of the Mitsuhide's..."

    kenshin "Mitsuhide? That name belongs to my traitor of a father! I don't want anything to do with it."

    mizuki "And right you are. But I'm afraid Mitsuhide blood runs in your veins still... And I am called to spill it."

    mizuki "It's good that [MC.name] got you here all alone, without armor or weapons... It will be an easy kill, kind of anticlimactic."

    play sound s_sigh

    mizuki angry "But I'm eager to get this over with."

    you "Wait!" with vpunch

    mizuki "What? Are you going to fight and protect the girl? Don't overestimate yourself, boy..."

    mizuki "There is really no need to spill your blood. Remove yourself from here, and you'll live. You might even gain from it."

    $ neutral_question = True

label c3_mizuki_kenshin_confrontation_menu:

    menu:
        extend ""

        "I can't let you harm Kenshin":

            $ MC.good += 3

            "You step away from Mizuki and draw your weapon."

            play sound s_sheathe

            you "No! I can't let you kill her, she's unarmed... Not on my watch."

            mizuki angry "Then you die, boy..."

            kenshin "STOP!!!" with vpunch

            kenshin "You, Lady! Why are you even trying to kill me?"

            mizuki "Why, indeed? Because you're a Mitsuhide from Westmarch, and all the Mitsuhide's must die. Your clan has wronged me, beyond what you can possibly imagine."

            kenshin "{i}I{/i} have wronged you? I have never even been to Westmarch! I only had one ancestor there..."

            mizuki "Well, it is one too many."

            mizuki "I nearly got your father, 15 years ago, but he died before I could get to him. And now that you are a grown-up woman, I'm afraid it is your turn to pay for the crimes of your ancestors."

            kenshin "Wait, my father? 15 years ago? But he disappeared when I was just a baby!"

            kenshin "What do you know about my father???" with vpunch

            "Mizuki shrugs."

            mizuki "The demons got to him first, and did the work for me. So there isn't much to tell. I helped the boy fend them off - he was no Mitsuhide."

            kenshin "The boy? What boy?"

            mizuki "The boy he was protecting, and... Who cares? I am not here to answer your questions!" with vpunch

            "Kenshin clenches her fists with fury."

            kenshin "You will tell me what you know about my father! If I have to punch out all your teeth first, I will!"

            mizuki "Ha! You have spirit, I'll give you that. But I am armed, and you are not."

            mizuki "It's time to say goodbye to this valley of tears. You'll be better off that way, I promise yo."

            play sound s_sheathe

            "Mizuki gets into a fighting stance. You ready yourself, siding with Kenshin, painfully aware that you are facing a deadly assassin with centuries of fighting experience."

            kenshin "Step aside, [MC.name]! Give me a weapon."

            if MC.playerclass == "Warrior":
                you "Are you sure, Kenshin?"

                "You see the resolve on her face, and know she's the better fighter. You hand her your blade."

            else:
                $ MC.rand_say("wi: It's a Wizard's staff. It won't be of any use to you...", "tr: Ahem, I only have a dagger on me... But my pet dragon will show up any second now! Hopefully.")

                kenshin "I can still use it to parry, so give it to me! If I die, it will be with a weapon in hand."

                play sound s_dodge

                you "Here... *toss your weapon*"

            play sound2 s_dodge

            pause 0.2

            play sound s_sheathe

            "Kenshin grabs it and immediately shoves you aside, just in time to parry Mizuki's first blow."

            mizuki "Ha!"
            with flash

            play sound s_clang

            kenshin "Watch out!"

            play sound s_clang

            with flash

            pause 0.3

            play sound2 s_clang

            mizuki "Hmph! You fight well, for a youngster."

            with doubleflash

            play sound s_clang

            pause 0.2

            play sound2 s_clang

            pause 0.1

            play sound3 s_clang

            pause 0.2

            play sound s_clang

            kenshin "And you're fast, for an old lady... *pant*"

            mizuki "Fufufufu..."

            "Ice particles begin to form in the air around Mizuki."

            mizuki "You {i}are{/i} a formidable fighter, I'll give you that. But {i}I{/i} am not a one-trick pony."

            "Mizuki starts summoning a powerful ice spell."

            "Kenshin cowers at the sight of magic, and she starts mumbling a prayer."

            kenshin normal "Fear not the shadows, for the stars are vigils that shall ward thee 'gainst the night..."

            you "What's that? A ward?"

            "Kenshin looks scared and vulnerable now, holding to her poor weapon for dear life."

            kenshin "Fear not the shadows... For the stars are vigils and shall ward thee 'gainst the night... *desperate*"

            "Mizuki freezes dead in her tracks."

            mizuki angry "You! W-What did you just say?" with vpunch

            kenshin "Fear not the shadows, for the stars-"

            mizuki "Stop, stop! This phrase you just used... Where did you learn it?!?"

            kenshin "What? That's just a prayer to ward off evil, everyone knows it."

            you "An old prayer then? I've never heard it."

            mizuki "No. Not everyone knows that."

            kenshin "Why do you even care! My father taught it to my Mom to soothe my cries, when I was just a baby."

            kenshin "And then he abandoned us. It's the last thing I remember from him."

            mizuki "Where! Where did your father learn it?"

            "You watch Mizuki, puzzled. Her face has changed, and now it's like she's the one looking scared."

            kenshin "From his parents before, maybe? Why does it even matter?!?" with vpunch

            mizuki normal "Who was your ancestor in Westmarch? Do you know, little girl?"

            "Her voice is suddenly very calm, begging almost. Kenshin hesitates, then shrugs."

            kenshin "Yes, I know. It was a great shame on my family... Until my father became a deserter, and made it seem trivial in comparison."

            you "What is that all about?"

            kenshin "My Westmarch ancestor was a noblewoman who fled from Telago, after falling with child, out of wedlock."

            kenshin "The father was some Mitsuhide prince, but he got himself killed in a siege before they ever had a chance to tie the knot. She was driven out of town in shame, but her child kept the name Mitsuhide, and ..."

            "Mizuki remains speechless, lost in her thoughts."

            kenshin "Here, is your curiosity satisfied now, you old harpy? Do you want me to unfold my genealogy all the way to the Goliath destroying the North?"

            play sound s_sheathe

            kenshin "Now, stand up and fight!" with vpunch

            with vpunch

            play sound s_clang

            "Something unexpected happens. Mizuki drops her weapon to the ground."

            mizuki sad "I see it now... I see it so clearly... Your face..."

            kenshin "What in Arios's name is going on here??? [MC.name], do you even know what this crazy woman is babbling about???"

            you "Maybe... I think I do..."

            mizuki "My son... My son lives... He lives through you..."

            kenshin "What?!?"

            you "Her son... Well, he got himself killed in a siege, two centuries ago. Just like the prince in your ancestor's story..."

            kenshin "Her son? Two centuries ago? What are you even saying???"

            you "I know, I know. Bear with me."

            you "Her son was young, but apparently old enough to fool around. It seems like you're the ultimate fruit of that dalliance."

            mizuki "'Fear not the shadows, for the stars are vigils and shall ward thee 'gainst the night'."

            kenshin "That's what I said!"

            mizuki "My son... He knew that nursery rhyme by heart. I wrote it for him, inspired by an old epic about Shalia."

            kenshin "I-It doesn't make any sense... Who is this lady???"

            "Kenshin is at a loss, and seems about to burst into a fit of anger or tears. But, surprisingly, you see that it is now Mizuki who is crying."

            kenshin "What in the name of Arios is going on?"

            mizuki "Kenshin, my child, I owe you the deepest apology. I'm so grateful now that I didn't kill your father. What a crime it would have been... But my son lives on!"

            kenshin "My father!!! You said you've seen him die, 15 years ago... Tell me what you know, please!"

            mizuki "Of course, my dear, this is the least I can do..."

            kenshin "Tell us, now. Who killed him?"

            mizuki "Not who... What. Demons from hell, I kid you not."

            you "Demons? You must be kidding!"

            mizuki "I never kid. I was as surprised as you are."

            kenshin "Why would demons go after my father?"

            mizuki "I don't know, but it's clear he was in hiding. He lived in a hut amidst the wilderness, alone with the boy..."

            kenshin "A boy? What boy?"

            mizuki "Oh, I'm not sure', a runt of 8 or 9 years... Not his, that's for sure. But he protected him with his life."

            mizuki "When I finally tracked him all the way to his hideout, I heard a commotion. I approached through the bushes, and there I saw this group of snarly demons fighting the old man and his child."

            mizuki "Your father fought like a lion, I have to say, but eventually he got gutted by claws and rended by fangs, and that was it."

            mizuki "The child was swinging a sword as big as him wildly to keep the demons away, but it was clear the demons were going to slaughter him. One of them clawed at his face and took his eyes out."

            mizuki "I was not going to reveal myself, but I don't know what came over me, I took pity on him. I never could stand to see a child suffer."

            mizuki "Before the demons could finish him, I jumped out of the bushes and struck the demons from the back when they least expected it. It was over before they knew I was on them."

            kenshin "What of the child?"

            mizuki "His wounds were nasty, but I helped him as best I could. There was nothing I could do about his eyes, though. He was a trooper, he didn't whine even once."

            mizuki "Once he was stable, I left him to rest inside the hut while I went looking for help. I arranged for word about the attack to reach the next village, hoping they'd go and rescue him."

            mizuki "But later I was told the rescue party only found your father's body... Perhaps more demons eventually came back to claim the boy, or he decided to hide from the villagers."

            you "A blind boy... Alone in the forest..."

            kenshin "Demons... Demons killed my father? But why? And who was that kid he was protecting when he should have been with us? With... Me..."

            mizuki "This is all I know. I'm sorry for you loss, child..."

            mizuki "But listen. I only want you to live a happy life. Do not dwell on the past as I have. It is not worth it."

            kenshin "Are you finally going to tell me what's going on? Hey! Come back!"

            play sound s_mystery

            hide mizuki with dissolve

            "Mizuki simply {i}vanishes{/i} into thin air. Kenshin is left rubbing her eyes in disbelief."

            kenshin "[MC.name]... Who was that lady?"

            "Her voice is calmer now."

            you "Well, if my calculations are correct... You were in the presence of your great-great-great-great-great-grandmother."

            kenshin "Ah."

            scene black with fade

            "You try your best to explain Mizuki's past to Kenshin, but she quickly gets lost in her own thoughts."

            "In the end she leaves without a word, and you wonder if any of your explanation has got through to her."

            "No blood was shed today. But is this really the last you'll see of Mizuki?"

            $ calendar.set_alarm(calendar.time+1, StoryEvent(label="c3_mizuki_goodbye", type="morning"))
            $ NPC_mizuki.flags["c3 path"] = "redeemed"


        "What's in it for me?" if neutral_question:
            $ neutral_question = False

            you "Suppose I were to get out of your way... What's in it for me?"

            mizuki happy "Aside from your life, you mean? Well..."

            "Mizuki steps close, putting her arm on your chest and whispering in your ear."

            mizuki "(Once I dispatch that Mitsuhide cockroach... I can be yours...)"

            you "Mine? *sweat*"

            "Mizuki giggles enticingly."

            mizuki "(Quite literally, my boy...)"

            "You wonder what she means by that, and it gets your mind racing."

            jump c3_mizuki_kenshin_confrontation_menu

        "Do what you will":

            $ MC.evil += 5

            $ NPC_kenshin.flags["dead"] = "mizuki ending"

            you "Well, you make a convincing argument. This isn't my fight."

            hide mizuki with dissolve
            show bg kenshin secret at top with dissolve

            kenshin "No! [MC.name], what are you doing?"

            you "Sorry Kenshin, but you're on your own. Maybe you should have thought twice before pissing me off at the castle."

            "You start to walk away, without looking back."

            kenshin "No-"

            play sound2 s_sheathe

            pause 0.3

            play sound s_scream_loud

            hide bg with pixellate

            "You try to block out the sounds of Kenshin's agony coming from behind you. Fortunately, it is quickly over."

            scene bg watchtower at top with fade

            show mizuki_rest with dissolve

            mizuki normal "'Tis done. My life - or death's - work, is over."

            you "Are you going to celebrate?"

            mizuki "No. I just feel nothing now. Empty."

            mizuki "As a witness, I should normally kill you where you stand, but... I feel too lazy to do even that."

            you "Whatever are you going to do?"

            mizuki "Well... There's nothing left for me to accomplish in this world. I guess I could just rest..."

            "Mizuki gives you a faint smile."

            mizuki "But I owe you, as the person who helped me get my final revenge."

            mizuki "Why don't you let me join you? I'll make myself useful."

            you "Me? I'm a brothel owner!"

            mizuki "I know that. I'd still join you."

            you "Really? Why?"

            mizuki "Now that killing has lost its edge, let's see if sex can still make me feel anything. I have centuries of experience; you won't regret it."

            menu:
                _("Accept Mizuki"):                    you "Sure, of course I'll have you."

                    mizuki "It is a deal, then. I'll meet you at your place."

                    $ girl = create_girl("Mizuki Ike", force_original=True, level=10)
                    $ girl.pop_virginity("other")

                    $ calendar.set_alarm(calendar.day + 1, StoryEvent(label="mizuki_brothel", type="morning", arg=girl))

                    call acquire_ninja(girl) from _call_acquire_ninja_3

                    scene black with fade

                "Refuse":
                    you "I'm not sure I need a ghost killer among my ranks, sorry. You should look elsewhere."

                    mizuki sad "Ouch, you could have been more of a gentleman about it. Rejection stings."

                    mizuki "So be it, I shall leave Zan forever. Pray that we never meet again."

                    scene black with fade

                    "Mizuki leaves, and you heave a sigh of relief to know there is one less killer in the city."

            you "I should inform the Princess about these unfortunate events. I hope the news of her Lady Commander's demise won't hit her too hard."

            $ NPC_mizuki.flags["c3 path"] = "revenge"

    $ game.set_task("The Water Kunoichi: Wait for events to unfold.", "story2", 3)

    $ calendar.set_alarm(calendar.time+1, StoryEvent(label="c3_mizuki_princess_debrief", type="morning"))

    return

label mizuki_brothel(girl): # Fires up every morning until Mizuki runs out of brothel events

    if NPC_mizuki.flags["bro service"] and NPC_mizuki.flags["bro sex"] and NPC_mizuki.flags["bro anal"] and NPC_mizuki.flags["bro fetish"]:
        call mizuki_brothel_last(girl) from _call_mizuki_brothel_last

    else:

        if not NPC_mizuki.flags["bro service"] and girl.get_log("perform service") > 0:

            $ NPC_mizuki.flags["bro service"] = True

            call mizuki_brothel_service(girl) from _call_mizuki_brothel_service

        elif not NPC_mizuki.flags["bro sex"] and girl.get_log("perform sex") > 0:

            $ NPC_mizuki.flags["bro sex"] = True

            call mizuki_brothel_sex(girl) from _call_mizuki_brothel_sex

        elif not NPC_mizuki.flags["bro anal"] and girl.get_log("perform anal") > 0:

            $ NPC_mizuki.flags["bro anal"] = True

            call mizuki_brothel_anal(girl) from _call_mizuki_brothel_anal

        elif not NPC_mizuki.flags["bro fetish"] and girl.get_log("perform fetish") > 0:

            $ NPC_mizuki.flags["bro fetish"] = True

            call mizuki_brothel_fetish(girl) from _call_mizuki_brothel_fetish

        $ calendar.set_alarm(calendar.day + 1, StoryEvent(label="mizuki_brothel", type="morning", arg=girl))
    return

label mizuki_brothel_service(girl):

    "Mizuki serviced a customer last night."

    scene black with fade
    show bg mizuki brothel service1 at top with dissolve

    play sound s_moans_mature_quiet

    customer "Hmmm, nice and wet... I love being with a real mature woman."

    mizuki naked "Ah, it's good, keep doing that..."

    "The customer is young and inexperienced, but Mizuki is teaching him how to please a woman."

    customer "My girlfriend's my age, but she won't let me do anything... It's much better to do it with you!"

    mizuki "I'm sure it is... What won't she let you do?"

    customer "Well, anything beyond missionary, really..."

    customer "I even bought a toy for her, but she won't even try it."

    mizuki "Hmmm... You wouldn't happen to have this toy with you, would you?"

    show bg mizuki brothel service2 at top with fade

    play sound s_moans_mature

    mizuki "Oh, yes!"

    customer "Hehe, this is great! You're getting so wet now, taking it all in like it is nothing..."

    mizuki "Your girlfriend is a real idiot, but it's her loss..."

    mizuki "When you feel an urge she won't satisfy, you should come to me.... Hmmm..."

    customer "Sure thing! I will, Ma'am!"

    mizuki "Now, fuck me harder with that thing, will you? I'm getting close..."

    show bg mizuki brothel service3 at top with doubleflash

    play sound s_orgasm_fast

    mizuki "Aaaah!!! [emo_heart]"

    scene black with fade

    $ girl.change_stat("service", dice(3) + 2)
    "Mizuki came hard as she kept playing with the customer. She became better at {b}service{/b}."


    return

label mizuki_brothel_sex(girl):

    "Tonight, Mizuki is giving a lesson to a new customer."

    show bg mizuki brothel sex1 at top with dissolve

    mizuki naked "Now, this is what the body of a real woman looks like."

    customer "A-Amazing..."

    mizuki "Our lesson for today will be: the cowgirl position. You know what it is, right?"

    customer "I-I've read about it..."

    mizuki "Read about it? Oh, boy, reading won't get you anywhere. It's practice you need."

    mizuki "Let me show you..."

    show bg mizuki brothel sex2 at top with dissolve

    play sound s_ahaa

    mizuki "Ahaaa! [emo_heart]" with vpunch

    play sound s_moans_mature_quiet

    customer "Ooooh..." with vpunch

    mizuki "Now, you want to move slowly at first... Like this..."

    "The man complies, sweating as he basks in the view of Mizuki's erotic body."

    mizuki "Yes... Make me nice and wet, then go faster..."

    show bg mizuki brothel sex3 at top with dissolve

    customer "Oh, aah, aaaah..." with vpunch

    mizuki "That's it! Keep going harder!"

    play sound s_moans_mature
    show bg mizuki brothel sex4 at top with dissolve

    mizuki "Oh, yes!" with vpunch

    "Mizuki is bouncing on her boy's dick."

    customer "Oh, it's too much, it's too..."

    mizuki "Don't stop! I'm cumming!!!" with vpunch

    show bg mizuki brothel sex5 at top with flash

    customer "UUUGH!"

    with doubleflash

    mizuki "Aaaaah!!!"

    "Mizuki cums as the man pops out his dick and starts spraying cum all over her body."

    with flash

    mizuki "Fufufufu... That was over quicker than I expected... But it was fun."

    mizuki "Give me a moment to clean up. You can leave payment on the table."

    scene black with fade

    $ girl.change_stat("sex", dice(3) + 2)
    "Working in the brothel, Mizuki got better at {b}sex{/b}."


    return

label mizuki_brothel_anal(girl):

    "Mizuki had an interesting time with a customer last night."

    show bg mizuki brothel anal1 at top with dissolve

    mizuki naked "What's up, big boy? You've been staring at my ass this whole time..."

    customer "I-I'm sorry Ma'am... It's that I... Uh..."

    mizuki "What, are you afraid to ask me something?"

    customer "Well, I just, ahem... I always wanted to try... {size=-12}anal sex{/size}..."

    mizuki "What was that? I couldn't hear?"

    customer "{size=-8}A-anal sex{/size}..."

    mizuki "Ah, you want to try {size=+10}anal sex{/size}?"

    customer "Hush, not so loud!!!" with vpunch

    mizuki "Relax, it's a brothel... Believe me, these walls have heard a lot worse."

    customer "B-But my mother told me Arios says it is unnatural to use the arse for anything else than poo-poo..."

    mizuki "Well, I am not your mom... Although maybe I look like her? *wink*"

    customer "*gulp*"

    mizuki "Why don't you try me..."

    show bg mizuki brothel anal2 at top with fade

    play sound s_aaah

    mizuki "Aaaah!!!" with vpunch

    customer "Oooh! I'm in It's incredible!!!"

    mizuki "Yes, nice and easy boy... You can go deeper..."

    customer "I will, I'm just..."

    play sound s_splat

    "Mizuki expertly squeezes his dick with her inner muscles."

    show bg mizuki brothel anal3 at top with flash

    play sound s_surprise
    mizuki "Oh!"

    customer "Aaaah!!!"
    with doubleflash

    customer "Urg... I'm sorry Ma'am, I just couldn't hold it..."

    mizuki "Well, it's all right, stud. But you time is not up yet... Why don't you go for another round?"

    customer "O-Okay... "

    play sound s_moans_mature

    show bg mizuki brothel anal4 at top with dissolve

    "The customer keeps fucking Mizuki, avoiding her ass this time as it was too intense."

    mizuki "Oh, yes, harder!"

    show bg mizuki brothel anal5 at top with flash

    play sound s_orgasm

    mizuki "Oh, aaah, aaaaah!!!"

    with flash

    "Eventually, Mizuki leaves the customer completely spent."

    scene black with fade

    $ girl.change_stat("anal", dice(3) + 2)
    "The encounter leaves Mizuki wanting for more. She has become better at {b}anal{/b} sex."

    return

label mizuki_brothel_fetish(girl):

    "Tonight, Mizuki is helping a customer accomplish one of his long-time fantasies."

    show bg mizuki brothel fetish1 at top with dissolve

    mizuki naked "Whoah, you're actually really good at knots..."

    customer "Yes, it comes with the trade..."

    mizuki "So you're a sailor?"

    customer "No, a hangman."

    mizuki "I see..."

    customer "It wasn't my first choice, you know. No little kid dreams of becoming a hangman."

    mizuki "I'm sure."

    customer "No, what I always wanted to be, was..."

    mizuki "Yes?"

    customer "A torturer!" with vpunch

    mizuki "Oh."

    customer "But there are only limited opportunities in this field, you know, only a handful of positions and the competition is savage..."

    mizuki "I can only imagine."

    customer "So that's why I only do it as a hobbyist, you see..."

    mizuki "Well, you're the one paying, so you call the shots..."

    show bg mizuki brothel fetish2 at top with dissolve

    play sound s_scream

    mizuki "Aaaah!" with vpunch

    "Mizuki squirms in pain as the customer drips hot wax on her exposed body. In spite of her supernatural abilities, it still stings."

    mizuki "Aaaah..."

    "But even pain is a welcome feeling for someone who became jaded over two centuries. Her nipples get erect in spite of herself."

    customer "Look at these naughty nipples... We'd better do something about these."

    show bg mizuki brothel fetish3 at top with dissolve

    play sound s_screams

    mizuki "AAAAH!" with vpunch

    mizuki "NGGGH..."

    "Mizuki clenches her teeth as the customer uses additional candles to chastize her tits. Still, she endures with a mix of pain and excitement."

    customer "Look at this, you're getting wet over being tortured..."

    customer "Well, it's perfect for the finishing touch. I brought these for you."

    show bg mizuki brothel fetish4 at top with dissolve

    play sound s_laugh

    mizuki "Flowers? For me? Aw, you shouldn't have..."

    customer "Ah... That was great, thank you... I'm going to tell everyone at work about you!"

    customer "I guess it won't do much good though, since I'll hang them by the neck shortly thereafter... Unless they come back in the afterlife, haha."

    mizuki "Well, stranger things have been known to happen..."

    scene black with fade

    $ girl.change_stat("fetish", dice(3) + 2)
    "Mizuki has become better at {b}fetish{/b}."

    return

label mizuki_brothel_last(girl):

    "Late at night, in [MC.name]'s room..."

    scene black with fade
    show bg mizuki brothel final1 at top with dissolve

    play sound s_mmmh

    mizuki naked "Oh, ah, aaah!!!" with hpunch

    you "I have to commend you, Mizuki... You've taken to your new life in [brothel.name] in the blink of an eye."

    show bg mizuki brothel final2 at top with dissolve

    play sound s_ahaa

    mizuki "It's because I have no other purpose now, Master..."

    mizuki "I spent years orchestrating my vengeance... Now that it's done, I'm just happy to let everything go..."

    play sound s_aah

    mizuki "Aaaah!" with hpunch

    "You thrust harder inside her dripping pussy, making her tremble with lust."

    you "Very good, Mizuki. I expect you to be a perfect little cum dump for me and my customers. I trust it won't be a problem?"

    mizuki "N-Not at all, Master [MC.name]... I'm happy to be used and stop worrying about what to do..."

    play sound s_scream

    mizuki "Aaaaaah! [emo_heart]" with hpunch

    show bg mizuki brothel final1 at top with dissolve

    "Fucking her harder, you smile as the formerly haughty ninja becomes your plaything."

    with flash
    play sound s_scream_loud

    you "Take that!"

    show bg mizuki brothel final3 at top with doubleflash

    play sound s_orgasm_fast

    mizuki "Ah, yes, yeeeees!!!"

    with flash

    "Mizuki has now completely adjusted to life in your brothel. She has gained {b}obedience{/b}."

    $ girl.change_stat("obedience", dice(6) + 2)
    $ unlock_achievement("mizuki revenge")

    return

label c3_mizuki_goodbye():

    scene black with fade
    "As you enter your bedroom, you are surprised to find an unexpected guest."

    show bg mizuki betrayal1 with dissolve

    you "Mizuki?"

    mizuki happy "Hello again, [MC.name]. Come in, I made you some tea."

    "You sniff the beverage carefully, raising a suspicious eyebrow."

    you "You're not... Having second thought about assassinating me, are you?"

    mizuki "Who knows! Maybe I am..."

    mizuki "But not by poison. With me, you get to choose your means of execution... It's the least I can do."

    "You are relieved to hear she is speaking in jest."

    you "Well, in that case... I would choose to orgasm to death, my Lady."

    play sound s_laugh

    mizuki "Fufufu... I had no doubt this would be your choice."

    mizuki "But fear not, I have not come to kill you, rather to thank you."

    you "About Kenshin?"

    mizuki "About everything. You went to great length to learn about my story, and help me..."

    you "I had my reasons."

    mizuki "No doubt. But it doesn't make me any less appreciative."

    you "So... Do I get a reward, then?"

    if NPC_mizuki.love >= 6:

        mizuki "Well... I guess a reward is in order. *wink*"

        "Mizuki steps closer to you, rocking her hips slightly. Not for the first time, you notice how her kimono has a tendency to slip off and reveal a lot of skin."

        you "Ahem... Is death by orgasm still on the table?"

        "Mizuki grins a wolfish smile, reaching you. She places her soft hands on your chest."

        mizuki "I would think so..."

        you "Err... On second thoughts, can you make it just within an inch of my life?"

        mizuki "We'll see if I can behave myself..."

        "Before you can object any further, Mizuki forcefully pushes you down on the bed."

        scene black with fade
        show bg mizuki sex1 at top with dissolve

        you "Oh!"

        play sound s_sucking

        mizuki naked "I saw you looking at my boobs for the longest time... It's time you got to enjoy them, don't you think?"

        you "They are certainly something... Hmmm..."

        "Mizuki's expert tongue is remarkably agile, and soon you get lost in the feeling."

        mizuki "I have to say, your nice fat cock is also enticing... I wanted to know what it tasted like."

        show bg mizuki sex2 at top with dissolve

        "Without further ado, Mizuki takes your whole length in her hungry mouth, bringing you new levels of pleasure."

        with vpunch

        mizuki "Nggh... *suck*"

        you "Oh, it's nice..."

        "Mizuki is sucking your dick with gusto, using her soft large breasts to massage your shaft. It's not long before she gets you close to cumming."

        with vpunch

        mizuki "Mmmmh..."

        you "Ugh..."

        with flash

        mizuki "Nggh?"

        show bg mizuki sex3 at top with doubleflash

        "Mizuki is surprised as you cum, but keeps most of your semen in her mouth."

        you "Fuck, yes!!!"

        "You shoot your load in the ninja's throat, making her swallow your sticky cum."

        play sound s_mmh

        mizuki "*slurp* Mmmm..."

        show bg mizuki sex1 at top with dissolve

        "She gives you a slutty look, savoring your seed in her mouth."

        you "Phew..."

        mizuki "Delicious. But I'm sure you still have a lot of life energy left..."

        "As if to answer for you, your cock gets rock hard again only after a few licks."

        mizuki "I may have slipped some vigor-enhancing plants in that tea..."

        you "I knew it!"

        mizuki "Now, stud, why don't you show me how you handle the main course..."

        you "Yes, boss."

        scene black with fade

        "It is your turn to push Mizuki down onto the bed."

        show bg mizuki sex4 at top with dissolve

        play sound s_ahaa

        mizuki "Taking initiative now! I love it. [emo_heart]"

        "Mizuki is not wearing any panties, and your cock easily slides inside her wet pussy."

        play sound s_aaah

        with hpunch

        mizuki "Aaaah!"

        "You watch her tits bounce as you start fucking her."

        with hpunch

        mizuki "Aaah, that's right... Just like that..."

        "Mizuki closes her eyes, enjoying the sensation."

        you "You're plenty warm inside for a ghost..."

        mizuki "Hey, don't be rude... Hmmm..."

        mizuki "When I'm in the moment, I'm as much flesh and blood as you are."

        with hpunch

        you "I can attest to the 'flesh' part..."

        play sound s_scream

        show bg mizuki sex5 with dissolve

        mizuki "Ahaa!"

        "Mizuki cries out as you hit her deepest parts. Ghost or not, she is still a woman."

        play sound s_moans_mature

        mizuki "Ah, yes... More! Give me more!"

        "Mizuki plays with her tit, spreading her legs wider."

        "You continue fucking her pussy harder, enjoying the feeling of her tight walls around your cock."

        you "You like it rough, don't you?"

        with hpunch
        play sound s_aaah

        mizuki "Aaaah! What can I say... I'm not a fragile old lady... You're welcome to pounce..."

        "You don't need to be told twice. The more you fuck Mizuki, the more you feel yourself losing control."

        you "Ugh, I'm getting close again."

        mizuki "Don't hold back, dear... Just fill me with your cum... Make me feel alive!"

        you "Ohhh..."

        with flash

        play sound s_scream_loud

        mizuki "Aaaah!"

        show bg mizuki sex6 at top with doubleflash

        mizuki "(Make me feel alive...)"

        with flash

        mizuki "(One last time...)"

        "You both take a moment to catch your breath, before going back for another round..."

        scene black with fade

        $ MC.change_prestige(3)

        "Now fully sated, you drift away into half-sleep, only to be roused by a chill breeze upon your bare skin."

        play music m_wind

        you "Is the window open? Mizuki?"

        "Glancing around, Mizuki is nowhere to be seen amidst the tangled sheets."

        show bg full_moon at top with dissolve

        "The window stands wide open, and you sigh."

        you "Another shadowy ninja trick? Let me close this..."

        play sound s_mystery



    else:
        mizuki "We've had our differences... But in the end, you've helped me, and it was worth a lot to me."

        mizuki "After tonight, we won't see each other ever again. I want you to have this. It served me well."

        play sound s_dress

        show bg okiya at top with dissolve
        show mizuki naked with dissolve

        "Mizuki drops her kimono to the ground."

        you "Uh??? What?"

        "Mizuki bows slightly, and heads out into the night."

        hide mizuki with dissolve

        you "Hey! Where are you going, crazy lady!"

        show bg full_moon at top with dissolve

        "You step outside right after her."

    "A cold shadow seems to dim the light of the moon, sending a shiver down your spine."

    you "M-Mizuki?"

    play sound s_spell

    show bg mizuki goodbye1 at top with dissolve

    "To your surprise, Mizuki materializes from thin air. But it is more than a ninja trick: she is hovering high above the ground, surrounded by a ghostly glow."

    "Her eyes are soft yet distant, weary as if they were witnessing the passing of eons."

    mizuki naked "I am tired, [MC.name]... And I am done. It is time for me to join my son."

    you "You... you mean..."

    mizuki "I never knew joy in the life I was given. I got more than my share of hatred, pain and tears."

    mizuki "But thanks to you, now, at the end... I can finally make peace with it."

    you "Mizuki..."

    mizuki "Farewell, [MC.name]. I do not believe in the afterlife... But as a spirit, I have to say... Stranger things have happened."

    play sound s_mystery

    show bg mizuki goodbye2 at top with dissolve

    you "Mizuki!"

    show bg mizuki goodbye3 at top with dissolve

    mizuki "Godspeed, [MC.name]..."

    play sound s_spell

    show bg full_moon at top with dissolve

    "With her face finally peaceful and at rest, Mizuki fades into the air, her form dissolving like mist under the moonlight."

    $ unlock_achievement("mizuki redeemed")

    "Thus disappeared from the face of Xeros, the legendary phantom Kunoichi."

    scene black with fade

    stop music fadeout(3.0)

    "The princess will want to hear of this... But for now, your mind drifts, not finding sleep until the wee hours of the morning."

    call receive_item(mizuki_kimono2, use_article=False) from _call_receive_item_47
    call c3_end_story(NPC_mizuki) from _call_c3_end_story_4

    return


label c3_mizuki_princess_debrief():

    scene black with fade
    show bg castle at top with dissolve

    "As expected, the events of the past few days have earned you a summon to the Royal Palace."

    play music m_palace fadein 3.0

    show bg palace corridor at top with dissolve

    knight "Come. The Princess will see you shortly."

    show bg palace room at top with dissolve
    show kuro with dissolve

    "Kurohime welcomes you by herself, dismissing the knight. She looks tired and concerned."

    kuro "[MC.name]... It is good to see a friendly face."

    if NPC_kenshin.flags["dead"]:
        kuro "As I'm sure you've heard, Commander Kenshin was brutally killed in broad daylight just a couple of days ago."

        "You hold your breath, hoping that she didn't get wind of your involvement in that matter."

        kuro "Details are scarce, but it seems she was murdered by one of the Kunoichi that's been rampaging around the city."

        kuro "It is crucial we put an end to this string of assassinations, or my family will lose what little sway we still have over the Court."

        you "What do you mean?"

        kuro "The Knight Commander was my right hand. We did not always agree on everything, but without her I have lost control of the knight orders, whose loyalties are now split between various influential factions."

        you "What are you going to do?"

        kuro "There is only one way out, of course. We need to hurry and proceed with this foolish wedding. I guess we're running out of time, and I must tell my father to make a choice soon among the powerful pretenders..."

        menu:
            _("Good idea"):                $ NPC_kuro.love -= 2

                you "Sounds good. A noble husband would protect you, and stabilize the Kingdom."

                "The Princess looks annoyed."

                kuro "Or precipitate a civil war! You shouldn't make light of this. The lives of the city's people is very much at stake!"

                you "Well..."

                kuro "Anyway, you must hurry and complete your assignment. I cannot afford to have assassins roaming free, killing my people anymore."

                you "I'm on it..."

            "No need to rush":
                $ NPC_kuro.love += 2

                you "You should give it time. Rushing to marrying the first noble you find is only going to make your position more precarious."

                you "Who knows, another power figure may emerge sooner than you think?"

                kuro "I know you're right, but... Time is running out."

                you "I can buy you time: my investigation in the Kunoichi will soon be complete."

        you "And by the way, you should know something about Kenshin's killer."

        kuro "Yes?"

        you "I could uncover her motives. She was not part of a conspiracy, but held a long-term grudge against Kenshin's family."

        you "Now that they are all dead, she is no longer a threat to you."

        kuro "Really? How did you find out this information?"

        you "It's a long story, but I assure you this is genuine."

        kuro "Well, that's a relief... Although it's too bad for my poor Uesugi. She didn't deserve this."

        you "Life is unfair..."

    else:
        kuro "Lady Kenshin was just here. She told me everything."

        kuro "And it seems we got rid of one of the pesky assassins that plagued our city."

        you "Absolutely. I can confirm that Mizuki is gone. She won't be back."

        kuro "Wonderful! I commend you for your actions. Your quick-thinking saved the day back then."

        you "Thank you..."

        kuro "But this is discomforting nonetheless. Uesugi Kenshin acted on her own without my knowledge, and could very well have gotten herself killed."

        kuro "Her recklessness is now the talk of the Court, as well as rumors she is from a cursed bloodline... I don't like the gossip I'm hearing."

        menu:
            _("She wanted to do the right thing"):                $ MC.good += 1
                $ NPC_kenshin.love += 2
                $ NPC_kuro.love -= 2

                you "She only wanted to do right by you, investigating every lead..."

                "The Princess looks annoyed."

                kuro "That's what I asked {i}you{/i} to do! She isn't supposed to waste time and put her life in danger running errands while we have a situation at court!"


            "She was foolish":
                $ MC.good -= 1
                $ NPC_kenshin.love -= 1
                $ NPC_kuro.love += 1

                you "She was foolish to disobey you."

                "She gives you a weak smile."

                kuro "Indeed you're right. My confidence in her is shaken, to say the least. Worse, it made us look weaker."

                kuro "And now we have a situation at Court..."

        you "A situation?"

        kuro "Yes. Things are accelerating around that foolish wedding. My father is under even more pressure to choose a pretender, the powers-that-be insisting that we need a man in charge."

        kuro "And people start questioning whether Kenshin is right for the job... And thus, my judgement."

        kuro "Finally, there is another matter..."

        you "Yes?"

        kuro "Kenshin told me the story about her father's disappearance, and about his young ward in the forest."

        you "Yeah, what was that all about?"

        kuro "I have my suspicions about his identity, but I need to follow a few more leads to make sure."

        kuro "Listen to me, [MC.name]. Do not - {i}under any circumstances{/i} - let anyone know about this."

        you "Erm, okay... I won't."

    kuro "Anyway. Thank you for coming this morning. I am sorry - I have so many things to attend to that I cannot keep you for lunch."

    call c3_end_story(NPC_mizuki) from _call_c3_end_story_5

    you "It's fine... Thank you, your majesty."

    scene black with fade

    "You salute the Princess, and a knight escorts you out. You heave a sigh of relief as you walk past the walls of the Palace, thick with ancient stones and political intrigue."

    return

label c3_mizuki_captured():
    "It is finally time to visit your new captive."

    scene black with fade
    show bg mizuki capture1 at top with dissolve

    mizuki "Uggh..."

    you "Finally, she's coming back to her senses."

    mizuki "What... Where..."

    "Mizuki is still in a daze, but she slowly recovers and her eyes focus."

    you "Good evening."

    show bg mizuki capture2 at top with dissolve

    mizuki angry "You!"

    "Mizuki stares daggers at you, furious to find herself in chains in your basement."

    mizuki "What in the Seven Hells do you want from me!"

    "She struggles against her bounds, but notices she is weakened."

    mizuki "There's some kind of... Ward magic... I can feel it..."

    you "Correct. You are bound to this place now."

    mizuki "Grrr..."

    "Mizuki notices the poor state of her kimono."

    mizuki "You even ruined my favorite kimono! You monster!"

    you "Calm down, it was by accident. Kind of."

    mizuki "What do you want?!?" with vpunch

    you "I only want information from you. On the murders happening in Zan."

    mizuki "The murders? I haven't murdered anyone in the city yet!"

    mizuki "Although now, I'm tempted... *hateful look*"

    you "Relax. You must know something about the murders happening at Court."

    mizuki "Hmph. I've heard about them, but you have the wrong gal. I heard the murderer was a male."

    you "That is correct, but you wouldn't be in cahoots with him, now, would you?"

    mizuki "I work alone. And I don't trust men. You should know that by now."

    mizuki normal "But I'll tell one thing I know... If you let me go."

    you "Let you go?"

    mizuki "Yes. If you let me go, I'll leave Zan, and I promise not to make trouble for you."

    you "I don't see how I could trust you to do that."

    mizuki "You don't have a choice. I'm already dead, [MC.name]. There's no way you could torture this information out of me."

    you "I suppose that's true..."

    mizuki "As a gesture of good will, I can tell you what I know. If you promise to let me go then."

    you "Okay..."

    mizuki "I was there you know. When the masked killer stormed the castle. I saw you run after him."

    you "So you're with him!"

    mizuki "Not at all. I was standing two hundred yards away from the castle, high atop the clock tower, using a looking glass to survey the palace's grounds."

    you "Why?"

    mizuki "As it happens, I was stalking my prey. But she needs not concern you."

    you "Your prey... ?"

    mizuki "Listen. I had all possible castle entrances covered that day. {i}All of them{/i}. And I didn't see the killer enter through any of them."

    you "You're saying?"

    mizuki "I'm saying: the killer didn't come in through any of the possible entry points a trained assassin would have used. And I know all of them."

    mizuki "Which means..."

    you "The killer was coming from the inside?"

    mizuki "Yes. Or he was laying in wait for days on end at least, because I had been there for a full day and I didn't see him."

    label mizuki_interrogation_menu():

        menu:
            _("What if he used magic?"):                mizuki "That's impossible. Every castle has basic defenses against basic teleportation."

                mizuki "And if he had tried to use more unconventional means, such as opening a portal to a hellish plane or something, the magic disturbance would have been felt a mile away."

                mizuki "Not to mention he would probably have got himself eaten by a Great Old One. *scoff*"

                jump mizuki_interrogation_menu

            "Did you see him leave?":
                mizuki "No, I didn't."

                mizuki "As soon as the commotion happened, I made myself scarce, because the whole castle was in alert and they would surely have spotted me."

                mizuki "For all we know, he might still be in there, lurking."

                mizuki "In fact, you should promptly let me go, and go check..."

                jump mizuki_interrogation_menu

            "What were you doing there anyway?":
                you "But what business did you have there?"

                mizuki "Like I said, this needn't concern you, because after you free me, I'm leaving Zan for good. My target is far too well-protected."

                mizuki "I'm sure I can catch up with her once she's outside the city limits. On the plus side, it means we never have to run into each other again."

                jump mizuki_interrogation_menu

            "I have no more questions":

                you "Okay, I have no more questions."

                mizuki "So you'll let me go?"

                "Mizuki looks at you, her voice halfway between hopeful and skeptical."

                menu:
                    _("Sure (let her go)"):                        $ MC.good += 2

                        you "I'm probably making a big mistake, but okay."

                        mizuki "Why, thank you my lord."

                        "Her tone is dry, but you can hear relief."

                        you "I hope you'll make good on your promise..."

                        mizuki "Listen, dear boy, you beat me fair and square."

                        mizuki "I have far more important grudges to nurse, so I'll leave you in peace. And as I promised, I will leave the town for good."

                        scene black with fade

                        "With the help of Suzume, you free Mizuki and send her on her way."

                        you "I guess I will have to live with the feeling that I could wake up with a knife in my throat any day now..."

                        you "*yawn* Big deal, I'm used to it."

                        call c3_end_story(NPC_mizuki) from _call_c3_end_story_6

                    "Haha, no (rape her)":
                        $ MC.evil += 4

                        you "No way. Can you really be that gullible? At your age?"

                        "She immediately tenses up."

                        mizuki angry "You swine! I knew it!"

                        you "I hope you are ready for a night of fun... In fact, for many nights of fun... I'm going to turn you into one of my own!"

                        mizuki "What? You think you can break me, boy?!? *furious*"

                        you "I do, and I will. Now, whay don't we start getting more acquainted..."

                        play sound s_dress

                        scene black with fade

                        "Several hours later."

                        show bg mizuki capture3 at top with flash

                        you "Muhahaha! *cum again*"

                        with doubleflash

                        "As you defile Mizuki for the last time of the night, her eyes look empty, even as thick semen trickles down her brow."

                        you "[MC.swear()], that was fun. I'm going to take my sweet time breaking you."

                        "Mizuki doesn't reply. She doesn't even look defiant or mad. She just looks into empty space, as if what you did awoke ages-old memories that made her stare into the abyss."

                        you "Pfff, you're not talking back now, are you? And here I thought you were going to make things difficult."

                        "Slightly disapointed by her lack of reaction, you leave her there. Alone in a dark cell, in a pool of cum."

                        $ calendar.set_alarm(calendar.time+1, StoryEvent(label = "c3_mizuki_gone", type="night"))

                        scene black with fade

                        "You probably need to work on Mizuki some more to truly break her spirit."

                        $ game.set_task("Wait and try to break Mizuki's spirit later.", "story2", 3)

    $ unlock_achievement("mizuki captured")

    return

label c3_mizuki_gone():

    scene black with fade

    "It is time to train Mizuki again."

    you "Hehehe, Mizuki, it's time pick up where we left off last night..."

    play music m_wind fadein 3.0

    show bg cell at top with dissolve

    you "Mizuki?!?" with vpunch

    "The cell is empty. Mizuki's chains stand on the floor, but her shackles aren't broken or opened."

    you "SUZUMEEEEEEEE!!!" with vpunch

    show suzume doubt with dissolve

    suzume doubt "Yeah, boss?"

    you "My prisoner! Where is my prisoner!" with vpunch

    "Suzume looks around."

    suzume "It appears she isn't here, boss."

    you "And how the fuck did she manage to slip off! You told me this cell was magic-proof!!!" with vpunch

    suzume "I don't know, boss... Maybe she really was a ghost..."

    "A chill goes down your spine."

    you "Mizuki..."

    "You have the creeping feeling you will never see her again. It's for the best, as she would surely skin you alive."

    you "Suzume, from now on you will double the patrols, and you will personally be on the lookout for trouble 7 days a week. Got it?"

    suzume "Ow, boss... *tearing up*"

    scene black with fade

    call c3_end_story(NPC_mizuki) from _call_c3_end_story_7

    "Mizuki is gone for good."

    return


label c3_mizuki_arrested():

    "Suzume came back to report."

    show expression bg_bro at top
    with dissolve

    show suzume bend with dissolve

    suzume "Phew! I brought Mizuki to the Palace just in the nick of time. She was beginning to wake up, but the Royal Mages put her in stasis before she could try some ghost business."

    you "Good. Here's hoping she never escapes, or we'll be in trouble."

    suzume "I doubt it. I heard they're going to keep her in stasis and study her for years to come. 'Fascinating post-mortem phenomenon', and all that."

    suzume "The Princess didn't care though. All she wanted was one less assassin on the streets."

    you "And what of our reward?"

    $ MC.change_gold(2500)
    suzume "Hehehe... Here it is!"

    $ unlock_achievement("mizuki arrested")
    call receive_item(rep_item) from _call_receive_item_48
    call c3_end_story(NPC_mizuki) from _call_c3_end_story_8

    scene black with fade

    "You have received a reward for capturing Mizuki Ike."

    return

## End of Mizuki  events ##


## Haruka story line ##

# Guard route #

label c3_haruka_guards():

    $ story_flags["haruka told guards"] = True

    you "So... How do we go about this?"

    if NPC_kenshin.flags["dead"]:
        suzume doubt "I suppose we could have told Kenshin about it... But we can't, on account she's dead."

        you "Yeah. You don't need to remind me."

    else:
        suzume "We could ask Kenshin to introduce us to prison's brass..."

        you "But what if she's in league with the abductors?"

        suzume "Then we don't tell her everything."

    suzume normal "Or... We could just wing it. Talk our way inside the Prison."

    you "What? I don't like the sound of that..."

    suzume "Come on! It'll be fun."

    you "Nothing about going to prison is 'fun'."

    menu:
        "How do you want to approach the Prison?"

        "Tell Kenshin" if not NPC_kenshin.flags["dead"]:

            you "All right, let's visit Kenshin. As the Captain of the Knights, she's our best bet."

            scene black with fade
            show bg palace at top with dissolve
            play music m_kenshin fadein 3.0

            show kenshin with dissolve

            kenshin "You want to do {i}what{/i}?"

            you "Inspect the prison. Talk to the knights in charge. I have information of interest to them."

            kenshin "Then why don't you tell me that information immediately then? I can talk to them."

            you "Sorry, but this is confidential information. It's related to the Princess's assignment, you see..."

            kenshin annoyed "Again with that assignment! I'm the Princess's most loyal servant! There's no need to hide anything from me!" with vpunch

            "Kenshin's eyes spark with fury."

            you "Are you questioning the Princess's judgement?"

            kenshin "Grrr..."

            you "So, will you help me or not?"

            kenshin "You... You..."

            play sound s_sigh

            kenshin normal "Fine, go talk to them, whatever. They'll give me a report afterwards anyway."

            you "Thank you. I assume you will give me a safe-conduct then?"

            kenshin "Hmph, see that with my scribe. But one more thing, [MC.name]..."

            you "Yes?"

            kenshin "You are not allowed to enter the maximum security area of the Prison, got it?"

            you "Why not?"

            kenshin "{i}Because{/i} we have there the most dangerous criminals in all of Xeros, and I don't want you to go around and stir trouble!"

            you "Aw, you don't me to get hurt... That melts my heart a little..."

            kenshin blush "What? No, I... *blush*"

            you "You're cute when you're blushing."

            kenshin annoyed "GO AWAY! NOW! *mad*" with vpunch

            hide kenshin with dissolve

            you "I think she's warming up to me."

            scribe "Here is your letter of conduct. Show it to the Prison Warden and he'll know you came with orders from Lady Kenshin."

            stop music fadeout 3.0

            scene black with fade
            show bg prison entrance at top with dissolve

            play sound s_knock

            "Joined by Suzume, you head back to the lower city to visit the Prison."

            play sound s_creak

            knight "These are not visiting hours, citizen. State your business or leave."

            you "Here, we have a letter of conduct from the Lady Commander."

            knight "Let me see it... Hmm... Everything looks to be in order."

            knight "Come on in then. I shall take you to the Warden."

            show bg office at top with fade
            show warden with dissolve

            you "Uh, hello. *clear throat*"

            warden "Hmm, yes? Who might you be?"

            you "I'm [MC.name], Sir. I work with Lady Kenshin on a royal investigation. And this is my... Bodyguard, Suzume."

            suzume "*chuckles*"

            "The Warden takes one bored look at your papers, and nods towards a couple of chairs by his desk."

            you "Sir, I have grave news. The Prison is in danger of a security breach, and... Sir?"

            "The Warden is busy shuffling papers around as he absent-mindedly listens to you."

            warden "Hmm Hmm... *whistle*"

            you "Someone is trying to break a prisoner out of here, and..."

            "The Warden rolls his eyes."

            warden "Oh, of course they are. *sigh*"

            warden "Come on, my boy, not a day goes by without a foolish wench trying to break her lover out of the prison yard by throwing herself at a guard..."

            warden "And we have riots every other week... I have to hang a dozen inmates to restore order, every time."

            warden "None of this is worth my time, or, might I say, Lady Kenshin's... No one ever escaped the Xotar Prison."

            suzume "But it's not just any threat, though... It's a highly trained killer!"

            warden "*yawn*"

            you "And their target is the maximum security part of the Prison."

            "Suddenly, he stops in his tracks and looks back straight at you. His voice takes a more serious tone."

            warden "The maximum security area? Well, you should have mentioned it immediately, my boy."

            you "Why?"

            warden "As it happens, under the security arrangement mandated by the King, I am only in charge of the upper levels of the Prison."

            you "Was that always the deal?"

            warden "Well, no. We changed that recently. But it suits me fine."

            warden "When I bought this office, I didn't really want to handle the wild beasts we keep downstairs anyway."

            suzume "You {i}bought{/i} this office?"

            warden "Why, sure, how else do you think people get commissioned to high office? On merit? Bwahahaha!"

            warden "I have certain dealings that work best with access to the Prison population, and... Anyway. You needn't concern yourself with that."

            warden "The maximum security area below the penitentiary is the private domain of the King, and only the Knights of the Flaming Hound stand guard down there."

            suzume doubt "The Flaming what, now?"

            warden "The flaming Hounds. They're a Knight Order of the first Circle, fanatically devoted to the Royal family..."

            warden "I try to leave them to their own devices. They're a frightening bunch, if you ask me."

            warden "It cannot be easy to deal with the worst scum in Xeros, every day. The people we have up here are just petty thieves or murderers. They have it far worse."

            you "Can I talk to them then?"

            "The Warden looks annoyed, but he pushes the papers back towards you."

            warden "Well, Lady Kenshin allowed it, correct?"

            suzume "Uhuh. Sure thing. She said, 'Go right ahead!'."

            you "Yup. I believe these were her exact words."

            warden "Do as you please, then... And don't bother coming back, I'm very busy. The knights will show you out."

            hide warden with dissolve

            "A knight waits for you outside of the Warden's office. He motions for you to follow him."

            call c3_meet_hound_knights(route="warden") from _call_c3_meet_hound_knights

        "Go to the prison on your own":

            scene black with fade
            show bg prison entrance at top with dissolve

            you "So... Here we are. What do we do, now?"

            show suzume normal with dissolve

            suzume "Easy... You knock!"

            you "I knock? On the door of the largest prison in Xeros?"

            suzume "Sure. It's not like you're going to damage it."

            you "Why am I even listening to you... *sigh*"

            hide suzume with dissolve

            play sound s_knock

            "You knock and wait expectantly."

            play sound s_creak

            "An intimidating knight opens a small hatch and gives you a cold stare."

            knight "These are not visiting hours, citizen. State your business or leave."

            you "I, err, want to talk to the manager..."

            knight "The mana... The Warden? Are you out of your mind? This is the Xotar penitentiary here, not a cursed tavern!"

            you "Listen. I have crucial information regarding the security of the Prison. Somebody is trying to break in."

            knight "Break {i}in{/i}? That's a first. People usually try to break out of prison!"

            knight "Now, if you're done wasting my time..."

            suzume "Wait! They {i}are{/i} trying to break in then break someone out... They're Kunoichi, you see, and..."

            knight "WAIT! What did you just say?" with vpunch

            you "Kunoichi. It's a kind of ninja..."

            knight "Oh, I {i}know{/i} what a Kunoichi is."

            "His tone becomes cold as ice."

            knight "I think we need to have a little chat, after all... Come in, you two."

            play sound s_door

            "As the door opens, you notice the knight has a firm grip on his sword's hilt."

            knight "Leave all your weapons here, and follow me."

            call c3_meet_hound_knights(route="knight") from _call_c3_meet_hound_knights_1

    return

label c3_meet_hound_knights(route):

    scene black with fade
    show bg prison at top with fade

    play music m_suspense fadein 3.0

    "You follow the knight across the Prison yard."

    "The place is dark and decrepit, and you can make out hundreds of people living in squalor in the various levels of the Prison."

    "Screams of fear and pain regularily echo against the cold stone walls. You shiver and try not to pay attention to them."

    show bg prison office with dissolve

    "The knight goes down a flight of stairs and takes you to an isolated office, a good deal away from the entrance."

    show hound_knight with dissolve

    "You take a good look at the knight for the first time. He's like any other, but he bears an unusual red marking on his chestplate, resembling a scar. It could be a trick of the light, but the marking looks as if it is glowing from the inside."

    knight "Wait here."
    hide hound_knight with dissolve
    play sound s_door

    "The knight leaves the room. You can't help but notice he locked the door behind him. Something feels off."

    if route == "knight":

        you "Looks like we're in."

        suzume "Told ya! Winging it was the way to go."

        you "No one knows that we're here though. We could disappear now and no one would be the wiser."

        you "I didn't like the look of that k-..."

    elif route == "warden":
        you "Seems like the Warden is only nominally in charge here."

        suzume "It's the knight orders who wield the real power."

        you "I noticed. Lots of fishy business involving knights, don't you think?"

    play sound s_door

    "You interrupt yourself as you hear the lock opens."

    show hound_leader at totheright:
        zoom 1.05
    show hound_knight at totheleft with dissolve:
        zoom 0.9

    with dissolve

    "The knight you met ushers in another knight, who looks like  small giant. You can tell he is an officer of sorts."

    hound_knight "Well, what do we have here? Who are these civilians?"

    if route == "knight":
        knight "They say they possess information about a potential intruder. A {i}kunoichi{/i}, Sir."

        knight "I took the liberty to bring them in for you to interrogate."

        hound_knight "Hmm..."

    elif route == "warden":
        knight "The Warden sent them. On a mission for Lady Kenshin, apparently."

        hound_knight "Hmph. We don't have time to entertain idle chat with guests, but if it suits Her Ladyship... *snark*"

        hound_knight "What business do you have with the Flaming Hounds?"

        you "Well, you are in charge of the maximum security area of the Prison, correct?"

        hound_knight "Aye. The prisoners here are the worst scum in all of Xeros, but we keep them in check. Using any means necessary."

        you "We got word of a plot to free one of the prisoners..."

    you "Are you the one in charge of the maximum security part of the prison?"

    if story_flags["c1_path"] != "evil":
        hound_knight "{i}We{/i} are in charge here. Ever since the incident, the Order of the Flaming Hound is the only force allowed in the bowels of Xotar prison."

        you "The incident?"

        hound_knight "A maximum security prisoner had an unfortunate accident recently. Some corrupt guard officer. That's what you get, when you leave high security to amateurs."

    else:
        hound_knight "{i}We{/i}, the knights of the Flaming Hound, are in charge here."

        hound_knight "There used to be a small detachment of the Warden's incompetent guards, but they got scared and they left off."

        hound_knight "But no one scares us. That's why they're only too happy to handle the scum down here."

    you "I have never heard of your order before. Are you Kenshin's men?"

    "He scoffs."

    hound_knight "Of course you haven't. Our order favors discretion, among other things."

    hound_knight "We are of course loyal to the Crown and Her Ladyship, as the Commander of all knight orders of the first circle."

    you "I see."

    hound_knight "Now that your curiosity has been sated, you will indulge mine. What is this plot you came to warn us about?"

    you "Well..."

    hound_knight "A word of warning, first. The Knights of the Flaming Hound are not renowned for their patience."

    "He leans forward towards you, bringing his helmet only a few inches from your face."

    if route == "knight":
        hound_knight "Tell me, young lad, what was this about a {i}kunoichi{/i}?"

    else:
        hound_knight "Let us hear more about this {i}plot{/i} against our prison."

    menu:
        "The unnatural glint of his unblinking eyes makes you shiver. You take a moment to ponder your answer."

        _("Tell him about Haruka"):            $ story_flags["c3_hounds_discussed_Haruka"] = True
            $ story_flags["c3_hounds_discussed_Subaru"] = True
            "You came here to discuss the Earth kunoichi, so it's time to get down to business."

            you "Her name is Haruka. She a kunoichi from the Earth school. She's been skulking around the prison for some time."

            "The knight straigthens up."

            hound_knight "Ah yes, we did know that, but thanks for confirming her identity. She's been poking around our defenses. Do you know her motives as well?"

            you "She's looking for her mentor, Subaru. The word is she's locked up in the maximum security area of this prison."

            hound_knight "Is that so..."

            "The head knight doesn't seem surprised."

            call c3_haruka_guards_success() from _call_c3_haruka_guards_success

        "Tell him about Subaru":
            $ story_flags["c3_hounds_discussed_Subaru"] = True
            "You decide to explore what they know about Subaru, the missing kunoichi."

            you "It's about a kunoichi called Subaru. She is believed to be in the city right now..."

            "The knight doesn't flinch. He says nothing, waiting for you to continue."

            you "We have reasons to believe she's here, in this very prison..."

            hound_knight "Pointless speculation. We know all the prisoners here. We have not registered anyone called 'Subaru'."

            you "She could be here under a fake name..."

            hound_knight "I don't see the need to continue this conversation."

            "There is a hint of a threat in his voice."

            if route == "knight":
                you "Wait! Your man, here, reacted earlier when we mentioned a kunoichi. It cannot just be a coincidence..."

                hound_knight "Did he, now?"

                "You can see the smaller knight cower a little, but the head knight quickly returns his attention to you."

                call c3_haruka_guards_success() from _call_c3_haruka_guards_success_1

            else:
                hound_knight "I see our estimed Warden may have had a lapse in judgment. It happens to the best of us."

                hound_knight "This hearsay doesn't concern us knights of the Flaming hound. Perhaps it is best you return to the Warden, to waste {i}his{/i} time."

                "You hear the sarcasm in his voice, but see that there is no more information to be obtained here."

                knight "Follow me. I will show you out."

                scene black with fade

        "Don't tell him":
            "Feeling nervous, you decide to stay vague until you learn more about the situation."

            you "Well, it's, err, rumors... Of an all powerful female ninja, out to liberate, er... Someone at the prison."

            "The knight brings his helmet even closer to your face. You can almost feel the cold metal brushing against your forehead."

            hound_knight "What is this giberrish? Didn't you say you were privy to some secret information?"

            you "I... I realize it's a bit vague, yes. I'm sorry, I shouldn't have wasted your time."

            hound_knight "No. You shouldn't have."

            if route == "knight":
                "The anger is palpable in his voice. You are painfully aware that you are stuck in the depth of Xotar prison, far from the surface and unarmed. He could skewer you and no one would hear you scream."

                "There is a long pause, then the knight straightens up."

                hound_knight "Show this man out. Levy an appropriate fine for wasting our precious time. *sigh*"

                "The other knight grabs you and Suzume, and shoves you both in the corridor."

                knight "You're lucky we don't throw your filthy commoner's ass in jail for contempt! Come with me!"

                scene black with fade

                $ MC.change_gold(-100)

                "You are thrown out of the jail. You had pay a 100 gold fine before you leave."

            else:
                hound_knight "You're lucky the Warden and Lady Kenshin vouched for you, or I would have you flogged in the courtyard."

                hound_knight "Out with you!"

                scene black with fade

                "One of the knights escorts you back out of the jail, visibly annoyed. They let you go without a word."

    return

label c3_haruka_guards_success():

    "He takes a long look at you, in silence. You {i}feel{/i} as if his gaze is piercing your soul."

    $ NPC_haruka.flags["subaru visit"] = True

    hound_knight "Very well. Follow me."

    "He nods towards Suzume."

    hound_knight "Let her stay here."

    "Disappointed, Suzume sits back down on her chair."

    play sound s_door_close

    "The other knight stays back with her as you follow the leader back into the Prison yard."

    scene black with fade
    show bg prison at top with dissolve

    play sound s_steps

    "You go down several long flight of stairs, then through a maze of corridors. In spite of his massive armor, the Knight doesn't seem to tire."

    "You are now in one of the lowest levels of the Prison, far from any direct sunlight. The air is thick with menace, even the screams have given way to an unatural silence."

    show bg jail at top with dissolve

    "Not a word is exchanged until you stand before a thick, heavy metal door. Another knight is standing guard in the shadows, silent as a tomb."

    show hound_leader at center:
        zoom 1.05

    hound_knight "Take a look inside this cell. You might find it interesting."

    "He slides open a metal slot, gesturing for you to observe."

    scene black
    show bg subaru prison at top
    with dissolve

    you "..."

    "From the description Haruka gave you, and the missing forearm, you have no difficulties recognizing Subaru."

    hound_knight "Is this the woman prisoner you were concerned about?"

    menu:
        _("Yes"):            you "Yes. This is Subaru."

            hound_knight "Indeed."

        "I'm not sure":
            you "Well... I'm not sure..."

            hound_knight "You're not sure? Ha! *hiss*"

    you "Why is she in jail?"

    hound_knight "Her crimes are highly classified. All that you need to know is that she is an enemy of the Crown."

    hound_knight "Make no mistake, she will rot here she dies of old age, or we deliver the King's mercy."

    you "She is a feared warrior. Doesn't she try to escape?"

    hound_knight "{i}Was{/i} a feared warrior. Her body is weak, and we keep her on a special mix of spices for unruly prisoners that makes them... fully compliant."

    hound_knight "And the walls in this part of the Prison were rebuilt from Cimerian ruins, and still infused with powerful antimagic runes. Her spells are no use down here."

    if MC.playerclass == "Wizard":
        you "(So that's why I've been feeling strangely light-headed... Magic is useless here. Better make note of that.)"

    you "Does she talk?"

    hound_knight "We... 'interrogate' her at least twice a week, using... various means. But she has yet to give us information of any value."

    hound_knight "Believe me, it's not that the men are going easy on her."

    "The silent knight in the shadow, who hadn't said anything up until now, gives out a rasp chuckle."

    you "Damn. She seems all right, given the circumstances."

    hound_knight "We haven't been able to break her will yet. But she hasn't been with us for that long."

    hound_knight "Eventually, she will break. They all do..."

    hound_knight "But I didn't bring you down here for idle chatter."

    "You know going in there was going to be a catch."

    if story_flags["c3_hounds_discussed_Haruka"]:

        hound_knight "This 'apprentice' of hers, Haruka... We know of her."

        hound_knight "If we could capture her..."

        if MC.get_alignment() == "evil":
            you "... you could torture her in front of her mentor, and maybe then she would tell you what you need to know."

            hound_knight "Precisely. I like the way you think..."

        else:
            you "Yes?"

            hound_knight "We could use her against her own mentor. Surely the pupil doesn't have the same mental fortitude..."

            hound_knight "And even is she did, her master might care about her enough to finally break."

            you "..."

    else:

        hound_knight "As I'm sure you understand, this is of the utmost importance that mortal enemies of the King like this assassin remain safely locked up in this very prison."

        hound_knight "But someone has been skulking around the prison lately, looking for an unguarded entrance. A kunoichi, by the looks of her."

        you "You don't say."

        hound_knight "Since you're so concerned about the security of the prison: know that we are looking for information on this intruder."

    hound_knight "If you could help us with her arrest, you would do your King a favor, of course, but you would also earn a handsome reward."

    if MC.get_alignment() == "good":
        you "Well, I can't make promises..."

        hound_knight "Hmph."

    else:
        you "I'm all ears."

        hound_knight "Good."

    hound_knight "If you succeed in locating the rogue kunoichi, try and lure her to the East postern. There is a hidden entrance to the Prison there, only it leads right into my men's barracks."

    hound_knight "You just have to lead her inside, we'll handle the rest. We will catch her and make sure no harm will come to you."

    "You wonder how much truth there is to that last statement."

    hound_knight "Think about the reward. We will be generous. In fact..."

    "He places his hand on your shoulder. You can feel unexpected heat radiating through his glove."

    hound_knight "Would you like to receive something now, let's call it... an incentive?"

    "You shiver. The soulless stare of his helmet creeps you out."

    hound_knight "I noticed how you looked at the prisoner. Maybe you'd like to have a go?"

    you "A go at what...?"

    hound_knight "Don't pretend to be thicker than you are."

    you "..."

    hound_knight "It's nothing she hasn't been through already, believe me. Like I said, the men didn't spare her."

    "The silent knight in the shadow scoffs, sounding more wolf than man."

    hound_knight "Don't worry, she's heavily sedated. She won't be a threat."

    menu:
        _("Accept his offer"):            $ MC.evil += 5
            you "Well, I won't turn away such an offer. Breaking tough bitches is kind of my thing."

            "The knight in the shadows gives a belly laugh, which startles you."

            "The head knight says nothing, but you can feel his grin widen."

            hound_knight "In you go, then. This should be good."

            call c3_subaru_rape() from _call_c3_subaru_rape

            play sound s_door_close

            scene black with fade
            show bg jail at top with dissolve

            "When you return, the Hound Knights are waiting for you. They seem amused."

            you "Hope you perverts were not peeping."

            hound_knight "Ha! We don't need to. We're going to be enjoying her again soon enough."

            hound_knight "Still, we could hear you gave her a good pounding. I think she lost it in the end."

            hound_knight "Perhaps this was the final push we needed. Hopefully this will help us break her resistance, bring her over to our... to the King's side."

            scene black with fade
            show bg prison office at top with dissolve

            "Going back to the office, you meet back with Suzume, who raises an eyebrow, wondering what took you so long."


        "Decline his offer":
            $ MC.evil -= 2
            you "Thank you for your offer, but I am no torturer. It is best left to professionals like you."

            "The knight in the shadow snarls menacingly, but the head knight only gives out a brief, creepy laugh."

            hound_knight "So be it. As you've seen, Master... [MC.name], we know how to tend to the King's prisoners, and they are well guarded."

            hound_knight "You'd do well to remember that."

            hide hound_knight with dissolve

            "The head knight walks you back out through another maze of corridors, and you realize you're completely lost again."

            "Finding your way back on your own would be impossible; he probably did it on purpose."

    play sound s_close
    scene black with fade

    "You heave a sigh of relief as you exit the prison and finally breathe some fresh air."


    return

label c3_subaru_rape():

    $ story_flags["subaru raped"] = True

    play sound s_door

    scene black with fade
    show bg subaru fondle1 at top with dissolve

    "You step inside the cell, taking a moment to look at Subaru."

    "As you know she lost her forearm in battle, her right sleeve is empty. She still has the firm body of a fighter, but in her sedated state, she seems to lack energy."

    "Her breathing is slow and her eyes glazed. She barely seems to register your presence."

    subaru "Who... Who is it..."

    "Uttering those words alone seems to take a toll on her. She looks in your general direction and tries to focus her eyes with great difficulty."

    you "Hello, Subaru."

    "You move in closer to her."

    subaru "You... Are not... A Noroi..."

    "You remember the Noroi are the demon clan she used to fight against."

    you "Oh, no... I'm just a visitor."

    subaru "What... You want..."

    "Instead of answering her, you move in closer, detailing the shape of her ass. You extend your hand and place it on her exposed shoulder."

    show bg subaru fondle2 at top with dissolve

    subaru "Don't... Touch!"

    "She tenses up, but seems unable to move at all from her prostrated position."

    you "Come on, Subaru, I'm sure you can guess what I'm here for..."

    subaru "Khhh!"

    you "You know, for a prisoner, I think you are in great shape... I'm going to enjoy myself."

    show bg subaru fondle3 at top with dissolve

    "Grabbing Subaru from behind, you waste no time, sliding your hand on her thigh while you grab one of her breast, fondling it."

    play sound s_surprise

    subaru "Aah!"

    "You pinch her nipple, feeling it stiffen against your fingertips."

    subaru "Nghh..."

    "Breathing down her neck, you enjoy the feeling of her firm ass against your body as you caress her thighs."

    "You feel yourself become hard as you press yourself against her."

    show bg fondle4 at top with dissolve

    "In spite of her drugged state, or maybe because of it, Subaru's body seems to react as you run your hands over her body."

    subaru "A-aah..."

    "Her nipples are already erect, and you can tell that she is getting wet as you rub her crotch through the fabric of her panties."

    you "I thought you'd be more resistant..."

    subaru "F... Fuck... You..."

    you "You know, I can't decide who's sexier, you or Haruka. The Earth school sure has fine tastes in the women they train."

    play sound s_scream
    show bg fondle5 at top with dissolve

    subaru "No! Haruka! What... Did..."

    menu:
        _("Tell her Haruka is fine"):            $ MC.evil -= 1
            you "Relax. Your pupil is not a prisoner... Yet."

            you "But in due time, I expect she'll learn her place, too."

            subaru "Grrr..."

            "Ignoring her resistance, you increase your pace, making sure your shaft rubs against her mound every time you thrust between her legs."

        "Tell her Haruka's been captured":

            you "She's in a cell, just like you. I expect at this very moment she has a fat cock in each of her holes..."

            subaru "N-No! Haruka!"

            play sound s_punch

            "Surprisingly, she seems to recover some fighting spirit. She hits you in the stomach with her elbow, forcing the air out of you."

            you "OUCH!" with vpunch

            subaru "You..."

            "She tries to turn to face you, but you recover in time to put her in a lock."

            you "How dare you hit me, bitch! You will pay for this."

            "Hound Knight's voice" "Everything all right in there?"

            you "Sure!"

            "Completely exhausted by her burst of aggression, Subaru cannot resist you any more."

            "Resuming your ministration, you treat her body even rougher, which only seems to make her more sensitive."

    show bg subaru fondle6 at top with dissolve

    subaru "Hah... Hah... Hah..."

    you "See, Subaru, if you cooperate, it will be better for you. Your student can't help you no matter what."

    you "You'd better get used to this, as I'm sure my knight friends have started to teach you."

    subaru "I... Kill... All you..."

    you "I like your spirit, Subaru, it makes it more fun for me... For now, just try to relax."

    "Shoving your cock even harder between her legs, you increase your pace."

    "She doesn't say anything now, gritting her teeth. Her breathing becomes ragged, and you knows what is coming."

    "You grab her from behind, holding her tight, feeling her ass against your groin."

    subaru "Oh..."

    "With your dick soaked in her juices, you have to take care not to slide directly inside her gaping pussy."

    "Going for the finish move, you squeeze her boob as hard as you can while biting her neck."

    play sound s_orgasm

    with flash

    subaru "Aah! Aah!"

    "Subaru's whole body tenses up, and she screams in pleasure and pain as she comes all over your cock."

    "Tossing her soiled panties to the side, you watch her with a grin. She is laying on her side, unable to move at all."

    you "Now, let's get these out of the way."

    play sound s_dress

    scene black with fade

    show bg subaru sex1 with dissolve

    "Quickly removing her remaining clothes, you push her on all threes, taking in the view of her wet pussy."

    subaru "..."

    "It seems Subaru's mind is wandering far off again, but her body knows what's coming. In spite of herself, she raises her hips slightly towards you."

    menu:
        _("Fuck her pussy"):            $ subaru_act = "sex"

            show bg subaru sex2 with dissolve

            with vpunch

            "You shove your cock inside Subaru's pussy, starting to fuck her from behind."

            subaru "Aah! Aah!"

            "She lets out a scream, and you feel her tighten around your cock."

            you "Good girl, Subaru. Just enjoy it."

            subaru "Aah... Nghh..."

            play sound s_moans_quiet

            "You enjoy her muffled moans as you keep pounding her mercilessly."

            "You didn't even bother to go slow at the beginning, confident her body could take it. And it seems you were right."

            show bg subaru sex3 with dissolve

            subaru "Ah... Ah..." with vpunch

            "With every thrust, you can feel your cock going deeper, hitting her cervix with every movement."

            "You grab her from behind, pulling her towards you, increasing the pace."

        "Fuck her ass":
            $ subaru_act = "anal"

            show bg subaru anal1 with dissolve

            "Grabbing her by the hair, you ram your cock deep into her ass, forcing her to take it."

            subaru "Khh!"

            you "Look at that, your body seems to be loving it... You are a perfect buttslut."

            show bg subaru anal2 with dissolve

    subaru "Aaah!" with vpunch

    "You slap her ass, making it bounce against your body."

    subaru "Aah... Hah..."

    you "Subaru, you are really getting into this... Hehe..."

    "She doesn't say anything, but her moans betray her arousal."

    "You can tell that her mind is slowly giving in, as she starts to match your movements."

    you "I don't see why you became a Kunoichi. You seem to be a natural whore... You could make a fortune in my brothel."

    subaru "..."

    you "I don't think the arm would be a problem... Some customers would actually love that."

    subaru "Fuck... You!"

    you "How I love your fighting spirit, Subaru."

    subaru "Aah!"

    "You pull her hair, forcing her head back."

    if subaru_act == "sex":
        "She moans in pain, but her pussy clenches around your dick. It seems your rough treatment is having an unexpected effect."

        "You feel your arousal become stronger as you pound her harder, feeling her tighten around you with every thrust."

        play sound s_orgasm
        show bg subaru sex4 with flash

        "You feel Subaru's pussy spasms as she comes all over your dick."

        subaru "Aah!"

        with doubleflash

        "With one final thrust, you come as well, shooting your load deep inside her."

        show bg subaru sex5 with flash

        subaru "Aah..."

        "Pulling out, you watch as your semen drips out of Subaru's pussy."

    else:
        "Leaning forward, you start kissing her neck, tasting the sweat on her skin."

        show bg subaru anal3 with flash

        play sound s_orgasm

        subaru "Aah! Aah!"

        "Unexpectedly, Subaru comes, clenching so hard on your dick as she reaches her climax that she almost forces your dick out."

        you "You dare cum before me? What a dirty slut..."

        "Not letting her recover from her orgasm, you slam your cock back in, treating her as a mere hole dedicated to your own pleasure."

        subaru "Aah! Aah! Ahh!" with vpunch

        "In spite of herself, Subaru can't help but moan as you thrust deep into her ass."

        "Her pussy is dripping with juices, and you can tell that she is having another orgasm."

        subaru "Aaah! Aaah!" with vpunch

        "Finally, you increase your pace and bury yourself deep inside her ass, unloading your cum into her bowels."

        show bg subaru anal4 with flash

        subaru "AAAAH!"

        with doubleflash

        "You and Subaru cum together, her anal walls tightening around your cock as you empty your balls inside her."

        show bg subaru anal5 with flash

        "Cumming a copious load inside her, you keep thrusting to make sure she gets it all."

        "Semen overflows from her gaping anus, leaking down her pussy as she collapses on the bed."

    "After emptying your balls inside her, you finally pull out, satisfied."

    $ MC.change_prestige(3)

    return

# Intercept #

label c3_haruka_final_intercept(): # Done

    play music m_haruka fadein 3.0

    scene black with fade
    show bg haruka intro at top with dissolve

    haruka "You, again?"

    haruka "I don't want to hurt you... But I can't let you interfere with my mission."

    menu:
        _("Negotiate with her"):
            you "Wait! I can help you."

            if NPC_haruka.flags["subaru visit"]:
                you "I have information for you. I know where Subaru is."

                haruka "She's in Xotar Prison, I know that already."

                you "Yes. But I know her precise location."

                haruka "..."

                call c3_haruka_negotiate() from _call_c3_haruka_negotiate

            else:
                you "I know where Subaru is. I have been able to piece everything together."

                you "Let me help you find her."

                haruka "Hmph. She's in Xotar Prison, I know that much. Why would I need you?"

                call challenge("force", 3) from _call_challenge_69 # result is stored in the _return variable
                $ r = _return

                "Haruka takes a good look at you."

                play sound s_sigh
                if r:
                    haruka "Hmm... You have the build of a fighter. Okay, maybe you can be of help."

                    call c3_haruka_negotiate() from _call_c3_haruka_negotiate_1

                else:

                    haruka "You're not fit for battle, you would only slow me down..."

                    you "Wait!"

                    haruka "I don't have time for this! Step aside. *firm*"

                    menu:
                        _("Try and capture her"):                            call c3_capture_haruka() from _call_c3_capture_haruka

                        "Give up":
                            "Prudently, you step aside."

                            play sound s_crash
                            hide bg with vpunch

                            suzume doubt "She's gone again..."

        "Try and capture her":
            jump c3_capture_haruka

    return

label c3_capture_haruka(): # Done

    $ ninja = NPC_haruka

    if story_flags["ninja hunt"] == calendar.time:
        "You can only attempt to catch a ninja once a day."
        return

    stop music fadeout 3.0

    if MC.has_item(earth_rune.name):

        "Feeling the reassuring weight of your trusty toy-hammer in your hand, you insert the Earth Rune in the handle."

        you "(It should be here, in the small compartment held by a screw... Where it says 'Made in Cathay'.)"

        "You give a knowing look to Suzume."

        you "Let's do this."

        haruka angry "Out of my way! EARTHQUAKE!"

        "..."

        "Nothing happens."

        haruka "What is this? Why won't my powers work?"

        you "We're evenly matched now... Seize her!"

        scene black with fade

        $ story_flags["ninja hunt"] = calendar.time

        call run_ninja_game(njgame) from _call_run_ninja_game_2

        return _return

        # results are in BKchapter2 - label intercept_haruka()

    else:

        suzume "It's useless though... We need something to counter her powers..."

        play sound s_crash
        with quake

        "As before, Haruka summons a small earthquake to cover her escape. She leaves you both panting in the dirt."
        hide bg with quake

        scene black with fade

        you "Damn, if only I had a counter to Earth magic..."

    return


label c3_haruka_negotiate():

    haruka "Speak then. Where is she?"

    you "In a cell, in the maximum security part of the prison."

    haruka "Of course, I could guess that much."

    if NPC_haruka.flags["subaru visit"]:
        you "I've seen her with my own two eyes. It... wasn't pretty. But she is alive, and she hasn't broken yet."

        "Her jaw clenches."

        you "We should hurry and rescue her."

    haruka "But I've tried everything. There's no way in. The Prison is too heavily guarded, and even then you'd have to fight through the main yard just to get to the lower levels."
    you "There is another way, though. A secret passage."

    haruka "There is? Tell me!"

    you "Only if we make a deal, though."

    haruka "A deal? What deal?"

    you "I want to secure this city, make sure no upstanding citizen is being murdered by the likes of you."

    haruka "If you help me rescue Subaru, we'll leave this Arios-forsaken city forever. I promise."

    you "Okay. But we'll do things my way. And Suzume is coming with us."

    haruka "Fine, whatever. The important thing is to save Subaru."

    "You shake hands. She is reluctant at first, but you feel her becoming slightly less tense as you let her hand go."

label c3_haruka_checkpoint():

    $ renpy.save("c3 haruka checkpoint", "Haruka's checkpoint")

    if NPC_haruka.flags["subaru visit"]:

        "You remember well the offer of the Hound Knight Leader."

        hound_knight "({i}You just have to lead her inside, we'll handle the rest.{/i})"

        hound_knight "({i}Think about the reward. We will be generous.{/i})"

        menu:
            "What do you tell Haruka?"

            _("Tell her about the true secret passage"):                $ renpy.block_rollback()
                $ NPC_haruka.flags["c3 path"] = "ally"
                $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_haruka)] = True

                you "The secret passage is in the Sewers. Leads right into the maximum security part of the Prison."

                haruka "Really?"

                suzume "We don't know where it is yet, but if you work together with us... We can shadow the next convoy and find the secret entrance."

                you "Using force is out of question, at least until we locate Subaru. We need to enter discreetly."

                haruka "Okay. Seems like this is our best chance. Let me gather some equipment, and we can meet at night, by the Sewers."

                suzume "Sure thing... Finally, we're going to see some action!"

                you "All right, we'll meet you later by {b}the Sewers{/b}."

                $ game.set_task("The Earth Kunoichi: Meet Haruka by the Sewers.", "story")
                $ add_event("c3_haruka_sewers", type="city", location = "sewers")


            "Lead her into a trap":
                $ renpy.block_rollback()
                $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_haruka)] = True

                you "(This Subaru business is no concern of mine. If I help the knights, I can get rid of Haruka and make some money and allies in one fell swoop.)"

                you "There is a secret passage, by the Eastern postern. I managed to lift the key from one the guards. From there, it's straight down to Subaru's cell."

                "Suzume knows you're lying, but to her credit, she doesn't display any emotion."

                haruka "That's... Perfect. The Eastern part of the Prison has less patrols. If we can get in and out fast, we can break Subaru out of there!"

                you "Sure, sure..."

                haruka "All right, let's meet by the prison at night. I'll gather the necessary equipment."

                you "All right, we'll meet you at {b}the Prison{/b}."

                $ game.set_task("The Earth Kunoichi: Meet Haruka at the Prison.", "story")
                $ add_event("c3_haruka_trap", type="city", location = "prison")

    else:
        $ renpy.block_rollback()
        $ NPC_haruka.flags["c3 path"] = "ally"
        $ story_flags["ninja hunt locked %s" % get_ninja_district(NPC_haruka)] = True

        you "The secret passage is in the Sewers. Leads right into the maximum security part of the Prison."

        haruka "Really?"

        suzume "We don't know where it is yet, but if you work together with us... We can shadow the next convoy and find the secret entrance."

        you "Using force is out of question, at least until we locate Subaru. We need to enter discreetly."

        haruka "Okay. Seems like this is our best chance. Let me gather some equipment, and we can meet at night, by the Sewers."

        suzume "Sure thing... Finally, we're going to see some action!"

        you "All right, we'll meet you later by {b}the Sewers{/b}."

        $ game.set_task("The Earth Kunoichi: Meet Haruka by the Sewers.", "story")
        $ add_event("c3_haruka_sewers", type="city", location = "sewers")

    haruka "Wait, [MC.name]..."

    you "Yes?"

    haruka happy "Thank you."

    scene black with fade

    return

# 'Good' path #

label c3_haruka_sewers(): # OK

    scene black with fade
    "You wait until nightfall before meeting with Haruka."

    play music m_suspense fadein 3.0

    show bg sewers at top with dissolve

    show haruka with dissolve:
        yalign 1.0
        zoom 0.9

    haruka "[MC.name]! You came."

    you "Of course."

    show suzume at totheright with dissolve

    suzume "Heyah!"

    haruka defiant "Ah. So you're here, too."

    suzume "I did some reconnaissance, and I saw the guard patrol we're looking for. They're moving some political prisoners in by night. It's likely they'll use the sewers entrance."

    haruka "Great. Let's follow them from a distance. We can't be seen, at least not until we know where that entrance is."

    hide haruka with moveoutleft
    hide suzume with moveoutright

    "You and the girls take position in a dark alley next to the main road. Soon, you see the patrol emerge. Half a dozen soldiers escort a couple of hooded figures, in chains."

    "The group is led by a knight who seems at ease skulking in the dark."

    haruka "I know this coat of arms. This is a knight of the Flaming Hound, the order that defends the prison."

    suzume "Let's see where they are headed."

    show bg street night at top with dissolve

    "The patrol passes you by as you watch from the shadows. You wait until they are some way off, then start following them carefully."

    "In spite of your efforts, you feel slow and clumsy, compared to the Kunoichi who seem to glide effortlessly into the night, silent as ghosts."

    if MC.playerclass == "Warrior":
        "Your experience fighting Elven scouts in the dark forests of the Holy Lands taught you a lot about sneaking though, so you manage to follow, not too far behind."

    elif MC.playerclass == "Wizard":
        "You cast a noise reduction spell on yourself, allowing you to move faster to keep up with the girls."

    elif MC.playerclass == "Trader":
        "As someone with a lot of experience thieving, you know enough about sneaking to follow cautiously. Besides, you have an ace up your sleeve."

        "Looking up, you see a dark silhouette gliding silently dozens of feet above the streets. It's your pet dragon, keeping an eye on your prey for you."

    "Fortunately, the squad is unsuspecting and does not stop to see if they are followed. Soon, it seems they have reached their destination."

    suzume "Wait, what are they doing?"

    "The guards stop in front of a building, which on closer inspection appears to be a barracks."

    show guard with dissolve:
        zoom 0.17
        xalign 0.21
        yalign 0.71

    "They exchange words with someone inside, then the whole group enters, save for one sentinel."

    haruka angry "This can't be right! You said they were headed to the Sewers!"

    you "I thought so... I..."

    "Haruka rummages frantically in her satchel, then pulls out a scroll."

    haruka defiant "Let me see... Could it be..."

    "You and Suzume give her a puzzled look."

    haruka "Here! I see. Let me just confirm something."

    "Haruka leaps on top of an old cart, lifts herself up on a balcony then climbs up a building effortlessly. A moment later, she reaches the roof, disappearing from view."

    you "What the..."

    suzume doubt "Hush, don't worry. She'll be back in a moment."

    "A minute later, Haruka comes back down, jumping in a somersault to land just next to you without barely a noise."

    haruka "I've seen them. There's a grate to the Sewers in the court behind the barracks. That's where they took the prisoners."

    haruka "The only way in is through the barracks' entrance, though."

    you "We can't fight our way through a guards' barracks! Even if we win, this will bring the whole city's attention down on us."

    haruka "I know. We need to infiltrate. And there's the issue of the sentinel they posted at the door..."

    haruka "We can't sneak past him, and he's wearing armor, so a takedown from afar is too risky..."

    suzume shrewd "Seems like we need to come up with a plan, and fast. I think I know just what to do."

    "She kneels besides Haruka, and whispers something in her ear."

    haruka surprise "What?!? I don't... It's not..." with vpunch

    haruka angry "Why don't {i}you{/i} do it?"

    suzume "I'm going to stay out here to cover you guys. It's better if no one sees me. But you need to get inside with [MC.name] fast, don't you?"

    haruka surprise "Y-Yes, but..."

    suzume normal "Don't argue, then! This is your chance to save Subaru. Don't let it slip!"

    haruka blush "I... You... I guess you're right..."

    you "Will someone tell me what's going on?"

    "Suzume grins, and whispers her plan in your ear."

    call c3_haruka_fondle() from _call_c3_haruka_fondle

    scene black with fade
    show bg street night at top with dissolve
    show suzume at totheright with dissolve

    suzume "Well done, you two! I feel like you could have gone on for a bit longer!"

    show suzume at totheright with move
    show haruka with dissolve:
        yalign 1.0
        zoom 0.9

    haruka blush "C-Couldn't you think of anything else to distract the guard?"

    suzume "Hey, it was just the first thing that came to mind!"

    haruka angry "What kind of mind thinks like this???" with vpunch

    suzume doubt "I suppose we could just have whistled to get the guard's attention... But hey, that way was more fun!"

    haruka "Fun for whom!!!" with vpunch

    you "Stop squabbling, you two! Haruka, we need to rush to the Sewers before we lose the trail."

    you "Suzume, hide the body and meet us at the rendezvous point."

    suzume bend "Okay. Good luck out there."

    hide suzume with dissolve
    show haruka at center with move

    haruka "Quick, let's follow them!"

    play sound s_creak

    scene black with fade
    show bg inner_sewers at top with dissolve

    "Moving quickly, you go through the grate behind the barracks and descend into the Sewers."

    "Once you reach the ground, Haruka motions for you to stay silent. She places her palm on the wall, concentrating."

    you "What... What are you doing?"

    haruka defiant "Hush! I can sense their footsteps echoing through the tunnels... They're already pretty far. We need to hurry."

    "Haruka darts into the nearest tunnel, and you follow her as fast as you can, half-blinded by the darkness."

    you "Hey! Wait..."

    with fade

    "From time to time, Haruka stops to feel the ground's vibrations, giving you time to catch up."

    "Eventually, she stops dead in her tracks and pulls you close."

    haruka "They're just around the bend over there. We must be quiet."

    "You can see the flickering of torches up ahead. You both move silently in the shadows, until you can cautiously look around the corner."

    show hound_knight with dissolve:
        zoom 0.65
        xalign 0.6
        yalign 0.8
        yanchor 1.0

    knight "We'll take over from here. Common guards are now allowed beyond this point."

    show guard with dissolve:
        zoom 0.6
        xalign 0.3
        yalign 0.8
        yanchor 1.0

    guard "Me legs are killing me, and me throat is parched!"

    guard "Aw, have a heart, Sir, at least let us rest a little in yer cosy barracks! I need me a drink!"

    knight "Giving me orders, are you now, commoner?"

    play sound s_punch
    with vpunch

    guard "OW!!!"
    hide guard with pixellate

    "The knight casually smacks the guard in the jaw with his armored gauntlet, knocking out a tooth."

    knight "Is this how you address your betters, pleb? I gave you an order. Now, scram with the rest of you."

    "Frightened, the other guards grab their knocked-out comrade and skitter back through the tunnel."

    "Haruka pulls you down behind a broken crate just in time for you to let the guards pass."

    "There's not much space behind the crate, so you have to stay close together. It isn't unpleasant."

    "She whispers in your ear."

    haruka "(Let's wait until they're out of hearing range. Then we move.)"

    "You turn your attention back to the knight and his wretched prisoners, blinded by hoods."

    "Elder prisoner" "Please, Sir! Where are you taking us? I-I can't walk much longer..."

    knight "Save your breath, old man. Or I'll be more than happy to give you the same treatment I gave that stupid guard."

    "The knight places his hand on the wall and does something."

    play sound s_stone
    with vpunch

    "You can feel the rumble of stone as the wall slowly moves to reveal an entrance."

    "He yanks the chains to lead the prisoners inside."

    haruka "(We strike, now!)"

    play sound s_dodge

    show haruka with blinds:
        zoom 0.075
        xalign 0.225
        yalign 0.525

    pause 0.3

    play sound2 s_dodge
    hide haruka with blinds
    show haruka behind hound_knight with blinds:
        zoom 0.5
        yanchor 1.0
        xalign 0.4
        ypos 0.8

    "One second Haruka is besides you, the next she is leaping across the tunnel, closing the gap with the knight at a terrifying speed."

    play sound s_sheath

    knight "Uh-"

    play sound s_splat

    with vpunch

    "The knight doesn't have a chance to turn around before Haruka plunges her dagger in his neck, striking at the gap between his armor and helmet."

    hide hound_knight with pixellate

    "For a second, Haruka freezes behind the knight's body, frowning."

    "Elder prisoner" "What is going on? Please, anyone, can you help us!"

    "The hooded prisoners start panicking, unable to see what just happened. Haruka snaps out of her daze."

    haruka angry "Quick, [MC.name], come with me! We need to go get her!"

    "You look at the two wretched prisoners, shackled and powerless."

    you "What about these people?"

    haruka "What about them? We have no time, [MC.name]!"

    menu:
        _("Help them out"):            $ MC.good += 2

            you "I just can't leave them here..."

            "Haruka sighs with exasperation as you remove the hooded sacks from their heads. She helps you snap their bounds open with her steel."

            "The prisoners are an old man and his teenage daughter, whom on better days look like they might have been part of good society."

            "They thank you profusely before running away in the tunnels."

            haruka defiant "Here, happy now? Now, let's go!"

            $ story_flags["c3 helped prisoners"] = True

            #! Return event for helped customers

        "Leave them":
            $ MC.good -= 2

            you "You're right, we have more important things to do."

    "Haruka charges recklessly inside the Prison through the secret entrance, barely giving you time to follow."

label c3_haruka_rescue():

    scene black with fade
    show bg thieves_guild corridor at top with dissolve

    play sound s_steps

    you "Wait, Haruka, wait!"

    "Haruka stops, looking uncertain."

    haruka surprise "The vibrations, I can't feel them any more. I can't locate Subaru!"

    you "These walls are Cimerian-built. I think they have wards against magic."

    haruka angry "Damn it!"

    if NPC_haruka.flags["subaru visit"]:
        you "Wait, I recognize this corridor... We're close to Subaru now!"
    else:
        you "It seems like we are already in the deepest part of the Prison... She can't be very far now, can she?"

    haruka angry "Look, down here!"

    "Haruka shows you some markings on the wall. To you, they look like a series of random scratches."

    haruka "I recognize this, this is a code from the Earth school. Subaru must have found a way to leave this alongside the way, behind her captors' back."

    haruka "This should lead her to her cell!"

    hide bg with dissolve
    "After just a few turns, you finally reach the cells."
    show bg jail at top with dissolve
    show haruka with dissolve

    haruka "The trail ends here!"

    you "There are no guards..."

    haruka "We've been lucky! Look, it's her cell! Quick, let's break her out!"

    you "But don't you think it's strange..."

    with flash
    play sound2 s_fire

    "Without listening to you, Haruka throws a ninja bomb at the cell's door, blowing it open." with vpunch

    "A silhouette emerges from the smoke, stumbling out of the cell."

    haruka "Sensei!"

    subaru "Haruka? Is that you?"

    haruka "It' me, Sensei! We're breaking you out!"

    play sound s_clang

    "Haruka flings a weapon at Subaru, who catches it swiftly with her good arm, in spite of her tired state."

    show haruka at right with move
    show subaru2 at left with dissolve

    subaru "We? Who's with you?"

    haruka "This is [MC.name]. He can be trusted. We need to make our way out, now. Can you walk?"

    if story_flags["subaru raped"]:
        subaru "This man... This man..."

        haruka "What is it, Subaru?"

        subaru "He's with them!"

        play sound s_sheath

        scene black
        show bg subaru kill at top
        with flash

        "Faster than your eyes can hope to follow, Subaru leaps at you, plunging her blade through your heart."

        subaru "Die, monster..."

        scene black with circlein

        "As your consciousness fades, you realize you've made a mistake..."

        $ unlock_achievement("game over")

        play music m_theme_quiet
        scene black with fade

        centered "{color=[c_red]}{b}GAME OVER{/b}{/color}"

        $ renpy.load("c3 haruka checkpoint")

    subaru "Yes, don't worry about me. Lead the way."

    play sound s_maniacal_laugh

    hound_knight "Not so fast!"

    hide subaru
    hide haruka
    hide bg

    show bg jail

    show hound_knight at left as k1:
        zoom 0.7
    show hound_knight at right as k4:
        zoom 0.7
    show hound_knight at totheright as k2:
        zoom 0.85
    show hound_knight at totheleft as k3:
        zoom 0.85

    show hound_knight:
        xalign 0.5
        yalign 1.0
        zoom 1.05

    with pushleft

    play music m_danger fadein 3.0

    hound_knight "Look what the hound dragged in... Haruka, the bitch ninja's own little whelp."

    hound_knight "Actually, I remember you... We had some fun last time with you, I recall."

    subaru "Haruka..."

    haruka angry "What the hell are you saying! I've never met you in my life" with vpunch

    hound_knight "Oh, but you have..."

    hide hound_knight
    hide k1
    hide k2
    hide k3
    hide k4
    with blinds

    show noroi at left as n1:
        zoom 0.7
    show noroi at right as n4:
        zoom 0.7
        xanchor 0.5
    show noroi at totheright as n2:
        zoom 0.85
        xanchor 0.5
    show noroi at totheleft as n3:
        zoom 0.85

    show noroi_leader:
        xalign 0.5
        yalign 1.0
        zoom 1.05

    with blinds

    noroi_leader "Haven't you?"

    haruka "No! No! It's impossible..."

    subaru "These knights. They're Noroi, Haruka."

    you "What in the Seven Hells is this?"

    if NPC_haruka.flags["subaru visit"]:
        "Noroi Leader" "And here is our little interloper... The Princess's own errand boy."
    else:
        "Noroi Leader" "And who is that fool?"

    noroi_leader "No matter, just kill him. And get the girls alive. Cut off their limbs if you have, to but don't let them die!"

    "Norois" "Yes, boss!!!" with vpunch

    # $ diff = 5

    if MC.playerclass == "Warrior":
        "Clutching your sword, you empty your mind, ready to enter the fray."
    elif MC.playerclass == "Wizard":
        "Unable to use your spells, you are at a serious disadvantage. You will have to think quick."
    elif MC.playerclass == "Trader":
        play sound s_roar
        drogon "*ROAR*"
        "A loud roar echoes through the corridors. You know your pet dragon has been following you the whole time, and he is now rushing to help."
        # $ diff = 4

    # $ chal = renpy.call_screen("challenge_menu", challenges=[("Fight", "fight", 4), ("Take charge of the battle", "rally", diff)])
    #
    # if chal == "fight":
    #     $ norollback()
    #
    #     call challenge(chal, 4)
    #     $ r = _return

    play sound s_sheath

    show noroi as n1 at jumping

    "The first Noroi comes clawing at you, mistaking you for an easy target."

    if MC.playerclass == "Warrior":
        play sound s_sheath

        # add slicing

        "Your blade slashes through him like butter, and he gives you a dumbfounded look as his body is sliced cleanly in halves."

    elif MC.playerclass == "Wizard":
        play sound s_punch

        "Reduced to using your staff as a mace, you hit the charging demon in the face, eliciting a painful grunt."

        play sound2 s_splat

        "Before he can recover, you grab your staff with both hands and bring it down on his skull, hearing a statisfying crunch."


    elif MC.playerclass == "Trader":
        play sound s_roar
        "His cry of triumph becomes a scream as Drogon swoops in and locks his neck between his jaws, crushing it."

        play sound s_splat

        "Demon blood splashes around as Drogon increases the pressure, while the demon jerks around helplessly. It isn't long before he stops moving."
    
    hide n1 with pixellate

    play sound s_sheath
    pause 0.2
    play sound2 s_wscream
    hide n4 with pixellate

    "A shriek of pain comes from the next Noroi as Subaru severs his arm at shoulder level, before swirling and taking his head off."

    play sound s_sheath
    pause 0.2
    play sound2 s_sheath
    pause 0.3
    play sound3 s_crash

    hide n2 with pixellate

    "Haruka also found her mark, sticking two kunais in the chest of her victim before extending her arms outwards and ripping it open."

    noroi_leader "Get them! Get them!"

    play sound s_dodge
    pause 0.2
    play sound s_splat

    "The last Noroi soldier hesitates just a bit too long before a kunai thrown by Haruka hits his throat. He dies in a gurgle."

    hide n3 with pixellate

    subaru "It's just you, now, demon!"

    noroi_leader "You will not get past me! I should have killed you a long time after all, but now I won't make that mistake!"

    play sound s_mystery

    show noroi_leader:
        ease 0.5 zoom 1.7 ypos 1.2

    "Dark energy swirls around the Noroi as he seems to feed on the remains of his dead comrades. He ends up towering above all of you, large as an ogre."

    play sound s_roar

    noroi_leader "Hyaaaaahahaha, POWER!!!"

    noroi_leader "Now you DIE!"

    play sound s_punch
    show noroi_leader at jumping

    "Charging at you with surprising speed, you barely have time to avoid the demon's strike but the shock sends you flying into the wall, hitting your head hard."

    you "OUCH!" with vpunch

    "Subaru and Haruka dodged away, but he is on them in an instant. Subaru can barely parry his flurry of attacks with her good arm, while Haruka struggles to find an opening."

    noroi_leader "Your temple is over! Your people is over!"

    play sound s_roar

    noroi_leader "With every life you lose, you grow weaker, but we feed on death! We are unstoppable!"

    play sound s_laugh

    subaru "Maggots feast on the dead too, but I can still crush them under my heel!"

    play sound s_punch

    "*HIT*" with vpunch

    "Seeing a fleeting opening in his guard, Subaru kicks him right in the chin, sending his head flinging backwards."

    play sound s_roar
    noroi_leader "ARRRH!" with vpunch

    "Stumbling blindly forward, trying to grab her, the Noroi ogre fails to see Subaru is already sliding between his legs, slashing at the back of both his knees."

    play sound s_sheath
    "*SLASH*"

    play sound s_roar
    noroi_leader "AAAAARRRRH!!!" with vpunch

    "The demon flips around. He nearly crushes Subaru's head with his weapon, but Haruka blocks it at the last moment."

    play sound s_punch
    pause 0.2
    play sound s_crash

    haruka "Haaaah!!!" with vpunch

    "Kicking Haruka viciously, the demon sends her flying, knocking down Subaru at the same time. He looms over them, ready to strike a killing blow."

    haruka "Subaru!!! Watch out!!!" with vpunch

    you "(It's my chance!)"

    "Having regained your footing, you take advantage of the giant's inattention."

    you "Hey, hunchback!"

    "Grabbing a kunai on the floor, you leap over the demon's back, sticking the weapon in his neck."

    play sound s_roar

    noroi_leader "*GROAR*" with vpunch

    show noroi_leader:
        ease 0.5 xalign 0.5 yalign 1.0 zoom 1.25

    "The monster trashes around as dark blood spurts from his neck, trying to shake you off. Eventually, he manages to fling you off, turning around to face you."

    noroi_leader "YOU WORM! ANY LAST WORDS?!?" with vpunch

    play sound s_sheath

    pause 0.2

    play sound s_splat
    stop music fadeout 3.0

    "*SPLAT*" with vpunch

    hide noroi_leader
    show noroi_leader as half1:
        crop (0, 0, 0.5, 1.0)
        zoom 1.25 xanchor 1.0 xpos 0.5 yalign 1.0
    show noroi_leader as half2:
        crop (0.5, 0, 0.5, 1.0)
        zoom 1.25 xanchor 0.0 xpos 0.5 yalign 1.0

    play sound2 s_sheath
    with flash

    show noroi_leader as half1:
        ease 1.5 ypos 0.0 yanchor 1.0

    show noroi_leader as half2:
        ease 1.5 ypos 1.5 yanchor 0.0

    "Before he can say anything further, his body is split cleanly in half by a blade."

    play sound s_crash
    hide half1
    hide half2

    show subaru2 at center
    show bg jail behind subaru2
    with pixellate

    "As his lifeless body crashes to the ground, you can see Subaru standing behind him, her blade covered in gore."

    subaru "Phew. Thanks, you guys. It nearly got the best of us."

    subaru "I'm really badly out of shape."

    show subaru2 at left with move
    show haruka at right with dissolve

    haruka normal "You used to be able to defeat three of these single-handedly... You need rest, Sensei. "

    subaru "Well, I need to learn to do a lot of things single-handedly now. *chukles*"

    haruka sad "I-I didn't mean..."

    you "Ladies, shall we get out of here? I think we've overstayed our welcome."

    subaru "I for one would love to leave this place behind. Lead the way."

    play sound s_dodge

    haruka angry "Of course! Follow me, let's go!"

    scene black with fade
    show bg thieves_guild corridor at top with dissolve

    play sound s_steps

    "Running like the wind, Haruka leads you and Subaru back through the maze of corridors. You're glad that she has memorized the way perfectly, as it is easy to get lost in the dimly-lit prison."

    scene black with fade
    show bg inner_sewers at top with dissolve

    if not story_flags["c3 helped prisoners"]:

        "You finally come out through the Sewers exit."

        play sound s_mystery

        "*BUMP*" with vpunch

        you "What's that?"

        you "Haaah!" with vpunch

        "With horror, you realize you stumbled on a mangled corpse. Although its features are barely recognizeable, you realize it's one of the shackled prisoners from earlier."

        "The body of the other prisoner is further away in the sewer, missing some limbs."

        you "W-What happened to them..."

        haruka sad "Seems like some sewer monster got to them while they were left here..."

        you "Damn... We shouldn't have left them alone here..."

        haruka "I'm sorry. What's done is done."

        subaru "Let's leave before the Noroi catch up to us... Or this 'thing' comes back for seconds."

    else:
        "The three of you run through the sewers at top speed, not looking back."

label c3_free_subaru():

    scene black with fade
    play sound s_creak

    "You manage to make your way back to another sewer exit, where you previously set up a rendezvous with Suzume."

    show bg street night at top with dissolve

    show subaru2 with dissolve

    subaru "Hmmmm... Finally, some fresh air!"

    subaru "I didn't think I was ever going to see the night sky again."

    show subaru2 at left with move

    show suzume bend at right with dissolve

    suzume "Kukukukuku, you made it!!! Subaru, I presume?"

    subaru "Oh, another kunoichi? That's quite the rescue operation... I'm flattered..."

    subaru "Haruka, you need to tell me how you managed to make so many useful allies."

    hide suzume with dissolve
    show haruka_humble at right with dissolve

    haruka blush "I... I didn't. It's all thanks to [MC.name]. He chose to help me."

    subaru "Well then, thank you, [MC.name]. Haruka and I are forever in your debt."

    "To your surprise, she bows gracefully to you, and Haruka immediately bows even deeper."

    subaru "On my honor, I shall repay this favor to you. If you need anything..."

    you "Well, the first thing I need if for Haruka to honor our deal. No more assassinations in the city, and I need to know everything you know about the kunoichi murders in the city."

    subaru "Hold on, hold on. Haruka, what is he talking about?"

    haruka normal "Well, I'm not sure. I haven't murdered anyone in the city, save for these 'knights'."

    you "But someone has been taking out important officials. They have links to a Kunoichi clan. Surely you know more?"

    haruka "Well, I have some suspicions. Whatever this demon cult is doing infiltrating the Knights, it must be related somehow."

    subaru "The least we can do is help you look into what's going on with the Noroi. It aligns well with our goals, too."

    you "Thank you. That would be helpful."

    you "But don't take anyone out. Or at least, come to me first."

    subaru "You've got it."

    haruka "Sensei, you're very tired... We must go."

    play sound s_sigh

    subaru "I know... *sigh*"

    subaru "We need to go, [MC.name]. We'll talk more after we've had a chance to rest."

    subaru "Thank you again."

    haruka happy "Thank you, [MC.name], from the bottom of my heart."

    play sound s_dodge

    hide subaru2 with dissolve
    hide haruka_humble with dissolve

    $ unlock_achievement("haruka ally")
    $ NPC_haruka.flags["c3 path"] = "ally"
    call c3_end_story(NPC_haruka) from _call_c3_end_story_9

    "The two ninjas fade into the night."

    show suzume bend with dissolve

    suzume "So this is Subaru, the legend, uh? She's only got the one arm, but she seems cool."

    you "Do you think we can trust these two?"

    suzume "I don't see why not. They seem just as reliable than I am."

    you "I don't know if that's reassuring..."

    scene black with fade

    return

label c3_haruka_fondle(): # OK

    scene black with fade

    "You and Haruka move into position into a dark alley, straight across from the barracks."

    you "*shout* Hey! Come here, little girlie! Let me have some fun!"

    show bg haruka fondle1 at top with dissolve

    play sound s_scream_loud

    haruka blush "EEEEK! Help!!!" with vpunch

    you "*in character* HEHEHE, Missus, I'm going to have some fun with ya! *hiccup*"

    play sound s_surprise

    haruka "*in character* I'm, err, in distress!!! Help!" with vpunch

    haruka "(What on earth are we doing???)"

    you "(It's like Suzume said, we need to get the guard's attention away from that door.)"

    haruka "(B-But, you're really touching me!!!)"

    you "(It has to look genuine... Play along!"

    play sound s_scream

    haruka "Haaa!" with vpunch

    "You squeeze her breast encouraginly."

    haruka "D-Don't do that! Stop!"

    you "(Yes, that's it, play along.)"

    show bg haruka fondle2 at top with dissolve

    play sound s_ahaa

    haruka "I'm not pla... Ahaa..."

    "Not one to pass such a great opportunity to have fun, you continue teasing Haruka, caressing her inner thigh, inching closer to her panties."

    you "*loud* HAHAHA! I'm going to deflower you right now, even though you are obviously non-consenting and this is completely against the law. Because I'm a LAW BREAKER!" with vpunch

    play sound s_moans_quiet

    haruka "(W-Why is your acting so bad?)"

    play sound s_scream
    haruka "*loud* HAAAAH!" with vpunch

    "In spite of your efforts, the guard remains impassive. Perhaps he hasn't seen you yet, or he doesn't care."

    haruka "(Aahh! You're too rough with me...)"

    you "(At least I'm trying to get his attention! You do it!)"

    play sound s_screams

    haruka "*louder* HAAAA, HAAA, HELP, ANYONE!" with vpunch

    haruka "I am being assaulted by a ruffian, even though I am obviously not consenting and it is completely against the law!"

    you "(You called me a bad actor, and then you use {i}my{/i} line?)"

    haruka "(It's all in the delivery! Mine was better! Aaaah...)"

    play sound s_aah
    haruka "Aaaah..."

    "You notice that Haruka has eased into her situation rather quickly. She barely fights you back as you fondle her, mellowing in your embrace."

    you "(At least we're having a good time, aren't we? You seem to feel fine.)"

    "You run your fingers against her panties, feeling a hint of wetness."

    haruka angry "(S-Shut up, stop doing that! Let's get this over with already!)"

    haruka "HELP, SOMEONE, HEEEELP!!! Is there anyone that can help me around here! Anyone who represents the legal authorities of this town, especially someone from the guard?" with vpunch

    play sound s_scream_loud

    haruka "PLEASE HEEEELP!!!" with vpunch

    you "(It's not working... He's looking straight at us, and yet he won't move a finger!)"

    haruka blush "(This was a stupid idea... Let's just stop...)"

    you "(We need a new approach. I know what to do, but you need to trust me.)"

    play sound s_dress

    show bg haruka fondle3 at top with dissolve

    play sound s_scream

    haruka "W-What are you doing!!!" with vpunch

    "Freeing Haruka's large tits from her jumpsuit, you keep rubbing them in plain view of the sentry."

    you "*drunken drawl* OOOH, look at that bitch's titties! She's a handful!"

    you "MAN, she must be PERFECT for a TITJOB!"

    you "Damn, I think I'm too drunk to get it up! Hey, is there ANOTHER DUDE out here who wants to relieve himself, uh?"

    you "Is there someone man enough to FUCK this innocent chick with the huge TITTIES?"

    "You see the sentry stir."

    haruka "(I don't believe it... I-It's working...)"

    "The man is now clearly oggling Haruka's tits by the streetlight. He hesitates to move, struggling to get a better view."

    you "(We just have to give him a little push...)"

    you "OOH, I think this bitch loves getting raped! She's in heat for sure! I can tell she is completely wet, ready to take a dick!"

    play sound s_ahaa

    haruka "Ahaaa, you're so rough, Mister, I can't take it!" with vpunch

    show bg haruka fondle4 at top with dissolve

    "Haruka leans back into your arms, almost grinding against you. She closes her eyes, moaning."

    haruka "I feel so strange, being manhandled in a dark alley by a stranger! I feel so hot down there!"

    haruka "Please, SOMEONE, make me feel better!" with vpunch

    play sound s_aaah
    show bg haruka fondle5 at top with dissolve

    haruka "AAAAAH!!!" with vpunch

    "Haruka screams wildly, moving her hips suggestively."

    you "(Wow, your acting is getting really good now!)"

    haruka "(S-Sorry, I think I'm getting carried away...)"

    you "(No no, keep at it! It's working!)"

    "The guard is now walking towards the alley, patting his crotch. He has a smug smile on his face."

    haruka "S-Sir?"

    you "Come over here, officer, there's plenty of ass for the both of us!"

    guard "Get lost, drifter, before I throw you in jail to feed the rats! She's mine..."

    you "Oh no, Sir, I'm sorry if I offended you, honest..."

    "You step back slowly, raising your hands."

    "He moves forward menacingly."

    haruka "A-Are you rescuing me, good Sir?"

    guard "Hehehe, sure... I'm rescuing you, so let me send that drunk loser on his way and then we'll get to the part where you reward me, hehehehe."

    you "B-But the girl was mine, Sir, you need to pay me a denar or two... Or I won't move! I got her nice and wet for you, didn't I?"

    guard "What??" with vpunch

    "As you say that, you slowly retreat into the dark alley. The guard reaches for his sword and walks towards you, stepping past Haruka, ."

    guard "If you don't scram right this instant, motherfu-..."

    play sound s_punch
    with vpunch

    pause 0.2

    play sound s_crash

    "Haruka hand-chops the guard right at the base of the neck, and he crumbles like a bag of sand."

    you "Nice! Is he alive?"

    haruka defiant "Who cares? Let's go."

    "Not making eye contact, she fixes her clothing, and runs for the barracks' entrance."

    $ MC.change_prestige(3)

    return

# 'Evil' path #

label c3_haruka_trap():

    scene black with fade
    "You and Suzume wait until nightfall before meeting with Haruka."

    show bg prison entrance at top with dissolve
    show haruka with dissolve

    play music m_wind fadein 3.0

    you "...see, this is the East Postern, where the secret door is."

    haruka "There are no guards..."

    you "Yes, it's perfect."

    haruka "It's strange, don't you think?"

    you "Well, no one is supposed to know about this entrance, I guess. It doesn't matter, let's get in before someone sees us."

    haruka "Well, I guess I have no choice but to trust you on this..."

    "Moving quickly, the three of you run towards the stone wall. You see the faint outline of a door cut directly in the stone."

    play sound s_stone
    with vpunch
    "Following the knight's instructions, you unlock the door and it pivots with a heavy noise, revealing a dark flight of stairs."

    you "Get in there, quick! I'll cover the rear."

    haruka "Okay. Subaru-sensei, here I come!"

    scene black with fade
    play sound s_steps
    "Haruka charges into the prison, rushing down the stairs."

    show bg jail at top with dissolve

    haruka surprise "Wait!" with vpunch

    play music m_mafia fadein 3.0

    if story_flags["subaru raped"]:
        show subaru evil hidden with dissolve

    else:
        show hound_knight as k1 with dissolve
        show hound_knight at totheleft as k2 behind k1 with dissolve:
            zoom 0.9
        show hound_knight at totheright as k3 behind k1 with dissolve:
            zoom 0.9
        show hound_knight at left as k4 behind k2:
            zoom 0.85
        show hound_knight at right as k5 behind k3:
            zoom 0.85
        with dissolve

    haruka ninja "What? What is this!?!" with vpunch

    if story_flags["subaru raped"]:
        play sound s_sheath

        "Haruka doesn't even have time to unsheath her blade before the mysterious figure casts a dark spell on her."

        play sound2 s_splat

        "*SPLASH*" with vpunch

        "Haruka finds herself intertwined in a giant, thick spiderlike web."

        haruka "W-Who... Who are you?!?"

        play music m_demons

        show subaru evil with dissolve

        "The scarlet-clad figure emerges from the shadows, and Haruka gasps."

        haruka "S-Sensei! Is this you?" with vpunch

        "You recognize Subaru, although she is completely changed, from the way she is dressed to the color of her eyes. Incredibly, her arm even seems to have been made whole."

        subaru evil "My sweet little Haruka... Welcome. I've been waiting for you."

        haruka "But Sensei... How? Why?"

        play sound s_evil_laugh

        subaru "You know, for the longest time, I was like you, fighting back against fate, questioning everything..."

        subaru "But then, I finally saw things clearly. You shouldn't fight the darkness within you, you should {i}embrace{/i} it..."

        haruka "No! What have they done to you?" with vpunch

        subaru "They have offered me a new life, one without rules and boundaries... And I have decided to accept it."

        "She turns towards you."

        subaru "And it's all thanks to you, by the way... You've helped me see the one true path."

        "She licks her lips seductively."

        subaru "After our meeting, I was drained, I couldn't resist them anymore... So I finally gave in to my urges... And now, I don't regret any of it."

        haruka "YOU! What did you do to her?!? You betrayed us!!!" with vpunch

        "She struggles against her bonds, to no avail."

        subaru "Hush, little girl, you're being an unruly pupil now... But I will deal with you."

        haruka "No!!!"

        call c3_haruka_demon_subaru() from _call_c3_haruka_demon_subaru

        scene black with fade
        show bg jail at top with dissolve

        show hound_leader at left
        show subaru evil at right
        with dissolve

        "As you reluctantly look away from this spectacle, you realize the Flaming Hound leader has joined you."

        hound_knight "You have kept your end of the bargain. The Order is pleased."

        you "Sure, sure. But you mentioned a reward."

        hound_knight "Here. You can have this."

        $ NPC_haruka.flags["c3 path"] = "banished"
        $ unlock_achievement("haruka banished")

    else:

        play sound s_sheath
        pause 0.3
        play sound2 s_sheath
        pause 0.1
        play sound3 s_sheath

        haruka "Stand back!" with vpunch

        play sound s_clang
        pause 0.2
        play sound2 s_clang
        pause 0.2
        play sound3 s_sheath

        "Haruka is surrounded by knights, desperately defending herself."

        play sound s_sheath
        pause 0.2
        play sound2 s_wscream

        hide k5 with pixellate

        knight "Aaargh!" with vpunch

        haruka "No!"

        play sound s_clang
        pause 0.2
        play sound2 s_punch
        pause 0.1
        play sound3 s_crash

        show hound_knight as k1 at bounce

        knight "Take that!"

        play sound s_scream

        haruka "OUCH!" with vpunch

        "Haruka crashes down on the floor, and soon the knights pile up over her."

        haruka surprise "No! Let me go, you bastards!"

        "The men finally manage to subdue Haruka, disarming her and tying her securely."

        haruka "No!!! My magic doesn't work... Why?"

        haruka "[MC.name]! Help me!" with vpunch

        play sound s_maniacal_laugh

        knight "Help you? he's the one who led you right to us!"

        haruka "What?"

        you "I did. Sorry, Haruka, you shouldn't trust strangers so readily."

        haruka angry "Grrr... Let me go! I'll kill you, [MC.name]!" with vpunch

        knight "Shut up bitch, you're ours now... I hope you enjoyed a bit of sun today, because you're never going to see the light of day again."

        play sound s_scream_loud

        haruka surprise "No!!!" with vpunch

        knight "You! You have done your job, now leave the rest to us. Here, have this as a present from the boss."

        $ NPC_haruka.flags["c3 path"] = "arrested"
        $ unlock_achievement("haruka arrested")

    call receive_item(subaru_tunic, use_article=False) from _call_receive_item_28

    you "Thanks. I'll be out of your hair, then."

    $ NPC_haruka.flags["c3 path"] = "demon"
    call c3_end_story(NPC_haruka) from _call_c3_end_story_10

    knight "Good. Now go. And you'd better forget everything you've seen in here."

    scene black with fade

    play sound s_screams

    haruka "Heeeeelp!!!" with vpunch

    "You hurry back out of the dungeon, leaving the screams of desperation of the captured Earth ninja behind."

    return


label c3_haruka_demon_subaru():

    play sound s_dress

    scene black

    show bg subaru_demon1 at top

    with dissolve

    "Before Haruka can resist any further, Subaru rips open her clothes with claw-like strength from her reconstructed arm."

    haruka "Sensei, please! Think of what you're doing! Break this spell, and escape with me!"

    "Ignoring her, Subaru grabs one of her boobs, feeling it."

    subaru evil "You don't get it, do you? Your old mentor is no more. All that is left of me is my core: animal instincts, desires... Lust."

    play sound s_scream

    haruka "Sensei!"

    "Without concern for you watching, Subaru slips her own large breasts from her body suit, rubbing them against Haruka's."

    play sound s_surprise

    haruka "Haaa!!!"

    subaru "I lasted for months... I'm curious to see how long it will take to break {i}you{/i}."

    play sound s_ahaa

    haruka "Aaah, ah..."

    subaru "You've always been the sensitive one. I'm sure we can make short work of you."

    show bg subaru_demon2 at top with dissolve

    "While still kneading one of Haruka's breasts, she moves her hand down to rub her crotch."

    play sound s_moans_quiet

    haruka "Nghh..."

    subaru "Hmmm... We need to get you wet. Let's see if you're as frigid as they remembered."

    haruka "T-They? Who..."

    subaru "Who? The Noroi, of course! Who do you think took us in!"

    haruka "The Noroi? Demons! H-How did you talk to them... What..."

    play sound s_evil_laugh

    subaru "Oh, they're here... They're in my head, even as we speak! I {i}am{/i} one of the Noroi now, you silly child!"

    subaru "And I am going to train you to be like me! Now, let's see..."

    "She starts rubbing your pupil's clit, making her squirm."

    subaru "Let's see if you're a natural slut, or if you need to be broken, like I was."

    haruka "No! Anything  but the Noroi! Anyone, help! [MC.name]!"

    "Haruka's voice shakes with utter fear."

    subaru "[MC.name] is the one who caught you, you stupid bitch. He's not going to lift a finger to help you."

    "She presses her lips against Haruka's neck."

    haruka "Mmmmh..."

    "She bites down, and Haruka can't suppress a moan."

    haruka "Ahhh..."

    "She feels a tongue run along her skin, and Subaru reaches her ear."

    subaru "You have such a pretty neck, it makes me want to sink my teeth into you... *hiss*"

    haruka "Please, stop..."

    subaru "*licks* Hush now..."

    "Subaru increases the pace of fingers, and slowly Haruka's body seems to react in spite of her defiance."

    haruka "Your arm... How..."

    subaru "The arm? Oh, it's nothing, you should know growing new flesh is nothing to us Noroi."

    subaru "In fact, let me show you something... A lot cooler."

    play sound s_mystery

    show bg subaru_demon3 at top with dissolve

    "Haruka's eyes widen in shock as she sees a bulge growing under Subaru's panties, until it rips them open to reveal a large and thick penis."

    subaru "See? I can just grow this with the power of my mind... You're very lucky, as you're going to be the first one I try this on."

    play sound s_scream_loud

    haruka "No!!! Get this away from me!"

    "She struggles with all her might, but she is well bound."

    subaru "Don't worry, my sweet, I'll make sure you enjoy it!"

    haruka "NOOOO!" with vpunch

    "Subaru bumps her large cock against Haruka's exposed belly, leaking sticky pre-cum all over her navel."

    subaru "Will this really fit in? Oh well... Only one way to find out."

    "Haruka closes her eyes as Subaru rubs her cock against her pussy."

    haruka "Please... No... Please..."

    "Despite Haruka's best efforts, her pussy lips are opening up to let Subaru in."

    subaru "Let's go for it."

    show bg subaru_demon4 at top with dissolve

    play sound s_screams

    haruka "AAHHH!" with vpunch

    "Subaru slams her cock inside her former pupil's pussy, forcing it wide open."

    subaru "So this is what it feels like to have a dick... Amazing..."

    haruka "Nooo... Please, stop!" with vpunch

    "Subaru's demonic cock is so large that you can see Haruka's underbelly get swollen by it."

    subaru "I wonder if I can make you pregnant like this..."

    haruka "Aah, ah... No..." with vpunch

    "She slams her hips against Haruka's, her cock buried to the hilt."

    show bg subaru_demon5 at top with dissolve

    subaru "Now, let the fun begin!"

    "Subaru starts moving back and forth, fucking Haruka's pussy."

    haruka "Ahh... Ahh..." with vpunch

    "Haruka starts moaning against her will."

    haruka "Aah! Aah!" with vpunch

    "Subaru grabs her boobs, kneading them as she thrusts her cock deep into Haruka."

    haruka "No! Nooo..."

    subaru "You're so tight... It's amazing! It seems you weren't raped near enough..."

    haruka "No!" with vpunch

    "Subaru slams her hips against Haruka."

    haruka "Ahh..."

    "She slams even deeper, pressing her belly against Haruka's, which makes her moan louder."

    subaru "Oh, but you will learn to love being raped... Don't worry, everyone here at the prison will gladly help..."

    haruka "Nooo!" with vpunch

    "Subaru is hitting all the right spots inside Haruka, making her moan uncontrollably."

    subaru "You are so wet now... You get aroused when I talk of rape, don't you?"

    haruka "No! Ahh..."

    subaru "I was thinking to give you away to some convicts for a week, would you like that?"

    haruka "Aah... Aaah... No!" with vpunch

    "Subaru starts pounding her faster, fucking her senseless."

    haruka "Aaah!"

    "You can tell Haruka's mind is completely overwhelmed. She seems to have no fight left in her, and whimpers like a wounded animal."

    subaru "This is your life now, Haruka... You can thank [MC.name] for that. Better learn to enjoy it."

    haruka "No... *sob*"

    subaru "Hush now, child... I'm going to impregnate you."

    haruka "Nooo!" with vpunch

    subaru "I'm cumming!" with flash

    play sound s_orgasm

    show bg subaru_demon6 at top with doubleflash

    "Subaru slams her cock inside Haruka, and shoots a thick load of semen inside her, filling her to the brim."

    "Haruka screams at the top of her lungs, feeling the burning hot liquid flood her womb."

    haruka "AAAAAAAAAAHHH!!!"

    with flash

    "Subaru cums so much that her seed overflows and drips from Haruka's pussy."

    show bg subaru_demon7 at top with flash

    subaru "Boy, what a mess... Having a cock is surely something. I'm going to enjoy the hell out of that thing."

    return

label c3_haruka_arrested():

    "Suzume came back to report."

    show expression bg_bro at top
    with dissolve
    show suzume bend with dissolve

    suzume "Hey Boss. So I took Haruka into custody. The Princess handled it herself."

    suzume "I avoided talking to Kenshin entirely. We never know what those knights are up to."

    you "Good."

    suzume "The Princess said to thank you and to asked me to give you these rewards."

    $ MC.change_gold(2500)
    call receive_item(rep_item) from _call_receive_item_29
    $ NPC_haruka.flags["c3 path"] = "arrested"
    $ unlock_achievement("haruka arrested")
    call c3_end_story(NPC_haruka) from _call_c3_end_story_11

    you "Nice! Was there anything else?"

    suzume "What, did you think she would give us, like, a dozen complimentary buns stuffed with fine bunting meat and Borgian olives? I would never keep that from you."

    you "That's... Strangely specific."

    suzume "*BUUUUURP*" with vpunch

    suzume "Just ignore that."

    scene black with fade

    return

label c3_haruka_captured():
    "That night, you decide to pay a visit to your new captive."

    play music m_haruka fadein 3.0

    you "Gizel should be in there already..."

    play sound s_open

    scene black with fade
    show bg haruka bondage1 at top with dissolve

    gizel normal "Ah, [MC.name]. How good of you to join us."

    gizel smirk "I took the liberty of preparing her a little."

    you "Wow, that's some serious knot-work. Is she still out?"

    gizel "Yup. But it shouldn't be long before she wakes up. Perhaps we can speed that along."

    play sound s_punch

    "*SMACK*" with vpunch

    show bg haruka bondage2 at top with dissolve

    play sound s_surprise

    haruka surprise "Ah!"

    gizel "Wakey wakey, lil' girlie..."

    play sound s_scream

    haruka "What? Who's there? Where am I???" with vpunch

    haruka "M-My magic... I can't feel it, it's gone..."

    you "Relax, Haruka. It's no use panicking."

    you "After all, you'll be with us for a big long while."

    "You take out her blindfold."

    show bg haruka bondage3 at top with dissolve

    play sound s_surprise

    haruka "It's you! You monster! I should have killed you when I had the chance..."

    haruka angry "Where am I? Where's Subaru? Tell me!" with vpunch

    you "Forget about Subaru. She's beyond your ability to help."

    play sound s_evil_laugh

    gizel "You should worry more about yourself, for now. Because your training is about to start... And I will be in charge."

    haruka "My training? What are you even talking about?"

    haruka blush "And w-why am I... Naked..."

    gizel "Well, I'm sure you can take a good guess, can't you? You've been there before, haven't you?"

    show bg haruka bondage4 at top with dissolve

    play sound s_surprise

    haruka "No, wait, don't do anything to me... I'll just go, I'll leave you in peace, but stop..."

    play sound s_punch
    show bg haruka bondage5 at top with dissolve

    "*SPANK*" with hpunch

    play sound s_scream

    haruka "AH!!!"

    gizel upset "Shut up now, slave! It's time you begin to learn your place."

    show bg haruka bondage6 at top with dissolve

    gizel "First of all, [MC.name] here is 'Master' to you, and I am Mistress Gizel."

    gizel "Say it!" with vpunch

    haruka "No, I..."

    play sound s_punch
    show bg haruka bondage5 at top with dissolve

    "*SPANK*" with hpunch

    play sound s_scream

    haruka "AAAAH!!"

    play sound s_punch
    pause 0.3
    play sound2 s_punch

    "*SPANK* *SPANK*" with hpunch

    play sound s_screams

    haruka "AAAH! No! Stop, stop!"

    gizel "SAY IT!" with vpunch

    show bg haruka bondage6 at top with dissolve

    haruka "M-Mistress Gizel... M-M-Master [MC.name]..."

    gizel normal "Good."

    play sound s_punch
    show bg haruka bondage5 at top with dissolve

    "*SPANK*" with hpunch

    play sound s_scream_loud

    haruka "OUCH!!!" with vpunch

    show bg haruka bondage6 at top with dissolve

    haruka "What did you that for? M-Mistress Gizel..."

    gizel smirk "Oh, nothing. I just felt like it."

    gizel "Over time, you will discover that pain is one of the best forms of pleasure. But we'll go step by step."

    "Gizel takes out equipment: clips with weights attached to them."

    "Her outfit is so skimpy, you really wonder where she keeps all these things."

    gizel normal "Let's not dance around the bush: your best feature is that huge pair of knockers. We need to make sure they're sensitive enough to pleasure our guests."

    haruka "G-Guests?"

    play sound s_clang

    show bg haruka bondage7 at top with dissolve

    haruka "Ow!!!" with hpunch

    gizel "Very nice! Not only is this going to stretch your nipples properly, but it will teach you that pleasure and pain mix well together."

    gizel "Maybe I'll leave you like this all night. This would be a teachable moment."

    play sound s_scream_loud

    haruka "No! You can't do that to me! Help!!!" with vpunch

    show bg haruka bondage8 at top with dissolve
    play sound s_punch
    pause 0.3
    play sound2 s_punch

    "*SPANK* *SPANK*" with hpunch

    play sound s_screams

    haruka "OW! OUCH!!!"

    gizel upset "What was that you were saying?"

    show bg haruka bondage9 at top with dissolve

    haruka defiant "..."

    gizel normal "You're still defiant, but that is to be expected from a new slave. We'll break you soon enough."

    haruka "Y-You called me a slave... What do you mean?"

    gizel smirk "Oh, just that you belong to [MC.name] now. I had you magically branded at the black market while you were passed out."

    gizel "It's all too easy to kidnap a girl like you. It cost me next to nothing to grease the Slavers' Guild paws to look the other way."

    gizel normal "No one knows you in Zan, no one cares for you here. All you have left is to work for us... I mean for [MC.name]."

    haruka "[MC.name]? But he's... He's..."

    play sound s_surprise

    haruka surprise "A brothel owner!" with vpunch

    gizel "You're finally catching up, aren't you?"

    haruka blush "No, don't make me... No..."

    play sound s_evil_laugh

    gizel smirk "Anyway. I think we've dilly-dallied long enough."

    gizel "[MC.name], will you do the honors?"

    stop music fadeout 3.0

    you "My pleasure."

    "Coming from behind Haruka, you enter her gaping pussy with no warning."

    show bg haruka bondage10 at top with fade
    play sound s_scream

    haruka "AAAAH!!!" with vpunch

    "It is easier than you thought. Seems like Gizel's ministrations had a bit of an effect on her body already."

    play sound s_moans

    haruka "Oh, aah..." with hpunch

    "You start moving your hips back and worth, enjoying the way Haruka's body bounces off you as she is dangling from the ceiling."

    gizel smirk "Look at you, taking it all in stride!"

    gizel "You're doing better than expected for a first time. We'll make a good whore out of you yet."

    haruka "No! I'm no... Whore!"

    play sound s_scream_loud

    haruka "Aaaah!" with hpunch

    "You increase your pace, making sure to hit her deepest parts with every thrust."

    gizel "This is only the beginning of your training, but already I can tell it's going to go well."

    gizel blush "I think your rape fetish is going to help us along..."

    play sound s_surprise

    haruka "R-Rape fetish? No! I don't have anything like that!!!" with vpunch

    play sound s_moans

    "In spite of her denegations, you can feel the moistness of her pussy as she bounces off your dick."

    gizel "Oh, but you can deny it all you want, I {i}know{/i} it's true... It takes one to know one."

    haruka "Aaah, aaaah, aaaah..." with hpunch

    "You have gone on for long enough, and decide it's time to let yourself go. You will have plenty of other opportunities to use this pussy later."

    you "Ooh, omph... Take that, Haruka!"

    play sound s_scream_loud

    haruka "AAAAAH!!!" with vpunch

    show bg haruka bondage11 at top with flash

    "Shooting your load deep inside Haruka's pussy, you fill her to the brim with hot cum."

    show bg haruka bondage12 at top with doubleflash

    play sound s_screams

    haruka "Oooh... Aaaah... You did... Inside..."

    gizel "My, my, that's a great creampie if I ever saw one!"

    gizel "To think we are only getting started... I'm salivating."

    haruka "Ohhh..."

    "Haruka cannot hear Gizel's taunts, as she just passed out."

    $ MC.change_prestige(3)

    "Gizel turns to you."

    gizel normal "Listen, I'll take over her training for now. We need to make sure she is completely broken before we let her around any customer."

    gizel "I'll use my minions at the farm. Make sure I have all of the minion types available. I will need to experiment with different approaches..."

    you "All right."

    gizel "And give me that rune. It will keep her under control when she is out of her cell."

    call remove_item(earth_rune, definite_article=True) from _call_remove_item_7

    scene black with fade

    "Gizel will train Haruka at the Farm with the help of her minions. Make sure she has {b}every type of minion available{/b} for this."

    # INIT BREAKING COUNTER
    $ NPC_haruka.flags["stallion counter"] = 0
    $ NPC_haruka.flags["beast counter"] = 0
    $ NPC_haruka.flags["monster counter"] = 0
    $ NPC_haruka.flags["machine counter"] = 0
    $ NPC_haruka.flags["farm completed"] = 0

    $ story_add_event("haruka_break_test", "daily")

    $ NPC_haruka.flags["c3 path"] = "captured"
    call c3_end_story(NPC_haruka) from _call_c3_end_story_12

    return


# Haruka captured events

label haruka_break_test(): # Fires up every morning after capturing Haruka

    # Step 1: Find a relevant minion type

    python:
        for min_type in all_minion_types:
            if NPC_haruka.flags[min_type + " counter"] < 4 and farm.has_minion_type(min_type):
                break
        else:
            min_type = None

    # Step 2: Train

    if min_type:
        $ NPC_haruka.flags[min_type + " counter"] += 1

        if NPC_haruka.flags[min_type + " counter"] < 4:
            $ notify("Haruka trained with a %s at the Farm." % min_type, pic="side haruka blush")
        else:
            call haruka_farm(min_type) from _call_haruka_farm
            $ NPC_haruka.flags["farm completed"] += 1
            $ renpy.block_rollback()

        if NPC_haruka.flags["farm completed"] == 4:
            $ story_remove_event("haruka_break_test", "daily")
            $ calendar.set_alarm(calendar.day + 1, StoryEvent(label="haruka_broken"))
        else:
            "You congratulate Gizel on her progress with Haruka. You look forward to the next part of her training."
    else:
        $ notify("Haruka couldn't train at the farm because some minion types are missing.", pic="side haruka blush", col=c_lightred)

    return

label haruka_farm(min_type): #! Add fixations and skill changes

    $ _min = rand_choice(farm.get_healthy_minions(min_type))

    if not _min:
        $ _min = "Bob"
    else:
        $ _min = _min.name

    if dice(2) == 1:
        play sound s_rooster
    else:
        play sound s_moo

    scene black with fade
    show bg farm at top with dissolve

    "Gizel called you to the farm, to check on the progress of her pensioner."

    gizel normal "Hey, [MC.name]. Haruka has been training hard lately. I thought you'd like to see the results."

    if min_type == "stallion":

        gizel "Now is the time for her morning stretch... [_min] is helping her."

        show bg haruka big1 at top with fade

        _min "[_min] going to stretch strong girl pussy. [_min] likes!"

        play sound s_surprise

        haruka angry "Get off me, you brute!"

        _min "Strong girl tied up good... Cannot punch [_min] like last time. That made [_min] sad..."

        haruka "Stop! Or, or..."

        show bg haruka big2 at top with dissolve

        haruka "*gasp*"

        play sound s_evil_laugh

        gizel smirk "Oh, my... I always forget [_min] gets that big when they fight back... He likes it."

        haruka blush "No, go away, you animal... Not again..."

        _min "Uhuhuh..."

        show bg haruka big3 at top with dissolve
        play sound s_scream

        haruka "EEEK!!!" with vpunch

        _min "Oh, strong girl pussy stretching good..."

        gizel "She's been getting plenty of practice, after all."

        with vpunch

        "[_min] is not done, though. Somehow he pushes his fat dick even deeper."

        show bg haruka big4 at top with dissolve
        play sound s_scream_loud

        haruka "AAAAH!!! It's going to break me in half!" with vpunch

        gizel "Don't be ridiculous. You know you can take it."

        show bg haruka big3 at top with Dissolve(0.2)

        _min "*grunt*"

        show bg haruka big4 at top with Dissolve(0.2)

        haruka "AH!" with vpunch

        show bg haruka big3 at top with Dissolve(0.2)

        gizel "Look at him go!"

        show bg haruka big4 at top with Dissolve(0.2)

        haruka "AAAAH!!!" with vpunch

        show bg haruka big3 at top with Dissolve(0.2)

        gizel "I think he's ready to..."

        show bg haruka big5 at top with flash

        _min "UAAAH!!!" with vpunch

        with doubleflash

        play sound s_mmmh

        haruka "NGGGGH!!!"

        with flash

        "Haruka shakes uncontrollably as [_min] releases a superhuman load deep inside her pussy."

        play sound s_ahaa

        haruka "Ahaaaa..."

        "Haruka is still shaking. With your expert eye, you can tell she just had a small orgasm."

        you "Woah, she came in spite of herself... And it hasn't even been five minutes!"

        gizel "Yeah... She's addicted to big dicks now. As she should be."

        play sound s_surprise
        show bg haruka big6 at top with dissolve

        haruka surprise "No! It's a lie!"

        gizel "Hmph, don't be such a killjoy. [_min], help her stretch a bit more."

        play sound s_roar

        _min "*GROAR*!"

        haruka "Nooo!!!" with vpunch

        "Not skipping a beat, [_min] slams his dick again inside Haruka's pussy."

        play sound s_ahaa

        haruka blush "Ahaa..." with vpunch

        "Well lubricated with his cum, [_min]'s fat cock keeps pounding Haruka's womb, making her moan harder."

        gizel "You can feel it, now, Haruka? Being raped by a fat dick is the best, isn't it?"

        play sound s_aah

        haruka "S-Stop... Aah!!!" with vpunch

        "Haruka's voice has become weak, it's like she's no longer there..."

        "But her hips started moving in spite of herself. It's like she's inviting [_min] to fuck her even harder, which he does."

        _min "*GRRRR*" with vpunch

        play sound s_evil_laugh

        gizel "Look, at that, [MC.name]! [_min] is going to cum again, and I can tell it's going to be a big one!"

        gizel "Say, it's your choice now: Where do you want it?"

        menu:
            extend ""

            "Cum inside her":

                gizel "So be it!"

                show bg haruka big7 at top with flash

                _min "UAAAAAAGH!!!"

                with doubleflash

                play sound s_scream_loud

                haruka "AAAAAAAH!!!!"

                "[_min] shoots an enormous load inside Haruka's pussy, stretching her belly full of thick cum."

                play sound s_orgasm
                with flash

                haruka "Oh, ah, aaahaaa!!!"

                "She cums more loudly this time."

                show bg haruka big8 at top with flash

                gizel "Wow, would you look at that... It's like you're pregnant with cum..."

                haruka "What... What's happening... to me..."

                gizel "Wait! I think there's some more left!"

                show bg haruka big9 at top with vpunch

                haruka "No, you c-can't be serious... NGH!"

                show bg haruka big10 at top with flash

                _min "*GRUNT*"

                with doubleflash
                gizel "That's my big boy!"

                show bg haruka big11 at top with flash

                play sound s_mmmh

                haruka "Aaaaah..."

            "Cum all over her":

                gizel "[_min], it's time for her morning shower!"

                play sound s_roar

                _min "GROAR!!!" with vpunch

                show bg haruka big12 at top with flash

                "[_min] obediently takes out his cock, shooting an enormous load all over her."

                with doubleflash

                play sound s_scream
                haruka "EEEK!!!"

                "Haruka's entire body is covered in sticky cum as the horny stallion empties his balls completely."

                show bg haruka big13 at top with flash

                play sound s_ahaa

                haruka "Ahaaa..."

                gizel "Woah, you're going to reek of cum all day after this..."

                haruka "Ughhh..."

                play sound s_evil_laugh

                gizel "Just like any other day, really. Bwahahaha!!!"


    elif min_type == "beast":

        gizel "Now is the time for her daily walk. She's enjoying some fresh air."

        show bg haruka beast1 at top with fade

        play sound s_surprise

        haruka blush "Mistress Gizel... How long do I have to stand like this..."

        haruka "I 'm cold..."

        gizel smirk "You're cold, are you?"

        "That won't do, you need something to warm you up."

        haruka "Yes, I..."

        haruka "Wait, what do you mean by that?"

        play sound s_whistle

        gizel "*whistle* [_min], come over here, you adorable critter!"

        haruka surprise "N-No, not [_min] again!" with vpunch

        play sound s_roar

        show bg haruka beast2 at top with dissolve

        "Running from the bushes, [_min] arrives on the scene, not hesitating a moment before climbing over Haruka."

        play sound s_scream

        haruka "Noooo!!!" with vpunch

        "With consumate skill, [_min] pushes Haruka's panties aside with his beastly dick, before shoving it inside her."

        haruka "AAAH!!!" with vpunch

        gizel "Come on, Haruka, your pussy should used to all sorts of animal dicks by now... Just focus on giving [MC.name] a good show."

        show bg haruka beast3 at top with vpunch

        haruka "EEEK! It's moving!"

        "The dog starts wiggling his hips, moving back and forth inside Haruka's pussy."

        gizel "You might think his dick is a bit small, but in reality it's swelling inside her, so it gets really thick."

        gizel "You feel that, Haruka?"

        play sound s_moans

        haruka "It's too much! It hurts! Aaaah..." with vpunch

        gizel "Pain is pleasure, I thought we had this covered by now."

        gizel blush "Now, tell me how it feels inside. Describe it."

        show bg haruka beast4 at top with dissolve

        haruka "It's... N-No... I'm so ashamed..."

        play sound s_roar

        "The beast increases its pace, frantically fucking Haruka with its weird dick."

        play sound s_scream_loud

        haruka "AAAH!!!" with vpunch

        gizel upset "Don't be impertinent. You know I have no patience for that. Answer my question!"

        haruka blush "I-It's growing inside me... Like an inflatable balloon..."

        gizel normal "And how does it feel?"

        play sound s_aah

        haruka "S-Strange... I don't know... Aaaah..."

        gizel "You know, I've noticed that our friend Haruka has a thing for big dicks..."

        gizel "Not only does she love being raped, but the more you ravage her pussy, the happier she gets."

        show bg haruka beast3 at top with dissolve

        play sound s_scream

        haruka "That's not tr... AAAAAH!!!" with vpunch

        gizel smirk "Oh yeah? Then you wouldn't like it if one of the stallions joined in?"

        play sound s_whistle

        gizel "*whistle*"

        show bg haruka beast5 at top with dissolve

        play sound s_aaah

        haruka "Ooooh...." with vpunch

        "Another minion joins the fray, poking his large dick on Haruka's face."

        play sound s_ahaa

        haruka "Ahaaa..." with vpunch

        "The beast keeps pounding her from behind, while pre-cum from the stallion's dick leaks on her face and body."

        haruka "Oooh..."

        "She looks lost within herself, overwhelmed by the strong smell of bodily fluids."

        gizel "I think we should turn up the humiliation even further. [MC.name], any ideas?"

        menu:
            extend ""

            "Fuck her mouth":
                you "You, the drooling moron, don't just stand there, use her mouth!"

                show bg haruka beast10 at top with dissolve
                play sound s_sucking

                "Obediently, the stallion starts fucking her face, shoving his dick deep inside her throat."


                haruka "Nggh, ngggh..." with vpunch

                "Haruka is doing her best to take his dick in, seemingly turned by being skewered from both sides."

                play sound s_roar

                _min "GRRRR!!!" with vpunch

                "Meanwhile, the beast is fucking Haruka even faster. You can tell it is close to the big finish."

                haruka  "NGGGH!!!" with vpunch

                "Haruka moans as the stallion pushes his monstrous dick all the way down her throat. He is about to explode as well."

                show bg haruka beast11 at top with flash

                "*SPURT* *SPURT*"

                with doubleflash

                play sound s_mmh

                haruka "*cough* *cough*... Aaaah..."

                "The stallion cums all over Haruka's face and hair."

                show bg haruka beast12 at top with flash

                play sound s_screams

                haruka "Aah, aaah, AAAAAAAAH!!!"

                play sound s_orgasm
                with doubleflash

                "It isn't long before [_min] cums as well, making Haruka erupt into an orgasm."

                haruka "Oh no... I came..."

                show bg haruka beast13 at top with dissolve

                play sound s_ahaa

                haruka "What have I... Become... Aaaah..."

            "Piss on her face":
                $ MC.evil += 2

                you "You, there, move it. I need to pee. Let's see how she likes that."

                play sound s_surprise

                haruka surprise "N-No!!!" with vpunch

                play sound s_roar

                show bg haruka beast6 at top with flash

                _min "*grunt*"

                with doubleflash

                "Oblivious to everything, the animal has reached its limit, shooting a wad of beastly cum deep inside Haruka's pussy."

                gizel "Look at that! She took it like a pro... Just like a real bitch in heat."

                show bg haruka beast7 at top with flash

                haruka blush "D-Don't say... That... I am no... Animal..."

                gizel "Oh really? You're just to prideful to admit to your true nature. But we'll do something about that."

                "Instructing the stallion to move aside, you whip out your dick."

                show bg haruka beast8 at top with dissolve

                play sound s_pee

                "*PEE*"

                haruka "Aaah! N-Nooo! *gulp*"

                "As she opens her mouth to protest, some of your pee lands on her tongue."

                haruka "EEEK!" with vpunch

                "She squeals, but that only makes it worse."

                show bg haruka beast9 at top with dissolve

                you "Phew, I feel better. Seems like she'd make a good human toilet."

                play sound s_evil_laugh

                gizel normal "That's an interesting idea. Maybe I'll have her sleep in the pigsty, as well."

                haruka "Oh no..."

                haruka sad "How far... Have I fallen..."

        gizel "Show's over."

        gizel smirk "I think I'll let her play with [_min] for today. *grin*"

    elif min_type == "monster":
        show bg haruka monster1 at top with fade

        you "G-Gizel? What's this?"

        "You give an uneasy look to the bulbous 'thing' occupying the middle of Haruka's cell."

        gizel smirk "Oh, don't worry, it's just [_min]. Say hi, [_min]."

        play sound s_bubbling

        _min "*unintelligible*"

        you "What about Haruka? Is she gone?"

        gizel "Oh, she's here, all right."

        gizel "[_min], show him."

        play sound s_stone
        show bg haruka monster2 at top with dissolve

        haruka blush "*cough* *cough* *gasp*"

        "The monster spreads its 'jaws' apart, revealing the exposed body of Haruka, floating on a wriggling mass of slimy tendrils."

        gizel "Haruka's been in there for a couple of hours already. Look how wet she is."

        gizel "Who knows how many orgasms she's had while she was inside? [_min]'s juices are strong aphrodisiacs."

        play sound s_mmmh

        haruka "Aaaah... Uhmmm..."

        gizel "Her body is super sensitive right now. She could cum from anything."

        play sound s_ahaa

        haruka "Nggh... I... Can't... Think... Straight..."

        gizel "Look, I'll show you something fun."

        show bg haruka monster3 at top with dissolve

        haruka "Aaaah!!!"

        "Gizel attaches a string to each of Haruka's nipples, giving you the end of one as she holds on to the other."

        gizel "Ready? On your mark, get set..."

        show bg haruka monster4 at top with vpunch
        gizel "GO!!!"

        play sound s_screams
        with flash
        haruka "AAAAAH!!!"

        play sound s_orgasm_fast

        "You both pull on the strings at the same time, painfully stretching Haruka's nipples."

        haruka "Oooh..." with flash

        "Haruka cums immediately, and she even starts squirting, splashing love juice all around."

        "[_min] looks pleased, inasmuch as you can tell for something that doesn't sport a face."

        show bg haruka monster3 at top with dissolve

        haruka "M-Make it stop... I keep... Cumming... It's too strong..."

        gizel "Hmph, you don't know what's good for you..."

        show bg haruka monster2 at top with dissolve

        "Reluctantly, Gizel removes the strings from Haruka's tits."

        haruka "I can't take any more..."

        gizel "Fufufu, you think we're done already?"

        gizel blush "[MC.name], my dear, I'm going to need your help."

        you "Sure."

        gizel "I've made sure to give Haruka's pussy plenty of training in the last days..."

        gizel "... But her asshole's been kind of neglected."

        gizel "Since you're here..."

        you "Say no more."

        play sound s_dress

        "*unzip*"

        haruka "What... What are you..."

        show bg haruka monster5 at top with dissolve

        play sound s_scream

        haruka "AAAH!!!" with vpunch

        "Haruka's asshole is slippery with all the fluids covering her, so you can slide your cock inside her easily."

        play sound s_mmmh

        haruka "My ass! You went all in... You're going to break it!"

        play sound s_moans

        "Even as she says that, Haruka can't control her moans. You can see her getting wetter with every thrust of your cock into her stretched asshole."

        haruka "Aaah... Aaah..." with vpunch

        "Moving your lubricated dick inside Haruka's butt is easy, and you increase your pace. Her hips start moving in tythm with your dick."

        haruka "My ass is being violated... B-But... W-Why..."

        play sound s_aaah

        haruka "Why does it feel so good... Aaah..." with vpunch

        "Tendrils tickle your balls, making you feel weird. Haruka's ass clenches around your dick, and you can tell she is in for another orgasm."

        play sound s_mmh

        haruka "Mmmh, mmmmh..." with vpunch

        "Hearing Haruka moan sexily as you fuck her lusty ass proves too much for you."

        show bg haruka monster6 at top with flash

        play sound s_scream_loud

        haruka "AAAAH! C-C-CUMIIIIIING!!!!"

        play sound s_orgasm

        with doubleflash

        "You cum hard inside Haruka's butt, filling her up with your spunk."

        with flash

        "The tentacle around her belly decides to squeeze it hard, making her squirt sperm out of her asshole."

        haruka "Oh no... I came so hard..."

        play sound s_evil_laugh

        gizel "Seems like she's a natural for anal..."

        $ MC.change_prestige(3)

        "Taking out your cock, you wipe it in Haruka's hair for good measure... But she doesn't notice it, as she is already passed out from multiple orgasms."

    elif min_type == "machine":
        gizel "She's in the middle of a training session with [_min]. I set its programming to hardcore..."

        play sound s_vibro
        show bg haruka machine1 at top with fade

        "You find Haruka in the basement, riding a strange contraption that you recognize as [_min]."

        haruka blush "M-Master... [MC.name]... Aaaah..."

        gizel "See? She addressed you properly. She is starting to know her place, now."

        gizel "She's been here for half an hour already. [_min] has been working her nice and slow..."

        play sound s_ahaa

        haruka "Mmmh..."

        gizel "Haruka, would you be a doll and describe to your master here what [_min] is doing to you?"

        play sound s_vibro

        haruka "Nggh... Ah!!!" with vpunch

        haruka "T-There's a dildo... In my pussy..."

        haruka "And another one... In my ass..."

        gizel "Good girl! Here, let me give you a small reward."

        play sound s_vibro
        show bg haruka machine2 at top with vpunch

        "Gizel turns up the vibration speed on [_min]."

        play sound s_aah

        haruka "Aaaah!!!"

        gizel normal "I am currently training her to resist orgasm, because she has become a little too slutty lately."

        you "Too slutty? Is there any such thing as 'too slutty'?"

        gizel "Well, you don't want her to be unable to control herself around customers, do you?"

        gizel "It's a normal part of training of a sex slave to learn to restrain your urges..."

        play sound s_vibro
        show bg haruka machine3 at top with vpunch

        haruka "A sex slave... Me..."

        "This time, the words 'sex slave' rolled off her tongue more easily. Could it be the beginning of... Acceptance?"

        you "What's keeping her from cumming?"

        gizel smirk "Fufufu... It's one of my better tricks."

        gizel "Haruka spent the whole night milking stallions, feeling a large vat full of cum."

        play sound s_vibro

        haruka "N-Ngh..." with vpunch

        gizel "The vat is right underneath the contraption. If she cums, [_min] is programmed to open a valve, and her precious holes will be filled up with pressured cum."

        gizel "It will really mess up her insides. So she'd better not cum, or else..."

        "Haruka blushes bright red, and you can tell she is nearing her limit."

        gizel "You're not about to let it slip, now, sugar?"

        gizel "Think of all the hot cum that would enter your pussy and ass... It would mess you up forever..."

        play sound s_ahaa

        haruka "N-Nggh..." with vpunch

        play sound s_vibro

        "Winking at you, Gizel turns up the vibrations even more."

        play sound s_scream

        haruka surprise "N-No! Don't!!! I can't resist that much..."

        "Panicked, Haruka does her best to try to hold it together."

        gizel "You know, even though the pain would be unbearable, I bet you would cum so hard if that happened..."

        play sound s_vibro

        gizel "Think of all that sweet cum... Just waiting to fill you up..." with vpunch

        play sound s_aah

        haruka "Oooh..." with vpunch

        "Haruka blushes bright red. She clenches har teeth, but you can tell she is losing this fight."

        play sound s_mmh

        haruka "Gallons of c-cum... Shooting... Inside... Me..."

        play sound s_scream_loud

        show bg haruka machine2 at top

        haruka "AAAAH!!!!" with vpunch

        play sound s_splash
        show bg haruka machine4 at top with flash

        "Unable to resist, Haruka finally cums. Within a split second, [_min] opens the valve and highly pressured cum starts erupting through."

        play sound s_scream_loud

        haruka "AAAAH!!! It's filling me up! I can't take iiit!!" with doubleflash

        play sound s_evil_laugh

        gizel "Oh my, you've really done it this time!"

        gizel "It went all in! Look, she's about to burst with cum."

        show bg haruka machine5 at top with dissolve

        haruka "My belly... My insides... What's happening to me..."

        gizel "You know what, let's turn the vibrations up to eleven. She really deserves it."

        haruka surprise "Wait, that wasn't the maximum?"

        play sound s_vibro

        haruka blush "G-GHHHH!!!" with vpunch

        haruka "Oh no!!! I'm... I'm cumming again!!!"

        show bg haruka machine6 at top with flash

        play sound s_splash

        "*SPLASH* *SPLASH*"

        play sound s_screams

        haruka "AAAAAAAAARRH!!!"

        play sound s_orgasm

        "Cumming hard, Haruka squirts semen everywhere as it splashes out of her cunt and asshole."

        gizel "Phew, that was a good lesson. I doubt she'll be able to walk for a while after this, but it was worth it."

        haruka sad "Aaaah... I'm filled with cum... And I came so hard... I'm such a degenerate now..."

    scene black with fade
    return

label haruka_broken:

    play sound s_rooster

    scene black with fade
    show bg farm at top with dissolve

    show gizel normal with dissolve

    gizel "Good news, [MC.name]! All my hard work on Haruka has paid off."

    show gizel at left with move
    show haruka_humble at right with dissolve

    haruka blush "Hello, Master [MC.name]."

    gizel smirk "Tell him what you told me."

    haruka "..."

    gizel upset "Tell him!" with vpunch

    haruka sad "Yes. Master, I..."

    haruka "I'm sorry. I was blinded by my pride, but I now realize..."

    haruka "I have no skill as a ninja, and I failed my mentor and my friends. I am worthless."

    haruka "Every time I tried to take matters into my own hands, I ended up failing completely. I am not fit to live a free life."

    haruka "I don't even know if I'm worthy of being a whore..."

    haruka "But if I need to use my weak body to please others, to atone for my sins, it is a fate I will accept."

    gizel smirk "There. That wasn't so hard, wasn't it? You're a slut that loves to be raped. There's no shame in that."

    haruka blush"..."

    gizel normal "Now that we took care of the small matter of breaking the girl's pride, let's think about the next step. [MC.name]?"

    menu:
        extend ""

        "Try her for yourself":

            you "Well, I was waiting for that day! Bring her to the brothel, I will personally make sure she's ready."

            scene black with fade
            show expression bg_bro at top
            with dissolve

            show haruka_humble with dissolve

            haruka blush "M-Master... What do you want me to do..."

            you "I want you to treat me like a VIP customer. Show me what you have learned."

            haruka "O-Okay..."

            you "Take the lead. I will be evaluating your performance."

            haruka "Yes Master..."

            scene black with fade
            show bg haruka cowgirl1 at top with dissolve

            haruka "H-Hello Sir, welcome to [brothel.name]."

            haruka "My name is Haruka, and I am here to... Serve all your needs today..."

            play sound s_sigh

            haruka blush "I hope... Mmh... My filthy body can make you happy... Hmmm..."

            you "Don't mumble. Some customers enjoy a shy girl, but you are expected to take the lead, remember?"

            haruka "Ahem, yes Master."

            haruka "Would you like to touch my breasts? I am told they're the best part of my body."

            play sound s_dress

            show bg haruka cowgirl2 at top with dissolve

            haruka "Hmmm... I hope you like them..."

            you "Not bad, Haruka. But look at me, down there. Can't you see I need something?"

            haruka "Oh! Oh my, Sir, you are already rock-hard...I-It makes me happy..."

            haruka "Here, would you like to rub your penis inside my body suit?"

            play sound s_dress

            you "Hmmm... That's kinky..."

            haruka "Something smells good... I think you're leaking pre-cum already."

            play sound s_aah

            haruka "It's making me wet... Haaa..."

            you "That's nice, Haruka. Keep the dirty talk coming."

            play sound s_mmmh

            haruka "Aaah, hmmm..."

            haruka "Sir, if you keep rubbing against me like that, I'm going to lose control..."

            haruka "My dirty pussy is all wet now... I need s-something... Inside me..."

            you "Then what are you waiting for? Take matters into your own hands!"

            show bg haruka cowgirl3 at top with dissolve

            "*SQUISH*" with vpunch

            "Guiding your dick with her soft hand, Haruka pushes it inside her."

            "She is already completely wet, and her pussy engulfs your shaft easily."

            play sound s_ahaa

            haruka "Aaaahaa..." with vpunch

            haruka "Oh, Mister, you're so big... I am so lucky to serve you..."

            "She starts grinding her hips, pleasantly stimulating your dick."

            you "You love big cocks, don't you?"

            haruka "Y-Yes, I do... I like a huge dick stretching my pussy to the limit..."

            you "Don't forget that not all customers are well-endowed. You don't want to make the little ones feel bad..."

            haruka "Oh, that's right... Of course, Master, I won't tell them that... Unless I mean it."

            you "Good. Keep moving."

            play sound s_aaah

            haruka "Hmm... Aaah..." with vpunch

            "You lay back and enjoy the show, as Haruka is doing all the work."

            play sound s_mmh

            haruka "Hmmm... Aaaah..." with vpunch

            "Even though you are barely doing anything, Haruka seems to enjoy herself well enough."

            play sound s_moans

            haruka "Oooh... Aaah..." with vpunch

            "Her pace is increasing, and it seems like she may be able to bring herself off by herself."

            you "Hey, talk to me. Don't focus on yourself, focus on the customer."

            haruka "Right... S-Sorry, Master."

            "She clenches her pussy around your shaft with surprising strength."

            haruka "Do you like... That..?"

            you "Oh yes."

            haruka "Let me massage your cock with my slave pussy. Master- I mean, Sir."

            play sound s_moans_short

            haruka "Aaaah, aaaaah!" with vpunch

            "She is bouncing off your dick hard now, and you can't help but feel your excitement building up."

            haruka "Ooooh... Aaaah..." with vpunch

            show bg haruka cowgirl4 at top with dissolve

            "Your cock hits her cervix repeatedly, making her moan even deeper."

            you "I want to cum inside you, Haruka."

            haruka "O-Of course, Sir..."

            haruka "Today is not a safe day, but... I am taking magic contraception, so don't worry."

            you "Like I care about that! Get ready, I'm going to creampie you."

            play sound s_mmh

            haruka "Y-Yes, Sir... Mmmmh..." with vpunch

            show bg haruka cowgirl5 at top with flash

            you "*GROAN*"

            with doubleflash

            play sound s_scream

            haruka "AAAAAAAAH!!!"

            play sound s_orgasm

            with flash

            "Haruka cums at the same time as you, crying out loud as you fill her with creamy semen."

            haruka "Ooooh... Master [MC.name]..."

            you "Hmmm... It was good... But stay in character."

            haruka "O-oh, sorry. Sir."

            "She keeps rubbing her hips against you for a while longer, still basking in the feeling of her orgasm."

            you "You'll make a fine whore. No doubt about that."

            show bg haruka cowgirl6 at top with dissolve

            haruka "T-Thank you."

            "Giving you an inviting smile, she scoops up some of your love juice with her finger."

            "She places it in her mouth, and starts sucking on it suggestively."

            you "Hmm, that's a nice touch."

            haruka "I thought the customers might like it when I do that."

            you "I'm sure they will."

            $ MC.change_prestige(3)

        "Test her with customers":

            you "About time! Let's round up some customers, make sure she is ready."

            $ cust = rand_choice(get_available_populations()).get_rand_name()

            scene black with fade

            "Sill gathered a group of regular customers, led by a [cust]."

            "They were intrigued by the perspective of getting it on with one of the infamous kunoichi."

            show bg onsen at top with dissolve

            show haruka_swimsuit with dissolve

            haruka blush "Welcome to [brothel.name], dear guests. Please follow me."

            "[cust!c]" "Wow, she's super hot!"

            "[cust!c]" "I was expecting her to be all muscular and stuff but... Man, she's perfect!"

            haruka "Thank you Sir, you are very kind..."

            "[cust!c]" "And check that ass..."

            play sound s_boing

            "*SMACK*" with vpunch

            "The customer slaps Haruka's ass. For a split second, you worry she's going to strike him back, but she just blushes."

            haruka "Please follow me. *blush*"

            scene black with fade
            show bg haruka massage1 at top with dissolve

            "[cust!c]" "Hmmm... So that's the taste of Kunoichi sweat..."

            play sound s_aah

            haruka blush "Ah, Mister..."

            "The [cust] is playing with Haruka in the sauna, while his buddies leer and jeer."

            haruka "Mister, if you keep touching me all over... Aaaah..."

            "[cust!c]" "What's that? I don't understand... *squish*"

            show bg haruka massage2 at top with dissolve

            play sound s_ahaa

            haruka "Ahaaa..."

            "The customer rubs himself against Haruka's butt, caressing her inner thigh. She is getting visibly wet."

            "[cust!c]" "Ain't you a sensitive thing? I only started touching you, and you're in the mood already..."

            haruka "I'm afraid so... I am a dirty whore..."

            "[cust!c]" "Of course you are! [MC.name] knows how to pick them."

            show bg haruka massage3 at top with dissolve

            "Other customer" "Man, you're having all the fun! Just looking at these titties, I get hard as fuck."

            haruka "S-Sorry, dear customer... You will get your turn..."

            show bg haruka massage4 at top with dissolve

            "More customers" "And don't forget about us too!"

            play sound s_sigh

            haruka "S-Sure..."

            "Other customer" "I wanna see those titties!"

            "[cust!c]" "Yeah, show us the goods!"

            haruka "O-Okay... Will you give me a little tip?"

            "[cust!c]" "Hmph... Here you go..."

            $ MC.change_gold(50)

            play sound s_dress

            show bg haruka massage5 at top with dissolve

            "All customers" "Whoah!!!"

            "Other customer" "Let me pull on these nipples... Hmmm, I wanna twist and tug them!"

            play sound s_surprise

            haruka "Aaaaaah!!! Please, Sir, I'm sensitive there..."

            "Other customer" "Shut up, whore, I paid, so I can be as rough as I want!"

            show bg haruka massage6 at top

            play sound s_scream

            haruka "Haaaah!" with vpunch

            "[cust!c]" "Look at her, she's not even trying to stop you!"

            "The customer is tugging at her nipples, eliciting painful moans from Haruka."

            "[cust!c]" "I've heard so much about the Kunoichi, but it seems that they are a joke..."

            haruka "N-No... The Kunoichi are not a joke... But I am not worthy of them."

            "Other customer" "You're just a slut, then, only good for taking cock? Am I right?"

            play sound s_sigh

            haruka "I... Yes, it's true."

            "[cust!c]" "Then enough fooling around! Get ready."

            play sound s_dress

            show bg haruka massage7 at top with fade

            haruka blush "Hmmm... Sir... Do you like this position?"

            "[cust!c]" "Damn right I do! Make sure to give my mates a great view!"

            "The [cust] spreads Haruka's legs apart, rubbing his manhood against her clit."

            play sound s_mmmh

            haruka "Hmmmh..."

            "It isn't long before he is rock-hard."

            "[cust!c]" "Enough waiting! I'm going in!"

            "Other customers" "*CHEER*"

            show bg haruka massage8 at top with dissolve

            haruka "AAAH!!!" with vpunch

            "[cust!c]" "Oh, your pussy's good! Feels like you were expecting me."

            haruka "Oh... It's my first for today... Mistress Gizel never left me that long without... Well..."

            "[cust!c]" "Come on, move your body! Show me how a Kunoichi fucks!"

            haruka "Y-Yes, Sir!" with vpunch

            "Moving her hips, Haruka starts fucking the customer enthusiastically, barely aware that she's being watched by the group."

            "[cust!c]" "Oh, you're good!"

            "Using the strong muscles in her thighs and pussy, she rides and squeezes the customer's dick in unexpected ways."

            "[cust!c]" "Oh, Shalia, she's strong! OH!!!"

            show bg haruka massage9 at top with flash

            play sound s_surprise

            haruka "Haaah! [emo_heart]"

            with doubleflash

            "Unable to resist, the [cust] explodes inside Haruka's pussy, smearing it with smelly cum."

            show bg haruka massage10 at top with flash

            play sound s_mmmh

            haruka "Hmmm..."

            "Other customer" "Bwahaha, you barely held in there for a minute!"

            "[cust!c]" "Grrr... She surprised me..."

            play sound s_ahaa

            show bg haruka massage11 at top with dissolve

            haruka "Ahaa..."

            haruka "Mister, you really came a lot... I'm happy..."

            $ MC.change_gold(100)

            "[cust!c]" "Here's a tip... I'm gonna need a moment to recover... Ooooh..."

            "Other customer" "Then it's my turn! Yeehah!"

            show bg haruka massage12 at top with dissolve

            play sound s_surprise

            haruka "Aaah, Mister!" with vpunch

            "Not wasting time, another customer jumps at the opportunity and starts fucking Haruka from behind."

            haruka "Oh, Mister, you're so rough!" with vpunch

            haruka "You're stirring up my insides..."

            "In spite of her protestations, Haruka seems lost in pleasure as the customer rams her doggy-style."

            "Other customer" "Come on, squeeze my dick like you did for him! Show me that Kunoichi power!"

            haruka "Aaah, hoh, oh..." with vpunch

            "Suddenly, Haruka tenses up, and you can almost see a shockwave riding out from her pussy, hitting the customer's dick."

            "Other customer" "OWHOOOH!!!" with vpunch

            show bg haruka massage13 at top with flash

            "Overwhelmed by pleasure, the customer cannot help but cum hard inside Haruka's tight pussy."

            with doubleflash

            "[cust!c]" "See? I told you, she's something else!"

            "Haruka's cunt keeps squeezing the customer's dick until she milks the last drop of his cum."

            show bg haruka massage14 at top with flash

            $ MC.change_gold(100)

            "Other customer" "Man... That was incredible... T-Take that, I think I'm gonna pass out..."

            "[cust!c]" "Then fuck off! I'm ready for round 2!"

            "Other customers" "Hey, what about us?"

            "[cust!c]" "Just get in line! I'm the one who got you in, so I get dibs on ninja pussy!"

            show bg haruka massage15 at top with dissolve

            haruka "Please, everyone, I must ask you for your patience..."

            "Customer" "Shut up! Hold my dick!"

            "[cust!c]" "I'm hard again! Do your worst, Kunoichi!"

            show bg haruka massage16 at top with dissolve

            play sound s_aaah

            haruka "Aaaah..."

            haruka "Aaaah!" with vpunch

            "[cust!c]" "Oh, yeah... It's even better the second time!"

            "Other customer" "I'm done waiting. Why don't I use her other hole?"

            haruka "M-Mister..."

            show bg haruka massage17 at top with dissolve

            haruka "Aaah!" with vpunch

            "The man pushes his cock near her tight asshole."

            haruka "P-Please, Sir! I haven't had much training with this hole yet!"

            "Other customer" "Perfect! Then I'll help you get more experience."

            show bg haruka massage18 at top with dissolve

            play sound s_scream

            "Ignoring her resistance, the fat man forces his cock deeper inside her ass."

            play sound s_moans

            haruka "Oh, I'm being fucked from both sides... Aaaah..." with vpunch

            "Both guys start fucking Haruka's holes in rhythm, while she does her best jerking off the other customers with her hands."

            "[cust!c]" "C'm'on, Kunoichi, use your secret powers! Make us cum!"

            "Other customer" "Yeah, you can go all out!"

            haruka "Hmmmh... Aaah..." with vpunch

            "With a look of resolve, Haruka starts concentrating."

            haruka "A-As you wish... I will now use my whole body... To pleasure you..."

            haruka "OMAE WA! MOU IKU!!!!" with vpunch

            "Other customer" "What was that?"

            "[cust!c]" "I think it's a Kunoichi battlecry or som-"

            play sound s_wscream

            "[cust!c]" "OWHOOOOH!!!" with vpunch

            with vpunch

            "Haruka's entire body tenses up, and waves of energy radiate from her naked form as she squeezes the many dicks around her."

            show bg haruka massage19 at top with flash

            "*SPURT* *SPURT*"

            play sound s_scream_loud

            haruka "HAAAAAHH!!!" with doubleflash

            play sound s_orgasm_fast

            show bg haruka massage20 at top with flash

            "Other customer" "OOOOOF!!!"

            "[cust!c]" "*GROAN*" with doubleflash

            "All the customers cum one by one, showering Haruka with hot cum and creampying both her holes."

            "Haruka came hard as well, giving her all to satisfy the customers."

            show bg haruka massage21 at top with flash

            haruka "T-Thank you, dear customers..."

            haruka "I am lucky to receive your precious cum..."

            haruka "Please... Come again to [brothel.name]..."

            $ MC.change_gold(250)

            scene black with fade
            show bg onsen with dissolve
            show haruka_swimsuit with dissolve

            you "Whoah, well done, Haruka!"

            haruka blush "T-Thank you, Master."

            you "I must say, I was worried about how you'd do... But you handled it like a pro."

            haruka "..."

    you "Very good. Welcome to the team! You can start working tonight."

    haruka blush "S-Sure. Thank you for having me."

    haruka sad "(So this is my life, now... I wonder if I can get used to it.)"

    $ unlock_achievement("haruka captured")

    $ girl = create_girl("Haruka Takamori", force_original=True, level=10)
    $ girl.pop_virginity("rape")

    call acquire_ninja(girl) from _call_acquire_ninja_1

    return

## End of Haruka events ##

# Generic acquire ninja menu #
label acquire_ninja(girl):

    if not NPC_gizel.flags["held_girls"]:
        $ NPC_gizel.flags["held_girls"] = []

    if len(MC.girls) >= brothel.bedrooms:

        girl.char "B-But! There is no room in the brothel for me..."

        if farm.active and farm.has_room():
            you "You should go to a pen at the farm."

            girl.char "Okay..."

            if girl in NPC_gizel.flags["held_girls"]:
                $ NPC_gizel.flags["held_girls"].remove(girl)
            $ farm.programs[girl] = FarmProgram(girl)
            $ girl.init_after_acquire()
            call send_to_farm(girl, can_beg=False, can_cancel=False, can_follow=False, silent=True) from _call_send_to_farm_5

        else:

            you "Damn, the farm's pens are full at the moment..."

            gizel "I'll keep her around to do chores. Talk to me when you are ready to accomodate her."

            scene black with fade

            "Once you have room for [girl.name], click on Gizel's portrait at the {b}Farm{/b} to recover her."

            $ NPC_gizel.flags["held_girls"].append(girl)

    else:
        scene black with fade

        if girl in NPC_gizel.flags["held_girls"]:
            $ NPC_gizel.flags["held_girls"].remove(girl)
        $ MC.girls.append(girl)
        $ girl.init_after_acquire()

        "[girl.name] has joined [brothel.name]."

    return

# End of ninja story label #
label c3_end_story(ninja):

    # Sanity check

    if not ninja.flags["c3 path"]:
        $ raise AssertionError("Warning: No c3 path found for %s. Please report this bug." % ninja.name)
    
    $ game.set_task(None, {NPC_haruka: "story", NPC_mizuki: "story2", NPC_narika: "story3"}[ninja])
    $ rune = {NPC_haruka: earth_rune, NPC_mizuki: water_rune, NPC_narika: void_rune}[ninja]

    if rune in MC.items:
        call remove_item(rune, definite_article=True)

    # Checks if all ninja storylines are complete
    if NPC_haruka.flags["c3 path"] and NPC_mizuki.flags["c3 path"] and NPC_mizuki.flags["c3 path"] != "waiting" and NPC_narika.flags["c3 path"] and NPC_narika.flags["c3 path"] != "MagicU":
        $ game.set_task("Wait for the Princess to hear about your progress.", "story")
        if not story_flags["c3 all kunoichi resolved"]:
            $ story_flags["c3 all kunoichi resolved"] = True
            $ suzume_hints_active = False
            $ calendar.set_alarm(calendar.day + 2, StoryEvent(label="c3_palace_visit"))

    return



## Chapter 3's Conclusion ##

label c3_palace_visit(): # Happens in the morning after all Kunoichi have been stopped

    scene black with fade
    show expression bg_bro at top
    with dissolve

    play sound s_knock

    "Once more, this morning, the princess sent a royal carriage to your doorstep."

    you "I have now seen to all three of the Kunoichi terrorizing the neighborhood... No doubt Princess Kurohime wants to talk about that."

    scene black with fade
    show bg castle at top with dissolve

    if NPC_kenshin.flags["dead"]:
        "As you pass by a poorer part of town, a group of scruffy children spots the carriage and start pelting it with stones, yelling colorful slurs about the King."

        "The driver whips his horses to cross the neighborhood faster, before heaving a sigh of relief as you spot the reassuring sight of the castle walls."

        "Driver" "These damn urchins would never have dared attack us back in Lady Kenshin's days... This city is going to the Seven Hells in a hand basket, let me tell ya."

    else:
        "As you're about to cross the bridge to the palace, the carriage as to slow down to make it's way past a group of noblemen loudly arguing."

        "Noble" "We need to stop with this dilly-dallying. Princess Kurohime will soon turn twenty-five, and she remains unmarried. Is the King so impotent that he can't make his own daughter obey him and marry my brother?"

        "Other noble" "Excuse me? Princess Kurohime would be a much better match for me. {b}I{/b} have just acquired the rights for all wine imports from Borgo, in perpetuity!"

        "Noble" "Ridiculous. This city has more than its share of upstart peddlers. My brother comes from one of Zan's oldest families, and he is a war hero..."

        "Other noble" "Your brother is a drunkard, he lost his leg when it got crushed by a beer keg... War hero? More like a war cripple!"

        play sound s_sheathe

        "Noble" "Say that again? I'll gut you!"

        "Courtier" "Gentlemen, gentlemen, please. The King will soon reach a decision. He has his reasons for delaying the wedding, I'm sure..."

        "Noble" "Damn the King and his bloody indecision!"

        "Other Noble" "Yes! The city's going to hell, and he's too incompetent to do anything about it!"

        "Courtier" "You dare call the King names, do you? Guards!"

        "A scuffle starts, and the driver hurries past the group onto the relative safety of the bridge."

    play music m_palace fadein 3.0

    scene black with fade
    show bg palace room at top with dissolve

    "You are still thinking about the incident when the princess shows up."
    show kuro with dissolve

    kuro "Welcome, [MC.name]. I was hoping we could catch up after the events of the last few weeks."

    you "Of course. I guess I have both good and bad news."

    kuro "Good news first, I beg you."

    you "Well, all three of the Kunoichi that were roaming the city have been caught or neutralized."

    kuro "That's a relief. What about the bad news?"

    you "I couldn't trace their actions to our killer. I'm afraid the rumors may have been wrong; maybe he has no connection to the Kunoichi after all."

    kuro "At least, let us review what we've learnt..."

label c3_palace_visit_menu(): #! Hide used-up questions later

    menu:
        "About the stolen magical mask" if NPC_narika.flags["c3 path"] in ("ally", "neutral", "banished", "raped"):
            with fade

            kuro "So you say a magical artifact was stolen from the Magic University, a mask that could make the blind see?"

            you "Yes."

            if NPC_narika.flags["c3 path"] in ("ally", "neutral"):
                kuro "And this note you found? What did it say?"

                you "'Now Haku will have his revenge.' Corny, I know."

                "Ignoring your attempt to make a joke, the princess's face is locked in a frown. She looks dead serious."

                you "Does this name ring a bell? Haku?"

                kuro "I'm afraid so."

                you "Who is it, then?"

                "Kurohime hesitates for a second, about to tell you, but she shakes her head."

                kuro "I'm afraid I can't let you know this information just yet. Not before I have a talk with my father."

            kuro "Anyway, the strange contraption the assassin was wearing must be this mask. It would be too strange of a coincidence otherwise."

            you "I agree."

            kuro "So this man must be originally blind... Thats is an important clue."

            $ story_flags["c3 clue mask"] = True

            jump c3_palace_visit_menu

        "About Kenshin's family" if NPC_mizuki.flags["c3 path"] in ("redeemed", "revenge"):
            with fade

            kuro "Ah, yes, I was as stunned as you were to learn about Uesugi's family history..."

            if not NPC_kenshin.flags["dead"]:
                you "Why isn't she here, by the way?"

                play sound s_sigh

                kuro "I've been keeping her at arm's length, to be honest. She's obviously distraught, but I have also begun to worry that she may be a liability."

                you "That boy Mizuki mentioned..."

                kuro "I am looking into it. Lord Mitsuhide disappeared around the time of my birth, almost twenty-five years ago to the day."

                kuro "It seems he was maybe not running away as much as protecting that boy..."

                you "And that boy was attacked by demons, and ended up blind."

                kuro "Indeed."

                you "You think this boy may have a link to our killer?"

                if story_flags["c3 clue mask"]:

                    kuro "He'd be about my age now... So maybe he {i}is{/i} the killer."

                    you "He was blind... That would be why he stole that mask..."

                    you "But he had to get help."

                $ story_flags["c3 clue boy"] = True

            else:
                you "I'm sorry for your loss."

                kuro "Yes, her death has weakened my hand significantly."

                kuro "Nevertheless, I think her father's fate may yet shed some light on the motives behind these killings..."

                you "How so?"

            kuro "I need to check up on some old rumors... But I will let you know as soon as I find something solid."

            jump c3_palace_visit_menu

        "About demon worship within the Knights' ranks" if NPC_haruka.flags["c3 path"] in ("ally", "banished"):

            with fade

            kuro "Demons among the Knights, you say? I trust you, but this is stretching the limits of my gullibility..."

            you "I know it's hard to believe, but I have seen them with my own eyes!"

            kuro "Curses. Why didn't Kenshin tell me anything about this?"

            kuro "The Kingdom relies on knight for so many things. Probably too much."

            kuro "It's high time we dealt with this weak spot..."

            you "What are your intentions?"

            kuro "I cannot divulge them for the moment. But if demons are indeed corrupting the knight orders, swift action will be needed to nip this conspiracy in the bud"

            $ story_flags["c3 clue demons"] = True

            jump c3_palace_visit_menu

        "Nothing else":
            pass

    if story_flags["c3 clue mask"] and story_flags["c3 clue boy"] and story_flags["c3 clue demons"]:

        kuro "This paints a clearer picture, doesn't it?"

        you "A mysterious boy living in the wood..."

        kuro "He got blinded in an attack..."

        you "Grew up into a man, then stole a mask to recover his eyesight..."

        kuro "To enact his revenge against demons from the Knight orders."

        you "He must believe the entire Royal family is in cahoots with demons."

        kuro "Preposterous! But I could see how he would believe that..."

    elif story_flags["c3 clue mask"] and story_flags["c3 clue boy"]:

        kuro "There is a high chance that the masked killer and that blind boy are the same person."

        you "But why would he be after the Royals?"

        kuro "We have yet to discover why. Perhaps if we knew why Lord Mistuhide ran away from Zan one night to live in the forest..."

    elif story_flags["c3 clue demons"] and story_flags["c3 clue boy"]:

        you "These demons, are they the same that attacked the boy in the forest?"

        kuro "Your guess is as good as mine."

        you "Could this boy be related to the murders?"

        kuro "But he was blinded in the attack. Our killer can see..."

    elif story_flags["c3 clue demons"] and story_flags["c3 clue mask"]:

        you "A magical artifact getting stolen, demons among the knights... What is the link between these facts?"

        kuro "I have no idea."

        you "We still need to investigate further..."

    with fade

    you "I think I have exhausted all avenues of investigation for now."

    kuro "We have no more lead, then."

    you "I'm afraid so."

    kuro "I find a small measure of relief in that there hasn't been any high-profile murder in a while."

    kuro "But we would be fools to believe the masked killer is done here. He must be biding his time..."

    you "What can we do about it?"

    kuro "I have a mind to lay down a trap for him."

    you "How?"

    kuro "It is still early, but I have concepts of a plan."

    kuro "I will send for you once the pieces are in place. In the meantime, we must be discreet."

    you "Of course, Your Majesty."

    kuro "It is almost noon. Please attend the luncheon with me."

    $ calendar.set_alarm(calendar.day + 3, StoryEvent(label="c3_homura_invitation"))
    $ game.set_task("Wait events to unfold.", "story")

    menu:
        you "Well..."

        "Sure":
            $ norollback()
            "Your stomach thinks this is a good idea."

            you "It would be my honor."

            kuro "Don't be silly. These events are dreadful. But your presence will help."

        "I can't":
            $ norollback()
            "While the offer of free food is tempting, you find the atmosphere at court to be suffocating."

            you "Thank you for your offer, Your Majesty. But I have other business to tend to."

            if NPC_kuro.flags["occupation"] == "truth":
                kuro "I suppose you need to take care of your... business. I understand."
            else:
                kuro "Ah, yes, your little operation won't take care of itself. Of course."

                "You see a glint of amusement in her eyes, but nervously dismiss it."

            you "Goodbye, Princess."

            return

label c3_luncheon: # Follows previous event

    scene black with fade
    show bg palace reception at top with dissolve

    $ _choice = defaultdict(list)

    "The luncheon is in full swing when you enter the room. Who do you wish to join?"

    $ i = 0

    while i < 2:
        $ i += 1

        if i == 2:
            "The luncheon is near its, but you still have a little time to mingle. Who do you want to see now?" with fade

        menu:
            extend ""

            "The princess" if not _choice["princess"]:
                $ norollback()
                $ _choice["princess"] = True

                show kuro with dissolve

                "Foreign courtier" "With all due rezpect, Your Grace, my fazer may be old, but he iz still spry. And you're a lady about to turn twenty-five, it iz not like you are, how you say... The spring chicken, yourself."

                "In spite of her usual coolness, you can see the princess going red in the face up, almost about to burst at the man's impertinence, until she spots you."

                kuro "Oh! Sir [MC.name]! Excuse me, My Lord. Send your father my regards, but my answer is 'no'."

                "Ignoring the man's protests, the princess steps aside with you. You feel the sting of a dozen jealous stares."

                kuro "Back so soon? I'm beginning to think you enjoy my company..."

                menu:
                    _("Of course"):                        $ NPC_kuro.love += 2

                        you "Of course, Your Highness. Who wouldn't?"

                        kuro "Oh, you charmer. But you should be careful what you say in here. Half these men are would-be suitors, and some are getting so impatient that I wouldn't put it past them to use violence against another pretender."

                        you "I have faced worse dangers for lesser prizes."

                        play sound s_laugh
                        kuro "Teeheehee, you amuse me [MC.name]."

                    "It's not that":
                        $ NPC_kuro.love -= 1

                        you "I'm only looking to discuss our mutual interests."

                        kuro "Of course you are. As is everyone around me. Alas, this is the cruel fate of all rulers: we only exist in the eyes of others to advance their goals..."

                        you "I didn't mean that..."

                        kuro "I know, I jest. This whole mess has me on edge..."

                you "By the way, how is this marriage intrigue shaping up?"

                kuro "Don't remind me. I have just about exhausted all my options to delay this woeful affair."

                kuro "It's just as well that my father is feeling ill, again. But once he gets back to his throne and remembers his duties, he will have to make a choice."

                you "Don't you get a say in it?"

                kuro "Inasmuch as I can influence him, I will try to sway his opinion, but... He listens to his council of advisors more than he does me."

                kuro "They wouldn't stoop so low as to take a woman's opinion... Curse them and their stupid 'tradition'!"

                "Her anger piercing through her usually calm demeanor strikes you as out of character."

                you "My Lady?"

                kuro "I'm sorry, it's just... This is a stressful time."

                kuro "What do I need a husband for? It's just dead weight. The Kingdom doesn't need that. Not now."

                kuro "Things would be so much simpler if women were allowed to rule."

                menu:
                    _("You're right"):                        $ NPC_kuro.love += 1
                        you "You're right. You're a more capable ruler than anyone in this crowd."

                        kuro "I am glad you see that."

                        kuro "Whoever I marry will have to come around to the fact that {i}I{/i} will still be the one calling the shots."

                    "What?":
                        $ NPC_kuro.love -= 2
                        you "Women, lead??? Preposterous!"

                        you "Your Highness, surely you can't mean that. You need a husband's steady hand to guide you, especially in these troubled times... There is only so much a woman can do."

                        "Her eyes dart daggers at you."

                        kuro "Your opinion is noted. Not that I haven't heard it voiced a hundred times before."

                kuro "Look, I need to get back to my guests. I'll be in touch, for the next phase of our plan."

                hide kuro with dissolve

            "A group of knights" if not _choice["knights"] and NPC_kenshin.flags["dead"]:
                $ norollback()
                $ _choice["knights"] = True

                "A group of knights and men-at-arms are brooding in a corner, closed faced with their arms folded. You hover just near enough to overhear their conversation."

                show initiate at left, flip:
                    zoom 0.9
                show hound_leader at flip:
                    xalign 0.3
                    yalign 1.35
                show guard at right:
                    yanchor 0.0
                    ypos 0.0
                    zoom 1.5
                show knight:
                    xalign 0.7
                    yalign 1.35

                with dissolve

                initiate "...with Lady Kenshin gone, who's even going to be in charge?"

                knight "Lord Kayen stepped up, but most orders have yet to recognize his authority."

                initiate "The old man is out of his depth. He doesn't have what it takes to lead."

                knight "Then who? Every over half-capable officer is off to the warfront anyway."

                hound_knight "Why would we even need someone in charge?"

                initiate "What do you mean?"

                hound_knight "This idea of grouping the Knight orders under a single banner was always at odds with what our vows. An attempt by the Crown to control us."

                hound_knight "The truth is that we all have our own beliefs and purpose, and it shouldn't be shameful to admit it would be best to preserve our independence from political intervention."

                guard "'Tis dangerous talk, Sir Knight..."

                hound_knight "Is that so? *eyes narrow*"

                guard "No offense, but I heard the higher-ups are discussing ditching the knights as their main forces, in favor of a citizens' army..."

                hound_knight "An' I heard your mother laid with boars, yet I wouldn't believe it until I saw your face!"

                "The knights burst in laughter."

                initiate "A 'citizens' army'? It's ridiculous. No army could fare well on the battlefield without officers of noble blood to command it."

                knight "Of course. And what noble would want to lead an army of commoners? Men-at-arms like you may be good against weak savages like the Elves, but against a real army? Maybe as a first wave to soften 'em up, but then you'd need real knights!"

                guard "And what good is besting an army on the battlefield when the real enemy is within? The King has enough viper nests to snuff out in this very city."

                guard "Maybe cunning is called for now more than brute force..."

                knight "And you think the likes of you are more cunning than us knights?"

                guard "Well, I'm not the one who's blind to the obvious signs that the Crown is turning sour on you knights... It would help if your Commander had not gotten herself assassinated while abandoning her post."

                knight "Who said that? Lies!"

                hound_knight "More idle gossip. Just ignore it."

                knight "But it is what people are saying, isn't it? It makes us look incompetent..."

                initiate "Could they truly be aiming to replace knights?"

                hound_knight "Fear not, my friend. We are not so easily replaceable. I'd wager we'll outlive the King, yet."

                knight "Hush brother, do not voice such thoughts out loud, are you mad?"

                "The soldiers start talking in hushed tones, looking around suspiciously. You rush back to the buffet before they find your behavior suspicious."

            "Commander Uesugi Kenshin" if not _choice["kenshin"] and not NPC_kenshin.flags["dead"]:
                $ norollback()
                $ _choice["kenshin"] = True

                "You find Kenshin brooding in a corner, watching the assembly with distrust."

                show kenshin with dissolve

                "She lightens up slightly as she sees you, though."

                kenshin "[MC.name]? I didn't know you'd be here."

                you "Yes, Princess Kurohime asked me to be here."

                "She grasps the situation quickly."

                kenshin "So the Princess had a security meeting with you then... And she didn't send for me."

                "Shes doesn't make it sound like a reproach, but her disappointment is visible."

                kenshin "Well, I believe thanks are in order. You finally rid the city of these assassins..."

                if NPC_mizuki.flags["c3 path"] == "redeemed":
                    kenshin "...and for saving me, as well."

                    $ MC.rand_say("gd: Oh, don't mention it.", "ne: We're both glad it didn't come to that.", "ev: And don't you forget it!")

                    you "How are you holding up?"

                    kenshin "I have a lot on my mind, but... I'd be lying if I said my family's history didn't weigh heavily on me."

                    you "Is there anything I can do?"

                    kenshin "No, [MC.name], thank you. You have done plenty already. This I need to come to terms with by myself."

                    kenshin "And the Royal family is still in danger. This is what we need to focus on."

                you "What else can we do to keep the Princess safe?"

                kenshin "The masked murderer is still loose, so we need to catch him."

                you "The Princess says she has a plan. Know anything about it?"

                kenshin "A plan? I-I'm not sure..."

                you "I thought you'd know. It's strange that she didn't confide in you."

                kenshin "S-Strange, indeed..."

                "Kenshin seems preoccupied by your words, and promptly excuses herself."

            "Random courtiers" if not _choice["courtiers"]:
                $ norollback()
                $ _choice["courtiers"] = True

                "There are somewhat less courtiers around than last time, and you wonder if it is a sign that the Crown's influence is waning. Still, enough conversations are going on by the drinks' table that you manage to inconspicuously blend in."

                "Baron" "If my ears serve me right, then she will marry her first cousin from Zerga."

                "Countess" "Abomination! From Zerga? That foreign cesspit?"

                "Count" "I'm afraid you are misled. She will marry a widower from an old Zanite house."

                "Baron" "And who told you that?"

                "Count" "A source of impeccable reliability."

                "Baron" "And which is that?"

                "Count" "*sigh* Fine, if you must know: the maid of the stepbrother of the King's stable groom's own roommate told me."

                "Baron" "Ha! Drivel."

                "Countess" "A maid? What were you doing with a maid? *raised eyebrow*"

                "Viscount" "Gentlemen, if you please, I believe both your tales have it wrong."

                "Baron" "Oh? Have you the truth wrapped in ribbons, Viscount?"

                "Viscount" "The news I have will shock you, and make your wigs curl. Do you want to know more?"

                "Count" "We sure do, Lord Cliquebate."

                "Viscount" "The Princess will marry not for blood, but for treasure. The King's coffers are bare from the War."

                "Baron" "Naturally. No one thought she'd marry a pauper of an aristocrat. You think Lord Kosmo..."

                "Viscount" "No, here's the thing: she is not to wed an aristocrat. She's going to marry the richest guild master, the Head of the slave traders!"

                "Countess" "A commoner {i}and{/i} a foreigner? Blessed Arios, take pity on us!"

                "Count" "A commoner? Madness!"

                "Baron" "*scoff* No amount of coin is worth soiling your bloodline for all eternity..."

                "Viscount" "Don't pretend you haven't noticed: as Zan grows, the bourgeoisie is wielding more and more power by the day... Gold trumps blood at every turn. And the wealth of the richest commoner families in Zan has overpassed our own, while we fritter away fortunes on frivolities."

                "Viscount" "Take all this talk about the League..."

                "Countess" "The league? Which league?"

                "Count" "Ha, the so-called 'League of Freethinkers'! Ignore it, my dear, it's a fable for the weak-willed..."

                "Countess" "Freethinkers? Are they a cult?"

                "Viscount" "No, my Lady. They're philosophers, inventors and entrepreneurs, noble-born and commoners alike, pooling their resources to advance human knowledge. They are behind some of the most groundbreaking discoveries in the past decade..."

                "Baron" "Rubbish. Should we be shaking in our boots because of a bunch of scholars? Children who believe in 'Science'?"

                "Countess" "What's this 'science' you speak of? Is it like... magic?"

                "Count" "No, my dear, it's nothing as grounded as magic. Science is the belief that nature follows certain immutable laws that can be discovered and used by anyone - without any special talent whatsoever! *laugh*"

                "Countess" "Heavens! These vulgar superstitions get worse by the day. Next, they'll claim the sun rises in the East not because Arios wills it!"

                "Viscount" "Call them what you will, but they're rolling in gold. Most influential commoners in the city are members, or so I'm told. And not an insignificant number of young nobles, too."

                "Baron" "And this slavemaster of yours is among them?"

                "Viscount" "Hard to say. I heard they have taken a dim view of slavery, among other institutions they call 'outmoded'."

                "Countess" "They even oppose slavery? Good Arios! What is the world coming to!"

                "Count" "It's as puzzling to you as it is to me, dear."

                "Viscount" "They believe that 'all men and women ought to be free'. Their words, not mine."

                "Baron" "Women too? May the Sun God scorch my arse if..."

                "Countess" "Language, Baron!"

                "Count" "Viscount, you spin a good tale, but I don't believe for a moment King Pharo will choose a commoner, and turn all the nobility against him."

                "Baron" "He'd best not, if He knows what's good for Him..."

                "Count" "You know where I stand on that..."

                "Countess" "Enough! I have heard enough nonsense for the day. I'm going home. *indignant*"

                "Countess" "And {b}you{/b} had best explain why you consort with a groom's roommate's stepbrother's maid!"

                "Moving away from the table, you leave the noble couple to their bickering."


            "The Palace Staff" if not _choice["staff"]:
                $ norollback()
                $ _choice["staff"] = True

                "Most of the gentry is busy stuffing their faces, so some of the staffers are taking a break, loitering by the kitchen stairs and chewing something that smells suspiciously like spice."

                "Housemaid" "I tells ya, He's not well."

                "Squire" "Bah, woman! It's probably just another bout of gout. He's had more comebacks than a minstrel."

                "Manservant" "But it's true, innit? No one but the Princess is allowed to talk to Him. I can't even go in there to change the chamberpot without a guard, and he's always in bed, just out of sight."

                "Manservant" "If I didn't hear his wheezy breathing, I'd think the bugger was already dead!"

                "Housemaid" "Arios *sun sign*! Ye can't speak ill of His Majesty..."

                "Manservant" "Oh, come off it. I don't think he'll make it even to the Princess's birthday. He's going to croak, and ye know it."

                "Squire" "Aren't we all? He survived the long march across the Arik mountains as he was wounded and hunted in his rebel days. Even as King, he's been ailing for years. And the old boy's still kicking."

                "Housemaid" "Aye, but He looks like a ghost of His former self. What's happened to Him?"

                "Squire" "Too many excesses I hear. Food, wine, spices... And far too many women."

                "Manservant" "Womin, eh? Does the old prick score a lot?"

                "Housemaid" "Hush, Arios, you're going to have us flogged!"

                "Manservant" "Maybe he got syphilis. A mate of mine got it after shagging some whore in Borgo. Ain't pretty."

                "Squire" "I hear He's still got a lover or three tucked away. The Princess doesn't like it, but she turns a blind eye."

                "Squire" "Though if I were his age, I'd take it slow... He did look exhausted recently."

                "Housemaid" "He did, and now, no one has seen Him in like... Two weeks?"

                "Squire" "He'll get through. Mark my words, the old warhorse isn't missing his daughter's birthday, or wedding."

                "Manservant" "We'll see. By the way, d'ye still know that hedge witch what brews a cure for syphilis? Asking for a friend..."

                "As whatever it is they're perusing takes hold, their voices blur into incoherence. You lose interest, and head to the kitchen for more stew."

    scene black with fade

    stop music fadeout 3.0

    "The luncheon is finally winding down, and the princess has already left. You find your way back to the carriage with minimal help from the staff. You are becoming a regular."

    return

label c3_homura_invitation(): # Happens the morning after the palace visit

    # Homura love thresholds: >10 = love, 5-10 = friends, 0-5 = neutral, <0 = dislike - Dialogue options: +13 to -13, H options +4 (first), +3 (repeat all)

    scene black with fade

    play sound s_chimes

    show expression bg_bro at top

    show homura with dissolve

    "Homura came to visit you today."

    if NPC_homura.love > 10:

        "She gives you a long, shameless kiss as soon as she sees you, hugging you tighter than usual."

        homura blush "It hasn't been that long, but... I've missed you, [MC.name]."

    elif NPC_homura.love > 5:

        "She hugs you shyly, giving you a smile."

        homura "Hi, [MC.name]. It's good to see you."

    else:

        "She stands there awkwardly, not sure if she should be seen with you in public."

        homura "Hello, [MC.name]. Can I, uh, some in?"

    "You invite Homura to step in, ordering Sill to fetch her a nice cup of tea."

    homura "Thank you, your... slave makes a nice cup of tea."

    homura "Where did you find that girl? I must say, she seems like a proper lady."

    "In the corner of your eye, you catch Sill lingering on the treshhold, but answer nonetheless."

    menu:
        _("She's had a good education"):
            you "Yes, Sill is from a family of means. I bought her when her parents were hit by misfortune."

            you "It's a shame it had to come to that, but I try to give her a good home."

            $ NPC_sill.love += 1
            $ NPC_homura.love += 1

            "Sill finally leaves the room, but you detect a spring in her step."

            homura "It's nice of you. I don't think all slave owners are this generous."

        "She's just a street girl":

            you "No, she's just your regular whore. She looks proper, but believe me, under the sheets..."

            $ NPC_sill.love -= 1

            homura blush "I-I didn't ask for that! Please, don't say anymore!"

            "Sill finally leaves the room, her face livid."

        "Oh, I don't really keep track":

            you "Oh, she may have been, I don't know. It's not good to dwell on the past in this life."

            "Sill leaves the room, sighing faintly."

            $ NPC_homura.love -= 1

            homura sad "Wait, don't you care about the women you brought in? They're people too, you know."

            you "I do, I try, but they are many, you know... It's hard to keep track."


    homura normal "Anyway, are you and her... You know..."

    menu:
        _("Physical?"):            you "Are we having sex, you mean?"


        "Special friends?":
            you "'Special friends', like you and me?"

        "Dating?":
            you "Are you asking if we're dating?"

    homura blush "Y-Yes..."

    menu:
        _("Yes"):            you "We are."

            homura "Oh... I should have expected it, of course."

            you "But it doesn't change how I feel about you."

            if NPC_homura.love > 10:

                $ NPC_homura.love -= 1

                homura "I guess..."

                "Even though she puts on a straight face, she still sounds disappointed by your answer."
            else:
                homura "I see."

        "No":
            you "Oh no, we're not."

            "You hear Sill audibly clear her throat from way back inside the kitchen."

            homura "Really?"

            "She gives you a skeptical look."

            if NPC_homura.love > 10:

                homura "Okay... I guess I'm relieved to hear that. *blush*"

            else:
                homura sad "Oh, come on... Don't take me for a fool."

                "She doesn't believe you."

                $ NPC_homura.love -= 1

    homura normal "Anyway, will you come next Saturday?"

    you "Next Saturday? What? Where?"

    homura "You know, of course. To Kurohime's birthday party."

    you "What, it's her birthday already? I didn't know."

    homura "We're throwing her a surprise party, all of her close friends will be there!"

    homura "Most people don't know you, so maybe that's why you weren't invited. But you can come anyway, just say you're with me."

    you "I don't know... Would it be proper for someone like me to attend her party?"

    if MC.noble:

        homura "Of course it would. You're nobility too, after all. And you'll be with me, Her Majesty's best friend!"

    else:

        homura "Normally not, commoners are not typically invited to such events, but I'll be vouching for you. And I'm sure Kurohime would love to have you."

    homura "Oh, come on, it will be fun!"

    you "Well, okay... Do we meet at the Palace?"

    homura "No, it's a surprise party, I told you. We're invited to a grand mansion in the upper city. Don't worry, it will be truly fit for a Queen."

    homura "And who knows, maybe we'll finally learn who the princess is going to marry! You have to come!"

    you "Who she's going to marry? Is it already decided?"

    homura "Hahaha, you're curious aren't you? Meet me at the mansion on Saturday. I'll send a carriage for you."

    you "Okay..."

    $ calendar.set_alarm(calendar.find_next("Saturday"), StoryEvent(label="c3_confrontation", type = "night"))
    $ game.set_task("Attend Princess Kurohime's birthday party on Saturday night.", "story")

    scene black with fade

    return


# Final Confrontation #

label c3_confrontation(): # Happens on the next Saturday night after Homura's visit

    if blue_ribbon in MC.items:
        $ MC.items.remove(blue_ribbon)
    $ plaza.action = False


    scene black with fade
    show bg carriage at top with dissolve

    "It's time for the princess's birthday party. As promised, Homura has sent for you."

    you "Strange... I feel like I have seen this carriage before."

    you "Oh, that's right! It's the carriage that picked me up on the first day I was summoned to the Palace."

    you "The day this strange investigation began..."

    play music m_palace fadein 3.0

    scene black with fade
    show bg exotic_emporium at top with dissolve

    "As the carriage drives uphill towards the noble quarters, you reflect on all that has happened since."

    you "I had to hunt not one, but three dangerous Kunoichi... It's a miracle I made it out alive."

    you "In spite of all of this, I still feel like I'm no closer to catching the real killer. It's infuriating."

    you "It's as if the masked murderer is leading me on a wild goose chase..."

    show bg pilgrim_road at top with dissolve

    "The carriage turns into Pilgrim's Road."

    you "And then, there's Homura..."

    "You think about the noble girl and the role she's played in your life recently."

    menu:
        "How do you really feel about her?"

        _("I may be falling for her"):
            you "I think I'm quite smitten with the girl."

            "You are surprised to hear yourself say this out loud."

            you "She's a strong woman, but she has a vulnerable side. She really opened herself to me."

            you "I should tread around her feelings carefully. She deserves to be treated well."

            $ NPC_homura.flags["MC opinion"] = "love"

        "She's more like a friend":

            you "It's nice to fuck her and everything, but I can't really get bogged down with a relationship at the moment."

            you "I simply have too much on my plate. But I guess we can remain 'friends'. I can use the relief."

            $ NPC_homura.flags["MC opinion"] = "like"

        "I don't trust her":

            you "There's something off about her, I'm sure."

            you "I'm not letting my guard down until I know what her deal is."

            $ NPC_homura.flags["MC opinion"] = "doubt"

        "I don't care for her at all":

            you "I need her to get close to the Royal family, but I don't care for her at all."

            you "I'll fuck her for as long as I need her, and then I'll just ditch the bitch."

            $ NPC_homura.flags["MC opinion"] = "hate"

    "The sun is fading behind the hills. You recognize this area. Homura told you the mansion where guests are waiting for the princess's birthday party isn't far."

    stop music fadeout 3.0
    scene black with fade
    show bg mansion night at top with dissolve

    "Your reverie stops when the carriage enters the courtyard of a large mansion, as night engulfs the Inner City."

    you "Wow. This place sure is gigantic. Whoever lives here must be disgustingly wealthy."

    "The dark and empty courtyard seems somewhat unwelcoming. As you get off, you fail to notice any sign of life coming from inside the large and overbearing building."

    you "(It sure looks quiet for a birthday party...)"

    "Homura's Voice" "Come in, [MC.name]! You're just in time."


    "Homura's voice beckons. You climb the stairs to the mansion, suddenly aware that the coach driver is close behind you."

    scene black with fade
    play music m_mafia fadein 3.0

    "You feel a strange chill down your spine as you push the door to the mansion open."

    $ game.set_task("Wait for news from the Palace.", "story")

    ## PHASE 0 - The Setup ##

    show bg mansion inside at top with dissolve
    show homura ninja with dissolve

    homura ninja "Welcome, [MC.name]. We've been waiting for you for the final act."

    "Homura stands in the entrance, but her clothing is completely different from what she usually wears."

    "And the blade at her side is definitely new..."

    you "Homura... What's with the disguise? Is this a costume party, and you somehow forgot to tell me? *nervous*"

    "The driver is standing right behind you. You realize that you haven't seen his face, covered as it was by a long scarf."

    play sound s_dress

    "He drops it, and you take your first good look at him."

    scene black with fade
    show bg mask driver1 at top with dissolve

    "Coach driver" "..."

    play sound s_vibro
    show bg mask driver2 at top
    pause 0.1
    show bg mask driver1 at top
    pause 0.1
    show bg mask driver2 at top
    pause 0.2
    show bg mask driver1 at top
    pause 0.1
    show bg mask driver2 at top with dissolve

    you "(Oh shit...)"

    scene black

    show bg mansion inside at top
    show homura ninja
    with fade

    homura ninja "As I was saying... We've been waiting for you."

    show homura ninja at totheright with move
    show mask at left with dissolve

    if NPC_homura.love > 10:
        homura "[MC.name], I'm sorry, I truly am. I wish I did not have to trick you. I didn't think it would go this far..."

        "She loses her composure for a moment, looking down."

    elif NPC_homura.love > 5:
        homura "I know you're surprised to see me like this. But I had little choice. This is all for the greater good."

    elif NPC_homura.love > 0:
        homura "Oh, dear, the costume party {i}is{/i} over. The disguise was the {i}other{/i} one... It's lucky you fell for it."

    else:
        homura "Ha! You fell for my 'frail noble girl' persona hook, line and sinker, didn't you? How dumb."

        homura "I couldn't wait to get this over with! To think I had to let you get inside me, ew!"

    you "What the heck, Homura?"

    homura "The truth is, I'm no more a noble woman than you are an Arios priest."

    $ unlock_achievement("homura secret")

    "The masked man scoffs."

    if NPC_homura.flags["MC opinion"] == "love":
        mask "What a cruel joke, darling... I overheard the man daydreaming about you in the carriage, unaware he was being manipulated by my loyal girlfriend... *smirk*"
        $ NPC_homura.love += 1

    elif NPC_homura.flags["MC opinion"] == "like":
        mask "He just thought of you as 'friend with benefits' anyway, Homura. I heard him say as much in the carriage. And you already have a boyfriend anyway... *smile*"
        $ NPC_homura.love -= 1

    elif NPC_homura.flags["MC opinion"] == "doubt":
        mask "Don't take the man for a fool, darling. He was onto you. I heard him voice his doubts in the carriage."

    else:
        mask "He never cared for you at all, anyway. I believe his exact words were {i}'I'll fuck her for as long as I need her, and then I'll just ditch the bitch.'{/i}. How dare he talk like that about my lovely girlfriend... I'm hurt. *amused*"
        $ NPC_homura.love -= 2

    you "Homura is your girlfriend?"

    if NPC_homura.love > 10:
        homura "I-It... It's complicated."

    if NPC_homura.love > 5:
        homura "Well... It is the truth, [MC.name]."

    elif NPC_homura.love > 0:
        homura "Of course. But didn't I play the part of the sweet young thing well?"

    else:
        homura "I am! Did you really believe I had fallen for you? A filthy brothel owner? Ha! You disgust me."

    "You are interrupted by muffled sounds coming from the back of the room."

    play sound s_gag
    show bg mansion inside2 with dissolve

    "Muffled Voice" "HNGGH!!! HNGGGGH!!!" with vpunch

    "For the first time, you notice that there are people huddled together behind Homura, bound with ropes and gagged."

    "Most of them look like house servants. But you can tell the one attempting to speak is the master."
    
    "You immediately recognize him."

    play sound s_gag
    kosmo "HNNNGGGH!" with vpunch

    you "Kosmo?"

    homura "Right, I forgot. You already know the master of the House."

    "Kosmo's pleading eyes dance from you to Homura, avoiding the masked man altogether."

    you "Wait- Is this Kosmo's house?"

    you "What is the meaning of this?" with vpunch

    homura "As you must have guessed, [MC.name], I never was a Court lady."

    homura "Lord Henso lost his daughter to illness months ago. It was a perfect opportunity for me to assume her identity..."

    homura "...and convince you that I was friends with the Princess. From there, I only had to seduce you."

    "You give a puzzled look to the masked man."

    you "You! You mentioned that Homura is your lover. Why put her into someone else's arms?"

    mask "Ha! Men such as yourself can only think with their nether regions. I am made of sterner stuff."

    mask "I am up against the most formidable foe. I need to use every tool at my disposal to succeed."
    
    mask "Homura is... One such a tool."

    "Homura flinches almost imperceptibly."

    you "Why me? What do you want from me?" with vpunch

    mask "Why you, indeed?"
    
    mask "For reasons that elude me, you happen to have quite a unique connection with my sister. The weakest link in her armor..."

    you "Your sister?"
    
    you "Look man, I'm sorry if I shagged your sister, I don't know the family of everyone I..."

    stop music fadeout 3.0
    play sound s_surprise

    kuro "WHAT'S THE MEANING OF THIS?" with vpunch

    hide mask
    hide homura
    show bg mansion inside
    show kuro
    with pushleft

    "You recognize the voice of the woman who just entered. It's none other than Princess Kurohime."

    you "Princess!"

    kuro "I received your message, [MC.name]. What's this life and death matter you meant to discuss?"

    you "A life and death matter? I-I didn't write to you, Your Highness."

    kuro "You didn't? But your seal..."

    hide kuro
    show bg mansion inside2
    show mask at left
    show homura ninja at totheright
    with pushright

    homura "Teehee... I took the liberty of borrowing his seal, and of writing that letter."

    you "You tricked us both!" with vpunch

    play sound s_maniacal_laugh

    mask "The trap is sprung! Happy birthday, dear sister. *sinister grin*"

    play music m_gizel fadein 3.0

    hide mask
    hide homura
    show bg mansion inside
    show kuro
    with pushleft

    "Kurohime looks confused, looking at the masked man and Homura in turns."

    if not NPC_kenshin.flags["dead"]:
        show kuro at left with move
        show kenshin at right with dissolve

        kenshin "Stand back, you filth! One step towards the Princess and I'll have your head!"

        "Kenshin's warning is including you as well."

        kuro "Uesugi... So you followed me here."

        homura "Hey! No fair. The letter requested that you come alone."

        kenshin "After what happened, did you really think I'd let Her Majesty venture out by herself?"
        
        mask "Alas, that will change nothing."

        "Kenshin's eyes narrow, sizing up her adversary."

        kenshin "We'll see."

    else:
        mask "You came here alone, defenseless. Do you trust this commoner that much?"

        kuro "I owe him."

        mask "*scoff*"

    kuro "Who are you people? I have never met you before. What business have you with the Crown?"

    hide kuro
    hide kenshin
    show bg mansion inside2
    show mask at left
    show homura ninja at totheright
    with pushright

    homura "Nice to finally meet you, Princess. You truly look nothing like your brother."

    hide mask
    hide homura
    show bg mansion inside
    if not NPC_kenshin.flags["dead"]:
        show kuro at left
        show kenshin at right
    else:
        show kuro
    with pushleft

    kuro "Enough! Who are you, and what is this masquerade?" with vpunch

    if not NPC_kenshin.flags["dead"]:
        kenshin "Identify yourself, citizens!"

    "The masked man straightens up and takes on an arrogant air."

    hide kuro
    hide kenshin
    show bg mansion inside2
    show mask at left
    show homura ninja at right
    with pushright

    $ mask_name = "Shirohito"

    mask "Heed my words. My full name is Prince Shirohito, Royal Heir of the Pharo dynasty."

    mask "My friends call me Shiro... But to you, I shall remain 'Your Highness'."

    kuro "Madness!!! Lies!!!" with vpunch

    if not NPC_kenshin.flags["dead"]:
        kenshin "..."

    mask "Could it be you don't know about me, sister? It pains me to hear that, on the day of our mutual birthday..."

    "Kurohime blemishes."

    you "I don't understand..."

    kuro "Me neither, but I demand answers, or I'll summon the guards!" with vpunch

    "The man gives a faint, cold smile."

    mask "Very well. You shall have your answers."

    $ answered = defaultdict(bool)

label c3_mask_questions(): # Follows previous label

    menu:
        "What will you ask the masked man?"

        "Who are you?" if not answered["who"]:

            $ answered["who"] = True

            mask "I am Shirohito, son of King Pharo the First, and sole rightful heir to his Kingdom."

            kuro "It couldn't be... The other child died at birth..."

            mask "This is what our monster of a father would have wanted, wouldn't he? *spit*"

            mask "But I am alive, and ready at last to claim my birthright!"

            mask "And you... *pointing finger* *You're no better than them..."

            menu:
                _("Defend the princess"):                    $ NPC_kuro.love += 1
                    $ NPC_mask.love -= 1

                    you "Mind yourself around the Princess, murderer! Or I will have your filthy tongue!"

                    mask "Ha! You think that this is within your power? *hiss*"

                    mask "We shall see about that shortly."

                "Say nothing":
                    $ NPC_kuro.love -= 1
                    $ NPC_mask.love += 1
                    you "..."

            mask "I was born first, the natural heir to the throne. But our father wanted a weak woman as an heir, for what dark purpose I do not know..."

            hide mask
            hide homura
            show bg mansion inside
            if not NPC_kenshin.flags["dead"]:
                show kuro at left
                show kenshin at right
            else:
                show kuro
                with pushleft

            kuro "Is this what you were told? Preposterous!"

            you "So, wait... The masked freak is your brother?"

            "The princess ponders the situation calmly."

            kuro "He claims to be my {i}twin{/i} brother, no less."

            kuro "I have heard of such rumors, but..."

            hide kuro
            hide kenshin
            show bg mansion inside2
            show mask at left
            show homura ninja at right
            with pushright

            mask "Then ask our cursed father! Ask him about the assassins he sent for me!"

            "The man looms larger than life now, his anger flaring. You could almost believe he possesses the wrath of a King."

            mask "I was but an infant when the first attack came... The old Knight Commander saved me."

            mask "He was sent to hide me into the forest for my safety, on my mother's orders."

            scene black with fade
            show bg c3_flashback0 at top with flashbackin

            mask "There were many attacks since, and we had to move time and time again. I have know the fear of demons and assassins since before I could talk."

            mask "Eventually, they took my eyes... Worse, they took him, my guardian, the one who taught me everything I know... The father I wished I had..."

            mask "Master Mitsuhide."

            if not NPC_kenshin.flags["dead"]:
                kenshin "WHAT???" with vpunch

            you "Kenshin's father? Kenshin's father protected you?" with vpunch

            if story_flags["c3 clue boy"]:
                you "The boy in the forest that Mizuki told us about! It was you!"

                mask "I assume you refer to the warrior lady who helped me defeat the attackers. I was fortunate to survive that day, even at the cost of my eyes."

                you "And Kenshin's father protected you to the end..."

            if not NPC_kenshin.flags["dead"]:

                kenshin "Do you speak the truth? You knew my father?"

                mask "Knew him? He raised me by himself, surviving in the deep forest."

                kenshin "He... He abandoned his family to raise you?"

                mask "He did his duty. He had to protect the rightful heir. Such was his vow to my mother."

                kenshin "..."

            else:
                mask "He did, until the demons gutted him."

            mask "But the loss of my eyes and mentor did not soothe the beasts. There were more attacks, even after I escaped."

            scene black
            show bg mansion inside2
            show mask at left
            show homura ninja at right
            with flashbackout

            jump c3_mask_questions

        "What happened to your eyes?" if answered["who"] and not answered["eyes"]:
            $ answered["eyes"] = True

            mask "When I was just a boy of eight, the attack came."

            mask "Demons surrounded the hut where we slept. They would have killed me if not for Master Mitsuhide's heroic defense, and the intervention of a mysterious lady warrior."

            mask "Thanks to your investigation and a little guess work, I now know that it was the Kunoichi you know as Mizuki Ike."

            mask "While the attackers stopped short of ending my life, a demon took my eyes out."

            mask "I remember the pain all too well. And for a long time, its fiendish claws were the last thing I saw..."

            mask "But Master Mitsuhide had taught me to fight since I was old enough to walk."
            
            mask "To survive in the forest, I had to learn to live without sight. I became a stronger warrior for it."

            mask "I could hunt with just sound and smell... And now that I can see again, I have reached the peak of my abilities."

            you "Modest, aren't you?"

            mask "No, accurate. More demons came for me over the years. And even without the use of my eyes, none of the assassins have come close to succeeding."

            if story_flags["c3 clue mask"]:
                you "And now you recovered your sight, thanks to the artifact you stole from the Magic University."

                mask "I see you've done your homework."

            else:
                you "But you've recovered from such an injury? What sorcery is this?"

                mask "The regular kind of sorcery."

            mask "My darling Homura is an expert thief. She stole the Oculus mask from the Magic University, and helped me recover my eyesight, which proved invaluable to navigate the unfamiliar environment of this city."

            mask "Now I'm stronger than I've ever been... My other senses have been honed by fifteen years of survival in the wild. And the mask grants me powers beyond what simple mortal eyes can perceive."

            "You sense that the Masked Man's boast is more than just bluster. The man and his mask are truly dangerous."

            jump c3_mask_questions


        "What's my role in this?" if not answered["MC"]:
            $ answered["MC"] = True

            mask "For the longest time, we were looking for an 'in' into the Palace. After all, it is the most well-guarded place in the city, and I haven't a ninja's knack for... Burglary."

            homura "But one day, we got lucky: a palace carriage was sent to the lower city, undefended, and we got a hold of it."

            mask "I was able to... Get the driver to talk. Imagine my surprise, when I heard that the Princess had been sending for a known whoremonger."

            if NPC_kuro.flags["occupation"] == "lie":
                $ NPC_kuro.love -= 3
                kuro "Whoremonger? *raise eyebrow*"

                mask "It seems you little protege hasn't told you everything... *smirk*"

            elif NPC_kuro.flags["occupation"] == "half-lie":
                $ NPC_kuro.love -= 1
                kuro "I didn't know of his occupation, besides... *sigh* It is not your place to judge."

                mask "As the rightful ruler, I can do as I damn well please!"

            else:
                kuro "So what? Do you pride yourself on hanging around with murderers? When matters of State need handling, you have to use every opportunity at your disposal."

                mask "On that we can agree."

            homura "We decided to seize the opportunity. I assumed the role of young Lady Henso, which I had been rehearsing for such an occasion..."

            mask "... and I took on the role of the driver."

            mask "We were able to ride into the castle, using [MC.name]'s own letter of conduct."

            homura "You unwittingly brought the proverbial fox inside the chicken coop."

            mask "Thanks to you, I was able to recon the place, and bring my sister a first warning... The judge's head."

            you "So that's how you got in at first..."
            
            you "But what happened to the real driver?"

            mask "Oh, that poor sod?"

            mask "What do you think happened to him? I slit his throat and threw his body in the sewers."

            menu:
                extend ""

                "You monster":
                    $ MC.good += 2

                    you "You killed an unarmed man in cold blood? How could you!"

                    mask "Obviously I couldn't leave a witness behind."

                    mask "It was distasteful, but no King ever fulfilled their destiny without spilling some commoner blood. Besides, no servant of this Court is innocent, anyway."

                "Cold":
                    $ MC.neutral += 2
                    you "Cold. You couldn't leave him alive if you wanted to carry on with your plan, I suppose."

                    mask "Of course not. But don't worry, I made it quick."

                "Nice touch":
                    $ MC.evil += 2

                    you "Sure. I didn't picture you for someone who would tolerate loose ends. You're not foolish."

                    mask "You've noticed."

            if NPC_homura.love > 5:
                "Homura stays silent and looks down, obviously uneasy."

            elif NPC_homura.love > 0:
                "Homura heaves a heavy sigh."

            else:
                homura "People die everyday. This sacrifice was but a small one to restore Shiro's glory."

                mask "That's right."

            kuro "You evil, despicable man! *snort*" with vpunch

            mask "Peh, women have such weak hearts. No wonder they are unfit to rule."

            jump c3_mask_questions


        "What's your connection to Homura?" if not answered["homura"]:
            $ answered["homura"] = True

            mask "Homura? Well, she saved me, in her own way... Perhaps my destiny is to be rescued by Kunoichi."

            homura "It's a long story..."

            menu:
                extend ""

                "Try me":

                    you "Well, I didn't have other plans for the evening."

                    "Homura shrugs and proceeds to tell her side of the story."

                    homura "As you might have guessed, I am a Kunoichi. I hail from the Temple of Fire, on the brink of an active volcano near Hokoma's border."

                    homura "After completing my training, I worked all around Xeros, getting to know all of the big cities, including Zan."

                    homura "But even when business takes me to a large urban center, I'm always more at ease in the wilderness. Thus I started hiding in the forest near Zan."

                    homura "I thought it safer, and more peaceful than the cutthroat streets. Until one day..."

                    scene black with fade
                    show bg forest at sepia with flashbackin

                    play sound s_clang

                    pause 0.3

                    play sound2 s_sheathe

                    pause 0.1

                    play sound s_wscream

                    homura sepia "W-What's this? A fight? In the middle of the forest?"

                    play sound s_clang
                    show bg c3_flashback1 at top with fade

                    homura ninja "That's when I saw him. He was just a boy my age, fighting with his eyes shut... But Arios, did he fight like a lion."

                    play sound s_clang

                    pause 0.3

                    play sound2 s_clang

                    pause 0.4

                    play sound3 s_clang

                    homura "He was facing four ninjas all by himself, and they couldn't lay a hand on him. But he was getting tired..."

                    play sound s_clang

                    pause 0.2

                    play sound2 s_sheathe

                    pause 0.1

                    play sound3 s_wscream

                    show bg c3_flashback2 at top with fade

                    homura "He took out three of them, but the last one had him cornered. I knew he was defeated, but the attacker hesitated for a fleeting moment. I didn't."

                    show bg c3_flashback3 at top with dissolve
                    play sound s_clang

                    homura sepia "Stop!"

                    homura ninja "I knew better than to interfere in another ninja temple's mission, but I couldn't watch that young man get killed in front of me."
                    
                    homura "I leapt in the middle of the fight, without thinking."

                    play sound2 s_sheathe

                    homura "The last ninja was dead before he landed his attack."

                    homura "He underestimated me... A mistake many have made... *wink*"

                    you "Who were these attackers?"

                    homura "I don't know. They were from a ninja temple I hadn't heard of... Until I heard about your new friend, Haruka."

                    homura "The Noroi..."

                    if story_flags["c3 clue demons"]:

                        you "The Noroi! The demon worshippers?"

                        homura "Yes. As you can see, the rot goes a long way."

                        mask "That is why the root of the corruption must be destroyed..."

                        you "Anyway, Homura, finish your story."

                    else:
                        you "The Noroi? Did Haruka mention them?"

                    homura "The boy was hurt. I tried to tend to his wounds on the spot."

                    show bg c3_flashback4 at top with dissolve

                    mask "All I remember is Homura's face in the sunlight. And then I slipt into unconsciousness."

                    homura sepia "It's okay... You're going to be okay..."

                    show bg c3_flashback5 at top with fade

                    homura ninja "Shiro had lost too much blood, and he passed out. I dragged him back to my hideout."

                    show bg c3_flashback6 at top with fade

                    homura "I don't know what took over me. Everything in my training said I should have left him to die in the forest. But after I got involved, I felt I had to see it through."

                    mask "Fate guided your hand, Homura, you must have felt its pull. I couldn't die in the forest. I must accomplish my destiny."

                    homura "When he got back to his senses, the most surprising thing happened. We... We made love."

                    menu:
                        _("Picture it"):                            call c3_homura_with_shiro() from _call_c3_homura_with_shiro

                        "Do not picture it":
                            you "Ew, okay, I don't want to know the details."

                    show bg c3_flashback7 at top with fade
                    homura "Eventually, I nursed him back to health. And over time, we became lovers..."

                    homura "After that, the die was cast. I didn't leave his side, even as more attackers kept coming."

                    show bg c3_flashback8 at top with fade

                    homura "He grew stronger."

                    show bg c3_flashback9 at top with dissolve

                    homura "We grew closer."

                    show bg c3_flashback10 at top with fade

                    homura "And five years later, we were ready to go back to Zan. Where it all started."

                "Skip it":
                    you "On second thought, I don't need to know."

                    homura "The important part is that when we got back to Zan, we had unfinished business."

            show bg mask rooftop at sepia with dissolve

            homura "We were nothing but forgotten paupers. I hadn't taken a job in years, and Shiro had never even been to a city."

            show bg mask rooftop at top_color with dissolve

            mask "But we persevered, and once I got my eyes back, I started my plan to take revenge."

            mask "I started to strip the Royal Family of its corrupt protectors... Picking them off one by one, like lost deer in the forest..."

            scene black
            show bg mansion inside2
            show mask at left
            show homura ninja at totheright
            with flashbackout

            mask "The forgotten prince and his warrior lover, carrying his righteous vengeance. Poetic, isn't it?"

            you "Very. You left out the part where Homura ended up in my bed..."

            mask "Ha! It's just an illusion that we had to maintain to trick you."

            mask "Homura got close to you, and we used you to try and get information on the Crown and their efforts to stop us."

            if NPC_homura.flags["divulged assignment"]:
                mask "I must say, a princess should pick better confidents... It's amazing how much one can learn from pillow talk."
                "The Princess frowns when she hears that you have been spilling the beans on your assignment."

                $ NPC_kuro.love -= 2

            else:
                mask "I must say I'm impressed, though. You held the Princess's secret about your assignment to the end."
                "The Princess nods approvingly."

                $ NPC_kuro.love += 2

            if NPC_homura.love > 10:
                homura "Listen, [MC.name], it wasn't all about..."

                mask "Oh, don't get sentimental, woman! You did your duty, it's all that counts."

                homura "I-I just..."

                "She interrupts herself, unable to look you in the eyes."

            elif NPC_homura.love > 5:
                homura "It was just a bit of fun and harmless spying, wasn't it, [MC.name]? *bat eyes*"

                you "Harmless??? That remains to be seen."

            elif NPC_homura.love > 0:
                homura "Let's not dwell on the past."

            else:
                homura "Well, you fell for our plan. That's what matters!"

            mask "But arguably, the biggest role you've played in this whole affair is tonight, delivering my sister to me on a silver platter."

            mask "History will not remember it... But I will."

            you "..."

            jump c3_mask_questions


        "What's your connection to the other Kunoichi?" if answered["homura"] and not answered["kunoichi"]:

            $ answered["kunoichi"] = True

            homura "They are not with us. I knew they were in town, so we just took advantage of them as a distraction..."
            
            homura "Gave you guys a little nudge, here and there, so that you would fight it out while we were pulling the strings."

            mask "Oh, I enjoyed watching this little cat and mouse game from afar. I even learnt some things that were surprisingly useful."

            if NPC_narika.flags["c3 path"] == "captured" or NPC_mizuki.flags["c3 path"] == "captured" or NPC_haruka.flags["c3 path"] == "captured":
                mask "I saw how you captured one of them and broke her into your service, too..."

                mask "I must say, evil as it was, I couldn't help but be impressed."

            elif NPC_narika.flags["c3 path"] == "ally" or NPC_mizuki.flags["c3 path"] == "revenge" or NPC_haruka.flags["c3 path"] == "ally":
                mask "I was fully expecting you to get killed sooner than later, but fortunately for us, you proved resilient."

                mask "You even made one of them an ally. I have since decided not to underestimate you."

            else:
                homura "Still, I must say I was disappointed in you for turning them in for a reward."

                mask "Wass that the best you could do, [MC.name]? I guess we'll never know."

            jump c3_mask_questions


        "Why are you after the Royal Family and their allies?" if answered["who"] and not answered["royals"]:

            $ answered["royals"] = True

            mask "I am the rightful ruler of this kingdom! Not my father, this pathetic husk of a man, devoured alive by his remorse and broken ambitions. And certainly not this weak-willed, poison-tongued sister of mine."

            "He nods scornfully at the princess."

            kuro "I will have your hide for this, schemer! Do not insult your liege, my father King Pharo!"

            mask "{i}Our{/i} father is unworthy of any such title! He consorted with demons, and conspired to kill his own son!"

            kuro "Lies! Treason!!! *furious*" with vpunch

            "The Princess seems about to break down under stress, while the masked avenger's red eyes gleam through his mask with anger."

            mask "All my life, I've been hunted by my father, for the mere crime of being born. I was maimed as a boy, suffered countless wounds and close-encounters with death. I never had a moment's rest!"

            mask "Do you know what it's like to live every moment, knowing that demons and killers are out to get you?"

            mask "This is what I wanted you to experience... What I wanted you {i}all{/i} to experience... Before I snuff it all out in blood!"

            kuro "You are MAD!!! Your wretched life has turned you into a broken and paranoid excuse of a man!" with vpunch

            mask "Paranoid? Believe me sister, just because you're paranoid..."

            you "...don't mean they're not after you, right?"

            "He gives you a chilling stare."

            you "Oh well, whatever. Never mind."

            you "Wait, what's your end game here? You can't just kill everyone and claim the throne for yourself? This is not how any of this works!"

            mask "Hmph, it's easier than you think. It's how my father did it."
            
            mask "In the short time I have been here, I have made the right kind of friends... Let's just say I'll have support."

            mask "All I had to do is to agree to certain conditions that, well, would not cost {i}me{/i} anything..."

            mask "...but would come as a nasty surprise to the parasites at Court."

            kuro "W-Who are your allies? What do you intend to do?"

            mask "Each in its own time, sister. One thing still stands in my way..."

            "He looks harder at Princess Kurohime, and his fiery red eyes take on a malevolent sheen."

            jump c3_mask_questions


        "Why did you capture Kosmo?" if answered["who"] and not answered["kosmo"]:
            $ answered["kosmo"] = True

            mask "Who?"

            play sound s_gag

            kosmo "HNNNGGGGHHHH! HNNGH, HNNNNGGGH!!!" with vpunch

            you "Kosmo. The sad creep who owns this mansion, and who lies crumpled on the floor as we speak."

            menu:
                _("Ask for his release"):                    $ MC.good += 1

                    you "What are you doing, Homura? Let Kosmo and his people go!"

                    homura "Really? I thought you two were sworn enemies. Anyway, I'm afraid I can't do that."

                "Mock him":
                    $ MC.evil += 1

                    you "What was that? You sound like one of your whores with a fat cock in her mouth! *scoff*"

                    play sound s_gag

                    kosmo "MMHNNNGGHH!" with vpunch

                    you "Ooh, someone just got burned!"

                "Ask to let him speak":
                    $ MC.neutral += 1

                    you "Homura, the man wants to say something."

                    homura "I don't think I should..."

            homura "He {i}is{/i} burning to say something, though. I guess we can let the man speak his mind..."

            play sound s_dress

            "She removes his gag."

            kosmo "[MC.name]... [MC.name], my friend! Oh, thank Arios, you've come to save me, haven't you?"
            
            kosmo "This is all a big misunderstanding, please tell your ninja girl to release me!!!"

            you "My ninja girl?"

            homura "Is he referring to me?"

            you "Homura isn't my girl, Kosmo. Pay attention to the plot, will you?"

            "You steal a tense look at the masked man whose red gaze shimmers unnaturally."

            homura "Master Kosmo here tried to hire my services to neuter you, [MC.name], if you can believe it. Would have been a pity... *wink*"

            homura "But I saw an opportunity when we met at his house... It was both secluded, and luxurious enough that we could lure you and the Princess there."

            kosmo "Lady ninja, be merciful! Let me go! You can keep the house, and all of my servants, you're welcome to have them!"

            homura "Aren't you the brave one! We're just borrowing your place for tonight, so relax... *scoff*"

            "She jests, but her eyes are cold."

            "In desperation, the bound whoremonger turns to the masked man and begs for his life."

            kosmo "Please, my good Sir! I have nothing to do with [MC.name]! Whatever your quarrel with him, you can settle it and leave me out of it! I swear I shall never tell anyone!"

            "Panicking, kosmo takes turns pleading each and every one of you for help."

            kosmo "Please help me, [MC.name]! I've made a mistake, I swear I shall never, ever bother you again! Free me from this mad bastard and his crazy bi-"

            play sound s_dress
            
            kosmo "*muffled*"


            "Homura expertly puts the gag back on again."

            play sound s_gag

            kosmo "HNNNGGGH!" with vpunch

            homura "I tire of his conversation incredibly quickly."

            you "You and me both."

            mask "Is he a friend of yours?"

            you "Hardly."

            mask "No matter... We will soon be done with him. And you."

            if NPC_homura.love > 10:
                homura "W-What do you mean, Shiro? Can't we just..."

                mask "Don't be a child, Homura. You know full well that after tonight, none of them can walk away from this."

            elif NPC_homura.love > 5:
                "Homura looks awkward and says nothing."

            elif NPC_homura.love > 0:
                homura "*sigh*"

            else:
                homura "Let's just get this over with. *roll eyes*"

            jump c3_mask_questions

        "I have no more questions":
            pass

label c3_confrontation_fight: # Follows previous label

    stop music fadeout 3.0

    mask "Very well, enough idle chatter. Let us come to the true purpose of our gathering."

    "He turns to Kurohime, who stiffens as he steps forward."

    mask "Which is {i}you{/i}, naturally."

    kuro "Naturally."

    mask "Our acquaintance was brief, sister. Perhaps that's for the best."

    kuro "Explain yourself."

    if not NPC_kenshin.flags["dead"]:
        kenshin "Stand back! Stay away from Her Highness!"

    mask "Fufufu... You see, our father isn't long for this world. And as I said, I am the rightful heir."

    mask "After all, I am a man, and the firstborn."

    mask "However... If someone were to marry you..."

    kuro "What? That cursed wedding, again?"

    mask "Indeed. Your husband would gain a claim to the throne as well. Weaker than mine, certainly... But feeble hearts and minds are easily swayed."

    mask "This would mean civil war, and we can't have that. For the good of the Realm, which you understand, of course, sister. You're no fool."

    kuro "..."

    you "Or, hear me out... Why don't you scurry back to your forest hut to eat leaves and lick nuts or whatever it is you do, and we'll just call it a day?"

    mask "Hmph, humor. Shield of the weak and feeble-minded..."

    you "Well, no one can accuse you of having it in excess."

    mask "Let's end this. Any last words, [MC.name]?"

    menu:
        extend ""

        "Pledge to defend the princess":
            you "I will gladly put my life on the line to protect Princess Kurohime."
            
            you "{i}En garde{/i}!" with vpunch

            "You place yourself between him and the princess, ready to match your words with action."

        "Make light of his threat":
            you "If your swords are as sharp as your wits, I'm afraid you'll bludgeon me to death..."

            mask "Humor again. How tiresome. *scoff*"

        "Inform that you will kill him":
            you "You should be the one answering that. Because by the time I'm done with you, you'll wish the demons had finished the job."

            "Behind his mask, his fiery eyes narrow."

        "Boast about fucking his girl":
            $ NPC_homura.love -= 1

            you "Ever hear Homura scream my name when you're getting it on? Don't blame her. How could a simple forest hick measure up?"

            "The masked man just smiles, not taking the bait. Homura rolls her eyes, annoyed."

        "Make a last attempt to negotiate":
            you "Think this through. Do you really want to start your rule over the corpses of innocents, including your own twin sister, of all people? You can still walk away from this madness."

            "The masked man falters, only for a moment. You catch it, and so does Homura. He exhales deeply."

            mask "We're far past the point of no return. The die is cast."

        "Call for aid":
            you "Heeeeeeelp!!! Anyone!!! Heeeeeeeelp!!!"

            "You realize the pointlessness of your plea. Kosmo's mansion is far too vast for your voice to reach the neighborhood."

    mask "A pity, [MC.name]. You were a worthy adversary, in your own way."

    mask "I wish your final words had more panache, but no one can rise above their station..."

    mask "Not men of low extraction such as you... Nor a fragile woman like my sister..."

    mask "And nor I, last in a dynasty of sellswords and adventurers, forever forced to seize by blade what's ours by right."

    play sound s_sheathe

    show mask attack at totheleft with dissolve
    mask "It is time for the dance of fire and steel. Sister. [MC.name]..."

    mask "Tonight, you DIE!" with vpunch

    play music m_chemical_factory fadein 3.0

    call c3_ninja_showdown(["homura showdown", "mask showdown"], [(homura, "With fire!"), (mask, "And steel!")]) from _call_c3_ninja_showdown

    if not NPC_kenshin.flags["dead"]:
        scene black with fade
        kuro "To arms, Uesugi! Don't let that madman near me!"

        call c3_ninja_showdown(["kenshin showdown"], [(kenshin, "I will protect you with my life, Your Majesty!")]) from _call_c3_ninja_showdown_1


    else:
        "The Princess stands defenseless, having lost her loyal Knight Commander with the death of Lady Kenshin."

        kuro "H-Help!!!" with vpunch

    # Check how many ninjas are allied with MC

    $ nin_list = []
    $ pics = []
    $ nin_intro = []

    if NPC_narika.flags["c3 path"] == "ally":
        $ nin_list.append(NPC_narika)
        $ pics.append("narika showdown")
        $ nin_intro.append((narika, "Leave my bo- My good friend alone!"))

    if NPC_mizuki.flags['c3 path'] == "revenge" or debug_mode:
        $ nin_list.append(NPC_mizuki)
        $ pics.append("mizuki showdown")
        $ nin_intro.append((mizuki, "Let me put some cold water on your pathetic fire!"))

    if NPC_haruka.flags["c3 path"] == "ally" or debug_mode:
        $ nin_list.append(NPC_haruka)
        $ pics.append("haruka showdown")
        $ nin_intro.append((haruka, "If you want to harm [MC.name], you'll have to go through me first!"))

    if nin_list:
        if len(nin_list) >1:
            "Woman's voice" "Hey, don't leave us out!" with vpunch
        else:
            "Woman's voice" "Hey, aren't you forgetting someone?" with vpunch

        scene black with fade

        call c3_ninja_showdown(pics, nin_intro) from _call_c3_ninja_showdown_2

        scene black with fade

        $ narrator("Your Kunoichi all%s ha%s come to your aid!" % (plural(len(nin_list), singular="y", ending="ies"), plural(len(nin_list), singular="s", ending="ve")))

    else:
        "With no allies to aid you, you prepare for a desperate duel against the duo of assassins."

        scene black with fade

    ## PHASE I - Homura faceoff ##

    $ ninja_hurt = []

    "You leap forward to shield Kurohime, but Homura stops you."

    homura ninja "Not so fast!" with vpunch

    play sound s_fire
    show bg homura fire at top with flash

    homura "FIREWALL!!!"

    "The room erupts into flames, cutting you off from the Princess and her brother."

    scene black with fade

    show bg mansion fire at top with dissolve

    show homura attack with dissolve

    you "Damn it, Homura! You can't just murder a sovereign, you lunatic!"

    "Doubt only flickers in Homura's eyes, as she ponders what to do with you."

    if NPC_homura.love > 10:
        you "What are you doing, Homura? After everything we've been through?"

        homura "I... I must..."

        "The masked man's voice booms across the curtain of flames."

        mask "Homura, don't falter! Strike him down!"

    elif NPC_homura.love > 5:
        you "What the hell, Homura? Do you really want my head?"

        homura "I have no choice, [MC.name]. Please... Step aside, and you can still walk away."

    elif NPC_homura.love > 0:
        homura "Nothing personal, [MC.name], but you are at the wrong place at the wrong time. I'll make it quick..."

        you "Back off!"

    else:
        homura "Finally, you bastard! Time to pay for all you did to me!"

        you "Hey, you consented, more or less... It was just a bit of fun..."

    "A curtain of fire now splits the room in two, leaving you and Homura facing off on one side."
    
    "Heat warps the air and blurs your vision. Homura bars your way, weapon raised."

    if MC.playerclass == "Warrior":

        play sound s_sheathe

        "Your blade is already drawn. You whirl it through the air, keeping distance to gauge your opponent."

        "Her stance is flawless. She's most likely faster, and more agile. You have the strength and reach - but she commands deadly fire magic. Your odds are grim."

    elif MC.playerclass == "Wizard":

        play sound s_spell

        "Your mind sharpens, bracing your mental defenses and focussing on half-a-dozen spells that could come in handy in such a fight."

        "However, you know full well that fire is the most destructive form of magic - and you'll need to dodge the deadly attacks of a trained assassin while you counter her spells. Your talent may not be enough to survive."

    elif MC.playerclass == "Trader":

        play sound s_whistle

        you "*whistle"

        play sound s_roar

        "You are relieved to hear Drogon's roar echo outside: your faithful pet has followed you all the way here. Still, the fire kunoichi has plenty of time to turn you into cinders before the wyrm makes it."

    $ _fight = False

    if NPC_homura.love > 10:

        "You are about to act, but something in her attitude gives you pause."

        homura "I've spent years following Shiro, helping him to the best of my abilities, forgetting myself in service of his destiny..."

        homura "And now that we're here, about to see this thing through... I can't do it."

        "Unexpectedly, she lowers her weapon, looking down, her eyes brimming with tears."

        homura "I want to help Shiro, I want to... But you've shown me kindness, [MC.name]. More than... More than he ever did."

        homura "And I... I care for you."

        homura "Enough blood has been spilled. I don't want to shed yours. I don't want to be part of this any longer. "

        "Shirohito's furious voice rises over the fire, his silhouette thrashing behind the flames."

        mask "YOU TOO, Homura? You would betray me, at the hour of my revenge?"

        "Her face steels with resolve."

        homura "Your hatred has poisoned your soul, Shiro! You are about to turn into the evil you vowed to fight!"

        mask "CURSE YOU, WOMAN!!! I don't need you! I don't need anyone! I will conquer my rightful place on the throne!"

        play sound s_crash

        "A large wooden beam crashes down from the ceiling, drowning out his fury."

        play sound s_clang

        "Homura looks at you, her face sad but resolute."

        homura "I thought I loved Shiro... But I was under a spell. Somewhere along the way, I lost my way."

        homura "But with you, I... I felt normal. Like I was allowed to be myself, that it wouldn't make me look weak, or unworthy. Like I didn't have to put my feelings last."

        homura "Ironic, isn't it? I was lying to you, I was wearing a mask... And yet somehow, I could reconnect with the real me."

        "She lets her weapon drop with a clang."

        homura "I won't raise a hand against you, [MC.name]. Do what you must. I'm your prisoner."

        "She moves out of you way, and you walk past her."

        you "Thank you, Homura. And... I'm Sorry."

        homura "Sorry? For what?"

        you "This."

        if MC.playerclass == "Warrior":

            play sound s_punch
            with vpunch

            "Using an old trick you learnt from your warmaster, you strike a precise blow to the backof her neck. She collapses, unconscious."

        elif MC.playerclass == "Wizard":

            play sound s_spell

            "Waving your hand in front of her, you cast a sleeping spell, and she is too surprised to resist. Her eyes flutt shut, and she falls unconscious."

        elif MC.playerclass == "Trader":

            play sound s_bubble

            "You uncork a small vial of chloroform under her nose, and old Borgo trick. She slips into unconsciousness."

        hide homura with pixellate

        "You catch her as she falls, and lay her on the floor gently, some way away from the flames."

        you "Stay here, while I end this."

        $ NPC_homura.flags["c3 path"] = "captured"

    elif NPC_homura.love > 5:

        "Despite the fiery situation, Homura remains calm. She nods towards something, and you cautiously follow her gaze, careful to keep your guard up."

        "There is a gap in the firewall by the stairs, just large enough for a person to go through unscathed."
        
        "She left it open on purpose!"

        homura "We don't have to fight, [MC.name]. I have nothing against you."

        homura "Just take the way out. Shiro will be satisfied with the Princess, and you can disappear and lay low for a while."

        you "But Princess Kurohime..."

        "She shrugs."

        homura "Kurohime will die tonight, [MC.name]. There's nothing you can do. Think about saving your own skin."

        "You are torn. You don't want to fight a trained killer, but can you really leave the princess behind?"

        menu:
            extend ""

            "Of course not":
                $ MC.good += 2
                you "I can't abandon the Princess. Prepare to fight."

                homura "I wanted to help you... *sigh*"

                "Her face hardens."

                homura "You foolish dreamer. Very well, we shall fight."

                $ _fight = True

            "I'm out of here":

                $ MC.neutral += 2
                $ _continue = False

                you "I've had enough with cloak and dagger politics. I'm getting the hell out of here!"

                hide homura with moveoutleft
                play sound s_dodge

                "Leaping through the gap in the flames, you search for a way out. A large window stands open on the top floor. Running up the stairs, you take one last look back before leaving."

                $ NPC_homura.flags["c3 path"] = "escaped"

    elif NPC_homura.love > 0:

        "Homura looks at you with cold, dispassionate eyes. Eyes you now know belong to a killer."

        homura "This is the end of the road. You know we can't let you go."

        you "No witnesses, eh? Well, I'm not going down without a fight."

        homura "Suit yourself..."

        $ _fight = True

    else:

        "Homura looks at you with fury and determination. She's spoiling for a fight."

        you "Holding a grudge isn't good for you. It makes your face all puffy and fat."

        homura "..."

        "She doesn't rise to the insult. Instead, she moves with blinding speed."

        play sound s_dodge

        pause 0.2

        play sound2 s_boing

        show homura attack at jumping

        "You barely dodge out in time to avoid an expertly throw shuriken."

        $ _fight = True

    ## PHASE II - Homura resolution ##

    # "c3 homura fight" possible values: capture, escape (MC escapes), ninja hurt (Homura escapes)

    if _fight:
        $ ninja = None
        
        $ bonus = 0
        $ bonus_ttip = ""

        if MC.has_item(fire_rune.name):

            you "(It's time... Let's use that fire rune I bought from Willow...)"

            "You don't have your trusty hammer, though. You will have to get creative if you want to beat Homura."

        "She is already coming at you, moving with the speed you've come to expect from a Kunoichi."

        show homura attack at jumping

        play sound s_shatter

        with vpunch

        "If not for the reflexes you honed over weeks of fighting the Kunoichi, her first strike would have pierced your heart."

        "Instead, you dodge just in time, out of sheer habit."

        if MC.has_item(fire_rune.name):

            "You grab her belt, trying to pull her off balance."

            "She answers with a visious elbow strike, splitting your lip. Her blade whizzes between you, inches from where your hand just was."

            "You retreat hastily. The metallic taste of blood in your mouth feels like victory, though."

            call remove_item(fire_rune, definite_article=True) from _call_remove_item_9

            "You smile through the pain, because the fire rune is now securely tucked inside her belt."

            homura "..."

            "Homura's expression tells you you did something right. She struggles to concentrate, as if something were tugging at at her mind."

            you "What's the matter, Homura? Are you scared?"

            "She growls and comes at you again."

            $ bonus += 3
            $ bonus_ttip += "Fire Rune: +3\n"

        if nin_list:
            play sound s_clang

            $ ninja = nin_list.pop(random.randrange(len(nin_list)))

            ninja.char "Leave him alone!"

            "[ninja.name] leaps to your aid, stopping Homura in her tracks."

            if ninja == NPC_narika:
                ninja.char "Don't touch him, bitch! [MC.name] is mine - Err, I mean, he's my ally... *blush*"
            elif ninja == NPC_mizuki:
                ninja.char "I'm afraid I can't let you do that. [MC.name] is my new boss. I can't let you harm him."
            elif ninja == NPC_haruka:
                ninja.char "[MC.name] saved my mentor. It is my turn to repay this debt."

            "Homura steps back, and the three of you walk in a circle, weapons drawn. Her eyes narrow, darting between you and [ninja.name]."

            "Are the odds turning in your favor?"

            $ bonus += 3
            $ bonus_ttip += "Ally: +3\n"

        # Challenge
        $ chal = renpy.call_screen("challenge_menu", challenges=[("Fight Homura", "fight", 8-bonus), ("Use a spell", "control", 8-bonus)])

        $ bonus_ttip += "Character bonus: %i\n" % (MC.get_stat("strength") - MC.get_stat("strength", raw=True))
        if MC.get_effect("change", chal + " challenges"):
            $ bonus_ttip += "Challenge bonus: %i" % MC.get_effect("change", chal + " challenges")

        # Run challenge

        $ norollback()

        call challenge(chal, 8, bonus=bonus, bonus_text = bonus_ttip) from _call_challenge_70 # result is stored in the _return variable
        $ r = _return

        $ norollback()

        if _return:
            $ NPC_homura.flags["c3 path"] = "captured"

            if ninja:
                "With [ninja.name] at your side, Homura is now on the back foot."

                show homura attack at jumping

                play sound s_clang

                pause 0.3

                play sound2 s_clang

                with flash

                "Every time she attempts a cautiously attack, [ninja.name] counters viciously. Eventually, Homura redirects more of her attention to the larger threat."

            else:
                play sound s_clang

                pause 0.3

                play sound2 s_clang

                pause 0.2

                play sound3 s_clang

                pause 0.1

                play sound s_clang

                with doubleflash

                "As you trade blows with Homura, you gradually find your rhythm, taking advantage of the experience accumulated since arriving in Zan."

                "While Homura is agile, she lacks Narika's speed, Mizuki's cunning, and Haruka's sheer strength."

                homura "You're... you're good..."

                play sound s_clang

                pause 0.3

                play sound2 s_clang

                with flash

                "Suddenly unleashing a flurry of attacks, you force Homura's back to the fire."

                play sound s_fire

                with flash

                "She begins weaving a spell with one hand, aiming a fireball at you. You shove her wrist upward just in time to avoid the blazing projectile."

                play sound s_crash

                with vpunch

                "The fireball hits the ceiling, and another beam comes crashing down. You both dive down out of the way, but you are slightly quicker to get back on your feet."

            you "(This is my chance...)"

            if chal == "fight":

                if MC.playerclass == "Warrior":

                    play sound s_sheathe

                    "While she is still disoriented, you lunge forward with a vicious blow, aimed at her head."

                    play sound s_punch
                    with vpunch

                    "She manages to dodge, but your strike catches her with the flat of the blade. The blow is enough to knock her unconscious."

                    hide homura with pixellate

                    "You make sure that she is out cold. Satisfied, you shift your focus to the other side of the fire."

                elif MC.playerclass == "Wizard":

                    "Desperate fights call for desperate measures: gripping your wizard's staff in both hands, you whirl it around, a trick you picked up while sparring with your security guys."

                    play sound s_punch
                    with vpunch

                    "Homura doesn't see it coming. The staff strikes her squarely on the head with a sickening *thud*. You hope you didn't break her skull."

                    hide homura with pixellate

                    "The Kunoichi is tough, but not that tough. She crumples unconscious."

                    "You turn your attention to the other side of the room."

                elif MC.playerclass == "Trader":

                    "Instinctively, you sense a reassuring presence in your periphery."

                    "Just as Homura turns har attention back to you, determined to give you the final blow, you summon some backup."

                    play sound s_whistle

                    you "DIVE BOMB!"

                    play sound s_roar

                    pause 0.3

                    play sound2 s_shatter

                    "The glass ceiling shatters, and a red projectile rockets into the room, hitting Homura square in the chest."

                    you "Yay, Drogon! Good boy!"

                    "Your pet dragon flaps excitedly, then perches on Homura's body as she stirs feebly beneath him."

                    "Unaffected by the flames around him, he turns to you, awaiting the command to finish her off."

                    you "Leave her. She's down. We've got more pressing matters."

                    hide homura with pixellate

                    "You turn your attention to the dark silhouettes on the far side of the fire."


            elif chal == "cast":

                if MC.playerclass == "Wizard":

                    "Taking advantage of the situation, you unleash the spell you'd been preparing: the perfect counter to fire."

                    play sound s_stone

                    with vpunch

                    you "GELATUM INCARCERUM! Ice coffin!" with vpunch

                    play sound s_stone
                    with flash

                    "Homura watches in horror as solid ice forms at her feet and quickly crawls up her legs to encase her body."

                    with flash

                    "She tries to ignite her hands, but it's too late. The ice reaches her waist, then her arms, then her neck."

                    with flash

                    "She locks eyes with you, white with panic, just before the ice reaches her face."

                    play sound s_stone
                    hide homura with pixellate

                    you "Don't worry, it's harmless... I think."

                    "She's frozen solid, but the fire still rages around. You must deal with the rest of the fight before she starts to thaw."

                else:

                    "Since your introduction to the dark belly of the city, you are no longer a stranger to magic. You picked up some useful tricks along the way."

                    play sound s_clang

                    with flash

                    "You parry Homura's blade, knocking it aside. Then, with your free hand, you snap your fingers at her face."

                    play sound s_lightning

                    with doubleflash

                    "*FLASH*"

                    "You close your eyes just in time as a blinding burst of light explodes."

                    play sound s_scream

                    homura "Aaaaah!!!" with vpunch

                    "The light overload scrambles her senses. She drops like a puppet with its strings cut."

                    hide homura with pixellate

                    "You rub your own eyes, fighting off a headache. After making sure that she is out of it, you refocus on the chaos beyond the flames."

        else:

            if ninja:
                "Fighting two-on-one, Homura realizes she's at a disadvantage."

                play sound s_fire

                "She shakes her fist, and a pillar of flame erupts under [ninja.name]'s feet, forcing her to leap back."

                "With [ninja.name] temporarily cut off, Homura turns her attention back to you."

                homura "The weakest link in the chainmail..."

            else:
                play sound s_clang

                pause 0.3

                play sound2 s_clang

                with flash

                "As you trade blows, you realize you are outmatched. Homura is faster, stronger, and every strike of hers is deadly accurate."

                "You start feeling overwhelmed."

            if chal == "fight":

                you "I must use my secret technique! WHAAAA!!!"

                play sound s_punch
                with vpunch

                "With a chuckle, Homura vanishes in a puff of smoke. Your mighty strike hits only a wooden log."

                "Before you can dislodge your weapon, Homura is on you again."

            else:

                "The spells you practiced sounded easier in theory. Now, dodging lethal strikes while trying to remember arcane syllables, your mind goes blank."

                "Taking advantage of a lull in her attacks, you try to form the words of a shield spell."

                you "M-Minoris di..."

                play sound s_punch
                with vpunch

                "It was a feint. Homura doubles down on her last attack with a spinning kick, connecting squarely with your jaw."

                "The whole world goes white. When you come back to, you are laying on your back."

            with pixellate

            homura "It's over, [MC.name]..."

            if ninja:
                $ NPC_homura.flags["c3 path"] = "escaped"
                $ ninja_hurt.append(ninja)

                play sound s_clang

                ninja.char "No!!!" with vpunch

                show expression ninja.char.image_tag at right with moveinright
                show homura attack at left with move

                "[ninja.name] dives in, blocking the fatal blow."

                play sound2 s_sheathe

                with flash

                "Homura's blade slips through, though. [ninja.name] drops to her knees, and she coughes blood."

                hide expression ninja.char.image_tag with pixellate

                you "[ninja.name]!!!"

                ninja.char "[MC.name]... Run!"

                "With the last of her strength, [ninja.name] casts one final spell."

                if ninja == NPC_narika:
                    narika "HAA!!!" with vpunch

                    "Narika howls in pain. A whirlwind bursts out around you,  flattening the flames."

                elif ninja == NPC_mizuki:
                    mizuki "Ouch... That one hurt... *panting* After this scrap... We're all going to need a shower."

                    play sound s_splash

                    "Suddenly, bucketloads of water pour over and around you, dousing the nearest fire."

                    "Through the hissing steam, you see the masked man, closing in on the princess with his swords drawn."

                elif ninja == NPC_haruka:
                    haruka "Stone... Crush... *groan*"

                    play sound s_stone
                    with vpunch

                    "With a last ditch effort, Haruka conjures a stone bridge over the fire behind you."

                "She gives you a nod, the light in her eyes fading. You understand."

                hide homura with dissolve
                play sound s_dodge

                "You leap across the fire to the other side, leaving [ninja.name] behind."

            else:
                $ NPC_homura.flags["c3 path"] = "escaped"

                play sound s_sheathe

                you "Arrh!" with hpunch

                with vpunch
                play sound s_splat

                "This time, you miss your dodge. You feel cold steel bite your side. The world starts spinning."

                "As you fall to the floor, you begin to see the scene as if through the eyes of someone else."

                "Homura towers above you, ready to finish you off. Her mind is already elsewhere, eager to join her master's fight."

                suzume shrewd "Hold on, boss!" with vpunch

                play sound s_fire
                scene black with flash

                "A leather pouch lands beside you, bursting open. Thick, white smoke fills your view."

                "Small yet strong hands grab you by the shoulders and drag you away."

                you "What the... Suzume?"

                suzume "It's me, boss! I'm pulling you out of here."

                "You hear Homura curse and cough as the smoke swirls."

                "Your vision is fading, but your focus lingers on the flickering shadows beyond the large fire - the dance of death has begun."

    stop music fadeout 3.0

    ## PHASE III - Fire interlude

    if NPC_homura.flags["c3 path"] == "captured" or ninja_hurt:
        $ _continue = True

        "Disoriented by the smoke and flames, you struggle to find your way to the other side of the room."

        play sound s_wscream

        "Panicked screams echo from the corners of the room, and you think about Kosmo and his servants, trapped amidst the fire."

        "Hopefully some of them will manage to break their bonds in time and help the others."

        if MC.get_alignment() == "good":
            "Your heart bleeds for the poor wretches, but you must focus on saving the princess for now."

        elif MC.get_alignment() == "neutral":
            you "Well, I've got my own problems to take care of right now. Where is the Princess?"

        elif MC.get_alignment() == "evil":
            you "Good riddance! Now, I'd better get to that asshole Shiro before the stench of roasted Kosmo reaches my delicate nostrils..."

        "A curtain of flames block your vision. You begin to panic, unsure if you can even find your way out of the blazing fire, when something catches your eye."

        stop music fadeout 3.0

        if MC.god == "Arios":
            call c3_arios_vision() from _call_c3_arios_vision

            "You have no time to ponder these mysteries longer. As if driven away by the divinity, the flames part, clearing your way towards the unfolding duel."

        "Just past some burning furniture, you get a glimpse of Shirohito and his victim."

    else:
        $ _continue = False

        "The flames that Homura sparked now raise all the way to the upper floor, their roar makes you shiver."

        stop music fadeout 3.0

        if MC.god == "Arios":
            call c3_arios_vision() from _call_c3_arios_vision_1

            "You have no time to ponder these mysteries longer. As if driven away by the divinity, the flames part, clearing your view of the unfolding duel."

        "Just before you pass out, your every sense is on alert in a bizarre out-of-body experience."

label c3_confrontation_shiro(): # Follows previous label

    ## PHASE IV - Shirohito confrontation

    show bg mansion fire with dissolve
    show mask attack at right with dissolve
    show kuro at left with dissolve

    play music m_danger fadein 3.0

    if not NPC_kenshin.flags["dead"]:
        "The princess is huddled back into a corner. Kenshin is stubbornly blocking all avenues of attack with her sword."

        "She has several bleeding wounds to show for her devotion. As far as you can tell, Shirohito is unhurt."

    else:
        "The cursed prince and the frail princess are walking in a circle, keeping away from each other."

        "Even though, or perhaps because, Kurohime is defenseless, Shirohito is taking his time to attack."

    "You can hear bits of their conversation. It seems like Shirohito is trying to work up the courage to carry out this final and most important murder."

    mask "Sister. I understand, you're just a pawn in this. But sometimes, pawns need to fall, to spare the King."

    "Though pale with fear, the Princess doesn't avert her gaze."

    kuro "I am no pawn. You forget that the queen {i}is{/i} the most powerful piece on the board."

    mask "You are no queen. Only a princess. So insignificant, no one ever bothered to write rules for you."

    play sound s_surprise

    kuro "I write my own rules!" with vpunch

    play sound s_maniacal_laugh

    mask "Insignificant, and delusional... You won't be missed. A mere footnote of history."

    kuro "So this is it, then? You'd murder your own kin? And compound regicide with fratricide?"

    "The masked man's voice rises in contempt, almost manic."

    mask "Don't you see? It is a matter of survival for our dynasty! Survival of the fittest!" with vpunch

    mask "My father is unfit to rule! And so are you, about to be sold to a power-hungry husband, who'll carve up the Realm for himself."

    mask "I {i}am{/i} fit to rule. I have the will, I have the skills, I have the courage, and I have..."

    mask "The RIGHT!" with vpunch

    "Kurohime remains silent, her eyes hurling daggers at her treacherous brother."

    if _continue:

        $ _fight = False

        $ allies = 0

        if not NPC_kenshin.flags["dead"]:
            $ allies += 1

        $ allies += len(nin_list)

        you "*cough*" with vpunch

        "Shirohito's shoulders tense slightly as he hears you clear your throat. Yet he turns slowly to face you, downplaying the threat you represent."

        hide kuro with dissolve
        show mask attack at center with move

        mask "So, Homura couldn't stop you... Interesting."

        "He doesn't seem particularly concerned about the fate of his lover."

        mask "So you would defy me, [MC.name]?"

        if nin_list:

            $ ninja = nin_list[0]
            $ ninja2 = False
            $ ninja3 = False

            if len(nin_list) > 1:
                $ ninja2 = nin_list[1]

                if len(nin_list) > 2:
                    $ ninja3 = nin_list[2]

            ninja.char "He's not alone!"

            "[ninja.name] appears at your side. Shirohito frowns."

            if ninja2:
                ninja2.char "I'm here too."

                "Shirohito feels the tide turn. His eyes flick nervously from side to side, considering his chances."

                if ninja3:
                    ninja3.char "And so am I."

                    "Zealous as he is, the prince can see this is a battle he cannot win. He grits his teeth in anger."

            you "I have backup. You don't."

        else:

            "He scans the room, betraying a flicker of anxiety - expecting more enemies to emerge. But he relaxes once he realizes you're alone."

            mask "Then bear witness, [MC.name]. There is nothing you, a mere shopkeeper, can do to hinder Royal destiny."

            you "I don't need help to kick your royal butt into the dirt. Your Highness."

        stop music fadeout 3.0

        if allies and story_flags["c3 clue mask"]:

            $ NPC_mask.flags["unmasked"] = True

            mask "Surely, you must see..."

            suzume "Hi there! Speaking of seeing..."

            play sound s_sheathe

            pause 0.2

            play sound s_dodge
            with flash

            "A lone kunai whistles through the air, barely missing Shirohito's face."

            hide mask with dissolve
            pause 0.05
            show mask attack with dissolve

            "He barely flinches in front of the surprise attack."

            show mask attack at right with move
            show suzume:
                xalign -0.6
                yalign 1.0
            with dissolve

            mask "And here is [MC.name]'s pet... You make a poor assassin. You missed."

            suzume bend "Did I? Kukukukuku..."

            play sound s_dodge
            show suzume bend at jumping

            "Hissing like a cat, Suzume leaps at him, and deftly swipes his mask away."
            
            show mask attack blind with dissolve
            
            mask "What?"

            "The prince realizes too late: the kunai had severed the leather strap of his mask."

            mask "My mask! My eyes! Nooo!!!" with vpunch

            show suzume bend at jumping

            play sound s_sheathe

            pause 0.2

            play sound2 s_sheathe

            pause 0.3

            play sound3 s_sheathe

            pause 0.1

            play sound s_sheathe

            show suzume bend at jumping

            "Shirohito unleashes a flurry of blows that would have shred anyone else to pieces. But Suzume dodges away with feline grace."

            play sound s_laugh

            suzume "Thanks! I'll leave you guys to it!"

            hide suzume with moveoutleft
            play sound s_dodge

            "After a few swift steps, she somersaults onto the window ledge."

            you "Wait, Suzume! Come back and help us!" with vpunch

            suzume "Sorry boss, I can't right now. I have a delivery to make!"

            "She disappears back into the night."

            you "Suzume! Curses..."

            show mask blind attack at center with move

            play sound s_sheathe
            with flash

            mask "YOU! This is all your fault!"

            play sound s_fire

            "The blind prince now turns his fury to you."

        else:
            "His unblinking red gaze fixes on you."

        scene black with fade
        if NPC_mask.flags["unmasked"]:
            show bg mask_duel1 blind with dissolve
        else:
            show bg mask_duel1 with dissolve

        $ allies = 0
        $ text1 = ""

        if not NPC_kenshin.flags["dead"]:
            $ allies = 1
            $ text1 = "Counting Kenshin, "

        $ allies += len(nin_list)

        if allies == 0:
            "With the princess standing defenseless, Shirohito's deadly focus is on you."

            "He looks as if he was about to swat a fly."

            $ _fight = True

        elif allies == 1:
            "[text1]Shirohito now faces two opponents."

            "He still doesn't see you as a serious threat, though, so it doesn't deter him in the least."

            $ _fight = True

        else:
            "[text1]Shirohito is now facing [allies] skillfull warriors."

            if NPC_mask.flags["unmasked"]:
                "And without his mask, he will have to fight blind."

            "He may not think much of you, but your quick defeat of Homura gives him pause."

            if allies > 2 or (allies > 1 and NPC_mask.flags["unmasked"]): # Shirohito retreats

                $ _fight = False

                "He glances at the princess, his fury hardening into cold contempt."

            else:
                $ _fight = True

                "Still, he thinks too much of himself to retreat now."


        if _fight:
            
            $ bonus = 0
            $ bonus_ttip = ""

            if allies:
                $ bonus += allies*2
                $ bonus_ttip += "Allies: +%i\n" % bonus

            if NPC_mask.flags["unmasked"]:
                $ bonus += 3
                $ bonus_ttip += "Unmasked: +3\n"

            play music m_chemical_factory fadein 3.0

            kuro "[MC.name]!"

            you "I'm here, Princess!"

            kuro "Be careful... There's something about him... None of my wards work on him!"

            "Princess Kurohime, like many highborn ladies, has powerful magic protections on her and even a cursory knowledge of magic. And yet..."

            kuro "Spells don't affect him as they should."

            play sound s_maniacal_laugh

            if NPC_mask.flags["unmasked"]:
                mask blind "Indeed, Sister. I am full of surprises. What better assassin than one magic cannot detect or harm?"
            else:
                mask "Indeed, Sister. I am full of surprises. What better assassin than one magic cannot detect or harm?"

            if nin_list:
                "He flashes a wicked grin at your allies."

                mask "And here goes half your strength, ninjas."

            "You find it hard to believe. Immunity to magic is nearly unheard of - something only ancient masters have achieved over lifetimes of study."

            you "There must be a trick to it!"

            mask "Indeed, but I am not about to share it with you. Let's just say that my new friends have been helpful..."

            "Whatever the source of his resistance, the result is the same: you must face his blades without your magic."

            "You don't have time to ponder this new mystery."

            kuro "Please, [MC.name]! Stop him!" with vpunch

            if allies:

                if not NPC_kenshin.flags["dead"]:
                    kenshin "You shall not pass!"

                    "Resolute, Kenshin stands by your side, shoulder to shoulder."

                if NPC_narika in nin_list:
                    narika "Leave me and [MC.name] alone, you... You dark and handsome stranger!"

                    narika "(Wait... Is he trying to start a love triangle with me? Like that novel with the vampire, the werewolf, and the tentacle monster and the...)"

                    "Even as she daydreams, Narika reflexively falls in battle formation."

                if NPC_mizuki in nin_list:
                    mizuki "I never could stand this macho posturing from young men."

                    mizuki "I'm old enough to be everyone's grand-mother here. If I catch a naughty boy, I'll spank him myself!"

                    "Mizuki fans herself defiantly as she takes her position."

                if NPC_haruka in nin_list:
                    haruka "I heard your words before, and I see what we have in common. We both suffered at the claws of demons."

                    haruka "Yet I am honor-bound to defend [MC.name] and his Liege. Defend yourself!"

                    "With practiced ease, Haruka steps into the battle line."

                "Shirohito scoffs."

                mask "United you stand. United you'll fall."

            else:
                "Nothing stands between his steel and the princess - Except you."

                mask "I figured you were many things, [MC.name], but not suicidal. *smirk*"

                mask "Seems you don't have a friend left in the world."

                mask "Perhaps you'll meet one in the next..."

            # Challenge
            $ chal = renpy.call_screen("challenge_menu", challenges=[("Fight the prince", "fight", 10-bonus), ("Distract him", "bluff", 10-bonus)])

            # Run challenge

            $ norollback()

            if chal == "fight":
                $ bonus_ttip += "Character bonus: %i\n" % (MC.get_stat("strength") - MC.get_stat("strength", raw=True))
                if MC.get_effect("change", "fight challenges"):
                    $ bonus_ttip += "Challenge bonus: %i" % MC.get_effect("change", "fight challenges")

                play sound s_sheathe

                "Drawing your weapon, you hold your ground."

                "You both stare at each other for a long time. Flames keep rising, licking the ceiling. The heat becomes almost unbearable."

                "No one moves. Until suddenly-"

                mask "KIAI!!!" with vpunch

                you "HA!!!" with vpunch

                if not NPC_kenshin.flags["dead"]:
                    kenshin "DAAAA!!!" with vpunch

                if NPC_haruka in nin_list:
                    haruka "RAAAAH!!!" with vpunch

                if NPC_narika in nin_list:
                    narika "HYAAAA!!!" with vpunch

                if NPC_mizuki in nin_list:
                    mizuki "..."

                play sound s_sheathe
                pause 0.3
                play sound2 s_sheathe
                pause 0.1
                play sound3 s_sheathe
                pause 0.2
                play sound s_sheathe

                with doubleflash

                if allies:
                    $ text1 = "Your side"

                else:
                    $ text1 = "You"

                call challenge(chal, 10, bonus=bonus, bonus_text=bonus_ttip) from _call_challenge_71 # result is stored in the _return variable
                $ r = _return

                $ norollback()

                "[text1] and Shirohito fly past each other in a flash of steel. For a heartbeat, you don't even know who was hit."

                if r:
                    $ _fight = "won"
                    with vpunch
                    "Behind you, you hear Shirohito cough. Blood runs from his mouth, and he stumbles."

                    mask "Un-Unbelievable... I was... So close..."

                    "A crimson flower slowly blooms under his shirt. He is wounded, yet not down."
                    
                    "Bleeding but still standing, he turns to face you, staggering toward the exit."

                else:
                    $ _fight = "lost"
                    "Then the pain hits you."

                    you "AWGH!!!" with vpunch

                    "You glance down. A clean cut on your leg is pouring blood. It's a miracle it missed the artery."

                    "You're not dead yet, but you're out of combat. Dizzy, you can barely stand."

                    if allies > 1:
                        $ text1 = "your allies"

                    elif allies:
                        $ text1 = "your ally"

                    "You are horrified to find [text1] in similar shape, if not worse off."

                    if not NPC_kenshin.flags["dead"]:
                        "Kenshin lies in a spreading pool of red, barely moving."

                    "Shirohito doesn't even bother to finish you. Instead, he turns toward the princess, raising his blade to her neck."


            else:
                $ bonus_ttip += "Character bonus: %i\n" % (MC.get_stat("charisma") - MC.get_stat("charisma", raw=True))
                if MC.get_effect("change", "bluff challenges"):
                    $ bonus_ttip += "Challenge bonus: %i" % MC.get_effect("change", "bluff challenges")

                "You size him up. He's a trained fighter, it's all he's known since he was little. Fighting him head on is too risky."

                "You need to have your wits about you if you want to survive."

                you "I don't think you've properly assessed the situation, murderer."

                mask "Oh really? Enlighten me then, whoremonger."

                you "I beat three trained assassins just getting to you. And that's not even counting Suzume."

                mask "Good for you. But I'm made of harder stuff."

                you "You think? I also dispatched your attack dog, Homura, without breaking a sweat. Doesn't that strike you as... suspicious?"

                "A flicker of doubt crosses his face."

                mask "That is no small feat, true... Maybe you got lucky."

                you "Not only am I kicking butts left and right, I'm also the Princess's confidant. A simple brothel-owner? Doesn't that seem odd to you?"

                "His eyes narrow."

                mask "Your point...?"

                "Time to play your cards right."

                you "Think about it. Could a mere pimp take down an army of ninjas? Command such allies and resources? Come and go to the palace at leisure?"

                mask "..."

                you "The truth was right under your nose all along. You've been played for a fool. I'm no brothel-owner..."

                you "I'm the Royal Master of Assassins!"

                "You strike your most menacing pose, hoping it sells."

                if allies:
                    you "And my allies are here to end your bloody rampage... This whole time, you thought you were the hunter..."

                    you "But you're the prey."

                call challenge(chal, 10, bonus=bonus, bonus_text=bonus_ttip) from _call_challenge_72 # result is stored in the _return variable
                $ r = _return

                $ norollback()

                if r:
                    $ _fight = "won"

                    kuro "Well done, my dear [MC.name], I don't know what I would do without your loyal service."

                    "The princess effortlessly leans into your lie. You could swear she was a born actor."

                    kuro "Now, collect this dog's head." with vpunch

                    play sound s_sheathe

                    you "Your wish is my command, Your Highness."
                
                    "Shirohito's composure cracks. For the first time, real doubt creeps in."

                    mask "Y-You! Of course... I should've known it couldn't be that easy..."

                    "He looks like a caged animal, ready to bolt. And then-"

                    mask "If you think you have me cornered, think again!"

                    play sound s_punch
                    with vpunch

                    "*CRASH*"

                    "Shirohito kicks a burning table your way with savage force."

                    "He jumps through the flames, howling in pain as the fire burns him, but he pushes until he reaches the exit."

                    "Flaming debris explode in your way. You are too stunned - and too relieved your bluff worked - to give chase."

                else:
                    $ _fight = "lost"

                    mask "You... The Royal Master of Assassins?"

                    play sound s_maniacal_laugh

                    mask "BWAHAHAHAHAHAHA!!!" with vpunch

                    you "Uh oh.."

                    mask "The local pimp, a 'Master of Assassins'... Ah... You're really killing me..."

                    "He laughs cruelly, twisting the knife in your humiliation."

                    mask "Do you take me for a fool? After months of spying on my sister, do you think I don't know exactly who works for the Palace, and in what capacity? You think I wouldn't notice a 'Master of Assassins' among them?"

                    "Things then happen all too quickly."

                    play sound s_dodge

                    pause 0.3

                    play sound2 s_sheathe

                    "Before you can move, the prince is upon you."

                    if allies:
                        $ ninja_hurt += nin_list

                        play sound s_sheathe

                        if allies > 1:
                            $ text1 = "Your allies try"

                        elif allies:
                            $ text1 = "Your ally tries"

                        with flash

                        "[text1] to save you, but he is faster. His blades dance, too quick for the eye to follow."

                        play sound s_scream_loud

                        if not NPC_kenshin.flags["dead"]:
                            kenshin "AAAARGH!!!" with vpunch

                            "Kenshin is gravely wounded."

                        else:
                            ninja.char "Aaaaah!!!" with vpunch

                        "You alone are left standing, but not for long."

                    play sound s_punch
                    with vpunch

                    "He slams the hilt of his sword into your solar plexus, knocking the air out of you."

                    play sound s_punch
                    with vpunch

                    "You collapse on the ground, writhing in pain. He kicks your head hard as you try to get up."

                    mask "Thanks for the laugh, pimp... I'm not even going to waste time finishing you off."

                    mask "Let the fire take you. Or not. I don't care."

                    mask "As for you, sister..."

                    "He raises one of his blades, pointing it at her chest."

        if not _fight or _fight == "won":

            stop music fadeout 3.0

            "The man gives you a long look of defiance."

            if NPC_mask.flags["unmasked"]:
                mask blind "It seems your underling's foolish heroics have earned you a momentary reprieve, sister."
            else:
                mask "It seems your underling's foolish heroics have earned you a momentary reprieve, sister."

            play sound s_sheathe
            if NPC_mask.flags["unmasked"]:
                show bg mask_duel2 blind with dissolve
            else:
                show bg mask_duel2 with dissolve

            "He sheathes his swords."

            mask "But don't delude yourself, thinking you are beyond my reach."

            kuro "..."

            mask "Before you are wed, you will die. This I swear on the Gods - Old, Holy, and Dark."

            if not NPC_kenshin.flags["dead"]:
                kenshin "I'll take your head, blasphemer!"

            elif ninja:
                ninja.char "Let's end this now!"

            "You brace for another clash, but the fire growing around your group is becoming too close to ignore."

            play sound s_fire
            scene black with flash

            "Suddenly, the fallen prince steps outside and vanishes into the night."

            show bg mansion fire with dissolve

            you "You! Get back here and fight!" with vpunch

            "The flames and smoke thicken, blurring your vision, and you can't see anything beyond the threshold."

            "You move to pursue, when flaming debris crumbles from the ceiling, blocking your path."

            "A hand weighs on your arm. It's the Princess, coughing and barely able to stand."

            show kuro with dissolve
            play sound s_surprise

            kuro "C-Come, [MC.name]. We need to get out of here!"

            play sound s_gust
            with flash

            "She waves her arm, casting an air spell that parts the flames. It reveals a path to the stairs."

            you "So you are a trained caster."

            kuro "Hurry! This way!"

            play music m_siege fadein 3.0

            hide kuro with dissolve

            if not NPC_kenshin.flags["dead"] and allies > 1:
                $ text1 = "Kenshin and the Kunoichi"
            elif not NPC_kenshin.flags["dead"]:
                $ text1 = "Kenshin"
            elif allies:
                $ text1 = "the Kunoichi"

            "You let [text1] cover your rear as you rush behind Kurohime."

            if NPC_homura.flags["c3 path"] == "captured":
                "You spot Homura's unconscious body on the ground. Scooping her up, you run up the stairs."

                $ calendar.set_alarm(calendar.time+1, StoryEvent("c3_homura_capture", type = "night"))

            else:
                $ calendar.set_alarm(calendar.time+14, StoryEvent("shiro_homura_rumor", type = "morning"))

            "Smoke stings your eyes as you reach the top floor - when you hear a panicked scream."

            play sound s_wscream

            kosmo "Heeeeeelp!!!" with vpunch

            show bg kosmo fall1 at top with dissolve

            you "Kosmo?"

            "You are surprised to see Kosmo clinging to the balcony for dear life, a burning pit yawning beneath him."

            if allies:
                $ text1 = "the princess and your companions"
            else:
                $ text1 = "the princess"

            "You let [text1] move ahead, and approach your wretched competitor."

            kosmo "[MC.name]! My good friend! S-Save me!!!" with vpunch

            you "Well, look who it is... Last I saw, you were bound and gagged. I thought you lost."

            kosmo "A servant gave his life to free me, but the others just ran away! Ungrateful dogs!"

            kosmo "I was getting away, but the floor collapsed!"

            kosmo "Please, [MC.name]! Help me! I swear I'll never cause you trouble again!"

            menu:
                "Will you help Kosmo?"

                _("Save him"):                    $ MC.good += 5

                    "With a sigh, you grab Kosmo's arm and haul him up."

                    you "I've helped you. Against my better judgement."

                    kosmo "T-Thank you... !"

                    kosmo "I- I'm... S-Sorry I tried to have your... Your dick cut off."

                    you "Get lost, damn it! And don't show up at my place ever again."

                    scene black with fade

                    "Leaving Kosmo to navigate the fire, you try and catch up with the princess as she escapes through a window."

                    $ NPC_kosmo.flags["c3 ending"] = "spared"

                "Push him down":
                    $ MC.evil += 10

                    "Grinning from ear to ear, you walk up to him."

                    you "I've been waiting for this moment..."

                    kosmo "W-Wait! [MC.name]! I-In the name of Arios... D-D-Don't..."

                    kosmo "I-I know we haven't always gotten along, b-but... I swear, I will never bother you again!"

                    you "That's right. You won't."

                    play sound s_punch
                    with vpunch

                    play sound s_wscream
                    show bg kosmo fall2 at top with dissolve

                    kosmo "AAAAAAAARH!!!" with flash

                    "With a kick, you break the fragile railing, sending him tumbling down to his death."

                    scene black with fade

                    "Followed by Kosmo's screams of agony, you catch up with the princess as she escapes through a window."

                    $ NPC_kosmo.flags["c3 ending"] = "killed"

                "Leave him to his fate":
                    $ MC.neutral += 5

                    you "You're a big boy, Kosmo. I'm sure you'll figure it out. *shrug*"

                    kosmo "No, [MC.name], no!!! Don't leave me!"

                    you "Consider this payback for all the times you came to my house and roasted me."

                    you "This time, it's me coming to your house. But you can still roast!"

                    kosmo "[MC.name]! Come back here! You can't leave me, you whelp! Mother-"

                    play sound s_wscream
                    scene black with fade

                    "Ignoring his ranting, you rejoin the princess as she escapes through a window."

                    $ NPC_kosmo.flags["c3 ending"] = "left"

            show bg fire outside at top with dissolve

            "From there, you are able to drop down and reach the courtyard, leaving the inferno behind."

            $ story_flags["c3 ending"] = "victory"
            scene black with fade

            "You are quickly surrounded by the city watch and other men-at-arms, who were looking for the princess."

            stop music fadeout 3.0

            "Before you have a chance to talk to her, you get rudely separated by a group of knights."

            "Exhausted, you make your way back to the brothel."

            $ calendar.set_alarm(calendar.time + 3, StoryEvent(label = "c3_ending", type = "morning"))

            return

        else: # Fight lost

            stop music fadeout 3.0

            "Wounded, there is nothing you can do now except watch in horror."

    else: # MC escaped

        "You watch helplessly from afar, unable to intervene."

    play music m_danger fadein 3.0

    mask "Forgive me, sister. 'Tis best it be done quickly."

    play sound s_sheathe
    with fade

    "He lunges, and his blade pierces Kurohime's chest."

    play sound s_scream_loud

    kuro "AAAAH!!!"

    hide kuro with pixellate

    you "NOOO!!!" with vpunch

    if not NPC_kenshin.flags["dead"]:
        play sound s_scream

        "Kenshin howls in rage and anguish."

    "Time stands still for a moment. Then the unexpected happens."

    play sound s_gust
    play music m_demons

    scene black
    show bg murder at top
    with flashbackin

    "A supernatural wind chills your soul, snuffing all the flames out as if it was a campfire."
    
    "Around you, the darkness is thick with presence, as if malicious shadows were whispering forbidden words into your ears."

    "An inhuman shriek fills you with primal dread. But it doesn't come from the princess. It comes from the prince."

    play sound s_wscream

    mask "AAAARH!!! IT BURNS!!!" with flash

    hide bg with pixellate

    play sound s_clang

    "You cannot see him in the dark, but you hear his blades clatter to the floor."

    "Then, his figure stumbles into view, framed by moonlight, hands clawing at his face as he moans in agony."

    stop music fadeout 3.0

    play sound s_ahaa

    "He disappears into the night, and you hear the sound of a woman's heavy breathing."

    you "What the hell! P-Princess???" with vpunch

    "You can't see her, but the wound she suffered leaves you little hope."

    play music m_siege fadein 3.0

    scene bg fire outside with flashbackout

    "You collapse as the world fades around you. Somewhere, voices shout. Soldiers. Knights."

    you "Kuro... Kurohime..."

    scene black with fade

    stop music fadeout 3.0

    "Everything goes black."

    scene black with Fade(0.5, 2.0, 0.5)
    show bg cell at top with dissolve

    "When you finally wake up, you're behind bars."

    play music m_tavern fadein 3.0
    play sound s_creak

    "Before you can move, someone approaches."

    show knight with dissolve

    knight "Get up. You're free to go."

    you "What?"

    knight "The Princess vouched for you. I was just waiting for you to wake up, so that I could let you go."

    you "The Princess? She's alive? How?" with vpunch

    knight "We don't know. She was in a bad way when we found you."

    if _continue:
        $ story_flags["c3 ending"] = "mask defeat"

        "Pain wracks your body as you stand. Your wound has been crudely bandaged, but your whole body hurts like hell."

        $ MC.wound(3, 7)

    else:
        $ story_flags["c3 ending"] = "homura defeat"

        you "You found me?"

        knight "Yup. Some blue-haired wench with funny ears was spotted trying to drag you through the back alley. She bolted, leaving you lying in the dust."

        $ MC.wound(2, 7)
        knight "You were wounded, but alive."

        you "Suzume... Grrr."


    if not NPC_kenshin.flags["dead"]:
        $ NPC_kenshin.flags["dead"] = "c3 ending"

    you "T-The Princess is fine, then?"

    knight "Fine? No. She was badly hurt. The royal surgeon said she'll live, but she lost a lot of blood."

    $ NPC_kuro.flags["hurt"] = True

    knight "You're very lucky she survived, you know. We thought you were the attacker at first."
    
    knight "The King was going to have you quartered and hung by your bowels, first thing in the morning."

    you "*gulp*"

    knight "The Princess was looking for you after she woke, but she was in no shape to talk to anyone. She must rest."

    you "What will happen now?"

    knight "The princess is in no shape to tend to her duties. It will be months before she can leave her bedside."

    stop music fadeout 3.0
    
    knight "Dark days are about to come..."

    you "..."

    scene black with fade
    play sound s_close

    "Eager to escape this place, you part with the knight and head out."

    "You were hoping to catch a breather, but something foul is in the air. And it isn't just the dungeon's stench."

    $ calendar.set_alarm(calendar.time + 3, StoryEvent(label = "c3_ending", type = "morning"))

    return

# Final confrontation side events #

label c3_ninja_showdown(pics, lines):

    show speed_effect with dissolve

    if len(pics) >= 3:
        show bg showdown all with dissolve:
            zoom 1.25
            xanchor 0.5
            linear 8.0 xanchor -1.0

    elif len(pics) == 2:

        show expression pics[0]:
            xanchor 1.0
            xpos 0.0
            yalign 1.0
            linear 8.0 xanchor -1.0

        show expression pics[1]:
            xanchor 0.0
            xpos 1.0
            yalign 0.0
            linear 8.0 xanchor 2.0

    else:
        show expression pics[0]:
            xanchor 1.0
            xpos 0.0
            yalign 0.5
            linear 8.0 xanchor -1.0

    python:
        for p in pics:
            unlock_pic(p)

    while lines:
        $ _char, _line = lines.pop(0)

        $ renpy.say(_char, _line, _with=vpunch)

    return

label c3_arios_vision(): # Called from within Phase III

    play music m_mizuki fadein 3.0

    "Sweat blurs your vision. You jump with fear as something moves in the fire in front of you, right where the flames are the thickest."

    play sound s_mystery

    "Voice" "[MC.name]..."

    you "W-Who?"

    play sound s_fire

    "Booming voice" "[MC.name]!!!" with vpunch

    "In awe, you see a shape form out of the fire itself, until it coalesces to form a towering creature."

    if MC.get_alignment() in ("good", "neutral"):

        show bg arios at top with burn_it
        play sound s_fire

        "Commanding voice" "Come, Son, I beseech you."

        "A fire elemental stands before you, taller than the mightiest ogre. Liquid fire seeps through his many wounds, as if it was fiery blood."

        "But you know that these gaping wounds do not make him weaker. Instead, they burn with the inexhaustible fire of Bravery and Truth."

        "For even though you have never met this creature, you have seen its depiction in scripture numerous times, and its likeness in temples and churches."

        play sound s_stone

        "Before you stands the Lightbringer, mighty Avatar of Arios."

    else:
        show bg arios_evil at top with burn_it
        play sound s_fire

        "Hellfire voice" "Bow before Me, mortal..."

        "A fiery beast stands before you, a mess of hound heads, horns and claws."

        "Its cruel, supernatural gaze pierces your soul. You fall on your knees."

        "For while its sudden appearance had shaken you to the core, the beast is in no way unknown to you."

        play sound s_roar

        "You have seen numerous popular depictions of the beast. Before you stands Cerberus, mighty Avatar of Arios."

    "Sheltering your eyes with your hand, you answer its call with a broken voice."

    you "Lord Arios?"

    "Arios" "Listen, my follower, for we have little time."

    "Arios" "My Shield has broken. Impious beasts covet the Jewel of My Crown."

    you "Your shield? Your crown?"

    "The words sound familar, but your soul is too overwhelmed by the crushing power of the apparition to make sense of them."

    "Arios" "A Champion will rise tonight, another will fall. It does not matter which: the Balance is already broken."

    "Arios" "Before the Light Festival, it befalls to you to right the Balance of fire and steel."

    you "M-Me? H-How?"

    "Arios" "When the time comes, you will know. Remember My words: fire brings purity. Scorched earth will yet bear the best fruit."

    you "Fire brings purity... Scorched earth..."

    "Arios" "Heed my words. Your choice will seal the fate of Zan forever."

    if MC.get_alignment() in ("good", "neutral"):
        play sound s_stone
        "Arios" "If your heart is true, you may yet protect this city and the faithful in it. *rumble*"

    else:
        play sound s_roar
        "Arios" "Righteous fire may yet claim this city. And you can be the one fanning the flames of a glorious sacrifice... *hiss*"

    you "Lord Arios."

    "Arios" "But the choice will be yours only. Answer me, child."

    "Arios" "Do you intend to save Zan, or let it be consumed fow a new dawn?"

    menu:
        extend ""

        "I will save it":
            $ MC.good += 5
            $ story_flags["arios choice"] = "save"

            you "Even though I am a foreigner, this city and its people gave me a new start."

            you "I will lend my strength to their aid."

            "Arios" "So be it. Let the Light guide your hand in this choice."

        "I will destroy it":
            $ MC.evil += 5
            $ story_flags["arios choice"] = "destroy"

            you "This wretched place is crumbling under the weight of its own filth and lucre. There is no saving it."

            you "I shall bring my own match to the powder keg."

            "Arios" "So be it. Let the Fire purify all so you can start anew."

        "I haven't made up my mind":
            $ MC.neutral += 5

            you "I don't understand enough about the situation to decide yet."

            you "I'm still weighing my options."

            "Arios" "Do not wait too long to make up your mind, lest you too become fuel for the pyre."

    play sound s_fire

    show bg mansion fire at top with flash
    stop music fadeout 3.0

    "The God vanishes in a puff of embers and smoke. As quickly as it appeared, the vision is gone. You are left utterly confused."

    you "What does Arios want me to do? What was it about the Shield, the Crown Jewel, and the Champion? What must happen at the Light Festival?"

    return

label c3_homura_with_shiro(): # Called from Phase 0

    scene black with fade

    play sound s_screams
    homura sepia "Oh! Ah! Aaaaah!!!" with vpunch

    show bg homura_tryst1 at sepia with dissolve

    "Soon after the wounded warrior woke from his injuries, he threw himself at Homura, shoving her clothing aside."

    show bg homura_tryst1 at top_color with dissolve

    play sound s_moans

    homura ninja "W-What are we doing... Aaaah!"

    "Still under the adrenaline rush from the fight, they soon found themselves in the throes of passion."

    show bg homura_tryst2 at top with dissolve

    homura "Oh, yes... Fuck me..." with vpunch

    "Without a word, Shirohito was pouncing her drenched pussy, lifting her small butt in the air as he went. She crossed her legs around him."

    show bg homura_tryst3 at top with dissolve

    homura "(He's so strong... And yet...) *moan*" with vpunch

    homura "(This is wild... We just met... I don't even know his name...)"

    "Shirohito" "Brace yourself. I'm gonna cum..."

    show bg homura_tryst2 at top with dissolve

    homura "What? A-Already?" with vpunch

    "Shirohito" "Shut up, and take it..."

    play sound s_scream_loud

    show bg homura_tryst4 at top with flash
    homura "Aaaaah!!!!" with vpunch

    play sound s_orgasm_fast
    with doubleflash

    "Shirohito came deep inside her pussy. It was a quickie, but it made her head spin."

    with fade

    "They were both panting, and Homura's head was spinning."

    "It was the beginning of something more."

    show bg homura_tryst4 at sepia with dissolve

    homura ninja "I soon realized that Shiro was a man to take what he wanted."

    homura "And I also found that... Maybe I liked it that way."

    return

# Homura's Fate #

label c3_homura_capture():

    scene black with fade

    "It is time to visit your latest prisoner."

    play music m_suspense fadein 3.0

    show bg homura_capture1 at top with dissolve

    homura ninja "..."

    "She barely seems aware of your presence at first, but her ninja senses kick in, and she wakes up with a start."

    show bg homura_capture2 at top with dissolve

    homura "What the... [MC.name]! Where am I?!?"

    you "Hello, Homura."

    homura "And where is Shiro!!!"

    if story_flags["c3 ending"] == "victory":

        you "He escaped, but I expect he's going to take a while to recover from his injuries."

    else:
        you "To tell you the truth, I don't know what happened to him."

        you "He got to the princess, and then everything went dark..."

        you "But I think he got hurt. Bad."

    homura "Grr..."

    "Her anger flares, but quickly breaks down."

    homura "At least... At least he's alive."

    "She takes a moment to focus back on her current predicament."

    if NPC_homura.love >= 5:

        show bg homura_capture1 at top with dissolve

        homura "Do you really have to keep me tied up like this? I thought we were friends..."

        you "Call it a precautionary measure..."

        homura "What... What do you have in store for me? *shiver*"

    else:
        homura "Why don't you let me go, so we can settle this debt one on one? *venomous*"

        you "Fufufu... This is not the kind of 'one on one' you're going to get."

        homura "W-What do you mean? *nervous*"

    stop music fadeout 3.0

label c3_homura_capture_menu():

    $ played = False

    menu:
        "What will you do with Homura?"

        _("Surrender her to the law"):

            you "After the little show you've pulled off, half the Realm is looking for you."

            you "I will get a nice price for your ass, figuratively speaking. A rare case for me."

            homura "No!!! They'll torture me, and then they'll execute me in the worst fashion!"

            homura "Please, have mercy [MC.name]! anything but that!"

            menu:
                _("Proceed"):                    you "Well, maybe you should have thought of that before crossing Her Majesty."
                    
                    you "Or crossing {b}me{/b}." with vpunch

                    $ unlock_achievement("homura arrested")
                    $ NPC_homura.flags["c3 path"] = "arrested"

                    scene black with fade

                    "Knights came by and took Homura into their custody. She was never to be seen again."


                    $ MC.change_gold(3000)
                    call receive_item(rep_item) from _call_receive_item_49
                    $ norollback()

                    "You were given a fat purse for your efforts, as well as a commendation."

                "Reconsider":
                    you "Hmmph."

                    jump c3_homura_capture_menu

        "Make her work for you":
            you "You're going to work for me."

            homura "F-For you... You mean?"

            you "That's right. No more skulking in the dark, killing or magicking your way around."

            you "Just good, honest cock-sucking and whoring, taking dicks for your next meal."

            if NPC_homura.love >= 10:
                homura "..."

                homura "I betrayed you... I fought you, and lost..."

                homura "You have every right to hate me. I deserve to atone for my sins."

                "She looks at you, with a mix of weariness and resolve."

                homura "Very well. I'll work for you. If only to regain a modicum of your friendship."

                you "That's what I like to hear."

                $ girl = create_girl("Homura Henso", force_original=True, level=10)
                $ girl.pop_virginity("other")
                $ girl.love = 50
                $ unlock_achievement("homura love")

                call acquire_ninja(girl) from _call_acquire_ninja_4

            else:
                homura "W-Whoring? Me??? Are you mad!?!" with vpunch

                you "What, you think you have a choice? *grin*"

                homura "I won't! I'll slice your throat in your sleep! I'll..."

                you "You're only saying that because you weren't given proper motivation yet..."

                you "Say hello to my little friend... *wink*"

                you "..."

                you "My little friend... *cough*"

                homura "What? Your weapon? Your penis?"

                you "No! Gizel, will you..." with vpunch

                "Gizel steps out from behind a pillar, a smug look on her face."

                you "You took your sweet time..."

                gizel "Oh, did I now? Sorry, I wasn't paying attention."

                gizel "(I did it on purpose to spoil his fun, fufufufu...)"

                you "I heard that."

                "Meanwhile, Homura is giving you both a puzzled look."

                homura "Who is she? Another one of your slaves?"

                gizel upset "Silence, whore!" with vpunch

                "Homura senses the menace oozing off from the diminutive Elven woman."

                you "Gizel, take her off to the farm, will you?"

                homura "The farm? What is that? I-I don't want to..."

                gizel "Silence, I said!"

                play sound s_punch

                "Gizel's whip cracks, inches from Homura's face."

                scene black with fade

                "Homura was taken off to the farm, for 'training'."

                $ story_add_event("homura_farm", "daily")

        "Play with her first" if not played:
            you "Before I decide what to do with you, I need to relieve some of the tension between us..."

            play sound s_dress

            "You unbuckle your pants."

            show bg homura_capture2 at top with dissolve

            homura "W-Wait!!! What do you think you're doing?"

            homura "Don't touch me!" with vpunch

            "You look at her with a grin."

            you "Don't touch you? Fine, then.Have it your way..."

            "She watches in horror as you start masturbating in front of her."
            
            "*flick* *flick*"

            "Until..."

            show bg homura_capture3 at top with flash

            homura "!!!"

            with doubleflash

            you "UGGGH!"

            homura "EW!!!" with vpunch

            if NPC_homura.love >= 8:
                show bg homura_capture4 at top with dissolve

                homura "I-It smells... *blush*"

                "Her embarrassment seems mixed with something else."

                homura "I... I suppose I had it coming. For betraying you..."

                you "Well, you certainly had {i}me{/i} coming. *mean laugh*"

            else:
                homura "Y-You bastard..."

                you "You betray me, you pay the price. This is just a 'taste' of things to come."

                homura "Grrr..."

            homura "M-My clothes..."

            you "Oh, right. Let me help you out of them, then... *grin*"

            play sound s_dress
            scene black with fade

            play sound s_scream
            homura naked "S-Stop!!!" with vpunch

            "*SPURT* *SPURT*"

            show bg homura_capture5 at top with flash

            "You spend some time with Homura. In the end she doesn't resist anymore, and you are finally satisfied."

            $ NPC_homura.love -= 2
            $ played = True
            $ unlock_achievement("homura shower")

            jump c3_homura_capture_menu

        "Let her go":
            you "I'm going to give you a single chance to get out of my sight, once and for all."

            you "Go back to your volcano lair, or wherever. Never come back to Zan, and don't try and contact your accomplice."

            you "He doesn't care for you anyway..."

            homura "That much is clear... *sigh*"

            homura "I accept, of course. I will leave and never come back. You have my word."

            you "Very well. Go."

            scene black with fade

            "Your security walks her to the edge of town, wearing only the ripped clothes on her back."

            "As she leaves, she turns, as if about to say something to you. {nw}"

            if played:
                "But her face hardens."

            else:
                "She seems about thank you. Yet-"

            "No words pass her mouth. Your men shove her forward, and she disappears from your sight, probably forever."

            $ NPC_homura.flags["c3 path"] = "freed"

    return

label homura_farm(): # Runs daily. An event every 3 days.

    if not NPC_homura.flags["farm counter"]:
        $ NPC_homura.flags["farm counter"] = 1
    else:
        $ NPC_homura.flags["farm counter"] += 1

    $ norollback()

    # 1. humiliation
    if NPC_homura.flags["farm counter"] == 3:
        play sound s_rooster

        show bg farm at top with dissolve

        "Meanwhile, at the farm..."

        show bg homura_farm1 at top with dissolve

        play sound s_punch
        pause 0.3
        play sound2 s_punch

        "*WHIP* *WHIP*" with vpunch

        play sound s_screams

        homura ninja "OW! OUCH! AW!!!" with vpunch

        gizel angry "You impudent whelp!!! If your empty head can't understand respect, your plump ass will!!!"

        play sound s_punch

        "*WHIP*" with vpunch

        "The beatings will continue until libido improves..."

    # 2. dawg
    if NPC_homura.flags["farm counter"] == 6:

        play sound s_moo
        show bg farm at top with dissolve
        "Meanwhile, at the farm..."

        show bg homura_farm1 at top with dissolve

        "Homura has been left hanging in the same painful position for days, starving and exhausted."

        gizel smirk "And how is my little pensioner faring? I hope you're ready for today's training session?"

        homura ninja "P-Please... No more beating... S-Stop..."

        gizel "So you're finally ready for the next stage of your training. Good."

        play sound s_whistle

        gizel "*Whistle*"

        "A dark, furry shape leaps out from behind the bushes."

        homura "Uh? What-"

        show bg homura_farm2 at top with dissolve

        play sound s_scream_loud

        homura "AAAAAH!!!" with vpunch

        gizel "Nice... Good doggie."

        "One of the hounds from the farm's stables has come, eager to mate with the hapless girl."

        gizel "How is your first time taking a dog's dick? What best to put an arrogant bitch in her place?"

        play sound s_scream

        homura "OH!!! AAAAH!!! It hurts-" with vpunch

        gizel "You'll get used to it in no time. Besides, he's almost finished."

        play sound s_splat
        show bg homura_farm3 at top with flash

        "*SPURT*"

        with doubleflash

        "The dog cums inside Homura's clenched pussy, filling her insides with dirty spunk."

        show bg homura_farm4 at top with flash

        homura "Aaaw..."

        "Tears flow from Homura's eyes. She cannot believe what just happened."

        gizel "How did you like it? We started small with the doggie, but don't worry, I'll introduce the whole menagery to you... Aren't you a luck girl!"

    # 3. big dawg
    if NPC_homura.flags["farm counter"] == 9:

        play sound s_wolf
        show bg farm at top with dissolve
        "Meanwhile, at the farm..."

        show bg homura_farm4 at top with dissolve

        gizel smirk "Fufufu... I see that you have become well acquainted with our little furry friends here at the farm."

        homura ninja "S-Stop... It's disgusting..."

        gizel "Well, good news, you are getting upgraded! Let me introduce you to 'The Beast'"

        play sound s_roar

        "The Beast" "*GROAR*" with vpunch

        homura "N-No!!! What is this???"

        gizel "It's time to stop playing around with the pups!"

        gizel "Have you ever heard of direwolves? *smirk*"

        "A massive, shaggy beast emerges from the forest, his yellow, inhuman eyes flaring when they spot Homura." 

        homura "Direwolf? What the-"

        show bg homura_farm5 at top with dissolve

        play sound s_scream_loud

        homura "AAAARHH!!!" with vpunch

        "The monster penetrates Homura, painfully stretching her tiny pussy as his massive cock forces its way in."

        play sound s_evil_laugh

        gizel "Look at that bulge under your tummy! The Beast is really messing with your innards... Muahaha!"

        homura "S-Stop!!! The p-pain..." with vpunch

        play sound s_wolf
        "The Beast" "*HOWL*" with vpunch

        "The monster keeps fucking Homura mercilessly, shaking her like a ragdoll. Her mind shuts down, her body hanging on for dear life."

        play sound s_roar

        "The Beast" "*GRRRRR*" with vpunch

        "Eventually, Homura goes numb, accepting her fate. Her womb relaxes and the Beast is able to fuck her even deeper, finally blowing its load with a furious growl."

        show bg homura_farm6 at top with flash

        "*SPURT* *SPURT*"

        with doubleflash

        play sound s_scream

        homura "Aah!!! It's filling me up! I'm going to tear up!!!"

        "Her voice is weak as she takes that final abuse, her body not resisting as if she had resigned to her fate."

        homura "S-So much... S-So big... I'm... I'm..."

        "Homura's mind seems halfway gone. Gizel gives her a cruel smile."

        gizel "You will be ready soon, sister... But we'll take the next few days to get you more acquainted with the Beast. Fufufu..."

        play sound s_surprise

        homura "M-More??? *wide eyes*"

        play sound s_evil_laugh
        scene black with fade

        "Gizel's cruel laugh echoes through the farm."

    # 4. group
    if NPC_homura.flags["farm counter"] == 12:

        play sound s_rooster
        show bg farm at top with dissolve
        "Meanwhile, at the farm..."

        play sound s_scream

        show bg homura_group1 at top with dissolve

        "One of the stallion is busy fucking Homura, making her bounce up and down his thick cock."

        play sound s_aaah

        homura ninja "Ooooh, aah, aaah!!!" with vpunch

        "After practicing with the direwolf though, this is nothing she can't handle."

        gizel smirk "Fufufu, this shit is too easy for you. Get in here, boys! Let's make it interesting."

        show bg homura_group2 at top with dissolve

        play sound s_surprise

        homura "*NGGH!!!*" with vpunch

        "A group of men show up, eager to join the party."

        play sound s_mmmh

        homura "*NGGH*... *MMMH*..." with vpunch

        "One of the men forces his way inside Homura's mouth, while another one pushes his cock inside her tight asshole."
        
        "The others take turns fondling her and forcing her to jerk them off."

        play sound s_sucking

        "After everything that's happened to her, Homura is not even shocked. She simply does her best to keep up with the men's pace, hoping to get finished quickly."

        "They keep going for a while, and Homura endures, her stamina hardened by Gizel's harsh training. She clenches her lower muscles around the men's cocks."

        "Brute" "RGHHH..." with vpunch

        show bg homura_group3 at top with flash

        "The big man unloads first, shooting a big load inside her waiting pussy."

        with flash

        "She doesn't skip a beat, keeping up the stimulation to bring the others over the edge."

        man "GWAAAH!!" with flash

        show bg homura_group4 at top with doubleflash

        "Cum fills her mouth, and she swallows as much as possible to keep breathing as she clenches her asshole tight, getting another load of semen in the back for her efforts."

        with flash

        "Groaning, the other men do not take a long time cumming, until Homura is left panting in a thick layer of stinky cum."

        gizel "Well done, sister... You're a fast learner. Hmmm... I envy you."

    # 5. MC visit
    if NPC_homura.flags["farm counter"] == 14:

        play sound s_moo
        show bg farm at top with dissolve

        "Today, Gizel sent for you. She said she had a nice surprise."

        show gizel at left with dissolve

        show homura ninja at totheright with dissolve

        gizel "Here she is, [MC.name]. Your very own obedient slave ninja bitch."

        homura "Hello, Master."

        "You eye Homura suspiciously, afraid she might pull one of her old tricks."

        play sound s_mmh

        homura "I am yours to command..."

        "She looks like herself, but her manner is completely changed. She does seem genuinely tamed."

        gizel "She's among my best work, if I may say so myself. Would you like to give her a try?"

        homura "..."

        gizel "Homura?"

        homura "Lead the way, Master. I am ready to go."

        you "Ready to go where?"

        homura "To your bedroom, or wherever you may see fit..."

        you "A room? Bullshit! I'm going to test you right here and now."

        scene black with fade

        play sound s_dress

        pause 0.3

        play sound2 s_surprise

        show bg homura_grass1 with dissolve

        homura "Oh!"

        you "Nice, your pussy is already wet... I see Gizel taught you well."

        you "And your beautiful round tits are perfect... I really want to lick them... *slurp*"

        play sound s_aah

        homura naked "Aaah!!" with vpunch

        homura naked "Th-... Thank you, Master."

        play sound s_sucking

        "You keep sucking on her nipples, which grow hard into your mouth."

        homura "W-Would you please..."

        you "What?"

        homura "Would you please... Fuck my nasty pussy... Master [MC.name]."

        you "Oh my... You really turned into a full-on slut."

        homura "S-Sorry..."

        you "Very well. I'll indulge you."

        play sound s_ahaa

        show bg homura_grass2 with dissolve

        "*SCHLIP*" with vpunch

        "You slip inside her, nice and easy."

        "In spite of her harsh treatment at the hands of Gizel, her body is still strong. She clenches around your cock in a pleasant manner as you push deeper."

        play sound s_splat

        "*SPLUSH*" with vpunch

        show bg homura_grass3 with dissolve

        play sound s_aaah

        homura "AAAAH!!!" with vpunch

        play sound s_moans

        "You fuck her faster, pinning her thighs in place. She moans suggestively."
        
        homura "Hmm, aaah..." with vpunch

        "Her moans do not sound fake. She looks at you with dreamy eyes."

        homura "M-Master... More!" with vpunch

        "Her request is blunt and sincere, and you are in no mood to object."

        you "Oh you dirty slut... A woman after my own heart."

        play sound s_mmmh

        homura "Oh, mmmh..."

        "You fuck her harder and harder, and she tightens her pussy walls around you, until you are both ready to go."

        you "NGGGH..." with vpunch

        play sound s_aaah

        homura "Aaaah..." with vpunch

        play sound s_orgasm_fast
        show bg homura_grass4 with flash

        "Release overwhelms you both as you finally cum inside her drenched pussy."

        with doubleflash

        "She follows, her body shaking in orgasm as you shove your cock in one last time."

        scene black with fade
        show bg farm at top with dissolve

        gizel "So. What did I tell you?"

        you "Congratulations on a job well done. I'm taking her."

        # Remove event from queue
        $ story_remove_event("homura_farm", "daily")
        $ unlock_achievement("homura farm")
        $ norollback()

        "You arrange for Homura to be brought to [brothel.name]."

        $ girl = create_girl("Homura Henso", force_original=True, level=10)
        $ girl.pop_virginity("other")
        $ girl.fear = 50

        call acquire_ninja(girl) from _call_acquire_ninja_5

    return

label shiro_homura_rumor():

    scene black with fade

    play music m_mafia fadein 3.0

    "A few weeks have passed since the battle in Kosmo's mansion. You start hearing some disturbing rumors."

    show bg mask duo at top with burn_it

    "A couple of assassins are roaming the countryside, ambushing caravans and ransacking villages that are loyal to the Crown."

    "Their depiction match that of Homura and Prince Shirohito, and they only grow more shameless and violent with time."

    "It is only a matter of time before they try to finish what they started."

    hide bg with burn_it
    stop music fadeout 3.0

    return


label c3_ending(): # Happens three days after the final battle

    show expression bg_bro at top
    with dissolve

    play music m_gio fadein 3.0

    "This morning, you receive an unexpected visit at the brothel."

    play sound s_surprise

    ev_girl1 "Aaah!!!"

    play sound s_scream

    ev_girl2 "Eeek!" with vpunch

    play sound s_shatter

    sill sad "S-Stop!!! Get your hand off my butt!!!" with vpunch

    "You look for the source of this commotion."

    scene black with fade
    show bg tavern at top with dissolve 

    show gio with dissolve

    gio "Heeeeey!!! If it isn't my old buddy, [MC.name]!"

    you "Gio... You're back. Yay."

    gio "I had an awesome vacation in Borgo, my friend! The girls there..."
    
    gio "I went to a ping-pong tournament, and you won't believe what-"

    you "Shut up, Gio!" with vpunch
    
    you "A lot has happened while you were in hiding! We were attacked! I almost died, and-"

    gio "Yes, yes, I heard all about it from the princess. *puff on his cigar*"

    you "The princess? Is she okay?"

    if NPC_kuro.flags["hurt"]:
        gio "Well, to tell you the truth, no."

        gio "Her wound was bad, but not lethal. She's recovering."

        gio "But her spirit, though... It's like her soul was hurt worse than her body."

        you "What do you mean?"

    else:
        gio "Yes, and I understand you played no small part in saving her. Well done."

        gio "But she's in a foul mood..."

        you "Why?"

    gio "Well, maybe it's the whole 'I have a secret twin and he wants to murder me' thing."

    if NPC_kenshin.flags["dead"]:
        gio "And it doesn't help that her most loyal knight died a tragic death."

    "You have to hand it to the old rogue, his intel is always up to date."

    gio "Anyway, you'll see for yourself. She asked me to call you to the Palace, discreetly."

    you "And here I thought I was done with these palace summons."

    gio "Rejoice, you're still popular. As for me... I guess I'll just wait for you here."

    hide gio with dissolve

    gio "Come here, you little mouse!"

    play sound s_shatter

    sill sad "EEEEK!!!" with vpunch

    scene black with fade

    play music m_palace fadein 3.0

    show bg castle at top with dissolve

    "As you approach the Palace, escorted by a small group of knights, you can feel the atmosphere is thick with tension."

    "Men-at-arms run from one building to the next, carrying orders and supplies. Something stirred the hornet's nest."

    show bg palace room at top with fade

    "When you finally get to the Princess's chambers, you hold your breath."

    show kuro with dissolve

    if NPC_kuro.flags["hurt"]:
        "Kurohime is sitting on a throne that is more like a half-bed, wrapped in furs and surrounded by apothecaries and their remedies."

        "Her usually serene face is sometimes contorted by pain, and her eyes look distant and aloof."

        kuro "[MC.name]... I... Wanted to see you."

        "She nods, and her servants leave the room."

        you "Your Majesty... Are you alright?"

        "Before she answers, she is seized by a coughing fit, and leaves a crimson-tainted handkerchief by her bedside."

        kuro "No, [MC.name], I am far from alright... But I'll live."

    else:
        "You are relieved to see Kurohime in good health. Nevertheless, she is seething with frustration."

        kuro "Ah! [MC.name], come see me! Finally, someone who is not utterly incompetent."

        "She waves her entourage away with a casual gesture."

        you "My Lady."

    kuro "We must speak of my brother's treachery."

    you "So... The masked murderer truly is your brother, then? You don't think he's lying?"

    kuro "He's a despicable, wretched coward who belongs on the gallows. But no, I don't think he's lying."

    kuro "I've always known I had a twin brother. But I was told he died shortly after our birth."

    kuro "Over the years, though, I picked up some bits and pieces that didn't fit. How Uesugi's father suddenly disappeared. Or the way my mother became disconsolate when we heard of his death, to the point many believed the old Knight Commander was her lover..."

    kuro "And... I know enough about secrets to sniff one my own {i}father{/i} has been hiding from me."

    "Her tone is dripping with contempt."

    if NPC_kuro.flags["hurt"]:
        "She is stopped in her track by another bloody coughing fit."

        kuro "I find out I have a brother, and he immediately tries to kill me..."

        you "What happened back there? I couldn't help you, and I thought you would die for sure..."

        kuro "I don't know myself what happened... I felt the steel bite in my chest, but then..."

        stop music fadeout 3.0

        play sound s_mystery

        scene black with fade
        show bg mansion fire at top with burn_it

        kuro "It felt like time stopped. My body was hot from the fire, and cold where the blade had struck."

        show mask attack with dissolve

        kuro "But the strangest thing was, I could see myself through his eyes, too."

        kuro "It's like we were connected through his sword. His thoughts and horror mirrored mine."

        play music m_demons fadein 3.0

        kuro "But... We were not alone."

        you "Not alone?"

        kuro "There was a dark force lurking behind him, I could feel its hunger... Thirsting for blood, my blood... And even my soul..."

        you "What?"

        kuro "But then, something arose from deep within me. A wrathful being of fire and crimson. Through my brother's eyes, I could see it rise where I stood."

        kuro "The spirits fought with fury, like a hot and cold wave clashing."
        
        stop music fadeout 3.0
        play sound s_fire
        with flash

        kuro "But eventually, mine won, and the dark force retreated, hissing in anger."

        kuro "It was over in a fleeting moment, but for me it felt like I had been trapped in there for an eternity, suffocating, drowning in my own blood."
        
        kuro "The blade withdrew my chest, and I could finally breathe."


        show bg palace room at top 
        show kuro
        with burn_it

        you "So... You're saying a supernatural being of pure bright energy rose to your defense, and stayed the assassin's hand?"

        kuro "Yes."

        if MC.god == "Arios":
            you "It sounds like our Lord Arios was on your side, then, Light bless Him."

            kuro "I guess so..."

        else:
            you "Sounds like Arios-worshipper mumbo-jumbo to me..."

            kuro "Well, I survived, didn't I? I have no better explanation for you."

        kuro "This all ties in with the dark story I'm about to tell you..."

    else:
        kuro "There is more to this, though."

        you "What do you mean?"

        kuro "Do you remember that my spells couldn't harm him?"

        kuro "I harbor over half a dozen wards of protection, woven by the most gifted mages in the city."

        kuro "It should have been enough to stop him from lifting even a finger against me."

        if MC.playerclass == "Wizard":
            you "True. Even an archmage would have struggled."
        else:
            you "I don't know, magic is fickle..."

        kuro "When it all happened, I saw something."

        you "Saw something? What did you see?"

        kuro "The wounds he suffered should have been grievous, but he tapped into another power to shun them off."

        kuro "I only briefly saw it, but there was this dark shadow looming over him... Taller than a golem, hissing and waving like smoke wisps."

    you "What do you suggest?"

    kuro "Look, [MC.name]. There' something you must know about my family."

    you "Must I? I feel like I already know too much, Your Highness."

    kuro "Correct. That makes you an asset, but also a loose end. You're involved, whether you like it or not."

    kuro "Now, listen. It is a troubling story."

    stop music fadeout 3.0

    scene black
    show bg old_general at top
    with flashbackin

    kuro "Before my father conquered Zan and laid waste to the old regime's power structures, he was just a rebel commander leading a ragtag army."
    
    kuro "He got caught by the loyalists at the foot of the Arik mountains, and was wounded in a terrible battle."
    
    kuro "He ended up cornered in the valley below, and would have perished with his army if he didn't lead a daring escape across the mountains."

    kuro "This is now the stuff of legend, and everyone knows of his 'Long March'. Crossing the Arik mountains in the heart of winter was supposed to be an impossible task, and he was wounded to boot."
    
    kuro "Nevertheless, he did cross them, and was able to take Zan by storm, undefended, when spring came."

    show bg palace room at top 
    show kuro
    with flashbackout

    kuro "This tale I often heard as a child. While it was a staple of official propaganda, I also heard it told by actual veterans of the long march."

    kuro "But there is a darker tale. Of {i}how{/i} he survived out there in the mountains."
    
    kuro "It was only spoken of in hushed tones. Getting caught telling it was liable to land one in jail, or worse."

    kuro "Nevertheless, I heard this story, even when I wasn't meant to. It was told behind closed doors, it even became a kind of folk's tale; some of the political factions that opposed my father made sure it could spread."

    kuro "I heard variations of this tale as horror stories, jokes, drunk late-night confessions or parables, but the key points remain the same."

    you "Tell me then."

    kuro "When my father started his ascent of the Arik mountains' highest peak, Mount Kumo, he was famished and had lost a lot of blood."

    you "Mount Kumo... I've heard tales about it. They say even mountain goats fall to their death on its treacherous paths."

    kuro "He would never have made it, if he hadn't run into an ancient cave..."

    play music m_suspense fadein 3.0
    scene black
    show bg cave entrance at top
    with flashbackin

    kuro "My father took his army forward into the darkness, confident that they would find a way to the other side."

    kuro "More than one soldier in his army thought him mad. There were desertions and mutiny, he had the leaders put to the sword."

    show bg cave at top with dissolve

    kuro "Going down, they found the half-buried corridors of an old structure. Cimerian-made. But even that was built upon the ruins of something much older..."

    kuro "After a week, they were utterly lost in the darkness. Running on empty bellies, my father's men didn't even have the nerves to rebel anymore."

    kuro "It is there, in the darkness, where my father saw a single flicker of light. A single candelabra was burning at the center of a gigantic stone hall, without a soul around to maintain it."

    kuro "Something overtook my father's mind, and he kneeled by the flame to pray and made a pledge."

    kuro "A day later, he and his army came out of the cave on the other side of Mount Kumo, unharmed."

    show bg palace room at top 
    show kuro
    with flashbackout

    kuro "Only half his men made it out alive of the dark cave. But the survivors would remain loyal to the last."

    you "What happened down there?"

    kuro "They said he made a pact with a spirit from the gaping abyss below Mount Kumo. A spirit older than the mountain itself."
    
    kuro "It was there when the Goliaths were roaming Xeros and sentient species were just cattle."

    you "A spirit?"

    kuro "Not just any wild spirit. From its depiction, I gather that it might have been a creature scholars refer to as... An Archdemon."

    you "What? Your father made a pact with an Archdemon?"

    kuro "So the story says. A blood pact."

    if MC.playerclass == "Warrior":
        you "Nothing good can come of meddling with such evil spirits!"

        kuro "And yet some good came of it, at first."

    elif MC.playerclass == "Wizard":
        you "A blood pact requires a sacrifice in blood or kin. The greater the spirit, the higher the cost."

        kuro "Precisely."

    elif MC.playerclass == "Trader":
        you "Gambling with the devil... I like it! Your father is a bold man."

        kuro "Was. He's but a shade of his former self."

    you "What were the terms of their deal?"

    kuro "There are variations, but most forms of the tale say this: my father requested safe passage for his troops and himself, and power. The power that would make him a King."

    you "Well, it seems he got his end of the bargain... What did the spirit want in exchange?"

    kuro "In exchange..."

    play sound s_gust
    with flash

    "It may be your imagination, but suddenly the lights dim, and all the room's candles flicker without a modicum of wind."

    kuro "He pledged to give his firstborn son over to the dark spirit."

    you "His firstborn son???" with vpunch

    kuro "Yes. He would give his firstborn to a soul-devouring demon, in exchange for a taste of absolute power."

    "You shiver. Kurohime seems unphased, but you can feel the turmoil under the surface as she utters these words."

    you "Do... Do you believe this?"

    kuro "'Not at all'... Would have been my answer, only a few days ago."

    kuro "After all, he didn't have a living son. Or so I thought."

    kuro "But then, I met my brother. And now I have to see all of my father's actions in a new light."

    you "You... You don't think your brother is harboring a demon, do you?"

    kuro "No! I mean... I hope not."

    kuro "But if he was 'pledged' to the evil spirit of Mount Kumo, whatever that means, it might be the reason why demons are so interested in him."

    kuro "I think his fate is linked to the Archdemon... And mine."

    stop music fadeout 3.0

    you "Your Majesty, uhm... Why are you telling me all of this?"

    kuro "Well, [MC.name]. You harbor knowledge about state affairs that only a handful of people in the Realm are privy to."

    kuro "So now, I have to make a choice: turn you into my confidant... Or have you killed."

    kuro "I've decided that I prefer the first option."

    you "As do I. *gulp*"

    kuro "Good. In part, it's because I need you to help me get to the bottom of this. There are not many people I can trust with this kind of information, or that would believe it."

    kuro "But there is something else."

    kuro "You see, [MC.name], ever since we met-"

    play sound s_crash

    guard "GIVE WAY!!! GIVE WAY!!!" with vpunch

    play music m_danger fadein 3.0

    "You hear a commotion outside, and the doors blast open."

    "Royal Guards pour into the room, bringing a single man forward."

    show kuro at left with move
    show lost_soldier at right with moveinright

    lost_soldier "P-Princess Kurohime..."

    "You wonder why the guards look so worried. The man before you is rather pitiful, a boy really, his simple clothing torn and dusty."
    
    "He looks like he hasn't rested in days, and is about to collapse from exhaustion."

    kuro "Wait, I know you... Aren't you a knight?"

    you "(Wait, this wretch... a Knight?)"

    lost_soldier "N-No, you Highness, merely a squire... I was with the First Army."

    lost_soldier "I came straight from the Holy Lands. I rode for three nights and three days. It killed my horse."

    kuro "Speak, Squire. What' wa's so important that you would come and disturb me at this hour?"

    lost_soldier "Your Majesty..."

    "His voice breaks."

    lost_soldier "All is lost. The beast people ambushed our army at dusk, the troops are dead or routed."

    kuro "Curses!!! What is the High Priest's plan after this? Why did he send you to me?" with vpunch

    lost_soldier "The High Priest and the Lord Commander... They're dead."
    
    lost_soldier "I saw the madness with my own eyes. The trees came alive and crushed the High Priest to a bloody pulp. Their roots ripped the Lord Commander apart."

    kuro "Seven Hells!"

    lost_soldier "I had not yet donned my armor and I managed to flee, but none of the knights did. It was a massacre."

    kuro "But the First army is... Was... The bulk of our Force. The beast people now have a clear way to the city. They could storm the walls within a fortnight."

    lost_soldier "Not even Arios could protect us... The beast people, they... They..."

    hide lost_soldier with dissolve
    play sound s_crash

    "The man faints, falling flat on his face. Kurohime doesn't notice, already lost in her thoughts."

    kuro "This is terrible news. When the citizens get word of this, as they inevitably will in the next hours, we'll have riots on our hands..."

    "She turns to you."

    kuro "Our conversation will have to wait, [MC.name]."

    "She looks about to add something, but surrounded as she is by her retinue, she stops in her tracks."

    kuro "You may go."

    scene black with fade
    show bg castle


    "As you leave the Palace, you hear a sound that makes your heart skip a bit."

    play sound s_bells

    "It's the city bells, all ringing at once."

    scene black with fade
    $ game.set_task(None, "story") # Lets you move on to the next chapter

    "War is coming to Zan."


    return


## End of c3's Conclusion ##

#### END OF CHAPTER 3 EVENTS ####


