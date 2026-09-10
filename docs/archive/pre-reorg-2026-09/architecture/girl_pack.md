# Girl Pack 系统架构

> **文件**: `game/core/framework/girlclass.rpy` (Girl 类), `game/core/framework/girl_factory.rpy`, `game/core/framework/girl_files_dict.rpy`  
> **数据**: `game/custom/girls/` (官方与社区女孩包)  
> **编辑支持**: ✅ 女孩包编辑器 (`girl_pack_editor`)

---

## 1. 系统职责

Girl Pack 是 Brothel King 的内容扩展单元，每个包包含：

- **`_BK.ini`**: 包元数据（名称、作者、版本、标签、特质覆盖、互动提示）。
- **图片资源**: 按命名约定组织的 PNG/WebP/AVIF 文件（如 `portrait_*`, `profile_*`, `act_*`, `naked_*` 等）。
- **自定义 Trait/Perk**: 包内可声明专属特质，通过编辑器创建。
- **对话覆盖**: 可选的 `_dialogue.rpy` 文件覆盖默认对话。

核心流程：
1. 游戏启动时扫描 `game/custom/girls/` 下的包目录。
2. 解析 `_BK.ini` 构建 `GirlPack` 对象。
3. 玩家招募时从包中实例化 `Girl`，加载图片标签映射。

---

## 2. 解耦方式

- **与 Girl 类解耦**: `GirlPack` 是工厂/数据源，`Girl` 是运行时实体。`Girl` 不直接依赖包目录结构，只通过 `GirlPack` 提供的接口获取图片路径和初始属性。
- **与 Trait/Perk 解耦**: 包内自定义 Trait/Perk 通过 `TraitRegistry` / `PerkRegistry` 注册，不直接修改全局字典。
- **与主游戏解耦**: 所有女孩包统一放在 `game/custom/girls/`，与引擎代码隔离，避免更新时冲突。

---

## 3. 系统间联系

```
game/custom/girls/
    └─→ <pack_name>/
           ├─→ _BK.ini          → GirlPack 元数据
           ├─→ portrait/*.png   → TagRegistry 图片标签
           ├─→ profile/*.png
           ├─→ act/*.png
           └─→ _dialogue.rpy    → DialogueRegistry (可选)
                  └─→ Girl.__init__()
                         ├─→ TraitRegistry  (初始特质)
                         ├─→ PerkRegistry   (初始天赋)
                         └─→ TagRegistry    (图片标签)
```

- `Girl.generate()` 从 `GirlPack` 获取基础属性模板，再结合随机因子生成具体数值。
- `HookManager.on_girl_generate` 允许 Mod 在女孩生成后修改属性。

---

## 4. 编辑器支持

| 编辑器 | 支持情况 | 说明 |
|--------|---------|------|
| 女孩包编辑器 (`girl_pack_editor`) | ✅ 完整 | `_BK.ini` 可视化编辑、图片批量打标、Trait/Perk 创建器、包完整性验证 |
| 图片打标工具 | ✅ 完整 | 支持 WebP/AVIF/PNG/JPG；自动建议标签；批量重命名 |

---

## 5. 向后兼容

- `_BK.ini` 格式保持向后兼容，新增字段（如 BK Evolution 的 `custom_traits`、`interact_prompt`）为可选。
- 旧包缺少 `custom_traits` 时，女孩使用全局注册表中的默认特质。
- `GirlPack` 加载失败时不阻止游戏启动，只跳过该包并记录警告。
