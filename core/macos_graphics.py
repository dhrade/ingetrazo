# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""Qt graphics compatibility switches for older macOS Intel GPUs."""
from __future__ import annotations

import os
import platform
import sys
from collections.abc import MutableMapping


def configure_qt_widget_composition(*, system: str | None = None,
                                    machine: str | None = None,
                                    environ: MutableMapping[str, str] | None = None) -> bool:
    """Disable Qt's optional QWidget backing-store RHI on Intel macOS.

    Qt enables this path through QT_WIDGETS_RHI or
    QT_WIDGETS_HIGHDPI_DOWNSCALE. On older Intel Macs it can fail in
    QPlatformBackingStore::rhiFlush while the normal QOpenGLWidget viewport
    is otherwise working. This switch must run before QApplication is
    created (and before Qt initializes its backing store).

    The app's own OpenGL viewport is deliberately untouched.
    """
    system = sys.platform if system is None else system
    machine = platform.machine() if machine is None else machine
    if system != "darwin" or machine != "x86_64":
        return False

    env = os.environ if environ is None else environ
    env["QT_WIDGETS_RHI"] = "0"
    env["QT_WIDGETS_HIGHDPI_DOWNSCALE"] = "0"
    return True
