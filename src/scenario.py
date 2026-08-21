"""Validated fictional patient and assessment scenario definitions."""

import json
from datetime import date
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


NonEmptyStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]
ScenarioId = Annotated[
    str,
    StringConstraints(pattern=r"^S\d{2}$"),
]


class FictionalPatient(BaseModel):
    """Minimum identity facts for a fictional test patient."""

    model_config = ConfigDict(extra="forbid")

    fictional: Literal[True]
    first_name: NonEmptyStr
    last_name: NonEmptyStr
    date_of_birth: date


class Scenario(BaseModel):
    """A controlled, fictional assessment conversation plan."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: ScenarioId
    objective: NonEmptyStr
    intended_outcome: NonEmptyStr
    steering_points: list[NonEmptyStr] = Field(min_length=1)
    safe_stopping_conditions: list[NonEmptyStr] = Field(min_length=1)
    patient: FictionalPatient


def load_scenario(path: Path) -> Scenario:
    """Load and validate a scenario from a local JSON fixture."""

    with path.open(encoding="utf-8") as scenario_file:
        return Scenario.model_validate(json.load(scenario_file))
