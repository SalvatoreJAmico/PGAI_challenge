"""Build provider-independent instructions from validated scenarios."""

from src.scenario import Scenario


def build_patient_instructions(scenario: Scenario) -> str:
    """Build deterministic agent instructions from one validated scenario."""

    if not isinstance(scenario, Scenario):
        raise TypeError("scenario must be a validated Scenario")

    patient = scenario.patient
    steering_points = _format_list(scenario.steering_points)
    stopping_conditions = _format_list(scenario.safe_stopping_conditions)

    return f"""You are role-playing one fictional patient for a controlled test.

Fictional patient:
- Name: {patient.first_name} {patient.last_name}
- Date of birth: {patient.date_of_birth.isoformat()}

Scenario objective:
{scenario.objective}

Intended outcome:
{scenario.intended_outcome}

Steering points:
{steering_points}

Safe stopping conditions:
{stopping_conditions}

Conversation behavior:
- Respond naturally and directly to PGAI's latest turn.
- Do not recite a fixed script or volunteer every scenario fact at once.
- Use only the fictional patient facts provided above; do not invent facts.
- Do not use or request real-patient information.
- Do not give medical advice or provide emergency guidance.
- Do not claim an outcome is complete until PGAI explicitly confirms its material details.
- When a safe stopping condition applies, end with a brief, neutral close."""


def _format_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)
