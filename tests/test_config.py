import pytest
from pydantic import ValidationError

from src.config import APPROVED_DESTINATION, Settings


def valid_settings_values() -> dict[str, str]:
    return {
        "LIVEKIT_URL": "wss://example.invalid",
        "LIVEKIT_API_KEY": "offline-livekit-key",  # pragma: allowlist secret
        "LIVEKIT_API_SECRET": "offline-livekit-secret",  # pragma: allowlist secret
        "LIVEKIT_SIP_OUTBOUND_TRUNK": "offline-trunk",
        "OPENAI_API_KEY": "offline-openai-key",  # pragma: allowlist secret
        "OPENAI_REALTIME_MODEL": "offline-realtime-model",
        "TWILIO_ACCOUNT_SID": "offline-account-sid",
        "TWILIO_AUTH_TOKEN": "offline-auth-token",
        "TWILIO_FROM_NUMBER": "+13125550123",
        "PGAI_DESTINATION_NUMBER": APPROVED_DESTINATION,
        "MAX_CALL_SECONDS": "180",
    }


def build_settings(**overrides: str) -> Settings:
    values = valid_settings_values()
    values.update(overrides)
    return Settings(_env_file=None, **values)


def test_exact_approved_destination_is_accepted() -> None:
    settings = build_settings()

    assert settings.pgai_destination_number == APPROVED_DESTINATION


def test_formatted_approved_destination_is_normalized() -> None:
    settings = build_settings(PGAI_DESTINATION_NUMBER="(805) 439-8008")

    assert settings.pgai_destination_number == APPROVED_DESTINATION


@pytest.mark.parametrize(
    "destination",
    [
        "not-a-phone-number",
        "+13125550123",
    ],
)
def test_unapproved_destination_is_rejected(destination: str) -> None:
    with pytest.raises(ValidationError):
        build_settings(PGAI_DESTINATION_NUMBER=destination)


def test_missing_destination_is_rejected() -> None:
    values = valid_settings_values()
    del values["PGAI_DESTINATION_NUMBER"]

    with pytest.raises(ValidationError):
        Settings(_env_file=None, **values)


def test_runtime_destination_override_is_rejected() -> None:
    with pytest.raises(ValidationError):
        build_settings(PGAI_DESTINATION_NUMBER="+13125550123")


@pytest.mark.parametrize("duration", ["0", "179", "181", "not-an-integer"])
def test_invalid_call_duration_is_rejected(duration: str) -> None:
    with pytest.raises(ValidationError):
        build_settings(MAX_CALL_SECONDS=duration)


def test_missing_field_error_does_not_expose_credentials() -> None:
    values = valid_settings_values()
    secret_values = {
        values["LIVEKIT_API_KEY"],
        values["LIVEKIT_API_SECRET"],
        values["OPENAI_API_KEY"],
        values["TWILIO_AUTH_TOKEN"],
    }
    del values["LIVEKIT_URL"]

    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None, **values)

    error_message = str(exc_info.value)
    assert all(secret not in error_message for secret in secret_values)


def test_secret_fields_are_masked() -> None:
    settings = build_settings()
    rendered_settings = repr(settings)

    assert "offline-openai-key" not in rendered_settings
    assert "offline-auth-token" not in rendered_settings
    assert "**********" in rendered_settings


@pytest.mark.parametrize(
    "credential",
    [
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "LIVEKIT_SIP_OUTBOUND_TRUNK",
        "OPENAI_API_KEY",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
    ],
)
def test_empty_credential_is_rejected(credential: str) -> None:
    values = valid_settings_values()
    values[credential] = ""

    with pytest.raises(ValidationError):
        Settings(_env_file=None, **values)
