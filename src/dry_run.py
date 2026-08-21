"""Offline readiness check that creates no provider or call resources."""

import json
from datetime import datetime
from pathlib import Path

from src.artifacts import generate_call_id, plan_candidate_artifacts
from src.config import Settings, load_settings
from src.scenario import Scenario, load_scenario


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIO_PATH = (
    PROJECT_ROOT / "scenarios" / "S01-appointment-scheduling.json"
)


def run_dry_run(
    settings: Settings,
    scenario: Scenario,
    attempt: int = 1,
    started_at: datetime | None = None,
) -> Path:
    """Validate readiness and save only a non-secret local plan."""

    call_id = generate_call_id(
        scenario.scenario_id,
        attempt,
        started_at,
    )
    artifact_plan = plan_candidate_artifacts(call_id)
    artifact_plan.candidate_dir.mkdir(parents=True, exist_ok=False)

    readiness_path = artifact_plan.candidate_dir / "readiness.json"
    readiness = {
        "status": "ready",
        "mode": "non-call-dry-run",
        "call_id": call_id,
        "scenario_id": scenario.scenario_id,
        "approved_destination": settings.pgai_destination_number,
        "max_call_seconds": settings.max_call_seconds,
        "planned_artifacts": artifact_plan.relative_paths(),
    }
    readiness_path.write_text(
        json.dumps(readiness, indent=2) + "\n",
        encoding="utf-8",
    )
    return readiness_path


def main() -> None:
    settings = load_settings()
    scenario = load_scenario(DEFAULT_SCENARIO_PATH)
    readiness_path = run_dry_run(settings, scenario)
    readiness = json.loads(readiness_path.read_text(encoding="utf-8"))

    print("Non-call dry run ready")
    print(f"Call ID: {readiness['call_id']}")
    print(f"Scenario ID: {readiness['scenario_id']}")
    print(f"Plan: {readiness_path.relative_to(PROJECT_ROOT)}")
    print("Provider clients initialized: no")
    print("Network requests made: no")
    print("Call resources created: no")


if __name__ == "__main__":
    main()
