"""Build an inert, approved outbound call-request plan."""

from pydantic import BaseModel, ConfigDict, SecretStr

from src.artifacts import ArtifactPlan
from src.config import Settings, normalize_approved_destination
from src.scenario import Scenario


class CallRequestPlan(BaseModel):
    """Validated values for a future LiveKit SIP participant request."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    call_id: str
    room_name: str
    participant_identity: str
    sip_trunk_id: SecretStr
    destination: str
    caller_number: str


def build_call_request_plan(
    settings: Settings,
    scenario: Scenario,
    artifacts: ArtifactPlan,
) -> CallRequestPlan:
    """Build the approved request data without creating a call resource."""

    if not artifacts.call_id.startswith(f"{scenario.scenario_id}-"):
        raise ValueError("call ID does not match the scenario")

    destination = normalize_approved_destination(
        settings.pgai_destination_number
    )
    safe_call_id = artifacts.call_id.lower()

    return CallRequestPlan(
        call_id=artifacts.call_id,
        room_name=f"pgai-{safe_call_id}",
        participant_identity=f"pgai-target-{safe_call_id}",
        sip_trunk_id=settings.livekit_sip_outbound_trunk,
        destination=destination,
        caller_number=settings.twilio_from_number,
    )
