# Girl Pack 系统架构

> 最后更新: 2026-09-11（与代码核对）
> **核心文件**: `game/core/framework/girl_files_dict.rpy`（416 行）、`game/core/framework/girl_factory.rpy`（833 行）、`game/core/framework/girlclass.rpy`（Girl 类）
> **数据**: `game/custom/girls/`（当前 102 个包）
> **编辑支持**: ✅ 女孩包编辑器（`tools/bk_editor/girl_pack_editor/` + 游戏内 `game/core/tools/girl_pack_editor/`）

---

## 1. 系统职责

Girl Pack 是内容扩展单元，每个包为一个文件夹：

- **`_BK.ini`**: 包元数据（姓名、作者、版本、标签、特质覆盖、生成选项）。由 `read_init_file()`（girl_factory.rpy:313）解析为 dict 缓冲，容忍用户笔误；文件损坏时抛 `AssertionError`（:328）。
- **图片资源**: 按命名约定打标（`portrait_*`、`profile_*`、行为标签等），由 TagRegistry 映射。
- **自定义 Trait/Perk 与对话**: `register_custom_tags_for_pack()`（girl_factory.rpy:515）、`register_custom_dialogue_for_pack()`（:535）。
- **packstates**: 打标状态的导入导出（`GirlFilesDict.import_packstates()`，girl_files_dict.rpy:259）。

## 2. 两大支柱

### 2.1 GirlFilesDict（girl_files_dict.rpy:12）

`class GirlFilesDict(NoRollback)` —— 全包文件的索引字典，init -3 实例化为 `globalFilesDict` 并注册服务 `services.girl_files_dict`（:412）。

- `__load_files()`（:17）经 `get_girl_path()` 建立 包名 → 文件列表 索引。
- 查询 API：`get_files()` / `contains_file()`（二分查找，:203）/ `get_pics()` / `get_tag_index()` / `get_pic_by_name()`。
- 统计 API：`get_totalcount()`（:174）/ `get_init_duration()`（:167，控制台可查加载耗时）。
- `reload_files()`（:246）供 AutoRepair 检测新增图片。

### 2.2 girl_factory.rpy 工厂函数

- `get_girl_path(file)`（:4）: 判定文件归属哪个包；下划线开头目录整体忽略，`#` 开头目录视为容器 mix。
- `generate_girls()`（:97）/ `create_girl(pack_name, ...)`（:131）/ `get_girl()`（:178）/ `get_girls()`（:181）: 女孩生成入口；v2 钩子 `girl_generated` 在 :278 触发。
- 生成约束：`can_generate()`（:613，数量/唯一性检查）、`can_spawn()`（:635，地点检查）、`randomize_girl_level()`（:777，按章节定级）。
- 包评分：`get_girlpack_rating()`（:691）与 `get_plus_rating()`（:741）评估包质量（图片数量/标签覆盖度），影响生成权重。
- `clone_init_dict()`（:549）支持模板克隆。

Girl 类本体见 [girl_components.md](girl_components.md)（组件化后 3,910 行）。

## 3. 包验证

三层验证：

1. **加载期**: `_BK.ini` 解析断言（girl_factory.rpy:328）；无有效图片的包自然进不了索引。
2. **游戏内编辑器**: `game/core/tools/girl_pack_editor/pack_editor_state.rpy:45` `validate_pack(pack_name)`：
   - 无图片 → `"No images found"`；
   - 缺 `profile` 标签 → 必需（显示用）；缺 `portrait` 标签 → 建议。
   - `_BK.ini` 缺失/非法单独报 issue。
3. **桌面编辑器**: `tools/bk_editor/girl_pack_editor/` 提供打标 + INI 编辑 + 验证的完整工具链（见 [editor_suite.md](editor_suite.md)）。

## 4. 系统间联系

```
game/custom/girls/<pack>/ (_BK.ini + 图片)
    └─→ GirlFilesDict (init -3 索引, 服务 girl_files_dict)
           ├─→ get_girl_path 归属判定
           ├─→ tag_dict/TagRegistry 标签解析
           └─→ girl_factory
                  ├─→ create_girl/get_girl → Girl(...).randomize()
                  │        └─→ v2 钩子 girl_generated (girl_factory.rpy:278)
                  ├─→ can_generate/can_spawn 生成约束
                  └─→ get_girlpack_rating 包质量评分
```

## 5. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 桌面女孩包编辑器 | ✅ 完整 | 打标、INI、Trait/Perk、验证（`tools/bk_editor/girl_pack_editor/`） |
| 游戏内包编辑器 | ✅ | `game/core/tools/girl_pack_editor/`，含 `validate_pack` |
| `screen mods` / girlpack_menu | ✅ | 包管理界面（screens.rpy 的 `girlpack_menu` label） |

---

## 相关文档

- [girl_components.md](girl_components.md) — Girl 类组件化
- [trait_perk.md](trait_perk.md) — 包自定义 Trait/Perk
- [registry.md](registry.md) — TagRegistry 标签映射
- [editor_suite.md](editor_suite.md) — 编辑器套件
