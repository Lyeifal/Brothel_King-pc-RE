# -*- coding: utf-8 -*-
"""
BK Editor — Shared Widgets
EN: Common tkinter widgets used across all editor tabs.
ZH: 所有编辑器标签页共用的 tkinter 组件。
"""

import tkinter as tk
from tkinter import ttk


class LabeledEntry(tk.Frame):
    """EN: A label + entry pair with optional validation.
       ZH: 标签+输入框组合，可选验证。"""

    def __init__(self, parent, label, default="", width=20, validate_fn=None, **kwargs):
        super().__init__(parent, bg=parent.cget("bg"))
        self.validate_fn = validate_fn

        self.lbl = tk.Label(self, text=label, bg=self.cget("bg"), fg="#FFFFFF", font=("Microsoft YaHei", 10))
        self.lbl.pack(side=tk.LEFT, padx=(0, 5))

        self.var = tk.StringVar(value=str(default) if default is not None else "")
        self.entry = tk.Entry(self, textvariable=self.var, width=width, **kwargs)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(str(value) if value is not None else "")

    def validate(self):
        if self.validate_fn:
            return self.validate_fn(self.get())
        return True


class LabeledSpinbox(tk.Frame):
    """EN: A label + spinbox for numeric input.
       ZH: 标签+数字选择框。"""

    def __init__(self, parent, label, default=0, from_=0, to=100, width=10):
        super().__init__(parent, bg=parent.cget("bg"))
        self.lbl = tk.Label(self, text=label, bg=self.cget("bg"), fg="#FFFFFF", font=("Microsoft YaHei", 10))
        self.lbl.pack(side=tk.LEFT, padx=(0, 5))

        self.var = tk.IntVar(value=int(default))
        self.spin = tk.Spinbox(self, from_=from_, to=to, textvariable=self.var, width=width)
        self.spin.pack(side=tk.LEFT)

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(int(value) if value is not None else 0)


class LabeledCombobox(tk.Frame):
    """EN: A label + combobox for selection from a list.
       ZH: 标签+下拉框。"""

    def __init__(self, parent, label, values, default="", width=18):
        super().__init__(parent, bg=parent.cget("bg"))
        self.lbl = tk.Label(self, text=label, bg=self.cget("bg"), fg="#FFFFFF", font=("Microsoft YaHei", 10))
        self.lbl.pack(side=tk.LEFT, padx=(0, 5))

        self.var = tk.StringVar(value=default)
        self.combo = ttk.Combobox(self, textvariable=self.var, values=values, width=width, state="readonly")
        self.combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(str(value) if value is not None else "")


class LabeledCheckbox(tk.Frame):
    """EN: A label + checkbox for boolean input.
       ZH: 标签+复选框。"""

    def __init__(self, parent, label, default=False):
        super().__init__(parent, bg=parent.cget("bg"))
        self.var = tk.BooleanVar(value=bool(default))
        self.chk = tk.Checkbutton(
            self, text=label, variable=self.var,
            bg=self.cget("bg"), fg="#FFFFFF", selectcolor="#333333",
            font=("Microsoft YaHei", 10),
            activebackground=self.cget("bg"), activeforeground="#FFFFFF",
        )
        self.chk.pack(side=tk.LEFT)

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(bool(value))


class EffectEditor(tk.Frame):
    """EN: Visual editor for a single Effect object.
       ZH: 单个 Effect 对象的可视化编辑器。"""

    EFFECT_TYPES = ["boost", "change", "gain", "instant", "special", "personality", "set", "allow", "gift", "flower"]
    EFFECT_TARGETS = [
        "reputation", "gold", "prestige", "AP", "energy", "mood",
        "beauty", "body", "charm", "refinement", "libido", "obedience", "constitution", "sensitivity",
        "service", "sex", "anal", "fetish",
        "waitress", "dancer", "masseuse", "geisha",
        "job customer budget", "whore customer budget",
        "customer defense", "crazy",
        "shop prices", "kidnap success", "spell learning",
        "special girl chance", "security upkeep",
        "overall customer satisfaction",
        "beauty preference", "body preference", "charm preference", "refinement preference",
    ]
    EFFECT_SCOPES = [None, "brothel", "farm", "city", "world"]

    def __init__(self, parent, effect=None):
        super().__init__(parent, bg=parent.cget("bg"))

        self.type_combo = LabeledCombobox(self, "类型:", self.EFFECT_TYPES, default=effect.get("type", "boost") if effect else "boost")
        self.type_combo.pack(fill=tk.X, pady=2)

        self.target_combo = LabeledCombobox(self, "目标:", self.EFFECT_TARGETS, default=effect.get("target", "") if effect else "")
        self.target_combo.pack(fill=tk.X, pady=2)

        self.value_spin = LabeledSpinbox(self, "数值:", default=effect.get("value", 0) if effect else 0, from_=-999, to=999)
        self.value_spin.pack(fill=tk.X, pady=2)

        self.scope_combo = LabeledCombobox(self, "范围:", ["(无)"] + self.EFFECT_SCOPES[1:], default=effect.get("scope", "") if effect else "")
        self.scope_combo.pack(fill=tk.X, pady=2)

    def get(self):
        return {
            "type": self.type_combo.get(),
            "target": self.target_combo.get(),
            "value": self.value_spin.get(),
            "scope": None if self.scope_combo.get() == "(无)" else self.scope_combo.get(),
        }


class JsonTreeview(ttk.Treeview):
    """EN: A Treeview specialized for displaying JSON item lists.
       ZH: 专用于显示 JSON 项列表的树形视图。"""

    def __init__(self, parent, columns, **kwargs):
        super().__init__(parent, columns=columns, show="headings", **kwargs)
        for col in columns:
            self.heading(col, text=col)
            self.column(col, width=100, anchor=tk.CENTER)
        self._items = []

    def populate(self, items, column_map):
        """EN: Clear and populate tree with items.
           column_map: dict of {tree_column: json_key}
           ZH: 清空并用 items 填充树。
           column_map: {树列名: JSON 键名} 字典。"""
        self._items = items
        self._last_column_map = column_map
        for row in self.get_children():
            self.delete(row)
        for idx, item in enumerate(items):
            values = [str(item.get(column_map.get(col, ""), "")) for col in self.cget("columns")]
            self.insert("", tk.END, values=values, tags=(str(idx),))

    def get_selected_item(self):
        """EN: Return the JSON item attached to the selected row.
           ZH: 返回选中行附加的 JSON 项。"""
        sel = self.selection()
        if not sel:
            return None
        tags = self.item(sel[0], "tags")
        if tags:
            try:
                idx = int(tags[0])
                if 0 <= idx < len(self._items):
                    return self._items[idx]
            except (ValueError, IndexError):
                pass
        return None

    def refresh(self):
        """EN: Re-populate with current items (must be called after items list changes).
           ZH: 使用当前项重新填充（items 列表变更后需调用）。"""
        self.populate(self._items, self._last_column_map)
