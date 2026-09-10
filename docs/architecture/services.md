# GameServices 服务容器架构

> 最后更新: 2026-09-11（与代码核对）
> **核心文件**: `game/core/systems/services/service_container.rpy`、`game/core/config/game_config.rpy`
> **Phase**: Phase 1（服务容器化，替代散落的模块级全局单例）

---

## 1. 系统职责

`GameServices` 是全游戏的服务定位器（Service Locator），把 `game`、`MC`、`brothel` 等原本以模块级全局变量存在的单例，收敛到一个容器中统一管理：

- **统一注册/获取**: `register(key, service)` / `get(key, default)` / `has(key)` / `require(key)`（未注册时抛 `RuntimeError`）。
- **类型化属性访问**: `services.game`、`services.mc`、`services.brothel` 等 IDE 友好的 property 访问器。
- **依赖断言**: `require_service(key)`（service_container.rpy:137，init -11）供各 init 块在开头的依赖检查。
- **生命周期**: `unregister(key)` 用于游戏重置（game reset）时清理。

设计目标（见文件头注释 service_container.rpy:6-13）：先建容器（init -12），各服务在自己原有的 init 层级注册，旧的全局变量保留为别名，旧代码无需修改即可继续工作，新代码逐步迁移到 `services.xxx`。

## 2. 已注册的 11 个服务

以下注册点全部经 grep 逐一核实：

| # | Key | 注册位置 | 注册时机 | 说明 |
|---|-----|---------|---------|------|
| 1 | `config` | `game/core/config/game_config.rpy:121` | init -11 | `GameConfig` 实例（见第 4 节） |
| 2 | `i18n` | `game/core/systems/services/i18n_service.rpy:121` | init -10 | `I18nService`，包装 Ren'Py `__()`，支持复数/语境/性别 |
| 3 | `event_engine` | `game/core/systems/events/event_engine.rpy:202` | init -4 | `EventEngine` 单例 |
| 4 | `girl_files_dict` | `game/core/framework/girl_files_dict.rpy:412` | init -3 | `globalFilesDict`（`GirlFilesDict` 实例） |
| 5 | `mod_api_v2` | `game/core/systems/mods/mod_api_v2.rpy:206` | init -3 | `ModAPIV2` 单例 |
| 6 | `game` | `game/core/init/start.rpy:245` | 运行时（label start） | `Game` 实例创建后注册 |
| 7 | `calendar` | `game/core/init/start.rpy:246` | 运行时（label start） | `Calendar` 实例 |
| 8 | `mc` | `game/core/init/start.rpy:339` | 运行时（label start） | `MC` 实例（`# Phase 1.1` 注释） |
| 9 | `farm` | `game/core/init/start.rpy:557` | 运行时（label start） | `Farm` 实例 |
| 10 | `brothel` | `game/core/systems/events_dispatcher.rpy:753` | 运行时（ brothel 创建流程中） | `Brothel` 实例 |
| 11 | `dev_console` | `game/core/tools/dev_console/console_commands.rpy:120` | 运行时（开发控制台开启时） | 游戏内开发控制台 |

注意：容器上还定义了 `mod_api` 和 `data_loader` 两个 property（service_container.rpy:106-119），但**没有任何地方调用 `services.register("mod_api", ...)` 或 `services.register("data_loader", ...)`**（已 grep 全库确认）——这两个访问器当前恒返回 `None`，属于为后续迁移预留的接口。

## 3. Init 优先级链

优先级表（service_container.rpy:152-159 注释 + 逐文件核实）：

```
init -12: GameServices 单例创建（service_container.rpy:15）—— 所有游戏代码之前
init -11: require_service() 辅助函数（service_container.rpy:135）
          GameConfig 注册 "config"（game_config.rpy:8）
          DataLoader 类定义（data_loader.rpy:7）
          EventBridge 单例（event_bridge.rpy:18）
init -10: Registry 基类（registry/registry.rpy:5）
          I18nService 注册 "i18n"（i18n_service.rpy，init -10）
          Goal / GameMode 类定义（framework/goal.rpy:2、systems/gamemodes/gamemode.rpy:6）
init -4:  HookManager（mods/mod_hooks.rpy:4）
          EventEngine 注册 "event_engine"（events/event_engine.rpy:7）
init -3:  ModAPI（mods/mod_api.rpy:4）、ModAPIV2 注册 "mod_api_v2"（mods/mod_api_v2.rpy:15）
          GirlFilesDict 注册 "girl_files_dict"（girl_files_dict.rpy:412）
init -2:  Girl 类与 15 个组件（framework/girlclass.rpy:7）
          v2 game_saved 钩子接入 Ren'Py 存档回调（mod_api_v2.rpy:209-219）
init -1:  DataLoader 驱动的难度表 JSON 覆盖（data_loader.rpy:1309）
init（label start，运行时）:
          game/calendar（start.rpy:245-246）→ DataLoader.load_all()（start.rpy:258）
          → mc（start.rpy:339）→ farm（start.rpy:557）→ brothel（events_dispatcher.rpy:753）
```

前 5 级（-12 ~ -2）是类与单例的定义期；真正的实体（game、MC、brothel 等）在 `label start` 运行期才注册。这也是容器 `require()` 报错信息提示"Check init priority ordering"的原因——依赖必须按上表先后注册。

## 4. GameConfig 集中配置

`GameConfig`（game_config.rpy:10，init -11）是所有可调参数的单一事实来源：

- **默认值**: `_load_defaults()`（game_config.rpy:22）覆盖女孩包目录、图片缓存（144）、自动存档（频率 200、12 槽）、显示（1920×1080）、玩法（难度、作弊开关）、i18n 默认语言、性能阈值等。
- **JSON 覆盖**: `_load_json_overrides()`（game_config.rpy:63）读取 `game/custom/config/*.json`，叠加到默认值之上（`dict.update`），对 Mod 友好。JSON 缺失或非法时静默忽略（try/except pass）。
- **访问方式**: `services.config.get(key, default)` / `.set(key, value)` / `.all()`，及常用 property（`girl_directories`、`image_cache_size`、`debug` 等）。

## 5. 解耦方式

- **与全局命名空间解耦**: 新代码通过 `services.xxx` 取依赖，不再各自 `global` 声明；旧全局变量作为兼容别名保留。
- **与 init 顺序解耦**: 各服务在自己原有的 init 层级注册，容器不强制统一的注册时刻，只保证容器本身足够早（-12）。
- **与调用方解耦**: `get(key, default)` 允许调用方对可选服务（如 `dev_console`）做空值降级；`require(key)` 用于必选服务，让顺序错误在 init 阶段立刻报错而非运行期静默出错。

## 6. 已知限制

- `mod_api` / `data_loader` 两个 property 未接线（见第 2 节）。
- 服务容器仍是单例模式（`GameServices._instance`），未做接口抽象；interfaces/ 目录（`i_event_service.rpy`、`i_girl_service.rpy`、`i_mod_service.rpy`）已有抽象接口定义，属于 Phase 1.2 的后续工作。

---

## 相关文档

- [registry.md](registry.md) — 注册表体系（多个服务依赖注册表）
- [mod_system.md](mod_system.md) — ModAPI v1/v2 均通过服务容器访问
- [event.md](event.md) — event_engine 服务的注册与事件桥
- [girl_components.md](girl_components.md) — Girl 组件化（与服务容器同批 Phase 工程）
