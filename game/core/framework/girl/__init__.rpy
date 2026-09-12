#### Girl Components Package — Phase 2.1 / Phase 7 ####
# 女孩组件包 | Girl decomposition into focused components
# 原来的 5,900 行 Girl 类被分解为多个专注组件
# 每个组件持有 Girl 实例引用，用于跨组件访问
#
# Components (★ = contains moved method implementations):
#  ★girl_base          — Identity: name, ini loading, acquire init (身份)
#  ★girl_stats         — Stats, caps, minmax, spillover, stat tests (属性)
#  ★girl_progression   — Level/rank/XP-JP-rep/Perk/stat upgrades (进阶)
#  ★girl_traits        — Trait/perk management, shields, defense (特质)
#  ★girl_items         — Equipment, item use, take/give (物品)
#  ★girl_schedule      — Job assignment, workdays, schedule (日程)
#  ★girl_sex           — Sex acts, fixations, preferences, tastes (性行为)
#  ★girl_mood          — Mood, sanity, energy, health, tiredness (情绪)
#  ★girl_relationships — Love, fear, MC relations, spoil/terrify (关系)
#  ★girl_economy       — Prices, upkeep, tips, customer capacity (经济)
#  ★girl_dialogue      — Dialogue, personality, is_, descriptions (对话)
#  ★girl_pictures      — Image selection, refresh, evaluation (图片)
#   girl_effects       — Effect wrappers (delegates to EffectBearer) (效果)
#   girl_generation    — Randomization orchestration (生成)
#  ★girl_logging       — Logging, tracking, memory, recent events (日志)
#  ★girl_training      — Farm training, obedience, build-up (训练)
#
# Total: 16 components (girl_progression added in Phase 7 批次6)
#        ★ = 14/16 含迁移实现 (effects/generation 为薄包装/编排)
#        girlclass.rpy 5,900 → 1,148 行 (Girl 类 = __init__ + 委托壳 + 24 活别名)
#        All existing 2,000+ call sites unchanged.
