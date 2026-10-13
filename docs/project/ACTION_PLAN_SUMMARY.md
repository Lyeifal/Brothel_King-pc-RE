# BK Evolution - 行动计划速查表

> 更新: 2026-10-13
> 状态: 重构Phase 1-7已完成，需要补完测试、文档和Mod生态

---

## 🎯 你的目标完成情况

| 目标 | 完成度 | 说明 |
|------|--------|------|
| ✅ 支持i18n | 95% | I18nService + JSON _i18n，中文覆盖95% |
| ⚠️ 规范化Mod API | 70% | ModAPIV2架构优秀，但缺拦截能力和完整文档 |
| ⚠️ 兼容旧女孩包 | 未验证 | 代码逻辑存在，但缺自动化测试和文档 |

---

## ⚡ 立即行动清单（2-3周，让项目可用）

### Week 1: 验证与测试
```bash
# Day 1-2: 手动回归测试
□ 启动游戏到主菜单
□ 新游戏 → 难度选择 → 进入游戏
□ 招募一个女孩（市场/拍卖）
□ 经营一天 → 查看结算
□ 存档 → 退出 → 读档
□ 测试女孩面板、青楼报告、农场界面
□ 记录所有发现的bug

# Day 3-5: 自动化测试
□ 扩展 game/core/tools/test_runner.rpy
  - test_new_game_flow()
  - test_girl_acquisition()
  - test_one_day_settlement()
  - test_save_load_cycle()
□ 创建 tools/test_girl_packs.py
  - 遍历custom/girls/下所有女孩包
  - 验证每个包能create_girl成功
  - 输出兼容性报告

# Day 6-7: CI基础
□ 创建 tools/ci/run_tests.sh
  - 运行lint
  - 运行translate --count
  - 运行test_runner
  - 运行test_girl_packs
```

### Week 2: 文档补全
```bash
# Day 8-10: Mod开发文档
□ 创建 docs_EN/modding/MOD_DEVELOPMENT_GUIDE.md
  - 从零创建Mod（step-by-step）
  - 每个钩子的使用场景和示例
  - 注册API（trait/perk/event等）完整说明
  - Manifest配置参考
  - 以Auction House和Item Quality为案例

# Day 11-13: 女孩包文档
□ 创建 docs_EN/modding/GIRL_PACK_COMPATIBILITY.md
  - _BK.ini 格式完整说明
  - 必需字段 vs 可选字段
  - 字段映射（旧Trait名 → 新系统）
  - 图片标签规范
  - 兼容性检查清单
  - 常见问题troubleshooting

# Day 14: 存档文档
□ 创建 docs_EN/architecture/SAVE_FORMAT.md
  - 存档结构说明
  - AutoRepair修复规则清单
  - 如何添加新migration规则
```

### Week 3: 示例与清理
```bash
# Day 15-18: 参考Mod创建
□ Example - Price Override Mod
  - 展示拦截girl_acquired钩子
  - 修改价格计算逻辑
  - 完整注释说明
□ Example - New Location Mod
  - 展示注册新地点（如果API支持）
  - 或展示扩展现有地点功能
□ 更新 game/core/templates/mod_template/
  - 添加更多注释
  - 每个钩子的实际用例

# Day 19-21: 技术债清理
□ 运行 tools/verify_json_migration.py（需创建）
  - 验证所有JSON加载不返回None
□ 删除 _fallback_* 字典
  - grep -r "_fallback_" game/core/
  - 逐个删除，改为JSON加载失败报错
□ 清理已知问题
  - screen_girl_list.rpy vs screen_misc.rpy 的 girls 屏幕重复定义
```

---

## 📋 自检清单（发布前必过）

### 核心功能
- [ ] 能从零开始新游戏
- [ ] 能招募女孩（市场、拍卖、事件）
- [ ] 能完成完整一天的经营和结算
- [ ] 能存档和读档，数据一致
- [ ] 能访问所有主要界面（女孩面板、青楼、农场、城区）

### 女孩包兼容性
- [ ] custom/girls/下至少5个不同作者的女孩包能加载
- [ ] 女孩属性正确映射（Trait、Perk、图片）
- [ ] 有验证工具 (tools/test_girl_packs.py)
- [ ] 有升级文档 (GIRL_PACK_COMPATIBILITY.md)

### Mod系统
- [ ] 至少2个v2 Mod能启用并正常工作
- [ ] Mod钩子能触发（通过日志验证）
- [ ] 有完整开发文档 (MOD_DEVELOPMENT_GUIDE.md)
- [ ] 有参考示例 (至少2个Example Mod)

### 文档完整性
- [ ] MOD_DEVELOPMENT_GUIDE.md - 从零到完整Mod
- [ ] GIRL_PACK_COMPATIBILITY.md - 女孩包格式和兼容性
- [ ] SAVE_FORMAT.md - 存档结构和migration
- [ ] README.md 更新 - 指向新文档

### 测试覆盖
- [ ] Test Runner包含集成测试
- [ ] 女孩包自动化测试工具
- [ ] CI脚本可运行全套测试
- [ ] 无已知P0/P1 bug

---

## 🚀 后续规划（可选，按需展开）

### 短期（完成上述后的1-2个月）
- **拦截型钩子**: 实现5个关键钩子的cancel_hook调用
- **扩展注册API**: register_location, register_job等
- **Mod数据覆盖**: Mod可覆盖core/data/中的JSON

### 中期（3-6个月）
- **事件系统统一**: 迁移所有事件到EventEngine
- **events_dispatcher.rpy拆分**: 8611行 → 多个小文件
- **世界系统数据化**: District/Location/NPC/Shop → JSON

### 长期（6个月+）
- **v1 Mod API退役**: 提供迁移工具，逐步废弃
- **性能优化**: 图片缓存、事件匹配算法
- **编辑器增强**: 可视化编辑District等

---

## 💡 关键建议

### 当前最重要的事情
1. **测试** - 确保现有代码稳定
2. **文档** - 让其他人（包括未来的你）能理解和使用
3. **示例** - 展示系统能力，降低学习曲线

### 避免的陷阱
- ❌ 继续添加新功能（在测试和文档完成之前）
- ❌ 过度追求架构完美（事件系统统一等可以等）
- ❌ 假设"代码能跑就行"（用户需要文档和示例）

### 推荐的工作节奏
- Week 1: 验证现状（测试）
- Week 2: 补全文档
- Week 3: 示例和清理
- **暂停新功能至少1个月**，让社区试用和反馈

---

## 📞 需要帮助？

如果你在执行过程中遇到问题，可以按优先级寻求帮助：

### 优先级1: 回归测试发现bug
- 记录复现步骤
- 检查是否是重构引入的
- 查看REFACTORING_PROGRESS.md找到相关commit

### 优先级2: 文档不知道怎么写
- 参考现有文档风格（PROJECT_GUIDE.md等）
- 从用户视角思考："我不懂代码，想做X，怎么办？"
- 多用示例，少用术语

### 优先级3: 不确定优先级
- 问自己："这个功能阻塞用户使用吗？"
- 如果答案是否，放到backlog
- 优先做阻塞项

---

**记住**: 你已经完成了80%的技术工作，剩下的20%是"让用户能用"。

这20%的价值 ≥ 前面80%的价值。
