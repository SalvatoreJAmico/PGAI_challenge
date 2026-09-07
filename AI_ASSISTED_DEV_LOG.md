# AI-Assisted Development Log

This log preserves representative prompts, decisions, and meaningful
corrections from the guided implementation. It intentionally excludes
credentials, private provider identifiers, and `.env.local` values.

## 2026-08-19 to 2026-08-21 — Issue #5 non-call safety foundation

### Typed configuration

- **Prompt:** “When we use the colon like this, what is happening—is this a
  dict?”
- **Decision:** Use Pydantic type annotations for required environment-backed
  settings and `SecretStr` for credentials.
- **Correction:** Distinguished Python type annotations from dictionary
  key/value syntax and confirmed that Pydantic enforces the annotations when
  `Settings()` is constructed.

### Exact duration validation

- **Prompt:** “Enforce the 180-second limit and immutable destination
  contract.”
- **Initial attempt:** Used `Literal[180]` for `MAX_CALL_SECONDS`.
- **Observed failure:** Environment values arrive as strings, so the raw
  `"180"` did not match the integer literal.
- **Correction:** Parse as `int` and constrain with `ge=180` and `le=180`,
  preserving both conversion and exact-value enforcement.

### Destination safety gate

- **Prompt:** “Check this work against the issue.”
- **Finding:** An exact string literal rejected every alternate destination
  but did not satisfy the issue requirement to normalize permitted phone
  formatting.
- **Correction:** Added `phonenumbers` parsing, US-format normalization to
  E.164, validity checking, and comparison with the one approved destination.

### Missing-setting test isolation

- **Prompt:** “Check.”
- **Observed failure:** A test intended to omit the destination unexpectedly
  passed because `BaseSettings` loaded the real ignored `.env.local` file.
- **Correction:** Disabled environment-file loading in offline tests with
  `_env_file=None`, proving that a genuinely missing destination fails closed.

### Credential validation and secret scanning

- **Finding:** `SecretStr` masked credential representations but accepted an
  empty string without an additional constraint.
- **Correction:** Added `min_length=1` to every credential field and focused
  rejection tests.
- **Finding:** The repository secret scanner flagged six synthetic test
  strings because their field names contained “key” or “secret.”
- **Correction:** Reviewed the findings by file, line, and detector type, then
  applied narrow inline allowlist annotations only to the synthetic fixtures.
  The repository-only scan then reported zero findings.

### Package execution

- **Prompt:** Reported `ModuleNotFoundError: No module named 'src'` after
  running `src/dry_run.py` directly.
- **Correction:** Run the package entry point with `python -m src.dry_run` so
  Python resolves `src` and its internal imports as a package.

### Verification result

- The focused offline suite passed 49 tests.
- The non-call dry run loaded validated configuration and a fictional scenario,
  generated a UTC call ID, and wrote only an ignored readiness plan.
- No provider client, network request, LiveKit room, SIP participant, Realtime
  session, recording, or telephone call was created.

## 2026-08-31 — Issue #7 runtime scope decision

- **Decision:** AI may implement the code in small increments, explain and show
  each change, run focused offline tests, and wait for Salvatore's review and
  permission before moving to the next increment.
- **User priority:** Move through the challenge quickly enough to complete the
  project while retaining enough explanation for Salvatore to understand and
  describe the code.
- **Scope correction:** Keep only controls that directly support the assignment
  or constrain plausible voice-agent behavior. Do not expand the implementation
  for hypothetical outside attacks, hostile local scenario files, or
  production-grade abuse cases that are unlikely in this closed simulation.
- **Controls retained:** Immutable assessment destination, one caller identity,
  180-second maximum, fictional-patient boundaries, no medical advice,
  confirmation before success, silence and repeated-loop handling, and
  evidence-linked outcomes.
- **Accepted tradeoff:** Locally reviewed scenario fixtures and the existing
  repository secret scan are sufficient for this challenge; no additional
  scenario-content threat scanner will be added unless an observed problem
  justifies it.
- **MVP reduction:** Removed generic unsafe-branch input, prompt rules for
  credential and payment attacks, immutable internal state wrappers,
  mutation-bypass defenses for trusted local code, and non-finite timer edge
  handling. These controls did not materially help the closed assessment.
- **Remaining runtime controls:** The state path, outcome confirmation,
  fictional-patient and no-medical-advice prompt rules, 165-second closing
  window, 180-second maximum, silence recovery, and repeated-loop stop remain
  because they directly affect assignment compliance or call quality.

### Provider-ready MVP result

- **Provider composition:** Added one explicit factory for the installed
  LiveKit `Agent`, OpenAI Realtime model, and `AgentSession`. Imports construct
  nothing, and mocked tests prove failures do not continue into session or
  agent construction.
- **Call request:** Added an inert request plan built only from validated
  settings, scenario, and artifact objects. It revalidates the immutable PGAI
  destination and exposes no destination override.
- **Evidence:** Added minimum call-ID-linked records for the provider recording,
  speaker-labelled transcript turns, metadata, human review, and cost.
- **Rehearsal:** Ran S01 through discovery, steering, confirmation, confirmed
  outcome, and closing without provider objects or network access. The ignored
  rehearsal record ended in `completion`.
- **Verification:** The complete offline suite passed 121 tests. The dry run,
  rehearsal, compile check, dependency check, `git diff --check`, ignore proof,
  and targeted tracked-file credential scan passed. `detect-secrets` was not
  installed, so the targeted scan result is recorded instead of claiming that
  tool ran.
- **Safety state:** No worker, room, SIP participant, Realtime session,
  recording, or telephone call was created.
- **Final review:** Salvatore reviewed the implementation incrementally, asked
  for the provider responsibilities, SIP/RTP path, latency expectations, first
  scenario, and MVP scope to be explained, and authorized completion of the
  offline test and publication gate.
- **Publication state:** Finalized S01, reran 121 offline tests, and prepared
  draft PR #8 to merge and close Issue #7 before Phase 5 begins.

## 2026-08-31 - Issue #9 first controlled live call

- **Prompt:** “Complete the test and close the PR and issue when finished.
  Update all mds to reflect the current state before final.”
- **Authorization:** Salvatore reviewed the exact call ID, scenario,
  destination, caller, 180-second maximum, recording state, and two execution
  commands, then authorized exactly one S01 call.
- **Observed failure before dispatch:** The worker exited because the SDK CLI
  did not load `.env.local`. No job was dispatched and no call was placed.
- **Correction:** Constructed `AgentServer` with the already validated LiveKit
  URL and masked credentials. Seven focused tests passed before retrying the
  worker start under the same one-call authorization.
- **Live result:** Exactly one call completed. Twilio reported 120 billed
  seconds and returned one dual-channel recording. The transcript showed
  active steering, an orthopedic/primary-care mismatch, an actionable
  alternative, a transfer to the PGAI test line, and a coherent close.
- **Quality finding:** Patient responses averaged 3.75 seconds after PGAI
  turns. Two long responses overlapped PGAI. The agent also corrected PGAI's
  demo date of birth even though that did not advance the objective.
- **Human recording review:** Salvatore confirmed three defects: the patient
  overanswered the name question and interrupted profile setup; it contradicted
  PGAI's fictional demo DOB instead of learning the profile premise; and it
  spoke after PGAI said goodbye.
- **Decision:** The first call is useful evidence but does not meet the quality
  bar. Preserve it privately, close Issue #9 as a completed evaluation, and
  move the three corrections to a focused follow-up issue. No retry or second
  call was attempted or authorized. Provider cost had not posted at closure and
  was recorded as unavailable rather than estimated.

## 2026-08-31 - Issue #10 S01 correction and A02 retry

- **Correction:** Updated the patient policy to listen to the complete turn,
  answer only current decisions, retain safe fictional demo-profile facts, and
  stop on goodbye. Added a deterministic LiveKit final-transcript handler that
  interrupts and closes the session when PGAI says goodbye.
- **Verification:** The corrected preflight passed and the complete offline
  suite reached 137 passing tests before authorization.
- **Authorization:** Salvatore authorized exactly one A02 retry after reviewing
  its fixed call ID, destination, caller, recording, duration, and commands.
- **Observed improvement:** Jamie gave concise separate answers for identity,
  DOB, routine-care confirmation, provider preference, and time. It requested
  the missing location and ultimately selected a fully specified appointment.
- **Remaining findings:** A compound time/provider choice received only a time
  answer; yes/no confirmation repeated known details; and complex booking turns
  included approximately 12-13 seconds of response silence.
- **Outcome:** `partial`. The duration limit ended the call before PGAI
  confirmed the booking or said goodbye. No further call was authorized or
  attempted. Instructions were refined behaviorally, without scripting exact
  responses, and the next work moves to a separate focused issue.

### Salvatore's verbatim call-review prompts

The following prompts are preserved exactly as written because they directly
drove the conversation-policy changes:

1. “the first problem is that the PGAI agent was trying to setup the profile an our agent interuped.”
2. “answer one questio at a time”
3. “italso looks like just the name was enouph to create the profile and our agent was trying to correct the dob insted of learning the prophile prems”
4. “so listen -> answre only what was asked -> listen and adapt the known demo profile -> answer”
5. “ok when the PGAI says Good by itis over stop talking”
6. “multipul questions are answerd with one answer. When PGAI gives both the doctors names a coice could have been made. The GPT only chose the morning when it could have chose the doctor too.”
7. “the GPT gives repeted information one incedent is the GPT was asked if it would like to book for rutine care, and answerd "Yes, It is a general office visit for rutine care,"”
8. “Yes, but dont prompt the gpt to say that exaclty.”
9. “there is too much silence.”

## 2026-08-31 - Issue #13 S02 rescheduling call

- **Preparation:** Added the fictional S02 appointment-rescheduling scenario,
  fixed the runtime and preflight to call ID `S02-A01-20260831T222747Z`, and
  prepared an ignored evidence workspace. The full offline suite passed 142
  tests before the live call.
- **Scenario objective:** Ask PGAI to move Jamie Rivera's existing fictional
  routine appointment with Dr. Kelly Noble from Tuesday, September 1 at
  10:00 a.m. to Wednesday, September 2 in the morning.
- **Authorization:** After confirming that all secrets were present, Salvatore
  explicitly authorized one call with the prompt: “yes make the call”.
  Exactly one S02 dispatch was made; no retry was attempted.
- **Observed conversation:** The patient stated the rescheduling request,
  supplied the fictional DOB, spelled the requested name, and answered PGAI's
  compound record-lookup question. PGAI then transferred the call to its test
  line instead of locating or rescheduling the appointment.
- **Terminal behavior:** PGAI ended with “Goodbye.” The deterministic terminal
  handler closed the session, and the patient did not speak after the goodbye.
- **Live result:** Twilio reported one completed 129-second call and one
  completed dual-channel recording. The recording and provider references are
  stored only in the ignored S02 candidate workspace.
- **Outcome:** `partial`. The requested appointment was not rescheduled or
  confirmed because PGAI transferred to the test-line ending during profile
  lookup.
- **Pause state:** The private recording was opened for human review. Salvatore
  paused the session before reporting audio findings. Resume by reviewing that
  recording and recording one observed problem at a time; do not place another
  call without new explicit authorization.
