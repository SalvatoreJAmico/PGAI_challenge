# PGAI Voice Bot

Automated voice bot for running realistic patient conversations against the Pretty Good AI test line.

## Status

The local non-call safety foundation is complete. It includes typed
configuration, an immutable normalized destination gate, fictional scenario
validation, UTC call IDs, safe artifact planning, and a provider-free dry run.
Phase 4B is complete. Phase 5 has executed exactly one separately authorized
S01 call through LiveKit, Twilio SIP, and OpenAI Realtime. The private candidate
evidence contains a dual-channel recording, speaker-labelled transcript,
metadata, latency observations, and a human-reviewed technical assessment.
The first call exposed three focused conversational defects. One separately
authorized retry showed substantially better turn discipline and reached a
fully stated appointment choice, but it hit the duration limit before PGAI
confirmed completion. The remaining refinements are complete compound-choice
answers, less repetition, and lower response silence. No further call is
authorized. Provider cost was unavailable and was not estimated.

S02 completed one authorized appointment-rescheduling call with a partial
outcome: PGAI transferred to its test-line ending before confirming a replacement
appointment. Human review of the recording is pending. Any further call requires
new explicit authorization; preparing or importing the code does not dial.

## Local setup

Create the project virtual environment and install the constrained dependencies:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copy `.env.example` to the ignored `.env.local` file and provide the required
private settings. Never commit `.env.local` or print its values.

Run the focused offline test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

Run the provider-free readiness check from the repository root:

```powershell
.\.venv\Scripts\python.exe -m src.dry_run
```

The dry run writes only a non-secret readiness plan under ignored
`.local/candidates/`; it does not initialize provider clients, use the network,
or create a call resource.

Run the provider-free S01 conversation rehearsal:

```powershell
.\.venv\Scripts\python.exe -m src.rehearsal
```

The rehearsal exercises discovery, steering, confirmation, and closing through
the runtime state and decision code. It writes only an ignored local rehearsal
record and creates no provider or call resource.

## Development process

This project is being developed in small, reviewed pieces with AI assistance.
Representative prompts, decisions, observed failures, corrections, and
verification results are preserved in [AI_ASSISTED_DEV_LOG.md](AI_ASSISTED_DEV_LOG.md).

## License

This project is source-available under the custom
[Challenge Evaluation and Educational Use License](LICENSE). Personal
educational use is permitted. Pretty Good AI and its affiliates may use the
software only to evaluate this challenge submission. Commercial, production,
and other corporate use is prohibited without separate written permission.
