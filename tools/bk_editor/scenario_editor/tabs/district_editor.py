# -*- coding: utf-8 -*-
"""
BK Scenario Editor — District / Location Reference Tab
EN: Read-only reference for districts and locations + code snippet generator.
ZH: District/Location 只读参考 + 代码片段生成器。
"""

import tkinter as tk
from tkinter import ttk


class DistrictEditorTab(tk.Frame):
    """EN: Reference viewer for districts/locations + snippet generator.
       ZH: District/Location 参考查看器 + 代码生成器。"""

    DISTRICTS = [
        {"key": "slum", "name": "The Slums", "chapter": 1, "rank": 1, "diff": 15, "room": "", "description": "贫民窟"},
        {"key": "docks", "name": "The Docks", "chapter": 2, "rank": 2, "diff": 40, "room": "tavern", "description": "码头区"},
        {"key": "warehouse", "name": "The Warehouse", "chapter": 2, "rank": 2, "diff": 40, "room": "strip club", "description": "仓库区"},
        {"key": "gardens", "name": "The Magic Gardens", "chapter": 4, "rank": 3, "diff": 100, "room": "onsen", "description": "魔法花园"},
        {"key": "cathedra", "name": "The Cathedra", "chapter": 4, "rank": 3, "diff": 100, "room": "okiya", "description": "大教堂区"},
        {"key": "hold", "name": "The King's Hold", "chapter": 6, "rank": 4, "diff": 150, "room": "free", "description": "王宫区"},
    ]

    LOCATIONS = {
        "The Slums": ["Spice market", "Sewers", "Farm", "Watchtower", "Junkyard", "Thieves guild"],
        "The Docks": ["Harbor", "Shipyard", "Seafront", "Beach", "Taverns", "Exotic emporium"],
        "The Warehouse": ["Market", "Stables", "Plaza", "Gallows", "Prison", "Arena"],
        "The Magic Gardens": ["Botanical garden", "Magic university", "Magic forest", "Hanging gardens", "Guild quarter", "Magic guild"],
        "The Cathedra": ["Pilgrim road", "Banking quarter", "Old ruins", "Lake", "Training ground", "Cathedra"],
        "The King's Hold": ["Battlements", "Keep", "Hall", "Courtyard", "Temple", "Falls"],
    }

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="District / Location 参考", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 14, "bold")).pack(anchor=tk.W, padx=10, pady=10)

        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1a1a2e", sashwidth=6)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        left = tk.Frame(paned, bg="#16213e", width=350)
        left.pack_propagate(False)
        paned.add(left, minsize=300)

        tk.Label(left, text="现有区域 (Districts)", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=5)
        self.dist_tree = ttk.Treeview(left, columns=["chapter", "rank", "diff"], show="headings", style="Dev.Treeview")
        self.dist_tree.heading("#0", text="District")
        self.dist_tree.heading("chapter", text="章节")
        self.dist_tree.heading("rank", text="等级")
        self.dist_tree.heading("diff", text="难度")
        for col in ["#0", "chapter", "rank", "diff"]:
            self.dist_tree.column(col, width=80)
        self.dist_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.dist_tree.bind("<<TreeviewSelect>>", self._on_dist_select)

        right = tk.Frame(paned, bg="#16213e", width=500)
        right.pack_propagate(False)
        paned.add(right, minsize=400)

        tk.Label(right, text="地点 (Locations)", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=5)
        self.loc_tree = ttk.Treeview(right, columns=["district"], show="headings", style="Dev.Treeview")
        self.loc_tree.heading("#0", text="Location")
        self.loc_tree.heading("district", text="所属区域")
        self.loc_tree.column("#0", width=200)
        self.loc_tree.column("district", width=150)
        self.loc_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Snippet generator
        snippet_frame = tk.Frame(self, bg="#16213e")
        snippet_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(snippet_frame, text="代码片段生成器", bg="#16213e", fg="#FFD700", font=("Microsoft YaHei", 12, "bold")).pack(anchor=tk.W, padx=5, pady=5)

        btn_frame = tk.Frame(snippet_frame, bg="#16213e")
        btn_frame.pack(fill=tk.X, padx=5)
        tk.Button(btn_frame, text="生成 District 代码", command=self._gen_dist_snippet, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="生成 Location 代码", command=self._gen_loc_snippet, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

        self.snippet_text = tk.Text(snippet_frame, height=8, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Consolas", 10))
        self.snippet_text.pack(fill=tk.X, padx=5, pady=5)

        self._populate_reference()

    def _populate_reference(self):
        for d in self.DISTRICTS:
            self.dist_tree.insert("", tk.END, text=d["name"], values=(d["chapter"], d["rank"], d["diff"]))
        for dist_name, locs in self.LOCATIONS.items():
            for loc in locs:
                self.loc_tree.insert("", tk.END, text=loc, values=(dist_name,))

    def _on_dist_select(self, event=None):
        sel = self.dist_tree.selection()
        if not sel:
            return
        dist_name = self.dist_tree.item(sel[0], "text")
        # Filter locations
        for row in self.loc_tree.get_children():
            self.loc_tree.delete(row)
        for dname, locs in self.LOCATIONS.items():
            if dname == dist_name:
                for loc in locs:
                    self.loc_tree.insert("", tk.END, text=loc, values=(dname,))

    def _gen_dist_snippet(self):
        snippet = '''# 添加新 District
new_district = District(
    name="The New District",
    chapter=1,
    rank=1,
    diff=20,
    pop=((beggar, 50), (thug, 50)),
    room=["tavern"],
    pic="resources/districts/new_district.webp",
    description=__("新区域描述")
)
district_dict["new_district"] = new_district
'''
        self.snippet_text.delete("1.0", tk.END)
        self.snippet_text.insert(tk.END, snippet)

    def _gen_loc_snippet(self):
        snippet = '''# 添加新 Location
new_location = Location(
    name="New Location",
    pic="New Location.webp",
    has_girls=True,
    secret=False,
    action=False,
    menu=("Visit", "visit_new_location"),
    menu_costs_AP=True
)
location_dict["The Slums"].append(new_location)
location_dict["New Location"] = new_location
'''
        self.snippet_text.delete("1.0", tk.END)
        self.snippet_text.insert(tk.END, snippet)
