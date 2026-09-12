#### GirlBase — Core identity component | 核心身份组件 ####
# Phase 2.1: Identity, name handling, level, serialization.
# 身份、名称处理、等级、序列化
# Methods: set_name, set_fullname, random_rename, get_name, get_badge,
#          is_unique, load_ini, read_ini, adjust_level, randomize.

init -2 python:

    class GirlBase(object):
        """Core identity and lifecycle for a Girl."""

        def __init__(self, girl):
            self.girl = girl

        def set_name(self): ## This creates the full name with or without lastname
            g = self.girl
            first, last = get_name(g.path)

            if g.original:
                if g.ini:
                    g.name = g.init_dict["identity/first_name"]
                    g.lastname = g.init_dict["identity/last_name"]
                    if not g.name and not g.lastname:
                        g.name, g.lastname = first, last
                else:
                    g.name, g.lastname = first, last

            else: # Clones will either receive _BK.ini settings as priority or option settings depending on option choice
                new_name = generate_name("girl")

                if not persistent.gp_name_customization and g.init_dict["identity/first_name"] != "?rand" and g.init_dict["identity/first_name"]: # If _BK.ini has priority
                    g.name = g.init_dict["identity/first_name"] # Automatically set to "?rand" if unspecified in _BK.ini
                elif persistent.keep_firstname:
                    g.name = first
                elif g.init_dict["identity/first_name"] != "?rand" and g.init_dict["identity/first_name"]:
                    g.name = g.init_dict["identity/first_name"] # Automatically set to "?rand" if unspecified in _BK.ini
                else:
                    g.name = new_name[0]

                if not persistent.gp_name_customization and g.init_dict["identity/last_name"] != "?rand": # If _BK.ini has priority
                    g.lastname = g.init_dict["identity/last_name"] # Automatically set to "?rand" if unspecified in _BK.ini
                elif persistent.keep_lastname:
                    g.lastname = last
                elif g.init_dict["identity/last_name"] != "?rand":
                    g.lastname = g.init_dict["identity/last_name"] # Automatically set to "?rand" if unspecified in _BK.ini
                else:
                    g.lastname = new_name[1]

            if g.name == "?rand" or not g.name:
                g.name = generate_name("girl")[0]

            if g.lastname == "?rand":
                g.lastname = generate_name("girl")[1]

            elif not g.lastname:
                g.lastname = ""

            g.set_fullname()

        def set_fullname(self):
            g = self.girl
            if g.init_dict["identity/inverted_name"]:
                g.fullname = g.lastname
                if g.name:
                    if g.fullname:
                        g.fullname += " "
                    g.fullname += g.name
            else:
                g.fullname = g.name
                if g.lastname:
                    if g.fullname:
                        g.fullname += " "
                    g.fullname += g.lastname

        def random_rename(self):
            g = self.girl
            g.name, g.lastname = generate_name("girl")
            g.set_fullname()

#             if g.lastname != "":
#                 g.fullname += " " + g.lastname

        def get_name(self):
            return self.girl._get_name_impl()
        def get_badge(self):
            return self.girl._get_badge_impl()
        def is_unique(self):
            return self.girl._is_unique_impl()
        def load_ini(self, search_for=None, skip_checks=False):
            g = self.girl
            g.init_dict = defaultdict(list)

            g.ini = GirlFilesDict.get_ini(g.path)

            if g.ini is not None:
                g.init_dict = read_init_file(g.ini, search_for=search_for, skip_checks=skip_checks)

                # Extract custom tags from init_dict
                g.custom_tags = {}
                for key, value in g.init_dict.items():
                    if key.startswith("custom tags/"):
                        tag_name = key[len("custom tags/"):]
                        if value:
                            g.custom_tags[tag_name] = make_list(value)

                # Apply custom tags to the global tag system and re-tag pictures
                if g.custom_tags:
                    register_custom_tags_for_pack(g.path, g.custom_tags)

                # Extract custom dialogue from init_dict
                g.custom_dialogue = {}
                for key, value in g.init_dict.items():
                    if key.startswith("custom dialogue/"):
                        topic = key[len("custom dialogue/"):]
                        if value:
                            g.custom_dialogue[topic] = make_list(value)

                # Register custom dialogue lines globally
                if g.custom_dialogue:
                    register_custom_dialogue_for_pack(g.path, g.custom_dialogue)

        def read_ini(self, section=None, key=None): # Debug function
            g = self.girl
            if section and key:
                return g.init_dict[section + "/" + key]
            elif section:
                return [[k, v] for k, v in g.init_dict.items() if k.startswith(section)]
            elif key:
                return [[k, v] for k, v in g.init_dict.items() if k.endswith(key)]
            elif g.ini:
                return g.init_dict
            else:
                return "No init file"

        def adjust_level(self, level):
            return self.girl.adjust_level(level)
        def randomize(self, free=False, p_traits=None, n_trait=None, perks=None, force_original=False, level=1, personality=None, temp_list=None):
            return self.girl._generation.randomize(free, p_traits, n_trait, perks, force_original, level, personality, temp_list)

        def update_files(self):
            g = self.girl
            #<Chris12 PackState>
            #Moved to GirlFilesDict - Should no longer be necessary
            return len(GirlFilesDict.get_pics(g.path)) > 0
            #</Chris12 PackState>
