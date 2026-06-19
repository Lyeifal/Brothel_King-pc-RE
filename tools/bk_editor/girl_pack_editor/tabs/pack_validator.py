# -*- coding: utf-8 -*-
"""
BK Girl Pack Editor — Pack Validator Tab
EN: Validate girl pack completeness and report issues with auto-fix hints.
ZH: 验证女孩包完整性并生成报告，支持一键修复提示。
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from bk_editor.shared import DATA_DIR, GIRLS_DIR


class PackValidatorTab(tk.Frame):
    """EN: Validate selected girl pack.
       ZH: 验证选中的女孩包。"""

    IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.pack_path = None
        self._build_ui()

    def _build_ui(self):
        header = tk.Label(
            self,
            text="女孩包验证器",
            bg="#1a1a2e",
            fg="#FFFFFF",
            font=("Microsoft YaHei", 14, "bold"),
        )
        header.pack(anchor=tk.W, padx=10, pady=10)

        btn_frame = tk.Frame(self, bg="#1a1a2e")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="运行验证", command=self._run_validation, bg="#0f3460", fg="#FFFFFF", font=("Microsoft YaHei", 11), relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="一键修复", command=self._auto_fix, bg="#660000", fg="#FFFFFF", font=("Microsoft YaHei", 11), relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

        self.result_text = tk.Text(
            self,
            bg="#1a1a2e",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            font=("Consolas", 10),
            wrap=tk.WORD,
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        sb = ttk.Scrollbar(self, command=self.result_text.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.configure(yscrollcommand=sb.set)

        self.result_text.insert(tk.END, "点击“运行验证”开始检查当前女孩包。\n")

    def on_pack_changed(self, path):
        self.pack_path = path
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"已切换包: {path.name if path else '无'}\n")

    def _run_validation(self):
        if not self.pack_path or not self.pack_path.exists():
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "错误: 未选择有效的女孩包。\n")
            return
        issues = self._validate(self.pack_path)
        self.result_text.delete("1.0", tk.END)
        if not issues:
            self.result_text.insert(tk.END, "✅ 未发现严重问题。女孩包看起来健康。\n")
        else:
            self.result_text.insert(tk.END, f"发现 {len(issues)} 个问题:\n\n")
            for level, msg in issues:
                icon = "🔴" if level == "error" else "🟡"
                self.result_text.insert(tk.END, f"{icon} [{level.upper()}] {msg}\n")
        self.app.set_status(f"验证完成: {len(issues)} 个问题")

    def _validate(self, pack_path):
        issues = []
        files = list(pack_path.iterdir())
        images = [f for f in files if f.suffix.lower() in self.IMAGE_EXTS]

        # EN: Check required tags via filename.
        # ZH: 检查文件名中是否包含 portrait/profile 标签。
        lower_names = [f.name.lower() for f in images]
        has_portrait = any("portrait" in n for n in lower_names)
        has_profile = any("profile" in n for n in lower_names)
        if not has_portrait:
            issues.append(("error", "缺少 portrait 图片（文件名需包含 'portrait'）"))
        if not has_profile:
            issues.append(("error", "缺少 profile 图片（文件名需包含 'profile'）"))

        # EN: Check _BK.ini existence and parse.
        # ZH: 检查 _BK.ini 是否存在并解析。
        ini_path = pack_path / "_BK.ini"
        if ini_path.exists():
            try:
                import configparser
                cfg = configparser.ConfigParser()
                cfg.read(ini_path, encoding="utf-8")
                issues += self._validate_ini(cfg)
            except Exception as e:
                issues.append(("error", f"_BK.ini 解析失败: {e}"))
        else:
            issues.append(("warning", "未找到 _BK.ini，将使用默认生成参数"))

        # EN: Check for duplicate image basenames.
        # ZH: 检查重复图片基名。
        from collections import Counter
        basenames = Counter(f.stem for f in images)
        dupes = {k: v for k, v in basenames.items() if v > 1}
        for name, count in dupes.items():
            issues.append(("warning", f"发现 {count} 个同名图片: {name}"))

        # EN: Check no images in subfolders? Some packs allow it; just warn.
        # ZH: 子文件夹中的图片仅警告。
        sub_images = []
        for sub in pack_path.iterdir():
            if sub.is_dir():
                sub_images.extend([f for f in sub.iterdir() if f.suffix.lower() in self.IMAGE_EXTS])
        if sub_images:
            issues.append(("warning", f"子文件夹中发现 {len(sub_images)} 张图片，可能未被游戏读取"))

        return issues

    def _validate_ini(self, cfg):
        issues = []
        known_sections = {"identity", "base skills", "ranking", "personality", "background", "traits", "custom", "exclude"}

        # EN: Load known traits/personalities from JSON.
        # ZH: 从 JSON 加载已知 trait/personality。
        trait_ids = self._load_trait_ids()
        personality_ids = self._load_personality_ids()

        if "traits" in cfg.sections():
            for key in cfg["traits"]:
                val = cfg["traits"][key].strip()
                if val and val not in trait_ids:
                    issues.append(("error", f"_BK.ini [traits] 引用未知 trait: '{val}'"))

        if "personality" in cfg.sections():
            for key in cfg["personality"]:
                val = cfg["personality"][key].strip()
                if val and val not in personality_ids:
                    issues.append(("error", f"_BK.ini [personality] 引用未知 personality: '{val}'"))

        for sec in cfg.sections():
            if sec.lower() not in known_sections:
                issues.append(("warning", f"_BK.ini 包含未知 section: [{sec}]"))

        return issues

    def _load_trait_ids(self):
        try:
            import json
            data = json.loads((DATA_DIR / "traits" / "traits.json").read_text(encoding="utf-8"))
            return {it.get("id") for it in data if it.get("id")}
        except Exception:
            return set()

    def _load_personality_ids(self):
        try:
            import json
            data = json.loads((DATA_DIR / "personalities" / "personalities.json").read_text(encoding="utf-8"))
            return {it.get("id") for it in data if it.get("id")}
        except Exception:
            return set()

    def _auto_fix(self):
        if not self.pack_path or not self.pack_path.exists():
            messagebox.showerror("错误", "未选择有效的女孩包", parent=self)
            return
        fixes = []
        images = [f for f in self.pack_path.iterdir() if f.suffix.lower() in self.IMAGE_EXTS]
        lower_names = [f.name.lower() for f in images]

        if not any("portrait" in n for n in lower_names):
            # EN: Rename the first image containing 'face' or just the first image to portrait.
            # ZH: 将第一张包含 'face' 的图片或第一张图片重命名为 portrait。
            candidate = next((f for f in images if "face" in f.name.lower()), images[0] if images else None)
            if candidate:
                new_name = f"portrait{candidate.suffix}"
                candidate.rename(self.pack_path / new_name)
                fixes.append(f"重命名 {candidate.name} → {new_name}")

        if not any("profile" in n for n in lower_names):
            candidate = next((f for f in images if "body" in f.name.lower() or "stand" in f.name.lower()), None)
            if candidate:
                new_name = f"profile{candidate.suffix}"
                candidate.rename(self.pack_path / new_name)
                fixes.append(f"重命名 {candidate.name} → {new_name}")

        self.result_text.delete("1.0", tk.END)
        if fixes:
            self.result_text.insert(tk.END, "已执行以下自动修复:\n\n")
            for f in fixes:
                self.result_text.insert(tk.END, f"🔧 {f}\n")
        else:
            self.result_text.insert(tk.END, "无需自动修复。\n")
        self.app.set_status("一键修复完成")
