# DataLoader 系统架构

> **文件**: `game/core/systems/data_loader.rpy`  
> **调用时机**: `init -1`（类定义）；`label init_game`（运行时一次性加载）  
> **数据目录**: `game/core/data/`

---

## 1. 系统职责

DataLoader 是 BK Evolution 中所有 JSON 驱动内容的统一加载入口：

- **一次性加载**: 每个 JSON 文件在会话期间只解析一次，结果缓存到对应注册表。
- **安全降级**: 文件不存在、格式错误或字段缺失时，静默跳过并 `renpy.notify()` 提示，不阻止游戏启动。
- **多类别支持**: Trait、Perk、Origin、StoryEvent、SandboxEvent、Scenario、Achievement、Difficulty、NGP Settings、Meta Progression 等。

核心方法：
- `DataLoader.load_all()` — 加载所有类别。
- `DataLoader.reset_cache()` — 清除缓存，支持运行时重载（调试用途）。
- `DataLoader._load_json_file(rel_path)` — 通过 `renpy.loadable()` / `renpy.open_file()` 安全读取。

---

## 2. 解耦方式

- **与游戏逻辑解耦**: DataLoader 只负责读取和构造对象，不干预游戏逻辑。构造后的对象交给各注册表管理。
- **与注册表解耦**: DataLoader 知道注册表的接口（如 `trait_registry.register_trait()`），但不依赖注册表内部实现。
- **与文件系统解耦**: 使用 Ren'Py 的 `renpy.loadable()` / `renpy.open_file()` 而非原生 Python IO，确保在打包后的游戏（如 Android/Steam）中也能工作。

---

## 3. 系统间联系

```
game/core/data/
    ├─→ traits/traits.json                → DataLoader.load_traits()
    ├─→ perks/perks.json                  → DataLoader.load_perks()
    ├─→ sandbox/origins.json              → DataLoader.load_origins()
    ├─→ events/event_dict.json            → DataLoader.load_story_events()
    ├─→ sandbox/events.json               → DataLoader.load_sandbox_events()
    ├─→ scenarios/scenarios.json          → DataLoader.load_scenarios()
    ├─→ achievements/achievements.json    → DataLoader.load_achievements()
    ├─→ difficulty/difficulty.json        → DataLoader.load_difficulty()
    ├─→ settings/ngp_settings.json        → DataLoader.load_ngp_settings()
    ├─→ meta/meta_progression.json        → DataLoader.load_meta_progression()
    └─→ goals/chapter_goals.json          → 由 init/settings.rpy 加载（未来可能统一进 DataLoader）
           └─→ 各注册表 (TraitRegistry, PerkRegistry, EventRegistry, ...)
                  └─→ 游戏运行时系统 (Girl, EventEngine, Game, ...)
```

- `settings.rpy` 中的 `chapter_goals` / `chapter_titles` 等也采用相同的 JSON-first 策略，但由 `settings.rpy` 自身加载，不经过 DataLoader（历史原因，未来可能统一）。

---

## 4. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 所有编辑器 | ✅ 间接 | 编辑器产出 JSON → DataLoader 加载 → 游戏生效。编辑器不负责调用 DataLoader |
| 开发控制台 (`data_sync.py`) | ✅ 支持 | 批量验证 JSON 格式、Schema 校验、格式化 |

---

## 5. 向后兼容

- `DataLoader._load_json_file()` 返回 `None` 时，调用方（如 `load_traits()`）直接 `return`，不修改注册表，旧数据保持有效。
- `from_dict()` 方法普遍使用 `.get(key, default)`，兼容字段缺失的旧 JSON。
- 硬编码回退字典在所有数据驱动化点保留，确保无 JSON 时游戏仍能启动。
