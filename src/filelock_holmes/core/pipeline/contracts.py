"""Static pipeline contracts for the processing flow."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, TypeVar, runtime_checkable


class StageName(StrEnum):
    """Canonical stage name from watch to audit"""

    WATCH = "watch"
    QUEUE = "queue"
    STABILITY_CHECK = "stability_check"
    CLAIM_TO_STAGING = "claim_to_staging"
    METADATA_EXTRACT = "metadata_extract"
    RULE_EVALUATION = "rule_evaluation"
    SCAN_PIPELINE = "scan_pipeline"
    DECISION_AGGREGATION = "decision_aggregation"
    ACTIONS = "actions"
    AUDIT = "audit"


InT = TypeVar("InT", contravariant=True)
OutT = TypeVar("OutT", covariant=True)


@runtime_checkable
class PipelineStage(Protocol[InT, OutT]):
    """Behavior contract for a single pipeline stage."""

    stage_name: StageName

    def run(self, payload: InT) -> OutT:
        """Transform input payload into next-stage payload."""


@dataclass(frozen=True, slots=True)
class StageBoundary:
    """Immutable boundary definition for one stage."""

    stage: StageName
    input_model: str
    output_model: str
    responsibility: str


PIPELINE_BOUNDARIES: tuple[StageBoundary, ...] = (
    StageBoundary(
        stage = StageName.WATCH,
        input_model = "InboxPath",
        output_model = "FileEvent",
        responsibility = "Capture file events from inbox.",
    ),
    StageBoundary(
        stage = StageName.QUEUE,
        input_model = "FileEvent",
        output_model = "QueuedEvent",
        responsibility = "Serialize processing through single-worker queue.",
    ),
    StageBoundary(
        stage = StageName.STABILITY_CHECK,
        input_model = "QueuedEvent",
        output_model = "StableCandidate",
        responsibility = "Verify size/mtime stability before claim.",
    ),
    StageBoundary(
        stage = StageName.CLAIM_TO_STAGING,
        input_model = "StableCandidate",
        output_model = "StagedFile",
        responsibility = "Atomically move file from inbox to staging.",
    ),
    StageBoundary(
        stage = StageName.METADATA_EXTRACT,
        input_model = "StagedFile",
        output_model = "FileMetadata",
        responsibility = "Extract sha256, size, extension and type hints.",
    ),
    StageBoundary(
        stage = StageName.RULE_EVALUATION,
        input_model = "FileMetadata",
        output_model = "RuleEvaluationResult",
        responsibility = "Run policy and security rules.",
    ),
    StageBoundary(
        stage = StageName.SCAN_PIPELINE,
        input_model = "RuleEvaluationResult",
        output_model = "ScanResultBundle",
        responsibility = "Run heuristics and optional plugin scanners.",
    ),
    StageBoundary(
        stage = StageName.DECISION_AGGREGATION,
        input_model = "ScanResultBundle",
        output_model = "DecisionRecord",
        responsibility = "Apply priority QUARANTINE > REJECT > ACCEPT.",
    ),
    StageBoundary(
        stage = StageName.ACTIONS,
        input_model = "DecisionRecord",
        output_model = "ActionResult",
        responsibility = "Route file to accepted/rejected/quarantine.",
    ),
    StageBoundary(
        stage = StageName.AUDIT,
        input_model = "ActionResult",
        output_model = "AuditEvent",
        responsibility = "Persist processing trail to audit storage.",
    ),
)



