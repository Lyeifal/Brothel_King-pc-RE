# -*- coding: utf-8 -*-
"""
BK Editor — JSON I/O
EN: JSON read/write helpers used across the editor suite.
ZH: 编辑器套件共用的 JSON 读写辅助函数。
"""

import json
from pathlib import Path

from .paths import DATA_DIR


def load_json(path, default=None):
    """EN: Load JSON file; return default if not exists or invalid.
       ZH: 加载 JSON 文件；不存在或无效时返回 default。"""
    if default is None:
        default = []
    path = Path(path)
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data, indent=2):
    """EN: Save data to JSON file with pretty-print.
       ZH: 将数据以格式化方式保存到 JSON 文件。"""
    path = Path(path)
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
    if not isinstance(existing, list):
        existing = []
    existing_map = {item.get(key_field): item for item in existing if key_field in item}
    for item in new_items:
        k = item.get(key_field)
        if k is not None:
            existing_map[k] = item
        else:
            existing.append(item)
    save_json(path, list(existing_map.values()))


def data_json(rel_path, default=None):
    """EN: Convenience helper to load a JSON file under game/core/data/.
       ZH: 便捷函数：加载 game/core/data/ 下的 JSON 文件。"""
    return load_json(DATA_DIR / rel_path, default=default)


def save_data_json(rel_path, data, indent=2):
    """EN: Convenience helper to save a JSON file under game/core/data/.
       ZH: 便捷函数：保存 game/core/data/ 下的 JSON 文件。"""
    save_json(DATA_DIR / rel_path, data, indent=indent)
