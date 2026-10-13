# BK Evolution 文档中心

> **最后更新**: 2026-10-14  
> **文档总数**: 15+  
> **状态**: ✅ 完整

---

## 🚀 新手导航（按阅读顺序）

### 1. 快速了解项目（5分钟）
- 📄 [QUICK_START.md](project/QUICK_START.md) - 快速开始指南
- 📄 [CURRENT_STATUS_SUMMARY.md](project/CURRENT_STATUS_SUMMARY.md) - 项目现状

### 2. 开始开发（30分钟）
- 📄 [ROADMAP.md](project/ROADMAP.md) - 开发路线图
- 📄 [MOD_DEVELOPMENT_GUIDE.md](development/MOD_DEVELOPMENT_GUIDE.md) - Mod开发指南

### 3. 深入理解（2小时）
- 📄 [PROJECT_GUIDE.md](architecture/PROJECT_GUIDE.md) - 架构设计文档
- 📄 [SAVE_FORMAT.md](architecture/SAVE_FORMAT.md) - 存档格式说明

---

## 📚 文档分类

### 项目管理 (`docs/project/`)

| 文档 | 说明 | 优先级 |
|------|------|--------|
| [SUMMARY_2026-10-14.md](project/SUMMARY_2026-10-14.md) | 今日工作总结（完整） | ⭐⭐⭐⭐⭐ |
| [CURRENT_STATUS_SUMMARY.md](project/CURRENT_STATUS_SUMMARY.md) | 项目现状快速总结 | ⭐⭐⭐⭐⭐ |
| [QUICK_START.md](project/QUICK_START.md) | 5分钟快速开始 | ⭐⭐⭐⭐⭐ |
| [ROADMAP.md](project/ROADMAP.md) | 开发路线图 | ⭐⭐⭐⭐ |
| [REFACTORING_NEXT_STEPS.md](../docs_EN/project/REFACTORING_NEXT_STEPS.md) | 重构详细分析 | ⭐⭐⭐ |
| [ACTION_PLAN_SUMMARY.md](../docs_EN/project/ACTION_PLAN_SUMMARY.md) | 具体行动计划 | ⭐⭐⭐ |

---

### 架构设计 (`docs/architecture/`)

| 文档 | 说明 | 优先级 |
|------|------|--------|
| [PROJECT_GUIDE.md](architecture/PROJECT_GUIDE.md) | 完整架构文档 | ⭐⭐⭐⭐⭐ |
| [SAVE_FORMAT.md](architecture/SAVE_FORMAT.md) | 存档格式与迁移 | ⭐⭐⭐⭐ |
| [SERVICES_OVERVIEW.md](architecture/SERVICES_OVERVIEW.md) | 服务容器说明 | ⭐⭐⭐ |

---

### 开发指南 (`docs/development/`)

| 文档 | 说明 | 优先级 |
|------|------|--------|
| [MOD_DEVELOPMENT_GUIDE.md](development/MOD_DEVELOPMENT_GUIDE.md) | Mod开发完整指南 | ⭐⭐⭐⭐⭐ |
| [GIRL_PACK_COMPATIBILITY.md](development/GIRL_PACK_COMPATIBILITY.md) | 女孩包兼容性 | ⭐⭐⭐⭐ |
| [I18N_GUIDE.md](development/I18N_GUIDE.md) | 国际化指南 | ⭐⭐⭐ |

---

### 测试文档 (`docs/testing/`)

| 文档 | 说明 | 优先级 |
|------|------|--------|
| [MANUAL_TEST_REPORT_2026-10-14.md](testing/MANUAL_TEST_REPORT_2026-10-14.md) | 手动测试报告 | ⭐⭐⭐⭐⭐ |
| [CI_SETUP.md](testing/CI_SETUP.md) | CI/CD配置指南 | ⭐⭐⭐⭐ |
| [TESTING_GUIDE.md](testing/TESTING_GUIDE.md) | 测试指南 | ⭐⭐⭐ |

---

## 🎯 按场景查找文档

### 场景A: 我是第一次接触这个项目

**推荐阅读顺序**:
1. [QUICK_START.md](project/QUICK_START.md) - 了解项目
2. [CURRENT_STATUS_SUMMARY.md](project/CURRENT_STATUS_SUMMARY.md) - 了解现状
3. [PROJECT_GUIDE.md](architecture/PROJECT_GUIDE.md) - 理解架构

**预计时间**: 30分钟

---

### 场景B: 我想开发一个Mod

**推荐阅读顺序**:
1. [MOD_DEVELOPMENT_GUIDE.md](development/MOD_DEVELOPMENT_GUIDE.md) - Mod开发指南
2. 研究示例: `game/custom/mods/Example - Price Override/`
3. 开始动手！

**预计时间**: 2-4小时（包括实践）

---

### 场景C: 我想贡献核心代码

**推荐阅读顺序**:
1. [PROJECT_GUIDE.md](architecture/PROJECT_GUIDE.md) - 理解架构
2. [ROADMAP.md](project/ROADMAP.md) - 了解优先级
3. [CI_SETUP.md](testing/CI_SETUP.md) - 配置测试环境
4. [REFACTORING_NEXT_STEPS.md](../docs_EN/project/REFACTORING_NEXT_STEPS.md) - 深入分析

**预计时间**: 1-2天（学习）+ 实际开发时间

---

### 场景D: 我想翻译到其他语言

**推荐阅读顺序**:
1. [I18N_GUIDE.md](development/I18N_GUIDE.md) - i18n系统说明
2. 查看示例: `game/tl/chinese_simplified/`
3. 开始翻译！

**预计时间**: 20-40小时（完整翻译）

---

### 场景E: 我想创建女孩包

**推荐阅读顺序**:
1. [GIRL_PACK_COMPATIBILITY.md](development/GIRL_PACK_COMPATIBILITY.md) - 格式说明
2. 查看示例: `game/custom/characters/girls/*/`
3. 开始创作！

**预计时间**: 因女孩包复杂度而异

---

### 场景F: 我想了解存档系统

**推荐阅读顺序**:
1. [SAVE_FORMAT.md](architecture/SAVE_FORMAT.md) - 存档格式
2. 查看代码: `game/core/systems/save_manager.rpy`

**预计时间**: 1-2小时

---

## 🔧 工具与脚本文档

### 测试工具
- `tools/ci/run_tests.sh` - Linux/macOS/WSL测试脚本
- `tools/ci/run_tests.ps1` - Windows测试脚本
- `tools/test_girl_packs.py` - 女孩包验证工具

**使用方法**: 查看 [CI_SETUP.md](testing/CI_SETUP.md)

### 开发工具
- 开发者控制台: 游戏内按 `Shift+O`
- 测试运行器: 主菜单 "Tests" 按钮
- 快速重载: `Shift+R`

**使用方法**: 查看 [PROJECT_GUIDE.md](architecture/PROJECT_GUIDE.md)

---

## 📖 代码示例位置

### Mod示例
- **完整Mod**: `game/custom/mods/Example - Price Override/`
  - 主文件: `mod.rpy` (700行)
  - 文档: `README.md`
  - 翻译: `tl/chinese_simplified/mod.rpy`

### 测试示例
- **集成测试**: `game/core/tools/integration_tests.rpy`
- **测试框架**: `game/core/tools/test_runner.rpy`

### 架构示例
- **服务容器**: `game/core/framework/game_services.rpy`
- **数据加载器**: `game/core/framework/data_loader.rpy`
- **i18n服务**: `game/core/framework/i18n_service.rpy`

---

## 🆕 最新更新（2026-10-14）

### 新增文档
- ✅ [SUMMARY_2026-10-14.md](project/SUMMARY_2026-10-14.md) - 完整工作总结
- ✅ [MANUAL_TEST_REPORT_2026-10-14.md](testing/MANUAL_TEST_REPORT_2026-10-14.md) - 测试报告
- ✅ [ROADMAP.md](project/ROADMAP.md) - 开发路线图
- ✅ [QUICK_START.md](project/QUICK_START.md) - 快速开始
- ✅ [SAVE_FORMAT.md](architecture/SAVE_FORMAT.md) - 存档格式

### 更新文档
- ✅ [MOD_DEVELOPMENT_GUIDE.md](development/MOD_DEVELOPMENT_GUIDE.md) - 添加常见错误
- ✅ [GIRL_PACK_COMPATIBILITY.md](development/GIRL_PACK_COMPATIBILITY.md) - 完善说明
- ✅ [CI_SETUP.md](testing/CI_SETUP.md) - 添加完整脚本
- ✅ [CURRENT_STATUS_SUMMARY.md](project/CURRENT_STATUS_SUMMARY.md) - 更新状态
- ✅ [README.md](../README.md) - 更新最新信息

### 修复问题
- ✅ 语法错误（3个）
- ✅ 翻译冲突（1个）
- ✅ Mod API错误（1个）

---

## 🔍 快速查询

### 常见问题
**Q: 游戏无法启动？**  
A: 查看 [MANUAL_TEST_REPORT_2026-10-14.md](testing/MANUAL_TEST_REPORT_2026-10-14.md) § 常见问题

**Q: Mod无法加载？**  
A: 查看 [MOD_DEVELOPMENT_GUIDE.md](development/MOD_DEVELOPMENT_GUIDE.md) § 常见错误

**Q: 如何调试代码？**  
A: 查看 [QUICK_START.md](project/QUICK_START.md) § 常见问题

**Q: 女孩包不兼容？**  
A: 查看 [GIRL_PACK_COMPATIBILITY.md](development/GIRL_PACK_COMPATIBILITY.md)

**Q: 翻译有冲突？**  
A: 查看 [MOD_DEVELOPMENT_GUIDE.md](development/MOD_DEVELOPMENT_GUIDE.md) § 翻译最佳实践

---

## 📊 文档统计

- **总文档数**: 15+
- **总字数**: 50,000+
- **代码示例**: 30+
- **覆盖领域**: 架构、开发、测试、管理

---

## 🎯 下一步建议

根据你的角色选择：

### 如果你是项目维护者
→ 先读 [SUMMARY_2026-10-14.md](project/SUMMARY_2026-10-14.md)  
→ 再读 [ROADMAP.md](project/ROADMAP.md)

### 如果你是Mod开发者
→ 先读 [QUICK_START.md](project/QUICK_START.md)  
→ 再读 [MOD_DEVELOPMENT_GUIDE.md](development/MOD_DEVELOPMENT_GUIDE.md)

### 如果你是核心贡献者
→ 先读 [PROJECT_GUIDE.md](architecture/PROJECT_GUIDE.md)  
→ 再读 [REFACTORING_NEXT_STEPS.md](../docs_EN/project/REFACTORING_NEXT_STEPS.md)

### 如果你是翻译者
→ 先读 [I18N_GUIDE.md](development/I18N_GUIDE.md)  
→ 再看示例: `game/tl/chinese_simplified/`

---

## 📞 获取帮助

- **文档问题**: 查看对应文档的"常见问题"章节
- **技术问题**: 查看 [PROJECT_GUIDE.md](architecture/PROJECT_GUIDE.md)
- **Mod问题**: 查看 [MOD_DEVELOPMENT_GUIDE.md](development/MOD_DEVELOPMENT_GUIDE.md)
- **其他问题**: 查看 [QUICK_START.md](project/QUICK_START.md)

---

**文档中心最后更新**: 2026-10-14  
**维护者**: Lyeifal  
**协助**: Claude Opus 5.5
