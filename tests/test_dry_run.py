import json
import socket
from datetime import datetime, timezone

from src import artifacts
from src.config import Settings
from src.dry_run import run_dry_run
from src.scenario import Scenario


def synthetic_settings() -> Settings:
    return Settings(
        _env_file=None,
        LIVEKIT_URL="wss://example.invalid",
        LIVEKIT_API_KEY="offline-livekit-key",  # pragma: allowlist secret
        LIVEKIT_API_SECRET="offline-livekit-secret",  # pragma: allowlist secret
        LIVEKIT_SIP_OUTBOUND_TRUNK="offline-trunk",
        OPENAI_API_KEY="offline-openai-key",  # pragma: allowlist secret
        OPENAI_REALTIME_MODEL="offline-realtime-model",
        TWILIO_ACCOUNT_SID="offline-account-sid",
        TWILIO_AUTH_TOKEN="offline-auth-token",
        TWILIO_FROM_NUMBER="+13125550123",
        PGAI_DESTINATION_NUMBER="+18054398008",
        MAX_CALL_SECONDS="180",
    )


def synthetic_scenario() -> Scenario:
    return Scenario.model_validate(
        {
            "scenario_id": "S01",
            "objective": "Test a fictional appointment request.",
            "intended_outcome": "Receive an appointment offer or next step.",
            "steering_points": ["Ask for a weekday morning."],
            "safe_stopping_conditions": ["Stop after a clear outcome."],
            "patient": {
                "fictional": True,
                "first_name": "Jamie",
                "last_name": "Rivera",
                "date_of_birth": "1988-04-12",
            },
        }
    )


def test_dry_run_writes_only_safe_readiness_plan(
    tmp_path,
    monkeypatch,
) -> None:
    candidate_root = tmp_path / ".local" / "candidates"
    monkeypatch.setattr(artifacts, "CANDIDATES_ROOT", candidate_root)
    started_at = datetime(2026, 8, 21, 16, 30, 45, tzinfo=timezone.utc)

    readiness_path = run_dry_run(
        synthetic_settings(),
        synthetic_scenario(),
        started_at=started_at,
    )

    readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
    assert readiness["status"] == "ready"
    assert readiness["call_id"] == "S01-A01-20260821T163045Z"
    assert readiness["scenario_id"] == "S01"
    assert readiness["approved_destination"] == "+18054398008"
    assert list(readiness_path.parent.iterdir()) == [readiness_path]

    rendered_readiness = json.dumps(readiness)
    assert "offline-openai-key" not in rendered_readiness
    assert "offline-auth-token" not in rendered_readiness
    assert "Jamie" not in rendered_readiness


def test_dry_run_uses_no_network(
    tmp_path,
    monkeypatch,
) -> None:
    candidate_root = tmp_path / ".local" / "candidates"
    monkeypatch.setattr(artifacts, "CANDIDATES_ROOT", candidate_root)

    def reject_network(*args, **kwargs):
        raise AssertionError("dry run attempted to open a network socket")

    monkeypatch.setattr(socket, "socket", reject_network)
    started_at = datetime(2026, 8, 21, 16, 30, 45, tzinfo=timezone.utc)

    readiness_path = run_dry_run(
        synthetic_settings(),
        synthetic_scenario(),
        started_at=started_at,
    )

    assert readiness_path.is_file()
