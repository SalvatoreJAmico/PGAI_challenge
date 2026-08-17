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

## Implementation and decision notes

Use this section as a chronological record. Notes should capture what was observed, what changed, why it changed, and the evidence used to judge the result. Do not rewrite early predictions to make them look correct after the fact.

### Initial decision

- **Primary selected:** LiveKit Agents + Twilio SIP + OpenAI `gpt-realtime-2.1`.
- **Backup selected:** Twilio bidirectional Media Streams + OpenAI `gpt-realtime-2.1`.
- **Reasoning:** The bot must clear the coherent-conversation gate, but the project should concentrate engineering time on testing quality, useful bug discovery, evidence, and genuine debugging. LiveKit provides established voice infrastructure while leaving our scenario and evaluation logic in Python.
- **Current state:** Architecture selected; implementation has not started.

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
