# -*- coding: utf-8 -*-
"""
BK Scenario Editor — Shop Reference Tab
EN: Reference for shop settings and item types + snippet generator.
ZH: 商店设置与物品类型参考 + 代码片段生成器。
"""

import tkinter as tk
from tkinter import ttk


class ShopEditorTab(tk.Frame):
    """EN: Shop settings reference + item snippet generator.
       ZH: 商店设置参考 + 物品代码生成器。"""

    ITEM_TYPES = [
        "Weapon", "Dress", "Ring", "Necklace", "Accessory",
        "Food", "Gift", "Misc", "Flower", "Toy", "Supplies",
    ]

    QUALITIES = ["junk", "common", "rare", "exceptional", "S", "U", "M", "F"]

    SHOP_SETTINGS = {
        "shop_item_number": {
            "shop": {"junk": "d3 + 3", "common": "d6", "rare": "d3", "exceptional": "d3 + -2"},
            "city": {"junk": "d6", "common": "d6 + 2", "rare": "d3 + 1", "exceptional": "d3 + -1"},
            "minion": {"minion": "d5", "item": "d4 + -1"},
        },
        "shop_chapter_modifiers": {
            1: {"junk": 0, "common": 0, "rare": 0, "exceptional": 0, "minion": 0, "item": 0},
            2: {"junk": 1, "common": 1, "rare": 0, "exceptional": 0, "minion": 0, "item": 0},
            3: {"junk": 1, "common": 2, "rare": 1, "exceptional": 0, "minion": 0, "item": 0},
            4: {"junk": 2, "common": 2, "rare": 1, "exceptional": 1, "minion": 1, "item": 1},
            5: {"junk": 2, "common": 3, "rare": 1, "exceptional": 1, "minion": 1, "item": 1},
            6: {"junk": 3, "common": 3, "rare": 2, "exceptional": 1, "minion": 1, "item": 2},
            7: {"junk": 3, "common": 3, "rare": 2, "exceptional": 1, "minion": 1, "item": 2},
        },
    }

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="商店编辑参考", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 14, "bold")).pack(anchor=tk.W, padx=10, pady=10)

        notebook = ttk.Notebook(self, style="Dev.TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Settings tab
        settings_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(settings_frame, text="商店设置")
        self._build_settings_tab(settings_frame)

        # Item types tab
        item_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(item_frame, text="物品类型")
        self._build_item_tab(item_frame)

    def _build_settings_tab(self, parent):
        tk.Label(parent, text="shop_item_number (基础库存骰子)", bg="#16213e", fg="#FFD700",
                 font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=5)
        for shop_type, vals in self.SHOP_SETTINGS["shop_item_number"].items():
            tk.Label(parent, text=f"  {shop_type}: {vals}", bg="#16213e", fg="#FFFFFF",
                     font=("Microsoft YaHei", 10)).pack(anchor=tk.W, padx=5)

        tk.Label(parent, text="shop_chapter_modifiers (章节修正)", bg="#16213e", fg="#FFD700",
                 font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=(15, 5))
        tree = ttk.Treeview(parent, columns=self.QUALITIES, show="headings", style="Dev.Treeview")
        tree.heading("#0", text="章节")
        for q in self.QUALITIES:
            tree.heading(q, text=q)
            tree.column(q, width=60)
        tree.pack(fill=tk.X, padx=5, pady=5)
        for ch, mods in self.SHOP_SETTINGS["shop_chapter_modifiers"].items():
            tree.insert("", tk.END, text=str(ch), values=tuple(mods.get(q, 0) for q in self.QUALITIES))

    def _build_item_tab(self, parent):
        tk.Label(parent, text="物品类型列表", bg="#16213e", fg="#FFD700",
                 font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=5)
        for it in self.ITEM_TYPES:
            tk.Label(parent, text=f"  • {it}", bg="#16213e", fg="#FFFFFF",
                     font=("Microsoft YaHei", 10)).pack(anchor=tk.W, padx=5)

        tk.Button(parent, text="生成 Item 代码片段", command=self._gen_item_snippet,
                  bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(anchor=tk.W, padx=5, pady=15)

    def _gen_item_snippet(self):
        snippet = '''# 添加新物品
new_item = Item(
    name="Magic Sword",
    target="MC",
    type=IT_Weapon,
    pic="magic_sword.png",
    rank=3,
    max_rank=6,
    rarity=3,
    price=500,
    effects=[Effect("boost", "defense", 3)],
    description="一把魔法剑。",
    template=True
)
item_dict["Magic Sword"] = new_item
'''
        win = tk.Toplevel(self)
        win.title("代码片段")
        win.geometry("600x300")
        txt = tk.Text(win, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Consolas", 10))
        txt.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        txt.insert(tk.END, snippet)
