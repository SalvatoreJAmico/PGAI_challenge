"""Explicitly dispatch the one prepared S01 candidate to a running worker."""

import asyncio
import json

from livekit import api

from src.config import Settings, load_settings
from src.live_call import AGENT_NAME
from src.preflight import PreflightSummary, run_preflight


def build_dispatch_request(
    summary: PreflightSummary,
) -> api.CreateAgentDispatchRequest:
    """Build a dispatch containing no destination or credential values."""

    return api.CreateAgentDispatchRequest(
        agent_name=AGENT_NAME,
        room=summary.room_name,
        metadata=json.dumps({"call_id": summary.call_id}),
    )


async def dispatch_once(
    settings: Settings,
    summary: PreflightSummary,
) -> None:
    """Create exactly one dispatch and then close the LiveKit API client."""

    client = api.LiveKitAPI(
        url=settings.livekit_url,
        api_key=settings.livekit_api_key.get_secret_value(),
        api_secret=settings.livekit_api_secret.get_secret_value(),
    )
    try:
        await client.agent_dispatch.create_dispatch(
            build_dispatch_request(summary)
        )
    finally:
        await client.aclose()


def main() -> None:
    summary = run_preflight()
    settings = load_settings()
    asyncio.run(dispatch_once(settings, summary))
    print(f"Dispatched one authorized candidate: {summary.call_id}")


if __name__ == "__main__":
    main()
