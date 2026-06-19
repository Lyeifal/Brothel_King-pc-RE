# -*- coding: utf-8 -*-
"""
BK Girl Pack Editor — Trait / Perk Creator Tab
EN: Form-based creator for custom traits and perks, saved to core/data/traits/ or perks/.
ZH: 自定义 Trait / Perk 表单创建器，保存到 core/data/traits/ 或 perks/。
"""

import tkinter as tk
from tkinter import ttk, messagebox

from bk_editor.shared import (
    load_json,
    save_json,
    merge_json,
    DATA_DIR,
    LabeledEntry,
    LabeledCombobox,
    LabeledCheckbox,
    EffectEditor,
)


class TraitCreatorTab(tk.Frame):
    """EN: Create and edit custom Trait / Perk definitions.
       ZH: 创建并编辑自定义 Trait / Perk 定义。"""

    TRAIT_TYPES = ["trait", "perk"]
    TRAIT_SLOTS = ["personality", "background", " genetic", "special", "fixation", "market"]
    EFFECT_TYPES = ["boost", "change", "gain", "instant", "special", "personality", "set", "allow", "gift", "flower"]

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.effect_editors = []
        self._build_ui()

    def _build_ui(self):
        header = tk.Label(
            self,
            text="自定义 Trait / Perk 创建器",
            bg="#1a1a2e",
            fg="#FFFFFF",
            font=("Microsoft YaHei", 14, "bold"),
        )
        header.pack(anchor=tk.W, padx=10, pady=10)

        # EN: Type selector.
        # ZH: 类型选择。
        type_frame = tk.Frame(self, bg="#1a1a2e")
        type_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(type_frame, text="类型:", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 11)).pack(side=tk.LEFT)
        self.type_var = tk.StringVar(value="trait")
        for t in self.TRAIT_TYPES:
            tk.Radiobutton(
                type_frame,
                text=t,
                variable=self.type_var,
                value=t,
                bg="#1a1a2e",
                fg="#FFFFFF",
                selectcolor="#333333",
                font=("Microsoft YaHei", 11),
                activebackground="#1a1a2e",
                activeforeground="#FFFFFF",
                command=self._on_type_changed,
            ).pack(side=tk.LEFT, padx=5)

        # EN: Form fields.
        # ZH: 表单字段。
        form_frame = tk.Frame(self, bg="#1a1a2e")
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        self.f_id = LabeledEntry(form_frame, "ID (唯一标识):", width=40)
        self.f_id.pack(fill=tk.X, pady=3)

        self.f_name = LabeledEntry(form_frame, "显示名称 i18n key:", width=40)
        self.f_name.pack(fill=tk.X, pady=3)

        self.f_desc = LabeledEntry(form_frame, "描述 i18n key:", width=40)
        self.f_desc.pack(fill=tk.X, pady=3)

        self.f_slot = LabeledCombobox(form_frame, "槽位 (slot):", self.TRAIT_SLOTS)
        self.f_slot.pack(fill=tk.X, pady=3)

        self.f_hidden = LabeledCheckbox(form_frame, "隐藏 (hidden):")
        self.f_hidden.pack(anchor=tk.W, pady=3)

        self.f_cost = LabeledEntry(form_frame, "cost / 解锁价格:", default="0", width=20)
        self.f_cost.pack(fill=tk.X, pady=3)

        # EN: Effects section.
        # ZH: Effects 区域。
        eff_label = tk.Label(self, text="Effects:", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 12))
        eff_label.pack(anchor=tk.W, padx=10, pady=(15, 5))

        self.effects_frame = tk.Frame(self, bg="#1a1a2e")
        self.effects_frame.pack(fill=tk.X, padx=10, pady=5)

        eff_btn_frame = tk.Frame(self, bg="#1a1a2e")
        eff_btn_frame.pack(fill=tk.X, padx=10)
        tk.Button(eff_btn_frame, text="+ 添加 Effect", command=self._add_effect, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(eff_btn_frame, text="- 移除最后一个", command=self._remove_last_effect, bg="#660000", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

        # EN: Existing entries list.
        # ZH: 已有条目列表。
        list_frame = tk.Frame(self, bg="#1a1a2e")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(list_frame, text="已有条目（双击加载）", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 11)).pack(anchor=tk.W)
        self.tree = ttk.Treeview(list_frame, columns=["id", "type", "name", "slot"], show="headings", style="Dev.Treeview")
        for col in ["id", "type", "name", "slot"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self._on_tree_double)
        sb = ttk.Scrollbar(list_frame, command=self.tree.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=sb.set)

        # EN: Action buttons.
        # ZH: 操作按钮。
        btn_frame = tk.Frame(self, bg="#1a1a2e")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="保存", command=self._on_save, bg="#0f3460", fg="#FFFFFF", font=("Microsoft YaHei", 11), relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="新建", command=self._on_new, bg="#0f3460", fg="#FFFFFF", font=("Microsoft YaHei", 11), relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="删除", command=self._on_delete, bg="#660000", fg="#FFFFFF", font=("Microsoft YaHei", 11), relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

        self._on_type_changed()

    def _on_type_changed(self):
        self._refresh_tree()

    def _json_path(self):
        sub = "traits" if self.type_var.get() == "trait" else "perks"
        return DATA_DIR / sub / f"{sub}.json"

    def _load_data(self):
        return load_json(self._json_path(), default=[])

    def _refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self._load_data():
            self.tree.insert(
                "",
                tk.END,
                values=(item.get("id", ""), self.type_var.get(), item.get("name_i18n_key", ""), item.get("slot", "")),
            )

    def _add_effect(self):
        editor = EffectEditor(self.effects_frame)
        editor.pack(fill=tk.X, pady=3)
        self.effect_editors.append(editor)

    def _remove_last_effect(self):
        if self.effect_editors:
            ed = self.effect_editors.pop()
            ed.destroy()

    def _on_tree_double(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        target_id = values[0]
        for item in self._load_data():
            if item.get("id") == target_id:
                self._load_form(item)
                return

    def _load_form(self, item):
        self.f_id.set(item.get("id", ""))
        self.f_name.set(item.get("name_i18n_key", ""))
        self.f_desc.set(item.get("description_i18n_key", ""))
        self.f_slot.set(item.get("slot", ""))
        self.f_hidden.set(item.get("hidden", False))
        self.f_cost.set(str(item.get("cost", 0)))
        for child in self.effects_frame.winfo_children():
            child.destroy()
        self.effect_editors = []
        for eff in item.get("effects", []):
            self._add_effect()
            self.effect_editors[-1].type_combo.set(eff.get("type", "boost"))
            self.effect_editors[-1].target_combo.set(eff.get("target", ""))
            self.effect_editors[-1].value_spin.set(eff.get("value", 0))
            scope = eff.get("scope", "")
            self.effect_editors[-1].scope_combo.set("" if scope is None else scope)

    def _on_new(self):
        self.f_id.set("")
        self.f_name.set("")
        self.f_desc.set("")
        self.f_slot.set(self.TRAIT_SLOTS[0])
        self.f_hidden.set(False)
        self.f_cost.set("0")
        for child in self.effects_frame.winfo_children():
            child.destroy()
        self.effect_editors = []

    def _on_save(self):
        try:
            new_item = {
                "id": self.f_id.get().strip(),
                "name_i18n_key": self.f_name.get().strip(),
                "description_i18n_key": self.f_desc.get().strip(),
                "slot": self.f_slot.get(),
                "hidden": bool(self.f_hidden.get()),
                "cost": int(self.f_cost.get() or 0),
                "effects": [ed.get() for ed in self.effect_editors],
            }
        except Exception as e:
            messagebox.showerror("表单错误", f"无法解析输入: {e}", parent=self)
            return
        if not new_item["id"]:
            messagebox.showerror("表单错误", "ID 不能为空", parent=self)
            return
        path = self._json_path()
        data = self._load_data()
        # EN: Replace existing or append.
        # ZH: 替换已有或追加。
        found = False
        for i, it in enumerate(data):
            if it.get("id") == new_item["id"]:
                data[i] = new_item
                found = True
                break
        if not found:
            data.append(new_item)
        save_json(path, data)
        self._refresh_tree()
        self.app.set_status(f"已保存 {self.type_var.get()}: {new_item['id']}")

    def _on_delete(self):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        target_id = values[0]
        if not messagebox.askyesno("确认删除", f"确定删除 {target_id}？", parent=self):
            return
        data = [it for it in self._load_data() if it.get("id") != target_id]
        save_json(self._json_path(), data)
        self._refresh_tree()
        self.app.set_status(f"已删除 {target_id}")

    def on_pack_changed(self, path):
        # EN: Trait creator doesn't depend on current pack; no-op.
        # ZH: Trait 创建器不依赖当前包，无需操作。
        pass
