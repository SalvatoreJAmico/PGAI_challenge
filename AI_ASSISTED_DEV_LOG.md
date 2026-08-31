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
