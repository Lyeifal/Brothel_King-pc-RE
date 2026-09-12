#### Girl Components Package — Phase 2.1 ####
# 女孩组件包 | Girl decomposition into focused components
# 原来的 5,900 行 Girl 类被分解为多个专注组件
# 每个组件持有 Girl 实例引用，用于跨组件访问
#
# Components (★ = contains moved method implementations):
#   girl_base          — Identity: name, rank, level, serialization (身份)
#   girl_stats         — Stats, stat caps, stat changes, spillover (属性)
#   girl_progression   — Level/rank/XP-JP-rep/Perk/stat upgrades (进阶)
#  ★girl_traits        — Trait/perk management (特质) — generate_traits
#   girl_items         — Equipment, items, inventory (物品)
#  ★girl_schedule      — Job assignment, workdays, schedule (日程) — get_status
#  ★girl_sex           — Sex acts, fixations, preferences (性行为)
#  ★girl_mood          — Mood, sanity, energy, health (情绪) — change_energy, heal, rest
#  ★girl_relationships — Love, fear, obedience, MC relations (关系) — change_love/fear
#  ★girl_economy       — Prices, upkeep, tips, performance (经济) — get_price/xp/jp/rep
#  ★girl_dialogue      — Dialogue selection, say(), personality (对话) — pick/say/rand_say
#  ★girl_pictures      — Image selection, refresh, evaluation (图片) — get_fix_pic
#   girl_effects       — Effect wrappers (delegates to EffectBearer) (效果)
#   girl_generation    — Randomization, personality, BG, preferences (生成)
#  ★girl_logging       — Logging, tracking, recent events (日志)
#
# Total: 11 components (10 delegation + 1 stub)
#        ★ = 10/11 含迁移实现
#        ~136 _impl aliases in Girl class
#        All existing 2,000+ call sites unchanged.
