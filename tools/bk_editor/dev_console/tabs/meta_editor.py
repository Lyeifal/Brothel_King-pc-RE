# -*- coding: utf-8 -*-
"""
BK Dev Console — Meta Progression Editor Tab
EN: CRUD editor for meta_progression.json.
ZH: meta_progression.json 的增删改查编辑器。
"""

import tkinter as tk
from tkinter import ttk

from bk_editor.dev_console.tabs.base import BaseJsonEditorTab
from bk_editor.shared import JsonTreeview, LabeledEntry, LabeledSpinbox, EffectEditor


class MetaEditorTab(BaseJsonEditorTab):
    JSON_PATH = "meta/meta_progression.json"

    def __init__(self, parent, app):
        self.upgrades = []
        self.selected_idx = None
        self.effect_editors = []
        super().__init__(parent, app)

    def _build_ui(self):
        super()._build_ui()

        self.tree = JsonTreeview(
            self.tree_frame,
            columns=["id", "name", "max_rank", "unlock"],
        )
        self.tree.column("id", width=150)
        self.tree.column("name", width=200)
        self.tree.column("max_rank", width=60)
        self.tree.column("unlock", width=100)
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

        self.f_id = LabeledEntry(self.form_frame, "upgrade_id / id:", width=40)
        self.f_id.pack(fill=tk.X, pady=3, padx=5)

        self.f_name = LabeledEntry(self.form_frame, "name_i18n_key:", width=40)
        self.f_name.pack(fill=tk.X, pady=3, padx=5)

        self.f_desc = LabeledEntry(self.form_frame, "description_i18n_key:", width=40)
        self.f_desc.pack(fill=tk.X, pady=3, padx=5)

        self.f_max_rank = LabeledSpinbox(self.form_frame, "max_rank:", default=1, from_=1, to=50)
        self.f_max_rank.pack(fill=tk.X, pady=3, padx=5)

        self.f_cost = LabeledEntry(self.form_frame, "cost_per_rank (JSON list):", width=40)
        self.f_cost.pack(fill=tk.X, pady=3, padx=5)

        self.f_unlock = LabeledEntry(self.form_frame, "unlock_condition:", width=40)
        self.f_unlock.pack(fill=tk.X, pady=3, padx=5)

        # EN: Effects section.
        # ZH: Effects 区域。
        eff_label = tk.Label(self.form_frame, text="Effects:", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 11))
        eff_label.pack(anchor=tk.W, padx=5, pady=(10, 5))

        self.effects_frame = tk.Frame(self.form_frame, bg="#1a1a2e")
        self.effects_frame.pack(fill=tk.X, padx=5, pady=5)

        eff_btn_frame = tk.Frame(self.form_frame, bg="#1a1a2e")
        eff_btn_frame.pack(fill=tk.X, padx=5)
        tk.Button(eff_btn_frame, text="+ 添加 Effect", command=self._add_effect_editor, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(eff_btn_frame, text="- 移除最后一个", command=self._remove_last_effect, bg="#660000", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

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
        return {"meta_upgrades": []}

    def _parse_data(self):
        if not isinstance(self.data, dict):
            self.data = self._default_data()
        self.upgrades = list(self.data.get("meta_upgrades", []))

    def _prepare_data(self):
        self._apply(silent=True)
        self.data["meta_upgrades"] = self.upgrades

    def _refresh_tree(self):
        column_map = {"id": "upgrade_id", "name": "name_i18n_key", "max_rank": "max_rank", "unlock": "unlock_condition"}
        self.tree.populate(self.upgrades, column_map)

    def _on_search(self, *args):
        term = self.search_var.get().lower()
        filtered = [u for u in self.upgrades if term in u.get("upgrade_id", "").lower() or term in u.get("name_i18n_key", "").lower()]
        column_map = {"id": "upgrade_id", "name": "name_i18n_key", "max_rank": "max_rank", "unlock": "unlock_condition"}
        self.tree.populate(filtered, column_map)

    def _on_select(self, event=None):
        sel = self.tree.get_selected_item()
        if not sel:
            return
        self._apply(silent=True)
        self.selected_idx = self.upgrades.index(sel)
        self._load_form(sel)

    def _load_form(self, item):
        self.f_id.set(item.get("upgrade_id") or item.get("id", ""))
        self.f_name.set(item.get("name_i18n_key", ""))
        self.f_desc.set(item.get("description_i18n_key", ""))
        self.f_max_rank.set(item.get("max_rank", 1))
        self.f_cost.set(self._list_to_str(item.get("cost_per_rank", [])))
        self.f_unlock.set(item.get("unlock_condition", "newgame+"))

        # EN: Clear and rebuild effect editors.
        # ZH: 清空并重建 effect 编辑器。
        for child in self.effects_frame.winfo_children():
            child.destroy()
        self.effect_editors = []
        for eff in item.get("effects", []):
            self._add_effect_editor(eff)

    def _add_effect_editor(self, effect=None):
        editor = EffectEditor(self.effects_frame, effect=effect)
        editor.pack(fill=tk.X, pady=3)
        self.effect_editors.append(editor)

    def _remove_last_effect(self):
        if self.effect_editors:
            editor = self.effect_editors.pop()
            editor.destroy()

    def _apply(self, silent=False):
        if self.selected_idx is None or self.selected_idx >= len(self.upgrades):
            if not silent:
                self.app.set_status("未选择局外养成词条")
            return
        try:
            item = self.upgrades[self.selected_idx]
            item["upgrade_id"] = self.f_id.get()
            item["name_i18n_key"] = self.f_name.get()
            item["description_i18n_key"] = self.f_desc.get()
            item["max_rank"] = int(self.f_max_rank.get())
            item["cost_per_rank"] = self._str_to_list(self.f_cost.get()) or []
            item["unlock_condition"] = self.f_unlock.get()
            item["effects"] = [ed.get() for ed in self.effect_editors]
            self._refresh_tree()
            if not silent:
                self.app.set_status(f"已更新: {item['upgrade_id']}")
        except Exception as e:
            if not silent:
                self.app.set_status(f"应用失败: {e}")

    def on_add(self):
        base = "new_meta_upgrade"
        counter = 1
        existing = [u.get("upgrade_id") or u.get("id") for u in self.upgrades]
        while f"{base}_{counter}" in existing:
            counter += 1
        new_item = {
            "upgrade_id": f"{base}_{counter}",
            "name_i18n_key": "New Meta Upgrade",
            "description_i18n_key": "No description",
            "max_rank": 1,
            "cost_per_rank": [],
            "effects": [],
            "unlock_condition": "newgame+",
        }
        self.upgrades.append(new_item)
        self.selected_idx = len(self.upgrades) - 1
        self._refresh_tree()
        self._load_form(new_item)
        self.app.set_status(f"添加局外养成: {new_item['upgrade_id']}")

    def on_delete(self):
        sel = self.tree.get_selected_item()
        if not sel:
            return
        name = sel.get("upgrade_id") or sel.get("id", "")
        if self.confirm_delete(name):
            self.upgrades.remove(sel)
            self.selected_idx = None
            self._refresh_tree()
            self.app.set_status("已删除局外养成词条")

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
            return []
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
