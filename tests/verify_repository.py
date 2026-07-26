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
for marker in ("saveState()", "restoreState", "resetColumnWidths", "legacyPurchaseSettingsRemoved"):
    if marker not in settings:
        raise SystemExit(f"settings regression marker missing: {marker}")

source = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in (root / "src").rglob("*.cpp"))
for forbidden in ("stripe", "creditCard", "SongShop"):
    if forbidden.casefold() in source.casefold():
        raise SystemExit(f"retired purchase/account functionality reintroduced: {forbidden}")

print("repository invariants: PASS")
