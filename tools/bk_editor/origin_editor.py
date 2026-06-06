# -*- coding: utf-8 -*-
"""
BK Editor — Origin Editor
EN: Visual editor for Sandbox mode player origins.
ZH: 沙盒模式玩家出身的可视化编辑器。
"""

import tkinter as tk
from bk_editor.core import load_json, save_json, DATA_DIR


class OriginEditorFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app

        tk.Label(self, text="出身编辑器", font=("Microsoft YaHei", 16, "bold"), bg="#1a1a2e", fg="#FFD700").pack(pady=10)
        tk.Label(self, text="功能：增删改查沙盒模式出身，编辑天赋与起始奖励", bg="#1a1a2e", fg="#AAAAAA", font=("Microsoft YaHei", 11)).pack(pady=5)

        self.info = tk.Label(self, text="【待实现】出身列表 + 天赋编辑器", bg="#1a1a2e", fg="#666666", font=("Microsoft YaHei", 12))
        self.info.pack(expand=True)
