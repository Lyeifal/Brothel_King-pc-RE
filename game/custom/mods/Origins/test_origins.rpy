################################################################################
##  Origins Mod — 冒烟测试
##  EN: Smoke tests for the origins registry and class injection. Called from
##      the core test runner (label bk_test_runner) via renpy.has_label, so
##      disabling/uninstalling this mod silently skips them.
##  ZH: 出身注册表与职业注入的冒烟测试。由核心测试运行器
##      （label bk_test_runner）经 renpy.has_label 调用——禁用或卸载本
##      Mod 时自动跳过。
################################################################################

label test_origins_mod:

    python:
        runner = TestRunner.instance()

        _oreg = globals().get("origin_registry")
        if _oreg is None or not hasattr(_oreg, "list_origins"):
            # EN: Mod disabled/uninstalled — nothing to test.
            # ZH: Mod 被禁用/卸载——无事可测。
            runner.skip("Origins registry unavailable (mod disabled?)")
        else:
            _run_origins_tests(runner)

    return


init -1 python:

    def _run_origins_tests(runner):
        """
        EN: Body of the Origins smoke test, kept in an init-level function so
            the label stays a thin wrapper (no early-return constraints in
            Ren'Py label python blocks).
        ZH: Origins 冒烟测试主体，放在 init 层函数中，使 label 保持
            薄封装（规避 Ren'Py label python 块不允许 early-return 的
            限制）。
        """
        _oreg = origin_registry
        _origins = _oreg.list_origins()

        # EN: Data integrity — five origins, each granting a unique class
        #     with a non-empty spell tree.
        # ZH: 数据完整性——五个出身，各授予带非空技能树的独特职业。
        runner.assert_eq(len(_origins), 5, "Origins registry holds 5 origins")

        _ids = set()
        for _o in _origins:
            _ids.add(_o.origin_id)
            runner.assert_true(bool(_o.class_id), "origin %s grants a class_id" % _o.origin_id)
            runner.assert_true(len(_o.class_def.get("spellbook", [])) >= 7,
                               "origin %s class has a spell tree (>=7 spells)" % _o.origin_id)
            runner.assert_true(len(_o.talents) >= 1,
                               "origin %s grants at least one talent" % _o.origin_id)
            for _t in _o.talents:
                for _e in _t.effects:
                    runner.assert_true(_e.target, "origin %s talent %s effect has a target" % (_o.origin_id, _t.talent_id))

        runner.assert_eq(len(_ids), 5, "origin ids are unique")

        # EN: Class ids must be distinct from the three base classes.
        # ZH: 出身职业 ID 不得与三个基础职业冲突。
        for _base in ("Warrior", "Wizard", "Trader"):
            runner.assert_true(_base not in [_o.class_id for _o in _origins],
                               "origin class does not clash with base class %s" % _base)

        # EN: Starting-bonus application on a fake MC. FakeMC implements the
        #     fields apply_to_mc touches (talents with zero effects + bonus
        #     keys) so the test needs no running game instance.
        # ZH: 在假 MC 上验证起始奖励的应用。FakeMC 实现了 apply_to_mc
        #     会触碰的字段（零效果天赋 + 奖励键），无需运行中的游戏实例。
        # EN: add_effects appends to thing.effects / thing.effect_dict, so the
        #     fake MC carries the same minimal surface the real EffectBearer
        #     has (plain list + defaultdict of lists).
        # ZH: add_effects 会向 thing.effects / thing.effect_dict 追加，因此
        #     假 MC 带上了与真实 EffectBearer 相同的最小接口（普通 list +
        #     defaultdict(list)）。
        class _OrigFakeMC(object):
            def __init__(self):
                self.gold = 0
                self.prestige = 0
                self.good = 0
                self.neutral = 0
                self.evil = 0
                self.effects = []
                self.effect_dict = defaultdict(list)

        for _o in _origins:
            _mc = _OrigFakeMC()
            _o.apply_to_mc(_mc)
            for _k, _v in _o.starting_bonus.items():
                runner.assert_eq(getattr(_mc, _k), _v,
                                 "origin %s starting bonus %s+%s applied" % (_o.origin_id, _k, _v))

        # EN: Class injection needs the store registries rebuilt by label
        #     init_spells (game started). From the main menu they may not
        #     exist yet — skip rather than fail.
        # ZH: 职业注入依赖 label init_spells（游戏已开始）重建的 store
        #     注册表。主菜单环境下可能尚未存在——跳过而非失败。
        if "all_player_classes" not in globals():
            runner.skip("Origins class injection (needs started game)")
            return

        origins_ensure_classes()

        _apc = globals()["all_player_classes"]
        _pics = globals()["playerclass_pics"]
        _descs = globals()["MC_playerclass_description"]
        _stats = globals()["MC_CLASS_STAT_DEFS"]
        _book = globals()["spellbook"]

        for _o in _origins:
            _cid = _o.class_id
            runner.assert_true(_cid in _apc, "origin class %s registered in all_player_classes" % _cid)
            runner.assert_true(_cid in _pics, "origin class %s has an icon entry" % _cid)
            runner.assert_true(_cid in _descs, "origin class %s has a description entry" % _cid)
            runner.assert_true(_cid in _stats, "origin class %s has stat defs" % _cid)
            runner.assert_true(_cid in _book and len(_book[_cid]) >= 7,
                               "origin class %s spellbook injected (>=7 spells)" % _cid)
            runner.assert_true("story" in _apc[_cid].get("modes", []),
                               "origin class %s available in story mode" % _cid)

        # EN: get_available_player_classes surfaces the origin classes too.
        # ZH: get_available_player_classes 也会列出出身职业。
        _avail = get_available_player_classes()
        for _o in _origins:
            runner.assert_true(_o.class_id in _avail,
                               "origin class %s offered on the setup page" % _o.class_id)
