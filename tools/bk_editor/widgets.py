# -*- coding: utf-8 -*-
"""
BK Editor — Shared Widgets (Compatibility Layer)
EN: Re-exports widgets from bk_editor.shared for backward compatibility.
    New code should import from bk_editor.shared directly.
ZH: 为兼容旧代码而从 bk_editor.shared 重新导出组件。
    新代码应直接从 bk_editor.shared 导入。
"""

from bk_editor.shared.widgets import (
    LabeledEntry,
    LabeledSpinbox,
    LabeledCombobox,
    LabeledCheckbox,
    EffectEditor,
    JsonTreeview,
)
