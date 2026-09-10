# Mod 翻译目录

本 Mod 的翻译文件放在这里，与 Mod 源码同址管理，**不要**放进 `game/tl/`。

```
game/custom/mods/<Mod名称>/
├── <mod源码>.rpy
└── tl/
    └── chinese_simplified/          # 本目录：该 Mod 的简体中文翻译
```

## 生成方法

在 Ren'Py SDK / 项目根目录执行：

```
python Brothel_King.py . translate chinese_simplified
```

Ren'Py 会把 `game/` 下所有文件的待译文本生成到 `game/tl/chinese_simplified/` 镜像路径。
Mod 的文件对应生成到 `game/tl/chinese_simplified/custom/mods/<Mod名称>/`，
**生成后请把属于本 Mod 的 .rpy 移回本目录**（Ren'Py 从 game/ 任意位置加载
translate 块，移回后效果相同，且翻译随 Mod 一起分发）。

也可以直接在 Mod 目录内手写 translate 块（以官方 `generate` 产出的块 ID 为准）。
