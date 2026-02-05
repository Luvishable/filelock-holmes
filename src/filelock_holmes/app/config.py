"""Runtime configuration models for filelock-holmes"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class WorkDirs:
    """Filesystem topology used by the pipeline runtime"""

    root: Path
    inbox: Path
    staging: Path
    accepted: Path
    rejected: Path
    quarantine: Path

    @classmethod
    def from_root(cls, root: Path) -> WorkDirs:
        """Build canonical work directory paths from a single root path."""
        return cls(
            root=root,
            inbox=root / "inbox",
            staging=root / "staging",
            accepted=root / "accepted",
            rejected=root / "rejected",
            quarantine=root / "quarantine",
        )

    def all_dirs(self) -> tuple[Path, ...]:
        """Return all managed directories in deterministic order."""
        return (
            self.root,
            self.inbox,
            self.staging,
            self.accepted,
            self.rejected,
            self.quarantine,
        )


@dataclass(frozen=True, slots=True)
class StabilityConfig:
    """Settings for size/mtime stabilization checks."""

    poll_interval_seconds: float = 0.5
    stable_window_checks: int = 3


@dataclass(frozen=True, slots=True)
class WorkerConfig:
    """Queue/worker runtime settings."""
    max_queue_size: int = 1024
    worker_count: int = 1


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    """Top-level runtime configuration consumed by app orchestration."""

    workdirs: WorkDirs
    stability_config: StabilityConfig
    worker_config: WorkerConfig
    audit_dsn: str

    @classmethod
    def for_local_dev(cls, project_root: Path) -> RuntimeConfig:
        """Create a pragmatic default config for local development."""
        workdirs = WorkDirs.from_root(project_root / "work")
        return cls (
            workdirs=workdirs,
            stability_config=StabilityConfig(),
            worker_config=WorkerConfig(),
            audit_dsn=f"sqlite:///{(project_root / 'work' / 'audit.db').as_posix()}",
        )