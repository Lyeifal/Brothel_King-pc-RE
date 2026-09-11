Game Modes Mod — 说明 | README
================================

本 Mod 通过 Mod API v2 注册，mod_id 为 "game_modes"。

可被前置依赖 (Usable as a dependency)
-------------------------------------
其他 v2 Mod 可以声明本 Mod 为前置依赖。在 manifest 中加入：

    "dependencies": ["game_modes"]

语义（Mod API v2）：
- 本 Mod 未安装、未注册或被禁用时，声明了该依赖的 Mod 不会激活；
- 主菜单 "Mods"（Mod 管理界面）会把缺失的前置显示为"缺少前置"。

本 Mod 提供的前置内容：
- gamemode_registry 中的剧情/沙盒/剧本三种 GameMode 实例
  （game/custom/mods/Game Modes/ 下的 story_mode.rpy / sandbox_mode.rpy /
  scenario_mode.rpy）；
- 玩家出身注册表 origin_registry（SandboxMode 实例持有）；
- 社区剧本注册表 scenario_registry（ScenarioMode 实例持有）。

注意：Mod 只有在"激活"状态下才能注册模式/出身/剧本——请在注册块里用

    if services.mod_api_v2.is_mod_active("your_mod_id"):

保护有副作用的注册代码（参考本目录 mod.rpy 对 gamemode_registry 的注册方式）。

可被禁用 (Can be disabled)
--------------------------
本 Mod 的 manifest 声明了 "always_on": False，玩家可以在主菜单
"Mods"（Mod 管理界面）中禁用它；开关存于 persistent._bk_v2_mod_states，
重启游戏后完全生效。被禁用时，开局流程回退为纯剧情模式
（无模式选择界面，见 game/core/init/start.rpy 的 select_game_mode）。

卸载 = 删除本目录。 | Uninstall = remove this folder.
