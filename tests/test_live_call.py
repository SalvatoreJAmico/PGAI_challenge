import asyncio
import importlib
from datetime import timedelta
from unittest.mock import AsyncMock, Mock, patch

import src.live_call as live_call_module
from src.call_request import CallRequestPlan
from src.live_call import (
    build_sip_participant_request,
    create_sip_participant,
    is_terminal_goodbye,
    register_goodbye_stop,
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


def test_only_clear_goodbye_is_terminal() -> None:
    assert is_terminal_goodbye("Hello, this is the test line. Goodbye.")
    assert is_terminal_goodbye("Good-bye for now.")
    assert not is_terminal_goodbye("How may I help you today?")


def test_goodbye_handler_interrupts_and_closes_session() -> None:
    async def exercise() -> None:
        callbacks = {}
        session = Mock()
        session.interrupt = Mock()
        session.aclose = AsyncMock()
        session.on = lambda event, callback: callbacks.setdefault(
            event,
            callback,
        )
        register_goodbye_stop(session)

        callback = callbacks["user_input_transcribed"]
        callback(
            live_call_module.UserInputTranscribedEvent(
                transcript="Goodbye.",
                is_final=True,
            )
        )
        await asyncio.sleep(0)

        session.interrupt.assert_called_once_with(force=True)
        session.aclose.assert_awaited_once()

    asyncio.run(exercise())
