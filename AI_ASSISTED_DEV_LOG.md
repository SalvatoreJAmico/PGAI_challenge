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
