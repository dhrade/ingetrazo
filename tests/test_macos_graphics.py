# SPDX-License-Identifier: GPL-3.0-or-later
"""The Qt backing-store compatibility switch is limited to Intel macOS."""
from core.macos_graphics import configure_qt_widget_composition


def test_intel_macos_disables_widget_rhi_before_qt_starts():
    env = {"QT_WIDGETS_RHI": "1", "QT_WIDGETS_HIGHDPI_DOWNSCALE": "1"}
    assert configure_qt_widget_composition(
        system="darwin", machine="x86_64", environ=env)
    assert env["QT_WIDGETS_RHI"] == "0"
    assert env["QT_WIDGETS_HIGHDPI_DOWNSCALE"] == "0"


def test_apple_silicon_is_unchanged():
    env = {"QT_WIDGETS_RHI": "1"}
    assert not configure_qt_widget_composition(
        system="darwin", machine="arm64", environ=env)
    assert env == {"QT_WIDGETS_RHI": "1"}


def test_other_operating_systems_are_unchanged():
    env = {"QT_WIDGETS_RHI": "1"}
    assert not configure_qt_widget_composition(
        system="linux", machine="x86_64", environ=env)
    assert env == {"QT_WIDGETS_RHI": "1"}
