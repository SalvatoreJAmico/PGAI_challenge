"""Prepare incomplete, private evidence files before an authorized call."""

import json
from pathlib import Path

from src.artifacts import ArtifactPlan


def prepare_evidence_workspace(artifacts: ArtifactPlan) -> None:
    """Create an ignored workspace without fabricating provider results."""

    artifacts.candidate_dir.mkdir(parents=True, exist_ok=False)

    scenario_id = artifacts.call_id.split("-", maxsplit=1)[0]

    _write_json(
        artifacts.readiness,
        {
            "call_id": artifacts.call_id,
            "twilio_recording_status": "unconfirmed",
            "livekit_session_recording_requested": True,
            "call_attempted": False,
            "planned_artifacts": artifacts.relative_paths(),
        },
    )
    _write_json(
        artifacts.recording_reference,
        {
            "call_id": artifacts.call_id,
            "twilio_call_sid": None,
            "twilio_recording_sid": None,
            "local_audio_path": artifacts.two_sided_audio.name,
        },
    )
    _write_json(
        artifacts.metadata,
        {
            "call_id": artifacts.call_id,
            "scenario_id": scenario_id,
            "started_at": None,
            "duration_seconds": None,
            "outcome": None,
            "provider_call_id": None,
        },
    )
    _write_json(
        artifacts.cost_entry,
        {
            "call_id": artifacts.call_id,
            "amount_usd": None,
            "notes": "Awaiting post-call provider usage review.",
        },
    )
    artifacts.speaker_labelled_transcript.write_text(
        "# Speaker-labelled transcript\n\nAwaiting the reviewed call recording.\n",
        encoding="utf-8",
    )
    artifacts.turn_observations.write_text(
        "# Turn observations\n\nAwaiting the reviewed call recording.\n",
        encoding="utf-8",
    )
    artifacts.call_review.write_text(
        "# Call review\n\nAwaiting the reviewed call recording.\n",
        encoding="utf-8",
    )
    artifacts.retrieval_notes.write_text(
        """# Provider evidence retrieval

- Twilio call: Elastic SIP Trunking > Logs > Calls
- Twilio recording: open the call, then its Recording SID
- LiveKit session: project dashboard > Sessions
- Download the complete two-sided audio only after the call finishes
- Replace all null fields only with observed provider values
""",
        encoding="utf-8",
    )


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2) + "\n",
        encoding="utf-8",
    )
