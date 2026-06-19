#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BK Girl Pack Editor — Main Entry Point
EN: Visual editor for girl packs: image tagging, _BK.ini editing, custom traits/perks, pack validation.
ZH: 女孩包可视化编辑器：图片打标、_BK.ini 编辑、自定义特质/天赋、包验证。

Usage:
    python tools/bk_editor/girl_pack_editor/main.py
"""

import tkinter as tk
import sys
from pathlib import Path

# EN: Add tools/ to path so bk_editor package can be imported.
# ZH: 将 tools/ 加入路径以便导入 bk_editor 包。
_TOOLS_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_TOOLS_DIR))

from bk_editor.girl_pack_editor.editor import GirlPackEditorApp


def main():
    root = tk.Tk()
    app = GirlPackEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
