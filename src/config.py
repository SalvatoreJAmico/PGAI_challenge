# Central configuration for the PGAI voice bot.
#
# This module will:
# - load the agreed settings from environment variables and `.env.local`;
# - expose typed LiveKit, OpenAI, Twilio, and project-safety fields;
# - protect credentials with Pydantic `SecretStr` values;
# - reject missing or malformed configuration without revealing secret values;
# - validate the call-duration setting and destination safety contract; and
# - provide one settings-loading function for the rest of the application.
#
# This module must not print settings, create provider clients, make network
# requests, create rooms or SIP participants, or initiate telephone calls.

from pathlib import Path
from typing import Annotated

import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat
from pydantic import Field, SecretStr, StringConstraints, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APPROVED_DESTINATION = "+18054398008"

NonEmptyStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env.local",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    livekit_url: NonEmptyStr = Field(validation_alias="LIVEKIT_URL")
    livekit_api_key: SecretStr = Field(
        validation_alias="LIVEKIT_API_KEY",
        min_length=1,
    )
    livekit_api_secret: SecretStr = Field(
        validation_alias="LIVEKIT_API_SECRET",
        min_length=1,
    )
    livekit_sip_outbound_trunk: SecretStr = Field(
        validation_alias="LIVEKIT_SIP_OUTBOUND_TRUNK",
        min_length=1,
    )

    openai_api_key: SecretStr = Field(
        validation_alias="OPENAI_API_KEY",
        min_length=1,
    )
    openai_realtime_model: NonEmptyStr = Field(
        validation_alias="OPENAI_REALTIME_MODEL"
    )

    twilio_account_sid: SecretStr = Field(
        validation_alias="TWILIO_ACCOUNT_SID",
        min_length=1,
    )
    twilio_auth_token: SecretStr = Field(
        validation_alias="TWILIO_AUTH_TOKEN",
        min_length=1,
    )
    twilio_from_number: NonEmptyStr = Field(
        validation_alias="TWILIO_FROM_NUMBER"
    )

    pgai_destination_number: NonEmptyStr = Field(
        validation_alias="PGAI_DESTINATION_NUMBER"
    )
    max_call_seconds: int = Field(
        validation_alias="MAX_CALL_SECONDS",
        ge=180,
        le=180,
    )

    @field_validator("pgai_destination_number")
    @classmethod
    def validate_destination(cls, value: str) -> str:
        try:
            parsed_number = phonenumbers.parse(value, "US")
        except NumberParseException as exc:
            raise ValueError(
                "PGAI destination must be a valid phone number"
            ) from exc

        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError(
                "PGAI destination must be a valid phone number"
            )

        normalized_number = phonenumbers.format_number(
            parsed_number,
            PhoneNumberFormat.E164,
        )

        if normalized_number != APPROVED_DESTINATION:
            raise ValueError(
                "PGAI destination is not the approved assessment number"
            )

        return normalized_number


def load_settings() -> Settings:
    return Settings()
