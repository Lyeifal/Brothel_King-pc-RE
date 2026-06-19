# BK Editor 拆分任务进度

> 创建于 2026-06-06
> 最后更新: 2026-06-06
> **状态: 全部完成 ✅**

---

## Phase 0: 基础设施

- [x] 创建 `tools/bk_editor/` 目录结构
- [x] 创建 `TASK_PROGRESS.md`
- [x] 创建 `README.md`
- [x] 创建 `AGENTS.md`
- [x] 迁移共享模块 (`shared/paths.py`, `shared/json_io.py`, `shared/widgets.py`, `shared/validators.py`, `shared/renpy_ref.py`)
- [x] 验证现有编辑器仍可启动

## Phase 1: 女孩包编辑器 (girl_pack_editor)

- [x] 创建 `main.py` + `editor.py` 主框架
- [x] 图片打标面板 (`tabs/image_tagger.py`) — 按钮打标、多选、标签分类、场景验证、拼写检查
- [x] `_BK.ini` 编辑器 (`tabs/ini_editor.py`) — Section 分块表单、trait/personality 下拉
- [x] 自定义 Trait/Perk 创建器 (`tabs/trait_creator.py`) — Effect 链编辑、JSON 保存
- [x] 包验证器 (`tabs/pack_validator.py`) — portrait/profile 检查、引用校验、一键修复
- [x] 启动测试通过
- [x] 支持 WebP/AVIF 预览（Pillow）
- [x] 支持 WebM 视频预览（OpenCV）

## Phase 2: 剧本编辑器 (scenario_editor)

- [x] 创建 `main.py` + `editor.py` 主框架
- [x] 事件编辑器 (`tabs/event_editor.py`) — StoryEvent / sandbox events JSON CRUD
- [x] 剧本管理 (`tabs/scenario_editor_tab.py`) — Scenario JSON CRUD
- [x] 地图/地点编辑器 (`tabs/district_editor.py`) — District/Location 参考 + 代码片段生成
- [x] NPC 编辑器 (`tabs/npc_editor.py`) — 商店 NPC / 特殊女孩参考 + 代码片段生成
- [x] 商店编辑器 (`tabs/shop_editor.py`) — 商店设置 / 物品类型参考 + 代码片段生成
- [x] 对话图片标签编辑器 (`tabs/image_tag_editor.py`) — {image=...} / emo_xxx 扫描与参考
- [x] 启动测试通过

## Phase 3: 开发控制台 (dev_console)

- [x] 创建 `main.py` + `editor.py` 主框架
- [x] 成就编辑器 (`tabs/achievement_editor.py`)
- [x] 难度编辑器 (`tabs/difficulty_editor.py`)
- [x] NG+ 编辑器 (`tabs/ngp_editor.py`)
- [x] Meta 编辑器 (`tabs/meta_editor.py`)
- [x] I18n 编辑器 (`tabs/i18n_editor.py`)
- [x] 数据同步面板 (`tabs/data_sync.py`)
- [x] 启动测试通过

## Phase 4: 收尾

- [x] 女孩包编辑器 / 剧本编辑器 / 开发控制台独立启动测试
- [x] 更新 `README.md` — 详细使用说明、依赖、架构、故障排除
- [x] 创建 `AGENTS.md` — Agent 开发指南
- [x] 更新 `docs/PROJECT_GUIDE.md` — 加入编辑器套件说明
- [x] 运行 `py_compile` 全部通过
- [x] 更新 `TASK_PROGRESS.md` 标记全部完成

---

## 最终交付物

```
tools/bk_editor/
├── README.md                  # 详细使用说明
├── AGENTS.md                  # Agent 开发指南
├── TASK_PROGRESS.md           # 本文件
├── shared/                    # 共享基础库
├── girl_pack_editor/          # 女孩包编辑器 ✅
├── scenario_editor/           # 剧本编辑器 ✅
└── dev_console/               # 开发控制台 ✅
```
