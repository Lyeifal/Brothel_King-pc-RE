# -*- coding: utf-8 -*-
"""
BK Editor — Story Event Editor
EN: Visual editor for StoryEvent definitions.
ZH: StoryEvent 定义的可视化编辑器。
"""

import tkinter as tk
from tkinter import ttk, messagebox
from bk_editor.core import load_json, save_json, DATA_DIR, EVENT_TYPES, GAME_MODES, WEEKDAYS, SEASONS, validate_story_event
from bk_editor.widgets import LabeledEntry, LabeledSpinbox, LabeledCombobox, LabeledCheckbox, JsonTreeview


class StoryEditorFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.json_path = DATA_DIR / "stories" / "story_events.json"
        self.items = []
        self.current_index = -1

        tk.Label(self, text="剧情事件编辑器", font=("Microsoft YaHei", 16, "bold"), bg="#1a1a2e", fg="#FFD700").pack(pady=5)

        # EN: Toolbar
        toolbar = tk.Frame(self, bg="#1a1a2e")
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(toolbar, text="+ 新建", command=self.new_item, bg="#2ECC71", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="保存", command=self.save, bg="#3498DB", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="删除", command=self.delete_item, bg="#E74C3C", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)

        # EN: Mode filter
        self.mode_filter = LabeledCombobox(toolbar, "模式筛选:", ["全部"] + GAME_MODES, default="全部")
        self.mode_filter.pack(side=tk.RIGHT, padx=5)
        self.mode_filter.combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_list())

        # EN: Split pane
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1a1a2e")
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # EN: Left — list
        left = tk.Frame(paned, bg="#1a1a2e")
        self.tree = JsonTreeview(left, columns=["标签", "章节", "类型", "模式"])
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        paned.add(left, minsize=300)

        # EN: Right — form
        right = tk.Frame(paned, bg="#16213e")
        self._build_form(right)
        paned.add(right, minsize=500)

        self.load()

    def _build_form(self, parent):
        self.form = tk.Frame(parent, bg="#16213e")
        self.form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.f_label = LabeledEntry(self.form, "标签 (label):", width=30)
        self.f_label.pack(fill=tk.X, pady=3)

        self.f_chapter = LabeledSpinbox(self.form, "章节:", from_=0, to=10, default=0)
        self.f_chapter.pack(fill=tk.X, pady=3)

        self.f_type = LabeledCombobox(self.form, "事件类型:", EVENT_TYPES, default="city")
        self.f_type.pack(fill=tk.X, pady=3)

        self.f_chance = LabeledEntry(self.form, "几率 (0.0-1.0):", default="1.0", width=10)
        self.f_chance.pack(fill=tk.X, pady=3)

        self.f_location = LabeledEntry(self.form, "地点:", width=25)
        self.f_location.pack(fill=tk.X, pady=3)

        self.f_condition = LabeledEntry(self.form, "条件 (story_flag):", width=25)
        self.f_condition.pack(fill=tk.X, pady=3)

        self.f_not_condition = LabeledEntry(self.form, "排除条件:", width=25)
        self.f_not_condition.pack(fill=tk.X, pady=3)

        self.f_once = LabeledCheckbox(self.form, "仅触发一次", default=True)
        self.f_once.pack(fill=tk.X, pady=3)

        self.f_order = LabeledSpinbox(self.form, "排序优先级:", from_=-10, to=10, default=0)
        self.f_order.pack(fill=tk.X, pady=3)

        self.f_modes = tk.Frame(self.form, bg="#16213e")
        self.f_modes.pack(fill=tk.X, pady=3)
        tk.Label(self.f_modes, text="适用模式:", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 10)).pack(side=tk.LEFT)
        self.mode_vars = {}
        for mode in GAME_MODES:
            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(self.f_modes, text=mode, variable=var, bg="#16213e", fg="#FFFFFF", selectcolor="#333333")
            chk.pack(side=tk.LEFT, padx=5)
            self.mode_vars[mode] = var

        self.f_desc = LabeledEntry(self.form, "描述:", width=40)
        self.f_desc.pack(fill=tk.X, pady=3)

        tk.Button(self.form, text="应用修改", command=self.apply, bg="#9B59B6", fg="#FFFFFF").pack(pady=10)

    def load(self):
        self.items = load_json(self.json_path)
        self.refresh_list()

    def save(self):
        save_json(self.json_path, self.items)
        self.app.set_status(f"已保存 {len(self.items)} 个事件到 {self.json_path}")

    def refresh_list(self):
        filter_mode = self.mode_filter.get()
        filtered = []
        for item in self.items:
            modes = item.get("modes", [])
            if filter_mode == "全部" or filter_mode in modes:
                filtered.append(item)
        self.tree.populate(filtered, {"标签": "label", "章节": "chapter", "类型": "type", "模式": "modes"})

    def on_select(self, event=None):
        item = self.tree.get_selected_item()
        if item is None:
            return
        self.current_index = self.items.index(item)
        self.f_label.set(item.get("label", ""))
        self.f_chapter.set(item.get("chapter", 0))
        self.f_type.set(item.get("type", "city"))
        self.f_chance.set(item.get("chance", 1.0))
        self.f_location.set(item.get("location", ""))
        self.f_condition.set(item.get("condition", ""))
        self.f_not_condition.set(item.get("not_condition", ""))
        self.f_once.set(item.get("once", True))
        self.f_order.set(item.get("order", 0))
        self.f_desc.set(item.get("description", ""))
        for mode, var in self.mode_vars.items():
            var.set(mode in item.get("modes", []))

    def new_item(self):
        new_item = {
            "label": "new_event",
            "chapter": 1,
            "type": "city",
            "chance": 1.0,
            "once": True,
            "order": 0,
            "modes": ["story"],
            "description": "",
        }
        self.items.append(new_item)
        self.refresh_list()
        self.app.set_status("新建事件，请在右侧编辑后保存")

    def delete_item(self):
        if self.current_index < 0 or self.current_index >= len(self.items):
            return
        self.items.pop(self.current_index)
        self.current_index = -1
        self.refresh_list()

    def apply(self):
        if self.current_index < 0 or self.current_index >= len(self.items):
            messagebox.showwarning("提示", "请先选择一个事件")
            return
        item = self.items[self.current_index]
        item["label"] = self.f_label.get()
        item["chapter"] = self.f_chapter.get()
        item["type"] = self.f_type.get()
        try:
            item["chance"] = float(self.f_chance.get())
        except ValueError:
            item["chance"] = 1.0
        loc = self.f_location.get()
        item["location"] = loc if loc else None
        cond = self.f_condition.get()
        item["condition"] = cond if cond else None
        ncond = self.f_not_condition.get()
        item["not_condition"] = ncond if ncond else None
        item["once"] = self.f_once.get()
        item["order"] = self.f_order.get()
        item["description"] = self.f_desc.get()
        item["modes"] = [m for m, var in self.mode_vars.items() if var.get()]
        errors = validate_story_event(item)
        if errors:
            messagebox.showerror("验证错误", "\n".join(errors))
            return
        self.refresh_list()
        self.app.set_status(f"已更新事件: {item['label']}")
