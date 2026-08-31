"""LiveKit worker for one explicitly dispatched S01 call."""

import asyncio
import json
import re
from datetime import timedelta
from pathlib import Path

from livekit import api
from livekit.agents import (
    AgentServer,
    AgentSession,
    JobContext,
    UserInputTranscribedEvent,
    cli,
    room_io,
)

from src.artifacts import plan_candidate_artifacts
from src.call_request import CallRequestPlan, build_call_request_plan
from src.config import load_settings
from src.provider import build_agent_composition
from src.scenario import load_scenario


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = (
    PROJECT_ROOT / "scenarios" / "S01-appointment-scheduling.json"
)
AGENT_NAME = "pgai-s01"

_worker_settings = load_settings()
server = AgentServer(
    ws_url=_worker_settings.livekit_url,
    api_key=_worker_settings.livekit_api_key.get_secret_value(),
    api_secret=_worker_settings.livekit_api_secret.get_secret_value(),
)

GOODBYE_PATTERN = re.compile(r"\b(?:goodbye|good[ -]bye)\b", re.IGNORECASE)


def is_terminal_goodbye(transcript: str) -> bool:
    """Return whether PGAI clearly ended the conversation."""

    return GOODBYE_PATTERN.search(transcript) is not None


def register_goodbye_stop(session: AgentSession) -> None:
    """Stop output and close the session after a final PGAI goodbye."""

    def on_user_input(event: UserInputTranscribedEvent) -> None:
        if not event.is_final or not is_terminal_goodbye(event.transcript):
            return

        session.interrupt(force=True)
        asyncio.create_task(session.aclose())

    session.on("user_input_transcribed", on_user_input)


def build_sip_participant_request(
    plan: CallRequestPlan,
) -> api.CreateSIPParticipantRequest:
    """Convert validated inert data into one LiveKit SIP request."""

    return api.CreateSIPParticipantRequest(
        sip_trunk_id=plan.sip_trunk_id.get_secret_value(),
        sip_call_to=plan.destination,
        room_name=plan.room_name,
        participant_identity=plan.participant_identity,
        participant_name="PGAI assessment",
        wait_until_answered=True,
        max_call_duration=timedelta(seconds=180),
    )


async def create_sip_participant(
    ctx: JobContext,
    plan: CallRequestPlan,
) -> None:
    """Execute the single provider action that begins the telephone call."""

    request = build_sip_participant_request(plan)
    await ctx.api.sip.create_sip_participant(request)


@server.rtc_session(agent_name=AGENT_NAME)
async def s01_call_job(ctx: JobContext) -> None:
    """Run one dispatched S01 call using a preflight-generated call ID."""

    metadata = json.loads(ctx.job.metadata)
    call_id = metadata.get("call_id")
    if not isinstance(call_id, str):
        raise ValueError("dispatch metadata must contain call_id")

    settings = load_settings()
    scenario = load_scenario(SCENARIO_PATH)
    artifacts = plan_candidate_artifacts(call_id)
    plan = build_call_request_plan(settings, scenario, artifacts)
    composition = build_agent_composition(settings, scenario)
    register_goodbye_stop(composition.session)

    try:
        await create_sip_participant(ctx, plan)
        await ctx.wait_for_participant(identity=plan.participant_identity)
        await composition.session.start(
            room=ctx.room,
            record=True,
            room_options=room_io.RoomOptions(
                participant_identity=plan.participant_identity,
            ),
            agent=composition.agent,
        )
    except Exception:
        ctx.shutdown()
        raise


def main() -> None:
    """Start the worker; dialing still requires a separate dispatch."""

    cli.run_app(server)


if __name__ == "__main__":
    main()
