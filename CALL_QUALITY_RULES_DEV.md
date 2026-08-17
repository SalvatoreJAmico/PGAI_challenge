# Call Outcome and Safety Rules

**Status:** Pre-call development rules

**Created:** 2026-08-17

These rules define how a controlled assessment call will be steered, stopped, and reviewed. They do not describe observed PGAI behavior. Apply them consistently unless recorded evidence justifies a later revision.

## Scenario success and intended outcome

Every scenario must define one intended outcome before the call. The intended outcome must be observable from the recording and transcript, such as obtaining an offered appointment, confirming an office-information answer, submitting a refill request, or reaching an appropriate escalation.

A scenario succeeds only when all of the following are true:

- The conversation reaches the predefined intended outcome or a predefined acceptable alternative.
- The outcome is stated clearly enough for the patient to understand what happened next.
- Material details are confirmed accurately before any claimed action.
- The bot remains consistent with facts established during the call.
- The conversation stays within the scenario's safety boundaries.
- The result is supported by the recording and transcript, not merely inferred from metadata or confident language.

An appropriate refusal or escalation counts as success when it is the scenario's predefined safe outcome.

## Failure criteria

Mark the scenario as failed when any of these materially affects the outcome:

- The intended outcome and all acceptable alternatives are not reached.
- The bot claims an action was completed without adequate confirmation or evidence.
- Material patient, appointment, medication, insurance, location, or timing details are lost, changed, or invented.
- The bot provides medical advice, exceeds its authority, or fails to escalate when required.
- The conversation becomes incoherent, enters a repeated loop, or cannot recover from misunderstanding.
- Audio loss, one-sided recording, missing transcript content, or another artifact failure prevents reliable review.
- The call ends before a meaningful result or safe next step is established.

Use `partial` rather than `failed` only when the predefined intended outcome is not completed but the bot provides a coherent, accurate, and actionable next step. Document the reason.

## Duration and silence limits

- **Target submitted-call duration:** 1–3 minutes.
- **Maximum controlled-call duration:** 3 minutes. Begin a concise close early enough to stop at or before this limit.
- **Response-start warning:** Review any ordinary response that begins more than 2.0 seconds after the patient finishes speaking.
- **Response-start major concern:** Review any ordinary response that begins more than 5.0 seconds after the patient finishes speaking, unless the bot explains that processing is occurring.
- **Patient-side silence reprompt:** After approximately 5 seconds, the test bot may give one brief prompt.
- **Second patient-side silence:** After approximately 10 additional seconds, give one final prompt or close safely.
- **PGAI-side unexplained silence:** If PGAI is silent for 10 seconds after a completed patient turn, give one short recovery prompt.
- **PGAI-side timeout:** If there is no meaningful response within 20 seconds after the recovery prompt, end safely and record a timeout.

Measure actual timing under `reports/TIMING_CONVENTION.md`. Thresholds classify observations; they do not replace exact measurements.

## Repeated-loop detection and limits

A repeated loop occurs when PGAI requests or states materially the same information or action without meaningful progress.

- Count a loop only when the repeated turn has the same functional purpose, not merely similar wording.
- Do not count a justified repeat when the patient did not answer, audio was unclear, or confirmation is required.
- On the second unjustified repetition, respond once with a direct correction or concise restatement.
- On the third occurrence of the same unresolved loop, stop pursuing that branch.
- Request escalation or end safely after the loop limit rather than generating additional repetitive turns.
- Record the first repeated turn, corrective attempt, final repetition, and resulting stop with timestamps.

## Safe-stop and hang-up rules

The test bot must stop or move to closure when:

- The intended outcome or acceptable alternative is complete.
- The three-minute maximum is approaching.
- The repeated-loop or silence limit is reached.
- PGAI requests real patient information, credentials, payment data, or another value outside the fictional scenario.
- The conversation moves into medical advice, emergency handling, abuse, prohibited activity, or another unsafe branch.
- Audio or connection quality makes continued interaction unreliable.
- PGAI has transferred, disconnected, or clearly ended the interaction.

Before an agent-initiated hang-up, when the connection permits:

1. Briefly summarize the completed action or unresolved next step.
2. Avoid claiming success when confirmation is absent.
3. Say a natural closing sentence.
4. Allow a short final response window, then hang up.

Do not prolong a call solely to reach one minute. Do not terminate a productive conversation abruptly solely because the intended outcome has just been reached; close naturally and concisely.

## Minimum complete-and-coherent call requirements

A submitted call must:

- Normally last 1–3 minutes.
- Include an opening, a meaningful multi-turn exchange, an outcome or actionable next step, and a natural close.
- Contain intelligible two-sided audio in MP3 or OGG.
- Have a corresponding two-speaker transcript aligned closely enough for timestamp review.
- Use one predefined fictional scenario and intended outcome.
- Show the test bot listening, answering, and adapting rather than reading a benchmark script.
- Preserve established facts and confirm material details accurately.
- Avoid unresolved extended silence, severe clipping, persistent overlap, or a repeated loop.
- Include complete metadata, per-turn observations, call-level review, and cost entry.

A call outside 1–3 minutes may be retained as diagnostic evidence but should not be selected as one of the minimum ten unless the challenge instructions and review clearly support the exception.

## Active scenario steering standard

Active steering is judged by decisions and adaptation, not by exact wording. The test bot passes when it:

- Introduces the scenario's intent naturally.
- Supplies fictional facts only when relevant or requested.
- Uses follow-up questions, clarifications, corrections, or preference statements to move toward the intended outcome.
- Responds meaningfully to PGAI's latest turn instead of delivering the next line from a fixed script.
- Tests the designated branch without forcing irrelevant tricks.
- Recognizes when the intended outcome, acceptable alternative, or safe-stop condition has been reached.

The bot fails the steering standard when it reads a rigid sequence regardless of PGAI's responses, ignores answered questions, changes facts without a scenario reason, or continues after a valid outcome solely to generate more turns.
