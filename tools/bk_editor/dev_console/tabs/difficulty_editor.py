# -*- coding: utf-8 -*-
"""
BK Dev Console — Difficulty Editor Tab
EN: Editor for difficulty/difficulty.json with top-level list + dict sections.
ZH: difficulty.json 编辑器，含顶层列表与难度字典部分。
"""

import tkinter as tk
from tkinter import ttk

from bk_editor.dev_console.tabs.base import BaseJsonEditorTab
from bk_editor.shared import LabeledEntry, LabeledCombobox, LabeledSpinbox


class DifficultyEditorTab(BaseJsonEditorTab):
    JSON_PATH = "difficulty/difficulty.json"

    def __init__(self, parent, app):
        self.selected_key = None
        super().__init__(parent, app)

    def _build_ui(self):
        # EN: Use a notebook inside this tab to separate list view from per-difficulty dict.
        # ZH: 用 notebook 分隔 diff_list 与单个难度配置。
        self.notebook = ttk.Notebook(self, style="Dev.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        list_frame = tk.Frame(self.notebook, bg="#16213e")
        list_frame.pack(fill=tk.BOTH, expand=True)
        dict_frame = tk.Frame(self.notebook, bg="#16213e")
        dict_frame.pack(fill=tk.BOTH, expand=True)

        self.notebook.add(list_frame, text="diff_list")
        self.notebook.add(dict_frame, text="diff_dict")

        self._build_list_view(list_frame)
        self._build_dict_view(dict_frame)

    def _build_list_view(self, parent):
        header = tk.Label(parent, text="难度名称列表（按顺序）", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 12))
        header.pack(anchor=tk.W, padx=10, pady=10)

        self.listbox = tk.Listbox(parent, bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 11), selectbackground="#0f3460")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        sb = ttk.Scrollbar(parent, command=self.listbox.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 10), padx=(0, 10))
        self.listbox.config(yscrollcommand=sb.set)

        btn_frame = tk.Frame(parent, bg="#16213e")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="添加", command=self._add_list_item, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="删除", command=self._del_list_item, bg="#660000", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="上移", command=lambda: self._move_list_item(-1), bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="下移", command=lambda: self._move_list_item(1), bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

    def _build_dict_view(self, parent):
        # EN: Split left selector and right details for diff_dict.
        # ZH: 左侧选择器 + 右侧详情。
        paned = tk.PanedWindow(parent, orient=tk.HORIZONTAL, bg="#16213e", sashwidth=6)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left = tk.Frame(paned, bg="#16213e", width=200)
        left.pack_propagate(False)
        paned.add(left)

        self.diff_listbox = tk.Listbox(left, bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 11), selectbackground="#0f3460")
        self.diff_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.diff_listbox.bind("<<ListboxSelect>>", self._on_diff_select)

        right_canvas = tk.Canvas(parent, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=right_canvas.yview)
        self.dict_form = tk.Frame(right_canvas, bg="#1a1a2e")
        self.dict_form.bind("<Configure>", lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all")))
        right_canvas.create_window((0, 0), window=self.dict_form, anchor=tk.NW, width=500)
        right_canvas.configure(yscrollcommand=scrollbar.set)

        paned.add(right_canvas)
        paned.add(scrollbar)
        paned.paneconfig(scrollbar, minsize=20)

        self.f_name = LabeledEntry(self.dict_form, "难度名称 (name):", width=40)
        self.f_name.pack(fill=tk.X, pady=3, padx=5)

        self.f_desc = LabeledEntry(self.dict_form, "描述 i18n key:", width=40)
        self.f_desc.pack(fill=tk.X, pady=3, padx=5)

        # EN: Generic key-value editor for diff settings.
        # ZH: 通用键值编辑器，用于难度数值。
        kv_label = tk.Label(self.dict_form, text="设置 (JSON key: value):", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 11))
        kv_label.pack(anchor=tk.W, padx=5, pady=(10, 5))

        self.kv_text = tk.Text(self.dict_form, height=15, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Consolas", 10))
        self.kv_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Button(self.dict_form, text="应用更改", command=self._apply_diff_dict, bg="#0f3460", fg="#FFFFFF", font=("Microsoft YaHei", 11), relief=tk.FLAT).pack(fill=tk.X, pady=10, padx=5)

        # EN: Buttons to add/remove difficulty.
        # ZH: 添加/删除难度按钮。
        btn_frame = tk.Frame(left, bg="#16213e")
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(btn_frame, text="+ 添加", command=self._add_diff, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="- 删除", command=self._del_diff, bg="#660000", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

    def _default_data(self):
        return {"diff_list": ["easy", "normal", "hard"], "diff_settings_range": {}, "diff_dict": {}}

    def _refresh_ui(self):
        self.listbox.delete(0, tk.END)
        for name in self.data.get("diff_list", []):
            self.listbox.insert(tk.END, name)
        self._refresh_diff_listbox()

    def _refresh_diff_listbox(self):
        self.diff_listbox.delete(0, tk.END)
        for key in self.data.get("diff_dict", {}).keys():
            self.diff_listbox.insert(tk.END, key)

    def _add_list_item(self):
        from tkinter.simpledialog import askstring
        new = askstring("添加难度", "输入新难度名称:", parent=self)
        if new and new.strip():
            new = new.strip()
            if new not in self.data.get("diff_list", []):
                self.data.setdefault("diff_list", []).append(new)
                self._refresh_ui()
                self.app.set_status(f"难度列表添加: {new}")

    def _del_list_item(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        name = self.listbox.get(idx)
        if self.confirm_delete(name):
            self.data["diff_list"].pop(idx)
            self._refresh_ui()
            self.app.set_status(f"从列表删除: {name}")

    def _move_list_item(self, delta):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        new_idx = idx + delta
        lst = self.data.get("diff_list", [])
        if 0 <= new_idx < len(lst):
            lst[idx], lst[new_idx] = lst[new_idx], lst[idx]
            self._refresh_ui()
            self.listbox.selection_set(new_idx)

    def _on_diff_select(self, event=None):
        sel = self.diff_listbox.curselection()
        if not sel:
            return
        self._apply_diff_dict(silent=True)
        key = self.diff_listbox.get(sel[0])
        self.selected_key = key
        diff = self.data.get("diff_dict", {}).get(key, {})
        self.f_name.set(diff.get("name", key))
        self.f_desc.set(diff.get("description_i18n_key", ""))
        import json
        kv = {k: v for k, v in diff.items() if k not in ("name", "description_i18n_key")}
        self.kv_text.delete("1.0", tk.END)
        self.kv_text.insert(tk.END, json.dumps(kv, indent=2, ensure_ascii=False))

    def _add_diff(self):
        from tkinter.simpledialog import askstring
        key = askstring("添加难度配置", "输入难度 key（例如 very_hard）:", parent=self)
        if not key or not key.strip():
            return
        key = key.strip()
        self.data.setdefault("diff_dict", {})[key] = {"name": key}
        self._refresh_diff_listbox()
        self.app.set_status(f"添加难度配置: {key}")

    def _del_diff(self):
        sel = self.diff_listbox.curselection()
        if not sel:
            return
        key = self.diff_listbox.get(sel[0])
        if self.confirm_delete(key):
            del self.data["diff_dict"][key]
            self.selected_key = None
            self._refresh_diff_listbox()
            self.app.set_status(f"删除难度配置: {key}")

    def _apply_diff_dict(self, silent=False):
        if self.selected_key is None:
            if not silent:
                self.app.set_status("未选择难度配置")
            return
        try:
            import json
            raw = self.kv_text.get("1.0", tk.END).strip()
            kv = json.loads(raw) if raw else {}
            diff = self.data["diff_dict"].get(self.selected_key, {})
            diff["name"] = self.f_name.get()
            desc = self.f_desc.get().strip()
            if desc:
                diff["description_i18n_key"] = desc
            else:
                diff.pop("description_i18n_key", None)
            for k, v in kv.items():
                diff[k] = v
            # EN: Remove stale keys that aren't in kv and aren't special fields.
            # ZH: 移除 kv 中不存在的非特殊键。
            for k in list(diff.keys()):
                if k not in ("name", "description_i18n_key") and k not in kv:
                    diff.pop(k, None)
            self.data["diff_dict"][self.selected_key] = diff
            if not silent:
                self.app.set_status(f"已更新难度: {self.selected_key}")
        except Exception as e:
            if not silent:
                self.app.set_status(f"JSON 解析失败: {e}")

    def _on_search(self, *args):
        # EN: No search on this tab at the moment.
        # ZH: 此标签页暂不支持搜索。
        pass

    def on_save(self):
        self._apply_diff_dict(silent=True)
        super().on_save()
