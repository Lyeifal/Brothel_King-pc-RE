# -*- coding: utf-8 -*-
"""
BK Editor — Origin Editor
EN: Visual editor for Sandbox mode player origins.
ZH: 沙盒模式玩家出身的可视化编辑器。
"""

import tkinter as tk
from tkinter import ttk, messagebox
from bk_editor.core import load_json, save_json, DATA_DIR, validate_origin, GAME_MODES
from bk_editor.widgets import LabeledEntry, LabeledSpinbox, LabeledCombobox, LabeledCheckbox, JsonTreeview, EffectEditor


class OriginEditorFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.json_path = DATA_DIR / "sandbox" / "origins.json"
        self.items = []
        self.current_index = -1

        tk.Label(self, text="出身编辑器", font=("Microsoft YaHei", 16, "bold"), bg="#1a1a2e", fg="#FFD700").pack(pady=5)

        toolbar = tk.Frame(self, bg="#1a1a2e")
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(toolbar, text="+ 新建", command=self.new_item, bg="#2ECC71", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="保存", command=self.save, bg="#3498DB", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="删除", command=self.delete_item, bg="#E74C3C", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)

        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1a1a2e")
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        left = tk.Frame(paned, bg="#1a1a2e")
        self.tree = JsonTreeview(left, columns=["ID", "名称"])
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        paned.add(left, minsize=250)

        right = tk.Frame(paned, bg="#16213e")
        self._build_form(right)
        paned.add(right, minsize=500)

        self.load()

    def _build_form(self, parent):
        self.form = tk.Frame(parent, bg="#16213e")
        self.form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.f_id = LabeledEntry(self.form, "出身ID:", width=30)
        self.f_id.pack(fill=tk.X, pady=3)

        self.f_name = LabeledEntry(self.form, "名称:", width=30)
        self.f_name.pack(fill=tk.X, pady=3)

        self.f_desc = LabeledEntry(self.form, "描述:", width=40)
        self.f_desc.pack(fill=tk.X, pady=3)

        self.f_icon = LabeledEntry(self.form, "图标标签:", width=25)
        self.f_icon.pack(fill=tk.X, pady=3)

        tk.Label(self.form, text="起始奖励:", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 10)).pack(anchor=tk.W, pady=(10, 2))
        self.bonus_frame = tk.Frame(self.form, bg="#16213e")
        self.bonus_frame.pack(fill=tk.X)
        self.f_bonus_gold = LabeledSpinbox(self.bonus_frame, "金币:", from_=-9999, to=9999, default=0)
        self.f_bonus_gold.pack(fill=tk.X, pady=2)
        self.f_bonus_rep = LabeledSpinbox(self.bonus_frame, "声望:", from_=-9999, to=9999, default=0)
        self.f_bonus_rep.pack(fill=tk.X, pady=2)

        tk.Label(self.form, text="适用模式:", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 10)).pack(anchor=tk.W, pady=(10, 2))
        self.mode_vars = {}
        modes_frame = tk.Frame(self.form, bg="#16213e")
        modes_frame.pack(fill=tk.X)
        for mode in GAME_MODES:
            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(modes_frame, text=mode, variable=var, bg="#16213e", fg="#FFFFFF", selectcolor="#333333")
            chk.pack(side=tk.LEFT, padx=5)
            self.mode_vars[mode] = var

        tk.Button(self.form, text="应用修改", command=self.apply, bg="#9B59B6", fg="#FFFFFF").pack(pady=15)

    def load(self):
        self.items = load_json(self.json_path)
        self.refresh_list()

    def save(self):
        save_json(self.json_path, self.items)
        self.app.set_status(f"已保存 {len(self.items)} 个出身到 {self.json_path}")

    def refresh_list(self):
        self.tree.populate(self.items, {"ID": "origin_id", "名称": "name"})

    def on_select(self, event=None):
        item = self.tree.get_selected_item()
        if item is None:
            return
        self.current_index = self.items.index(item)
        self.f_id.set(item.get("origin_id", ""))
        self.f_name.set(item.get("name", ""))
        self.f_desc.set(item.get("description", ""))
        self.f_icon.set(item.get("icon_tag", ""))
        bonus = item.get("starting_bonus", {})
        self.f_bonus_gold.set(bonus.get("gold", 0))
        self.f_bonus_rep.set(bonus.get("reputation", 0))
        for mode, var in self.mode_vars.items():
            var.set(mode in item.get("modes", []))

    def new_item(self):
        new_item = {
            "origin_id": "new_origin",
            "name": "新出身",
            "description": "",
            "icon_tag": "origin_default",
            "talents": [],
            "starting_bonus": {},
            "modes": ["sandbox"],
        }
        self.items.append(new_item)
        self.refresh_list()

    def delete_item(self):
        if self.current_index < 0 or self.current_index >= len(self.items):
            return
        self.items.pop(self.current_index)
        self.current_index = -1
        self.refresh_list()

    def apply(self):
        if self.current_index < 0 or self.current_index >= len(self.items):
            messagebox.showwarning("提示", "请先选择一个出身")
            return
        item = self.items[self.current_index]
        item["origin_id"] = self.f_id.get()
        item["name"] = self.f_name.get()
        item["description"] = self.f_desc.get()
        item["icon_tag"] = self.f_icon.get()
        item["starting_bonus"] = {}
        g = self.f_bonus_gold.get()
        if g:
            item["starting_bonus"]["gold"] = g
        r = self.f_bonus_rep.get()
        if r:
            item["starting_bonus"]["reputation"] = r
        item["modes"] = [m for m, var in self.mode_vars.items() if var.get()]
        errors = validate_origin(item)
        if errors:
            messagebox.showerror("验证错误", "\n".join(errors))
            return
        self.refresh_list()
        self.app.set_status(f"已更新出身: {item['name']}")
