"""Minimum evidence records for reviewed assessment calls."""

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from pathlib import Path
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from src.artifacts import CALL_ID_PATTERN
from src.conversation import OutcomeStatus


NonEmptyStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]


class Speaker(StrEnum):
    PATIENT = "patient"
    PGAI = "pgai"


class EvidenceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    call_id: str

    @field_validator("call_id")
    @classmethod
    def validate_call_id(cls, value: str) -> str:
        if CALL_ID_PATTERN.fullmatch(value) is None:
            raise ValueError("call_id must use the required safe format")
        return value


class RecordingReference(EvidenceRecord):
    provider_recording_id: NonEmptyStr
    local_audio_path: Path


class TranscriptTurn(EvidenceRecord):
    speaker: Speaker
    started_at_seconds: float = Field(ge=0)
    ended_at_seconds: float = Field(ge=0)
    text: NonEmptyStr

    @model_validator(mode="after")
    def validate_timing_order(self) -> "TranscriptTurn":
        if self.ended_at_seconds < self.started_at_seconds:
            raise ValueError("transcript turn cannot end before it starts")
        return self


class CallMetadata(EvidenceRecord):
    scenario_id: NonEmptyStr
    started_at: datetime
    duration_seconds: float = Field(ge=0, le=180)
    outcome: OutcomeStatus
    provider_call_id: NonEmptyStr

    @field_validator("started_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("started_at must include timezone information")
        return value


class CallReview(EvidenceRecord):
    coherent: bool
    active_steering: bool
    notes: NonEmptyStr


class CostEntry(EvidenceRecord):
    amount_usd: Decimal = Field(ge=0)
    notes: NonEmptyStr
