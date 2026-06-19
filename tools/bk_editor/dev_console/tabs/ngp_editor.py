# -*- coding: utf-8 -*-
"""
BK Dev Console — NG+ Editor Tab
EN: CRUD editor for ngp_settings.json.
ZH: ngp_settings.json 的增删改查编辑器。
"""

import tkinter as tk
from tkinter import ttk

from bk_editor.dev_console.tabs.base import BaseJsonEditorTab
from bk_editor.shared import JsonTreeview, LabeledEntry, LabeledCombobox, LabeledSpinbox


class NGPEditorTab(BaseJsonEditorTab):
    JSON_PATH = "ngp/ngp_settings.json"

    NGP_TYPES = ["gold", "resources", "int", "bool", "plus", "boost", "dispenser", "item", "pref", "girl rank"]
    CATEGORIES = ["resources", "girls", "MC", "misc"]

    def __init__(self, parent, app):
        self.selected_idx = None
        super().__init__(parent, app)

    def _build_ui(self):
        super()._build_ui()

        self.tree = JsonTreeview(
            self.tree_frame,
            columns=["name", "type", "label", "category"],
        )
        self.tree.column("name", width=180)
        self.tree.column("type", width=80)
        self.tree.column("label", width=150)
        self.tree.column("category", width=80)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        self._build_details()

    def _build_details(self):
        canvas = tk.Canvas(self.details_frame, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.details_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.form_frame = tk.Frame(canvas, bg="#1a1a2e")
        self.form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.form_frame, anchor=tk.NW, width=480)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.f_name = LabeledEntry(self.form_frame, "name:", width=40)
        self.f_name.pack(fill=tk.X, pady=3, padx=5)

        self.f_type = LabeledCombobox(self.form_frame, "type:", self.NGP_TYPES)
        self.f_type.pack(fill=tk.X, pady=3, padx=5)

        self.f_label = LabeledEntry(self.form_frame, "label:", width=40)
        self.f_label.pack(fill=tk.X, pady=3, padx=5)

        self.f_category = LabeledCombobox(self.form_frame, "category:", self.CATEGORIES)
        self.f_category.pack(fill=tk.X, pady=3, padx=5)

        self.f_values = LabeledEntry(self.form_frame, "values (JSON list):", width=40)
        self.f_values.pack(fill=tk.X, pady=3, padx=5)

        self.f_cost = LabeledEntry(self.form_frame, "cost (JSON list or int):", width=40)
        self.f_cost.pack(fill=tk.X, pady=3, padx=5)

        self.f_ttip = LabeledEntry(self.form_frame, "ttip:", width=40)
        self.f_ttip.pack(fill=tk.X, pady=3, padx=5)

        btn = tk.Button(
            self.form_frame,
            text="应用更改",
            command=self._apply,
            bg="#0f3460",
            fg="#FFFFFF",
            font=("Microsoft YaHei", 11),
            relief=tk.FLAT,
        )
        btn.pack(fill=tk.X, pady=10, padx=5)

    def _default_data(self):
        return []

    def _refresh_tree(self):
        column_map = {"name": "name", "type": "type", "label": "label", "category": "category"}
        self.tree.populate(self.data, column_map)

    def _on_search(self, *args):
        term = self.search_var.get().lower()
        filtered = [it for it in self.data if term in it.get("name", "").lower() or term in it.get("label", "").lower()]
        column_map = {"name": "name", "type": "type", "label": "label", "category": "category"}
        self.tree.populate(filtered, column_map)

    def _on_select(self, event=None):
        sel = self.tree.get_selected_item()
        if not sel:
            return
        self._apply(silent=True)
        self.selected_idx = self.data.index(sel)
        self._load_form(sel)

    def _load_form(self, item):
        self.f_name.set(item.get("name", ""))
        self.f_type.set(item.get("type", ""))
        self.f_label.set(item.get("label", ""))
        self.f_category.set(item.get("category", "misc"))
        self.f_values.set(self._list_to_str(item.get("values")))
        self.f_cost.set(self._list_to_str(item.get("cost")))
        self.f_ttip.set(item.get("ttip", ""))

    def _apply(self, silent=False):
        if self.selected_idx is None or self.selected_idx >= len(self.data):
            if not silent:
                self.app.set_status("未选择 NG+ 设置")
            return
        try:
            item = self.data[self.selected_idx]
            item["name"] = self.f_name.get()
            item["type"] = self.f_type.get()
            item["label"] = self.f_label.get()
            item["category"] = self.f_category.get()
            item["values"] = self._str_to_list(self.f_values.get())
            item["cost"] = self._str_to_list(self.f_cost.get()) or 0
            item["ttip"] = self.f_ttip.get()
            self._refresh_tree()
            if not silent:
                self.app.set_status(f"已更新: {item['name']}")
        except Exception as e:
            if not silent:
                self.app.set_status(f"应用失败: {e}")

    def on_add(self):
        new_name = "new_setting"
        counter = 1
        existing = [it.get("name") for it in self.data]
        while f"{new_name}_{counter}" in existing:
            counter += 1
        new_item = {
            "name": f"{new_name}_{counter}",
            "type": "bool",
            "label": "New Setting",
            "category": "misc",
            "cost": 0,
            "ttip": "",
        }
        self.data.append(new_item)
        self.selected_idx = len(self.data) - 1
        self._refresh_tree()
        self._load_form(new_item)
        self.app.set_status(f"添加 NG+ 设置: {new_item['name']}")

    def on_delete(self):
        sel = self.tree.get_selected_item()
        if not sel:
            return
        if self.confirm_delete(sel.get("name", "")):
            self.data.remove(sel)
            self.selected_idx = None
            self._refresh_tree()
            self.app.set_status("已删除 NG+ 设置")

    @staticmethod
    def _list_to_str(value):
        if value is None:
            return ""
        if isinstance(value, list):
            return ", ".join(str(v) for v in value)
        return str(value)

    @staticmethod
    def _str_to_list(value):
        if not value or not value.strip():
            return None
        if "," not in value:
            try:
                return int(value.strip())
            except ValueError:
                try:
                    return float(value.strip())
                except ValueError:
                    return value.strip()
        result = []
        for part in value.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                result.append(int(part))
            except ValueError:
                try:
                    result.append(float(part))
                except ValueError:
                    result.append(part)
        return result
