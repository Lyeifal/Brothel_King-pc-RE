#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BK Scenario Editor — Main Entry Point
EN: Visual editor for scenarios, story events, districts/locations, NPCs, shops, and dialogue image tags.
ZH: 剧本编辑器：场景、事件、地图、NPC、商店、对话图片标签。

Usage:
    python tools/bk_editor/scenario_editor/main.py
"""

import tkinter as tk
import sys
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_TOOLS_DIR))

from bk_editor.scenario_editor.editor import ScenarioEditorApp


def main():
    root = tk.Tk()
    app = ScenarioEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
