import asyncio
import importlib
from datetime import timedelta
from unittest.mock import AsyncMock, Mock, patch

import src.live_call as live_call_module
from src.call_request import CallRequestPlan
from src.live_call import (
    build_sip_participant_request,
    create_sip_participant,
)


def call_plan() -> CallRequestPlan:
    return CallRequestPlan(
        call_id="S01-A01-20260831T200000Z",
        room_name="pgai-s01-a01-20260831t200000z",
        participant_identity="pgai-target-s01-a01-20260831t200000z",
        sip_trunk_id="test-trunk",
        destination="+18054398008",
        caller_number="+14785550100",
    )


def test_sip_request_uses_only_the_validated_plan() -> None:
    plan = call_plan()

    request = build_sip_participant_request(plan)

    assert request.sip_trunk_id == "test-trunk"
    assert request.sip_call_to == "+18054398008"
    assert request.room_name == plan.room_name
    assert request.participant_identity == plan.participant_identity
    assert request.wait_until_answered is True
    assert request.max_call_duration.ToTimedelta() == timedelta(seconds=180)


def test_create_sip_participant_makes_one_provider_request() -> None:
    ctx = Mock()
    ctx.api.sip.create_sip_participant = AsyncMock()

    asyncio.run(create_sip_participant(ctx, call_plan()))

    ctx.api.sip.create_sip_participant.assert_awaited_once()


def test_import_does_not_start_worker_or_create_call() -> None:
    with patch("livekit.agents.cli.run_app") as run_app:
        importlib.reload(live_call_module)

    run_app.assert_not_called()
    importlib.reload(live_call_module)
