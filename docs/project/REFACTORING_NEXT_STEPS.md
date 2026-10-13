# Brothel King Evolution - 项目重构现状分析与后续方案

> 更新时间: 2026-10-13
> 分析人: Claude Opus 5.5
> 目标: 梳理当前重构进度，提出下一步方案

---

## 一、项目现状总结

### 1.1 已完成的核心重构（✅ 优秀的基础）

你已经完成了一次**非常系统和高质量**的重构，建立了扎实的技术基础：

#### 架构层面：
- ✅ **服务容器化** (`GameServices`) - 解耦全局状态，11个核心服务注册
- ✅ **数据驱动化** (`DataLoader` + JSON) - 40+领域的数据外置，支持Mod覆盖
- ✅ **组件化** (Girl 16组件) - girlclass从5900行削减81%至1148行
- ✅ **UI分离** (108屏幕提取) - screens.rpy从8886行减至620行
- ✅ **Mod API v2** - 19个标准化钩子，声明式Manifest，版本化能力标识

#### i18n支持：
- ✅ `I18nService` 完整实现 (t/tn/tc/pronoun/possessive)
- ✅ JSON `_i18n` 字段自动注册翻译系统
- ✅ 中文覆盖率 27,933/29,367 (95%)

#### 开发工具：
- ✅ Dev Console (Shift+O)
- ✅ Test Runner (主菜单Tests按钮)
- ✅ 三个可视化编辑器 (girl pack / scenario / dev console GUI)

### 1.2 当前存在的主要问题

#### 问题1: 技术债务未完全清理
- ⚠️ **双重数据源**: `_fallback_*` 硬编码字典仍然保留，与JSON数据并存
- ⚠️ **巨型文件**: `events_dispatcher.rpy` 仍有8611行，职责混乱
- ⚠️ **v1 Mod API遗留**: HookManager与ModAPIV2并存，两套钩子系统

#### 问题2: Mod生态未充分展开
- ⚠️ **缺少实际拦截能力**: 19个钩子全部是"通知型"，`cancel_hook`无调用点
- ⚠️ **Mod API表面积不足**: 注册能力有限（trait/perk/event/tag/dialogue/quality）
- ⚠️ **Girl Pack兼容性机制不明确**: 如何保证新框架下旧女孩包仍可用？

#### 问题3: 文档与验证缺口
- ⚠️ **缺少Mod开发完整示例**: 当前示例都是stub，缺少真实功能展示
- ⚠️ **缺少自动化集成测试**: 只有单元smoke测试，缺少全流程回归测试
- ⚠️ **旧存档兼容性依赖AutoRepair**: 没有显式的migration路径

---

## 二、后续重构方案（优先级排序）

### 🎯 阶段A: 稳固基础（1-2周，高优先级）

#### A1. 建立完整的自动化测试体系
**为什么**: 后续重构的安全网，避免回归

**任务**:
1. 扩展Test Runner支持集成测试：
   ```python
   # game/core/tools/test_runner.rpy 增加测试套件
   - test_new_game_flow()       # 新游戏启动流程
   - test_girl_acquisition()     # 女孩获取与初始化
   - test_one_day_settlement()   # 完整一天结算
   - test_mod_lifecycle()        # Mod加载/卸载/钩子触发
   - test_save_load_cycle()      # 存档/读档一致性
   ```

2. 添加Girl Pack兼容性测试：
   ```python
   def test_legacy_girl_pack_loading():
       """确保旧格式_BK.ini仍能正确加载"""
       # 遍历 game/custom/girls/ 下所有包
       # 验证每个包至少能create_girl成功
   ```

3. 建立CI/CD基础：
   ```bash
   # tools/ci/run_tests.sh
   python Brothel_King.py . lint
   python Brothel_King.py . translate --count chinese_simplified
   python tools/verify_mod_api.py
   python -c "import renpy; renpy.bootstrap.bootstrap()" --run-tests
   ```

#### A2. 文档补全与规范
**为什么**: 降低未来自己和社区接手成本

**任务**:
1. 创建 `docs_EN/modding/MOD_DEVELOPMENT_GUIDE.md`:
   - 从零开始创建Mod的完整流程
   - 每个钩子的真实使用场景
   - 注册API的参数说明
   - 完整的Mod项目结构示例

2. 创建 `docs_EN/migration/GIRL_PACK_COMPATIBILITY.md`:
   - `_BK.ini` 格式规范
   - 字段映射关系（旧字段 → 新Trait/Perk系统）
   - 升级检查清单

3. 创建 `docs_EN/architecture/SAVE_FORMAT.md`:
   - 存档结构说明
   - AutoRepair修复规则清单
   - 如何添加新的migration规则

#### A3. 清理双重数据源
**为什么**: 避免数据不一致，明确唯一数据源

**任务**:
1. 逐个验证JSON加载完整性：
   ```python
   # tools/verify_json_migration.py (新建)
   for domain in ['traits', 'perks', 'achievements', ...]:
       json_data = DataLoader.load_xxx()
       fallback_data = _fallback_xxx_dict
       assert json_data is not None, f"{domain} JSON加载失败"
       compare_data_equivalence(json_data, fallback_data)
   ```

2. 一次性删除所有 `_fallback_*` 变量：
   - 修改DataLoader在JSON缺失时raise明确错误
   - 在启动时做integrity check

3. 将硬编码迁移到JSON的最后几个领域：
   - `start.rpy` 中的 District/Location/NPC/Shop 定义
   - 创建 `data/world/districts.json`, `data/world/locations.json` 等

---

### 🎯 阶段B: Mod生态完善（2-3周，中高优先级）

#### B1. 实现拦截型钩子机制
**为什么**: 释放Mod真正的能力，让社区可以深度定制游戏

**任务**:
1. 审计当前19个钩子，标识哪些应该支持拦截：
   ```python
   # 示例: girl_acquired 支持拦截
   # 用例: Mod可以修改购买价格，或替换获取逻辑
   
   # systems/events_dispatcher.rpy:8465
   # 修改前:
   $ mod_api_v2.execute_hook(HOOK_GIRL_ACQUIRED, {"girl": g, "price": p})
   
   # 修改后:
   context = {"girl": g, "price": p}
   if mod_api_v2.cancel_hook(HOOK_GIRL_ACQUIRED, context):
       # Mod返回True，取消默认逻辑
       return context.get("result")  # Mod可以返回自定义结果
   # 继续默认逻辑...
   ```

2. 添加5-10个新的钩子覆盖核心流程：
   ```python
   HOOK_GIRL_PRICE_CALCULATE   # 价格计算
   HOOK_CUSTOMER_MATCH         # 顾客匹配
   HOOK_TRAINING_RESULT        # 训练结果
   HOOK_SKILL_CHECK            # 技能检定
   HOOK_GIRL_TRAIT_ADD         # 添加特质时
   ```

3. 创建参考Mod展示拦截能力：
   ```
   game/custom/mods/Advanced Pricing/
   ├── mod.rpy                 # 重写价格计算逻辑
   ├── pricing_algorithm.rpy   # 复杂定价算法
   └── README.md               # 说明如何覆盖游戏逻辑
   ```

#### B2. 扩展Mod注册API表面积
**为什么**: 让Mod可以注册更多类型的内容

**任务**:
1. 添加缺失的注册API：
   ```python
   # game/core/systems/mods/mod_api_v2.rpy
   
   def register_location(self, location_id, location):
       """注册自定义地点（Mod可添加新城区）"""
       
   def register_job(self, job_id, job):
       """注册自定义工作类型"""
       
   def register_customer_type(self, type_id, customer_type):
       """注册自定义顾客类型"""
       
   def register_girl_component(self, component_name, component_class):
       """高级API: 让Mod可以扩展Girl的组件系统"""
   ```

2. 实现数据覆盖机制：
   ```python
   # Mod可以覆盖core/data/中的任意JSON
   # 加载顺序: core/data/ → custom/mods/*/data/
   # 合并策略: 深度合并，Mod数据优先
   ```

#### B3. Girl Pack兼容性保障
**为什么**: 确保社区资源不会因为重构而失效

**任务**:
1. 明确女孩包加载流程：
   ```python
   # game/core/framework/girl_factory.rpy
   def create_girl(pack_path):
       # 1. 读取_BK.ini
       ini_data = read_ini(pack_path / "_BK.ini")
       
       # 2. 字段映射（旧格式→新系统）
       traits = map_legacy_traits(ini_data.get("traits", []))
       perks = map_legacy_perks(ini_data.get("perks", []))
       
       # 3. 图片目录扫描（兼容旧标签格式）
       pics = scan_girl_pictures(pack_path, legacy_compat=True)
       
       # 4. 创建Girl实例
       girl = Girl(name=ini_data["name"], ...)
       return girl
   ```

2. 创建女孩包验证工具：
   ```python
   # tools/validate_girl_pack.py
   # 扫描custom/girls/下所有包
   # 检查: _BK.ini格式、必需字段、图片文件存在性
   # 输出: 兼容性报告 + 推荐修复建议
   ```

3. 提供女孩包升级指南：
   ```
   docs_EN/modding/GIRL_PACK_UPGRADE_GUIDE.md
   - 旧格式 vs 新格式对比
   - 自动迁移工具使用方法
   - 新特性（JSON覆盖、_i18n支持）
   ```

---

### 🎯 阶段C: 遗留系统重构（3-4周，中等优先级）

#### C1. 事件系统统一化
**为什么**: 消除EventEngine vs 遗留city_events/daily_events的二元性

**任务**:
1. 将遗留事件迁移到EventEngine：
   ```python
   # 当前: city_events / daily_events 混杂在events_dispatcher.rpy
   # 目标: 全部通过EventEngine.register_event统一管理
   
   # 迁移步骤:
   # 1. 审计events_dispatcher.rpy中所有"if chance:"分支
   # 2. 提取为StoryEvent JSON定义
   # 3. 通过EventEngine注册
   # 4. 删除events_dispatcher.rpy中对应代码
   ```

2. 重构events_dispatcher.rpy（8611行 → <2000行）：
   ```python
   # 拆分为:
   systems/events/
   ├── event_engine.rpy           # 已存在
   ├── event_dispatcher.rpy       # 重写: 纯调度逻辑
   ├── story_events.rpy           # 主线事件定义
   ├── city_events.rpy            # 城市事件定义
   └── daily_events.rpy           # 日常事件定义
   ```

3. 删除EventBridge兼容层：
   ```python
   # 当所有事件迁移完成后
   # game/core/systems/events/event_bridge.rpy → 删除
   ```

#### C2. v1 Mod API退役评估
**为什么**: 两套系统并存增加维护负担

**任务**:
1. 评估现存v1 Mod依赖：
   ```bash
   # 扫描custom/mods/下使用v1 API的Mod
   grep -r "Mod(" game/custom/mods/
   grep -r "detected_mods" game/custom/mods/
   ```

2. 提供v1→v2迁移工具：
   ```python
   # tools/migrate_mod_v1_to_v2.py
   # 自动转换Mod代码结构
   # 生成v2 manifest
   ```

3. 弃用计划：
   ```
   - v1 API标记为deprecated（文档/代码注释）
   - 保留1-2个版本供迁移
   - 最终删除game/core/framework/challenges.rpy Mod类
   ```

#### C3. 世界系统数据化
**为什么**: 最后的大块硬编码

**任务**:
1. District/Location外置JSON：
   ```json
   // data/world/districts.json
   {
     "slums": {
       "name_i18n": "Slums",
       "locations": ["tavern", "market", ...],
       "danger_level": 3
     }
   }
   
   // data/world/locations.json
   {
     "tavern": {
       "name_i18n": "Tavern",
       "district": "slums",
       "actions": ["drink", "gamble", ...]
     }
   }
   ```

2. NPC/Shop定义外置：
   ```json
   // data/npcs/npcs.json
   // data/shops/shops.json
   ```

3. 修改start.rpy加载逻辑：
   ```python
   # 删除硬编码的district/location定义
   # 改为: districts = DataLoader.load_districts()
   ```

---

### 🎯 阶段D: 高级特性与polish（4+周，低优先级）

#### D1. 性能优化
- 女孩图片延迟加载优化
- EventEngine事件匹配算法优化
- 大量女孩时的UI渲染优化

#### D2. 编辑器增强
- Scenario Editor支持District/Location可视化编辑
- Girl Pack Editor增加批量操作
- 新增Item Editor

#### D3. 多语言生态
- 添加第三语言支持（如日语）示例
- 翻译工作流文档化
- 翻译质量自动检查工具

---

## 三、具体实施建议（接下来怎么做）

### 3.1 短期（1个月内）

#### 优先级1: 测试体系（阻塞后续重构）
```bash
# 第一步: 扩展Test Runner
1. 编辑 game/core/tools/test_runner.rpy
2. 添加 test_new_game_flow / test_one_day_settlement 等
3. 运行测试，确保当前代码通过

# 第二步: Girl Pack兼容性测试
1. 新建 tools/test_girl_packs.py
2. 遍历 custom/girls/ 下所有包
3. 验证每个包能成功加载

# 第三步: CI脚本
1. 新建 tools/ci/run_tests.sh
2. 集成lint / translate / 测试
3. 每次commit前运行
```

#### 优先级2: 文档补全（降低重拾成本）
```bash
# MOD_DEVELOPMENT_GUIDE.md
- 参考现有mod（Auction House, Item Quality）
- 从零到完整Mod的step-by-step教程
- 每个钩子的实际用例

# GIRL_PACK_COMPATIBILITY.md
- _BK.ini 字段完整说明
- 旧女孩包能否直接用？如何升级？
- 常见问题troubleshooting

# SAVE_FORMAT.md
- 当前存档结构（哪些数据持久化）
- AutoRepair都修复了什么
- 如何添加新的migration
```

#### 优先级3: 双重数据源清理（技术债）
```bash
# 1. 验证JSON完整性
python tools/verify_json_migration.py
# 如发现缺失，补全JSON

# 2. 删除fallback字典
grep -r "_fallback_" game/core/
# 逐个删除，改为JSON加载失败时报错

# 3. 最后的硬编码迁移
# start.rpy → data/world/*.json
```

### 3.2 中期（2-3个月）

#### Mod生态建设
1. **拦截型钩子**:
   - 选5个最有价值的钩子（girl_acquired, customer_match, price_calculate等）
   - 实现cancel_hook调用
   - 创建示例Mod展示拦截能力

2. **扩展注册API**:
   - register_location / register_job / register_customer_type
   - 实现数据覆盖机制（Mod数据 > core数据）

3. **参考Mod库**:
   ```
   custom/mods/
   ├── Example - Price Override/      # 展示拦截价格计算
   ├── Example - New District/        # 展示添加新城区
   ├── Example - Custom Training/     # 展示自定义训练系统
   └── Example - UI Extension/        # 展示添加UI屏幕
   ```

#### Girl Pack工具链
1. `tools/validate_girl_pack.py` - 自动检查女孩包兼容性
2. `tools/migrate_girl_pack.py` - 自动升级旧格式
3. Girl Pack Editor增强 - 支持新特性（JSON覆盖、_i18n）

### 3.3 长期（6个月+）

#### 遗留系统重构
- events_dispatcher.rpy拆分（8611行 → 多个小文件）
- 事件系统统一到EventEngine
- v1 Mod API退役

#### 世界系统数据化
- District/Location/NPC/Shop全部JSON化
- start.rpy瘦身

#### 高级特性
- 性能优化（图片缓存、事件匹配算法）
- 编辑器增强（可视化编辑District）
- 多语言生态（第三语言示例）

---

## 四、关于你的重构初衷的评估

### 你的目标回顾:
> 让游戏支持i18n，规范化mod开发的api，让社区mod开发更轻松，能兼容以前的女孩包

### 当前达成情况:

#### ✅ i18n支持 - **已达成95%**
- I18nService完整实现
- JSON `_i18n` 字段自动注册
- 中文覆盖率95%
- **剩余**: 部分UI字符串未包裹`__()`

#### ⚠️ 规范化Mod API - **部分达成70%**
- ModAPIV2架构优秀（Manifest、版本化、能力标识）
- 19个钩子已接入
- **缺失**: 拦截能力、注册API表面积不足
- **缺失**: 完整的Mod开发文档和示例

#### ⚠️ 女孩包兼容性 - **未明确验证**
- 理论上兼容（girl_factory.rpy有读取_BK.ini逻辑）
- **缺失**: 自动化兼容性测试
- **缺失**: 升级指南和工具
- **风险**: 未覆盖的edge case可能导致旧包加载失败

### 建议的最小可行产品（MVP）:

如果要**现在**就让社区可以安全使用你的重构版本，需要完成：

1. **测试覆盖** - 至少通过100个女孩包加载测试
2. **Mod文档** - 完整的MOD_DEVELOPMENT_GUIDE.md
3. **女孩包文档** - GIRL_PACK_COMPATIBILITY.md + 验证工具
4. **示例Mod** - 3-5个展示不同能力的参考Mod
5. **回归测试** - 主流程（新游戏→招募女孩→经营一周→存档读档）无崩溃

预计时间: **2-3周全职工作**

---

## 五、个人建议

作为AI，我从代码质量和架构设计角度给你以下建议：

### 你已经做得很好的地方 👍
1. **架构设计**: 服务容器、组件化、数据驱动，都是教科书级别的重构
2. **文档习惯**: PROJECT_GUIDE, REFACTORING_PROGRESS等文档非常详细
3. **渐进式重构**: 通过委托shell保持2000+调用点不变，降低回归风险
4. **工具链**: 三个编辑器零依赖，Test Runner集成，体现了对开发者体验的重视

### 可以改进的地方 🔧
1. **测试先行**: 重构前应该先建立测试覆盖，你是"裸奔"重构（高风险）
2. **文档滞后**: 很多架构决策在代码里，但缺少面向使用者的指南
3. **MVP意识**: 追求完美的架构，但忽略了"能用"和"完美"之间的优先级
4. **兼容性验证**: 女孩包兼容性是你的核心目标之一，但没有自动化验证

### 接下来应该做什么？

如果你的时间有限（比如只有周末）：
1. **第一周末**: 写测试 + 运行一遍主流程，确保没有明显崩溃
2. **第二周末**: 写MOD_DEVELOPMENT_GUIDE.md，用Auction House Mod作为案例
3. **第三周末**: 写GIRL_PACK_COMPATIBILITY.md，测试5-10个真实女孩包
4. **第四周末**: 创建1-2个示例Mod，展示钩子和注册API

如果你想做到生产可用：
- 按照上面"短期（1个月内）"的计划执行
- 重点是测试覆盖和文档，而不是新功能

如果你想继续打磨架构：
- 先完成测试和文档（安全网）
- 再去做事件系统统一、v1 API退役等深度重构

### 最后的建议

你的重构**技术上非常扎实**，但**工程上缺少最后一公里**：
- 代码能跑 ≠ 用户能用
- 架构优秀 ≠ 社区能上手

建议你花2-3周时间做"收尾工作"（测试+文档+示例），让这个项目从"个人重构"变成"社区可用"。

之后，如果你想继续打磨，可以按照上面的阶段B/C/D逐步推进。

---

## 附录：快速自检清单

在继续任何新功能之前，请先确认：

- [ ] 能否从零开始新游戏？
- [ ] 能否招募一个女孩？
- [ ] 能否完成一天的经营结算？
- [ ] 能否存档并读档？
- [ ] 能否加载至少一个女孩包（从custom/girls/）？
- [ ] 能否启用至少一个Mod（v2 API）？
- [ ] Mod的钩子是否触发？
- [ ] 是否有完整的Mod开发文档？
- [ ] 是否有女孩包兼容性说明文档？

如果有任何一项是"不确定"或"否"，建议先修复，再继续新功能。

---

**总结**: 你的重构非常优秀，但需要补充测试、文档和示例，才能让社区真正受益。建议优先完成"阶段A"，再考虑后续功能。
