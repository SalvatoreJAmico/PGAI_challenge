import json

from src import artifacts as artifacts_module
from src.artifacts import plan_candidate_artifacts
from src.evidence_workspace import prepare_evidence_workspace


def test_prepare_workspace_creates_incomplete_private_templates(
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        artifacts_module,
        "CANDIDATES_ROOT",
        tmp_path / ".local" / "candidates",
    )
    artifacts = plan_candidate_artifacts("S01-A01-20260831T210000Z")

    prepare_evidence_workspace(artifacts)

    readiness = json.loads(artifacts.readiness.read_text(encoding="utf-8"))
    recording = json.loads(
        artifacts.recording_reference.read_text(encoding="utf-8")
    )
    metadata = json.loads(artifacts.metadata.read_text(encoding="utf-8"))
    cost = json.loads(artifacts.cost_entry.read_text(encoding="utf-8"))

    assert readiness["twilio_recording_status"] == "unconfirmed"
    assert readiness["livekit_session_recording_requested"] is True
    assert readiness["call_attempted"] is False
    assert recording["twilio_call_sid"] is None
    assert recording["twilio_recording_sid"] is None
    assert metadata["duration_seconds"] is None
    assert metadata["provider_call_id"] is None
    assert cost["amount_usd"] is None
    assert not artifacts.two_sided_audio.exists()
