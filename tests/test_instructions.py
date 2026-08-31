from pathlib import Path

import pytest

from src.instructions import build_patient_instructions
from src.scenario import load_scenario


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scenarios"
    / "S01-appointment-scheduling.json"
)


def test_instructions_include_validated_fictional_scenario() -> None:
    scenario = load_scenario(FIXTURE_PATH)

    instructions = build_patient_instructions(scenario)

    assert "Jamie Rivera" in instructions
    assert "1988-04-12" in instructions
    assert scenario.objective in instructions
    assert scenario.intended_outcome in instructions
    assert all(point in instructions for point in scenario.steering_points)
    assert all(
        condition in instructions
        for condition in scenario.safe_stopping_conditions
    )


def test_instructions_identify_patient_as_fictional() -> None:
    scenario = load_scenario(FIXTURE_PATH)

    instructions = build_patient_instructions(scenario)

    assert "fictional patient" in instructions.lower()


def test_instructions_reject_unvalidated_mapping() -> None:
    with pytest.raises(TypeError, match="validated Scenario"):
        build_patient_instructions({})  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "required_boundary",
    [
        "Respond naturally and directly to PGAI's latest turn.",
        "Do not recite a fixed script",
        "do not invent facts",
        "Do not use or request real-patient information.",
        "Do not give medical advice or provide emergency guidance.",
        "until PGAI explicitly confirms its material details",
        "end with a brief, neutral close",
    ],
)
def test_instructions_include_fixed_behavioral_boundaries(
    required_boundary: str,
) -> None:
    scenario = load_scenario(FIXTURE_PATH)

    instructions = build_patient_instructions(scenario)

    assert required_boundary in instructions
