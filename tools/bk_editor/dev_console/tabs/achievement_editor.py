# -*- coding: utf-8 -*-
"""
BK Dev Console — Achievement Editor Tab
EN: CRUD editor for achievements.json.
ZH: achievements.json 的增删改查编辑器。
"""

import tkinter as tk
from tkinter import ttk

from bk_editor.dev_console.tabs.base import BaseJsonEditorTab
from bk_editor.shared import JsonTreeview, LabeledEntry, LabeledSpinbox, LabeledCheckbox


class AchievementEditorTab(BaseJsonEditorTab):
    JSON_PATH = "achievements/achievements.json"

    def __init__(self, parent, app):
        self.items = []
        self.selected_idx = None
        super().__init__(parent, app)

    def _build_ui(self):
        super()._build_ui()

        # EN: Tree columns.
        # ZH: 树列。
        self.tree = JsonTreeview(
            self.tree_frame,
            columns=["target", "title", "level_nb", "multi"],
        )
        self.tree.column("target", width=180)
        self.tree.column("title", width=280)
        self.tree.column("level_nb", width=60)
        self.tree.column("multi", width=60)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # EN: Details form.
        # ZH: 详情表单。
        self._build_details()

    def _build_details(self):
        canvas = tk.Canvas(self.details_frame, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.details_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.form_frame = tk.Frame(canvas, bg="#1a1a2e")

        self.form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self.form_frame, anchor=tk.NW, width=480)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # EN: Form fields.
        # ZH: 表单字段。
        self.f_target = LabeledEntry(self.form_frame, "target:", width=40)
        self.f_target.pack(fill=tk.X, pady=3, padx=5)

        self.f_title = LabeledEntry(self.form_frame, "title:", width=40)
        self.f_title.pack(fill=tk.X, pady=3, padx=5)

        self.f_description = LabeledEntry(self.form_frame, "description:", width=40)
        self.f_description.pack(fill=tk.X, pady=3, padx=5)

        self.f_pic = LabeledEntry(self.form_frame, "pic:", width=40)
        self.f_pic.pack(fill=tk.X, pady=3, padx=5)

        self.f_pic_path = LabeledEntry(self.form_frame, "pic_path:", width=40)
        self.f_pic_path.pack(fill=tk.X, pady=3, padx=5)

        self.f_level_nb = LabeledSpinbox(self.form_frame, "level_nb:", default=1, from_=1, to=20)
        self.f_level_nb.pack(fill=tk.X, pady=3, padx=5)

        self.f_multi = LabeledSpinbox(self.form_frame, "multi:", default=1, from_=1, to=1000)
        self.f_multi.pack(fill=tk.X, pady=3, padx=5)

        self.f_requirements = LabeledEntry(self.form_frame, "requirements (JSON):", width=40)
        self.f_requirements.pack(fill=tk.X, pady=3, padx=5)

        self.f_requirements2 = LabeledEntry(self.form_frame, "requirements2 (JSON):", width=40)
        self.f_requirements2.pack(fill=tk.X, pady=3, padx=5)

        self.f_custom_titles = LabeledEntry(self.form_frame, "custom_titles (JSON):", width=40)
        self.f_custom_titles.pack(fill=tk.X, pady=3, padx=5)

        # EN: Apply button.
        # ZH: 应用按钮。
        btn = tk.Button(
            self.form_frame,
            text="应用更改",
            command=self._apply_changes,
            bg="#0f3460",
            fg="#FFFFFF",
            font=("Microsoft YaHei", 11),
            relief=tk.FLAT,
        )
        btn.pack(fill=tk.X, pady=10, padx=5)

    def _default_data(self):
        return {}

    def _parse_data(self):
        self.items = []
        if isinstance(self.data, dict):
            for target, item in self.data.items():
                row = dict(item)
                row["target"] = target
                self.items.append(row)
        self.items.sort(key=lambda x: x.get("target", ""))

    def _prepare_data(self):
        self._apply_changes(silent=True)
        new_data = {}
        for item in self.items:
            target = item.get("target", "")
            if target:
                new_data[target] = {k: v for k, v in item.items() if k != "target"}
        self.data = new_data

    def _refresh_tree(self):
        column_map = {"target": "target", "title": "title", "level_nb": "level_nb", "multi": "multi"}
        self.tree.populate(self.items, column_map)

    def _on_search(self, *args):
        term = self.search_var.get().lower()
        filtered = [it for it in self.items if term in it.get("target", "").lower() or term in it.get("title", "").lower()]
        column_map = {"target": "target", "title": "title", "level_nb": "level_nb", "multi": "multi"}
        self.tree.populate(filtered, column_map)

    def _on_tree_select(self, event=None):
        sel = self.tree.get_selected_item()
        if not sel:
            return
        self._apply_changes(silent=True)
        self.selected_idx = self.items.index(sel)
        self._load_form(sel)

    def _load_form(self, item):
        self.f_target.set(item.get("target", ""))
        self.f_title.set(item.get("title", ""))
        self.f_description.set(item.get("description", ""))
        self.f_pic.set(item.get("pic", ""))
        self.f_pic_path.set(item.get("pic_path", ""))
        self.f_level_nb.set(item.get("level_nb", 1))
        self.f_multi.set(item.get("multi", 1))
        self.f_requirements.set(self._dict_to_str(item.get("requirements")))
        self.f_requirements2.set(self._dict_to_str(item.get("requirements2")))
        self.f_custom_titles.set(self._dict_to_str(item.get("custom_titles")))

    def _apply_changes(self, silent=False):
        if self.selected_idx is None or self.selected_idx >= len(self.items):
            if not silent:
                self.app.set_status("未选择成就")
            return
        try:
            item = self.items[self.selected_idx]
            item["target"] = self.f_target.get()
            item["title"] = self.f_title.get()
            item["description"] = self.f_description.get()
            item["pic"] = self.f_pic.get()
            item["pic_path"] = self.f_pic_path.get()
            item["level_nb"] = int(self.f_level_nb.get())
            item["multi"] = int(self.f_multi.get())
            item["requirements"] = self._str_to_dict(self.f_requirements.get())
            item["requirements2"] = self._str_to_dict(self.f_requirements2.get())
            item["custom_titles"] = self._str_to_dict(self.f_custom_titles.get())
            self._refresh_tree()
            if not silent:
                self.app.set_status(f"已更新: {item['target']}")
        except Exception as e:
            if not silent:
                self.app.set_status(f"应用失败: {e}")

    def on_add(self):
        new_target = "new_achievement"
        counter = 1
        while f"{new_target}_{counter}" in [it.get("target") for it in self.items]:
            counter += 1
        new_item = {
            "target": f"{new_target}_{counter}",
            "title": "New Achievement",
            "description": "No description",
            "pic": "misc.webp",
            "pic_path": "resources/ui/achievements/",
            "level_nb": 1,
            "multi": 1,
        }
        self.items.append(new_item)
        self.selected_idx = len(self.items) - 1
        self._refresh_tree()
        self._load_form(new_item)
        self.app.set_status(f"添加成就: {new_item['target']}")

    def on_delete(self):
        sel = self.tree.get_selected_item()
        if not sel:
            return
        if self.confirm_delete(sel.get("target", "")):
            self.items.remove(sel)
            self.selected_idx = None
            self._refresh_tree()
            self.app.set_status("已删除成就")

    @staticmethod
    def _dict_to_str(value):
        if value is None:
            return ""
        if isinstance(value, dict):
            parts = []
            for k, v in value.items():
                parts.append(f"{k}:{v}")
            return ", ".join(parts)
        return str(value)

    @staticmethod
    def _str_to_str(value):
        if not value or not value.strip():
            return None
        result = {}
        for part in value.split(","):
            part = part.strip()
            if not part:
                continue
            if ":" not in part:
                continue
            k, v = part.split(":", 1)
            k = k.strip()
            v = v.strip()
            # EN: Try numeric conversion for both key and value.
            # ZH: 尝试将键和值转换为数字。
            try:
                k = int(k)
            except ValueError:
                pass
            try:
                v = int(v)
            except ValueError:
                try:
                    v = float(v)
                except ValueError:
                    pass
            result[k] = v
        return result if result else None

    # Alias for typo compatibility
    _str_to_dict = _str_to_str
