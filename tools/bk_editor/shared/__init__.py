# -*- coding: utf-8 -*-
"""
BK Editor — Shared Library
EN: Common utilities used by all three editor suites.
ZH: 三个编辑器套件共用的通用工具库。
"""

from .paths import PROJECT_ROOT, GAME_DIR, DATA_DIR, GIRLS_DIR, find_project_root
from .json_io import load_json, save_json, merge_json
from .validators import validate, validate_type
from .widgets import (
    LabeledEntry,
    LabeledSpinbox,
    LabeledCombobox,
    LabeledCheckbox,
    EffectEditor,
    JsonTreeview,
)

__all__ = [
    "PROJECT_ROOT",
    "GAME_DIR",
    "DATA_DIR",
    "find_project_root",
    "load_json",
    "save_json",
    "merge_json",
    "validate",
    "validate_type",
    "LabeledEntry",
    "LabeledSpinbox",
    "LabeledCombobox",
    "LabeledCheckbox",
    "EffectEditor",
    "JsonTreeview",
]
