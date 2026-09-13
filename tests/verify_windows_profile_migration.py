#!/usr/bin/env python3
"""Regression checks for migration from the original Windows profile."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
settings = (root / "src" / "settings.cpp").read_text(encoding="utf-8")
mainwindow = (root / "src" / "mainwindow.cpp").read_text(encoding="utf-8")

# The original profile that users already have must remain a read-only source.
for marker in (
    'QStringLiteral("OpenKJ")',
    'QStringLiteral("OpenKJ-rewired")',
    'QStringLiteral("openkj.sqlite")',
    'migrateLegacyWindowsDatabase',
    'legacyDatabaseMigrationCompleted',
    'legacyDatabasePath',
    'legacySettingsMigrationVersion',
):
    if marker not in settings:
        raise SystemExit(f"Windows profile migration marker missing: {marker}")

# Rewired must open its own database directory, after Settings has migrated it.
if 'm_settings.rewiredWindowsDataDirectory()' not in mainwindow:
    raise SystemExit("MainWindow does not use the rewired Windows data directory")
if 'tr("This will replace this copy\'s settings and database' not in mainwindow:
    raise SystemExit("Windows import confirmation is not a complete translated argument")

print("Windows profile migration regression checks: PASS")
