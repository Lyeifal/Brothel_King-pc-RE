# -*- coding: utf-8 -*-
"""
BK Editor — Validators
EN: Lightweight validation helpers with no external dependencies.
ZH: 轻量级验证辅助函数，无外部依赖。
"""


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


def validate_scenario(item):
    """EN: Validate a Scenario JSON item.
       ZH: 验证 Scenario JSON 项。"""
    errors = []
    if "scenario_id" not in item:
        errors.append("Missing required field: scenario_id")
    if "name" not in item:
        errors.append("Missing required field: name")
    return errors


def validate_achievement(item):
    """EN: Validate an Achievement JSON item.
       ZH: 验证 Achievement JSON 项。"""
    errors = []
    if "title" not in item:
        errors.append("Missing required field: title")
    if "target" not in item:
        errors.append("Missing required field: target")
    return errors


def validate_difficulty_table(item):
    """EN: Validate a difficulty modifier table.
       ZH: 验证难度修正表。"""
    errors = []
    if not isinstance(item, dict):
        errors.append("difficulty table must be an object")
        return errors
    numeric_keys = [
        "gold", "budget", "rewards", "resources", "stats", "pref",
        "xp", "jp", "rep", "prestige", "tax rate", "satisfaction", "security",
    ]
    for key in numeric_keys:
        if key in item and not isinstance(item[key], (int, float)):
            errors.append(f"{key} must be a number")
    return errors


def validate(item, schema_name):
    """EN: Generic validation dispatcher.
       ZH: 通用验证分发器。"""
    validators = {
        "story_event": validate_story_event,
        "trait": validate_trait,
        "perk": validate_perk,
        "origin": validate_origin,
        "scenario": validate_scenario,
        "achievement": validate_achievement,
        "difficulty": validate_difficulty_table,
    }
    fn = validators.get(schema_name)
    if not fn:
        return False, f"Unknown schema: {schema_name}"
    errs = fn(item)
    if errs:
        return False, "\n".join(errs)
    return True, ""
