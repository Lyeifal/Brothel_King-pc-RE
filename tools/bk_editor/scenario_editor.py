# -*- coding: utf-8 -*-
"""
BK Editor — Scenario Editor
EN: Visual editor for community-created scenarios.
ZH: 社区创作剧本的可视化编辑器。
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from bk_editor.core import load_json, save_json, DATA_DIR


class ScenarioEditorFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app

        # EN: Title
        tk.Label(self, text="剧本编辑器", font=("Microsoft YaHei", 16, "bold"), bg="#1a1a2e", fg="#FFD700").pack(pady=10)

        # EN: Placeholder UI
        tk.Label(self, text="功能：新建/编辑剧本 JSON，设置规则与胜利条件", bg="#1a1a2e", fg="#AAAAAA", font=("Microsoft YaHei", 11)).pack(pady=5)

        self.info = tk.Label(self, text="【待实现】剧本列表 + 属性表单", bg="#1a1a2e", fg="#666666", font=("Microsoft YaHei", 12))
        self.info.pack(expand=True)
