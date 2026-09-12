#### GirlLogging — Event logging and tracking | 日志与追踪组件 ####
# Phase 2.1: Logging, stats tracking, memory, event history.
# 日志、属性追踪、记忆、事件历史
# ★ commit/return_from/add_log/get_log/get_average_performance — 已从 girlclass.rpy 移入 (Phase 7 批次2)
# ★ track_event/get_recent_events/get_recent_events_description/count_occurences (Phase 7 批次2)
# ★ will_remember/remembers/forgets (Phase 7 批次2)

init -2 python:

    class GirlLogging(object):
        """Event logging, stats tracking, memory and event history for a Girl."""

        def __init__(self, girl):
            self.girl = girl

        def commit(self, quest):
            g = self.girl
            g.away = True
            g.return_date = calendar.time + quest.duration
            g.assignment = quest
            quest.enrolled.append(g)
            add_event("return_from_quest", call_args = [g, quest], date = g.return_date)
            g.class_friend_bonus = 0
            for gf in g.friends:
                if gf in quest.enrolled:
                    g.class_friend_bonus = 2
                    break
            for gf in g.rivals:
                if gf in quest.enrolled:
                    g.class_friend_bonus = -1
                    break

            #             calendar.set_alarm(calendar.time + quest.duration, Event(label = "return_from_quest", object = (g, quest)))
            norollback()

        def return_from(self, quest):
            g = self.girl
            if g in quest.enrolled:
                quest.enrolled.remove(g)
            g.away = False
            g.assignment = None
            g.return_date = -1

            if quest.type == "quest":
                g.add_log("completed quest")
            elif quest.type == "class":
                g.add_log("completed class")

        def add_log(self, root, v = 1, _delay = 0):
            g = self.girl
            global temp_log

            k = root + str(calendar.time + _delay)

            ## Creates or increment daily log

            if k in g.log:
                g.log[k] += v
            else:
                g.log[k] = v

            ## Girl log garbage collection (attempt to improve performance)

            _old = root + str(calendar.time - 30)
            if _old in g.log:
                # Deletes entries 30 days prior
                del g.log[_old]

            ## Adds value to all time total

            if root in g.log:
                g.log[root] += v
            else:
                g.log[root] = v

            ## Tracking total game stats
            game.track(root, v)

            ## Tracking day stats
            if logs[calendar.time + _delay]:
                logs[calendar.time + _delay].track(root, v)
            else:
                logs[calendar.time + _delay] = Log(calendar.time + _delay)

        def get_log(self, root, days = 0): # If days = 0, get all time stats
            g = self.girl
            if days == 0:
                if root in g.log:
                    return g.log[root]
                else:
                    return 0

            elif days == "today":
                if (root + str(calendar.time)) in g.log:
                    return g.log[root + str(calendar.time)]
                else:
                    return 0

            else:

                total = 0

                for i in range(days):

                    if calendar.time - 1 - i > 0:
                        k = root + str(calendar.time - 1 - i)

                        if k in g.log:
                            total += g.log[k]
                        else:
                            total += 0

                    else:
                        break

                return total

        def get_average_performance(self, root, days):
            g = self.girl
            if g.get_log(root + "_score_base", days) != 0:

                perf = float(g.get_log(root + "_score", days)) / float(g.get_log(root + "_score_base", days))

                details = {}


                for r in ("perfect", "very good", "good", "average", "bad", "very bad",):

                    details[r] = str(round_int((100.0 * g.get_log(root + "_" + r, days) / g.get_log(root + "_score_base", days))))

                ttip = "Perfect: " + details["perfect"] + "%" + "           Average: " + details["average"] + "%" + "\nVery good: " + details["very good"] + "%" + "      Bad: " + details["bad"] + "%" + "\nGood: " + details["good"] + "%" + "              Very bad: " + details["very bad"] + "%"

                return round(perf, 1), ttip

            else:

                return "-", "This girl hasn't performed this action over the selected period."

        def track_event(self, type, arg=None, silent=False):
            g = self.girl
            # Only the latest occurance of an event type is kept in the list

            if not g.recent_events[type]: # copies the template event once if it doesn't exist
                g.recent_events[type] = copy.copy(recent_event_templates[type])

            # Updates time and description

            g.recent_events[type].time = calendar.time

            if arg:
                g.recent_events[type].description = g.recent_events[type].base_description % arg
            else:
                g.recent_events[type].description = g.recent_events[type].base_description

            if not silent:
                debug_notify("Tracking " + type + "...", pic=g.portrait)

            return

        def get_recent_events(self, day_number = 7, filter = None): # Events are returned with a tuple: Type, description, date
            g = self.girl
            event_list = []

            if g.recent_events:

                for type in g.recent_events.keys():
                    if g.recent_events[type]:
                        if g.recent_events[type].time in range(calendar.time - day_number, calendar.time+1):
                            if not filter or type == filter:
                                event_list.append(g.recent_events[type])

            event_list.sort(key = lambda x: x.time, reverse = True)

            return event_list # Returns a list sorted by date

        def get_recent_events_description(self, day_number = 7):
            g = self.girl
            description = ""
            events = g.get_recent_events(day_number)

#            renpy.notify(str(len(events)))

            if events:
                for ev in events:
                    description += calendar.get_date(ev.time) + ": " + ev.description
                    if g.remembers("reward", ev.type):
                        description += "{color=[c_emerald]} *rewarded* [emo_heart]{/color}"

                    if g.remembers("punish", ev.type):
                        description += "{color=[c_crimson]} *punished* [emo_broken_heart]{/color}"

                    description += "\n"


                if len(events) > 5:
                    description = __("{size=-1}") + description + "{/size}"
            else:
                description = calendar.get_date(calendar.time) + ": No recent events to report"

            return description

        def count_occurences(self, context="all", original=False, add_list=None):
            g = self.girl
            if not add_list:
                add_list = []

            i = 0

            if context == "all":
                mylist = MC.girls + farm.girls + game.free_girls + slavemarket.girls + MC.escaped_girls + add_list
                if isinstance(enemy_general, Girl):
                    mylist += [enemy_general]

            elif context == "player":
                mylist = MC.girls + farm.girls + MC.escaped_girls + add_list

            for gf in mylist:
                if gf != g:
                    if original:
                        if gf.original and gf.pack_name == g.pack_name:
                            i += 1
                    elif gf.pack_name == g.pack_name:
                        i += 1

            return i

        def will_remember(self, context, type, score):
            g = self.girl
            if g.recent_events[type]:

                if context == "reward":
                    g.recent_events[type].reward(score)

                elif context == "punish":
                    g.recent_events[type].punish(score)

        def remembers(self, context, type): # Remembering is more effective when the memory is fresh
            g = self.girl
            if g.recent_events[type]:
                if context == "reward":
                    if g.recent_events[type].rewarded > 0:
                        return g.recent_events[type].rewarded * g.get_effect("boost", "reward efficiency")
                elif context == "punish":
                    if g.recent_events[type].punished > 0:
                        return g.recent_events[type].punished * g.get_effect("boost", "punishment efficiency")

            return 0

        def forgets(self):
            g = self.girl
            for type in g.recent_events.keys():
                if g.recent_events[type]:
                    g.recent_events[type].refresh()
