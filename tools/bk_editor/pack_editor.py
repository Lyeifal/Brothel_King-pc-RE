# -*- coding: utf-8 -*-
"""
BK Editor — Girl Pack Tool
EN: Visual tool for creating/editing Girl Packs.
ZH: 女孩包制作的可视化工具。
"""

import tkinter as tk
from tkinter import ttk, filedialog
from bk_editor.core import DATA_DIR


class PackEditorFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app

        tk.Label(self, text="女孩包制作工具", font=("Microsoft YaHei", 16, "bold"), bg="#1a1a2e", fg="#FFD700").pack(pady=10)
        tk.Label(self, text="功能：可视化编辑 _BK.ini、图片标签检测、一键打包", bg="#1a1a2e", fg="#AAAAAA", font=("Microsoft YaHei", 11)).pack(pady=5)

        self.info = tk.Label(self, text="【待实现】文件夹选择 + INI 可视化编辑 + 预览", bg="#1a1a2e", fg="#666666", font=("Microsoft YaHei", 12))
        self.info.pack(expand=True)
