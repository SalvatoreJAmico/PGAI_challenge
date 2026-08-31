"""Final provider-free checks for the single prepared S01 candidate."""

import json
from dataclasses import asdict, dataclass

from src.artifacts import plan_candidate_artifacts
from src.call_request import build_call_request_plan
from src.config import APPROVED_DESTINATION, load_settings
from src.live_call import SCENARIO_PATH
from src.scenario import load_scenario


CALL_ID = "S01-A01-20260831T195646Z"
CONFIRMED_RECORDING_STATUS = "confirmed_dual_from_answer"


@dataclass(frozen=True)
class PreflightSummary:
    call_id: str
    scenario_id: str
    destination: str
    caller_number: str
    max_call_seconds: int
    room_name: str
    participant_identity: str
    sip_trunk_configured: bool
    twilio_recording_status: str


def run_preflight(call_id: str = CALL_ID) -> PreflightSummary:
    """Validate one prepared call without initializing provider clients."""

    settings = load_settings()
    scenario = load_scenario(SCENARIO_PATH)
    artifacts = plan_candidate_artifacts(call_id)
    plan = build_call_request_plan(settings, scenario, artifacts)
    readiness = json.loads(artifacts.readiness.read_text(encoding="utf-8"))

    recording_status = readiness.get("twilio_recording_status")
    if recording_status != CONFIRMED_RECORDING_STATUS:
        raise ValueError(
            "Twilio recording must be confirmed as Dual Record from answer"
        )
    if plan.destination != APPROVED_DESTINATION:
        raise ValueError("destination did not normalize to the approved number")
    if settings.max_call_seconds != 180:
        raise ValueError("MAX_CALL_SECONDS must be exactly 180")

    return PreflightSummary(
        call_id=call_id,
        scenario_id=scenario.scenario_id,
        destination=plan.destination,
        caller_number=plan.caller_number,
        max_call_seconds=settings.max_call_seconds,
        room_name=plan.room_name,
        participant_identity=plan.participant_identity,
        sip_trunk_configured=bool(
            plan.sip_trunk_id.get_secret_value().strip()
        ),
        twilio_recording_status=recording_status,
    )


def main() -> None:
    summary = run_preflight()

    print("Final non-call preflight ready")
    for key, value in asdict(summary).items():
        print(f"{key}: {value}")
    print("Provider clients initialized: no")
    print("Network requests made: no")
    print("Call resources created: no")


if __name__ == "__main__":
    main()
