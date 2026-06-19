# -*- coding: utf-8 -*-
"""
BK Scenario Editor — Event Editor Tab
EN: CRUD editor for story_events.json and sandbox/events.json.
ZH: story_events.json / sandbox/events.json 的增删改查编辑器。
"""

import tkinter as tk
from tkinter import ttk, messagebox

from bk_editor.shared import load_json, save_json, DATA_DIR
from bk_editor.shared.widgets import LabeledEntry, LabeledSpinbox, LabeledCombobox, LabeledCheckbox


class EventEditorTab(tk.Frame):
    """EN: Editor for StoryEvent JSON entries.
       ZH: StoryEvent JSON 条目编辑器。"""

    EVENT_TYPES = ["any", "city", "day", "night", "morning"]
    WEEKDAYS = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    SEASONS = ["", "Spring", "Summer", "Fall", "Winter"]
    GAME_MODES = ["story", "sandbox", "scenario"]

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.data = []
        self.selected_idx = None
        self._build_ui()
        self._load_file("stories/story_events.json")

    def _build_ui(self):
        # Toolbar
        toolbar = tk.Frame(self, bg="#16213e", height=40)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        toolbar.pack_propagate(False)

        tk.Label(toolbar, text="数据源:", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 10)).pack(side=tk.LEFT, padx=5, pady=8)
        self.file_var = tk.StringVar(value="stories/story_events.json")
        file_combo = ttk.Combobox(toolbar, textvariable=self.file_var, values=["stories/story_events.json", "sandbox/events.json"], state="readonly", width=28)
        file_combo.pack(side=tk.LEFT, padx=5, pady=8)
        file_combo.bind("<<ComboboxSelected>>", self._on_file_change)

        for text, cmd in [("刷新", self._refresh), ("保存", self._save), ("添加", self._add), ("删除", self._delete)]:
            tk.Button(toolbar, text=text, command=cmd, bg="#0f3460", fg="#FFFFFF", font=("Microsoft YaHei", 10), relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5, pady=5)

        # Search
        search_frame = tk.Frame(toolbar, bg="#16213e")
        search_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        tk.Label(search_frame, text="搜索:", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 10)).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        tk.Entry(search_frame, textvariable=self.search_var, bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF", width=20).pack(side=tk.LEFT, padx=5)

        # Main paned
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1a1a2e", sashwidth=6)
        paned.pack(fill=tk.BOTH, expand=True)

        # Left: tree
        left = tk.Frame(paned, bg="#16213e", width=350)
        left.pack_propagate(False)
        paned.add(left, minsize=300)

        self.tree = ttk.Treeview(left, columns=["label", "chapter", "type"], show="headings", style="Dev.Treeview")
        self.tree.heading("label", text="label")
        self.tree.heading("chapter", text="chapter")
        self.tree.heading("type", text="type")
        self.tree.column("label", width=180)
        self.tree.column("chapter", width=60)
        self.tree.column("type", width=80)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Right: form
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
        tk.Label(self.form_frame, text="StoryEvent 表单", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 13, "bold")).pack(anchor=tk.W, padx=5, pady=10)

        self.f_label = LabeledEntry(self.form_frame, "label*:", width=50)
        self.f_label.pack(fill=tk.X, pady=3, padx=5)

        row1 = tk.Frame(self.form_frame, bg="#1a1a2e")
        row1.pack(fill=tk.X, pady=3, padx=5)
        self.f_chapter = LabeledSpinbox(row1, "chapter:", default=0, from_=0, to=20, width=8)
        self.f_chapter.pack(side=tk.LEFT, padx=(0, 10))
        self.f_rank = LabeledSpinbox(row1, "rank:", default=0, from_=0, to=10, width=8)
        self.f_rank.pack(side=tk.LEFT, padx=(0, 10))
        self.f_date = LabeledSpinbox(row1, "date:", default=0, from_=0, to=999, width=8)
        self.f_date.pack(side=tk.LEFT, padx=(0, 10))

        row2 = tk.Frame(self.form_frame, bg="#1a1a2e")
        row2.pack(fill=tk.X, pady=3, padx=5)
        self.f_year = LabeledSpinbox(row2, "year:", default=0, from_=0, to=10, width=8)
        self.f_year.pack(side=tk.LEFT, padx=(0, 10))
        self.f_month = LabeledSpinbox(row2, "month:", default=0, from_=0, to=12, width=8)
        self.f_month.pack(side=tk.LEFT, padx=(0, 10))
        self.f_day = LabeledSpinbox(row2, "day:", default=0, from_=0, to=31, width=8)
        self.f_day.pack(side=tk.LEFT, padx=(0, 10))

        self.f_weekday = LabeledCombobox(self.form_frame, "weekday:", self.WEEKDAYS, default="", width=18)
        self.f_weekday.pack(fill=tk.X, pady=3, padx=5)

        row3 = tk.Frame(self.form_frame, bg="#1a1a2e")
        row3.pack(fill=tk.X, pady=3, padx=5)
        self.f_chance = LabeledEntry(row3, "chance (0-1):", default="1.0", width=10)
        self.f_chance.pack(side=tk.LEFT, padx=(0, 10))
        self.f_type = LabeledCombobox(row3, "type:", self.EVENT_TYPES, default="any", width=12)
        self.f_type.pack(side=tk.LEFT, padx=(0, 10))
        self.f_AP_cost = LabeledSpinbox(row3, "AP_cost:", default=1, from_=0, to=10, width=8)
        self.f_AP_cost.pack(side=tk.LEFT, padx=(0, 10))

        row4 = tk.Frame(self.form_frame, bg="#1a1a2e")
        row4.pack(fill=tk.X, pady=3, padx=5)
        self.f_order = LabeledSpinbox(row4, "order:", default=0, from_=0, to=999, width=8)
        self.f_order.pack(side=tk.LEFT, padx=(0, 10))
        self.f_weight = LabeledSpinbox(row4, "weight:", default=1, from_=1, to=100, width=8)
        self.f_weight.pack(side=tk.LEFT, padx=(0, 10))
        self.f_once = LabeledCheckbox(row4, "once:", default=True)
        self.f_once.pack(side=tk.LEFT, padx=(0, 10))

        self.f_location = LabeledEntry(self.form_frame, "location:", width=40)
        self.f_location.pack(fill=tk.X, pady=3, padx=5)

        self.f_locations = LabeledEntry(self.form_frame, "locations (JSON list):", width=50)
        self.f_locations.pack(fill=tk.X, pady=3, padx=5)

        self.f_seasons = LabeledEntry(self.form_frame, "seasons (JSON list):", width=50)
        self.f_seasons.pack(fill=tk.X, pady=3, padx=5)

        self.f_min_gold = LabeledEntry(self.form_frame, "min_gold:", default="-999999999", width=20)
        self.f_min_gold.pack(fill=tk.X, pady=3, padx=5)

        self.f_condition = LabeledEntry(self.form_frame, "condition (story_flags key):", width=40)
        self.f_condition.pack(fill=tk.X, pady=3, padx=5)

        self.f_not_condition = LabeledEntry(self.form_frame, "not_condition:", width=40)
        self.f_not_condition.pack(fill=tk.X, pady=3, padx=5)

        self.f_room = LabeledEntry(self.form_frame, "room (brothel room):", width=30)
        self.f_room.pack(fill=tk.X, pady=3, padx=5)

        self.f_modes = LabeledEntry(self.form_frame, "modes (JSON list):", default='["story"]', width=40)
        self.f_modes.pack(fill=tk.X, pady=3, padx=5)

        self.f_call_args = LabeledEntry(self.form_frame, "call_args (JSON list):", default="[]", width=40)
        self.f_call_args.pack(fill=tk.X, pady=3, padx=5)

        self.f_description = LabeledEntry(self.form_frame, "description:", width=60)
        self.f_description.pack(fill=tk.X, pady=3, padx=5)

        tk.Button(self.form_frame, text="应用更改", command=self._apply, bg="#0f3460", fg="#FFFFFF", font=("Microsoft YaHei", 11), relief=tk.FLAT).pack(fill=tk.X, pady=10, padx=5)

        # EN: Code snippet generator
        # ZH: 代码片段生成器
        snippet_frame = tk.Frame(self.form_frame, bg="#1a1a2e")
        snippet_frame.pack(fill=tk.X, pady=5, padx=5)
        tk.Button(snippet_frame, text="生成 StoryEvent 代码", command=self._gen_event_snippet, bg="#0f3460", fg="#FFFFFF", font=("Microsoft YaHei", 10), relief=tk.FLAT).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(snippet_frame, text="生成 Ren'Py label 模板", command=self._gen_label_snippet, bg="#0f3460", fg="#FFFFFF", font=("Microsoft YaHei", 10), relief=tk.FLAT).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(snippet_frame, text="生成 add_event 代码", command=self._gen_add_event_snippet, bg="#0f3460", fg="#FFFFFF", font=("Microsoft YaHei", 10), relief=tk.FLAT).pack(side=tk.LEFT)

    def _load_file(self, rel_path):
        self.current_path = DATA_DIR / rel_path
        self.data = load_json(self.current_path, default=[])
        self.selected_idx = None
        self._refresh_tree()
        self.app.set_status(f"已加载: {rel_path} ({len(self.data)} 条)")

    def _on_file_change(self, event=None):
        self._apply(silent=True)
        self._load_file(self.file_var.get())

    def _refresh(self):
        self._load_file(self.file_var.get())

    def _save(self):
        self._apply(silent=True)
        save_json(self.current_path, self.data)
        self.app.set_status(f"已保存: {self.current_path.name}")

    def _refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, item in enumerate(self.data):
            self.tree.insert("", tk.END, values=(item.get("label", ""), item.get("chapter", 0), item.get("type", "any")), tags=(str(idx),))

    def _on_search(self, *args):
        term = self.search_var.get().lower()
        filtered = [(i, it) for i, it in enumerate(self.data) if term in it.get("label", "").lower() or term in it.get("description", "").lower()]
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, item in filtered:
            self.tree.insert("", tk.END, values=(item.get("label", ""), item.get("chapter", 0), item.get("type", "any")), tags=(str(idx),))

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
        self.f_label.set(item.get("label", ""))
        self.f_chapter.set(item.get("chapter", 0))
        self.f_rank.set(item.get("rank", 0))
        self.f_date.set(item.get("date", 0))
        self.f_year.set(item.get("year", 0))
        self.f_month.set(item.get("month", 0))
        self.f_day.set(item.get("day", 0))
        self.f_weekday.set(item.get("weekday", ""))
        self.f_chance.set(str(item.get("chance", 1.0)))
        self.f_type.set(item.get("type", "any"))
        self.f_AP_cost.set(item.get("AP_cost", 1))
        self.f_order.set(item.get("order", 0))
        self.f_weight.set(item.get("weight", 1))
        self.f_once.set(item.get("once", True))
        self.f_location.set(item.get("location", "") or "")
        self.f_locations.set(self._list_to_str(item.get("locations")))
        self.f_seasons.set(self._list_to_str(item.get("seasons")))
        self.f_min_gold.set(str(item.get("min_gold", -999999999)))
        self.f_condition.set(item.get("condition", "") or "")
        self.f_not_condition.set(item.get("not_condition", "") or "")
        self.f_room.set(item.get("room", "") or "")
        self.f_modes.set(self._list_to_str(item.get("modes", ["story"])))
        self.f_call_args.set(self._list_to_str(item.get("call_args", [])))
        self.f_description.set(item.get("description", "") or "")

    def _apply(self, silent=False):
        if self.selected_idx is None or self.selected_idx >= len(self.data):
            if not silent:
                self.app.set_status("未选择事件")
            return
        try:
            item = self.data[self.selected_idx]
            item["label"] = self.f_label.get()
            item["chapter"] = int(self.f_chapter.get())
            item["rank"] = int(self.f_rank.get())
            item["date"] = int(self.f_date.get())
            item["year"] = int(self.f_year.get())
            item["month"] = int(self.f_month.get())
            item["day"] = int(self.f_day.get())
            item["weekday"] = self.f_weekday.get()
            item["chance"] = float(self.f_chance.get())
            item["type"] = self.f_type.get()
            item["AP_cost"] = int(self.f_AP_cost.get())
            item["order"] = int(self.f_order.get())
            item["weight"] = int(self.f_weight.get())
            item["once"] = bool(self.f_once.get())
            loc = self.f_location.get().strip()
            item["location"] = loc if loc else None
            item["locations"] = self._str_to_list(self.f_locations.get())
            item["seasons"] = self._str_to_list(self.f_seasons.get())
            item["min_gold"] = int(self.f_min_gold.get())
            cond = self.f_condition.get().strip()
            item["condition"] = cond if cond else None
            ncond = self.f_not_condition.get().strip()
            item["not_condition"] = ncond if ncond else None
            room = self.f_room.get().strip()
            item["room"] = room if room else None
            item["modes"] = self._str_to_list(self.f_modes.get()) or ["story"]
            item["call_args"] = self._str_to_list(self.f_call_args.get()) or []
            item["description"] = self.f_description.get()
            self._refresh_tree()
            if not silent:
                self.app.set_status(f"已更新: {item['label']}")
        except Exception as e:
            if not silent:
                self.app.set_status(f"应用失败: {e}")

    def _add(self):
        base = "new_event"
        counter = 1
        existing = {it.get("label") for it in self.data}
        while f"{base}_{counter}" in existing:
            counter += 1
        new_item = {
            "label": f"{base}_{counter}",
            "chapter": 0, "rank": 0, "date": 0, "year": 0, "month": 0, "day": 0,
            "weekday": "", "chance": 1.0, "type": "any", "AP_cost": 1,
            "order": 0, "weight": 1, "once": True, "location": None,
            "locations": None, "seasons": None, "min_gold": -999999999,
            "condition": None, "not_condition": None, "room": None,
            "modes": ["story"], "call_args": [], "description": "",
        }
        self.data.append(new_item)
        self.selected_idx = len(self.data) - 1
        self._refresh_tree()
        self._load_form(new_item)
        self.app.set_status(f"添加事件: {new_item['label']}")

    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            return
        tags = self.tree.item(sel[0], "tags")
        if not tags:
            return
        idx = int(tags[0])
        label = self.data[idx].get("label", "")
        if messagebox.askyesno("确认删除", f"确定删除 '{label}'？", parent=self):
            self.data.pop(idx)
            self.selected_idx = None
            self._refresh_tree()
            self.app.set_status("已删除事件")

    def _gen_event_snippet(self):
        """EN: Generate StoryEvent constructor code.
           ZH: 生成 StoryEvent 构造函数代码。"""
        if self.selected_idx is None:
            messagebox.showinfo("提示", "请先选择一个事件", parent=self)
            return
        item = self.data[self.selected_idx]
        parts = ['"%s"' % item.get("label", "")]
        for key in ["chapter", "rank", "date", "year", "month", "day", "weekday",
                    "chance", "type", "location", "locations", "seasons",
                    "min_gold", "condition", "not_condition", "room", "modes", "call_args"]:
            val = item.get(key)
            if val is None:
                continue
            if key in ("locations", "seasons", "modes", "call_args") and isinstance(val, list):
                parts.append("%s=%s" % (key, repr(val)))
            elif key == "weekday" and val:
                parts.append('%s="%s"' % (key, val))
            elif key in ("type", "location", "condition", "not_condition", "room") and val:
                parts.append('%s="%s"' % (key, val))
            elif key == "chance" and val != 1.0:
                parts.append("%s=%s" % (key, val))
            elif key in ("chapter", "rank", "date", "year", "month", "day", "min_gold") and val:
                parts.append("%s=%s" % (key, val))
        code = "StoryEvent(%s)" % ", ".join(parts)
        self._copy_to_clipboard(code)
        self.app.set_status("已复制 StoryEvent 代码到剪贴板")

    def _gen_label_snippet(self):
        """EN: Generate Ren'Py label template.
           ZH: 生成 Ren'Py label 模板。"""
        if self.selected_idx is None:
            messagebox.showinfo("提示", "请先选择一个事件", parent=self)
            return
        label = self.data[self.selected_idx].get("label", "my_event")
        template = '''label %s:
    # EN: Event generated by BK Scenario Editor
    # ZH: 由 BK 剧本编辑器生成的事件

    scene black with fade

    # TODO: Add your dialogue and choices here

    return
''' % label
        self._copy_to_clipboard(template)
        self.app.set_status("已复制 Ren'Py label 模板到剪贴板")

    def _gen_add_event_snippet(self):
        """EN: Generate add_event or story_add_event call code.
           ZH: 生成 add_event 或 story_add_event 调用代码。"""
        if self.selected_idx is None:
            messagebox.showinfo("提示", "请先选择一个事件", parent=self)
            return
        item = self.data[self.selected_idx]
        label = item.get("label", "")
        ev_type = item.get("type", "city")
        location = item.get("location", "")

        if location:
            code = 'story_add_event("%s")' % label
        else:
            code = 'add_event("%s", type="%s")' % (label, ev_type)
        self._copy_to_clipboard(code)
        self.app.set_status("已复制 add_event 代码到剪贴板")

    def _copy_to_clipboard(self, text):
        """EN: Copy text to system clipboard.
           ZH: 将文本复制到系统剪贴板。"""
        self.clipboard_clear()
        self.clipboard_append(text)

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
        return result if result else None
