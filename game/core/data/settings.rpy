#### DIFFICULTY AND SETTINGS ####
## Migrated from BKinit_variables.rpy ##
init -10 python:

    diff_name = {"very easy" : __("Gigolo"), "easy" : __("Hustler"), "normal" : __("Whorelord"), "hard" : __("Brothel Prince"), "insane" : __("Brothel King{#1}")}

    diff_description = {"very easy" : __("No challenge at all. You're either here for the story, or the pretty pictures. {i}All achievements are locked.{/i}"), "easy" : __("A basic challenge for new players."), "normal" : __("The classic experience."), "hard" : __("Want more challenge? Hard has got you covered."), "insane" : __("The ultimate challenge.")}

    diff_settings = ["stats", "xp", "jp", "pref", "rep", "gold", "budget", "rewards", "resources", "prestige", "tax rate", "satisfaction", "security"] # A list is needed to show the values in order

    diff_setting_name = {
                        "gold" : __("Income"),
                        "budget" : __("Customer budget"),
                        "rewards" : __("Rewards"),
                        "resources" : __("Resources"),
                        "stats" : __("Girl skills"),
                        "pref" : __("Preferences"),
                        "xp" : __("XP"),
                        "jp" : __("JP"),
                        "rep" : __("Girl reputation"),
                        "prestige" : __("Prestige"),
                        "tax rate" : __("Guild Fee Offset"),
                        "satisfaction" : __("Customer satisfaction"),
                        "security" : __("Security grace period"),
                        }

    diff_setting_description = {
                        "gold" : __("Affects your {b}Brothel Income{/b}."),
                        "budget" : __("Changes cap on customers' individual {b}budget{/b}."),
                        "rewards" : __("Affects {b}Rewards{/b} from quests, classes and monthly contracts."),
                        "resources" : __("Affects the amount of {b}Resources{/b} you get from collecting and trading."),
                        "stats" : __("Affects the progression of your girls' {b}Skills{/b}."),
                        "pref" : __("Affects the progression of your girls' {b}Sexual Preferences{/b}."),
                        "xp" : __("Affects the progression of your girls' {b}XP{/b}."),
                        "jp" : __("Affects the progression of your girls' {b}JP{/b}."),
                        "rep" : __("Affects the progression of your girls' {b}REP{/b}."),
                        "prestige" : __("Affects the progression of your Main Character's {b}Prestige{/b}."),
                        "tax rate" : __("Increases or decreases the Slave Guild's {b}fee{/b}."),
                        "satisfaction" : __("Changes customer {b}satisfaction{/b} bonus."),
                        "security" : __("Delays threat buildup by this number of days after each event."),
                        }


#### STAT NAMES ####
## Migrated from BKsettings.rpy ##

    stat_name_dict = {
                        "Beauty" : __("Beauty"),
                        "Body" : __("Body"),
                        "Charm" : __("Charm"),
                        "Refinement" : __("Refinement"),
                        "Sensitivity" : __("Sensitivity"),
                        "Libido" : __("Libido"),
                        "Constitution" : __("Constitution"),
                        "Obedience" : __("Obedience"),
                        "Service" : __("Service"),
                        "Sex" : __("Sex"),
                        "Anal" : __("Anal"),
                        "Fetish" : __("Fetish"),
                        "Energy" : __("Energy"),
                    }

