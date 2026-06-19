# -*- coding: utf-8 -*-
"""
BK Girl Pack Editor — Main Application
EN: Notebook-based editor for girl packs.
ZH: 基于 Notebook 的女孩包编辑器。
"""

import tkinter as tk
from tkinter import ttk, filedialog

from bk_editor.girl_pack_editor.tabs.image_tagger import ImageTaggerTab
from bk_editor.girl_pack_editor.tabs.ini_editor import INIEditorTab
from bk_editor.girl_pack_editor.tabs.trait_creator import TraitCreatorTab
from bk_editor.girl_pack_editor.tabs.pack_validator import PackValidatorTab
from bk_editor.shared import GIRLS_DIR


class GirlPackEditorApp:
    """EN: Main girl pack editor window.
       ZH: 女孩包编辑器主窗口。"""

    def __init__(self, root):
        self.root = root
        self.root.title("BK Girl Pack Editor — 女孩包编辑器")
        self.root.geometry("1500x950")
        self.root.minsize(1200, 800)
        self.root.configure(bg="#1a1a2e")

        # EN: Top toolbar with pack selector.
        # ZH: 顶部工具栏，含包选择器。
        self.toolbar = tk.Frame(root, bg="#16213e", height=45)
        self.toolbar.pack(fill=tk.X, pady=(0, 5))
        self.toolbar.pack_propagate(False)

        tk.Label(
            self.toolbar,
            text="当前女孩包:",
            bg="#16213e",
            fg="#FFFFFF",
            font=("Microsoft YaHei", 11),
        ).pack(side=tk.LEFT, padx=(10, 5), pady=8)

        self.pack_var = tk.StringVar()
        self.pack_combo = ttk.Combobox(
            self.toolbar,
            textvariable=self.pack_var,
            state="readonly",
            width=40,
            font=("Microsoft YaHei", 11),
        )
        self.pack_combo.pack(side=tk.LEFT, padx=5, pady=8)
        self.pack_combo.bind("<<ComboboxSelected>>", self._on_pack_changed)

        tk.Button(
            self.toolbar,
            text="浏览…",
            command=self._browse_pack,
            bg="#0f3460",
            fg="#FFFFFF",
            font=("Microsoft YaHei", 10),
            relief=tk.FLAT,
        ).pack(side=tk.LEFT, padx=5, pady=8)

        tk.Button(
            self.toolbar,
            text="刷新",
            command=self._refresh_packs,
            bg="#0f3460",
            fg="#FFFFFF",
            font=("Microsoft YaHei", 10),
            relief=tk.FLAT,
        ).pack(side=tk.LEFT, padx=5, pady=8)

        # EN: Notebook with tabs.
        # ZH: 带标签页的 Notebook。
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self._add_tab("图片打标", ImageTaggerTab)
        self._add_tab("_BK.ini 编辑", INIEditorTab)
        self._add_tab("Trait/Perk 创建", TraitCreatorTab)
        self._add_tab("包验证", PackValidatorTab)

        # EN: Status bar.
        # ZH: 状态栏。
        self.status = tk.Label(
            root,
            text="就绪 — 请选择一个女孩包",
            font=("Microsoft YaHei", 10),
            bg="#16213e",
            fg="#FFFFFF",
            anchor=tk.W,
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM, ipady=4)

        self._refresh_packs()

    def _add_tab(self, title, tab_class):
        frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(frame, text=title)
        editor = tab_class(frame, self)
        editor.pack(fill=tk.BOTH, expand=True)

    @property
    def current_pack_path(self):
        name = self.pack_var.get()
        if not name:
            return None
        return GIRLS_DIR / name

    def _refresh_packs(self):
        packs = []
        if GIRLS_DIR.exists():
            packs = sorted([p.name for p in GIRLS_DIR.iterdir() if p.is_dir()])
        self.pack_combo["values"] = packs
        if packs and not self.pack_var.get():
            self.pack_var.set(packs[0])
            self._notify_pack_changed()

    def _browse_pack(self):
        path = filedialog.askdirectory(initialdir=str(GIRLS_DIR), parent=self.root)
        if not path:
            return
        path = Path(path)
        if GIRLS_DIR in path.parents or path == GIRLS_DIR:
            name = path.name
            if name not in self.pack_combo["values"]:
                self._refresh_packs()
            self.pack_var.set(name)
            self._notify_pack_changed()
        else:
            self.set_status("请选择 game/custom/girls/ 下的文件夹")

    def _on_pack_changed(self, event=None):
        self._notify_pack_changed()

    def _notify_pack_changed(self):
        path = self.current_pack_path
        self.set_status(f"已切换包: {path.name if path else '无'}")
        for tab in self.notebook.winfo_children():
            for child in tab.winfo_children():
                if hasattr(child, "on_pack_changed"):
                    child.on_pack_changed(path)

    def set_status(self, text):
        self.status.config(text=text)
