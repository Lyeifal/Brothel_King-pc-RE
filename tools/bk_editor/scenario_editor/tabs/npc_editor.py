# -*- coding: utf-8 -*-
"""
BK Scenario Editor — NPC Reference Tab
EN: Reference for shop NPCs and special girls + snippet generator.
ZH: 商店 NPC 与特殊女孩参考 + 代码片段生成器。
"""

import tkinter as tk
from tkinter import ttk


class NPCEditorTab(tk.Frame):
    """EN: NPC reference viewer + code snippet generator.
       ZH: NPC 参考查看器 + 代码生成器。"""

    SHOP_NPCS = [
        {"name": "Riche", "item_types": "Flower", "bg": "bg botanical_garden", "portrait": "side riche"},
        {"name": "Ramias", "item_types": "Weapon", "bg": "bg arena_front", "portrait": "side ramias"},
        {"name": "Gurigura", "item_types": "Toy, Food, Supplies", "bg": "bg prison", "portrait": "side gurigura"},
        {"name": "Katryn", "item_types": "Ring, Necklace", "bg": "bg magic_university", "portrait": "side katryn"},
        {"name": "Gift Shop Girl", "item_types": "Gift, Misc", "bg": "bg exotic_emporium", "portrait": "side giftgirl"},
        {"name": "Today", "item_types": "Dress, Accessory", "bg": "bg pilgrim_road", "portrait": "side today"},
        {"name": "Stella (minion)", "item_types": "stallion", "bg": "bg harbor", "portrait": "side stella"},
        {"name": "Goldie (minion)", "item_types": "beast", "bg": "bg farmland", "portrait": "side goldie"},
        {"name": "Willow (minion)", "item_types": "monster", "bg": "bg sewers", "portrait": "side willow"},
        {"name": "Gina (minion)", "item_types": "machine", "bg": "bg junkyard", "portrait": "side gina"},
    ]

    SPECIAL_GIRLS = [
        {"npc_id": "lost_noble", "name": "艾拉腊女士", "min_chapter": 1, "quest_label_prefix": "quest_elara"},
        {"npc_id": "cursed_dancer", "name": "未来", "min_chapter": 2, "quest_label_prefix": "quest_mirai"},
        {"npc_id": "ex_knight", "name": "伊尔莎军士", "min_chapter": 2, "quest_label_prefix": "quest_yrsa"},
    ]

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="NPC 参考", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 14, "bold")).pack(anchor=tk.W, padx=10, pady=10)

        notebook = ttk.Notebook(self, style="Dev.TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Shop NPC tab
        shop_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(shop_frame, text="商店 NPC")
        self._build_shop_tab(shop_frame)

        # Special girl tab
        sg_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(sg_frame, text="特殊女孩 NPC")
        self._build_special_girl_tab(sg_frame)

    def _build_shop_tab(self, parent):
        tree = ttk.Treeview(parent, columns=["item_types", "bg", "portrait"], show="headings", style="Dev.Treeview")
        tree.heading("#0", text="NPC 名称")
        tree.heading("item_types", text="售卖类型")
        tree.heading("bg", text="背景")
        tree.heading("portrait", text="肖像标签")
        tree.column("#0", width=150)
        tree.column("item_types", width=180)
        tree.column("bg", width=200)
        tree.column("portrait", width=120)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        for npc in self.SHOP_NPCS:
            tree.insert("", tk.END, text=npc["name"], values=(npc["item_types"], npc["bg"], npc["portrait"]))

        tk.Button(parent, text="生成商店 NPC 代码", command=self._gen_shop_snippet,
                  bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(anchor=tk.W, padx=5, pady=5)

    def _build_special_girl_tab(self, parent):
        tree = ttk.Treeview(parent, columns=["name", "min_chapter", "quest"], show="headings", style="Dev.Treeview")
        tree.heading("#0", text="npc_id")
        tree.heading("name", text="名称")
        tree.heading("min_chapter", text="最低章节")
        tree.heading("quest", text="任务前缀")
        for col in ["#0", "name", "min_chapter", "quest"]:
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        for sg in self.SPECIAL_GIRLS:
            tree.insert("", tk.END, text=sg["npc_id"], values=(sg["name"], sg["min_chapter"], sg["quest_label_prefix"]))

        tk.Button(parent, text="生成特殊女孩代码", command=self._gen_sg_snippet,
                  bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(anchor=tk.W, padx=5, pady=5)

    def _gen_shop_snippet(self):
        snippet = '''# 添加商店 NPC
NPC_new = NPC(
    name="New Merchant",
    char=new_char,
    portrait="side new_merchant",
    bg='bg new_location',
    item_types=["Weapon", "Ring"]
)
# 如果是 minion 商人:
# NPC_new = NPC(name="New Minion", char=new_char, portrait="side new", bg='bg location', minion_type="beast")
'''
        self._show_snippet(snippet)

    def _gen_sg_snippet(self):
        snippet = '''# 注册特殊女孩 NPC
special_girl_registry.register(SpecialGirlNPC(
    npc_id="my_girl",
    name="My Girl",
    description="一位神秘的女孩...",
    portrait_tag="my_girl_portrait",
    quest_label_prefix="quest_my_girl",
    min_chapter=1
))
'''
        self._show_snippet(snippet)

    def _show_snippet(self, text):
        win = tk.Toplevel(self)
        win.title("代码片段")
        win.geometry("600x300")
        txt = tk.Text(win, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Consolas", 10))
        txt.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        txt.insert(tk.END, text)
