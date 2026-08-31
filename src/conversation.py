"""Provider-independent conversation state definitions."""

from enum import StrEnum
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
)


NonEmptyStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]

PGAI_SILENCE_RECOVERY_SECONDS = 10.0
PGAI_POST_RECOVERY_TIMEOUT_SECONDS = 20.0
REPEATED_LOOP_LIMIT = 3
CLOSE_START_SECONDS = 165.0


class ConversationState(StrEnum):
    """Named stages in one controlled assessment conversation."""

    OPENING = "opening"
    DISCOVERY = "discovery"
    STEERING = "steering"
    CONFIRMATION = "confirmation"
    COMPLETION = "completion"
    SAFE_STOP = "safe_stop"
    FAILURE = "failure"


class OutcomeStatus(StrEnum):
    """Reviewable result of a controlled conversation."""

    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    ACCEPTABLE_ALTERNATIVE = "acceptable_alternative"
    PARTIAL = "partial"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    SAFE_STOP = "safe_stop"


class NextAction(StrEnum):
    """Deterministic instruction for the runtime's next behavior."""

    CONTINUE = "continue"
    RECOVERY_PROMPT = "recovery_prompt"
    REQUEST_CONFIRMATION = "request_confirmation"
    BEGIN_CLOSE = "begin_close"
    STOP = "stop"


class ConversationDecision(BaseModel):
    """Result of one deterministic runtime decision."""

    model_config = ConfigDict(extra="forbid")

    action: NextAction
    outcome: OutcomeStatus
    reason: NonEmptyStr


TERMINAL_STATES = frozenset(
    {
        ConversationState.COMPLETION,
        ConversationState.SAFE_STOP,
        ConversationState.FAILURE,
    }
)


class ConversationProgress(BaseModel):
    """Validated state and progress facts for one conversation."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    objective: NonEmptyStr
    intended_outcome: NonEmptyStr
    acceptable_alternative: NonEmptyStr | None = None
    current_state: ConversationState = ConversationState.OPENING
    confirmed_facts: set[NonEmptyStr] = Field(default_factory=set)
    unresolved_facts: set[NonEmptyStr] = Field(default_factory=set)
    elapsed_seconds: float = Field(default=0, ge=0, allow_inf_nan=False)
    silence_seconds: float = Field(default=0, ge=0, allow_inf_nan=False)
    silence_recovery_prompted_at: float | None = Field(
        default=None,
        ge=0,
        allow_inf_nan=False,
    )
    repeated_loop_count: int = Field(default=0, ge=0)
    max_duration_seconds: int = Field(default=180, ge=180, le=180)

    def transition_to(self, target: ConversationState) -> None:
        """Move to an allowed state or fail without changing state."""

        if not is_transition_allowed(self.current_state, target):
            raise ValueError(
                "conversation transition is not allowed: "
                f"{self.current_state.value} -> {target.value}"
            )

        self.current_state = target

    def add_unresolved_fact(self, fact: str) -> None:
        """Add one scenario fact that still needs confirmation."""

        self.unresolved_facts.add(fact)

    def confirm_fact(self, fact: str) -> None:
        """Mark one scenario fact as confirmed and no longer unresolved."""

        self.unresolved_facts.discard(fact)
        self.confirmed_facts.add(fact)

    def advance_elapsed(self, seconds: float) -> None:
        """Add a nonnegative measured interval to total elapsed time."""

        self.elapsed_seconds = _add_measured_interval(
            self.elapsed_seconds,
            seconds,
        )

    def advance_silence(self, seconds: float) -> None:
        """Add a nonnegative measured interval to current PGAI silence."""

        self.silence_seconds = _add_measured_interval(
            self.silence_seconds,
            seconds,
        )

    def clear_silence(self) -> None:
        """Reset the silence interval after meaningful PGAI activity."""

        self.silence_seconds = 0
        self.silence_recovery_prompted_at = None

    def record_silence_recovery_prompt(self) -> None:
        """Record the one recovery prompt at the current silence time."""

        if not self.silence_recovery_due:
            raise ValueError("silence recovery prompt is not due")
        self.silence_recovery_prompted_at = self.silence_seconds

    def record_repeated_loop(self) -> None:
        """Record one verified repetition without meaningful progress."""

        self.repeated_loop_count += 1

    def clear_repeated_loop(self) -> None:
        """Reset the loop count after meaningful progress."""

        self.repeated_loop_count = 0

    @property
    def maximum_duration_reached(self) -> bool:
        return self.elapsed_seconds >= self.max_duration_seconds

    @property
    def closing_window_reached(self) -> bool:
        return self.elapsed_seconds >= CLOSE_START_SECONDS

    @property
    def silence_recovery_due(self) -> bool:
        return (
            self.silence_recovery_prompted_at is None
            and self.silence_seconds >= PGAI_SILENCE_RECOVERY_SECONDS
        )

    @property
    def silence_timeout_reached(self) -> bool:
        if self.silence_recovery_prompted_at is None:
            return False
        return (
            self.silence_seconds - self.silence_recovery_prompted_at
            >= PGAI_POST_RECOVERY_TIMEOUT_SECONDS
        )

    @property
    def repeated_loop_limit_reached(self) -> bool:
        return self.repeated_loop_count >= REPEATED_LOOP_LIMIT

ALLOWED_TRANSITIONS: dict[
    ConversationState,
    frozenset[ConversationState],
] = {
        ConversationState.OPENING: frozenset(
            {
                ConversationState.DISCOVERY,
                ConversationState.SAFE_STOP,
                ConversationState.FAILURE,
            }
        ),
        ConversationState.DISCOVERY: frozenset(
            {
                ConversationState.STEERING,
                ConversationState.CONFIRMATION,
                ConversationState.SAFE_STOP,
                ConversationState.FAILURE,
            }
        ),
        ConversationState.STEERING: frozenset(
            {
                ConversationState.DISCOVERY,
                ConversationState.CONFIRMATION,
                ConversationState.SAFE_STOP,
                ConversationState.FAILURE,
            }
        ),
        ConversationState.CONFIRMATION: frozenset(
            {
                ConversationState.STEERING,
                ConversationState.COMPLETION,
                ConversationState.SAFE_STOP,
                ConversationState.FAILURE,
            }
        ),
        ConversationState.COMPLETION: frozenset(),
        ConversationState.SAFE_STOP: frozenset(),
        ConversationState.FAILURE: frozenset(),
}


def is_transition_allowed(
    current: ConversationState,
    target: ConversationState,
) -> bool:
    """Return whether the state machine permits this transition."""

    return target in ALLOWED_TRANSITIONS[current]


def decide_next_action(
    progress: ConversationProgress,
    *,
    intended_outcome_reached: bool = False,
    acceptable_alternative_reached: bool = False,
    outcome_confirmed: bool = False,
    partial_outcome_available: bool = False,
    unrecoverable_failure: bool = False,
) -> ConversationDecision:
    """Choose the next action without mutating progress or using providers."""

    if intended_outcome_reached and acceptable_alternative_reached:
        raise ValueError("only one final outcome may be selected")
    if outcome_confirmed and not (
        intended_outcome_reached or acceptable_alternative_reached
    ):
        raise ValueError("a selected outcome is required for confirmation")

    if progress.maximum_duration_reached:
        return ConversationDecision(
            action=NextAction.STOP,
            outcome=OutcomeStatus.TIMEOUT,
            reason="maximum duration reached",
        )
    if progress.silence_timeout_reached:
        return ConversationDecision(
            action=NextAction.STOP,
            outcome=OutcomeStatus.TIMEOUT,
            reason="PGAI silence timeout reached",
        )
    if progress.silence_recovery_due:
        return ConversationDecision(
            action=NextAction.RECOVERY_PROMPT,
            outcome=OutcomeStatus.IN_PROGRESS,
            reason="PGAI silence recovery prompt due",
        )
    if progress.repeated_loop_limit_reached:
        return ConversationDecision(
            action=NextAction.BEGIN_CLOSE,
            outcome=OutcomeStatus.SAFE_STOP,
            reason="repeated-loop limit reached",
        )
    if unrecoverable_failure:
        return ConversationDecision(
            action=NextAction.STOP,
            outcome=OutcomeStatus.FAILURE,
            reason="unrecoverable conversation failure",
        )

    if intended_outcome_reached or acceptable_alternative_reached:
        if not outcome_confirmed:
            return ConversationDecision(
                action=NextAction.REQUEST_CONFIRMATION,
                outcome=OutcomeStatus.IN_PROGRESS,
                reason="material outcome requires confirmation",
            )

        outcome = (
            OutcomeStatus.SUCCESS
            if intended_outcome_reached
            else OutcomeStatus.ACCEPTABLE_ALTERNATIVE
        )
        return ConversationDecision(
            action=NextAction.BEGIN_CLOSE,
            outcome=outcome,
            reason="material outcome confirmed",
        )

    if partial_outcome_available:
        return ConversationDecision(
            action=NextAction.BEGIN_CLOSE,
            outcome=OutcomeStatus.PARTIAL,
            reason="actionable partial outcome available",
        )

    if progress.closing_window_reached:
        return ConversationDecision(
            action=NextAction.BEGIN_CLOSE,
            outcome=OutcomeStatus.SAFE_STOP,
            reason="maximum duration is approaching",
        )

    return ConversationDecision(
        action=NextAction.CONTINUE,
        outcome=OutcomeStatus.IN_PROGRESS,
        reason="conversation remains active",
    )


def _add_measured_interval(current: float, seconds: float) -> float:
    if seconds < 0:
        raise ValueError("measured interval cannot be negative")
    return current + seconds
