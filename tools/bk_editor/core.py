# -*- coding: utf-8 -*-
"""
BK Editor — Core Module (Compatibility Layer)
EN: This module re-exports shared utilities for backward compatibility.
    New code should import from bk_editor.shared directly.
ZH: 本模块为兼容旧代码而重新导出共享工具。
    新代码应直接从 bk_editor.shared 导入。
"""

# EN: Re-export shared utilities.
# ZH: 重新导出共享工具。
from bk_editor.shared.paths import (
    PROJECT_ROOT,
    GAME_DIR,
    DATA_DIR,
    find_project_root,
)
from bk_editor.shared.json_io import (
    load_json,
    save_json,
    merge_json,
)
from bk_editor.shared.validators import (
    validate,
    validate_type,
    validate_story_event,
    validate_trait,
    validate_perk,
    validate_origin,
    validate_scenario,
)
from bk_editor.shared.widgets import (
    LabeledEntry,
    LabeledSpinbox,
    LabeledCombobox,
    LabeledCheckbox,
    EffectEditor,
    JsonTreeview,
)

# EN: Ensure legacy data directories exist (kept for compatibility).
# ZH: 确保旧版数据目录存在（为兼容性保留）。
import os
for sub in ["scenarios", "stories", "sandbox", "traits", "perks", "archetypes"]:
    os.makedirs(DATA_DIR / sub, exist_ok=True)

# EN: Legacy constants.
# ZH: 遗留常量。
EVENT_TYPES = ["any", "city", "day", "night", "morning"]
GAME_MODES = ["story", "sandbox", "scenario"]
WEEKDAYS = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SEASONS = ["", "Spring", "Summer", "Fall", "Winter"]

EFFECT_TYPES = ["boost", "change", "gain", "instant", "special", "personality", "set", "allow", "gift", "flower"]
EFFECT_TARGETS = [
    "reputation", "gold", "prestige", "AP", "energy", "mood",
    "beauty", "body", "charm", "refinement", "libido", "obedience", "constitution", "sensitivity",
    "service", "sex", "anal", "fetish",
    "waitress", "dancer", "masseuse", "geisha",
    "job customer budget", "whore customer budget",
    "customer defense", "crazy",
    "shop prices", "kidnap success", "spell learning",
    "special girl chance", "security upkeep",
    "overall customer satisfaction",
    "beauty preference", "body preference", "charm preference", "refinement preference",
]
EFFECT_SCOPES = [None, "brothel", "farm", "city", "world"]

GOAL_TYPES = ["gold", "ranked", "reputation", "prestige", "story"]
GOAL_CHANNELS = ["story", "story2", "story3", "advance", "advance2", "papa", "contract", "other"]

PERK_TYPES = ["skill", "passive", "active"]

STAT_NAMES = ["beauty", "body", "charm", "refinement", "libido", "obedience", "constitution", "sensitivity"]
SEX_ACTS = ["service", "sex", "anal", "fetish"]
JOBS = ["waitress", "dancer", "masseuse", "geisha"]
