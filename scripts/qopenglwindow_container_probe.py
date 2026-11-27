#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Isolated native probe for QOpenGLWindow in a QWidget container."""
from __future__ import annotations
import sys
from PySide6.QtCore import QTimer
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtOpenGL import QOpenGLWindow
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

class ProbeWindow(QOpenGLWindow):
    def __init__(self):
        super().__init__()
        self.initialized = self.painted = self.swapped = False
        self.renderer = "unknown"
    def initializeGL(self):
        ctx = self.context()
        if ctx is None or not ctx.isValid():
            raise RuntimeError("No valid OpenGL context")
        self.initialized = True
        raw = ctx.functions().glGetString(0x1F01)
        if isinstance(raw, bytes):
            self.renderer = raw.decode("utf-8", "replace")
        elif raw:
            self.renderer = str(raw)
        else:
            self.renderer = "unknown"
    def paintGL(self):
        gl = self.context().functions()
        gl.glClearColor(0.12, 0.18, 0.24, 1.0)
        gl.glClear(0x00004000 | 0x00000100)
        self.painted = True

def main():
    app = QApplication(sys.argv[:1])
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.CoreProfile)
    fmt.setDepthBufferSize(24)
    QSurfaceFormat.setDefaultFormat(fmt)
    top = QWidget()
    top.setWindowTitle("IngeTrazo — QOpenGLWindow container probe")
    layout = QVBoxLayout(top)
    window = ProbeWindow()
    container = QWidget.createWindowContainer(window, top)
    container.setMinimumSize(640, 480)
    layout.addWidget(container)
    window.frameSwapped.connect(lambda: setattr(window, "swapped", True))
    top.resize(800, 600)
    top.show()
    def finish():
        ok = window.initialized and window.painted and window.swapped and window.context() is not None and window.context().isValid()
        print(f"initialized={window.initialized}")
        print(f"painted={window.painted}")
        print(f"frame_swapped={window.swapped}")
        print(f"renderer={window.renderer}")
        print(f"format={window.format().majorVersion()}.{window.format().minorVersion()}")
        app.exit(0 if ok else 2)
    QTimer.singleShot(8000, finish)
    return app.exec()
if __name__ == "__main__":
    raise SystemExit(main())
