# -*- coding: utf-8 -*-
"""
BK Dev Console — Data Sync Tab
EN: Inspect, validate and reformat all core/data JSON files.
ZH: 检查、验证并重新格式化所有 core/data JSON 文件。
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json

from bk_editor.dev_console.tabs.base import BaseJsonEditorTab
from bk_editor.shared import DATA_DIR, load_json, save_json


class DataSyncTab(tk.Frame):
    """EN: Sync/inspect JSON data files.
       ZH: 同步/检查 JSON 数据文件。"""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self._build_ui()
        self._scan_files()

    def _build_ui(self):
        header = tk.Label(self, text="数据同步面板", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 14, "bold"))
        header.pack(anchor=tk.W, padx=10, pady=10)

        btn_frame = tk.Frame(self, bg="#1a1a2e")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="重新扫描", command=self._scan_files, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="验证所有 JSON", command=self._validate_all, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="格式化所有 JSON", command=self._reformat_all, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

        tree_frame = tk.Frame(self, bg="#1a1a2e")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tree = ttk.Treeview(tree_frame, columns=["status", "size"], show="tree headings", style="Dev.Treeview")
        self.tree.heading("#0", text="文件")
        self.tree.heading("status", text="状态")
        self.tree.heading("size", text="大小")
        self.tree.column("#0", width=400)
        self.tree.column("status", width=100)
        self.tree.column("size", width=100)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb = ttk.Scrollbar(tree_frame, command=self.tree.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=sb.set)

        self.log = tk.Text(self, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Consolas", 10), height=10)
        self.log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def _scan_files(self):
        for child in self.tree.get_children():
            self.tree.delete(child)
        self.files = []
        if not DATA_DIR.exists():
            return
        for sub in sorted(DATA_DIR.iterdir()):
            if sub.is_dir():
                node = self.tree.insert("", tk.END, text=sub.name)
                for f in sorted(sub.iterdir()):
                    if f.suffix.lower() == ".json":
                        self.tree.insert(node, tk.END, text=f.name, values=("", f"{f.stat().st_size / 1024:.1f} KB"))
                        self.files.append(f)
        self._log(f"扫描到 {len(self.files)} 个 JSON 文件")

    def _validate_all(self):
        errors = []
        for f in self.files:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    for idx, item in enumerate(data):
                        if not isinstance(item, dict):
                            errors.append(f"{f}: 索引 {idx} 不是 dict")
                # EN: Check meta_progression has meta_upgrades key.
                # ZH: 检查 meta_progression 是否含 meta_upgrades。
                if f.name == "meta_progression.json" and "meta_upgrades" not in data:
                    errors.append(f"{f}: 缺少 meta_upgrades")
            except Exception as e:
                errors.append(f"{f}: {e}")
        self._log(f"验证完成: {len(errors)} 个错误")
        for e in errors[:20]:
            self._log(f"  ❌ {e}")
        if errors:
            messagebox.showerror("验证失败", f"发现 {len(errors)} 个问题，详见日志。", parent=self)

    def _reformat_all(self):
        count = 0
        for f in self.files:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                f.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                count += 1
            except Exception as e:
                self._log(f"格式化失败 {f}: {e}")
        self._scan_files()
        self._log(f"已格式化 {count} 个文件")

    def _log(self, text):
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)

    def load_data(self):
        pass

    def save_data(self):
        pass
