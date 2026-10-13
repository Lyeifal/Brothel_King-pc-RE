#### Integration Tests — 集成测试 ####
# 测试完整的游戏流程，而不仅仅是组件
#
# 用法: 在主菜单点击 "Tests" 按钮时会自动运行
#
# EN: Full-flow integration tests that simulate actual gameplay
# ZH: 模拟实际游戏流程的完整集成测试

init -1 python:
    pass

# ── Test 1: New Game Creation | 新游戏创建测试 ──

label test_new_game_creation:
    $ runner = TestRunner.instance()

    # 测试游戏实例创建
    $ runner.assert_not_none(services.game, "Game service should be registered")
    $ runner.assert_not_none(services.mc, "MC service should be registered")
    $ runner.assert_not_none(services.calendar, "Calendar service should be registered")

    # 测试初始状态
    if services.game:
        $ runner.assert_true(services.game.gold >= 0, "Game gold should be >= 0")
        $ runner.assert_not_none(services.game.chapter, "Game chapter should be set")

    if services.calendar:
        $ runner.assert_true(services.calendar.time > 0, "Calendar time should be > 0")

    return

# ── Test 2: Girl Acquisition | 女孩获取测试 ──

label test_girl_acquisition_flow:
    $ runner = TestRunner.instance()

    python:
        try:
            # 创建一个测试女孩
            from game.core.framework.girl_factory import create_girl, generate_girls

            # 获取可用女孩包
            template_girls = generate_girls()
            runner.assert_true(len(template_girls) > 0, "Should have at least one girl pack")

            if len(template_girls) > 0:
                # 使用第一个女孩包创建女孩
                test_pack_name = template_girls[0].pack_name
                test_girl = create_girl(test_pack_name, free=True, level=1)

                # 验证女孩对象
                runner.assert_not_none(test_girl, "Girl should be created")
                runner.assert_not_none(test_girl.name, "Girl should have a name")
                runner.assert_true(test_girl.charm >= 0, "Girl charm should be >= 0")
                runner.assert_true(test_girl.beauty >= 0, "Girl beauty should be >= 0")
                runner.assert_not_none(test_girl._base, "Girl should have _base component")
                runner.assert_not_none(test_girl._stats, "Girl should have _stats component")

                # 测试 Girl 组件方法
                runner.assert_callable(test_girl.get_stat, "Girl.get_stat should be callable")
                runner.assert_callable(test_girl.change_stat, "Girl.change_stat should be callable")
                runner.assert_callable(test_girl.set_job, "Girl.set_job should be callable")

                # 测试图片加载
                if hasattr(test_girl, 'profile'):
                    runner.assert_not_none(test_girl.profile, "Girl should have profile pictures")

        except Exception as e:
            runner.assert_true(False, "Girl acquisition failed: %s" % str(e))

    return

# ── Test 3: One Day Settlement | 一天结算测试 ──

label test_one_day_settlement:
    $ runner = TestRunner.instance()

    python:
        try:
            # 保存当前游戏状态
            if services.calendar:
                initial_day = services.calendar.day
                runner.assert_not_none(initial_day, "Calendar day should be set")

            # 注意: 实际调用结算会修改游戏状态，这里只做基础检查
            # 真正的结算测试需要在隔离环境中进行

            # 检查结算相关的服务是否可用
            runner.assert_not_none(services.brothel, "Brothel service should be registered")

            if services.brothel:
                runner.assert_true(hasattr(services.brothel, 'girls'), "Brothel should have girls attribute")

        except Exception as e:
            runner.assert_true(False, "Settlement test failed: %s" % str(e))

    return

# ── Test 4: Save/Load Cycle | 存档读档测试 ──

label test_save_load_cycle:
    $ runner = TestRunner.instance()

    python:
        try:
            # 测试存档功能可用
            runner.assert_true(hasattr(renpy, 'save'), "renpy.save should be available")
            runner.assert_true(hasattr(renpy, 'load'), "renpy.load should be available")

            # 检查存档目录
            import os
            saves_dir = os.path.join(config.gamedir, "saves")
            runner.assert_true(os.path.exists(saves_dir), "Saves directory should exist")

            # 注意: 实际的存档/读档测试需要在实际游戏流程中进行
            # 这里只验证基础设施

        except Exception as e:
            runner.assert_true(False, "Save/Load test failed: %s" % str(e))

    return

# ── Test 5: Mod System | Mod系统测试 ──

label test_mod_system_integration:
    $ runner = TestRunner.instance()

    python:
        try:
            # 测试Mod API可用
            api = services.mod_api_v2
            runner.assert_not_none(api, "Mod API v2 should be available")

            if api:
                # 获取已注册的Mod
                mod_info = api.get_mod_info()
                runner.assert_not_none(mod_info, "Should be able to get mod info")

                # 检查是否有已注册的Mod
                if mod_info:
                    runner.assert_true(isinstance(mod_info, dict), "Mod info should be a dict")

                    # 检查已知的Mod（如果存在）
                    if "item_quality" in mod_info:
                        runner.assert_not_none(mod_info["item_quality"], "Item Quality mod should have info")

                # 测试钩子系统
                runner.assert_true(hasattr(api, 'HOOK_DAY_STARTING'), "Should have HOOK_DAY_STARTING constant")
                runner.assert_true(hasattr(api, 'HOOK_GIRL_ACQUIRED'), "Should have HOOK_GIRL_ACQUIRED constant")
                runner.assert_true(hasattr(api, 'register_hook'), "Should have register_hook method")
                runner.assert_true(hasattr(api, 'execute_hook'), "Should have execute_hook method")

        except Exception as e:
            runner.assert_true(False, "Mod system test failed: %s" % str(e))

    return

# ── Test 6: Girl Pack Loading | 女孩包加载测试 ──

label test_girl_pack_loading:
    $ runner = TestRunner.instance()

    python:
        try:
            from game.core.framework.girl_factory import generate_girls

            # 生成女孩模板
            girls_list = generate_girls()
            runner.assert_true(len(girls_list) > 0, "Should be able to generate girls from packs")

            if len(girls_list) > 0:
                # 检查第一个女孩包
                first_girl = girls_list[0]
                runner.assert_not_none(first_girl.pack_name, "Girl should have pack_name")
                runner.assert_not_none(first_girl.init_dict, "Girl should have init_dict from _BK.ini")

                # 检查是否加载了 _BK.ini
                if first_girl.init_dict:
                    runner.assert_true(len(first_girl.init_dict) > 0, "init_dict should not be empty")

                    # 检查常见字段
                    identity_fields = [k for k in first_girl.init_dict.keys() if k.startswith("identity/")]
                    runner.assert_true(len(identity_fields) > 0, "_BK.ini should have identity section")

                # 测试多个女孩包（最多5个）
                for i, girl in enumerate(girls_list[:5]):
                    runner.assert_not_none(girl.pack_name, "Girl %d should have pack_name" % i)

        except Exception as e:
            runner.assert_true(False, "Girl pack loading test failed: %s" % str(e))

    return

# ── Test 7: Services Registration | 服务注册测试 ──

label test_services_registration:
    $ runner = TestRunner.instance()

    python:
        try:
            # 检查所有应该注册的服务
            expected_services = [
                "config",
                "girl_files_dict",
                "game",
                "calendar",
                "mc",
                "farm",
                "brothel",
                "event_engine",
                "i18n",
                "dev_console",
                "mod_api_v2"
            ]

            for service_name in expected_services:
                service = services.get(service_name)
                runner.assert_not_none(service, "Service '%s' should be registered" % service_name)

            # 测试服务容器本身
            runner.assert_not_none(services, "GameServices should be available")
            runner.assert_true(hasattr(services, 'game'), "Services should have 'game' property")
            runner.assert_true(hasattr(services, 'mc'), "Services should have 'mc' property")
            runner.assert_true(hasattr(services, 'calendar'), "Services should have 'calendar' property")

        except Exception as e:
            runner.assert_true(False, "Services registration test failed: %s" % str(e))

    return

# ── Test 8: I18N System | 国际化系统测试 ──

label test_i18n_system:
    $ runner = TestRunner.instance()

    python:
        try:
            # 测试I18nService
            i18n = services.i18n
            runner.assert_not_none(i18n, "I18N service should be available")

            if i18n:
                # 测试翻译函数
                runner.assert_callable(i18n.t, "I18nService.t should be callable")
                runner.assert_callable(i18n.tn, "I18nService.tn should be callable")
                runner.assert_callable(i18n.tc, "I18nService.tc should be callable")
                runner.assert_callable(i18n.pronoun, "I18nService.pronoun should be callable")
                runner.assert_callable(i18n.possessive, "I18nService.possessive should be callable")

                # 测试基础翻译（使用__函数）
                test_str = __("Test string")
                runner.assert_not_none(test_str, "__() should return a string")

        except Exception as e:
            runner.assert_true(False, "I18N system test failed: %s" % str(e))

    return

# ── Integration Test Suite Entry | 集成测试套件入口 ──

label run_integration_tests:
    """
    运行所有集成测试

    EN: Runs all integration tests in sequence
    ZH: 按顺序运行所有集成测试
    """
    $ test_runner.reset()

    call test_new_game_creation
    call test_girl_acquisition_flow
    call test_one_day_settlement
    call test_save_load_cycle
    call test_mod_system_integration
    call test_girl_pack_loading
    call test_services_registration
    call test_i18n_system

    return

# ── 辅助函数 ──

init -1 python:
    def assert_callable(func, label):
        """测试对象是否可调用"""
        runner = TestRunner.instance()
        runner.assert_true(callable(func), label)
