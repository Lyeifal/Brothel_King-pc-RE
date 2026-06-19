# -*- coding: utf-8 -*-
"""
BK Dev Console — I18n Key Review Tab
EN: Read-only i18n key listing extracted from JSON data (achievements, meta, etc.).
ZH: 只读 i18n key 审查标签页，从 JSON 数据中提取国际化键名。
"""

import tkinter as tk
from tkinter import ttk

from bk_editor.dev_console.tabs.base import BaseJsonEditorTab


class I18nEditorTab(BaseJsonEditorTab):
    JSON_PATH = None  # EN: Read-only, not backed by a single JSON file.

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._collect_keys()

    def _build_ui(self):
        header = tk.Label(self, text="I18n Keys 审查（只读）", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 14))
        header.pack(anchor=tk.W, padx=10, pady=10)

        # EN: Search bar.
        # ZH: 搜索栏。
        search_frame = tk.Frame(self, bg="#16213e")
        search_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        tk.Label(search_frame, text="搜索:", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 11)).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        tk.Entry(search_frame, textvariable=self.search_var, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Microsoft YaHei", 11)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # EN: Treeview listing keys grouped by source file.
        # ZH: 按来源文件分组的 treeview 列表。
        tree_frame = tk.Frame(self, bg="#16213e")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tree = ttk.Treeview(tree_frame, columns=["key", "context"], show="tree headings", style="Dev.Treeview")
        self.tree.heading("#0", text="来源")
        self.tree.heading("key", text="I18n Key")
        self.tree.heading("context", text="上下文")
        self.tree.column("#0", width=180)
        self.tree.column("key", width=300)
        self.tree.column("context", width=200)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb = ttk.Scrollbar(tree_frame, command=self.tree.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=sb.set)

        # EN: Buttons.
        btn_frame = tk.Frame(self, bg="#16213e")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="刷新", command=self._collect_keys, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="导出 CSV", command=self._export_csv, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

    def _default_data(self):
        return None

    def _collect_keys(self):
        import json
        from bk_editor.shared import DATA_DIR
        self.keys = []
        sources = [
            ("achievements", DATA_DIR / "achievements" / "achievements.json", self._extract_achievement_keys),
            ("meta", DATA_DIR / "meta" / "meta_progression.json", self._extract_meta_keys),
            ("ngp", DATA_DIR / "ngp" / "ngp_settings.json", self._extract_ngp_keys),
        ]
        for label, path, extractor in sources:
            try:
                data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
                if data is not None:
                    for key, ctx in extractor(data):
                        self.keys.append((label, key, ctx))
            except Exception as e:
                self.keys.append((label, f"<读取失败: {e}>", ""))
        self._refresh_tree()

    @staticmethod
    def _extract_achievement_keys(data):
        keys = []
        for item in data if isinstance(data, list) else []:
            keys.append((item.get("name_i18n_key", ""), f"成就 {item.get('target', '')}"))
            keys.append((item.get("description_i18n_key", ""), f"成就描述 {item.get('target', '')}"))
        return [(k, c) for k, c in keys if k]

    @staticmethod
    def _extract_meta_keys(data):
        keys = []
        for item in data.get("meta_upgrades", []):
            keys.append((item.get("name_i18n_key", ""), f"Meta {item.get('upgrade_id', item.get('id', ''))}"))
            keys.append((item.get("description_i18n_key", ""), f"Meta描述 {item.get('upgrade_id', item.get('id', ''))}"))
        return [(k, c) for k, c in keys if k]

    @staticmethod
    def _extract_ngp_keys(data):
        keys = []
        for item in data if isinstance(data, list) else []:
            keys.append((item.get("label", ""), f"NGP {item.get('name', '')}"))
            keys.append((item.get("ttip", ""), f"NGP提示 {item.get('name', '')}"))
        return [(k, c) for k, c in keys if k]

    def _refresh_tree(self):
        for child in self.tree.get_children():
            self.tree.delete(child)
        grouped = {}
        for source, key, ctx in self.keys:
            grouped.setdefault(source, []).append((key, ctx))
        for source, rows in sorted(grouped.items()):
            node = self.tree.insert("", tk.END, text=source)
            for key, ctx in rows:
                self.tree.insert(node, tk.END, text="", values=(key, ctx))

    def _on_search(self, *args):
        term = self.search_var.get().lower()
        filtered = [k for k in self.keys if term in k[1].lower() or term in k[2].lower()]
        for child in self.tree.get_children():
            self.tree.delete(child)
        grouped = {}
        for source, key, ctx in filtered:
            grouped.setdefault(source, []).append((key, ctx))
        for source, rows in sorted(grouped.items()):
            node = self.tree.insert("", tk.END, text=source)
            for key, ctx in rows:
                self.tree.insert(node, tk.END, text="", values=(key, ctx))

    def _export_csv(self):
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], parent=self)
        if not path:
            return
        import csv
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["source", "i18n_key", "context"])
            for source, key, ctx in self.keys:
                writer.writerow([source, key, ctx])
        self.app.set_status(f"已导出 i18n keys 到 {path}")

    def on_save(self):
        # EN: Read-only tab; nothing to save.
        # ZH: 只读标签页，无需保存。
        self.app.set_status("I18n 标签页为只读，无需保存")

    def on_add(self):
        pass

    def on_delete(self):
        pass
