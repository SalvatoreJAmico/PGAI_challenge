import importlib
import json
from unittest.mock import patch

import src.dispatch_call as dispatch_module
from src.dispatch_call import build_dispatch_request
from src.preflight import PreflightSummary


def summary() -> PreflightSummary:
    return PreflightSummary(
        call_id="S02-A01-20260831T220000Z",
        scenario_id="S02",
        destination="+18054398008",
        caller_number="+14785550100",
        max_call_seconds=180,
        room_name="pgai-s02-a01-20260831t220000z",
        participant_identity="pgai-target-s02-a01-20260831t220000z",
        sip_trunk_configured=True,
        twilio_recording_status="confirmed_dual_from_answer",
    )


def test_dispatch_request_contains_only_agent_room_and_call_id() -> None:
    request = build_dispatch_request(summary())

    assert request.agent_name == "pgai-s02"
    assert request.room == "pgai-s02-a01-20260831t220000z"
    assert json.loads(request.metadata) == {
        "call_id": "S02-A01-20260831T220000Z"
    }
    assert "+18054398008" not in request.metadata
    assert "+14785550100" not in request.metadata


def test_import_does_not_create_livekit_client_or_dispatch() -> None:
    with patch("livekit.api.LiveKitAPI") as livekit_api:
        importlib.reload(dispatch_module)

    livekit_api.assert_not_called()
    importlib.reload(dispatch_module)
