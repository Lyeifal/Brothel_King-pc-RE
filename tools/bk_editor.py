#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BK Editor — Main Entry Point
EN: Visual editor for Brothel King Evolution content.
ZH: 青楼之王 Evolution 内容可视化编辑器。

Usage:
    python tools/bk_editor.py
"""

import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path

# EN: Add project root to path so bk_editor package can be imported.
# ZH: 将项目根目录加入路径以便导入 bk_editor 包。
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from bk_editor import core
from bk_editor.scenario_editor import ScenarioEditorFrame
from bk_editor.story_editor import StoryEditorFrame
from bk_editor.origin_editor import OriginEditorFrame
from bk_editor.girl_editor import GirlEditorFrame
from bk_editor.pack_editor import PackEditorFrame


class BKEditorApp:
    """EN: Main application window with Notebook tabs for each editor.
       ZH: 主应用窗口，用 Notebook 标签页组织各编辑器。"""

    def __init__(self, root):
        self.root = root
        self.root.title("BK Evolution 编辑器")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)

        # EN: Set a dark theme-like background.
        # ZH: 设置深色主题背景。
        self.root.configure(bg="#1a1a2e")

        # EN: Title bar.
        # ZH: 标题栏。
        title = tk.Label(
            root,
            text="BK Evolution 内容编辑器",
            font=("Microsoft YaHei", 20, "bold"),
            bg="#1a1a2e",
            fg="#FFD700",
        )
        title.pack(pady=(10, 5))

        subtitle = tk.Label(
            root,
            text=f"项目路径: {core.find_project_root()}",
            font=("Microsoft YaHei", 10),
            bg="#1a1a2e",
            fg="#AAAAAA",
        )
        subtitle.pack(pady=(0, 10))

        # EN: Notebook with editor tabs.
        # ZH: 带编辑器标签页的 Notebook。
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # EN: Create tabs.
        # ZH: 创建标签页。
        self._add_tab("剧本编辑器", ScenarioEditorFrame)
        self._add_tab("剧情事件", StoryEditorFrame)
        self._add_tab("出身编辑", OriginEditorFrame)
        self._add_tab("女孩系统", GirlEditorFrame)
        self._add_tab("女孩包工具", PackEditorFrame)

        # EN: Status bar.
        # ZH: 状态栏。
        self.status = tk.Label(
            root,
            text="就绪",
            font=("Microsoft YaHei", 10),
            bg="#16213e",
            fg="#FFFFFF",
            anchor=tk.W,
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM, ipady=4)

    def _add_tab(self, title, frame_class):
        """EN: Add a new tab with the given editor frame class.
           ZH: 添加一个包含指定编辑器框架类的新标签页。"""
        frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(frame, text=title)
        editor = frame_class(frame, self)
        editor.pack(fill=tk.BOTH, expand=True)

    def set_status(self, text):
        """EN: Update status bar text.
           ZH: 更新状态栏文字。"""
        self.status.config(text=text)


def main():
    root = tk.Tk()
    app = BKEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
