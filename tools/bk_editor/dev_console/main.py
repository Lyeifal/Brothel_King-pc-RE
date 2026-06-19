#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BK Dev Console — Main Entry Point
EN: Internal game data editor for achievements, difficulty, NG+, and meta progression.
ZH: 内部游戏数据编辑器，用于成就、难度、NG+ 和局外养成。

Usage:
    python tools/bk_editor/dev_console/main.py
"""

import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path

# EN: Add tools/ to path so bk_editor package can be imported.
# ZH: 将 tools/ 加入路径以便导入 bk_editor 包。
_TOOLS_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_TOOLS_DIR))

from bk_editor.dev_console.editor import DevConsoleApp


def main():
    root = tk.Tk()
    app = DevConsoleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
