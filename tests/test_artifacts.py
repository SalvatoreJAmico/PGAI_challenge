from datetime import datetime, timedelta, timezone

import pytest

from src.artifacts import (
    CANDIDATES_ROOT,
    generate_call_id,
    plan_candidate_artifacts,
)


def test_call_id_uses_scenario_attempt_and_utc_timestamp() -> None:
    started_at = datetime(2026, 8, 21, 16, 30, 45, tzinfo=timezone.utc)

    call_id = generate_call_id("S01", 1, started_at)

    assert call_id == "S01-A01-20260821T163045Z"


def test_call_id_converts_timestamp_to_utc() -> None:
    central_time = timezone(timedelta(hours=-5))
    started_at = datetime(2026, 8, 21, 11, 30, 45, tzinfo=central_time)

    call_id = generate_call_id("S01", 2, started_at)

    assert call_id == "S01-A02-20260821T163045Z"


@pytest.mark.parametrize("scenario_id", ["", "S1", "S001", "../S01"])
def test_unsafe_scenario_id_is_rejected(scenario_id: str) -> None:
    with pytest.raises(ValueError):
        generate_call_id(scenario_id, 1)


@pytest.mark.parametrize("attempt", [-1, 0, 100])
def test_invalid_attempt_is_rejected(attempt: int) -> None:
    with pytest.raises(ValueError):
        generate_call_id("S01", attempt)


def test_naive_timestamp_is_rejected() -> None:
    with pytest.raises(ValueError):
        generate_call_id("S01", 1, datetime(2026, 8, 21, 16, 30, 45))


def test_candidate_artifact_plan_stays_under_ignored_root() -> None:
    call_id = "S01-A01-20260821T163045Z"

    plan = plan_candidate_artifacts(call_id)

    assert plan.candidate_dir.parent == CANDIDATES_ROOT
    assert all(
        path.parent == plan.candidate_dir
        for path in (
            plan.two_sided_audio,
            plan.speaker_labelled_transcript,
            plan.metadata,
            plan.turn_observations,
            plan.call_review,
            plan.cost_entry,
        )
    )


def test_candidate_plan_includes_every_required_artifact() -> None:
    plan = plan_candidate_artifacts("S01-A01-20260821T163045Z")

    assert set(plan.relative_paths()) == {
        "two_sided_audio",
        "speaker_labelled_transcript",
        "metadata",
        "turn_observations",
        "call_review",
        "cost_entry",
    }


@pytest.mark.parametrize(
    "call_id",
    [
        "../S01-A01-20260821T163045Z",
        "S01-A01-20260821T163045Z/escape",
        "S01-A1-20260821T163045Z",
        "S01-A01-not-a-timestamp",
    ],
)
def test_unsafe_call_id_is_rejected(call_id: str) -> None:
    with pytest.raises(ValueError):
        plan_candidate_artifacts(call_id)
