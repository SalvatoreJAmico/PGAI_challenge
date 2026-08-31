import json

import pytest

from src import artifacts as artifacts_module
from src.artifacts import plan_candidate_artifacts
from src.config import APPROVED_DESTINATION
from src.evidence_workspace import prepare_evidence_workspace
from src.preflight import CONFIRMED_RECORDING_STATUS, run_preflight


CALL_ID = "S01-A01-20260831T210000Z"


def prepare_workspace(tmp_path, monkeypatch, recording_status: str) -> None:
    monkeypatch.setattr(
        artifacts_module,
        "CANDIDATES_ROOT",
        tmp_path / ".local" / "candidates",
    )
    artifacts = plan_candidate_artifacts(CALL_ID)
    prepare_evidence_workspace(artifacts)
    readiness = json.loads(artifacts.readiness.read_text(encoding="utf-8"))
    readiness["twilio_recording_status"] = recording_status
    artifacts.readiness.write_text(
        json.dumps(readiness, indent=2) + "\n",
        encoding="utf-8",
    )


def test_preflight_returns_only_non_secret_call_summary(
    tmp_path,
    monkeypatch,
) -> None:
    prepare_workspace(
        tmp_path,
        monkeypatch,
        CONFIRMED_RECORDING_STATUS,
    )

    summary = run_preflight(CALL_ID)

    assert summary.call_id == CALL_ID
    assert summary.scenario_id == "S01"
    assert summary.destination == APPROVED_DESTINATION
    assert summary.max_call_seconds == 180
    assert summary.sip_trunk_configured is True
    assert not hasattr(summary, "livekit_api_key")
    assert not hasattr(summary, "openai_api_key")
    assert not hasattr(summary, "twilio_auth_token")


def test_preflight_stops_when_twilio_recording_is_unconfirmed(
    tmp_path,
    monkeypatch,
) -> None:
    prepare_workspace(tmp_path, monkeypatch, "unconfirmed")

    with pytest.raises(ValueError, match="Dual Record from answer"):
        run_preflight(CALL_ID)
