#### BK Achievements ####

## How to add an achievement easily:
## Simple binary unlock (use level_cap to limit the max unlock level, optional):
# $ unlock_achievement(target, level_cap)

## Increment a counter:
## 1/ Declare the target in 'tracked_achievements' below
## 2/ Insert this in the relevant part of code:
# $ game.track(target, value)
# Note: The 'add_log' method of the Girl object does the same.

init python:
    def count_achievements(locked=False):
        if locked:
            return sum(a.level_nb*a.multi for a in achievement_list)
        else:
            return sum(a.level*a.multi for a in achievement_list)



    achievement_list = [
                        Achievement("Introduction: Brothel Management 101", "Watch the introduction.", pic="portrait.webp", pic_path="NPC/Sill/", target="intro"),

                        Achievement("New trainer: Maya", "You have unlocked Maya. She can improve your girls' defense.", pic="portrait.webp", pic_path="NPC/Maya/", target="trainer maya", multi=3),
                        Achievement("New trainer: Renza", "You have unlocked Renza. She can train your girls as thieves.", pic="portrait.webp", pic_path="NPC/Renza/", target="trainer renza", multi=3),
                        Achievement("New trainer: Satella", "You have unlocked Satella. She will strike fear into your girl's hearts.", pic="portrait.webp", pic_path="NPC/Satella/", target="trainer satella", multi=3),
                        Achievement("New trainer: Farah", "You have unlocked Farah. She trains the spicier sex acts.", pic="portrait.webp", pic_path="NPC/Captain/", target="trainer farah", multi=3),
                        Achievement("New trainer: Lydie", "You have unlocked Lydie. She can make your girls more obedient.", pic="portrait.webp", pic_path="NPC/Lieutenant/", target="trainer lydie", multi=3),
                        Achievement("New trainer: Stella", "You have unlocked Stella. She can boost your farm techniques.", pic="portrait.webp", pic_path="NPC/Stella/", target="trainer stella", multi=3),
                        Achievement("New trainer: Bast", "You have unlocked Bast. She can improve your resource collection.", pic="portrait.webp", pic_path="NPC/Bast/", target="trainer bast", multi=3),
                        Achievement("New trainer: Goldie", "You have unlocked Goldie. She can train your girls in softcore techniques.", pic="portrait.webp", pic_path="NPC/Goldie/", target="trainer goldie", multi=3),
                        Achievement("New trainer: Guild Woman", "You have unlocked the Guild Woman. She can shield part of your income from taxes.", pic="portrait.webp", pic_path="NPC/Taxgirl/", target="trainer taxgirl", multi=3),

                        Achievement("New merchant: Goldie", "You have unlocked the ranch, where Goldie sells beasts and related items.", pic="portrait.webp", pic_path="NPC/Goldie/", target="merchant goldie", multi=2),
                        Achievement("New merchant: Stella", "Stella sells stallions and related items, if you dare approach her.", pic="portrait.webp", pic_path="NPC/Stella/", target="merchant stella", multi=2),
                        Achievement("New merchant: Willow", "Willows sells monsters that she captures for a living, and related items.", pic="portrait.webp", pic_path="NPC/Willow/", target="merchant willow", multi=2),
                        Achievement("New merchant: Gina", "Gina the scientist sells mechanical gizmos, and studies flight.", pic="portrait.webp", pic_path="NPC/Gina/", target="merchant gina", multi=2),
                        Achievement("New merchant: Riche", "Riche sells flowers she picks at the botanical garden.", pic="portrait.webp", pic_path="NPC/Riche/", target="merchant riche", multi=4),
                        Achievement("New merchant: Katryn", "Katryn sells trinkets and has a short temper.", pic="portrait.webp", pic_path="NPC/Katryn/", target="merchant katryn", multi=4),
                        Achievement("New merchant: Gurigura", "Gurigura sells toys, food and supplies, when she doesn't get distracted.", pic="portrait.webp", pic_path="NPC/Gurigura/", target="merchant gurigura", multi=4),
                        Achievement("New merchant: Ramias", "Ramias sells weapons, and does not suffer fools and hagglers.", pic="portrait.webp", pic_path="NPC/Ramias/", target="merchant ramias", multi=4),
                        Achievement("New merchant: Gift shop", "The gift shop girl sells... Gifts. Duh.", pic="portrait.webp", pic_path="NPC/Gift girl/", target="merchant giftgirl", multi=4),
                        Achievement("New merchant: Twins", "Twins, Austin! Twins!", pic="body.webp", pic_path="NPC/Twins/", target="merchant twins", multi=4),

                        Achievement("Chapter 1: Gangbanger", "You helped a bunch of thugs fuck a helpless woman in the sewers.", pic="portrait naked.webp", pic_path="NPC/Sewer girl/", target="c1 gang", multi=2),
                        Achievement("Chapter 1: Friend Of Justice", "You have completed Chapter 1, and sided with Maya.", pic="portrait.webp", pic_path="NPC/Maya/", target="c1 good", multi=10),
                        Achievement("Chapter 1: Friend Of The Guild", "You have completed Chapter 1, and sided with Renza.", pic="portrait.webp", pic_path="NPC/Renza/", target="c1 neutral", multi=10),
                        Achievement("Chapter 1: Friend Of The Guard", "You have completed Chapter 1, and sided with the Captain.", pic="portrait.webp", pic_path="NPC/Captain/", target="c1 evil", multi=10),

                        Achievement("Chapter 2: The Hunt", "You have caught your first Kunoichi.", pic="kunoichi portrait.webp", pic_path="NPC/kunoichi/", target="c2 kunoichi", multi=4),
                        Achievement("Chapter 2: Painful Memories", "You have learnt about Haruka's traumatic past.", pic="portrait.webp", pic_path="NPC/kunoichi/haruka/", target="c2 haruka", multi=4),
                        Achievement("Chapter 2: The Onsen Ghost", "You have had a strange and arousing encounter in your onsen with Mizuki.", pic="portrait.webp", pic_path="NPC/kunoichi/mizuki/", target="c2 mizuki", multi=4),
                        Achievement("Chapter 2: The Naughty Schoolgirl", "You have peeped on Narika's secret intimate session.", pic="portrait.webp", pic_path="NPC/kunoichi/narika/", target="c2 narika", multi=4),

                        Achievement("Chapter 3: Take a hint", "You have obtained your first hint in the hunt for the mysterious Kunoichi.", pic="portrait doubt.webp", pic_path="NPC/suzume/", target="suzume hint", multi=5),
                        Achievement("Chapter 3: Light my Fire", "You have learnt the true identity of the mysterious Fire Kunoichi.", pic="portrait ninja.webp", pic_path="NPC/homura/", target="homura secret", multi=5),

                        Achievement("The last Earthbender", "You have captured the Earth Kunoichi and made her your sex slave.", pic="portrait blush.webp", pic_path="NPC/kunoichi/haruka/", target="haruka captured", multi=10),
                        Achievement("The last Voidbender", "You have captured the Void Kunoichi and made her your sex slave.", pic="portrait blush.webp", pic_path="NPC/kunoichi/narika/", target="narika captured", multi=10),
                        Achievement("The last Waterbender", "You have made a deal with the Water Kunoichi and she became your sex slave.", pic="portrait naked.webp", pic_path="NPC/kunoichi/mizuki/", target="mizuki revenge", multi=10),
                        Achievement("The last Firebender", "You have enlisted the help of Gizel to break Homura's will and turn her into your sex slave.", pic="portrait naked.webp", pic_path="NPC/homura/", target="homura farm", multi=10),

                        Achievement("Chapter 3: Spitting out the Demons", "You have helped Haruka rescue her Master Subaru from the clutches of evil demon knights.", pic="portrait.webp", pic_path="NPC/kunoichi/subaru/", target="haruka ally", multi=10),
                        Achievement("Chapter 3: Ocean's Two", "You have helped Narika unfold her not-so-master plan to rob the Magic University, and escaped by the skin of your teeth.", pic="portrait sad.webp", pic_path="NPC/kunoichi/narika/", target="narika ally", multi=10),
                        Achievement("Chapter 3: A Zanese Ghost Story", "You have helped Mizuki meet her long-lost heir, and brought her suffering to an end.", pic="portrait sad.webp", pic_path="NPC/kunoichi/mizuki/", target="mizuki redeemed", multi=10),
                        Achievement("Chapter 3: The Power of Love", "Homura renounced her oath to Shirohito and became yours instead.", pic="portrait blush.webp", pic_path="NPC/homura/", target="homura love", multi=10),

                        Achievement("Chapter 3: It's a Trap!", "You have led Haruka into a horrible trap.", pic="portrait evil.webp", pic_path="NPC/kunoichi/subaru/", target="haruka banished", multi=10),
                        Achievement("Chapter 3: Honey, I Shrunk your Ass", "You have turned poor Narika into a fleshlight.", pic="enlarger.webp", pic_path="items/misc/", target="narika raped", multi=10),
                        Achievement("Chapter 3: The One that Got Away", "You have captured Mizuki, only for her to slip between your fingers.", pic="portrait ninja.webp", pic_path="NPC/kunoichi/mizuki/", target="mizuki captured", multi=5),
                        Achievement("Chapter 3: Hot Shower", "You have captured Homura, and relieved some of the tension between you.", pic="capture (5).webp", pic_path="NPC/homura/", target="homura shower", multi=5),

                        Achievement("Chapter 3: Earth Kunoichi down", "You have defeated the Earth Kunoichi and turned her over to the authorities.", pic="portrait surprise.webp", pic_path="NPC/kunoichi/haruka/", target="haruka arrested", multi=5),
                        Achievement("Chapter 3: Void Kunoichi down", "You have defeated the Void Kunoichi and turned her over to the authorities.", pic="portrait angry.webp", pic_path="NPC/kunoichi/narika/", target="narika arrested", multi=5),
                        Achievement("Chapter 3: Water Kunoichi down", "You have defeated the Water Kunoichi and turned her over to the authorities.", pic="portrait ninja.webp", pic_path="NPC/kunoichi/mizuki/", target="mizuki arrested", multi=5),
                        Achievement("Chapter 3: Fire Kunoichi down", "You have defeated the Fire Kunoichi and turned her over to the authorities.", pic="portrait ninja.webp", pic_path="NPC/homura/", target="homura arrested", multi=5),

                        Achievement("Treasure hunter: Blondie", "You had sex with the blonde treasure girl.", pic="amber ring.webp", pic_path="items/ring/", target="h treasure blonde", multi=10),
                        Achievement("Treasure hunter: Pinky", "You had sex with the pink-haired treasure girl.", pic="amber ring.webp", pic_path="items/ring/", target="h treasure pink", multi=10),
                        Achievement("Bedded: The Slave", "You had hot sex with your slave Sill.", pic="portrait2.webp", pic_path="NPC/Sill/", target="h sill1", multi=5),
                        Achievement("Bedded: The Maid", "You had sex with Gio's maid.", pic="portrait blush.webp", pic_path="NPC/Maid/", target="h maid", multi=5),
                        Achievement("Bedded: The Banker", "You had sex with the Banker.", pic="portrait.webp", pic_path="NPC/Banker/", target="h banker", multi=10),
                        Achievement("Bedded: The Captain", "You had sex with Farah.", pic="portrait.webp", pic_path="NPC/Captain/", target="h farah", multi=5),
                        Achievement("Bedded: The Lieutenant", "You had sex with Lydie.", pic="portrait.webp", pic_path="NPC/Lieutenant/", target="h lydie", multi=5),
                        Achievement("Bedded: The Sergeant", "You had sex with Kashiv.", pic="portrait.webp", pic_path="NPC/Sergeant/", target="h kashiv", multi=5),
                        Achievement("Bedded: The Guard", "You had sex with Maya.", pic="portrait.webp", pic_path="NPC/Maya/", target="h maya", multi=5),
                        Achievement("Bedded: The Thief", "You had sex with Renza.", pic="portrait.webp", pic_path="NPC/Renza/", target="h renza", multi=10),
                        Achievement("Bedded: The Rancher", "You had sex with Goldie.", pic="portrait.webp", pic_path="NPC/Goldie/", target="h goldie", multi=5),
                        Achievement("Bedded: The Officer", "You had sex with Stella.", pic="portrait.webp", pic_path="NPC/Stella/", target="h stella", multi=5),
                        Achievement("Bedded: The General", "You had sex with Ka.", pic="ka portrait.webp", pic_path="NPC/Stella/", target="h ka", multi=10),
                        Achievement("Bedded: The Admiral", "You had sex with Zee.", pic="zee portrait.webp", pic_path="NPC/Stella/", target="h zee", multi=10),
                        Achievement("Bedded: The Hunter", "You had sex with Willow.", pic="portrait.webp", pic_path="NPC/Willow/", target="h willow", multi=5),
                        Achievement("Bedded: The Relative", "You had sex with Willow's relative.", pic="portrait.webp", pic_path="NPC/Willow/", target="h relative", multi=10),
                        Achievement("Battle Toad", "You had sex as a toad, and now you can never tell your friends.", pic="milkmaid.webp", pic_path="NPC/Misc/", target="h toad", multi=10),
                        Achievement("Bedded: The Shop Owner", "You had sex with the shop owner.", pic="silky nighties.webp", pic_path="items/gift/", target="h shop", multi=10),
                        Achievement("Bedded: The Night Mistress", "You had sex with Satella.", pic="portrait.webp", pic_path="NPC/Satella/", target="h satella", multi=10),
                        Achievement("Bedded: The Moon Goddess", "You had sex with the Goddess, Shalia.", pic="portrait.webp", pic_path="NPC/Shalia/", target="h shalia", multi=25),
                        Achievement("Bedded: The Accountant", "You had sex with the woman you rescued from the sewers.", pic="portrait.webp", pic_path="NPC/Sewer girl/", target="h sewer", multi=10),
                        Achievement("Bedded: The Holy Builder", "You had sex with Bast.", pic="portrait.webp", pic_path="NPC/Bast/", target="h bast", multi=10),
                        Achievement("Bedded: The Swimmer", "You had sex with Anika.", pic="anika portrait.webp", pic_path="NPC/Jobgirl/beach/", target="h anika", multi=10),
#                         Achievement("Bedded: The Adventurer", "You had sex with Scarlet.", pic="portrait.webp", pic_path="NPC/Jobgirl/", target="h jobgirl"), # Event not ready yet?
                        Achievement("Bedded: The Taxwoman", "You had sex with the Slavers' Guild woman.", pic="portrait.webp", pic_path="NPC/taxgirl/", target="h taxgirl", multi=10),
                        Achievement("Bedded: The Air Kunoichi", "You had (repeated) sex with Suzume.", pic="portrait.webp", pic_path="NPC/suzume/", target="h suzume", multi=10),
                        Achievement("Bedded: The Noble Girl", "You had sex with Lady Homura Henso.", pic="portrait.webp", pic_path="NPC/homura/", target="h homura", multi=10),


                        Achievement("City: The Raiders", "You had sex with %s of the women adventurers.", pic="impress0.webp", pic_path="NPC/encounters/", target="h impress", level_nb=4, multi=2),
                        Achievement("City: The Slave Apprentice", "You helped with a slavegirl's training.", pic="slave2.webp", pic_path="NPC/misc/", target="h slavegirl", multi=2),
                        Achievement("City: The Slave Mistress", "You had sex with the slavemarket girls.", pic="slave1.webp", pic_path="NPC/misc/", target="h slavemarket", multi=4),
                        Achievement("City: The Catgirls", "You had sex with %s of the catgirls.", pic="cat found.webp", pic_path="NPC/encounters/", target="h catgirl", level_nb=2, multi=2),
                        Achievement("City: The Gypsy", "You had sex with a gypsy girl.", pic="gypsy1_1.webp", pic_path="NPC/encounters/", target="h gypsy", multi=2),
                        Achievement("City: The Robber", "You had sex with a defeated robber.", pic="rob5_1.webp", pic_path="NPC/encounters/", target="h robber", multi=2),
                        Achievement("City: The Gambler", "You had sex with a gambling girl.", pic="gambler4_1.webp", pic_path="NPC/encounters/", target="h gambler", multi=2),
                        Achievement("Merry H-Mas Everyone", "You had sex with a mysterious winter visitor.", pic="portrait.webp", pic_path="NPC/Hmas/", target="hmas", multi=10),


                        Achievement("Let's play: Master And Servants", "Own %s slaves (not counting Sill).", pic="slave1.webp", pic_path="NPC/Misc/", level_nb=5, target="slaves", requirements={1 : 4, 2 : 8, 3 : 16, 4 : 24, 5 : 32}, multi=5),
                        Achievement("P.I.M.P", "Have %s slaves with rank B or above.", pic="slave2.webp", pic_path="NPC/Misc/", level_nb=5, target="rank B", requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=2),
                        Achievement("Hustler", "Have %s slaves with rank A or above.", pic="slave2.webp", pic_path="NPC/Misc/", level_nb=5, target="rank A", requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=3),
                        Achievement("Monsieur", "Have %s slaves with rank S or above.", pic="slave2.webp", pic_path="NPC/Misc/", level_nb=5, target="rank S", requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=5),
                        Achievement("Milord", "Have %s slaves with rank X or above.", pic="slave2.webp", pic_path="NPC/Misc/", level_nb=5, target="rank X", requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=10),
                        Achievement("Enter The Dungeon", "Have %s masochist slaves.", pic="slave2.webp", pic_path="NPC/Misc/", level_nb=5, target="masochist", requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, multi=3),
                        Achievement("A Day At The Farm", "Your girls have spent a combined %s days training at the farm in one playthrough.", pic="beast2.webp", pic_path="NPC/Minions/", level_nb=5, target="farm_days", requirements={1 : 10, 2 : 30, 3 : 90, 4 : 180, 5 : 365}, multi=2),
                        Achievement("Toy Story", "Have your girls use toys %s times in one playthrough.", pic="black dildo.webp", pic_path="Items/Toy/", level_nb=5, target="used toy", requirements={1 : 1, 2 : 10, 3 : 100, 4 : 500, 5 : 2500}, multi=3),
                        Achievement("Babes With Blades", "Equip %s girls with weapons.", pic="knife.webp", pic_path="Items/Weapon/", level_nb=5, target="hands", requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}),
                        Achievement("Dress To Impress", "Equip %s girls with dresses.", pic="frilly dress.webp", pic_path="Items/dress/", level_nb=5, target="body", requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}),
                        Achievement("Pet Collars", "Equip %s girls with necklaces.", pic="dog collar.webp", pic_path="Items/necklace/", level_nb=5, target="neck", requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}),
                        Achievement("My Precious", "Equip %s girls with rings.", pic="brass ring.webp", pic_path="Items/ring/", level_nb=5, target="finger", requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}),
                        Achievement("The IT panties", "Equip %s girls with accessories.", pic="lace panties.webp", pic_path="Items/accessory/", level_nb=5, target="accessory", requirements={1 : 2, 2 : 4, 3 : 8, 4 : 16, 5 : 32}),
                        Achievement("Nudist Beach", "Have %s girls naked at the same time.", pic="naked2.webp", pic_path="UI/status/", level_nb=5, target="naked", requirements={1 : 2, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=3),
                        Achievement("Bi Curious", "Have %s girls comfortable with bisexual sex.", pic="naked2.webp", pic_path="UI/status/", level_nb=5, target="bisexual", requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=5),
                        Achievement("Groupon", "Have %s girls comfortable with group sex.", pic="naked2.webp", pic_path="UI/status/", level_nb=5, target="group", requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=10),


                        Achievement("Hokuto No Chin-Chin", "Reach level %s as a Warrior.", pic="warrior.webp", pic_path="UI/", level_nb=5, target="Warrior", requirements={1 : 5, 2 : 10, 3 : 15, 4 : 20, 5 : 25}, multi=5),
                        Achievement("Klaatu Barada Nikto", "Reach level %s as a Wizard.", pic="wizard.webp", pic_path="UI/", level_nb=5, target="Wizard", requirements={1 : 5, 2 : 10, 3 : 15, 4 : 20, 5 : 25}, multi=5),
                        Achievement("Gold Finger", "Reach level %s as a Trader.", pic="trader.webp", pic_path="UI/", level_nb=5, target="Trader", requirements={1 : 5, 2 : 10, 3 : 15, 4 : 20, 5 : 25}, multi=5),
                        Achievement("Johny B. Good", "Become a shining example of justice. And a brothel owner. Why not?", pic="al_good.webp", pic_path="UI/", target="good", multi=10),
                        Achievement("Switzerland", "You don't take sides, you just collect your winnings.", pic="al_neutral.webp", pic_path="UI/", target="neutral", multi=10),
                        Achievement("Evil Heart", "Become inordinately evil. Obtain over %s evil points.", pic="al_evil.webp", pic_path="UI/", level_nb=3, target="evil", requirements={1 : 10, 2 : 100, 3 : 1000}, custom_titles={1 : "Mother-In-Law", 2 : "Dr. Evil", 3 : "Palpatine"}, multi=5),
                        Achievement("P.E.T.A. Disclaimer", "No supernatural animals were harmed in the production of this game. {b}{i}OR WERE THEY?{/i}{/b}", pic="pet1.webp", pic_path="NPC/Misc/Pets/", target="pet armageddon", multi=25),
                        Achievement("The Mountain", "Reach 10 in strength.", pic="warrior.webp", pic_path="UI/", target="mc strength", multi=10),
                        Achievement("Gandalf", "Reach 10 in spirit.", pic="wizard.webp", pic_path="UI/", target="mc spirit", multi=10),
                        Achievement("Solo", "Reach 10 in charisma.", pic="trader.webp", pic_path="UI/", target="mc charisma", multi=10),
                        Achievement("Meep Meep", "Reach 10 in speed.", pic="Leather boots.webp", pic_path="items/accessory/", target="mc speed", multi=10),

                        Achievement("Long And Hard", "Play Brothel King for %s game months in one playthrough.", pic="calendar.webp", pic_path="UI/", level_nb=5, target="months", requirements={1 : 1, 2 : 3, 3 : 6, 4 : 12, 5 : 24}, multi=5),
                        Achievement("Hitwoman", "Successfully complete %s contracts.", pic=license_dict[1][1], pic_path="UI/", level_nb=5, target="completed contracts", requirements={1 : 1, 2 : 3, 3 : 6, 4 : 12, 5 : 24}, multi=10),
                        Achievement("Career change", "Sell a girl after a perfectly successful contract.", pic="maid.webp", pic_path="NPC/Misc/", target="contract sale", multi=25),
                        Achievement("HeroQuest", "Complete %s quests.", pic="portrait.webp", pic_path="NPC/Jobgirl/", level_nb=5, target="completed quest", requirements={1 : 5, 2 : 25, 3 : 50, 4 : 100, 5 : 250}, multi=5),
                        Achievement("Hentai High School", "Complete %s classes.", pic="portrait.webp", pic_path="NPC/Jobgirl/", level_nb=5, target="completed class", requirements={1 : 5, 2 : 25, 3 : 50, 4 : 100, 5 : 250}, multi=5),
                        Achievement("Sensei", "Fill out a class with your girls.", pic="portrait.webp", pic_path="NPC/Sewer girl/", target="filled class", multi=10),
                        Achievement("Animal Farm", "Recruit %s minions.", pic="beast1.webp", pic_path="NPC/Minions/", level_nb=5, target="minions", requirements={1 : 2, 2 : 4, 3 : 8, 4 : 12, 5 : 20}, multi=5),
                        Achievement("Brothel Tycoon", "Earn %s denars in a single playthrough.", pic="gold bag.webp", pic_path="items/misc/", level_nb=6, target="total_gold", requirements={1 : 1000, 2 : 10000, 3 : 100000, 4 : 1000000, 5 : 10000000, 6 : 100000000}, multi=10),
                        Achievement("The Executive", "Make %s denars in a single night.", pic="coin.webp", pic_path="UI/", level_nb=5, target="income", requirements={1 : 100, 2 : 1000, 3 : 10000, 4 : 100000, 5 : 250000}, multi=10),
                        Achievement("WeWork", "Lose %s denars in a single night.", pic="portrait.webp", pic_path="NPC/Kosmo/", level_nb=5, target="losses", requirements={1 : 100, 2 : 1000, 3 : 5000, 4 : 10000, 5 : 25000}, multi=10),
                        Achievement("Cockfeller", "Amass %s denars in cash.", pic="jewel bag.webp", pic_path="items/misc/", level_nb=5, target="gold", requirements={1 : 1000, 2 : 10000, 3 : 100000, 4 : 1000000, 5 : 10000000}, multi=10),
                        Achievement("Friends With Benefits", "%s of your girls have friends.", pic="heart.webp", pic_path="UI/", level_nb=5, target="friends", requirements={1 : 2, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=5),
                        Achievement("Mean Girls", "%s of your girls have rivals.", pic="broken heart.webp", pic_path="UI/", level_nb=5, target="rivals", requirements={1 : 2, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=5),
                        Achievement("Battle Tested", "Survive %s security events.", pic="shield.webp", pic_path="UI/", level_nb=5, target="security events", requirements={1 : 10, 2 : 25, 3 : 50, 4 : 125, 5 : 250}, multi=5),
                        Achievement("War Master", "Capture an enemy general.", pic="portrait.webp", pic_path="NPC/Kenshin", target="general captured", multi=25),
                        Achievement("Cavalry", "Rescue a kidnapped girl.", pic="knight portrait.webp", pic_path="NPC/Misc/", target="rescued from kidnapping", multi=25),
                        Achievement("Does This Make You Ticklish?", "Discover %s positive fixations on your girls.", pic="droplet.webp", pic_path="UI/", target="pos fixations", level_nb=5, requirements={1 : 10, 2 : 25, 3 : 50, 4 : 125, 5 : 250}, multi=5),
                        Achievement("Phobia", "Discover %s negative fixations on your girls.", pic="skull.webp", pic_path="UI/", target="neg fixations", level_nb=5, requirements={1 : 10, 2 : 25, 3 : 50, 4 : 125, 5 : 250}, multi=5),
                        Achievement("Sex Therapist", "Remove %s negative fixations from your girls.", pic="droplet.webp", pic_path="UI/", target="neg fixation removed", level_nb=5, requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=5),
                        Achievement("Oops", "Lock a girl's negative fixation by trying too hard.", pic="skull.webp", pic_path="UI/", target="neg fixation locked", multi=5),
                        Achievement("Trussst In Me", "Successfully hypnotize girls %s times.", pic="droplet.webp", pic_path="UI/", target="hypnotize success", level_nb=5, requirements={1 : 1, 2 : 10, 3 : 50, 4 : 100, 5 : 250}, multi=5),
                        Achievement("Charlatan", "Fail at hypnotizing girls %s times.", pic="droplet.webp", pic_path="UI/", target="hypnotize failure", level_nb=5, requirements={1 : 1, 2 : 5, 3 : 25, 4 : 50, 5 : 100}, multi=3),

                        Achievement("Lovebirds", "Have %s girls with %s love or more.", level_nb=5, pic="heart.webp", pic_path="UI/", target="love", requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 25, 2 : 50, 3 : 75, 4 : 100, 5 : 125}, multi=3),
                        Achievement("Scarecrow", "Have %s girls with %s fear or more.", level_nb=5, pic="skull.webp", pic_path="UI/", target="fear", requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 25, 2 : 50, 3 : 75, 4 : 100, 5 : 125}, multi=3),
                        Achievement("Beauty Mastery", "Have %s girls with over %s beauty.", pic="portrait.webp", pic_path="NPC/Katryn/", target="Beauty", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=2),
                        Achievement("Body Mastery", "Have %s girls with over %s body.", pic="portrait.webp", pic_path="NPC/Ramias/", target="Body", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=2),
                        Achievement("Charm Mastery", "Have %s girls with over %s charm.", pic="portrait.webp", pic_path="NPC/Gurigura/", target="Charm", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=2),
                        Achievement("Refinement Mastery", "Have %s girls with over %s refinement.", pic="portrait.webp", pic_path="NPC/Riche/", target="Refinement", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=2),
                        Achievement("Libido Mastery", "Have %s girls with over %s libido.", pic="portrait.webp", pic_path="NPC/Captain/", target="Libido", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=2),
                        Achievement("Obedience Mastery", "Have %s girls with over %s obedience.", pic="portrait.webp", pic_path="NPC/Maid/", target="Obedience", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=2),
                        Achievement("Constitution Mastery", "Have %s girls with over %s constitution.", pic="portrait.webp", pic_path="NPC/Jobgirl/", target="Constitution", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=2),
                        Achievement("Sensitivity Mastery", "Have %s girls with over %s sensitivity.", pic="portrait.webp", pic_path="NPC/Satella/", target="Sensitivity", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=2),
                        Achievement("Service Mastery", "Have %s girls with over %s service skill.", pic="portrait.webp", pic_path="NPC/Willow/", target="Service", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=4),
                        Achievement("Sex Mastery", "Have %s girls with over %s sex skill.", pic="portrait.webp", pic_path="NPC/Goldie/", target="Sex", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=4),
                        Achievement("Anal Mastery", "Have %s girls with over %s anal skill.", pic="portrait.webp", pic_path="NPC/Kosmo/", target="Anal", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=4),
                        Achievement("Fetish Mastery", "Have %s girls with over %s fetish skill.", pic="portrait.webp", pic_path="NPC/Stella/", target="Fetish", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=4),
                        Achievement("Ultimate Mastery", "Have %s girls with over %s in all skills.", pic="portrait.webp", pic_path="NPC/Sill/", target="ultimate", level_nb=5, requirements={1 : 1, 2 : 2, 3 : 4, 4 : 8, 5 : 16}, requirements2={1 : 50, 2 : 100, 3 : 150, 4 : 200, 5 : 250}, multi=5),
                        Achievement("Slaver", "Sell girls for a total of %s denars during one playthrough.", pic="slave1.webp", pic_path="NPC/Misc/", target="sell girl gold", level_nb=5, requirements={1 : 500, 2 : 2500, 3 : 10000, 4 : 25000, 5 : 100000}, multi=5),
                        Achievement("Heartless", "Sell a girl who loves you.", pic="spirit portrait.webp", pic_path="NPC/Misc/", target="sell girl love", multi=20),
                        Achievement("Let Her Go", "Let a girl get her freedom back.", pic="broken heart.webp", pic_path="UI/", target="release free girl", multi=10),
                        Achievement("Rapelay", "Rape your girls %s times.", pic="spirit portrait.webp", pic_path="NPC/Misc/", target="raped", level_nb=5, requirements={1 : 1, 2 : 5, 3 : 10, 4 : 25, 5 : 100}, multi=3),
                        Achievement("Wife Beater", "Beat your girls up %s times.", pic="spirit portrait.webp", pic_path="NPC/Misc/", target="beaten", level_nb=5, requirements={1 : 1, 2 : 5, 3 : 10, 4 : 25, 5 : 100}, multi=3),
                        Achievement("Harsh Master", "Punish your girls %s times.", pic="skull.webp", pic_path="UI/", target="punished", level_nb=5, requirements={1 : 5, 2 : 25, 3 : 100, 4 : 250, 5 : 500}, multi=2),
                        Achievement("Sugar Daddy", "Reward your girls %s times.", pic="droplet.webp", pic_path="UI/", target="rewarded", level_nb=5, requirements={1 : 5, 2 : 25, 3 : 100, 4 : 250, 5 : 500}, multi=2),
                        Achievement("Spoiler Alert", "You have rewarded one of your girls so much that she became spoiled.", pic="bun.webp", pic_path="items/food/", target="spoiled", multi=2),
                        Achievement("Terrorist", "You have punished one of your girls so much that she became terrified.", pic="monster juice.webp", pic_path="items/misc/", target="terrified", multi=2),
                        Achievement("Farmer", "You have unlocked the Farm.", pic="beast2.webp", pic_path="NPC/Minions/", target="farm", multi=2),
                        Achievement("Knock On Wood", "You have unlocked the Carpenter's Wagon.", pic="portrait.webp", pic_path="NPC/Carpenter/", target="wagon", multi=2),
                        Achievement("Sewer Knight", "You saved the prisoner in the sewers.", pic="portrait naked.webp", pic_path="NPC/Sewer girl/", target="sewer defender", multi=2),
                        Achievement("Enduring", "Kosmo visited you %s times.", pic="portrait.webp", pic_path="NPC/Kosmo/", target="kosmo", level_nb=4, requirements={1 : 1, 2 : 5, 3 : 10, 4 : 20}, multi=2),

                        Achievement("Casanova", "Sleep with girls %s times.", pic="heart.webp", pic_path="UI/", level_nb=5, target="had sex", requirements={1 : 5, 2 : 25, 3 : 100, 4 : 250, 5 : 1000}, multi=5),
                        Achievement("Big Spender", "Spend %s denars at the slave market.", pic="slave2.webp", pic_path="NPC/Misc/", target="gold spent slavemarket", level_nb=4, requirements={1 : 500, 2 : 2500, 3 : 10000, 4 : 25000, 5 : 100000}, multi=2),
                        Achievement("Fashion Victim", "Spend %s denars in shops.", pic="portrait.webp", pic_path="NPC/Gift girl/", target="gold spent shops", level_nb=4, requirements={1 : 500, 2 : 2500, 3 : 10000, 4 : 25000, 5 : 100000}, multi=2),
                        Achievement("The Confident", "Hear %s girl origin stories in one playthrough.", pic="empty heart.webp", pic_path="UI/", target="origin stories", level_nb=5, requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 24}, multi=2),
                        Achievement("Gigolo", "Convince %s free girls to join your brothel.", pic="empty heart.webp", pic_path="UI/", target="free girl acquired", level_nb=5, requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=5),
                        Achievement("You Might Get Murdered", "Have ten girlfriends simultaneously.", pic="heart.webp", pic_path="UI/", target="girlfriends", requirements={1 : 10}, multi=25),
                        Achievement("We Have The Original", "Have %s original girls in your brothel.", pic="license2.webp", pic_path="UI/", target="originals", level_nb=5, requirements={1 : 1, 2 : 4, 3 : 8, 4 : 16, 5 : 32}, multi=2),

                        Achievement("Broke: Beggar", "Have a Beggar spend all his money in the brothel.", pic="beggar.webp", pic_path="UI/customers/", target="broke beggars"),
                        Achievement("Broke: Thug", "Have a Thug spend all his money in the brothel.", pic="thug.webp", pic_path="UI/customers/", target="broke thugs", multi=2),
                        Achievement("Broke: Laborer", "Have a Laborer spend all his money in the brothel.", pic="Laborer.webp", pic_path="UI/customers/", target="broke laborers", multi=2),
                        Achievement("Broke: Sailor", "Have a Sailor spend all his money in the brothel.", pic="Sailor.webp", pic_path="UI/customers/", target="broke sailors", multi=2),
                        Achievement("Broke: Commoner", "Have a Commoner spend all his money in the brothel.", pic="Commoner.webp", pic_path="UI/customers/", target="broke commoners", multi=3),
                        Achievement("Broke: Craftsman", "Have a Craftsman spend all his money in the brothel.", pic="Craftsman.webp", pic_path="UI/customers/", target="broke craftsmen", multi=3),
                        Achievement("Broke: Bourgeois", "Have a Bourgeois spend all his money in the brothel.", pic="Bourgeois.webp", pic_path="UI/customers/", target="broke bourgeois", multi=3),
                        Achievement("Broke: Guild Member", "Have a Guild Member spend all his money in the brothel.", pic="Guild Member.webp", pic_path="UI/customers/", target="broke guild members", multi=4),
                        Achievement("Broke: Patrician", "Have a Patrician spend all his money in the brothel.", pic="Patrician.webp", pic_path="UI/customers/", target="broke patricians", multi=4),
                        Achievement("Broke: Aristocrat", "Have an Aristocrat spend all his money in the brothel.", pic="aristocrat.webp", pic_path="UI/customers/", target="broke aristocrats", multi=4),
                        Achievement("Broke: Noble", "Have a Noble spend all his money in the brothel.", pic="Noble.webp", pic_path="UI/customers/", target="broke nobles", multi=5),
                        Achievement("Broke: Royal", "Have a Royal family member spend all his money in the brothel.", pic="Royal.webp", pic_path="UI/customers/", target="broke royals", multi=10),
                        Achievement("Perfect: Beggar", "Have a Beggar reach maximum satisfaction in the brothel.", pic="beggar.webp", pic_path="UI/customers/", target="happy beggars"),
                        Achievement("Perfect: Thug", "Have a Thug reach maximum satisfaction in the brothel.", pic="thug.webp", pic_path="UI/customers/", target="happy thugs", multi=2),
                        Achievement("Perfect: Laborer", "Have a Laborer reach maximum satisfaction in the brothel.", pic="Laborer.webp", pic_path="UI/customers/", target="happy laborers", multi=2),
                        Achievement("Perfect: Sailor", "Have a Sailor reach maximum satisfaction in the brothel.", pic="Sailor.webp", pic_path="UI/customers/", target="happy sailors", multi=2),
                        Achievement("Perfect: Commoner", "Have a Commoner reach maximum satisfaction in the brothel.", pic="Commoner.webp", pic_path="UI/customers/", target="happy commoners", multi=3),
                        Achievement("Perfect: Craftsman", "Have a Craftsman reach maximum satisfaction in the brothel.", pic="Craftsman.webp", pic_path="UI/customers/", target="happy craftsmen", multi=3),
                        Achievement("Perfect: Bourgeois", "Have a Bourgeois reach maximum satisfaction in the brothel.", pic="Bourgeois.webp", pic_path="UI/customers/", target="happy bourgeois", multi=3),
                        Achievement("Perfect: Guild Member", "Have a Guild Member reach maximum satisfaction in the brothel.", pic="Guild Member.webp", pic_path="UI/customers/", target="happy guild members", multi=4),
                        Achievement("Perfect: Patrician", "Have a Patrician reach maximum satisfaction in the brothel.", pic="Patrician.webp", pic_path="UI/customers/", target="happy patricians", multi=4),
                        Achievement("Perfect: Aristocrat", "Have an Aristocrat reach maximum satisfaction in the brothel.", pic="aristocrat.webp", pic_path="UI/customers/", target="happy aristocrats", multi=4),
                        Achievement("Perfect: Noble", "Have a Noble reach maximum satisfaction in the brothel.", pic="Noble.webp", pic_path="UI/customers/", target="happy nobles", multi=5),
                        Achievement("Perfect: Royal", "Have a Royal family member reach maximum satisfaction in the brothel.", pic="Royal.webp", pic_path="UI/customers/", target="happy royals", multi=10),

                        Achievement("Perks: The Maid Tree", "Unlock all perks in the Maid tree on one of your girls.", pic="The Maid portrait.webp", pic_path="perks/", target="The Maid", multi=5),
                        Achievement("Perks: The Player Tree", "Unlock all perks in the Player tree on one of your girls.", pic="The Player portrait.webp", pic_path="perks/", target="The Player", multi=5),
                        Achievement("Perks: The Model Tree", "Unlock all perks in the Model tree on one of your girls.", pic="The Model portrait.webp", pic_path="perks/", target="The Model", multi=5),
                        Achievement("Perks: The Courtesan Tree", "Unlock all perks in the Courtesan tree on one of your girls.", pic="The Courtesan portrait.webp", pic_path="perks/", target="The Courtesan", multi=5),
                        Achievement("Perks: The Escort Tree", "Unlock all perks in the Escort tree on one of your girls.", pic="The Escort portrait.webp", pic_path="perks/", target="The Escort", multi=5),
                        Achievement("Perks: The Fox Tree", "Unlock all perks in the Fox tree on one of your girls.", pic="The Fox portrait.webp", pic_path="perks/", target="The Fox", multi=5),
                        Achievement("Perks: The Slut Tree", "Unlock all perks in the Slut tree on one of your girls.", pic="The Slut portrait.webp", pic_path="perks/", target="The Slut", multi=5),
                        Achievement("Perks: The Bride Tree", "Unlock all perks in the Bride tree on one of your girls.", pic="The Bride portrait.webp", pic_path="perks/", target="The Bride", multi=5),

                        Achievement("Service Mania", "Have your girls perform service acts %s times.", pic="egg vibrator.webp", pic_path="items/toy/", target="perform service", level_nb=5, requirements={1 : 1, 2 : 10, 3 : 100, 4 : 1000, 5 : 10000}, multi=5),
                        Achievement("Sex Mania", "Have your girls perform sex acts %s times.", pic="lace panties.webp", pic_path="items/accessory/", target="perform sex", level_nb=5, requirements={1 : 1, 2 : 10, 3 : 100, 4 : 1000, 5 : 10000}, multi=5),
                        Achievement("Anal Mania", "Have your girls perform anal acts %s times.", pic="butt plug.webp", pic_path="items/toy/", target="perform anal", level_nb=5, requirements={1 : 1, 2 : 10, 3 : 100, 4 : 1000, 5 : 10000}, multi=5),
                        Achievement("Fetish Mania", "Have your girls perform fetish acts %s times.", pic="ropes.webp", pic_path="items/toy/", target="perform fetish", level_nb=5, requirements={1 : 1, 2 : 10, 3 : 100, 4 : 1000, 5 : 10000}, multi=5),
                        Achievement("Bisexual Mania", "Have your girls perform bisexual acts %s times.", pic="black dildo.webp", pic_path="items/toy/", target="perform bisexual", level_nb=5, requirements={1 : 1, 2 : 5, 3 : 25, 4 : 100, 5 : 250}, multi=5),
                        Achievement("Group Mania", "Have your girls perform group acts %s times.", pic="beer keg.webp", pic_path="items/furniture/", target="perform group", level_nb=5, requirements={1 : 1, 2 : 5, 3 : 25, 4 : 100, 5 : 250}, multi=5),
                        Achievement("Star System", "Reach %s reputation.", pic="star.webp", pic_path="UI/", target="rep", level_nb=5, requirements={1 : 100, 2 : 1000, 3 : 5000, 4 : 10000, 5 : 30000}, multi=5),
                        Achievement("Interior Designer", "Build all furniture for chapter %s.", pic="steam jacuzzi.webp", pic_path="items/furniture/", target="furniture", level_nb=6, requirements={1 : 2, 2 : 3, 3 : 4, 4 : 5, 5 : 6, 6 : 7}, multi=2),
                        Achievement("Home Sweet Home", "Build all upgrades for chapter %s.", pic="chapel.webp", pic_path="items/furniture/", target="upgrades", level_nb=7, requirements={1 : 1, 2 : 2, 3 : 3, 4 : 4, 5 : 5, 6 : 6, 7 : 7}, multi=2),
                        Achievement("Does This Bring You Joy?", "Spend %s denars on cleaning.", pic="broom.webp", pic_path="items/furniture/", target="gold clean", level_nb=5, requirements={1 : 250, 2 : 1000, 3 : 5000, 4 : 25000, 5 : 100000}, multi=2),
                        Achievement("Close Call", "Repay the Banker's loan.", pic="portrait.webp", pic_path="NPC/Banker/", target="first loan", multi=3),
                        Achievement("Fail Fast", "Lose the game once.", pic="zap traps.webp", pic_path="items/furniture/", target="game over", multi=3),
                        Achievement("The One That Got Away", "A girl has run away from you.", pic="skull.webp", pic_path="UI/", target="runaway", multi=3),
                        Achievement("The One That Got Caught", "Your hirelings have caught a runaway girl.", pic="guard portrait.webp", pic_path="NPC/Misc/", target="caught NPC", multi=3),
                        Achievement("What's Mine Is Mine", "You have caught a runaway girl and brought her back.", target="caught MC", multi=5),
                        Achievement("Brothel Prince", "Reach endless mode in normal difficulty.", pic="bronze statue.webp", pic_path="items/furniture/", target="win normal", multi=25),
                        Achievement("Brothel King", "Reach endless mode in hard difficulty.", pic="silver statue.webp", pic_path="items/furniture/", target="win hard", multi=50),
                        Achievement("Brothel Emperor", "Reach endless mode in hardest difficulty.", pic="gold statue.webp", pic_path="items/furniture/", target="win insane", multi=100),

                        Achievement("Faust", "Cast %s evil powers.", pic="evil deck.webp", pic_path="UI/powers/", target="powers", level_nb=5, requirements={1 : 1, 2 : 5, 3 : 25, 4 : 50, 5 : 100}, multi=3),
                        Achievement("Purple Rain", "Accumulate %s purple mojo.", pic="purple mojo.webp", pic_path="UI/powers/", target="purple mojo", level_nb=5, requirements={1 : 10, 2 : 25, 3 : 50, 4 : 100, 5 : 500}, multi=2),
                        Achievement("Dr. Greenthumb", "Accumulate %s green mojo.", pic="orb_green.webp", pic_path="UI/powers/", target="green mojo", level_nb=5, requirements={1 : 10, 2 : 25, 3 : 50, 4 : 100, 5 : 500}, multi=2),
                        Achievement("Blue Monday", "Accumulate %s blue mojo.", pic="orb_blue.webp", pic_path="UI/powers/", target="blue mojo", level_nb=5, requirements={1 : 10, 2 : 25, 3 : 50, 4 : 100, 5 : 500}, multi=2),
                        Achievement("Red Alert", "Accumulate %s red mojo.", pic="orb_red.webp", pic_path="UI/powers/", target="red mojo", level_nb=5, requirements={1 : 10, 2 : 25, 3 : 50, 4 : 100, 5 : 500}, multi=2),
                        Achievement("Yellow Fever", "Accumulate %s yellow mojo.", pic="orb_yellow.webp", pic_path="UI/powers/", target="yellow mojo", level_nb=5, requirements={1 : 10, 2 : 25, 3 : 50, 4 : 100, 5 : 500}, multi=2),
                        Achievement("Can't make an omelet...", "Break %s girls' sanity.", pic="whip.webp", pic_path="Items/weapon/", target="broken", level_nb=5, requirements={1 : 1, 2 : 3, 3 : 10, 4 : 25, 5 : 50}, multi=2),
                        Achievement("Somebody Else's Problem", "Dump a broken girl on the market.", pic="navThe Slums_idle.webp", pic_path="UI/", target="broken girl auction", multi=5),
                        Achievement("See? I'm Not That Bad!", "Send a broken girl to an asylum.", pic="navThe Cathedra_idle.webp", pic_path="UI/", target="broken girl asylum", multi=5),
                        Achievement("Back from the brink", "Successfully heal a broken girl.", pic="Tonic.webp", pic_path="items/misc/", target="broken girl healed", multi=5),
                        Achievement("Bitch Better Get My Money", "Have %s street whores.", pic="brothelnavbutton_idle.webp", pic_path="UI/", target="broken girl street", level_nb=4, requirements={1 : 1, 2 : 3, 3 : 10, 4 : 20}, multi=3),
                        Achievement("Chaos Unleashed", "Unlock Chaos the talking sword.", pic="portrait.webp", pic_path="NPC/Chaos/", target="chaos", multi=25),

                        Achievement("NewGame+ unlocked", "Finish the game for the first time to unlock NewGame+.", pic="pet1.webp", pic_path="NPC/misc/Pets/", target="newgame+", multi=5),
                        Achievement("Free Girl Challenge", "Finish the game with the free girl challenge activated.", pic="girl.webp", pic_path="spells/", target="free girl challenge", multi=100),
                        Achievement("Training Challenge", "Finish the game with the training challenge activated.", pic="militia.webp", pic_path="spells/", target="training challenge", multi=200),

                        Achievement("Hall of Fame", "Reach #%s spot in the city's brothel rankings.", pic="holy handgrenade.webp", pic_path="items/weapon/", target="brothel ranking", level_nb=8, requirements={1 : 35, 2 : 30, 3 : 25, 4 : 20, 5 : 15, 6 : 10, 7: 5, 8: 1}, multi=5),
                        ]

    achievement_dict = {}

    for achv in achievement_list:
        achievement_dict[achv.target] = achv

    # List of achievement targets that are tested with a game.track() update
    tracked_achievements = ["used toy", "farm_days", "had sex", "completed quest", "completed class", "completed contracts", "total_gold", "security events", "neg fixation removed", "hypnotize success", "hypnotize failure", "sell girl gold", "raped", "beaten", "punished", "rewarded", "free girl acquired", "origin stories", "gold spent slavemarket", "gold spent shops", "gold clean", "kosmo", "powers", "purple mojo", "green mojo", "blue mojo", "red mojo", "yellow mojo", "broken", "broken girl street", "perform service", "perform sex", "perform anal", "perform fetish", "perform bisexual", "perform group"]

    def unlock_achievement(target, level_cap=99):
        if target not in achievement_dict.keys():
            raise AssertionError("Attempt to unlock an unknown achievement: %s" % target)
        elif achievement_dict[target].unlock(level_cap):
            renpy.show_screen("achievement_notification", [achievement_dict[target]])
            memorize_achievement(target)

    def reset_achievements():
        global selected_achievement

        for achv in achievement_list:
            achv.level = 0
        persistent.achievements = {}
        selected_achievement = None
        latest_achievements = []

    def test_achievements(target_list):
        r = []
        for target in target_list:
            if achievement_dict[target].test():
                r.append(achievement_dict[target])
                memorize_achievement(target)

        renpy.show_screen("achievement_notification", r)

    def test_achievement(target):
        test_achievements([target])

    def memorize_achievement(target):
        global latest_achievements

        # Rotates the last 3 achievements
        if len(latest_achievements) >=3:
            latest_achievements = [[achievement_dict[target], achievement_dict[target].level]] + latest_achievements[0:2]
        else:
            latest_achievements = [[achievement_dict[target], achievement_dict[target].level]] + latest_achievements

#### END OF BK ACHIEVEMENTS FILE ####
