# -*- coding: utf-8 -*-
"""
BK Scenario Editor — Main Application
EN: Notebook-based editor for game world data.
ZH: 基于 Notebook 的游戏世界数据编辑器。
"""

import tkinter as tk
from tkinter import ttk

from bk_editor.scenario_editor.tabs.event_editor import EventEditorTab
from bk_editor.scenario_editor.tabs.scenario_editor_tab import ScenarioEditorTab
from bk_editor.scenario_editor.tabs.district_editor import DistrictEditorTab
from bk_editor.scenario_editor.tabs.npc_editor import NPCEditorTab
from bk_editor.scenario_editor.tabs.shop_editor import ShopEditorTab
from bk_editor.scenario_editor.tabs.image_tag_editor import ImageTagEditorTab


class ScenarioEditorApp:
    """EN: Main scenario editor window.
       ZH: 剧本编辑器主窗口。"""

    def __init__(self, root):
        self.root = root
        self.root.title("BK Scenario Editor — 剧本编辑器")
        self.root.geometry("1500x950")
        self.root.minsize(1200, 800)
        self.root.configure(bg="#1a1a2e")

        # Status bar first (tabs may call set_status during init)
        self.status = tk.Label(
            root,
            text="就绪",
            font=("Microsoft YaHei", 10),
            bg="#16213e",
            fg="#FFFFFF",
            anchor=tk.W,
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM, ipady=4)

        title = tk.Label(
            root,
            text="BK Scenario Editor",
            font=("Microsoft YaHei", 20, "bold"),
            bg="#1a1a2e",
            fg="#FFD700",
        )
        title.pack(pady=(10, 5))

        subtitle = tk.Label(
            root,
            text="事件 · 剧本 · 地图 · NPC · 商店 · 对话标签",
            font=("Microsoft YaHei", 11),
            bg="#1a1a2e",
            fg="#AAAAAA",
        )
        subtitle.pack(pady=(0, 10))

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self._add_tab("事件编辑器", EventEditorTab)
        self._add_tab("剧本管理", ScenarioEditorTab)
        self._add_tab("地图/地点", DistrictEditorTab)
        self._add_tab("NPC 编辑", NPCEditorTab)
        self._add_tab("商店编辑", ShopEditorTab)
        self._add_tab("对话图片标签", ImageTagEditorTab)

    def _add_tab(self, title, tab_class):
        frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(frame, text=title)
        editor = tab_class(frame, self)
        editor.pack(fill=tk.BOTH, expand=True)

    def set_status(self, text):
        self.status.config(text=text)
