# -*- coding: utf-8 -*-
"""
BK Girl Pack Editor — _BK.ini Editor Tab
EN: Visual form editor for _BK.ini with validation and trait/personality pickers.
ZH: _BK.ini 可视化表单编辑器，支持校验与 trait/personality 选择器。
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import configparser
import json

from bk_editor.shared import DATA_DIR, LabeledEntry, LabeledSpinbox, LabeledCombobox, LabeledCheckbox


class INIEditorTab(tk.Frame):
    """EN: Edit _BK.ini for the selected girl pack.
       ZH: 编辑选中女孩包的 _BK.ini。"""

    BOOL_FIELDS = {
        "inverted_name", "unique", "keep_first_name", "keep_last_name", "keep_inverted",
        "keep_skills", "keep_traits", "keep_personality", "custom_personality", "generic_dialogue",
        "keep_tastes", "keep_sex", "move_after_meeting", "keep_generate_as", "keep_background",
    }
    INT_FIELDS = {
        "beauty", "body", "charm", "refinement", "libido", "obedience", "constitution", "sensitivity",
        "dialogue_personality_weight", "dialogue_attribute_weight",
    }
    LIST_FIELDS = {
        "always", "often", "rarely", "never",
        "favorite_acts", "disliked_acts",
        "always_fixations", "never_fixations", "favorite_fixations", "disliked_fixations",
        "always_negative_fixations", "never_negative_fixations",
        "always_slave_story", "often_slave_story", "rarely_slave_story", "never_slave_story",
        "personality_dialogue_only",
    }

    SEX_ACTS = ["naked", "service", "sex", "anal", "fetish", "bisexual", "group"]
    FARM_WEAKNESS = ["stallion", "beast", "monster", "machine", "random"]
    SEXUAL_EXPERIENCE = ["very experienced", "experienced", "average", "inexperienced", "very inexperienced", "random"]
    GENERATE_AS = ["all", "free", "slave", "story"]

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.pack_path = None
        self.cfg = None
        self.ini_path = None
        self.fields = {}
        self.trait_names = []
        self.personality_names = []
        self._load_reference_data()
        self._build_ui()

    def _load_reference_data(self):
        try:
            traits = json.loads((DATA_DIR / "traits" / "traits.json").read_text(encoding="utf-8"))
            self.trait_names = sorted({t.get("name", "") for t in traits if t.get("name")})
        except Exception:
            self.trait_names = []
        try:
            pers = json.loads((DATA_DIR / "personalities" / "personalities.json").read_text(encoding="utf-8"))
            self.personality_names = sorted({p.get("id", "") for p in pers if p.get("id")})
        except Exception:
            self.personality_names = []

    def _build_ui(self):
        header = tk.Label(
            self,
            text="_BK.ini 编辑器（保存时会移除注释，请提前备份）",
            bg="#1a1a2e",
            fg="#FFD700",
            font=("Microsoft YaHei", 12, "bold"),
        )
        header.pack(anchor=tk.W, padx=10, pady=10)

        # EN: Main paned layout.
        # ZH: 主分栏布局。
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1a1a2e", sashwidth=6)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        left = tk.Frame(paned, bg="#16213e", width=220)
        left.pack_propagate(False)
        paned.add(left, minsize=200)

        self.section_list = tk.Listbox(left, bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 11), selectbackground="#0f3460")
        self.section_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.section_list.bind("<<ListboxSelect>>", self._on_section_select)

        btn_frame = tk.Frame(left, bg="#16213e")
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(btn_frame, text="+ Section", command=self._add_section, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="- Section", command=self._del_section, bg="#660000", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="保存", command=self._save_ini, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

        right_canvas = tk.Canvas(paned, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(paned, orient=tk.VERTICAL, command=right_canvas.yview)
        self.form_frame = tk.Frame(right_canvas, bg="#1a1a2e")
        self.form_frame.bind("<Configure>", lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all")))
        right_canvas.create_window((0, 0), window=self.form_frame, anchor=tk.NW, width=800)
        right_canvas.configure(yscrollcommand=scrollbar.set)
        paned.add(right_canvas, minsize=500)
        paned.add(scrollbar, minsize=20)

    def on_pack_changed(self, path):
        self.pack_path = path
        self.fields.clear()
        for child in self.form_frame.winfo_children():
            child.destroy()
        self.section_list.delete(0, tk.END)
        if not path:
            self.cfg = None
            self.ini_path = None
            return
        self.ini_path = path / "_BK.ini"
        self.cfg = configparser.ConfigParser()
        if self.ini_path.exists():
            try:
                self.cfg.read(self.ini_path, encoding="utf-8")
            except Exception as e:
                messagebox.showerror("读取失败", f"无法解析 _BK.ini: {e}", parent=self)
                self.cfg = configparser.ConfigParser()
        else:
            self.cfg.add_section("identity")
        self._refresh_sections()
        if self.cfg.sections():
            self.section_list.selection_set(0)
            self._on_section_select()

    def _refresh_sections(self):
        self.section_list.delete(0, tk.END)
        for sec in self.cfg.sections():
            self.section_list.insert(tk.END, sec)

    def _on_section_select(self, event=None):
        sel = self.section_list.curselection()
        if not sel:
            return
        # EN: Persist edits in the previously shown section before switching.
        # ZH: 切换前先保存当前 section 的编辑。
        self._apply_current_section()
        section = self.section_list.get(sel[0])
        self._build_section_form(section)

    def _build_section_form(self, section):
        for child in self.form_frame.winfo_children():
            child.destroy()
        self.fields.clear()

        title = tk.Label(self.form_frame, text=f"Section: [{section}]", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 13, "bold"))
        title.pack(anchor=tk.W, padx=5, pady=10)

        if section not in self.cfg.sections():
            return

        items = list(self.cfg.items(section))
        for key, val in items:
            frame = tk.Frame(self.form_frame, bg="#1a1a2e")
            frame.pack(fill=tk.X, padx=5, pady=3)

            tk.Label(frame, text=key, bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 10), width=28, anchor=tk.E).pack(side=tk.LEFT)

            widget = self._make_widget(frame, section, key, val)
            widget.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            self.fields[(section, key)] = widget

        # EN: Button to add a new key.
        # ZH: 添加新键按钮。
        tk.Button(
            self.form_frame,
            text="+ 添加新键",
            command=lambda: self._add_key(section),
            bg="#0f3460",
            fg="#FFFFFF",
            relief=tk.FLAT,
        ).pack(anchor=tk.W, padx=5, pady=10)

    def _make_widget(self, parent, section, key, val):
        lower_key = key.lower()
        stripped = val.strip().strip('"')

        if lower_key in self.BOOL_FIELDS or (stripped.lower() in ("true", "false") and not val.startswith(("[", "("))):
            return LabeledCheckbox(parent, "", default=stripped.lower() == "true")

        if lower_key in self.INT_FIELDS:
            try:
                num = int(stripped)
            except ValueError:
                num = 0
            return LabeledSpinbox(parent, "", default=num, from_=0, to=10, width=10)

        if lower_key == "favorite_acts" or lower_key == "disliked_acts":
            return _ListFieldEditor(parent, val, fixed_values=self.SEX_ACTS)

        if lower_key in self.LIST_FIELDS:
            # EN: Use a multiline text widget for list fields with helper pickers.
            # ZH: 列表字段使用多行文本框并带选择器。
            if section.lower() in ("base positive traits", "base negative traits", "traits"):
                return _ListFieldEditor(parent, val, trait_names=self.trait_names)
            if section.lower() in ("base personality", "personality"):
                return _ListFieldEditor(parent, val, personality_names=self.personality_names)
            return _ListFieldEditor(parent, val)

        if lower_key == "farm_weakness":
            return LabeledCombobox(parent, "", self.FARM_WEAKNESS, default=stripped)

        if lower_key == "sexual_experience":
            return LabeledCombobox(parent, "", self.SEXUAL_EXPERIENCE, default=stripped)

        if lower_key == "generate_as":
            return LabeledCombobox(parent, "", self.GENERATE_AS, default=stripped)

        return LabeledEntry(parent, "", default=val.strip('"'), width=50)

    def _add_section(self):
        from tkinter.simpledialog import askstring
        name = askstring("新建 Section", "输入 Section 名称:", parent=self)
        if not name:
            return
        if not self.cfg.has_section(name):
            self.cfg.add_section(name)
            self._refresh_sections()

    def _del_section(self):
        sel = self.section_list.curselection()
        if not sel:
            return
        section = self.section_list.get(sel[0])
        if messagebox.askyesno("确认删除", f"删除 section [{section}]？", parent=self):
            self.cfg.remove_section(section)
            self._refresh_sections()
            for child in self.form_frame.winfo_children():
                child.destroy()

    def _add_key(self, section):
        from tkinter.simpledialog import askstring
        key = askstring("新建键", "输入键名:", parent=self)
        if not key:
            return
        val = ""
        self.cfg.set(section, key, val)
        self._build_section_form(section)

    def _save_ini(self):
        if not self.ini_path or not self.cfg:
            return
        self._apply_form_to_config()
        try:
            with open(self.ini_path, "w", encoding="utf-8") as f:
                self.cfg.write(f)
            self.app.set_status(f"已保存 _BK.ini: {self.ini_path.name}")
        except Exception as e:
            messagebox.showerror("保存失败", str(e), parent=self)

    def _apply_current_section(self):
        sel = self.section_list.curselection()
        if not sel:
            return
        section = self.section_list.get(sel[0])
        for (sec, key), widget in self.fields.items():
            if sec != section:
                continue
            val = self._widget_value(widget, key)
            self.cfg.set(section, key, val)

    def _apply_form_to_config(self):
        self._apply_current_section()

    def _widget_value(self, widget, key):
        lower_key = key.lower()
        if lower_key in self.BOOL_FIELDS:
            return "True" if widget.get() else "False"
        if lower_key in self.INT_FIELDS:
            return str(widget.get())
        if isinstance(widget, _ListFieldEditor):
            return widget.get()
        raw = widget.get()
        # EN: Quote string if it contains spaces and isn't already quoted.
        # ZH: 如果字符串包含空格且未加引号，则加上引号。
        if " " in raw and not (raw.startswith('"') and raw.endswith('"')):
            return f'"{raw}"'
        return raw


class _ListFieldEditor(tk.Frame):
    """EN: Helper widget for list fields like ["A", "B"].
       ZH: 列表字段辅助组件，例如 ["A", "B"]。"""

    def __init__(self, parent, value, trait_names=None, personality_names=None, fixed_values=None):
        super().__init__(parent, bg=parent.cget("bg"))
        self.trait_names = trait_names or []
        self.personality_names = personality_names or []
        self.fixed_values = fixed_values or []

        self.text = tk.Text(self, height=3, width=50, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Consolas", 10))
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text.insert(tk.END, value)

        if self.trait_names or self.personality_names or self.fixed_values:
            picker = ttk.Combobox(self, values=self.fixed_values or self.trait_names or self.personality_names, state="readonly", width=18)
            picker.pack(side=tk.LEFT, padx=5)
            tk.Button(self, text="添加", command=lambda: self._add_item(picker), bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT)

    def _add_item(self, picker):
        val = picker.get()
        if not val:
            return
        current = self.text.get("1.0", tk.END).strip()
        # EN: Append inside list brackets if present.
        # ZH: 如果当前内容有方括号，则在内部追加。
        if current.startswith("[") and current.endswith("]"):
            inner = current[1:-1].strip()
            if inner:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, f"[{inner}, \"{val}\"]")
            else:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, f"[\"{val}\"]")
        else:
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, f"[\"{val}\"]")

    def get(self):
        return self.text.get("1.0", tk.END).strip()
