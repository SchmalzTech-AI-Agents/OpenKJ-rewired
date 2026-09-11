#!/usr/bin/env python3
"""Fast, dependency-free regression checks for repository invariants."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
required = [root / "LICENSE", root / "src" / "LICENSE", root / "src" / "cdg" / "LICENSE"]
missing = [str(path.relative_to(root)) for path in required if not path.is_file()]
if missing:
    raise SystemExit(f"missing license files: {', '.join(missing)}")

cmake = (root / "CMakeLists.txt").read_text(encoding="utf-8")
if "cmake_minimum_required(VERSION 3.24)" not in cmake:
    raise SystemExit("CMake minimum version was not modernized")
if "find_package(QT NAMES Qt6 Qt5" not in cmake:
    raise SystemExit("Qt 6-first package discovery is missing")

settings = (root / "src" / "settings.cpp").read_text(encoding="utf-8")
for marker in (
    "saveState()",
    "restoreState",
    "resetColumnWidths",
    "legacyPurchaseSettingsRemoved",
    "OpenKJ-rewired",
    "QFile::copy",
    "legacySettingsPath",
    "legacySettingsMigrationCompleted",
    "migrationComplete",
    "importLegacyWindowsSettings",
    "pre-import-",
):
    if marker not in settings:
        raise SystemExit(f"settings regression marker missing: {marker}")

mainwindow = (root / "src" / "mainwindow.cpp").read_text(encoding="utf-8")
mainwindow_ui = (root / "src" / "mainwindow.ui").read_text(encoding="utf-8")
if "actionImportOriginalSettingsTriggered" not in mainwindow:
    raise SystemExit("manual settings import handler missing")
if "actionImport_Original_Settings" not in mainwindow_ui:
    raise SystemExit("manual settings import menu item missing")

source = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in (root / "src").rglob("*.cpp"))
for forbidden in ("stripe", "creditCard", "SongShop"):
    if forbidden.casefold() in source.casefold():
        raise SystemExit(f"retired purchase/account functionality reintroduced: {forbidden}")

windows_workflow = (root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
for marker in (
    "windeployqt --release --compiler-runtime",
    "openkj-rewired-windows-x86_64-portable",
    "collect_runtime_deps.py",
):
    if marker not in windows_workflow:
        raise SystemExit(f"portable Windows packaging marker missing: {marker}")
launcher = (root / "packaging" / "windows" / "run-openkj.bat").read_text(encoding="utf-8")
if "GST_PLUGIN_PATH" not in launcher:
    raise SystemExit("portable GStreamer launcher configuration is missing")
for path in (
    root / "packaging" / "windows" / "collect_runtime_deps.py",
    root / "packaging" / "windows" / "run-openkj.bat",
    root / "packaging" / "windows" / "README-WINDOWS.txt",
):
    if not path.is_file():
        raise SystemExit(f"portable Windows packaging file missing: {path.relative_to(root)}")

print("repository invariants: PASS")
