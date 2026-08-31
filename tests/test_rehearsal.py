import json
import socket
from datetime import datetime, timezone
from pathlib import Path

from src import artifacts as artifacts_module
from src.artifacts import generate_call_id, plan_candidate_artifacts
from src.conversation import ConversationState
from src.rehearsal import run_rehearsal
from src.scenario import load_scenario


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scenarios"
    / "S01-appointment-scheduling.json"
)


def test_rehearsal_completes_without_network_or_provider_resources(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        artifacts_module,
        "CANDIDATES_ROOT",
        tmp_path / ".local" / "candidates",
    )

    def block_network(*args, **kwargs):
        raise AssertionError("rehearsal attempted network access")

    monkeypatch.setattr(socket, "create_connection", block_network)
    monkeypatch.setattr(socket.socket, "connect", block_network)

    scenario = load_scenario(FIXTURE_PATH)
    call_id = generate_call_id(
        scenario.scenario_id,
        1,
        datetime(2026, 8, 31, 18, 0, tzinfo=timezone.utc),
    )
    artifacts = plan_candidate_artifacts(call_id)

    result = run_rehearsal(scenario, artifacts)
    output = json.loads(result.output_path.read_text(encoding="utf-8"))

    assert result.final_state is ConversationState.COMPLETION
    assert output["provider_free"] is True
    assert output["final_state"] == "completion"
    assert [
        event["state"]
        for event in output["events"]
        if "state" in event
    ] == ["discovery", "steering", "confirmation", "completion"]
    assert "request_confirmation" in {
        event.get("action") for event in output["events"]
    }
    assert "begin_close" in {
        event.get("action") for event in output["events"]
    }


def test_rehearsal_output_contains_no_provider_identifiers(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        artifacts_module,
        "CANDIDATES_ROOT",
        tmp_path / ".local" / "candidates",
    )
    scenario = load_scenario(FIXTURE_PATH)
    artifacts = plan_candidate_artifacts(
        "S01-A01-20260831T180000Z"
    )

    result = run_rehearsal(scenario, artifacts)
    output = result.output_path.read_text(encoding="utf-8")

    assert "api_key" not in output
    assert "sip_trunk" not in output
    assert "provider_call_id" not in output
