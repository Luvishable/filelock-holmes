"""Workspace bootstrap helpers."""

from __future__ import annotations

from .config import WorkDirs


def ensure_workdirs(workdirs: WorkDirs) -> None:
    """Create required runtime directories if they do not exist."""
    for directory in workdirs.all_dirs():
        directory.mkdir(parents=True, exist_ok=True)
