import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from src.scenario import FictionalPatient, Scenario, load_scenario


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scenarios"
    / "S01-appointment-scheduling.json"
)


def valid_scenario_values() -> dict[str, object]:
    return {
        "scenario_id": "S01",
        "objective": "Test routine appointment scheduling.",
        "intended_outcome": "Receive an appointment offer or next step.",
        "steering_points": ["Ask for a weekday morning."],
        "safe_stopping_conditions": ["Stop after a clear outcome."],
        "patient": {
            "fictional": True,
            "first_name": "Jamie",
            "last_name": "Rivera",
            "date_of_birth": "1988-04-12",
        },
    }


def test_minimal_fictional_fixture_loads() -> None:
    scenario = load_scenario(FIXTURE_PATH)

    assert scenario.scenario_id == "S01"
    assert scenario.patient.fictional is True
    assert scenario.steering_points
    assert scenario.safe_stopping_conditions


def test_patient_must_be_explicitly_fictional() -> None:
    with pytest.raises(ValidationError):
        FictionalPatient(
            fictional=False,
            first_name="Jamie",
            last_name="Rivera",
            date_of_birth="1988-04-12",
        )


@pytest.mark.parametrize("scenario_id", ["", "1", "S1", "S001", "A01"])
def test_invalid_scenario_id_is_rejected(scenario_id: str) -> None:
    values = valid_scenario_values()
    values["scenario_id"] = scenario_id

    with pytest.raises(ValidationError):
        Scenario.model_validate(values)


@pytest.mark.parametrize(
    "field",
    ["objective", "intended_outcome"],
)
def test_required_description_cannot_be_blank(field: str) -> None:
    values = valid_scenario_values()
    values[field] = "   "

    with pytest.raises(ValidationError):
        Scenario.model_validate(values)


@pytest.mark.parametrize(
    "field",
    ["steering_points", "safe_stopping_conditions"],
)
def test_required_plan_list_cannot_be_empty(field: str) -> None:
    values = valid_scenario_values()
    values[field] = []

    with pytest.raises(ValidationError):
        Scenario.model_validate(values)


def test_undocumented_patient_fields_are_rejected() -> None:
    values = valid_scenario_values()
    patient = dict(values["patient"])
    patient["medical_record_number"] = "should-not-be-stored"
    values["patient"] = patient

    with pytest.raises(ValidationError):
        Scenario.model_validate(values)


def test_fixture_contains_no_real_patient_flag() -> None:
    fixture_data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    assert fixture_data["patient"]["fictional"] is True
