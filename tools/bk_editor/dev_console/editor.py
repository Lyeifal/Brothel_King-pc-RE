# -*- coding: utf-8 -*-
"""
BK Dev Console — Main Application
EN: Notebook-based editor for JSON-driven game data.
ZH: 基于 Notebook 的 JSON 驱动游戏数据编辑器。
"""

import tkinter as tk
from tkinter import ttk

from bk_editor.dev_console.tabs.achievement_editor import AchievementEditorTab
from bk_editor.dev_console.tabs.difficulty_editor import DifficultyEditorTab
from bk_editor.dev_console.tabs.ngp_editor import NGPEditorTab
from bk_editor.dev_console.tabs.meta_editor import MetaEditorTab
from bk_editor.dev_console.tabs.data_sync import DataSyncTab


class DevConsoleApp:
    """EN: Main dev console window.
       ZH: 开发控制台主窗口。"""

    def __init__(self, root):
        self.root = root
        self.root.title("BK Dev Console — 游戏数据编辑器")
        self.root.geometry("1400x900")
        self.root.minsize(1100, 700)
        self.root.configure(bg="#1a1a2e")

        # EN: Title bar.
        # ZH: 标题栏。
        title = tk.Label(
            root,
            text="BK Dev Console",
            font=("Microsoft YaHei", 20, "bold"),
            bg="#1a1a2e",
            fg="#FFD700",
        )
        title.pack(pady=(10, 5))

        subtitle = tk.Label(
            root,
            text="成就 · 难度 · NG+ · 局外养成 · 数据同步",
            font=("Microsoft YaHei", 11),
            bg="#1a1a2e",
            fg="#AAAAAA",
        )
        subtitle.pack(pady=(0, 10))

        # EN: Status bar must exist before tabs call set_status during init.
        # ZH: 状态栏必须在标签页初始化调用 set_status 之前创建。
        self.status = tk.Label(
            root,
            text="就绪",
            font=("Microsoft YaHei", 10),
            bg="#16213e",
            fg="#FFFFFF",
            anchor=tk.W,
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM, ipady=4)

        # EN: Notebook with tabs.
        # ZH: 带标签页的 Notebook。
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self._add_tab("成就", AchievementEditorTab)
        self._add_tab("难度", DifficultyEditorTab)
        self._add_tab("NG+", NGPEditorTab)
        self._add_tab("局外养成", MetaEditorTab)
        self._add_tab("数据同步", DataSyncTab)

    def _add_tab(self, title, tab_class):
        """EN: Add a new tab with the given editor class.
           ZH: 添加一个包含指定编辑器类的新标签页。"""
        frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(frame, text=title)
        editor = tab_class(frame, self)
        editor.pack(fill=tk.BOTH, expand=True)

    def set_status(self, text):
        """EN: Update status bar text.
           ZH: 更新状态栏文字。"""
        self.status.config(text=text)
