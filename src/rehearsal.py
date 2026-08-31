"""Provider-free rehearsal of the minimum conversation path."""

import json
from dataclasses import dataclass
from pathlib import Path

from src.artifacts import ArtifactPlan
from src.conversation import (
    ConversationProgress,
    ConversationState,
    NextAction,
    decide_next_action,
)
from src.scenario import Scenario


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIO_PATH = (
    PROJECT_ROOT / "scenarios" / "S01-appointment-scheduling.json"
)


@dataclass(frozen=True)
class RehearsalResult:
    call_id: str
    final_state: ConversationState
    event_count: int
    output_path: Path


def run_rehearsal(
    scenario: Scenario,
    artifacts: ArtifactPlan,
) -> RehearsalResult:
    """Exercise the successful S01 path without any provider objects."""

    progress = ConversationProgress(
        objective=scenario.objective,
        intended_outcome=scenario.intended_outcome,
    )
    events: list[dict[str, str]] = []

    _transition(progress, ConversationState.DISCOVERY, events)
    events.append(
        {
            "speaker": "patient",
            "text": "I am calling to schedule a routine appointment.",
        }
    )

    progress.add_unresolved_fact("weekday morning availability")
    _transition(progress, ConversationState.STEERING, events)
    events.append(
        {
            "speaker": "patient",
            "text": "A weekday morning would work best.",
        }
    )

    _transition(progress, ConversationState.CONFIRMATION, events)
    confirmation = decide_next_action(
        progress,
        intended_outcome_reached=True,
    )
    if confirmation.action is not NextAction.REQUEST_CONFIRMATION:
        raise RuntimeError("rehearsal did not request confirmation")
    events.append(
        {
            "action": confirmation.action.value,
            "text": "Please confirm the offered appointment details.",
        }
    )

    progress.confirm_fact("weekday morning availability")
    closing = decide_next_action(
        progress,
        intended_outcome_reached=True,
        outcome_confirmed=True,
    )
    if closing.action is not NextAction.BEGIN_CLOSE:
        raise RuntimeError("rehearsal did not begin its close")
    events.append(
        {
            "action": closing.action.value,
            "text": "Thank you. That appointment works for me.",
        }
    )
    _transition(progress, ConversationState.COMPLETION, events)

    artifacts.candidate_dir.mkdir(parents=True, exist_ok=True)
    output_path = artifacts.candidate_dir / "rehearsal.json"
    output_path.write_text(
        json.dumps(
            {
                "call_id": artifacts.call_id,
                "scenario_id": scenario.scenario_id,
                "provider_free": True,
                "final_state": progress.current_state.value,
                "events": events,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    return RehearsalResult(
        call_id=artifacts.call_id,
        final_state=progress.current_state,
        event_count=len(events),
        output_path=output_path,
    )


def _transition(
    progress: ConversationProgress,
    target: ConversationState,
    events: list[dict[str, str]],
) -> None:
    progress.transition_to(target)
    events.append({"state": target.value})


def main() -> None:
    """Run one local rehearsal and print only non-secret results."""

    from src.artifacts import generate_call_id, plan_candidate_artifacts
    from src.scenario import load_scenario

    scenario = load_scenario(DEFAULT_SCENARIO_PATH)
    artifacts = plan_candidate_artifacts(
        generate_call_id(scenario.scenario_id, attempt=1)
    )
    result = run_rehearsal(scenario, artifacts)

    print("Provider-free rehearsal complete")
    print(f"Call ID: {result.call_id}")
    print(f"Final state: {result.final_state.value}")
    print(f"Events: {result.event_count}")
    print(f"Output: {result.output_path.relative_to(PROJECT_ROOT)}")
    print("Provider resources created: no")
    print("Telephone call created: no")


if __name__ == "__main__":
    main()
