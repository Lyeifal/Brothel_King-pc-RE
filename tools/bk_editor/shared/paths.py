# -*- coding: utf-8 -*-
"""
BK Editor — Path Constants
EN: Centralized path resolution for the editor suite.
ZH: 编辑器套件的路径常量集中定义。
"""

import sys
from pathlib import Path


# EN: Detect project root from this file's location: tools/bk_editor/shared/paths.py
# ZH: 根据本文件位置推断项目根目录：tools/bk_editor/shared/paths.py
_PROJECT_ROOT_CANDIDATE = Path(__file__).resolve().parent.parent.parent.parent


def find_project_root():
    """EN: Return the detected project root path.
       ZH: 返回检测到的项目根目录路径。"""
    return _PROJECT_ROOT_CANDIDATE


PROJECT_ROOT = find_project_root()
GAME_DIR = PROJECT_ROOT / "game"
CUSTOM_DIR = GAME_DIR / "custom"
CORE_DIR = GAME_DIR / "core"
DATA_DIR = CORE_DIR / "data"
GIRLS_DIR = CUSTOM_DIR / "girls"
SCHEMA_DIR = DATA_DIR / "_schemas"


def ensure_data_subdirs():
    """EN: Ensure commonly used data subdirectories exist.
       ZH: 确保常用的数据子目录存在。"""
    for sub in [
        "scenarios", "stories", "sandbox", "traits", "perks", "archetypes",
        "achievements", "difficulty", "ngp", "meta",
    ]:
        (DATA_DIR / sub).mkdir(parents=True, exist_ok=True)


def inject_project_root():
    """EN: Add project root to sys.path so Ren'Py modules can be imported if needed.
       ZH: 将项目根目录加入 sys.path，以便在需要时导入 Ren'Py 模块。"""
    root = str(PROJECT_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
