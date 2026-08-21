"""Safe call identifiers and local candidate artifact plans."""

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_ROOT = PROJECT_ROOT / ".local" / "candidates"

SCENARIO_ID_PATTERN = re.compile(r"S\d{2}")
CALL_ID_PATTERN = re.compile(r"S\d{2}-A\d{2}-\d{8}T\d{6}Z")


@dataclass(frozen=True)
class ArtifactPlan:
    call_id: str
    candidate_dir: Path
    two_sided_audio: Path
    speaker_labelled_transcript: Path
    metadata: Path
    turn_observations: Path
    call_review: Path
    cost_entry: Path

    def relative_paths(self) -> dict[str, str]:
        """Return safe paths relative to the candidate directory."""

        return {
            "two_sided_audio": self.two_sided_audio.name,
            "speaker_labelled_transcript": (
                self.speaker_labelled_transcript.name
            ),
            "metadata": self.metadata.name,
            "turn_observations": self.turn_observations.name,
            "call_review": self.call_review.name,
            "cost_entry": self.cost_entry.name,
        }


def generate_call_id(
    scenario_id: str,
    attempt: int,
    started_at: datetime | None = None,
) -> str:
    """Generate an S##-A## timestamped identifier in UTC."""

    if SCENARIO_ID_PATTERN.fullmatch(scenario_id) is None:
        raise ValueError("scenario_id must use the S## format")
    if not 1 <= attempt <= 99:
        raise ValueError("attempt must be between 1 and 99")

    timestamp = started_at or datetime.now(timezone.utc)
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("started_at must include timezone information")

    utc_timestamp = timestamp.astimezone(timezone.utc)
    return (
        f"{scenario_id}-A{attempt:02d}-"
        f"{utc_timestamp:%Y%m%dT%H%M%SZ}"
    )


def plan_candidate_artifacts(call_id: str) -> ArtifactPlan:
    """Derive the complete safe artifact plan for one candidate call."""

    if CALL_ID_PATTERN.fullmatch(call_id) is None:
        raise ValueError("call_id must use the required safe format")

    candidate_dir = CANDIDATES_ROOT / call_id
    _require_within_candidates(candidate_dir)

    return ArtifactPlan(
        call_id=call_id,
        candidate_dir=candidate_dir,
        two_sided_audio=candidate_dir / "two-sided-audio.mp3",
        speaker_labelled_transcript=(
            candidate_dir / "speaker-labelled-transcript.md"
        ),
        metadata=candidate_dir / "metadata.json",
        turn_observations=candidate_dir / "turn-observations.md",
        call_review=candidate_dir / "call-review.md",
        cost_entry=candidate_dir / "cost-entry.json",
    )


def _require_within_candidates(path: Path) -> None:
    candidates_root = CANDIDATES_ROOT.resolve()
    resolved_path = path.resolve()

    if not resolved_path.is_relative_to(candidates_root):
        raise ValueError("artifact path must remain under .local/candidates")
