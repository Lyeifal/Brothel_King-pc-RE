# -*- coding: utf-8 -*-
"""
BK Girl Pack Editor — Image Tagger Tab (Enhanced)
EN: Button-based image tagging with multi-select, scenario validation, and typo checking.
ZH: 基于按钮的图片打标，支持多选、场景验证与拼写检查。
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import re

from bk_editor.shared import GAME_DIR


# ========================================================================
# 1. TAG DATA
# ========================================================================

def _load_tag_patterns():
    """Parse _tag_dict_data from settings.rpy into {pattern: [tags]}."""
    patterns = {}
    settings_path = GAME_DIR / "core" / "init" / "settings.rpy"
    if not settings_path.exists():
        return patterns
    text = settings_path.read_text(encoding="utf-8")
    m = re.search(r"_tag_dict_data\s*=\s*\{(.*?)\n\s*\}", text, re.DOTALL)
    if not m:
        return patterns
    body = m.group(1)
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        tm = re.match(r'"([^"]+)"\s*:\s*\(([^)]+)\)', line)
        if tm:
            key = tm.group(1)
            values = re.findall(r'"([^"]+)"', tm.group(2))
            patterns.setdefault(key, []).extend(values)
            continue
        sm = re.match(r'"([^"]+)"\s*:\s*__\(\s*"([^"]+)"\s*\)', line)
        if not sm:
            sm = re.match(r'"([^"]+)"\s*:\s*"([^"]+)"', line)
        if sm:
            key, val = sm.group(1), sm.group(2)
            patterns.setdefault(key, []).append(val)
    return patterns


TAG_PATTERNS = _load_tag_patterns()
TAG_ORDER = sorted(TAG_PATTERNS.keys(), key=lambda x: -len(x))

# tag -> [patterns] reverse mapping
TAG_TO_PATTERNS = {}
for pattern, tags in TAG_PATTERNS.items():
    for tag in tags:
        TAG_TO_PATTERNS.setdefault(tag, []).append(pattern)

# Organized categories for the button palette
TAG_CATEGORIES = {
    "频率": ["freq_highest", "freq_high", "freq_low", "freq_lowest", "xq", "hq", "lq"],
    "肖像/资料": ["portrait", "profile", "market", "beauty", "card", "model", "advertise", "quest", "shop", "battle", "fight", "combat", "hurt", "gallery"],
    "情绪": ["happy", "neutral", "sad", "refuse"],
    "休息/工作": ["rest", "ecchi", "wait", "bunny", "maid", "danc", "run", "sing", "strip", "mass", "swim", "geisha", "etiquette", "kimono", "date"],
    "裸露": ["naked", "nude"],
    "地点": ["public", "beach", "nature", "town", "city"],
    "侍奉": ["service", "mast", "oral", "blowjob", "bj", "cunnilingus", "hand", "titj", "ttj", "tits", "titty"],
    "性交": ["sex", "fuck", "xxx"],
    "肛交": ["anal"],
    "调教": ["fetish", "bdsm", "bondage", "hardcore", "foot", "fj"],
    "多人/特殊": ["group", "bis", "bisexual", "les", "beast", "best", "big", "stallion", "toy", "machine", "monster", "tent"],
    "农场": ["libido", "obedience", "sensitivity", "constitution"],
    "癖好": ["cosplay", "dild", "vibr", "plug", "dirty", "penis w", "penisw", "penis_w", "penis-w", "oil", "wet", "sub", "humiliat", "master", "dom", "gag", "strap", "role", "bead", "irru", "deep", "dt", "double", "finger", "fist", "insults", "sixty", "watersp", "enema", "kiss", "spank", "rim", "grop", "fondl", "lact", "doggy", "cowg", "pile", "spoon"],
    "射精/高潮": ["cum", "buk", "cim", "mouth", "cif", "cof", "face", "cih", "coh", "hair", "cob", "body", "shower", "swa", "cream", "cin", "inside", "orgasm", "denied", "squirt"],
    "未使用": ["death", "preg"],
}

# Scenario requirements: what TAGS the game looks for in each context
SCENARIO_REQUIREMENTS = [
    {"name": "基础必须", "required": {"portrait", "profile"}, "optional": {"market", "model", "beauty", "card", "quest", "shop"}, "desc": "每个女孩包必须至少包含 portrait 和 profile"},
    {"name": "休息", "required": set(), "optional": {"rest", "libido"}, "desc": "女孩休息时使用的图片"},
    {"name": "工作- waitress", "required": set(), "optional": {"waitress", "bunny", "maid"}, "desc": "女服务员工作"},
    {"name": "工作- dancer", "required": set(), "optional": {"dancer", "dance", "sing", "strip"}, "desc": "脱衣舞娘工作"},
    {"name": "工作- masseuse", "required": set(), "optional": {"masseuse", "swimsuit", "swim"}, "desc": "按摩技师工作"},
    {"name": "工作- geisha", "required": set(), "optional": {"geisha", "kimono", "date"}, "desc": "艺妓工作"},
    {"name": "性行为- service", "required": set(), "optional": {"service", "mast", "oral", "cunni", "handjob", "titjob"}, "desc": "侍奉/口交/手淫等"},
    {"name": "性行为- sex", "required": set(), "optional": {"sex"}, "desc": "正常性交"},
    {"name": "性行为- anal", "required": set(), "optional": {"anal"}, "desc": "肛交"},
    {"name": "性行为- fetish", "required": set(), "optional": {"fetish", "bondage", "footjob", "hardcore"}, "desc": "调教/癖好"},
    {"name": "性行为- group", "required": set(), "optional": {"group", "bisexual", "lesbian"}, "desc": "群交/双性/女同"},
    {"name": "农场", "required": set(), "optional": {"libido", "obedience", "sensitivity", "constitution"}, "desc": "农场训练"},
    {"name": "农场- 特殊", "required": set(), "optional": {"beast", "monster", "machine", "big"}, "desc": "农场特殊训练"},
    {"name": "情绪", "required": set(), "optional": {"happy", "neutral", "sad", "refuse"}, "desc": "对话中的情绪表现"},
    {"name": "战斗", "required": set(), "optional": {"fight", "hurt"}, "desc": "战斗/受伤场景"},
    {"name": "公共场合", "required": set(), "optional": {"public", "beach", "nature", "town"}, "desc": "公开场合/地点"},
    {"name": "处女", "required": set(), "optional": {"virgin"}, "desc": "破处事件"},
    {"name": "画廊", "required": set(), "optional": {"gallery"}, "desc": "CG画廊背景"},
    {"name": "射精/高潮", "required": set(), "optional": {"cumshot", "cim", "cof", "cih", "cob", "cin", "creampie", "buk", "orgasm", "squirt", "denied"}, "desc": "性行为结束"},
]

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".avif"}
VIDEO_EXTS = {".webm", ".mkv", ".avi", ".mpg", ".mpeg"}
ALL_MEDIA_EXTS = IMAGE_EXTS | VIDEO_EXTS


# ========================================================================
# 2. HELPER FUNCTIONS
# ========================================================================

def add_pattern_to_filename(filename, pattern):
    stem, ext = Path(filename).stem, Path(filename).suffix
    if pattern.lower() not in stem.lower():
        return f"{stem}_{pattern}{ext}"
    return filename


def remove_pattern_from_filename(filename, pattern):
    stem, ext = Path(filename).stem, Path(filename).suffix
    new_stem = re.sub(rf'[_\-]?{re.escape(pattern)}[_\-]?', '_', stem, flags=re.IGNORECASE)
    new_stem = re.sub(r'_+', '_', new_stem).strip('_')
    return f"{new_stem}{ext}"


def _levenshtein(a, b):
    """Simple Levenshtein distance."""
    if len(a) < len(b):
        return _levenshtein(b, a)
    if len(b) == 0:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(curr[-1] + 1, prev[j + 1] + 1, prev[j] + (0 if ca == cb else 1)))
        prev = curr
    return prev[-1]


def detect_tags(filename):
    lower = Path(filename).stem.lower()
    tags = []
    matched = set()
    for pattern in TAG_ORDER:
        if pattern in lower:
            for tag in TAG_PATTERNS[pattern]:
                if tag not in matched:
                    tags.append(tag)
                    matched.add(tag)
    return tags


# ========================================================================
# 3. UI CLASS
# ========================================================================

class ImageTaggerTab(tk.Frame):
    """Button-based image tagger with multi-select, validation, and scenario coverage."""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.pack_path = None
        self.images = []  # list of Path objects
        self.photo = None
        self._remove_mode = False
        self._build_ui()

    def _build_ui(self):
        # Main vertical layout: top paned area + bottom validation area
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        top_paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1a1a2e", sashwidth=6)
        top_paned.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

        # --- LEFT: File list ---
        left_frame = tk.Frame(top_paned, bg="#16213e", width=280)
        left_frame.pack_propagate(False)
        top_paned.add(left_frame, minsize=250)

        tk.Label(left_frame, text="图片文件 (Ctrl/Shift 多选)", bg="#16213e", fg="#FFFFFF",
                 font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=5)

        list_btn_frame = tk.Frame(left_frame, bg="#16213e")
        list_btn_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Button(list_btn_frame, text="全选", command=self._select_all, bg="#0f3460", fg="#FFFFFF",
                  relief=tk.FLAT, font=("Microsoft YaHei", 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(list_btn_frame, text="全不选", command=self._select_none, bg="#0f3460", fg="#FFFFFF",
                  relief=tk.FLAT, font=("Microsoft YaHei", 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(list_btn_frame, text="刷新", command=self._refresh_file_list, bg="#0f3460", fg="#FFFFFF",
                  relief=tk.FLAT, font=("Microsoft YaHei", 9)).pack(side=tk.LEFT, padx=2)

        tree_frame = tk.Frame(left_frame, bg="#16213e")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.file_tree = ttk.Treeview(tree_frame, columns=["tags"], show="tree headings", selectmode="extended",
                                      style="Dev.Treeview")
        self.file_tree.heading("#0", text="文件名")
        self.file_tree.heading("tags", text="当前标签")
        self.file_tree.column("#0", width=160)
        self.file_tree.column("tags", width=180)
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_tree.bind("<<TreeviewSelect>>", self._on_file_select)
        sb = ttk.Scrollbar(tree_frame, command=self.file_tree.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_tree.configure(yscrollcommand=sb.set)

        self.file_stats = tk.Label(left_frame, text="", bg="#16213e", fg="#AAAAAA", font=("Microsoft YaHei", 10))
        self.file_stats.pack(anchor=tk.W, padx=5, pady=2)

        # --- CENTER: Preview + actions ---
        center_frame = tk.Frame(top_paned, bg="#1a1a2e", width=450)
        center_frame.pack_propagate(False)
        top_paned.add(center_frame, minsize=400)

        tk.Label(center_frame, text="图片预览", bg="#1a1a2e", fg="#FFFFFF",
                 font=("Microsoft YaHei", 12, "bold")).pack(anchor=tk.W, padx=5, pady=5)

        self.preview_label = tk.Label(center_frame, bg="#1a1a2e")
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.selection_info = tk.Label(center_frame, text="未选择", bg="#1a1a2e", fg="#FFD700",
                                       font=("Microsoft YaHei", 10, "bold"), wraplength=400)
        self.selection_info.pack(anchor=tk.W, padx=5, pady=2)

        action_frame = tk.Frame(center_frame, bg="#1a1a2e")
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        self.remove_mode_var = tk.BooleanVar(value=False)
        tk.Checkbutton(action_frame, text="移除模式 (点击按钮移除标签)", variable=self.remove_mode_var,
                       bg="#1a1a2e", fg="#FFFFFF", selectcolor="#333333",
                       font=("Microsoft YaHei", 10), activebackground="#1a1a2e", activeforeground="#FFFFFF"
                       ).pack(side=tk.LEFT, padx=2)

        # --- RIGHT: Tag palette ---
        right_frame = tk.Frame(top_paned, bg="#16213e", width=420)
        right_frame.pack_propagate(False)
        top_paned.add(right_frame, minsize=380)

        tk.Label(right_frame, text="标签面板 (点击添加到选中图片)", bg="#16213e", fg="#FFFFFF",
                 font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=5)

        self.tag_notebook = ttk.Notebook(right_frame, style="Dev.TNotebook")
        self.tag_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._build_tag_palette()

        # --- BOTTOM: Validation report ---
        bottom_frame = tk.Frame(self, bg="#16213e")
        bottom_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        bottom_frame.rowconfigure(0, weight=1)
        bottom_frame.columnconfigure(0, weight=3)
        bottom_frame.columnconfigure(1, weight=2)

        # Validation text
        val_frame = tk.Frame(bottom_frame, bg="#16213e")
        val_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        tk.Label(val_frame, text="验证报告", bg="#16213e", fg="#FFFFFF",
                 font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=2)
        val_btn_frame = tk.Frame(val_frame, bg="#16213e")
        val_btn_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Button(val_btn_frame, text="运行验证", command=self._run_validation,
                  bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT, font=("Microsoft YaHei", 10)).pack(side=tk.LEFT, padx=2)
        tk.Button(val_btn_frame, text="一键重命名 (去重+整理)", command=self._batch_cleanup,
                  bg="#0f3460", fg="#FFFFFF", relief=tk.FLAT, font=("Microsoft YaHei", 10)).pack(side=tk.LEFT, padx=2)

        self.val_text = tk.Text(val_frame, bg="#1a1a2e", fg="#FFFFFF", insertbackground="#FFFFFF",
                                font=("Consolas", 10), wrap=tk.WORD, height=8)
        self.val_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        vsb = ttk.Scrollbar(val_frame, command=self.val_text.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.val_text.configure(yscrollcommand=vsb.set)

        # Scenario coverage
        cov_frame = tk.Frame(bottom_frame, bg="#16213e")
        cov_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        tk.Label(cov_frame, text="场景覆盖", bg="#16213e", fg="#FFFFFF",
                 font=("Microsoft YaHei", 11, "bold")).pack(anchor=tk.W, padx=5, pady=2)
        self.cov_tree = ttk.Treeview(cov_frame, columns=["status"], show="tree headings", style="Dev.Treeview")
        self.cov_tree.heading("#0", text="场景")
        self.cov_tree.heading("status", text="状态")
        self.cov_tree.column("#0", width=140)
        self.cov_tree.column("status", width=100)
        self.cov_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _build_tag_palette(self):
        """Build category tabs with pattern buttons."""
        self.tag_buttons = []
        for category, patterns in TAG_CATEGORIES.items():
            tab = tk.Frame(self.tag_notebook, bg="#1a1a2e")
            self.tag_notebook.add(tab, text=category)

            canvas = tk.Canvas(tab, bg="#1a1a2e", highlightthickness=0)
            scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
            btn_frame = tk.Frame(canvas, bg="#1a1a2e")
            btn_frame.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
            canvas.create_window((0, 0), window=btn_frame, anchor=tk.NW, width=360)
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            row, col = 0, 0
            for pattern in patterns:
                if pattern not in TAG_PATTERNS:
                    continue
                tags = TAG_PATTERNS[pattern]
                tag_text = ", ".join(tags[:2]) + ("…" if len(tags) > 2 else "")
                btn = tk.Button(
                    btn_frame,
                    text=f"{pattern}\n({tag_text})",
                    command=lambda p=pattern: self._on_tag_button(p),
                    bg="#0f3460",
                    fg="#FFFFFF",
                    font=("Microsoft YaHei", 8),
                    relief=tk.FLAT,
                    width=12,
                    height=2,
                )
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
                self.tag_buttons.append((btn, pattern))
                col += 1
                if col >= 3:
                    col = 0
                    row += 1

    def on_pack_changed(self, path):
        self.pack_path = path
        self._refresh_file_list()
        self._clear_preview()
        self.val_text.delete("1.0", tk.END)
        self.val_text.insert(tk.END, "切换包后请点击“运行验证”。\n")

    def _refresh_file_list(self):
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        self.images = []
        if not self.pack_path or not self.pack_path.exists():
            self.file_stats.config(text="")
            return
        for f in sorted(self.pack_path.iterdir()):
            if f.is_file() and f.suffix.lower() in ALL_MEDIA_EXTS:
                self.images.append(f)
                tags = detect_tags(f.name)
                tag_str = ", ".join(tags) if tags else "—"
                self.file_tree.insert("", tk.END, text=f.name, values=(tag_str,))
        self.file_stats.config(text=f"共 {len(self.images)} 张图片")

    def _select_all(self):
        for item in self.file_tree.get_children():
            self.file_tree.selection_add(item)

    def _select_none(self):
        self.file_tree.selection_remove(self.file_tree.selection())

    def _on_file_select(self, event=None):
        selected = self.file_tree.selection()
        if not selected:
            self.selection_info.config(text="未选择")
            self._clear_preview()
            return

        if len(selected) == 1:
            name = self.file_tree.item(selected[0], "text")
            path = self.pack_path / name
            self.selection_info.config(text=f"选中: {name}")
            self._show_preview(path)
        else:
            names = [self.file_tree.item(i, "text") for i in selected]
            self.selection_info.config(text=f"批量选中: {len(selected)} 张")
            # Preview first selected
            path = self.pack_path / names[0]
            self._show_preview(path)

    def _clear_preview(self):
        self.preview_label.config(image="", text="未选择图片")
        self.photo = None

    def _show_preview(self, path):
        try:
            from PIL import Image, ImageTk
            if path.suffix.lower() in VIDEO_EXTS:
                img = self._extract_video_frame(path)
            else:
                img = Image.open(path)
            img.thumbnail((420, 560))
            self.photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=self.photo, text="")
        except Exception as e:
            self.preview_label.config(image="", text=f"无法预览\n{path.name}\n{path.suffix}\n({e})")

    def _extract_video_frame(self, path):
        """Extract a frame from video using OpenCV (no external ffmpeg needed)."""
        import cv2
        from PIL import Image
        cap = cv2.VideoCapture(str(path))
        if not cap.isOpened():
            raise RuntimeError(f"无法打开视频: {path.name}")
        # Seek to ~0.5s to avoid black first frame
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(fps * 0.5))
        ret, frame = cap.read()
        cap.release()
        if not ret:
            raise RuntimeError(f"无法读取视频帧: {path.name}")
        # OpenCV uses BGR, PIL uses RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(frame_rgb)

    def _on_tag_button(self, pattern):
        selected = self.file_tree.selection()
        if not selected:
            self.app.set_status("请先选择至少一张图片")
            return
        remove = self.remove_mode_var.get()
        changed = 0
        for item in selected:
            old_name = self.file_tree.item(item, "text")
            if remove:
                new_name = remove_pattern_from_filename(old_name, pattern)
            else:
                new_name = add_pattern_to_filename(old_name, pattern)
            if new_name != old_name:
                old_path = self.pack_path / old_name
                new_path = self.pack_path / new_name
                # Avoid collision
                counter = 1
                base_new = new_path.stem
                while new_path.exists() and new_path != old_path:
                    new_name = f"{base_new}_{counter}{new_path.suffix}"
                    new_path = self.pack_path / new_name
                    counter += 1
                try:
                    old_path.rename(new_path)
                    changed += 1
                except Exception as e:
                    self.app.set_status(f"重命名失败: {e}")
                    return
        self._refresh_file_list()
        action = "移除" if remove else "添加"
        self.app.set_status(f"{action} '{pattern}' 到 {len(selected)} 张图片 ({changed} 张变更)")

    def _run_validation(self):
        if not self.pack_path:
            return
        self.val_text.delete("1.0", tk.END)
        self.cov_tree.delete(*self.cov_tree.get_children())

        # Build tag coverage from all images
        all_tags = set()
        tag_counts = {}
        typo_issues = []
        for img in self.images:
            tags = detect_tags(img.name)
            for t in tags:
                all_tags.add(t)
                tag_counts[t] = tag_counts.get(t, 0) + 1
            typos = self._check_typos(img.name)
            for bad, suggestion in typos:
                typo_issues.append(f"  🔴 拼写疑似错误: '{bad}' 在 {img.name} 中 (建议: '{suggestion}')")

        lines = []
        lines.append("=" * 50)
        lines.append("验证报告")
        lines.append("=" * 50)

        # 1. Required tags
        has_portrait = "portrait" in all_tags
        has_profile = "profile" in all_tags
        if has_portrait:
            lines.append(f"✅ portrait: 已覆盖 ({tag_counts.get('portrait', 0)} 张)")
        else:
            lines.append("🔴 portrait: 缺失！每个女孩包必须至少包含一张 portrait 图片")
        if has_profile:
            lines.append(f"✅ profile: 已覆盖 ({tag_counts.get('profile', 0)} 张)")
        else:
            lines.append("🔴 profile: 缺失！每个女孩包必须至少包含一张 profile 图片")

        lines.append("")

        # 2. Typos
        if typo_issues:
            lines.append(f"⚠️  发现 {len(typo_issues)} 个潜在拼写错误:")
            lines.extend(typo_issues)
        else:
            lines.append("✅ 未发现明显拼写错误")

        lines.append("")

        # 3. Scenario coverage
        lines.append("场景覆盖详情:")
        for scenario in SCENARIO_REQUIREMENTS:
            name = scenario["name"]
            req = scenario["required"]
            opt = scenario["optional"]
            covered_req = req & all_tags if req else set()
            covered_opt = opt & all_tags if opt else set()

            if req and covered_req == req:
                status = "✅ 完全覆盖"
                cov_color = "#2ECC71"
            elif req:
                missing = req - covered_req
                status = f"🔴 缺少 {', '.join(missing)}"
                cov_color = "#E74C3C"
            elif opt and covered_opt:
                status = f"🟡 部分覆盖 ({len(covered_opt)}/{len(opt)})"
                cov_color = "#F39C12"
            elif opt:
                status = "⚪ 未覆盖"
                cov_color = "#AAAAAA"
            else:
                status = "✅"
                cov_color = "#2ECC71"

            lines.append(f"  {status} — {name}: {scenario['desc']}")
            if opt and not req:
                lines.append(f"      可选标签: {', '.join(sorted(opt))}")
                lines.append(f"      已覆盖: {', '.join(sorted(covered_opt)) or '无'}")

            self.cov_tree.insert("", tk.END, text=name, values=(status,))

        self.val_text.insert(tk.END, "\n".join(lines))
        self.app.set_status("验证完成")

    def _check_typos(self, filename):
        """Find potential typos in filename."""
        stem = Path(filename).stem.lower()
        words = set(re.findall(r'[a-z]{3,}', stem))
        typos = []
        for word in words:
            if word in TAG_PATTERNS:
                continue
            if len(word) >= 10:
                continue  # Likely part of a name
            best_pattern = None
            best_dist = 999
            for pattern in TAG_ORDER:
                if len(pattern) < 3:
                    continue
                dist = _levenshtein(word, pattern)
                if dist < best_dist:
                    best_dist = dist
                    best_pattern = pattern
            if best_dist <= 2 and best_pattern and abs(len(word) - len(best_pattern)) <= 2:
                typos.append((word, best_pattern))
        return typos

    def _batch_cleanup(self):
        """Rename all images to clean format: base_pattern1_pattern2.ext"""
        if not self.pack_path:
            return
        changed = 0
        for img in list(self.images):
            stem = img.stem
            lower_stem = stem.lower()
            # Extract base name (everything before first known tag pattern)
            first_tag_pos = len(stem)
            for pattern in TAG_ORDER:
                pos = lower_stem.find(pattern)
                if pos != -1 and pos < first_tag_pos:
                    first_tag_pos = pos
            base = stem[:first_tag_pos].rstrip("_- ") if first_tag_pos < len(stem) else stem
            # Collect all patterns found in filename
            patterns_found = [p for p in TAG_ORDER if p in lower_stem]
            tag_part = "_".join(patterns_found)
            if tag_part:
                new_name = f"{base}_{tag_part}{img.suffix}" if base else f"{tag_part}{img.suffix}"
            else:
                new_name = img.name
            # Clean up
            new_name = re.sub(r'_+', '_', new_name).strip('_')
            if new_name != img.name:
                new_path = self.pack_path / new_name
                counter = 1
                while new_path.exists():
                    new_name = f"{Path(new_name).stem}_{counter}{Path(new_name).suffix}"
                    new_path = self.pack_path / new_name
                    counter += 1
                try:
                    img.rename(new_path)
                    changed += 1
                except Exception:
                    pass
        self._refresh_file_list()
        self.app.set_status(f"一键整理完成: {changed} 张图片被重命名")
