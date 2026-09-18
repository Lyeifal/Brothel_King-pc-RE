# Brothel King PC — Evolution 重构版

> 分支：`bk-evolution` · Ren'Py 8.2.0 / Python 3.9 · 中文本地化已完成
>
> 🇨🇳 中文 | [🇬🇧 English](README_EN.md)

**Brothel King Evolution** 是对 Ren'Py 成人经营游戏《Brothel King》的数据驱动改造与架构重构版本：游戏数据由 JSON 承载，注册表（Registry）+ DataLoader 分层加载，服务容器解耦全局状态，并提供可视化编辑器与 Mod API，大幅降低二次开发和 Mod 制作门槛。

⚠️ **本仓库仅包含代码、文档与翻译**，不含游戏资源文件（图片/音频）、Ren'Py 引擎二进制与女孩包。clone 后需要将本仓库内容放入完整的游戏本体目录中才能运行。

⚠️ **下方的文档是由AI审计生成的尚未完全人工审查，内容并不可靠，很多内容并未真正实现，但大概目标一致。**
---

## ✨ 主要特性

| 特性 | 说明 |
|------|------|
| 📦 数据驱动架构 | 131 个 Trait、53 个 Perk、物品、成就、合同、起源、法术等 50+ 领域已从硬编码迁移至 `game/core/data/` JSON（含 Schema 校验） |
| 🧩 服务容器 | `GameServices` 统一管理 11 个核心服务；事件桥接 EventBridge 兼容新旧事件系统 |
| 👧 女孩组件化 | `girlclass.rpy` 从 5,900 行拆解至 1,148 行，16 个组件文件，2,000+ 调用点保持不变 |
| 🖥️ UI 架构 | 108 个屏幕从单一 8,886 行文件抽取为 16 个文件，逐字符验证一致 |
| 🌐 完整中文本地化 | 简体中文翻译覆盖率 100%（0 缺失对话 / 0 缺失字符串）；I18nService 支持 `t()`/`tn()`/`tc()`/`plural()` 等多语言 API，新语言仅需翻译文件 + 字体配置 |
| 🔧 Mod API v2 | 版本化清单 + 19 个钩子点（注册/执行）+ UI 按钮注入；自带两个官方示例 Mod：[拍卖行](game/custom/mods/Auction%20House/)（UI 型）、[物品品质](game/custom/mods/Item%20Quality/)（数据型，自带翻译） |
| 🛠️ 开发工具 | Dev Console（Shift+O，开发者模式）、Test Runner（主菜单 Tests 按钮）、`tools/` 下 30+ 审计/翻译/验证脚本 |
| 📝 可视化编辑器 | tkinter 编辑器套件（零第三方依赖）：女孩包编辑器（8 标签页）、场景事件编辑器、Trait/Perk CRUD |

## 📁 目录结构

```
├── game/
│   ├── core/            # 核心框架：服务容器、数据加载、事件、UI、i18n、Mod 系统、开发工具
│   │   ├── data/        # JSON 游戏数据（含 _schemas/ 校验）
│   │   ├── framework/   # Girl 组件化框架（girl/ 下 16 个组件）
│   │   ├── systems/     # 系统层：拍卖、物品、特质、安全、注册表…
│   │   ├── ui/          # 屏幕（16 个抽取文件）+ ViewModel
│   │   └── tl/          # 游戏内翻译（chinese_simplified 中文）
│   ├── custom/          # 用户内容：girls/ 女孩包、mods/ 社区 Mod（均不追踪）
│   ├── resources/       # 游戏资源（不追踪，需自备）
│   └── tl/              # Ren'Py 翻译目录（strings.rpy 等）
├── docs/                # 中文文档
├── docs_EN/             # 英文文档（与 docs/ 镜像）
├── tools/               # 翻译/审计/验证脚本 + bk_editor 编辑器套件
└── renpy/ lib/          # Ren'Py 引擎与运行时（不追踪）
```

## 🚀 运行

需要完整的游戏本体（含 `game/resources/`、`lib/`、Ren'Py 引擎）。将本仓库代码覆盖到游戏目录后：

```powershell
# Lint 检查
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . lint

# 启动游戏
.\Brothel_King.exe
```

## 🌐 翻译工作流

```powershell
# JSON 新增 _i18n 字段后必须先同步进 strings.rpy
python tools/import_json_i18n.py

# 提取空缺翻译 → 导出 Excel → 翻译 → 导入
& "lib\py3-windows-x86_64\python.exe" "Brothel_King.py" . translate --empty chinese_simplified
python tools/export_empty_to_xlsx.py
python tools/import_translated_empty.py

# 审计与回归验证
python tools/audit_json_i18n.py      # JSON _i18n 覆盖
python tools/audit_placeholders.py   # 占位符一致性
python tools/verify_i18n.py          # 缺失回归（基线：0 缺失）
```

## 📚 文档

| 文档 | 说明 |
|------|------|
| [docs/project/ROADMAP.md](docs/project/ROADMAP.md) | 主路线图（已完成 / 进行中 / 待办） |
| [docs/project/PROJECT_GUIDE.md](docs/project/PROJECT_GUIDE.md) | 项目指南：目录规范、init 链、服务访问、数据约定 |
| [docs/architecture/](docs/architecture/) | 各子系统架构（DataLoader、事件、女孩包、注册表…） |
| [docs/i18n/I18N_ROADMAP.md](docs/i18n/I18N_ROADMAP.md) | i18n 唯一活跃参考 |
| [docs/modding/MOD_API.md](docs/modding/MOD_API.md) | Mod API 完整文档 |
| [docs/migration/DATA_MIGRATION.md](docs/migration/DATA_MIGRATION.md) | 硬编码 → JSON 迁移清单 |

## ⚠️ 免责声明

- 本项目为**成人内容（18+）**，包含裸露与性相关描写，仅供成年玩家学习与研究
- 本仓库不包含任何游戏资源与商业素材；游戏原始版权归原开发者所有
- 请勿将本项目用于任何商业用途

## 📄 协议

代码部分遵循仓库内许可文件（如有）。游戏原始资源版权归原开发者所有，不在本仓库分发。
