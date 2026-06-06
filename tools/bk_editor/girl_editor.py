# -*- coding: utf-8 -*-
"""
BK Editor — Girl System Editor
EN: Visual editor for traits, perks, stats and archetypes.
ZH: 特质、天赋、属性与原型系统的可视化编辑器。
"""

import tkinter as tk
from tkinter import ttk, messagebox
from bk_editor.core import load_json, save_json, DATA_DIR, validate_trait, validate_perk
from bk_editor.widgets import LabeledEntry, LabeledSpinbox, LabeledCombobox, LabeledCheckbox, JsonTreeview, EffectEditor


class GirlEditorFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        tk.Label(self, text="女孩系统编辑器", font=("Microsoft YaHei", 16, "bold"), bg="#1a1a2e", fg="#FFD700").pack(pady=5)
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.trait_editor = TraitEditorTab(notebook, app)
        self.perk_editor = PerkEditorTab(notebook, app)
        notebook.add(self.trait_editor, text="特质管理")
        notebook.add(self.perk_editor, text="天赋管理")


class TraitEditorTab(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.json_path = DATA_DIR / "traits" / "traits.json"
        self.items = []
        self.current_index = -1

        toolbar = tk.Frame(self, bg="#1a1a2e")
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(toolbar, text="+ 新建特质", command=self.new_item, bg="#2ECC71", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="保存", command=self.save, bg="#3498DB", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="删除", command=self.delete_item, bg="#E74C3C", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)

        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1a1a2e")
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left = tk.Frame(paned, bg="#1a1a2e")
        self.tree = JsonTreeview(left, columns=["名称", "动词", "原型"])
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
        self.f_name = LabeledEntry(self.form, "特质名称:", width=30)
        self.f_name.pack(fill=tk.X, pady=3)
        self.f_verb = LabeledEntry(self.form, "动词:", width=20)
        self.f_verb.pack(fill=tk.X, pady=3)
        self.f_archetype = LabeledEntry(self.form, "星座原型:", width=20)
        self.f_archetype.pack(fill=tk.X, pady=3)
        self.f_desc = LabeledEntry(self.form, "描述:", width=40)
        self.f_desc.pack(fill=tk.X, pady=3)
        self.f_public = LabeledCheckbox(self.form, "随机女孩可生成", default=True)
        self.f_public.pack(fill=tk.X, pady=3)
        tk.Label(self.form, text="效果列表:", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 10, "bold")).pack(anchor=tk.W, pady=(10, 2))
        self.effects_container = tk.Frame(self.form, bg="#16213e")
        self.effects_container.pack(fill=tk.X)
        eff_buttons = tk.Frame(self.form, bg="#16213e")
        eff_buttons.pack(fill=tk.X, pady=2)
        tk.Button(eff_buttons, text="+ 添加效果", command=self.add_effect_editor, bg="#2ECC71", fg="#FFFFFF").pack(side=tk.LEFT)
        tk.Button(eff_buttons, text="- 清除效果", command=self.clear_effects, bg="#E74C3C", fg="#FFFFFF").pack(side=tk.LEFT, padx=5)
        self.effect_editors = []
        tk.Button(self.form, text="应用修改", command=self.apply, bg="#9B59B6", fg="#FFFFFF").pack(pady=15)

    def add_effect_editor(self, effect_data=None):
        editor = EffectEditor(self.effects_container, effect=effect_data)
        editor.pack(fill=tk.X, pady=2)
        self.effect_editors.append(editor)

    def clear_effects(self):
        for ed in self.effect_editors:
            ed.destroy()
        self.effect_editors = []

    def load(self):
        self.items = load_json(self.json_path)
        self.refresh_list()

    def save(self):
        save_json(self.json_path, self.items)
        self.app.set_status(f"已保存 {len(self.items)} 个特质")

    def refresh_list(self):
        self.tree.populate(self.items, {"名称": "name", "动词": "verb", "原型": "archetype"})

    def on_select(self, event=None):
        item = self.tree.get_selected_item()
        if item is None:
            return
        self.current_index = self.items.index(item)
        self.f_name.set(item.get("name", ""))
        self.f_verb.set(item.get("verb", "be"))
        self.f_archetype.set(item.get("archetype", "") or "")
        self.f_desc.set(item.get("base_description", ""))
        self.f_public.set(item.get("public", True))
        self.clear_effects()
        for eff in item.get("effects", []):
            self.add_effect_editor(eff)

    def new_item(self):
        self.items.append({"name": "新特质", "verb": "be", "effects": [], "opposite": [], "archetype": None, "base_description": "", "public": True})
        self.refresh_list()

    def delete_item(self):
        if self.current_index < 0:
            return
        self.items.pop(self.current_index)
        self.current_index = -1
        self.refresh_list()

    def apply(self):
        if self.current_index < 0:
            messagebox.showwarning("提示", "请先选择一个特质")
            return
        item = self.items[self.current_index]
        item["name"] = self.f_name.get()
        item["verb"] = self.f_verb.get()
        arc = self.f_archetype.get()
        item["archetype"] = arc if arc else None
        item["base_description"] = self.f_desc.get()
        item["public"] = self.f_public.get()
        item["effects"] = [ed.get() for ed in self.effect_editors]
        errors = validate_trait(item)
        if errors:
            messagebox.showerror("验证错误", "\n".join(errors))
            return
        self.refresh_list()
        self.app.set_status(f"已更新特质: {item['name']}")


class PerkEditorTab(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.json_path = DATA_DIR / "perks" / "perks.json"
        self.items = []
        self.current_index = -1

        toolbar = tk.Frame(self, bg="#1a1a2e")
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(toolbar, text="+ 新建天赋", command=self.new_item, bg="#2ECC71", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="保存", command=self.save, bg="#3498DB", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="删除", command=self.delete_item, bg="#E74C3C", fg="#FFFFFF").pack(side=tk.LEFT, padx=2)

        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1a1a2e")
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left = tk.Frame(paned, bg="#1a1a2e")
        self.tree = JsonTreeview(left, columns=["名称", "类型", "原型"])
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
        self.f_name = LabeledEntry(self.form, "天赋名称:", width=30)
        self.f_name.pack(fill=tk.X, pady=3)
        self.f_type = LabeledCombobox(self.form, "类型:", ["skill", "passive", "active"], default="skill")
        self.f_type.pack(fill=tk.X, pady=3)
        self.f_archetype = LabeledEntry(self.form, "星座原型:", width=20)
        self.f_archetype.pack(fill=tk.X, pady=3)
        self.f_level = LabeledSpinbox(self.form, "等级:", from_=0, to=3, default=0)
        self.f_level.pack(fill=tk.X, pady=3)
        self.f_min_rank = LabeledSpinbox(self.form, "最低Rank:", from_=0, to=10, default=0)
        self.f_min_rank.pack(fill=tk.X, pady=3)
        self.f_desc = LabeledEntry(self.form, "描述:", width=40)
        self.f_desc.pack(fill=tk.X, pady=3)
        tk.Label(self.form, text="效果列表:", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 10, "bold")).pack(anchor=tk.W, pady=(10, 2))
        self.effects_container = tk.Frame(self.form, bg="#16213e")
        self.effects_container.pack(fill=tk.X)
        eff_buttons = tk.Frame(self.form, bg="#16213e")
        eff_buttons.pack(fill=tk.X, pady=2)
        tk.Button(eff_buttons, text="+ 添加效果", command=self.add_effect_editor, bg="#2ECC71", fg="#FFFFFF").pack(side=tk.LEFT)
        tk.Button(eff_buttons, text="- 清除效果", command=self.clear_effects, bg="#E74C3C", fg="#FFFFFF").pack(side=tk.LEFT, padx=5)
        self.effect_editors = []
        tk.Button(self.form, text="应用修改", command=self.apply, bg="#9B59B6", fg="#FFFFFF").pack(pady=15)

    def add_effect_editor(self, effect_data=None):
        editor = EffectEditor(self.effects_container, effect=effect_data)
        editor.pack(fill=tk.X, pady=2)
        self.effect_editors.append(editor)

    def clear_effects(self):
        for ed in self.effect_editors:
            ed.destroy()
        self.effect_editors = []

    def load(self):
        self.items = load_json(self.json_path)
        self.refresh_list()

    def save(self):
        save_json(self.json_path, self.items)
        self.app.set_status(f"已保存 {len(self.items)} 个天赋")

    def refresh_list(self):
        self.tree.populate(self.items, {"名称": "name", "类型": "type", "原型": "archetype"})

    def on_select(self, event=None):
        item = self.tree.get_selected_item()
        if item is None:
            return
        self.current_index = self.items.index(item)
        self.f_name.set(item.get("name", ""))
        self.f_type.set(item.get("type", "skill"))
        self.f_archetype.set(item.get("archetype", "") or "")
        self.f_level.set(item.get("perk_level", 0))
        self.f_min_rank.set(item.get("min_rank", 0))
        self.f_desc.set(item.get("base_description", ""))
        self.clear_effects()
        for eff in item.get("effects", []):
            self.add_effect_editor(eff)

    def new_item(self):
        self.items.append({"name": "新天赋", "type": "skill", "effects": [], "archetype": None, "perk_level": 0, "min_rank": 0, "base_description": ""})
        self.refresh_list()

    def delete_item(self):
        if self.current_index < 0:
            return
        self.items.pop(self.current_index)
        self.current_index = -1
        self.refresh_list()

    def apply(self):
        if self.current_index < 0:
            messagebox.showwarning("提示", "请先选择一个天赋")
            return
        item = self.items[self.current_index]
        item["name"] = self.f_name.get()
        item["type"] = self.f_type.get()
        arc = self.f_archetype.get()
        item["archetype"] = arc if arc else None
        item["perk_level"] = self.f_level.get()
        item["min_rank"] = self.f_min_rank.get()
        item["base_description"] = self.f_desc.get()
        item["effects"] = [ed.get() for ed in self.effect_editors]
        errors = validate_perk(item)
        if errors:
            messagebox.showerror("验证错误", "\n".join(errors))
            return
        self.refresh_list()
        self.app.set_status(f"已更新天赋: {item['name']}")
