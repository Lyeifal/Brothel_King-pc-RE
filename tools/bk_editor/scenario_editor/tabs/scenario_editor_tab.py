# -*- coding: utf-8 -*-
"""
BK Scenario Editor — Scenario Editor Tab
EN: CRUD editor for scenarios/scenarios.json.
ZH: scenarios.json 的增删改查编辑器。
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json

from bk_editor.shared import load_json, save_json, DATA_DIR
from bk_editor.shared.widgets import LabeledEntry, LabeledSpinbox


class ScenarioEditorTab(tk.Frame):
    """EN: Editor for scenario pack JSON entries.
       ZH: 剧本包 JSON 条目编辑器。"""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.data = []
        self.selected_idx = None
        self._build_ui()
        self._load()

    def _build_ui(self):
        toolbar = tk.Frame(self, bg="#16213e", height=40)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        toolbar.pack_propagate(False)
        for text, cmd in [("刷新", self._load), ("保存", self._save), ("添加", self._add), ("删除", self._delete)]:
            tk.Button(toolbar, text=text, command=cmd, bg="#0f3460", fg="#FFFFFF", font=("Microsoft YaHei", 10), relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5, pady=5)

        search_frame = tk.Frame(toolbar, bg="#16213e")
        search_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        tk.Label(search_frame, text="搜索:", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 10)).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        tk.Entry(search_frame, textvariable=self.search_var, bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF", width=20).pack(side=tk.LEFT, padx=5)

        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1a1a2e", sashwidth=6)
        paned.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(paned, bg="#16213e", width=350)
        left.pack_propagate(False)
        paned.add(left, minsize=300)

        self.tree = ttk.Treeview(left, columns=["id", "name"], show="headings", style="Dev.Treeview")
        self.tree.heading("id", text="scenario_id")
        self.tree.heading("name", text="name")
        self.tree.column("id", width=180)
        self.tree.column("name", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        right_canvas = tk.Canvas(paned, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(paned, orient=tk.VERTICAL, command=right_canvas.yview)
        self.form_frame = tk.Frame(right_canvas, bg="#1a1a2e")
        self.form_frame.bind("<Configure>", lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all")))
        right_canvas.create_window((0, 0), window=self.form_frame, anchor=tk.NW, width=700)
        right_canvas.configure(yscrollcommand=scrollbar.set)
        paned.add(right_canvas, minsize=600)
        paned.add(scrollbar, minsize=20)

        self._build_form()

    def _build_form(self):
        tk.Label(self.form_frame, text="Scenario 表单", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 13, "bold")).pack(anchor=tk.W, padx=5, pady=10)

        self.f_id = LabeledEntry(self.form_frame, "scenario_id*:", width=50)
        self.f_id.pack(fill=tk.X, pady=3, padx=5)

        self.f_name = LabeledEntry(self.form_frame, "name*:", width=50)
        self.f_name.pack(fill=tk.X, pady=3, padx=5)

        self.f_desc = LabeledEntry(self.form_frame, "description:", width=60)
        self.f_desc.pack(fill=tk.X, pady=3, padx=5)

        self.f_author = LabeledEntry(self.form_frame, "author:", width=40)
        self.f_author.pack(fill=tk.X, pady=3, padx=5)

        self.f_version = LabeledEntry(self.form_frame, "version:", default="1.0", width=20)
        self.f_version.pack(fill=tk.X, pady=3, padx=5)

        self.f_script = LabeledEntry(self.form_frame, "events_script (Ren'Py label):", default="scenario_default", width=40)
        self.f_script.pack(fill=tk.X, pady=3, padx=5)

        tk.Label(self.form_frame, text="starting_conditions (JSON):", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 10)).pack(anchor=tk.W, padx=5, pady=(10, 2))
        self.f_start = tk.Text(self.form_frame, height=4, width=60, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Consolas", 10))
        self.f_start.pack(fill=tk.X, padx=5, pady=2)
        self.f_start.insert(tk.END, "{}")

        tk.Label(self.form_frame, text="victory_conditions (JSON list):", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 10)).pack(anchor=tk.W, padx=5, pady=(10, 2))
        self.f_victory = tk.Text(self.form_frame, height=4, width=60, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Consolas", 10))
        self.f_victory.pack(fill=tk.X, padx=5, pady=2)
        self.f_victory.insert(tk.END, "[]")

        tk.Label(self.form_frame, text="rules (JSON):", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 10)).pack(anchor=tk.W, padx=5, pady=(10, 2))
        self.f_rules = tk.Text(self.form_frame, height=4, width=60, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Consolas", 10))
        self.f_rules.pack(fill=tk.X, padx=5, pady=2)
        self.f_rules.insert(tk.END, "{}")

        tk.Button(self.form_frame, text="应用更改", command=self._apply, bg="#0f3460", fg="#FFFFFF", font=("Microsoft YaHei", 11), relief=tk.FLAT).pack(fill=tk.X, pady=10, padx=5)

    def _load(self):
        self.data = load_json(DATA_DIR / "scenarios" / "scenarios.json", default=[])
        self.selected_idx = None
        self._refresh_tree()
        self.app.set_status(f"已加载 scenarios ({len(self.data)} 条)")

    def _save(self):
        self._apply(silent=True)
        save_json(DATA_DIR / "scenarios" / "scenarios.json", self.data)
        self.app.set_status("已保存 scenarios")

    def _refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, item in enumerate(self.data):
            self.tree.insert("", tk.END, values=(item.get("scenario_id", ""), item.get("name", "")), tags=(str(idx),))

    def _on_search(self, *args):
        term = self.search_var.get().lower()
        filtered = [(i, it) for i, it in enumerate(self.data) if term in it.get("scenario_id", "").lower() or term in it.get("name", "").lower()]
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, item in filtered:
            self.tree.insert("", tk.END, values=(item.get("scenario_id", ""), item.get("name", "")), tags=(str(idx),))

    def _on_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        tags = self.tree.item(sel[0], "tags")
        if tags:
            try:
                idx = int(tags[0])
                self._apply(silent=True)
                self.selected_idx = idx
                self._load_form(self.data[idx])
            except (ValueError, IndexError):
                pass

    def _load_form(self, item):
        self.f_id.set(item.get("scenario_id", ""))
        self.f_name.set(item.get("name", ""))
        self.f_desc.set(item.get("description", ""))
        self.f_author.set(item.get("author", ""))
        self.f_version.set(item.get("version", "1.0"))
        self.f_script.set(item.get("events_script", "scenario_default"))
        self.f_start.delete("1.0", tk.END)
        self.f_start.insert(tk.END, json.dumps(item.get("starting_conditions", {}), indent=2, ensure_ascii=False))
        self.f_victory.delete("1.0", tk.END)
        self.f_victory.insert(tk.END, json.dumps(item.get("victory_conditions", []), indent=2, ensure_ascii=False))
        self.f_rules.delete("1.0", tk.END)
        self.f_rules.insert(tk.END, json.dumps(item.get("rules", {}), indent=2, ensure_ascii=False))

    def _apply(self, silent=False):
        if self.selected_idx is None or self.selected_idx >= len(self.data):
            if not silent:
                self.app.set_status("未选择剧本")
            return
        try:
            item = self.data[self.selected_idx]
            item["scenario_id"] = self.f_id.get().strip()
            item["name"] = self.f_name.get().strip()
            item["description"] = self.f_desc.get().strip()
            item["author"] = self.f_author.get().strip()
            item["version"] = self.f_version.get().strip()
            item["events_script"] = self.f_script.get().strip()
            item["starting_conditions"] = json.loads(self.f_start.get("1.0", tk.END).strip() or "{}")
            item["victory_conditions"] = json.loads(self.f_victory.get("1.0", tk.END).strip() or "[]")
            item["rules"] = json.loads(self.f_rules.get("1.0", tk.END).strip() or "{}")
            self._refresh_tree()
            if not silent:
                self.app.set_status(f"已更新: {item['scenario_id']}")
        except Exception as e:
            if not silent:
                self.app.set_status(f"应用失败: {e}")

    def _add(self):
        base = "author.scenario_name"
        counter = 1
        existing = {it.get("scenario_id") for it in self.data}
        while f"author.scenario_{counter}" in existing:
            counter += 1
        new_item = {
            "scenario_id": f"author.scenario_{counter}",
            "name": "New Scenario",
            "description": "",
            "author": "",
            "version": "1.0",
            "events_script": "scenario_default",
            "starting_conditions": {},
            "victory_conditions": [],
            "rules": {},
        }
        self.data.append(new_item)
        self.selected_idx = len(self.data) - 1
        self._refresh_tree()
        self._load_form(new_item)
        self.app.set_status(f"添加剧本: {new_item['scenario_id']}")

    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            return
        tags = self.tree.item(sel[0], "tags")
        if not tags:
            return
        idx = int(tags[0])
        sid = self.data[idx].get("scenario_id", "")
        if messagebox.askyesno("确认删除", f"确定删除 '{sid}'？", parent=self):
            self.data.pop(idx)
            self.selected_idx = None
            self._refresh_tree()
            self.app.set_status("已删除剧本")
