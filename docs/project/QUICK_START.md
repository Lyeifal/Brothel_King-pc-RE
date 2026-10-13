# BK Evolution 快速开始指南

> 5分钟了解项目，15分钟开始开发

---

## 🎯 项目简介

**BK Evolution** 是《Brothel King》的架构重构版本，目标是：
1. ✅ 支持完整的i18n（中英文已完成）
2. ✅ 规范化Mod开发API
3. ✅ 兼容旧女孩包

**当前状态**: 核心功能已验证，可正常游玩

---

## 📂 项目结构速览

```
BK Evolution/
├── game/
│   ├── core/                      # 核心系统（你的重构重点）
│   │   ├── framework/            # 框架层（服务容器、组件）
│   │   ├── systems/              # 游戏系统（经营、战斗）
│   │   ├── data/                 # JSON数据文件
│   │   └── ui/                   # UI界面
│   ├── custom/mods/              # Mod目录
│   └── tl/chinese_simplified/    # 中文翻译
├── docs/                         # 文档中心
│   ├── architecture/             # 架构文档
│   ├── development/              # 开发指南
│   ├── project/                  # 项目管理
│   └── testing/                  # 测试文档
└── tools/                        # 开发工具
```

---

## 🚀 5分钟快速测试

### 1. 启动游戏
```bash
# Windows
./Brothel King.exe

# 或者用Ren'Py SDK
renpy.exe .
```

### 2. 基础功能测试
- ✅ 新游戏 → 选择难度 → 进入游戏
- ✅ 招募一个女孩
- ✅ 经营一天
- ✅ 存档 → 读档

### 3. Mod系统测试
- ✅ 主页右侧 → "定价" 按钮
- ✅ 打开配置界面
- ✅ 调整参数并保存

**如果以上都正常，恭喜！游戏核心功能完好。**

---

## 📚 关键文档导航

### 新手必读（按顺序）
1. **[CURRENT_STATUS_SUMMARY.md](CURRENT_STATUS_SUMMARY.md)** - 了解项目现状
2. **[ROADMAP.md](ROADMAP.md)** - 了解开发计划
3. **[PROJECT_GUIDE.md](../architecture/PROJECT_GUIDE.md)** - 深入架构设计

### 开发相关
- **Mod开发**: [MOD_DEVELOPMENT_GUIDE.md](../development/MOD_DEVELOPMENT_GUIDE.md)
- **女孩包**: [GIRL_PACK_COMPATIBILITY.md](../development/GIRL_PACK_COMPATIBILITY.md)
- **存档系统**: [SAVE_FORMAT.md](../architecture/SAVE_FORMAT.md)
- **测试**: [CI_SETUP.md](../testing/CI_SETUP.md)

### 代码示例
- **完整Mod**: `game/custom/mods/Example - Price Override/`
- **集成测试**: `game/core/tools/integration_tests.rpy`

---

## 🔧 开发环境设置

### 必需工具
- **Ren'Py SDK** 8.2.0+
- **Python** 3.9+ (Ren'Py内置)
- **文本编辑器** (VS Code推荐)

### 推荐配置

**VS Code扩展**:
- Ren'Py Language
- Python
- Markdown All in One

**开发模式快捷键**:
- `Shift+O` - 打开控制台
- `Shift+R` - 快速重载
- `Shift+D` - 开发者菜单

---

## 🎓 从哪里开始？

### 场景A: 我想开发Mod
1. 阅读 [MOD_DEVELOPMENT_GUIDE.md](../development/MOD_DEVELOPMENT_GUIDE.md)
2. 研究 `game/custom/mods/Example - Price Override/`
3. 复制示例Mod，修改manifest
4. 实现你的功能
5. 测试并发布

**预计时间**: 2-4小时（简单Mod）

---

### 场景B: 我想贡献核心代码
1. 阅读 [PROJECT_GUIDE.md](../architecture/PROJECT_GUIDE.md) 了解架构
2. 查看 [ROADMAP.md](ROADMAP.md) 的优先级
3. 从P0任务开始（女孩包兼容性、测试）
4. 提交PR前运行 `tools/ci/run_tests.sh`

**推荐起点**: 
- 补全女孩包_BK.ini（简单）
- 扩展集成测试（中等）
- 实现拦截型钩子（高级）

---

### 场景C: 我想翻译到其他语言
1. 阅读 i18n系统文档
2. 复制 `game/tl/chinese_simplified/` 为新语言
3. 翻译 `.rpy` 文件
4. 配置字体（`i18n_service.rpy`）
5. 测试并提交

**预计时间**: 20-40小时（完整翻译）

---

## 🐛 常见问题

### Q: 游戏启动报错怎么办？
A: 
1. 检查是否是完整的游戏本体（包含资源文件）
2. 查看 `docs/testing/MANUAL_TEST_REPORT_2026-10-14.md` 的已知问题
3. 尝试删除 `game/saves/` 和 `game/cache/`
4. 查看错误日志，搜索文档

### Q: 我的Mod无法加载？
A: 
1. 检查 `mod.rpy` 的 manifest 格式
2. 确保 `init -100` 优先级正确
3. 查看控制台错误信息
4. 参考 Example Mod 的格式

### Q: 如何调试代码？
A: 
1. 使用 `renpy.log()` 输出日志
2. 开发者控制台 (`Shift+O`) 执行代码
3. 使用 `renpy.pause()` 暂停执行
4. 查看 `log.txt` 日志文件

### Q: 翻译冲突如何解决？
A: 
- Mod翻译不要重复定义通用字符串（ON/OFF/Close等）
- 只翻译Mod特有的字符串
- 使用唯一的key前缀（如 `mymod_setting_name`）

---

## 📞 获取帮助

### 文档
- **架构**: `docs/architecture/`
- **开发**: `docs/development/`
- **测试**: `docs/testing/`

### 工具
- **测试脚本**: `tools/ci/run_tests.sh`
- **女孩包验证**: `tools/test_girl_packs.py`
- **开发控制台**: 游戏内 `Shift+O`

### 社区
- **GitHub Issues**: 报告bug和建议
- **Discord/论坛**: 社区讨论（如有）

---

## ✅ 自检清单

开始开发前，确保你已经：

- [ ] 成功启动游戏
- [ ] 完成基础功能测试（新游戏、招募、经营、存档）
- [ ] 阅读了相关领域的文档
- [ ] 了解项目的代码规范
- [ ] 知道如何运行测试
- [ ] 知道如何查看日志

**如果以上都完成了，你已经准备好开发了！🎉**

---

## 🎯 第一个任务建议

根据你的兴趣选择：

### 初学者友好
1. **补全女孩包_BK.ini** (2-4小时)
   - 文件: `game/custom/characters/girls/`
   - 参考: [GIRL_PACK_COMPATIBILITY.md](../development/GIRL_PACK_COMPATIBILITY.md)
   - 价值: 提高兼容性到100%

2. **添加简单测试** (2-3小时)
   - 文件: `game/core/tools/integration_tests.rpy`
   - 参考: 现有测试代码
   - 价值: 提高测试覆盖率

### 中等难度
1. **创建一个简单Mod** (4-6小时)
   - 参考: Example - Price Override
   - 文档: [MOD_DEVELOPMENT_GUIDE.md](../development/MOD_DEVELOPMENT_GUIDE.md)
   - 价值: 验证Mod API易用性

2. **优化启动性能** (1-2天)
   - 文件: `game/core/framework/girl_factory.rpy`
   - 目标: 延迟加载女孩包图片
   - 价值: 改善用户体验

### 高级挑战
1. **实现拦截型钩子** (3-5天)
   - 文件: `game/core/framework/mod_api_v2.rpy`
   - 设计: 允许Mod修改数据流
   - 价值: 大幅扩展Mod能力

2. **事件系统重构** (1-2周)
   - 文件: 多个事件相关文件
   - 目标: 统一事件架构
   - 价值: 降低维护成本

---

## 🎉 欢迎贡献！

这个项目需要你的帮助！无论是：
- 🐛 报告bug
- 📝 改进文档
- 🔧 修复问题
- ✨ 添加功能
- 🌐 翻译到其他语言
- 🎨 创建Mod

**所有贡献都很有价值！**

---

**最后更新**: 2026-10-14  
**维护者**: Lyeifal  
**协助**: Claude Opus 5.5
