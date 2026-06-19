#### Goal classes ####

init -10 python:
    class Goal(object):

        def __init__(self, type, value = 0, target = 0, label = "", channel="advance", max_chapter=None, blocking=True):

            self.type = type
            self.value = value
            self.target = int(target)
            self.label = label
            self.channel = channel
            self.max_chapter = max_chapter
            self.blocking = blocking
            self.description = ""

        @classmethod
        def from_dict(cls, data):
            """EN: Create a Goal from a JSON-compatible dict.
               ZH: 从 JSON 兼容的字典创建 Goal 对象。"""
            return cls(
                type=data.get("type"),
                value=data.get("value", 0),
                target=data.get("target", 0),
                label=data.get("label", ""),
                channel=data.get("channel", "advance"),
                max_chapter=data.get("max_chapter"),
                blocking=data.get("blocking", True)
            )

        def get_description(self):
            if not self.description:
                if self.type == "gold":
                    self.description = __("you must collect %s gold") % str(int(self.value))

                elif self.type == "ranked":
                    self.description = __("%s of your girls must reach rank %s") % (str(self.target), rank_name[self.value])

                elif self.type == "reputation":
                    self.description = __("your brothel must reach %s reputation") % str(int(self.value))

                elif self.type == "prestige":
                    self.description = __("you must gather %s prestige") % str(int(self.value))

                elif self.type == "story":
                    self.description = self.value # value for story events must be text

                else:
                    self.description = __("You are now in endless mode, enjoy continuing the game!")

            return self.description

        def reached(self):

            if not self.blocking:
                return True

            elif self.max_chapter and self.max_chapter > game.chapter:
                return True

            elif self.type == "gold":
                if MC.gold >= self.value:
                    return True

            elif self.type == "ranked":
                if len([g for g in MC.girls if g.rank >= self.value]) >= self.target:
                    return True

            elif self.type == "reputation":
                if brothel.rep >= self.value:
                    return True

            elif self.type == "prestige":
                if MC.prestige >= self.value:
                    return True

            elif self.type == "story":
                if story_flags[self.label] or not game.is_story_mode():
                    return True

            return False

