import importlib
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pydantic import SecretStr

from src.config import Settings
import src.provider as provider_module
from src.provider import build_agent_composition
from src.scenario import load_scenario


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scenarios"
    / "S01-appointment-scheduling.json"
)


def provider_settings() -> Settings:
    return Settings(
        LIVEKIT_URL="wss://example.invalid",
        LIVEKIT_API_KEY=SecretStr("local-livekit-key"),  # pragma: allowlist secret
        LIVEKIT_API_SECRET=SecretStr("local-livekit-secret"),  # pragma: allowlist secret
        LIVEKIT_SIP_OUTBOUND_TRUNK=SecretStr("local-trunk"),  # pragma: allowlist secret
        OPENAI_API_KEY=SecretStr("local-openai-key"),  # pragma: allowlist secret
        OPENAI_REALTIME_MODEL="gpt-realtime-2.1",
        TWILIO_ACCOUNT_SID=SecretStr("local-account"),  # pragma: allowlist secret
        TWILIO_AUTH_TOKEN=SecretStr("local-token"),  # pragma: allowlist secret
        TWILIO_FROM_NUMBER="+14785550100",
        PGAI_DESTINATION_NUMBER="+18054398008",
        MAX_CALL_SECONDS=180,
        _env_file=None,
    )


def test_build_agent_composition_wires_model_session_and_agent() -> None:
    settings = provider_settings()
    scenario = load_scenario(FIXTURE_PATH)
    model = Mock(name="realtime_model")
    session = Mock(name="agent_session")
    agent = Mock(name="agent")

    with (
        patch(
            "src.provider.openai.realtime.RealtimeModel",
            return_value=model,
        ) as realtime_model,
        patch("src.provider.AgentSession", return_value=session) as agent_session,
        patch("src.provider.Agent", return_value=agent) as agent_class,
    ):
        composition = build_agent_composition(settings, scenario)

    realtime_model.assert_called_once_with(
        model="gpt-realtime-2.1",
        api_key="local-openai-key",  # pragma: allowlist secret
    )
    agent_session.assert_called_once_with(llm=model)
    agent_class.assert_called_once()
    assert scenario.objective in agent_class.call_args.kwargs["instructions"]
    assert composition.session is session
    assert composition.agent is agent


def test_import_does_not_build_provider_objects() -> None:
    with (
        patch("livekit.plugins.openai.realtime.RealtimeModel") as model,
        patch("livekit.agents.AgentSession") as session,
    ):
        importlib.reload(provider_module)

    model.assert_not_called()
    session.assert_not_called()
    importlib.reload(provider_module)


def test_model_construction_failure_does_not_build_session_or_agent() -> None:
    settings = provider_settings()
    scenario = load_scenario(FIXTURE_PATH)

    with (
        patch(
            "src.provider.openai.realtime.RealtimeModel",
            side_effect=RuntimeError("model construction failed"),
        ),
        patch("src.provider.AgentSession") as agent_session,
        patch("src.provider.Agent") as agent_class,
        pytest.raises(RuntimeError, match="model construction failed"),
    ):
        build_agent_composition(settings, scenario)

    agent_session.assert_not_called()
    agent_class.assert_not_called()
