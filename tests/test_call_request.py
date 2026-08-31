from datetime import datetime, timezone
from pathlib import Path

import pytest

from src.artifacts import generate_call_id, plan_candidate_artifacts
from src.call_request import build_call_request_plan
from src.scenario import load_scenario
from tests.test_provider import provider_settings


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scenarios"
    / "S01-appointment-scheduling.json"
)


def test_call_request_uses_only_validated_project_values() -> None:
    scenario = load_scenario(FIXTURE_PATH)
    call_id = generate_call_id(
        scenario.scenario_id,
        1,
        datetime(2026, 8, 31, 18, 0, tzinfo=timezone.utc),
    )
    artifacts = plan_candidate_artifacts(call_id)
    settings = provider_settings()

    request = build_call_request_plan(settings, scenario, artifacts)

    assert request.call_id == call_id
    assert request.destination == "+18054398008"
    assert request.caller_number == settings.twilio_from_number
    assert request.sip_trunk_id == settings.livekit_sip_outbound_trunk
    assert request.room_name == f"pgai-{call_id.lower()}"
    assert request.participant_identity == f"pgai-target-{call_id.lower()}"


def test_call_request_rejects_call_id_for_another_scenario() -> None:
    scenario = load_scenario(FIXTURE_PATH)
    artifacts = plan_candidate_artifacts(
        "S02-A01-20260831T180000Z"
    )

    with pytest.raises(ValueError, match="does not match"):
        build_call_request_plan(provider_settings(), scenario, artifacts)


def test_call_request_exposes_no_destination_override() -> None:
    parameter_names = build_call_request_plan.__annotations__

    assert "destination" not in parameter_names
