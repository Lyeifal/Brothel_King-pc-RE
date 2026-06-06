# -*- coding: utf-8 -*-
"""
BK Editor — Girl System Editor
EN: Visual editor for traits, perks, stats and archetypes.
ZH: 特质、天赋、属性与原型系统的可视化编辑器。
"""

import tkinter as tk
from tkinter import ttk
from bk_editor.core import load_json, save_json, DATA_DIR


class GirlEditorFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app

        tk.Label(self, text="女孩系统编辑器", font=("Microsoft YaHei", 16, "bold"), bg="#1a1a2e", fg="#FFD700").pack(pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # EN: Trait tab
        trait_tab = tk.Frame(notebook, bg="#1a1a2e")
        notebook.add(trait_tab, text="特质管理")
        tk.Label(trait_tab, text="【待实现】Trait 增删改查", bg="#1a1a2e", fg="#666666").pack(expand=True)

        # EN: Perk tab
        perk_tab = tk.Frame(notebook, bg="#1a1a2e")
        notebook.add(perk_tab, text="天赋管理")
        tk.Label(perk_tab, text="【待实现】Perk 增删改查 + 天赋树", bg="#1a1a2e", fg="#666666").pack(expand=True)

        # EN: Stats tab
        stats_tab = tk.Frame(notebook, bg="#1a1a2e")
        notebook.add(stats_tab, text="属性系统")
        tk.Label(stats_tab, text="【待实现】基础属性定义与计算公式", bg="#1a1a2e", fg="#666666").pack(expand=True)

        # EN: Balance tab
        balance_tab = tk.Frame(notebook, bg="#1a1a2e")
        notebook.add(balance_tab, text="数值平衡")
        tk.Label(balance_tab, text="【待实现】批量调整与平衡报告", bg="#1a1a2e", fg="#666666").pack(expand=True)
