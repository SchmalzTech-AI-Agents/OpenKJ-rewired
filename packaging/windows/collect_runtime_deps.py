#!/usr/bin/env python3
"""Collect non-system MinGW runtime DLLs needed by a portable OpenKJ bundle."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

SYSTEM_PREFIXES = ("/c/Windows/", "/mingw64/share/", "/usr/bin/")
DLL_LINE = re.compile(r"^\s*([^\s]+)\s+=>\s+([^\s]+)")
DIRECT_LINE = re.compile(r"^\s*([^\s]+\.dll)\s+\([^)]*\)")


def is_system_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return normalized.startswith(SYSTEM_PREFIXES) or "/Windows/System32/" in normalized


def resolve_dll(name: str, resolved: str, search_dirs: list[Path]) -> Path | None:
    if resolved not in ("", "not", "found") and not is_system_path(resolved):
        candidate = Path(resolved)
        if candidate.is_file():
            return candidate
    for directory in search_dirs:
        candidate = directory / name
        if candidate.is_file():
            return candidate
    return None


def dependencies(binary: Path, search_dirs: list[Path]) -> list[Path]:
    result = subprocess.run(
        ["ldd", str(binary)], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(f"ldd failed for {binary}: {result.stderr.strip()}")

    found: list[Path] = []
    for line in result.stdout.splitlines():
        match = DLL_LINE.match(line) or DIRECT_LINE.match(line)
        if not match:
            continue
        name = match.group(1)
        resolved = match.group(2) if match.lastindex and match.lastindex >= 2 else ""
        if name.lower() in {"kernel32.dll", "user32.dll", "advapi32.dll", "shell32.dll"}:
            continue
        path = resolve_dll(name, resolved, search_dirs)
        if path is not None and not is_system_path(str(path)):
            found.append(path)
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--prefix", type=Path, required=True)
    parser.add_argument("--executable", type=Path, required=True)
    args = parser.parse_args()

    bundle = args.bundle.resolve()
    prefix = args.prefix.resolve()
    executable = args.executable.resolve()
    bundle.mkdir(parents=True, exist_ok=True)

    search_dirs = [bundle, bundle / "bin", prefix / "bin"]
    queue = [executable]
    queue.extend(p for p in bundle.rglob("*.dll") if p.is_file())
    seen: set[Path] = set()

    while queue:
        binary = queue.pop()
        binary = binary.resolve()
        if binary in seen or not binary.is_file():
            continue
        seen.add(binary)
        for dependency in dependencies(binary, search_dirs):
            destination = bundle / dependency.name
            if not destination.exists():
                shutil.copy2(dependency, destination)
            queue.append(destination)

    print(f"Collected {len([p for p in bundle.glob('*.dll') if p.is_file()])} runtime DLLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
