# -*- coding: utf-8 -*-
"""
BK Scenario Editor — Dialogue Image Tag Reference Tab
EN: Search codebase for {image=...} tags and emo_xxx tags used in dialogue.
ZH: 搜索代码库中的对话图片标签 {image=...} 和表情标签 emo_xxx。
"""

import tkinter as tk
from tkinter import ttk
import re
from pathlib import Path

from bk_editor.shared import GAME_DIR


class ImageTagEditorTab(tk.Frame):
    """EN: Read-only reference for dialogue image tags.
       ZH: 对话图片标签只读参考。"""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self._build_ui()
        self._scan()

    def _build_ui(self):
        tk.Label(self, text="对话图片标签参考", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 14, "bold")).pack(anchor=tk.W, padx=10, pady=10)

        btn_frame = tk.Frame(self, bg="#1a1a2e")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="重新扫描", command=self._scan, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="复制到剪贴板", command=self._copy_all, bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

        search_frame = tk.Frame(self, bg="#1a1a2e")
        search_frame.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(search_frame, text="搜索:", bg="#1a1a2e", fg="#FFFFFF", font=("Microsoft YaHei", 10)).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        tk.Entry(search_frame, textvariable=self.search_var, bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF", width=30).pack(side=tk.LEFT, padx=5)

        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1a1a2e", sashwidth=6)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        left = tk.Frame(paned, bg="#16213e", width=300)
        left.pack_propagate(False)
        paned.add(left, minsize=250)

        tk.Label(left, text="{image=...} 标签", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=5)
        self.image_tree = ttk.Treeview(left, columns=["count"], show="headings", style="Dev.Treeview")
        self.image_tree.heading("#0", text="标签")
        self.image_tree.heading("count", text="出现次数")
        self.image_tree.column("#0", width=180)
        self.image_tree.column("count", width=80)
        self.image_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        right = tk.Frame(paned, bg="#16213e", width=300)
        right.pack_propagate(False)
        paned.add(right, minsize=250)

        tk.Label(right, text="emo_xxx / 表情标签", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=5)
        self.emo_tree = ttk.Treeview(right, columns=["count"], show="headings", style="Dev.Treeview")
        self.emo_tree.heading("#0", text="标签")
        self.emo_tree.heading("count", text="出现次数")
        self.emo_tree.column("#0", width=180)
        self.emo_tree.column("count", width=80)
        self.emo_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Context viewer
        bottom = tk.Frame(self, bg="#16213e")
        bottom.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        tk.Label(bottom, text="上下文 (选中标签后显示)", bg="#16213e", fg="#FFFFFF", font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=2)
        self.ctx_text = tk.Text(bottom, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Consolas", 9), wrap=tk.WORD)
        self.ctx_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        sb = ttk.Scrollbar(bottom, command=self.ctx_text.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.ctx_text.configure(yscrollcommand=sb.set)

        self.image_tree.bind("<<TreeviewSelect>>", lambda e: self._show_context(self.image_tree, self.image_contexts))
        self.emo_tree.bind("<<TreeviewSelect>>", lambda e: self._show_context(self.emo_tree, self.emo_contexts))

    def _scan(self):
        self.image_tags = {}
        self.emo_tags = {}
        self.image_contexts = {}
        self.emo_contexts = {}

        rpy_files = list(GAME_DIR.rglob("*.rpy"))
        for f in rpy_files:
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            # Find {image=xxx}
            for m in re.finditer(r'\{image=([^}]+)\}', text):
                tag = m.group(1).strip()
                self.image_tags[tag] = self.image_tags.get(tag, 0) + 1
                self.image_contexts.setdefault(tag, []).append((str(f.relative_to(GAME_DIR)), text[max(0, m.start()-80):m.end()+40]))
            # Find emo_xxx
            for m in re.finditer(r'\b(emo_[a-zA-Z0-9_]+)\b', text):
                tag = m.group(1)
                self.emo_tags[tag] = self.emo_tags.get(tag, 0) + 1
                self.emo_contexts.setdefault(tag, []).append((str(f.relative_to(GAME_DIR)), text[max(0, m.start()-80):m.end()+40]))

        self._refresh_trees()
        self.app.set_status(f"扫描完成: {len(self.image_tags)} 个 image 标签, {len(self.emo_tags)} 个 emo 标签")

    def _refresh_trees(self):
        for row in self.image_tree.get_children():
            self.image_tree.delete(row)
        for row in self.emo_tree.get_children():
            self.emo_tree.delete(row)
        for tag, count in sorted(self.image_tags.items(), key=lambda x: -x[1]):
            self.image_tree.insert("", tk.END, text=tag, values=(count,))
        for tag, count in sorted(self.emo_tags.items(), key=lambda x: -x[1]):
            self.emo_tree.insert("", tk.END, text=tag, values=(count,))

    def _on_search(self, *args):
        term = self.search_var.get().lower()
        for row in self.image_tree.get_children():
            self.image_tree.delete(row)
        for row in self.emo_tree.get_children():
            self.emo_tree.delete(row)
        for tag, count in sorted(self.image_tags.items(), key=lambda x: -x[1]):
            if term in tag.lower():
                self.image_tree.insert("", tk.END, text=tag, values=(count,))
        for tag, count in sorted(self.emo_tags.items(), key=lambda x: -x[1]):
            if term in tag.lower():
                self.emo_tree.insert("", tk.END, text=tag, values=(count,))

    def _show_context(self, tree, contexts):
        sel = tree.selection()
        if not sel:
            return
        tag = tree.item(sel[0], "text")
        self.ctx_text.delete("1.0", tk.END)
        for file_path, ctx in contexts.get(tag, [])[:20]:
            self.ctx_text.insert(tk.END, f"--- {file_path} ---\n")
            self.ctx_text.insert(tk.END, ctx + "\n\n")

    def _copy_all(self):
        lines = []
        lines.append("=== image tags ===")
        for tag in sorted(self.image_tags):
            lines.append(tag)
        lines.append("\n=== emo tags ===")
        for tag in sorted(self.emo_tags):
            lines.append(tag)
        text = "\n".join(lines)
        self.clipboard_clear()
        self.clipboard_append(text)
        self.app.set_status("已复制所有标签到剪贴板")
