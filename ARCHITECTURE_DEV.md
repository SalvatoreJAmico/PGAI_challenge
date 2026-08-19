# Architecture — Development Notes

## Decision summary

The primary architecture is a Python voice agent built with LiveKit Agents, connected to the phone network through a Twilio SIP trunk and powered by OpenAI `gpt-realtime-2.1`. If LiveKit creates an unresolved problem with SIP routing, deployment, audio quality, recording, or observability, the backup architecture removes LiveKit and connects Twilio Programmable Voice directly to OpenAI Realtime through bidirectional Media Streams.

Both designs preserve the same scenario definitions, fictional patient profiles, one approved outbound number, destination allowlist, call identifiers, transcripts, recordings, metadata, and reports. This keeps a fallback from becoming a complete rewrite.

## Primary architecture: LiveKit Agents + Twilio SIP + OpenAI Realtime

### Data and audio flow

1. The Python scenario runner selects a patient profile, testing objective, steering points, and safe stopping conditions.
2. A LiveKit Python agent creates an outbound SIP participant using the configured Twilio trunk.
3. Twilio places the call from the single approved outbound number to the PGAI assessment number.
4. The PGAI agent's audio enters the LiveKit session through SIP and is passed to OpenAI `gpt-realtime-2.1`.
5. OpenAI generates the simulated patient's speech, which LiveKit returns through Twilio to the PGAI agent.
6. Call events, speaker transcripts, timings, scenario progress, and outcomes are saved under one shared call ID.
7. Twilio produces the required two-sided recording, while LiveKit session recording and observability provide secondary debugging evidence.

### Why this is the primary choice

The challenge does evaluate the bot: coherent, natural voice interaction is the first gate, and submissions that fail it are rejected before deeper review. However, the bot is enabling infrastructure rather than the main end product. Once it clears that quality bar, the stronger differentiators are the quality of the testing, substantive bugs discovered, evidence, iteration, and clarity of reasoning.

LiveKit gives us mature building blocks for outbound SIP calls, session lifecycle, audio transport, turn handling, transcripts, recordings, traces, and metrics. Using those building blocks reduces time spent rebuilding low-level audio plumbing. That lets us spend more of the project on realistic patient behavior, scenario steering, listening to calls, identifying failure patterns, and demonstrating a genuine debugging and improvement process. This is the main reason for the decision: use reliable infrastructure for the parts that are not unique to the assessment, while keeping the scenario logic, safeguards, evaluation, and reporting in our Python code.

OpenAI `gpt-realtime-2.1` was selected for native speech-to-speech interaction and its focus on silence, noise, interruption behavior, instruction following, and tool use. Twilio was selected as the carrier because it supports a stable outbound E.164 number, SIP trunking, two-sided recording, call callbacks, and auditable usage records.

### Tradeoffs

The primary design introduces LiveKit as an additional service and abstraction layer. That means another account, configuration surface, and possible failure point. Some turn behavior will still be controlled by the Realtime model, so LiveKit cannot eliminate every interruption or endpointing problem. We accept those costs because the framework lowers implementation risk, improves observability, and gives us more time to test and debug the PGAI agent rather than our media transport.

## Backup architecture: Twilio Media Streams + OpenAI Realtime

### Data and audio flow

1. The Python application asks Twilio Programmable Voice to place the approved outbound call.
2. Twilio opens a bidirectional Media Stream to our Python WebSocket service.
3. The service forwards incoming telephone audio and relevant events to OpenAI Realtime.
4. It returns OpenAI's generated audio to Twilio for playback on the call.
5. The application manages buffering, interruptions, call state, transcripts, timings, and artifact creation directly.
6. Twilio remains responsible for the authoritative two-sided recording and provider call metadata.

### Why this is the backup

This design uses fewer platforms and gives us direct control over the audio and event bridge. It also reuses the same Twilio number, OpenAI account, scenarios, prompts, evidence structure, and reporting workflow as the primary design. It is therefore a practical fallback if LiveKit blocks progress.

It is not the first choice because we would need to build and tune audio forwarding, buffering, playback cancellation, turn synchronization, interruption recovery, reconnection behavior, and transcript alignment ourselves. That work could be valuable in a production voice platform, but for this assessment it would consume time better spent evaluating the target agent and documenting useful bugs.

### Conditions for switching to the backup

We switch only after documenting a reproducible primary-path problem that cannot be resolved quickly enough, such as:

- Twilio-to-LiveKit SIP routing cannot be made reliable.
- LiveKit adds unacceptable latency, clipping, or audio degradation.
- The required two-sided recording cannot be captured and retrieved reliably.
- Call events or transcripts cannot be linked to the correct scenario and recording.
- LiveKit deployment or account restrictions prevent a complete controlled call.

A weak first call by itself does not automatically justify switching. We first determine whether the cause is the scenario prompt, Realtime settings, turn detection, SIP transport, or recording configuration. The observed failure and diagnostic process should be preserved as genuine iteration evidence.

## Shared safeguards and evidence model

Regardless of architecture:

- The destination is hard-locked to `+18054398008`.
- Exactly one outbound E.164 number is used for all assessment calls.
- Only fictional test-patient information is used.
- Every call receives a shared ID linking its scenario, recording, transcript, metadata, review, cost, and bug evidence.
- Every submitted call must have two-sided MP3 or OGG audio and a speaker-labelled transcript.
- One complete controlled call is reviewed before any multi-scenario run.
- Calls have duration, repeated-loop, failure, and safe-stop rules.
- Provider recordings are treated as authoritative; generated transcripts are checked against the audio.

## Call and artifact identifiers

Every call uses this shared identifier:

```text
S##-A##-YYYYMMDDThhmmssZ
```

- `S##` is the two-digit scenario number, such as `S01`.
- `A##` is the two-digit attempt number for that scenario, such as `A01`.
- The final component is the call start time in UTC, formatted as a compact ISO 8601 timestamp. The trailing `Z` explicitly means UTC.

Example:

```text
S01-A01-20260817T143000Z
```

Retries increment the attempt number and receive their own start timestamp. Identifiers never contain patient names, phone numbers, provider credentials, or other sensitive values.

The root artifact folders are canonical. Reusable scenario definitions use their scenario ID; every artifact produced by an individual call repeats the exact call ID:

```text
scenarios/S01-appointment-scheduling.yaml
recordings/S01-A01-20260817T143000Z.mp3
transcripts/S01-A01-20260817T143000Z.md
reports/metadata/S01-A01-20260817T143000Z.json
reports/reviews/S01-A01-20260817T143000Z.md
reports/cost-ledger.csv
```

The metadata record contains both the complete call ID and its scenario ID. The review and cost-ledger row also reference the complete call ID. Raw provider downloads and incomplete calls remain under ignored `.local/` directories rather than the canonical evidence folders.

Bug IDs use a separate sequence such as `BUG-001`. Each entry in `submission/BUG_REPORT.md` references the exact call ID, recording path, transcript path, and evidence timestamp, for example `S01-A01-20260817T143000Z` at `01:23`.

## Artifact publication policy

Generated call artifacts begin in an ignored local staging area and are promoted into canonical GitHub folders only after human review.

```text
.local/candidates/<call-id>/
        ↓ listen, compare, validate, and sanitize
recordings/
transcripts/
reports/metadata/
reports/reviews/
```

The following reviewer-facing artifacts are committed:

- Fictional scenario definitions.
- At least 10 selected two-sided MP3 or OGG recordings.
- Matching speaker-labelled transcripts.
- Metadata and human review notes for every selected call.
- A sanitized cost ledger without receipts or payment information.
- The completed bug report with exact call IDs and timestamps.
- Final documentation, Loom links, reproduction instructions, and selected before-and-after iteration evidence.

The following remain local and ignored:

- `.env`, API keys, provider credentials, and private configuration exports.
- Receipts, payment details, and the private submission worksheet.
- Raw WAV, PCM, and temporary conversion files.
- Unreviewed candidates, incomplete calls, accidental calls, and low-quality calls not selected as evidence.
- Provider downloads, logs, debugging dumps, and any artifact containing accidental personal or sensitive information.

An early failed call may be promoted when it is safe and useful evidence of genuine iteration. Promotion requires listening to the recording, checking the transcript against it, confirming that both speakers are present, confirming that all patient data is fictional, validating metadata and filenames, and ensuring no secret or unintended sensitive information will become public.

## Implementation and decision notes

Use this section as a chronological record. Notes should capture what was observed, what changed, why it changed, and the evidence used to judge the result. Do not rewrite early predictions to make them look correct after the fact.

### Initial decision

- **Primary selected:** LiveKit Agents + Twilio SIP + OpenAI `gpt-realtime-2.1`.
- **Backup selected:** Twilio bidirectional Media Streams + OpenAI `gpt-realtime-2.1`.
- **Reasoning:** The bot must clear the coherent-conversation gate, but the project should concentrate engineering time on testing quality, useful bug discovery, evidence, and genuine debugging. LiveKit provides established voice infrastructure while leaving our scenario and evaluation logic in Python.
- **Current state:** Architecture selected; implementation has not started.

### 2026-08-17 — Shared call-ID convention selected

- **Context:** Every scenario, recording, transcript, metadata record, review, and bug needs an unambiguous cross-reference.
- **Decision:** Use `S##-A##-YYYYMMDDThhmmssZ` for every call and repeat the exact ID across all call artifacts.
- **Reasoning and tradeoff:** The format is sortable, distinguishes retries, records UTC start time, avoids sensitive data, and remains readable in reports and videos. It is longer than a simple sequence number but substantially reduces ambiguity.
- **Architecture impact:** None; shared by both primary and backup architectures.
- **Loom talking point:** Show how one identifier connects the complete evidence chain for a test call.

### 2026-08-17 — Canonical artifact folders selected

- **Context:** Duplicate working and submission artifact folders would make it unclear which recording or transcript is authoritative.
- **Decision:** Keep final selected recordings and transcripts in the repository-root `recordings/` and `transcripts/` folders. Store structured metadata under `reports/metadata/`, human reviews under `reports/reviews/`, and the cost ledger at `reports/cost-ledger.csv`. Keep only reviewer-facing documents and video-link notes under `submission/`.
- **Reasoning and tradeoff:** One canonical location prevents duplicate evidence and broken references. The submission folder is cleaner, although final deliverables are distributed between the root artifact folders and reviewer-facing submission documents.
- **Architecture impact:** None; shared by both primary and backup architectures.
- **Loom talking point:** Explain that canonical paths make each bug traceable to one authoritative evidence chain.

### 2026-08-17 — Artifact publication policy selected

- **Context:** Generated calls and provider files should not become public automatically.
- **Decision:** Stage all generated evidence under ignored `.local/` paths and promote only reviewed, sanitized, submission-quality artifacts into canonical GitHub folders.
- **Reasoning and tradeoff:** A deliberate review gate protects secrets and low-quality evidence while preserving the ability to publish a genuine early failure when it demonstrates iteration. Promotion adds one manual step, which is appropriate for public voice evidence.
- **Architecture impact:** None; shared by both primary and backup architectures.
- **Loom talking point:** Explain the human quality gate between call generation and public evidence.

### 2026-08-17 — Cost ledger template added

- **Context:** Every selected call needs an auditable cost entry, while receipts and payment information must remain private.
- **Decision:** Use the committed `reports/cost-ledger.csv` with one row per call. Track the call and scenario IDs, attempt, UTC start, duration, itemized Twilio, LiveKit, OpenAI Realtime, transcription, and other costs, total cost, provider usage reference, private receipt reference, and notes.
- **Reasoning and tradeoff:** A CSV is simple to review, total, and export without adding a database or spreadsheet dependency. Receipt references are safe to publish only when they are internal labels and not private URLs, account identifiers, or payment data.
- **Architecture impact:** None; shared by both primary and backup architectures.
- **Loom talking point:** Show how call IDs connect technical evidence to actual provider usage and cost.

### 2026-08-17 — Private receipt location established

- **Context:** Provider receipts must be preserved for reimbursement without exposing account or payment information in the public repository.
- **Decision:** Store receipts under `.local/receipts/`, which is covered by the `.local/` Git-ignore rule. The committed cost ledger may contain only non-sensitive internal receipt labels that point back to this private directory.
- **Reasoning and tradeoff:** Keeping receipts inside the workspace makes reconciliation convenient, while the ignored parent directory prevents ordinary staging from publishing them. A deliberate force-add could bypass Git ignore rules, so secret scanning and staged-diff review remain required before every publication.
- **Architecture impact:** None; shared by both primary and backup architectures.
- **Loom talking point:** Explain the separation between public cost evidence and private reimbursement documents.

### 2026-08-17 — Environment-variable contract established

- **Context:** The provider configuration names must be documented before credentials are created or implementation begins.
- **Decision:** The safe `.env.example` lists empty variables for LiveKit (`LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, and `LIVEKIT_SIP_OUTBOUND_TRUNK`), OpenAI (`OPENAI_API_KEY` and `OPENAI_REALTIME_MODEL`), Twilio (`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_FROM_NUMBER`), and project safety controls (`PGAI_DESTINATION_NUMBER` and `MAX_CALL_SECONDS`).
- **Reasoning and tradeoff:** Standard provider names reduce setup friction, while explicit project controls make the caller identity, destination, and maximum duration reviewable. The template intentionally contains no example values so secret scans and reviewers can distinguish configuration names from live credentials.
- **Architecture impact:** Supports the primary architecture and retains the Twilio/OpenAI variables needed by the backup.
- **Loom talking point:** Show that the same configuration contract supports a controlled fallback without exposing credentials.

### 2026-08-17 — Repository secret scan passed

- **Context:** Repository-safety changes must be scanned before they are committed and pushed.
- **Evidence:** `detect-secrets` reported 0 findings across all files; targeted OpenAI, GitHub, AWS, and private-key pattern checks reported 0 findings; `.env.example` contained 0 non-empty variable values.
- **Decision:** Proceed with the repository-safety commit. Repeat the same checks immediately before final publication/submission because later credentials and provider artifacts may change the risk profile.
- **Architecture impact:** None.
- **Loom talking point:** Demonstrate that secret handling was verified rather than assumed.

### 2026-08-18 - Destination configuration fails closed

- **Context:** The assessment authorizes calls only to `+18054398008`; a missing or altered setting must never broaden that scope.
- **Decision:** Treat `+18054398008` as the immutable approved destination. Before any provider request, require the configured value to exist, parse as E.164, normalize to the exact approved value, and reject missing, malformed, overridden, or different values without a fallback.
- **Implementation status:** Contract documented during provider setup. Configuration loading, enforcement code, and fixture tests are deliberately deferred to Phase 4.
- **Reasoning and tradeoff:** A configuration error stops execution instead of risking an unauthorized call. This is stricter than accepting arbitrary valid phone numbers and matches the challenge safety boundary.
- **Architecture impact:** Shared by the primary and backup call paths.
- **Loom talking point:** Show that both call paths use one immutable destination gate before contacting LiveKit or Twilio.

### Note template

#### YYYY-MM-DD — Short decision or observation

- **Context:**
- **Observed behavior:**
- **Evidence:**
- **Decision or change:**
- **Reasoning and tradeoff:**
- **Result:**
- **Architecture impact:** None / Primary adjusted / Switched to backup
- **Loom talking point:**
