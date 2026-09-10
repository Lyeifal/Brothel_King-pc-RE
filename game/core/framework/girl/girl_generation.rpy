#### GirlGeneration — Girl random generation component | 女孩随机生成组件 ####
# Phase 2.1: 女孩初始化与随机生成 | Girl initialization and random generation
# Methods: randomize

init -2 python:

    class GirlGeneration(object):
        '''女孩随机生成 | Random generation for a Girl'''

        def __init__(self, girl):
            # 持有 Girl 实例引用 | Hold reference to the Girl instance
            self.girl = girl

        def randomize(self, free=False, p_traits=None, n_trait=None, perks=None, force_original=False, level=1, personality=None, temp_list=None):
            '''随机生成女孩 | Randomize a girl (name, personality, stats, traits, preferences, pictures)'''
            g = self.girl

            # 性能计时埋点（原样保留）| Performance timing instrumentation (preserved as-is)
            t0 = time.perf_counter()
            game.func_time_log2 = "\nstart: %s" % t0

            # 1. INIT GIRL

            g.free = free

            # Has a chance to generate original if it doesn't exist, otherwise creates a clone:
            # 'original' attribute stores the source for debugging

            if force_original:
                g.original = "forced original"
            elif g.is_unique():
                g.original = "unique"
            elif g.free and dice(100)<=15 and not g.count_occurences("all", original=True, add_list=temp_list) > 0:
                g.original = "random free"
            elif not free and dice(100)<=5 and not g.count_occurences("all", original=True, add_list=temp_list) > 0:
                g.original = "random slave"
            else:
                g.original = False

            if not g.original and g.ini:
                g.init_dict = clone_init_dict(g.init_dict)

            g.set_name()
            g.activation_date = calendar.time
            g.talked_to_date = None
            g.recent_events = defaultdict(list)
            g.relations = defaultdict(int)

            t1 = time.perf_counter()
            game.func_time_log2 += "\ninit: %s" % (t1 - t0)

            # 2. PERSONALITY

            g.generate_personality(personality)

            t2 = time.perf_counter()
            game.func_time_log2 += "\npersonality: %s" % (t2 - t1)

            t3 = g.generate_background(t2)

            # 3. LEVEL AND REGULAR SKILLS

            g.adjust_level(level)
            g.generate_stats()

            t4 = time.perf_counter()
            game.func_time_log2 += "\nstats: %s" % (t4 - t3)

            # 4. TRAITS AND PERKS

            g.generate_traits(p_traits, n_trait)

            if perks:
                for perk in perks:
                    g.acquire_perk(perk, forced=True)

            t5 = time.perf_counter()
            game.func_time_log2 += "\ntraits: %s" % (t5 - t4)

            g.update_can_perk() # This is not checked dynamically for performance

            # 5. ADJUSTMENTS

            g.auto_upkeep = True
            g.upkeep = -1
            g.upkeep_ratio = 1.0
            g.locked_upkeep = None
            g.generate_preferences()
            t6 = time.perf_counter()
            game.func_time_log2 += "\npreferences: %s" % (t6 - t5)

            g.upkeep = g.get_med_upkeep()
            g.energy = g.get_stat_minmax("energy")[1]
            g.init_sanity() # Used as a limit on farm powers (degrades over time, unrecoverable)
            g.last_power = 0
            g.broken = False
            g.streetdays = 0
            g.interactions = 0
            g.reset_interactions()

            # 6. PICTURES AND CHAR

            g.refresh_pictures(silent=True)

            t7 = time.perf_counter()
            game.func_time_log2 += "\nrefresh pictures: %s" % (t7 - t6)

            # Creating girl character (for talking)

            g.create_char()

            t8 = time.perf_counter()
            game.func_time_log2 += "\nchar creation: %s" % (t8 - t7)

            game.func_time_log2 += "\nend: %s" % t8
            game.func_time_log2 += "\ntotal time: %s" % (t8 - t0)
