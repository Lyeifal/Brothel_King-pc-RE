# -*- coding: utf-8 -*-
"""
BK Editor — Core Module
EN: Shared utilities for all editor submodules: JSON I/O, validation, constants.
ZH: 所有编辑器子模块的共享工具：JSON 读写、验证、常量定义。
"""

import json
import os
import sys
from pathlib import Path


# EN: Auto-detect project root from script location.
# ZH: 从脚本位置自动检测项目根目录。
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
GAME_DIR = PROJECT_ROOT / "game"
DATA_DIR = GAME_DIR / "custom" / "data"
SCHEMA_DIR = DATA_DIR / "_schemas"

# EN: Ensure data directories exist.
# ZH: 确保数据目录存在。
for sub in ["scenarios", "stories", "sandbox", "traits", "perks", "archetypes"]:
    (DATA_DIR / sub).mkdir(parents=True, exist_ok=True)


# ============================================================
# EN: JSON I/O helpers with UTF-8 encoding and pretty-print.
# ZH: 带 UTF-8 编码和格式化的 JSON 读写辅助函数。
# ============================================================

def load_json(path):
    """EN: Load JSON file, return empty list if not exists.
       ZH: 加载 JSON 文件，若不存在则返回空列表。"""
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data, indent=2):
    """EN: Save data to JSON file with pretty-print.
       ZH: 将数据以格式化方式保存到 JSON 文件。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
        f.write("\n")


def merge_json(path, new_items, key_field="id"):
    """EN: Merge new items into existing JSON file by key_field.
       Existing items with same key are updated, new ones appended.
       ZH: 按 key_field 将新项合并到现有 JSON 文件中。
       同键的现有项被更新，新项被追加。"""
    existing = load_json(path)
    existing_map = {item.get(key_field): item for item in existing if key_field in item}
    for item in new_items:
        k = item.get(key_field)
        if k is not None:
            existing_map[k] = item
        else:
            existing.append(item)
    save_json(path, list(existing_map.values()))


# ============================================================
# EN: Schema validation (lightweight, no external deps).
# ZH: 轻量级 Schema 验证（无外部依赖）。
# ============================================================

def validate_type(value, expected_type, field_name):
    """EN: Validate a single value against expected Python type.
       ZH: 将单个值与期望的 Python 类型进行验证。"""
    if expected_type is None:
        return True
    if expected_type == "string" and not isinstance(value, str):
        return f"{field_name}: expected string, got {type(value).__name__}"
    if expected_type == "number" and not isinstance(value, (int, float)):
        return f"{field_name}: expected number, got {type(value).__name__}"
    if expected_type == "boolean" and not isinstance(value, bool):
        return f"{field_name}: expected boolean, got {type(value).__name__}"
    if expected_type == "array" and not isinstance(value, list):
        return f"{field_name}: expected array, got {type(value).__name__}"
    if expected_type == "object" and not isinstance(value, dict):
        return f"{field_name}: expected object, got {type(value).__name__}"
    return True


def validate_story_event(item):
    """EN: Validate a StoryEvent JSON item.
       ZH: 验证 StoryEvent JSON 项。"""
    errors = []
    required = ["label"]
    for field in required:
        if field not in item:
            errors.append(f"Missing required field: {field}")
    if not isinstance(item.get("label"), str):
        errors.append("label must be a string")
    if "chapter" in item and not isinstance(item["chapter"], int):
        errors.append("chapter must be an integer")
    if "chance" in item and not (0.0 <= item["chance"] <= 1.0):
        errors.append("chance must be between 0.0 and 1.0")
    if "type" in item and item["type"] not in ("any", "city", "day", "night", "morning"):
        errors.append("type must be one of: any, city, day, night, morning")
    return errors


def validate_trait(item):
    """EN: Validate a Trait JSON item.
       ZH: 验证 Trait JSON 项。"""
    errors = []
    if "name" not in item:
        errors.append("Missing required field: name")
    if not isinstance(item.get("name"), str):
        errors.append("name must be a string")
    return errors


def validate_perk(item):
    """EN: Validate a Perk JSON item.
       ZH: 验证 Perk JSON 项。"""
    errors = []
    if "name" not in item:
        errors.append("Missing required field: name")
    if "type" not in item:
        errors.append("Missing required field: type")
    return errors


def validate_origin(item):
    """EN: Validate an Origin JSON item.
       ZH: 验证 Origin JSON 项。"""
    errors = []
    if "origin_id" not in item:
        errors.append("Missing required field: origin_id")
    if "name" not in item:
        errors.append("Missing required field: name")
    return errors


# ============================================================
# EN: Constants and type mappings shared across editors.
# ZH: 跨编辑器共享的常量和类型映射。
# ============================================================

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


def find_project_root():
    """EN: Return the detected project root path.
       ZH: 返回检测到的项目根目录路径。"""
    return PROJECT_ROOT
