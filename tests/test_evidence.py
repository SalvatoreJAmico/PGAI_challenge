from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest
from pydantic import ValidationError

from src.conversation import OutcomeStatus
from src.evidence import (
    CallMetadata,
    CallReview,
    CostEntry,
    RecordingReference,
    Speaker,
    TranscriptTurn,
)


CALL_ID = "S01-A01-20260831T180000Z"


def test_minimum_evidence_records_share_the_call_id() -> None:
    recording = RecordingReference(
        call_id=CALL_ID,
        provider_recording_id="provider-recording-1",
        local_audio_path=Path("two-sided-audio.mp3"),
    )
    transcript = TranscriptTurn(
        call_id=CALL_ID,
        speaker=Speaker.PATIENT,
        started_at_seconds=1.0,
        ended_at_seconds=2.5,
        text="I would like to schedule an appointment.",
    )
    metadata = CallMetadata(
        call_id=CALL_ID,
        scenario_id="S01",
        started_at=datetime(2026, 8, 31, 18, 0, tzinfo=timezone.utc),
        duration_seconds=120,
        outcome=OutcomeStatus.SUCCESS,
        provider_call_id="provider-call-1",
    )
    review = CallReview(
        call_id=CALL_ID,
        coherent=True,
        active_steering=True,
        notes="Reviewed against the complete recording.",
    )
    cost = CostEntry(
        call_id=CALL_ID,
        amount_usd=Decimal("0.42"),
        notes="Recorded from provider usage after the call.",
    )

    assert {
        recording.call_id,
        transcript.call_id,
        metadata.call_id,
        review.call_id,
        cost.call_id,
    } == {CALL_ID}


def test_transcript_requires_speaker_label_and_ordered_timing() -> None:
    with pytest.raises(ValidationError, match="end before"):
        TranscriptTurn(
            call_id=CALL_ID,
            speaker=Speaker.PGAI,
            started_at_seconds=5,
            ended_at_seconds=4,
            text="How may I help you?",
        )


def test_metadata_rejects_duration_over_call_limit() -> None:
    with pytest.raises(ValidationError):
        CallMetadata(
            call_id=CALL_ID,
            scenario_id="S01",
            started_at=datetime.now(timezone.utc),
            duration_seconds=181,
            outcome=OutcomeStatus.TIMEOUT,
            provider_call_id="provider-call-1",
        )


@pytest.mark.parametrize("invalid_call_id", ["", "S01", "../S01-A01"])
def test_evidence_rejects_invalid_call_id(invalid_call_id: str) -> None:
    with pytest.raises(ValidationError, match="safe format"):
        CostEntry(
            call_id=invalid_call_id,
            amount_usd=Decimal("0"),
            notes="Invalid fixture.",
        )
