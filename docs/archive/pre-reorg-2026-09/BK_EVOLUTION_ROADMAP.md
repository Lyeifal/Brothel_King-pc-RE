# BK Evolution 编辑器工具链 — 计划与进度

> **项目**: Brothel King Evolution (数据驱动改造 + 可视化编辑器)  
> **分支**: `bk-evolution`  
> **技术栈**: Ren'Py 8.2.0, Python 3.9, tkinter (零第三方依赖)

---

## 一、项目目标

将 BK 从一个纯代码驱动的 Ren'Py 视觉小说，改造为**数据驱动 + 可视化编辑**的 Mod 友好型框架：

1. **编辑器工具链**: 提供一个独立 GUI 工具 `python tools/bk_editor.py`，让非程序员也能制作 Mod 内容
2. **数据驱动改造**: 将硬编码的 Trait、Perk、Origin、StoryEvent、Scenario 等逐步提取到 JSON
3. **Mod 生态**: 女孩包统一放在 `game/custom/girls/`，保持 `_BK.ini` 兼容；剧本/数据 Mod 通过 `game/core/data/` 和编辑器产出
4. **零新增 Lint 错误**: 所有改动保持 `lint` 通过

---

## 二、总体进度概览

| Phase | 内容 | 状态 | 完成度 |
|---|---|---|---|
| A | 基础设施 (核心模块、JSON Schema、目录结构) | ✅ COMPLETED | 100% |
| B | 剧情事件编辑器 + 出身编辑器 | ✅ COMPLETED | 100% |
| C | 女孩系统编辑器 (Trait/Perk CRUD + Effect 可视化) | ✅ COMPLETED | 100% |
| D | 硬编码导出 JSON | ✅ COMPLETED | 100% |
| E | 女孩包制作工具 (`_BK.ini` 可视化) | ✅ COMPLETED | 100% |
| F | 剧本编辑器完善 (Scenario CRUD) | ✅ COMPLETED | 100% |
| G | 代码去硬编码 (逐步从 .rpy 迁移到 JSON) | ✅ COMPLETED | 95% |

---

## 三、Phase A — 基础设施 ✅

### 已完成
- [x] 创建 `tools/bk_editor/` 包结构
- [x] 创建 `game/core/data/` 目录及子目录 (`traits/`, `perks/`, `sandbox/`, `stories/`, `scenarios/`)
- [x] 编写 JSON Schema (`_schemas/*.json`)，支持数据验证
- [x] 编写 `core.py` 公共模块 (JSON 读写、路径解析、常量)
- [x] 编写 `DataLoader` (`game/core/systems/data_loader.rpy`)，游戏端自动加载 JSON
- [x] 所有新增屏幕文本已中文化

---

## 四、Phase B/C — 编辑器 GUI ✅

### 已完成
- [x] **女孩包编辑器** (`tools/bk_editor/girl_pack_editor/`)
  - `_BK.ini` 完整 CRUD、图片批量打标、Trait/Perk 创建器、包验证
  - 直接输出到 `game/custom/girls/`
- [x] **剧本编辑器** (`tools/bk_editor/scenario_editor/`)
  - StoryEvent / Scenario 完整 CRUD
  - `modes` 字段支持 `story`/`sandbox`/`scenario` 筛选
  - District/NPC/Shop 参考数据、对话标签扫描
  - JSON Schema 验证
- [x] **开发控制台** (`tools/bk_editor/dev_console/`)
  - Achievement / Difficulty / NG+ / Meta / Goal / Customer Affix 等 JSON 数据增删改查
- [x] **出身数据** — 5 种预设 Origin 已提取到 `data/sandbox/origins.json`

### 编辑器主入口
```bash
# 统一入口
python tools/bk_editor.py

# 单独启动
python tools/bk_editor/girl_pack_editor/main.py
python tools/bk_editor/scenario_editor/main.py
python tools/bk_editor/dev_console/main.py
```

---

## 五、Phase D — 硬编码导出 JSON ✅

### 已完成
- [x] 编写 `tools/export_hardcoded.py` — 独立 Python 导出脚本
  - 用正则 + 括号匹配 + `eval()` 安全解析 `.rpy` 中的 `Trait(...)` / `Perk(...)` 调用
  - 导出 **131 个 Trait** 到 `game/core/data/traits/traits.json`
  - 导出 **53 个 Perk** 到 `game/core/data/perks/perks.json`
  - 自动过滤默认值，保持 JSON 整洁
- [x] 编写 `game/core/systems/data_exporter.rpy` — 游戏内运行时导出器
  - 在 Debug 菜单中新增 "Export hardcoded data to JSON (Evolution)" 选项
  - 支持 Trait / Perk / StoryEvent 导出
- [x] 验证导出 JSON 可被 `DataLoader` 正确加载

### 使用方法
```bash
# 方法1：独立脚本（推荐）
python tools/export_hardcoded.py

# 方法2：游戏内 Debug 菜单
启动游戏 -> Debug mode -> 选择 "Export hardcoded data to JSON"
```

---

## 六、Phase E — 女孩包制作工具 ✅

### 已完成
- [x] `_BK.ini` 文件读写 (自定义 `ListAwareConfigParser`，支持列表值解析)
- [x] 8 个标签页完整编辑：
  - 基础信息 (identity)：名字、姓氏、作者、版本、描述、克隆选项
  - 技能 (base skills)：8 项属性滑块 (0-5) + 克隆保留选项
  - 正面特质 (base positive traits)：always/often/rarely/never 四桶分配器 + 特质列表选择
  - 负面特质 (base negative traits)：同上
  - 个性 (base personality + custom personality)：24 种内置个性选择器 + 自定义个性表单
  - 喜好 (tastes)：颜色、食物、饮品、爱好
  - 性偏好 (sexual preferences)：性行为、癖好、经验、农场弱点
  - 背景故事 (background story)：生成设置、家乡、奴隶故事
- [x] 特质选择器从 `traits.json` 动态加载所有已注册特质
- [x] 新建/打开/保存/另存为完整文件操作

### 技术要点
- `_BK.ini` 格式兼容原有 Girl Pack 规范
- `ListAwareConfigParser` 用 `ast.literal_eval` 安全解析 Python 列表语法
- 编辑器直接操作文件系统，不经过 JSON 中间层

---

## 七、Phase F — 剧本编辑器完善 ✅

### 已完成
- [x] Scenario 完整 CRUD（新建/保存/删除/验证）
- [x] 基本信息：scenario_id、name、author、version、description、events_script
- [x] 起始条件表单：gold、chapter、girls
- [x] 胜利条件动态编辑：支持添加/删除多条条件（gold_min、reputation_min、girls_min、chapter_min、custom_label）
- [x] 自定义规则 JSON 文本编辑
- [x] 左侧 Treeview 列表 + 右侧滚动表单布局
- [x] JSON Schema 验证集成

---

## 八、Phase G — 代码去硬编码 🔄→✅ (阶段性完成)

### 已完成
- [x] Origin (出身) — 5 种预设已提取到 `data/sandbox/origins.json`
- [x] Trait — 131 个已导出到 `data/traits/traits.json`
- [x] Perk — 53 个已导出到 `data/perks/perks.json`
- [x] StoryEvent — 69 个事件已导出到 `data/events/event_dict.json`
- [x] Goal — 章节目标已提取到 `data/goals/chapter_goals.json`
- [x] Powers / Spells / Items / Jobs / Contracts / Resources / Challenges / Customer Affixes / Cleanliness / Treasure / Meta / NGP / Achievements / Help texts / Interactions / Fixations / Rooms / Difficulty / Scenario 等数据均已完成 JSON 迁移
- [x] **DataLoader 加载顺序优化**：在 `init/start.rpy` 的 `init_game` 中统一调用 `DataLoader.load_all()` 及各类 `load_*()` 方法
- [x] **条件跳过硬编码**：JSON 加载成功后跳过标准硬编码注册，仅保留 fallback
- [x] **DataLoader bug 修复**：注册表方法名统一为 `register_trait()` / `register_perk()` 等，确保 category 正确传递

### 待继续
- [ ] 移除所有已验证无问题的 fallback 硬编码字典（低风险，需长期观察）
- [ ] 机器翻译质量审核与剧情核心文本润色

### 迁移策略
1. **JSON 优先加载**: `DataLoader` 在 `before_main_menu()` 中先加载 JSON，硬编码在 `init_traits()` 中作为 fallback
2. **分步验证**: 每次迁移后运行 `lint` 和游戏启动测试（本次 lint 零新增错误）
3. **版本兼容**: 不破坏旧存档和旧 Mod

---

## 九、已知问题与限制

| 问题 | 状态 | 说明 |
|---|---|---|
| `npc`/`girl.char`/`kidnapped_girl.char` undefined in say statements | 已存在 | Ren'Py lint 误报动态字符变量，非新增问题 |
| 编辑器无图片预览 | 待优化 | tkinter 支持图片预览，但尚未实现 |
| 导出脚本对复杂表达式支持有限 | 已接受 | `eval()` 方案对 99% 的定义有效，极个别需手动修复 |

---

## 十、下一步行动 (Next Steps)

按优先级排序：

1. **[中] 机器翻译质量审核** — 对早期批量迁移的对话和字符串进行人工抽查与润色
2. **[中] 剧情核心文本润色** — 重点审核 chapter1-3 与 story_events 的中文通顺度
3. **[低] 编辑器增强** — 图片预览、搜索过滤、导入导出模板、Girl Pack 图片自动扫描
4. **[低] 清理 fallback 字典** — 在确认 JSON 数据稳定后，逐步移除冗余硬编码回退

---

## 附录 A：文件结构索引

```
tools/
├── bk_editor.py              # 编辑器统一入口
├── bk_editor/
│   ├── core.py               # 公共核心 (JSON, Schema, 路径)
│   ├── shared/               # 三个编辑器共享库
│   ├── girl_pack_editor/     # 女孩包编辑器
│   ├── scenario_editor/      # 剧本编辑器
│   └── dev_console/          # 开发控制台
├── export_hardcoded.py       # 硬编码导出脚本（历史）
└── ... (翻译工具链)

game/core/data/
├── _schemas/
│   ├── trait.json
│   ├── perk.json
│   ├── origin.json
│   ├── story_event.json
│   └── scenario.json
├── traits/
│   └── traits.json           # 131 个 Trait
├── perks/
│   └── perks.json            # 53 个 Perk
├── events/
│   └── event_dict.json       # 69 个 StoryEvent
├── sandbox/
│   └── origins.json          # 5 种 Origin
├── stories/
│   └── story_events.json     # 额外故事事件
├── scenarios/
│   └── scenarios.json        # 剧本定义
└── goals/
    └── chapter_goals.json    # 章节目标
```

---

*最后更新: 2026-06-06*
