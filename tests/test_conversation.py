import pytest
from pydantic import ValidationError

from src.conversation import (
    ALLOWED_TRANSITIONS,
    ConversationDecision,
    ConversationProgress,
    ConversationState,
    NextAction,
    OutcomeStatus,
    TERMINAL_STATES,
    decide_next_action,
    is_transition_allowed,
)


def test_conversation_states_have_stable_string_values() -> None:
    assert [state.value for state in ConversationState] == [
        "opening",
        "discovery",
        "steering",
        "confirmation",
        "completion",
        "safe_stop",
        "failure",
    ]


def test_outcome_statuses_cover_review_results() -> None:
    assert [status.value for status in OutcomeStatus] == [
        "in_progress",
        "success",
        "acceptable_alternative",
        "partial",
        "failure",
        "timeout",
        "safe_stop",
    ]


def test_next_actions_are_runtime_commands() -> None:
    assert [action.value for action in NextAction] == [
        "continue",
        "recovery_prompt",
        "request_confirmation",
        "begin_close",
        "stop",
    ]


def test_only_end_states_are_terminal() -> None:
    assert TERMINAL_STATES == {
        ConversationState.COMPLETION,
        ConversationState.SAFE_STOP,
        ConversationState.FAILURE,
    }


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (ConversationState.OPENING, ConversationState.DISCOVERY),
        (ConversationState.DISCOVERY, ConversationState.STEERING),
        (ConversationState.DISCOVERY, ConversationState.CONFIRMATION),
        (ConversationState.STEERING, ConversationState.DISCOVERY),
        (ConversationState.STEERING, ConversationState.CONFIRMATION),
        (ConversationState.CONFIRMATION, ConversationState.STEERING),
        (ConversationState.CONFIRMATION, ConversationState.COMPLETION),
        (ConversationState.OPENING, ConversationState.SAFE_STOP),
        (ConversationState.CONFIRMATION, ConversationState.FAILURE),
    ],
)
def test_expected_transitions_are_allowed(
    current: ConversationState,
    target: ConversationState,
) -> None:
    assert is_transition_allowed(current, target)


@pytest.mark.parametrize("terminal_state", TERMINAL_STATES)
def test_terminal_states_have_no_outgoing_transitions(
    terminal_state: ConversationState,
) -> None:
    assert ALLOWED_TRANSITIONS[terminal_state] == frozenset()
    assert all(
        not is_transition_allowed(terminal_state, target)
        for target in ConversationState
    )


def test_states_cannot_skip_directly_to_completion() -> None:
    assert not is_transition_allowed(
        ConversationState.OPENING,
        ConversationState.COMPLETION,
    )
    assert not is_transition_allowed(
        ConversationState.DISCOVERY,
        ConversationState.COMPLETION,
    )


def test_progress_starts_with_safe_defaults() -> None:
    progress = ConversationProgress(
        objective="Schedule a fictional patient appointment.",
        intended_outcome="Receive an appointment offer.",
    )

    assert progress.current_state is ConversationState.OPENING
    assert progress.confirmed_facts == set()
    assert progress.unresolved_facts == set()
    assert progress.elapsed_seconds == 0
    assert progress.silence_seconds == 0
    assert progress.silence_recovery_prompted_at is None
    assert progress.repeated_loop_count == 0
    assert progress.max_duration_seconds == 180


def test_progress_fact_sets_are_not_shared() -> None:
    first = ConversationProgress(
        objective="First objective",
        intended_outcome="First outcome",
    )
    second = ConversationProgress(
        objective="Second objective",
        intended_outcome="Second outcome",
    )

    first.confirm_fact("Date of birth confirmed")

    assert second.confirmed_facts == set()


def test_progress_moves_fact_from_unresolved_to_confirmed() -> None:
    progress = ConversationProgress(
        objective="Schedule a fictional patient appointment.",
        intended_outcome="Receive an appointment offer.",
    )

    progress.add_unresolved_fact("Weekday morning requested")
    assert progress.unresolved_facts == {"Weekday morning requested"}

    progress.confirm_fact("Weekday morning requested")
    assert progress.unresolved_facts == set()
    assert progress.confirmed_facts == {"Weekday morning requested"}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("elapsed_seconds", -0.1),
        ("silence_seconds", -0.1),
        ("repeated_loop_count", -1),
        ("max_duration_seconds", 179),
        ("max_duration_seconds", 181),
    ],
)
def test_progress_rejects_unsafe_counters(
    field: str,
    value: float | int,
) -> None:
    values = {
        "objective": "Schedule a fictional patient appointment.",
        "intended_outcome": "Receive an appointment offer.",
        field: value,
    }

    with pytest.raises(ValidationError):
        ConversationProgress.model_validate(values)


def test_progress_rejects_blank_goal_text() -> None:
    with pytest.raises(ValidationError):
        ConversationProgress(
            objective="   ",
            intended_outcome="Receive an appointment offer.",
        )


def test_progress_performs_an_allowed_transition() -> None:
    progress = ConversationProgress(
        objective="Schedule a fictional patient appointment.",
        intended_outcome="Receive an appointment offer.",
    )

    result = progress.transition_to(ConversationState.DISCOVERY)

    assert result is None
    assert progress.current_state is ConversationState.DISCOVERY


def test_progress_rejects_transition_that_skips_required_states() -> None:
    progress = ConversationProgress(
        objective="Schedule a fictional patient appointment.",
        intended_outcome="Receive an appointment offer.",
    )

    with pytest.raises(
        ValueError,
        match="opening -> completion",
    ):
        progress.transition_to(ConversationState.COMPLETION)

    assert progress.current_state is ConversationState.OPENING


@pytest.mark.parametrize("terminal_state", TERMINAL_STATES)
def test_progress_cannot_leave_a_terminal_state(
    terminal_state: ConversationState,
) -> None:
    progress = ConversationProgress(
        objective="Schedule a fictional patient appointment.",
        intended_outcome="Receive an appointment offer.",
        current_state=terminal_state,
    )

    with pytest.raises(ValueError, match="transition is not allowed"):
        progress.transition_to(ConversationState.OPENING)

    assert progress.current_state is terminal_state


def test_progress_tracks_elapsed_time_and_duration_limit() -> None:
    progress = ConversationProgress(
        objective="Schedule a fictional patient appointment.",
        intended_outcome="Receive an appointment offer.",
    )

    progress.advance_elapsed(179.5)
    assert not progress.maximum_duration_reached

    progress.advance_elapsed(0.5)
    assert progress.elapsed_seconds == 180
    assert progress.maximum_duration_reached


def test_progress_tracks_and_clears_silence() -> None:
    progress = ConversationProgress(
        objective="Schedule a fictional patient appointment.",
        intended_outcome="Receive an appointment offer.",
    )

    progress.advance_silence(9.9)
    assert not progress.silence_recovery_due

    progress.advance_silence(0.1)
    assert progress.silence_recovery_due
    assert not progress.silence_timeout_reached

    progress.record_silence_recovery_prompt()
    assert not progress.silence_recovery_due

    progress.advance_silence(19.9)
    assert not progress.silence_timeout_reached

    progress.advance_silence(0.1)
    assert progress.silence_timeout_reached

    progress.clear_silence()
    assert progress.silence_seconds == 0
    assert not progress.silence_timeout_reached


def test_silence_recovery_prompt_cannot_be_recorded_early_or_twice() -> None:
    progress = make_progress()

    with pytest.raises(ValueError, match="not due"):
        progress.record_silence_recovery_prompt()

    progress.advance_silence(10)
    progress.record_silence_recovery_prompt()

    with pytest.raises(ValueError, match="not due"):
        progress.record_silence_recovery_prompt()


def test_progress_tracks_and_clears_repeated_loops() -> None:
    progress = ConversationProgress(
        objective="Schedule a fictional patient appointment.",
        intended_outcome="Receive an appointment offer.",
    )

    progress.record_repeated_loop()
    progress.record_repeated_loop()
    assert not progress.repeated_loop_limit_reached

    progress.record_repeated_loop()
    assert progress.repeated_loop_limit_reached

    progress.clear_repeated_loop()
    assert progress.repeated_loop_count == 0
    assert not progress.repeated_loop_limit_reached


@pytest.mark.parametrize(
    ("method_name", "seconds"),
    [
        ("advance_elapsed", -0.1),
        ("advance_silence", -0.1),
    ],
)
def test_progress_rejects_negative_measured_intervals(
    method_name: str,
    seconds: float,
) -> None:
    progress = ConversationProgress(
        objective="Schedule a fictional patient appointment.",
        intended_outcome="Receive an appointment offer.",
    )

    method = getattr(progress, method_name)

    with pytest.raises(ValueError, match="cannot be negative"):
        method(seconds)


def make_progress() -> ConversationProgress:
    return ConversationProgress(
        objective="Schedule a fictional patient appointment.",
        intended_outcome="Receive an appointment offer.",
    )


def test_active_conversation_continues() -> None:
    decision = decide_next_action(make_progress())

    assert decision == ConversationDecision(
        action=NextAction.CONTINUE,
        outcome=OutcomeStatus.IN_PROGRESS,
        reason="conversation remains active",
    )


@pytest.mark.parametrize(
    ("outcome_arguments", "expected_outcome"),
    [
        ({"intended_outcome_reached": True}, OutcomeStatus.SUCCESS),
        (
            {"acceptable_alternative_reached": True},
            OutcomeStatus.ACCEPTABLE_ALTERNATIVE,
        ),
    ],
)
def test_material_outcome_requires_confirmation(
    outcome_arguments: dict[str, bool],
    expected_outcome: OutcomeStatus,
) -> None:
    unconfirmed = decide_next_action(
        make_progress(),
        **outcome_arguments,
    )
    confirmed = decide_next_action(
        make_progress(),
        outcome_confirmed=True,
        **outcome_arguments,
    )

    assert unconfirmed.action is NextAction.REQUEST_CONFIRMATION
    assert unconfirmed.outcome is OutcomeStatus.IN_PROGRESS
    assert confirmed.action is NextAction.BEGIN_CLOSE
    assert confirmed.outcome is expected_outcome


def test_partial_outcome_begins_close() -> None:
    decision = decide_next_action(
        make_progress(),
        partial_outcome_available=True,
    )

    assert decision.action is NextAction.BEGIN_CLOSE
    assert decision.outcome is OutcomeStatus.PARTIAL


@pytest.mark.parametrize(
    ("condition", "expected_action", "expected_outcome"),
    [
        ("duration", NextAction.STOP, OutcomeStatus.TIMEOUT),
        ("silence", NextAction.STOP, OutcomeStatus.TIMEOUT),
        ("loop", NextAction.BEGIN_CLOSE, OutcomeStatus.SAFE_STOP),
        ("failure", NextAction.STOP, OutcomeStatus.FAILURE),
    ],
)
def test_stop_conditions_have_deterministic_results(
    condition: str,
    expected_action: NextAction,
    expected_outcome: OutcomeStatus,
) -> None:
    progress = make_progress()
    arguments: dict[str, bool] = {}

    if condition == "duration":
        progress.advance_elapsed(180)
    elif condition == "silence":
        progress.advance_silence(10)
        progress.record_silence_recovery_prompt()
        progress.advance_silence(20)
    elif condition == "loop":
        for _ in range(3):
            progress.record_repeated_loop()
    elif condition == "failure":
        arguments["unrecoverable_failure"] = True

    decision = decide_next_action(progress, **arguments)

    assert decision.action is expected_action
    assert decision.outcome is expected_outcome


def test_silence_first_requests_one_recovery_prompt() -> None:
    progress = make_progress()
    progress.advance_silence(10)

    decision = decide_next_action(progress)

    assert decision.action is NextAction.RECOVERY_PROMPT
    assert decision.outcome is OutcomeStatus.IN_PROGRESS


def test_closing_window_begins_before_hard_duration_limit() -> None:
    progress = make_progress()
    progress.advance_elapsed(164.9)
    assert decide_next_action(progress).action is NextAction.CONTINUE

    progress.advance_elapsed(0.1)
    decision = decide_next_action(progress)

    assert decision.action is NextAction.BEGIN_CLOSE
    assert decision.outcome is OutcomeStatus.SAFE_STOP


def test_inconsistent_outcome_flags_are_rejected() -> None:
    with pytest.raises(ValueError, match="only one final outcome"):
        decide_next_action(
            make_progress(),
            intended_outcome_reached=True,
            acceptable_alternative_reached=True,
        )

    with pytest.raises(ValueError, match="selected outcome"):
        decide_next_action(
            make_progress(),
            outcome_confirmed=True,
        )
