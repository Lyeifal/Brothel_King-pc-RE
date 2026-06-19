# -*- coding: utf-8 -*-
"""
BK Dev Console — Base Tab
EN: Common base class for JSON data editor tabs.
ZH: JSON 数据编辑器标签页的公共基类。
"""

import tkinter as tk
from tkinter import ttk, messagebox

from bk_editor.shared import load_json, save_json, DATA_DIR


class BaseJsonEditorTab(tk.Frame):
    """EN: Base class for a dev-console JSON editor tab.
       ZH: 开发控制台 JSON 编辑器标签页基类。"""

    JSON_PATH = None  # EN: Override in subclass (relative to DATA_DIR). ZH: 在子类中覆盖（相对于 DATA_DIR）。
    SCHEMA_NAME = None

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.data = None
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        """EN: Build common UI: toolbar, tree, details pane.
           ZH: 构建通用 UI：工具栏、树、详情面板。"""
        # EN: Toolbar.
        # ZH: 工具栏。
        self.toolbar = tk.Frame(self, bg="#16213e", height=40)
        self.toolbar.pack(fill=tk.X, pady=(0, 5))
        self.toolbar.pack_propagate(False)

        self._add_toolbar_button("刷新", self.load_data)
        self._add_toolbar_button("保存", self.save_data)
        self._add_separator()
        self._add_toolbar_button("添加", self.on_add)
        self._add_toolbar_button("删除", self.on_delete)

        # EN: Main paned window.
        # ZH: 主分隔窗格。
        self.paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1a1a2e")
        self.paned.pack(fill=tk.BOTH, expand=True)

        # EN: Left: tree frame.
        # ZH: 左侧：树形框架。
        self.tree_frame = tk.Frame(self.paned, bg="#1a1a2e")
        self.paned.add(self.tree_frame, minsize=300)

        # EN: Right: details frame.
        # ZH: 右侧：详情框架。
        self.details_frame = tk.Frame(self.paned, bg="#1a1a2e")
        self.paned.add(self.details_frame, minsize=400)

        # EN: Search box above tree.
        # ZH: 树上方搜索框。
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search)
        search_entry = tk.Entry(self.tree_frame, textvariable=self.search_var, bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
        search_entry.pack(fill=tk.X, padx=5, pady=5)

    def _add_toolbar_button(self, text, command):
        btn = tk.Button(
            self.toolbar,
            text=text,
            command=command,
            bg="#0f3460",
            fg="#FFFFFF",
            activebackground="#1a4b8c",
            activeforeground="#FFFFFF",
            font=("Microsoft YaHei", 10),
            relief=tk.FLAT,
            padx=10,
        )
        btn.pack(side=tk.LEFT, padx=5, pady=5)

    def _add_separator(self):
        tk.Frame(self.toolbar, bg="#555555", width=2).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=8)

    def _on_search(self, *args):
        """EN: Override in subclass to filter tree.
           ZH: 在子类中覆盖以实现树过滤。"""
        pass

    def get_full_path(self):
        if self.JSON_PATH:
            return DATA_DIR / self.JSON_PATH
        return None

    def load_data(self):
        """EN: Load JSON data. Override _parse_data to transform.
           ZH: 加载 JSON 数据。覆盖 _parse_data 进行转换。"""
        path = self.get_full_path()
        if path:
            self.data = load_json(path, default=self._default_data())
        else:
            self.data = self._default_data()
        self._parse_data()
        self._refresh_tree()
        self.app.set_status(f"已加载: {self.JSON_PATH}")

    def save_data(self):
        """EN: Save JSON data. Override _prepare_data to transform back.
           ZH: 保存 JSON 数据。覆盖 _prepare_data 进行反向转换。"""
        path = self.get_full_path()
        if not path:
            return
        self._prepare_data()
        save_json(path, self.data)
        self.app.set_status(f"已保存: {self.JSON_PATH}")

    def _default_data(self):
        """EN: Return default data structure when file is missing.
           ZH: 文件缺失时返回默认数据结构。"""
        return []

    def _parse_data(self):
        """EN: Post-load hook.
           ZH: 加载后钩子。"""
        pass

    def _prepare_data(self):
        """EN: Pre-save hook.
           ZH: 保存前钩子。"""
        pass

    def _refresh_tree(self):
        """EN: Override in subclass to refresh tree view.
           ZH: 在子类中覆盖以刷新树视图。"""
        pass

    def on_add(self):
        """EN: Override in subclass.
           ZH: 在子类中覆盖。"""
        pass

    def on_delete(self):
        """EN: Override in subclass.
           ZH: 在子类中覆盖。"""
        pass

    def confirm_delete(self, name):
        """EN: Show delete confirmation dialog.
           ZH: 显示删除确认对话框。"""
        return messagebox.askyesno("确认删除", f"确定要删除 '{name}' 吗？此操作不可撤销。")
