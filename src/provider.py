"""Create the LiveKit/OpenAI agent composition without starting it."""

from dataclasses import dataclass

from livekit.agents import Agent, AgentSession
from livekit.plugins import openai

from src.config import Settings
from src.instructions import build_patient_instructions
from src.scenario import Scenario


@dataclass(frozen=True)
class AgentComposition:
    """In-memory provider objects that have not been started."""

    agent: Agent
    session: AgentSession


def build_agent_composition(
    settings: Settings,
    scenario: Scenario,
) -> AgentComposition:
    """Build the provider objects without connecting or starting a session."""

    model = openai.realtime.RealtimeModel(
        model=settings.openai_realtime_model,
        api_key=settings.openai_api_key.get_secret_value(),
    )
    session = AgentSession(llm=model)
    agent = Agent(instructions=build_patient_instructions(scenario))

    return AgentComposition(agent=agent, session=session)
