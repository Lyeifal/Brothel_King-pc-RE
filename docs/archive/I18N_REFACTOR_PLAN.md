# BK Evolution — 全面 i18n 重构计划（达到 Ren'Py 最佳实践）

> 目标：系统性消除 `game/core` 中所有不符合 Ren'Py i18n 最佳实践的代码，使所有玩家可见文本（剧情、UI、选项、物品/技能描述、随机生成女孩对话）都能被翻译系统正确收集，并位于与其语义来源一致的目录结构中。
>
> 周期：长期（预计 6–10 个迭代阶段，可分批执行）
>
> 约束：零新增 lint 错误；保持游戏可启动；不改业务逻辑。

---

## 一、现状诊断

### 1.1 已符合规范的部分

| 区域 | 状态 | 说明 |
|------|------|------|
| 剧情对话 (`say`/`narrator`) | ✅ 基本符合 | Ren'Py 原生 `translate` 块已覆盖 |
| JSON 数据 `_i18n` 约定 | ✅ 基本符合 | `json_i18n.rpy` 扫描 105 个 JSON 文件并注册到 `__()` |
| `DataLoader` + `get_i18n()` | ✅ 基本符合 | 多数 JSON 加载入口已使用 `get_i18n` / `I18nMixin` |
| 旧 `_cn` 翻译迁移 | ✅ 完成 | Hash + 文本级匹配已导入 |

### 1.2 不符合最佳实践的主要问题

基于对 `game/core` 的扫描，问题按严重程度排序：

#### A. 裸字符串（最严重，玩家直接看到英文）

| 模式 | 估算数量 | 典型位置 | 影响 |
|------|----------|----------|------|
| `call_screen("yes_no", "...")` | 6+ | `systems/help.rpy`, `story_events.rpy`, `core_entities.rpy` | 确认框英文 |
| `renpy.say(..., "...")` 裸字符串 | ~206 | `girlclass.rpy`, `help.rpy`, `interactions.rpy` | 旁白/提示英文 |
| `renpy.notify("...")` | 少量 | 各系统 | 通知英文 |
| Screen `text`/`button`/`label` 裸字符串 | ~109 个可见 | `ui/screens.rpy`, `config/screens.rpy`, 各 screen 文件 | UI 英文 |
| `menu:` 变量/表达式选项 | 少量 | `interactions.rpy`, `help.rpy` | 选项英文 |

#### B. 字符串拼接与格式化（阻碍翻译质量）

| 模式 | 估算数量 | 典型位置 | 问题 |
|------|----------|----------|------|
| `"X" + var + "Y"` | ~1,015 | `girlclass.rpy`, `ui/screens.rpy`, `farm.rpy` | 语法不可译、占位符易丢失 |
| `"... %s ..." % var` 未包裹 `__()` | ~471 | 全代码库 | 英文模板未进入翻译系统 |
| 随机生成描述（女孩、事件） | 大量 | `girl_factory.rpy`, `girlclass.rpy`, `day_events.rpy` | 按词拼接，无法完整翻译 |

#### C. 目录/数据归属不清晰（结构性问题）

| 问题 | 说明 |
|------|------|
| 女孩随机对话硬编码在 `.rpy` | 应迁移到 `data/interactions/` 或 `data/dialogue_pools/` 的 JSON 模板 |
| 物品/技能描述部分仍在代码中 | 应完全由 `data/items/items.json`、`data/powers/powers.json` 等驱动 |
| UI 提示分散在各 screen 文件 | 部分通用提示应归到 `data/settings/ui_texts.json` 或类似位置 |
| 翻译文件分布 | `translate --empty` 后字符串块分散在源文件同目录，这是 Ren'Py 标准做法，但需要按目录维护 |

---

## 二、重构目标与最终状态

### 2.1 代码层目标

1. **所有玩家可见字符串必须被 `__()` 或 `_()` 包裹**
   - `call_screen` 提示：`call_screen("yes_no", __("..."))`
   - `renpy.say`：`renpy.say(who, __("..."))`
   - Screen 文本：`text _("...")`、`button _("...")`
   - `menu:` 选项：字面量直接写，变量选项重构为字面量或包裹 `__(caption)`

2. **禁止用 `+` 拼接玩家可见句子**
   - 改用完整模板 + 占位符：
     ```renpy
     # 重构前
     "Are you sure you want to take a loan for " + str(r.amount) + " gold?"
     # 重构后
     __("Are you sure you want to take a loan for %s gold?") % r.amount
     # 或
     __("Are you sure you want to take a loan for {amount} gold?").format(amount=r.amount)
     ```

3. **JSON 数据驱动所有静态/半静态文本**
   - 物品描述 → `data/items/items.json`
   - 技能/法术描述 → `data/powers/powers.json`、`data/spells/spells.json`
   - 女孩出身/特质/天赋 → `data/origins/`、`data/traits/`、`data/perks/`
   - UI 通用提示 → `data/settings/ui_texts.json`
   - 随机对话池 → `data/dialogue_pools/`（新增）

### 2.2 目录结构目标

```
game/core/
├── content/            # 固定剧情、事件、互动（翻译在 tl/chinese_simplified/core/content/）
│   ├── main_story/
│   ├── side_stories/
│   ├── city_events/
│   ├── day_events/
│   ├── story_events/
│   └── interactions.rpy
├── data/               # 数据驱动文本（_i18n 字段，json_i18n.rpy 自动注册）
│   ├── items/
│   ├── powers/
│   ├── spells/
│   ├── traits/
│   ├── perks/
│   ├── origins/
│   ├── dialogue_pools/   # ← 新增：女孩随机对话模板池
│   └── settings/
│       ├── ui_texts.json       # ← 新增：通用 UI 提示
│       └── girl_descriptions.json
├── systems/            # 系统逻辑，尽量不包含硬编码文本
├── ui/                 # screen 文件，文本用 _() 包裹
└── i18n/
    └── json_i18n.rpy   # 已存在，继续维护

game/tl/chinese_simplified/
├── core/content/       # 剧情、事件、互动翻译
├── core/ui/            # UI 翻译
├── core/systems/       # 系统提示翻译（少量）
└── strings.rpy         # 通用字符串翻译
```

### 2.3 验证目标

- `translate --count chinese_simplified` 显示 **0 missing**
- `lint` 无新增错误
- 新游戏启动后，切换语言无英文残留
- 所有 `%s`/`[var]` 占位符在翻译后保留

---

## 三、分阶段实施计划

### Phase 0 — 基础设施与规范（1 周）

#### 0.1 建立 i18n 规范文档
- 更新/新建 `docs/I18N_BEST_PRACTICES.md`
- 明确规则：
  - 玩家可见字符串必须 `__()`/`_()`
  - 禁止 `+` 拼接句子
  - JSON 数据使用 `_i18n` 后缀
  - 新增代码必须经过 `translate --count` 检查

#### 0.2 创建审计脚本
- 新建 `tools/i18n_lint.py`
- 功能：
  - 扫描 `game/core/**/*.rpy`
  - 检测裸字符串模式（call_screen、renpy.say、screen text、menu 变量）
  - 检测 `+` 拼接玩家可见文本
  - 输出报告（文件、行号、建议）
- 不自动修复，只报告

#### 0.3 创建回归测试
- 新增 `tools/verify_i18n.py`
- 运行 `translate --count` 并断言 0 missing
- 运行 `lint` 并断言无新增错误

#### 0.4 备份当前状态
- 创建 git tag：`before-i18n-refactor`
- 保留 `_translation_backup/` 和代码备份

**验收标准**：
- `docs/I18N_BEST_PRACTICES.md` 存在且完整
- `tools/i18n_lint.py` 能输出当前问题清单
- `tools/verify_i18n.py` 可运行（当前允许失败，作为基线）

---

### Phase 1 — 修复 call_screen / notify / renpy.say 裸字符串（1–2 周）

#### 1.1 call_screen 提示
- 目标文件：`systems/help.rpy`, `content/story_events/story_events.rpy`, `framework/core_entities.rpy`, 其他含 `call_screen` 的文件
- 操作：将第二个参数包裹 `__()`
- 注意：保留 `[girl.fullname]`、`[price]` 等 Ren'Py 插值；将 `+` 拼接的提示重构为完整模板
- 示例：
  ```renpy
  # 重构前
  renpy.call_screen("yes_no", "Are you sure you want to take a loan for " + str(r.amount) + " gold?")
  # 重构后
  renpy.call_screen("yes_no", __("Are you sure you want to take a loan for %s gold?") % r.amount)
  ```

#### 1.2 renpy.notify
- 扫描所有 `renpy.notify("...")`
- 包裹 `__()`，内部拼接改为模板

#### 1.3 renpy.say 旁白
- 目标：`framework/girlclass.rpy`, `systems/help.rpy`, `content/interactions.rpy` 等
- 将裸字符串包裹 `__()`
- 对拼接字符串，先重构为完整句子再包裹

#### 1.4 提取并翻译
- 运行 `translate --empty chinese_simplified`
- 导出新增条目到 `temp/translations/to_translate_phase1.xlsx`
- 翻译后导入
- 运行 `lint` 和 `verify_i18n.py`

**验收标准**：
- `i18n_lint.py` 中 call_screen/notify/renpy.say 裸字符串数量为 0
- 新增翻译导入完成
- lint 通过

---

### Phase 2 — 修复 Screen Language 裸文本（1–2 周）

#### 2.1 UI screen 文本
- 目标：`ui/screens.rpy`（约 67 个可见字符串）、`config/screens.rpy`（约 14 个）、`systems/auction/screen_auction.rpy` 等
- 操作：将 `text "..."`、`button "..."`、`label "..."` 改为 `text _("...")` 等
- 注意：
  - 单字符/图标（如 `{image=...}`、`-`、`+`）不包裹
  - 纯数字标签不包裹
  - 占位符文本如 `[selected_lot.current_bid]` 需要包裹：
    ```renpy
    text _("Current bid: {b}[selected_lot.current_bid]{/b} gold")
    ```

#### 2.2 通用 UI 提示归集（可选）
- 对于在多个 screen 中重复出现的提示（如 "Choose an option", "Are you sure?"），考虑迁移到 `data/settings/ui_texts.json`
- 通过 `__(ui_texts["choose_option"])` 或类似方式引用

#### 2.3 提取并翻译
- 运行 `translate --empty`
- 导出、翻译、导入
- lint 验证

**验收标准**：
- `i18n_lint.py` 中 screen 裸文本数量为 0
- lint 通过

---

### Phase 3 — 修复 menu: 选项（1 周）

#### 3.1 字面量 menu 选项
- Ren'Py 原生 `translate` 已能自动提取字面量 menu 选项
- 确认当前 `.rpy` 中的 `menu:` 块选项是否为字面量
- 对变量/表达式选项重构：
  ```renpy
  # 重构前
  $ caption = "Train her gently"
  menu:
      "[caption]":
  # 重构后
  menu:
      "Train her gently":
  ```

#### 3.2 动态菜单选项
- 对于必须动态生成的选项（如基于 girl 属性变化），使用 `__(caption)`：
  ```renpy
  menu:
      __(caption) if condition:
          ...
  ```

#### 3.3 提取并翻译
- 运行 `translate --empty`
- 导出、翻译、导入

**验收标准**：
- 所有 menu 选项在 `translate --empty` 后都被提取
- 游戏中菜单无英文

---

### Phase 4 — 重构字符串拼接（2–3 周，最耗时）

#### 4.1 优先处理高影响文件
按玩家可见度和拼接数量排序：
1. `framework/girlclass.rpy`（151 处拼接）
2. `ui/screens.rpy`（129 处）
3. `systems/farm.rpy`（78 处）
4. `systems/security.rpy`（66 处）
5. `framework/girl_factory.rpy`（59 处）
6. `content/city_events/city_events.rpy`（42 处）
7. `framework/economy.rpy`（38 处）
8. `framework/game_systems.rpy`（38 处）

#### 4.2 重构模式
将 `"X" + var + "Y"` 改为以下之一：

**模式 A：单个变量**
```renpy
# 重构前
"You have " + str(gold) + " gold."
# 重构后
__("You have %s gold.") % gold
```

**模式 B：多个变量**
```renpy
# 重构前
"Train " + girl.name + " in " + act + " for " + str(cost) + " gold?"
# 重构后
__("Train %s in %s for %s gold?") % (girl.name, act, cost)
# 或
__("Train {name} in {act} for {cost} gold?").format(name=girl.name, act=act, cost=cost)
```

**模式 C：条件分支内的拼接**
- 如果条件影响整个句子结构，保留多个完整模板：
  ```renpy
  if success:
      text = __("%s succeeded in her training.") % girl.name
  else:
      text = __("%s failed in her training.") % girl.name
  ```

#### 4.3 格式化字符串包裹
将所有 `"... %s ..." % var` 包裹 `__()`：
```renpy
# 重构前
"You gained %s gold." % amount
# 重构后
__("You gained %s gold.") % amount
```

#### 4.4 分文件提交
每个文件独立修改、lint、测试，避免一次性大规模变更难以回滚。

**验收标准**：
- `i18n_lint.py` 中 `+` 拼接玩家可见文本数量为 0
- `%` 格式化未包裹 `__()` 的数量为 0
- lint 通过

---

### Phase 5 — 将女孩随机对话/描述迁移到 JSON（2–3 周）

#### 5.1 设计 JSON 结构
新建 `game/core/data/dialogue_pools/` 目录，结构示例：

```json
{
  "greeting": {
    "friendly": [
      "Good morning, Master!",
      "I hope you're having a good day."
    ],
    "shy": [
      "H-hello...",
      "Um, good morning..."
    ]
  },
  "training_response": {
    "positive": [
      "%s seems happy with her training.",
      "%s is making good progress."
    ],
    "negative": [
      "%s is struggling with the training.",
      "%s doesn't seem to enjoy this."
    ]
  }
}
```

#### 5.2 迁移硬编码字符串池
- 从 `framework/girlclass.rpy`、`framework/girl_factory.rpy`、`content/interactions.rpy`、`content/day_events.rpy` 等文件中提取女孩相关描述/对话池
- 按主题分类：
  - `appearance_descriptions.json` — 外貌描述
  - `personality_reactions.json` — 性格反应
  - `training_lines.json` — 训练对话
  - `farm_lines.json` — 农场事件对话
  - `night_lines.json` — 夜间事件对话

#### 5.3 代码适配
- 编写 `DialoguePool` 类或函数，从 JSON 加载模板
- 在运行时根据女孩属性选择模板，并填充占位符
- 示例：
  ```renpy
  init python:
      def get_girl_line(pool_name, personality, **kwargs):
          templates = dialogue_pools.get(pool_name, {}).get(personality, [])
          if templates:
              tmpl = random.choice(templates)
              return __(tmpl) % kwargs
          return ""
  ```

#### 5.4 注册到 json_i18n
- 确保 `dialogue_pools/*.json` 中的字符串使用 `_i18n` 后缀或父 key 以 `_i18n` 结尾
- `json_i18n.rpy` 已支持父 key `_i18n` 的字典值收集

**验收标准**：
- 新增 `data/dialogue_pools/*.json`
- 原 `.rpy` 中女孩相关硬编码描述/对话池显著减少
- 游戏内女孩随机对话显示中文

---

### Phase 6 — JSON 数据层清理（1–2 周）

#### 6.1 补全缺失的 `_i18n` 字段
- 检查 `data/traits/traits.json`：确认 `base_description_i18n` 已使用，补充缺失字段
- 检查 `data/perks/perks.json`：确认 `base_description_i18n` 已使用
- 检查 `data/scenarios/scenarios.json`：补充 `name_i18n`、`description_i18n`
- 检查 `data/challenges/challenges.json`：虽然 `name` 是图片路径，但如果有显示名称，应加 `display_name_i18n`

#### 6.2 物品/技能/法术描述完全 JSON 化
- 确认 `data/items/items.json` 中所有物品都有 `name_i18n` 和 `description_i18n`
- 确认 `data/powers/powers.json` 中所有技能都有 `name_i18n`、`short_description_i18n`、`description_i18n`
- 确认 `data/spells/spells.json` 中所有法术都有 `display_name_i18n`、`description_i18n`
- 清理代码中残留的物品/技能硬编码描述

#### 6.3 UI 通用文本 JSON 化
- 新建 `data/settings/ui_texts.json`
- 迁移重复出现的 UI 提示：
  - "Choose an option"
  - "Are you sure?"
  - "Do you really want to..."
  - "Not enough gold."
  - "Already at max level."

**验收标准**：
- `translate --count` 中 JSON 相关 missing 为 0
- `i18n_lint.py` 中无硬编码物品/技能/UI 描述

---

### Phase 7 — 翻译文件目录结构整理（1 周）

#### 7.1 确认 Ren'Py 标准分布
- `translate --empty` 生成的 `translate chinese_simplified strings:` 块按源文件位置分布
- 保持这种分布，因为符合 Ren'Py 最佳实践
- 不要强制把所有字符串移回 `strings.rpy`

#### 7.2 按目录维护
- `game/tl/chinese_simplified/core/content/` — 剧情、事件、互动
- `game/tl/chinese_simplified/core/ui/` — UI screen
- `game/tl/chinese_simplified/core/systems/` — 系统提示
- `game/tl/chinese_simplified/strings.rpy` — 通用字符串（如来自 `__()` 的代码字符串）

#### 7.3 清理 orphan translations
- 运行 `translate --empty` 会自动标记 orphan
- 审查并删除已失效的翻译块

**验收标准**：
- 翻译文件目录结构与 `game/core` 源文件目录结构一致
- 无孤立翻译块

---

### Phase 8 — 全面验证与质量审核（1–2 周）

#### 8.1 自动化验证
- 运行 `python tools/verify_i18n.py`
- 运行 `python tools/i18n_lint.py` 并确认 0 问题
- 运行 `& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . lint`
- 运行 `& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . translate --count chinese_simplified` → 期望 0 missing

#### 8.2 占位符检查
- 运行 `tools/fix_placeholders.py`（已存在）
- 确保翻译后的 `%s`/`[var]` 占位符与原文一致
- 对新增 JSON  dialogue pools 同样检查

#### 8.3 游戏内测试
- 启动新游戏，覆盖：
  - 开场 intro
  - 第一章剧情
  - 商店购买女孩（yes_no 确认框）
  - 女孩互动菜单与选项
  - 训练、农场、夜间事件
  - 物品栏、技能/法术界面
  - 设置界面、存档读档
- 切换语言确认无英文残留

#### 8.4 社区 Mod 兼容性
- 检查 `custom/mods/` 下的示例 mod
- 确保 mod 中的字符串也遵循 `__()` 规范

**验收标准**：
- 所有自动化检查通过
- 游戏内主要场景无英文
- 占位符无丢失

---

### Phase 9 — 文档与持续维护（持续）

#### 9.1 更新文档
- 更新 `docs/I18N_PLAN.md`：标记 Phase 5 清理完成
- 更新 `docs/TRANSLATION_COMPLETION_PLAN.md`：记录最终状态
- 新建/更新 `docs/I18N_BEST_PRACTICES.md`：供后续开发参考
- 更新 `docs/ROADMAP.md`：将 i18n 重构标记为完成

#### 9.2 建立开发规范
- 新增代码必须满足：
  - 玩家可见字符串 `__()`/`_()`
  - 无 `+` 拼接句子
  - JSON 数据使用 `_i18n`
- Code Review Checklist 中加入 i18n 检查项

#### 9.3 CI/自动化
- 在提交前运行 `tools/i18n_lint.py` 和 `tools/verify_i18n.py`
- 可考虑在 git hook 中加入检查

---

## 四、工具链清单

| 工具 | 用途 | 状态 |
|------|------|------|
| `tools/i18n_lint.py` | 扫描裸字符串、拼接、未包裹 `%` 格式化 | 待创建 |
| `tools/verify_i18n.py` | 运行 translate --count + lint，断言通过 | 待创建 |
| `tools/wrap_yes_no_strings.py` | 批量包裹 call_screen yes_no 字符串 | 已存在 |
| `tools/export_remaining_english.py` | 导出英文空翻译到 Excel | 已存在 |
| `tools/import_translated_remaining_v3.py` | 从 Excel 导回翻译 | 已存在 |
| `tools/auto_fill_nonenglish_empty.py` | 自动填充原文已是中文的条目 | 已存在 |
| `tools/fix_placeholders.py` | 修复 %s 占位符 | 已存在 |

---

## 五、风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 大规模重构引入语法错误 | 高 | 每文件修改后立即 lint；使用 git 分步提交；保留备份 |
| 字符串拼接重构改变语义 | 中 | 只改格式不改词；人工审核高影响文件；游戏内测试 |
| 翻译占位符丢失 | 中 | 使用 fix_placeholders.py；导出/导入时检查 |
| 随机对话 JSON 化后变单调 | 低 | 保持原有模板数量和变体；必要时增加新模板 |
| Mod 兼容性 | 中 | 不修改 Mod API；只修改 Mod 内部字符串写法示例 |

---

## 六、推荐执行顺序

由于这是一个长期计划，建议按以下顺序分迭代执行：

1. **Phase 0**（基础）→ 必须首先完成
2. **Phase 1**（call_screen/notify/say）→ 快速见效，解决最明显英文
3. **Phase 2**（screen text）→ 解决 UI 英文
4. **Phase 3**（menu 选项）→ 解决选项英文
5. **Phase 4**（字符串拼接）→ 最大工作量，分文件推进
6. **Phase 5**（女孩随机对话 JSON 化）→ 与 Phase 4 可并行
7. **Phase 6**（JSON 数据清理）→ 与 Phase 4/5 可并行
8. **Phase 7**（目录整理）→ 在主要代码修改后
9. **Phase 8**（验证）→ 最后
10. **Phase 9**（文档/维护）→ 持续

---

## 七、是否采用此计划

此计划为单一推荐方案：按阶段、从代码层到数据层、从静态文本到动态生成文本，系统性达到 Ren'Py i18n 最佳实践。

若你确认，将从 Phase 0 开始执行。
