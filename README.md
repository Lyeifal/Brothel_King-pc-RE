# Brothel King PC — Evolution 重构版

> 分支：`bk-evolution` · Ren'Py 8.2.0 / Python 3.9 · 完整中文本地化
>
> 🇨🇳 中文 | [🇬🇧 English](README_EN.md)

**Brothel King Evolution** 是对 Ren'Py 成人经营游戏《Brothel King》的数据驱动改造与架构重构版本：游戏数据由 JSON 承载，注册表（Registry）+ DataLoader 分层加载，服务容器解耦全局状态，并提供可视化编辑器与 Mod API v2，大幅降低二次开发和 Mod 制作门槛。

⚠️ **本仓库仅包含代码、文档与翻译**，不含游戏资源文件（图片/音频）、Ren'Py 引擎二进制与女孩包。clone 后需要将本仓库内容放入完整的游戏本体目录中才能运行。

---

## 🎯 最新更新 (2026-10-14)

### ✅ 核心功能验证完成

经过完整的手动回归测试，确认游戏核心功能稳定可用：

- ✅ **游戏流程**: 启动、新游戏、招募、经营、存档/读档 全部通过
- ✅ **Mod系统**: 注册、按钮、界面、钩子、翻译 工作正常
- ✅ **女孩包**: 102个女孩包中75个完全兼容（73%），其余27个仍可加载
- ✅ **i18n系统**: 中英文切换、翻译加载、冲突处理 正常

**详细测试报告**: [`docs/testing/MANUAL_TEST_REPORT_2026-10-14.md`](docs/testing/MANUAL_TEST_REPORT_2026-10-14.md)

### 🐛 已修复的问题

1. **语法错误**: 修复测试框架和示例Mod中的Python语法问题
2. **翻译冲突**: 修正Mod翻译文件的重复定义问题
3. **Mod API**: 修正 `home_rightmenu_add_buttons` 的格式规范

### 📚 文档完善

本次更新补全了项目的测试、文档和示例代码，使项目真正"社区可用"：

- 📋 **完整的测试体系**
  - 手动测试报告
  - 集成测试套件
  - CI/CD脚本（跨平台支持）
  - 女孩包验证工具

- 📚 **详细的开发文档**
  - Mod开发完整指南（含常见错误）
  - 女孩包兼容性指南
  - 存档格式与Migration文档
  - CI/CD设置指南

- 🎯 **完整示例Mod**
  - Advanced Pricing System（700行完整实现）
  - 展示所有Mod API核心功能
  - 详细注释和最佳实践

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
├── renpy/               # Ren'Py 引擎 (不追踪，需自备) 
└── lib/                 # 运行时所需库 (不追踪，需自备)
```

## 🚀 快速开始

### 运行游戏

需要完整的游戏本体（含 `game/resources/`、`lib/`、Ren'Py 引擎）。将本仓库代码覆盖到游戏目录后：

```powershell
# 启动游戏
.\Brothel_King.exe

# 或使用Python启动脚本
python Brothel_King.py
```

### 开发者快速验证

```powershell
# 1. 运行自动化测试套件
.\tools\ci\run_tests.ps1  # Windows
./tools/ci/run_tests.sh    # Linux/macOS

# 2. Lint 检查
python Brothel_King.py . lint

# 3. 验证女孩包兼容性
python tools/test_girl_packs.py

# 4. 游戏内测试（开发者模式）
# 主菜单 → Tests 按钮
```

### 新手指引

1. **玩家**: 直接启动游戏即可，中文翻译已完整
2. **Mod开发者**: 阅读 [`docs/modding/MOD_DEVELOPMENT_GUIDE.md`](docs/modding/MOD_DEVELOPMENT_GUIDE.md)
3. **女孩包作者**: 阅读 [`docs/modding/GIRL_PACK_COMPATIBILITY.md`](docs/modding/GIRL_PACK_COMPATIBILITY.md)
4. **贡献者**: 阅读 [`docs/project/PROJECT_GUIDE.md`](docs/project/PROJECT_GUIDE.md)

---

## 🔧 Mod API v2 | 完整的 Mod 生态

### 19个标准化钩子

支持Mod在以下时机介入游戏逻辑：

| 类别 | 钩子 |
|------|------|
| 女孩相关 | girl_generated, girl_acquired, girl_sold, girl_runaway |
| 时间循环 | day_starting, day_ending, night_starting, night_finished, week_starting |
| 事件 | event_triggering, event_finished, security_event |
| 章节 | chapter_starting, chapter_finished |
| 系统 | game_saved, game_loaded, item_generated |
| 交互 | girl_destination_list, girl_destination_accept |

### 示例Mod

| Mod | 类型 | 说明 |
|-----|------|------|
| **Example - Price Override** | 功能完整 | 自定义定价系统（380行，完整注释） |
| Item Quality | 数据型 | 物品品质系统（含翻译） |
| Auction House | UI型 | 拍卖系统 |
| Game Modes | 复杂型 | 游戏模式框架 |

### 5分钟创建第一个Mod

```python
## game/custom/mods/My Mod/mod.rpy

init -1 python:
    api = ModAPIV2.instance()
    
    api.register_mod("my_mod", {
        "name": "My First Mod",
        "version": "1.0.0",
        "api_version": 2,
        "description": __("我的第一个Mod"),
    })
    
    def on_day_start(context):
        renpy.notify("新的一天！")
    
    api.register_hook(api.HOOK_DAY_STARTING, on_day_start)
```

**详细教程**: [`docs/modding/MOD_DEVELOPMENT_GUIDE.md`](docs/modding/MOD_DEVELOPMENT_GUIDE.md)

---

## 🧪 测试与质量保证

### 自动化测试

```powershell
# 运行完整测试套件（推荐）
.\tools\ci\run_tests.ps1  # Windows
./tools/ci/run_tests.sh    # Linux/macOS

# 单独运行各项测试
python Brothel_King.py . lint                 # 语法检查
python tools/verify_mod_api.py                 # Mod API验证
python tools/test_girl_packs.py                # 女孩包兼容性
```

### 游戏内测试

开发者模式下：
- 主菜单 → **Tests** 按钮
- 运行组件测试和集成测试
- 按 `Shift+O` 打开开发者控制台

### 测试覆盖

- ✅ 语法检查（Ren'Py Lint）
- ✅ 翻译覆盖率检查（95%+）
- ✅ Mod API验证（19个钩子）
- ✅ 女孩包格式验证（102个包）
- ✅ 组件单元测试（5个组件）
- ✅ 集成测试（8个流程）

**详细测试指南**: [`docs/testing/MANUAL_TEST_GUIDE.md`](docs/testing/MANUAL_TEST_GUIDE.md)

---

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

## 📚 文档导航

### 🚀 快速开始
| 文档 | 说明 |
|------|------|
| [HANDOVER_CHECKLIST.md](HANDOVER_CHECKLIST.md) | **从这里开始！** 测试和发布清单 |
| [DELIVERY_DOCUMENT.md](DELIVERY_DOCUMENT.md) | 完整的项目交付文档 |

### 👨‍💻 开发者文档
| 文档 | 说明 |
|------|------|
| [docs/modding/MOD_DEVELOPMENT_GUIDE.md](docs/modding/MOD_DEVELOPMENT_GUIDE.md) | Mod开发完整指南（必读） |
| [docs/modding/GIRL_PACK_COMPATIBILITY.md](docs/modding/GIRL_PACK_COMPATIBILITY.md) | 女孩包格式和兼容性 |
| [docs/architecture/SAVE_FORMAT.md](docs/architecture/SAVE_FORMAT.md) | 存档格式与Migration |
| [docs/modding/MOD_API.md](docs/modding/MOD_API.md) | Mod API 参考 |

### 🧪 测试文档
| 文档 | 说明 |
|------|------|
| [docs/testing/MANUAL_TEST_GUIDE.md](docs/testing/MANUAL_TEST_GUIDE.md) | 手动测试完整指南 |
| [docs/testing/CI_SETUP.md](docs/testing/CI_SETUP.md) | CI/CD设置和使用 |

### 📖 项目文档
| 文档 | 说明 |
|------|------|
| [docs/project/PROJECT_GUIDE.md](docs/project/PROJECT_GUIDE.md) | 项目指南：目录规范、服务访问 |
| [docs/project/ROADMAP.md](docs/project/ROADMAP.md) | 开发路线图 |
| [docs/project/CURRENT_STATUS_SUMMARY.md](docs/project/CURRENT_STATUS_SUMMARY.md) | 项目现状总结 |

### 🏗️ 架构文档
| 文档 | 说明 |
|------|------|
| [docs/architecture/](docs/architecture/) | 各子系统架构文档 |
| [docs/migration/DATA_MIGRATION.md](docs/migration/DATA_MIGRATION.md) | 数据迁移清单 |
| [docs/i18n/I18N_ROADMAP.md](docs/i18n/I18N_ROADMAP.md) | 国际化路线图 |

---

## ⚠️ 免责声明

- 本项目为**成人内容（18+）**，包含裸露与性相关描写，仅供成年玩家学习与研究
- 本仓库不包含任何游戏资源与商业素材；游戏原始版权归原开发者所有
- 请勿将本项目用于任何商业用途

## 📄 协议

代码部分遵循仓库内许可文件（如有）。游戏原始资源版权归原开发者所有，不在本仓库分发。
