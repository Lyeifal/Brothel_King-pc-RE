# BK Evolution — 国际化（i18n）路线图

> 最后更新：2026-09-11（第二轮：全部补完）
>
> 本文档是 i18n 工作的**唯一活跃参考**，整合原 `I18N_PLAN.md` 与 `I18N_REFACTOR_PLAN.md` 的内容，并反映当前代码实际状态。
>
> 历史版本：[`docs/archive/I18N_PLAN.md`](../archive/I18N_PLAN.md)、[`docs/archive/I18N_REFACTOR_PLAN.md`](../archive/I18N_REFACTOR_PLAN.md)

---

## 1. 当前状态

| 指标 | 状态 |
|------|------|
| JSON `_i18n` 迁移 | ✅ 全部完成（`tools/audit_json_i18n.py` 实测：104 个 JSON 文件，3,533 条字符串全部已翻译） |
| `json_i18n.rpy` 白名单模式 | ✅ 已移除，仅保留 `_i18n` 后缀识别 |
| 代码裸字符串包裹 | ✅ 主要 UI/菜单/旁白/互动选项已包裹；天赋树/特质/物品显示链路已于 2026-09-11 修复（见 `TRANSLATION_STATUS.md` 第 7 节） |
| 中文翻译覆盖率 | ✅ **零缺失**（`translate --count chinese_simplified` 实测）：0 dialogue + 0 string 缺失 |
| 当前缺失基线（2026-09-11） | ✅ 0 dialogue + 0 string —— 回归基线归零，新增代码必须保持为零 |
| i18n 审计工具 | ✅ `tools/i18n_lint.py`、`tools/verify_i18n.py` 已存在；i18n_lint 基线 18 处开发者面向文本误报（原 17，2026-09-11 新增 1 条 `character.rpy` 异常消息） |

---

## 2. 核心约定

### 2.1 JSON 字段：`name` vs `name_i18n`

```json
{
  "id": "pirate_captain",
  "name": "pirate_captain",
  "name_i18n": "Pirate Captain",
  "description_i18n": "A feared captain of the high seas."
}
```

- **代码 key**：`name`、`id`、`type`、`tag` 等字段保持英文/标识符，用于逻辑查找。
- **可翻译文本**：字段名以 `_i18n` 结尾，通过 `game/core/i18n/json_i18n.rpy` 自动注册到 Ren'Py 翻译系统。
- **图片/音频路径**：保持原字段名（如 `pic`、`sound`），**不加** `_i18n`。
- **数值/布尔/代码字段**：保持原字段名，不加 `_i18n`。

### 2.2 代码中使用 `__()` / `_()`

```renpy
# Python 代码中
text = __("You have %s gold.") % gold

# Screen language 中
text _("Welcome to Brothel King")
```

- 玩家可见字符串必须包裹 `__()`（Python）或 `_()`（Screen）。
- 内部标识符、调试日志、文件路径不要包裹。

### 2.3 加载时翻译

```python
from core.i18n import get_i18n

class MyEntity:
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=get_i18n(data, "name"),        # 优先取 name_i18n，否则 name
            description=get_i18n(data, "description", ""),
        )
```

`get_i18n(data, key)` 会自动处理 `key_i18n` → `key` 的回退，并返回当前语言翻译。

---

## 3. 已完成的工作

### 3.1 JSON `_i18n` 迁移（Phase 1-4）

所有含可翻译文本的 JSON 已适配 `_i18n` 后缀，主要类别：

- **核心系统**: difficulty, origins, shops, powers, spells, personalities, achievements, contracts, customer_affixes, meta, ngp, chapter_titles, mc_classes
- **内容数据**: traits, perks, fixations, items, contracts, rooms, story_events
- **交互与事件**: interact_dict, free_interact_dict, default_world
- **农场与表演**: farm_descriptions, farm_perform_dict, farm_holding_params
- **文本字典**: cleanliness_penalties, dialogue_texts, event_texts, gossip, help_texts, loading_tips, mc_descriptions, merchants, recent_events, sex_act_descriptions, sex_descriptions, small_texts 等

> 完整文件列表见 [`docs/archive/I18N_PLAN.md`](../archive/I18N_PLAN.md)。

### 3.2 代码包裹（原 I18N_REFACTOR_PLAN Phase 1-3）

- `renpy.say` / `renpy.notify` 裸字符串已包裹 `__()`。
- `call_screen("yes_no", ...)` 等屏幕调用提示已包裹 `__()`。
- 屏幕语言中的菜单选项、分类标题、Tab 标签已包裹 `_()` / `__()`。
- 拼接字符串已重构为完整句子后包裹 `__()`。

### 3.3 工具链（原 I18N_REFACTOR_PLAN Phase 4-6）

| 工具 | 路径 | 用途 |
|------|------|------|
| `i18n_lint.py` | `tools/i18n_lint.py` | 扫描裸字符串、拼接文本、未包裹格式化等 i18n 问题 |
| `verify_i18n.py` | `tools/verify_i18n.py` | 运行 `translate --count` + `lint` + `i18n_lint.py`，断言无缺失翻译（当前基线：1,433 dialogue + 124 string 缺失，为内容存量非代码缺陷） |
| `audit_placeholders.py` | `tools/audit_placeholders.py` | 检查中文翻译与原文占位符是否一致 |
| `export_empty_to_xlsx.py` | `tools/export_empty_to_xlsx.py` | 导出空翻译到 `temp/translations/to_translate_empty.xlsx`（2026-09-11 起项目路径自动推导） |
| `import_translated_empty.py` | `tools/import_translated_empty.py` | 从 Excel 导回翻译（2026-09-11 起项目路径自动推导） |
| `import_json_i18n.py` | `tools/import_json_i18n.py` | **必需**：JSON 新增 `_i18n` 字段后，将其同步进 `strings.rpy` 空槽位（见第 4 节步骤 0） |
| `audit_json_i18n.py` | `tools/audit_json_i18n.py` | 审计所有 JSON `_i18n` 字符串在 `strings.rpy` 中均有翻译 |

---

## 4. 标准翻译工作流

```powershell
# 0. 若新增/修改了 JSON `_i18n` 字段：必须先同步进 strings.rpy！
#    （translate --empty 无法提取 JSON 字符串——它们在 init 期动态注册，提取器不可见）
python tools/import_json_i18n.py

# 1. 提取空翻译
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . translate --empty chinese_simplified

# 2. 导出到 Excel
python tools/export_empty_to_xlsx.py

# 3. 人工/机器翻译 temp/translations/to_translate_empty.xlsx

# 4. 导回
python tools/import_translated_empty.py

# 5. JSON _i18n 覆盖审计（必须输出 "All JSON _i18n strings are translated!"）
python tools/audit_json_i18n.py

# 6. 占位符与标签审计
python tools/audit_placeholders.py

# 7. 运行 i18n 审计与验证
python tools/i18n_lint.py
python tools/verify_i18n.py

# 8. 最终 lint
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . lint
```

详细统计与历史记录见 [`TRANSLATION_STATUS.md`](TRANSLATION_STATUS.md)。

---

## 5. 编码最佳实践

详见 [`BEST_PRACTICES.md`](BEST_PRACTICES.md)。要点：

1. 玩家可见字符串必须 `__()` / `_()`。
2. 中文翻译保留所有 `%s`/`%d`/`[var]` 占位符。
3. 避免字符串拼接，先组合成完整句子再翻译。
4. JSON 可翻译字段使用 `_i18n` 后缀。
5. 不要翻译内部 key、图片路径、音效路径。
6. 新增字符串后运行 `translate --empty` 并导出/翻译/导入。

---

## 6. 遗留与待优化项

| 项 | 状态 | 说明 |
|----|------|------|
| 机器翻译质量审核 | 🚧 持续 | 早期迁移的 ~3,500 对话块和 ~9,000 字符串为机翻，需运行时抽查。2026-09-11 一轮（2,130 条存量 + 208 条天赋/特质/物品字符串）由 AI 译者翻译，非旧机翻管线，质量更高但仍建议抽查 |
| 剧情核心文本重点审核 | 🚧 持续 | chapter1-3、story_events 建议人工润色 |
| Mod 内容翻译 | ⏳ 待规划 | `game/custom/` 内容默认保持原文；未来可通过统一字符串表支持 |
| `tools/translate_sync.py` | ✅ 不实现（2026-06-25 决策） | "同步 strings.rpy 与 tl 文件 old/new"的需求已由现有工具链覆盖：缺失检测 = `verify_i18n.py`（`translate --count`）；占位符完整性 = `audit_placeholders.py`；空翻译导出/导回往返 = `export_empty_to_xlsx.py` / `import_translated_empty.py`；源字符串变更后由 Ren'Py `translate` 命令重写 tl 文件时清理陈旧条目。不重复造轮子。 |
| i18n_lint 开发者面向误报 | 📝 记录 | `i18n_lint.py` 当前报 18 处 issue（基线 17 + 2026-09-11 新增 1 条），全部位于开发者面向文本（dev console 输出、test runner 断言消息、异常消息），非玩家可见字符串，暂不包裹 `__()`；如后续需要可为工具增加路径白名单。 |
| 新撰写描述 | 📝 记录（2026-09-11） | ~209 条天赋/特质/物品描述原本无源文本，为英文新撰后翻译；建议游戏内核对语气。29 件武器/法杖类物品原本即无描述，属正常。 |

---

## 7. 相关文件

| 文件 | 说明 |
|------|------|
| [`BEST_PRACTICES.md`](BEST_PRACTICES.md) | 编码与翻译最佳实践 |
| [`TRANSLATION_STATUS.md`](TRANSLATION_STATUS.md) | 中文翻译补完记录（已收官，历史记录+当前基线） |
| [`game/core/i18n/json_i18n.rpy`](../../game/core/i18n/json_i18n.rpy) | JSON i18n 注册实现 |
| [`tools/i18n_lint.py`](../../tools/i18n_lint.py) | i18n 静态审计 |
| [`tools/verify_i18n.py`](../../tools/verify_i18n.py) | i18n 回归验证 |
