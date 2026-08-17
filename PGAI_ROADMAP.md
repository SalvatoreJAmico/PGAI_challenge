# Pretty Good AI Engineering Challenge — Live Roadmap

**Status:** Architecture research and selection complete; implementation not started  
**Working pace:** One or two steps at a time; Salvatore writes the Python in small pieces with AI code completion and review  
**Expected duration:** Four working days, with a fifth contingency day if integration or call quality requires it  
**Assessment destination:** `+18054398008` only  
**Outbound number:** Not yet selected — after selection, use exactly that one E.164 number for every assessment call

## Current architecture direction

- **Primary:** LiveKit Agents in Python + Twilio Elastic SIP Trunking + OpenAI `gpt-realtime-2.1`.
- **Backup:** Twilio Programmable Voice bidirectional Media Streams + OpenAI `gpt-realtime-2.1`.
- **Decision rationale:** Voice coherence is the first evaluation gate, so the primary design uses established voice infrastructure to reduce avoidable transport and session-lifecycle work. Once that gate is cleared, project effort should concentrate on realistic scenario steering, substantive bug discovery, evidence quality, and genuine debugging and iteration.
- **Fallback rule:** Switch only after preserving and diagnosing a reproducible LiveKit/SIP/deployment/audio/recording blocker. The backup reuses the Twilio number, OpenAI model, scenarios, prompts, identifiers, and evidence format.
- **Working record:** Architecture reasoning and implementation observations belong in `ARCHITECTURE_DEV.md`. The concise reviewer-facing explanation will be finalized in `submission/ARCHITECTURE.md` after call evidence exists.
- **Cost posture:** Track all usage and preserve receipts, but do not sacrifice the strongest overall architecture merely to remain under the $20 reimbursement amount.

## Non-negotiable safety gates

- [ ] Create and use only fictional test-patient data.
- [ ] Create a test account at <https://pgai.us/athena> to understand the patient experience.
- [ ] Never call the number displayed on Athena's confirmation screen.
- [ ] Every assessment call goes only to `+18054398008`.
- [ ] Select exactly one outbound number and record it accurately in E.164 format.
- [ ] Use that same outbound number for every test call, including mapping and retest calls.
- [ ] Do not make a manual call from a personal phone.
- [ ] Do not make any call until the approved outbound number, two-sided recording, transcript capture, and metadata capture are configured.
- [ ] Do not make bulk calls until one complete early call has been heard, inspected, and approved.
- [ ] Do not commit API keys, phone credentials, tokens, secrets, `.env`, or sensitive recordings.
- [X] Commit a safe `.env.example` containing the agreed provider and safety variable names with no values or secrets; extend it only when the configuration contract changes.
- [ ] Preserve receipts and provider usage records for reimbursement.
- [ ] Track anticipated spending and warn Salvatore before material costs; the $20 reimbursement amount is not an architecture constraint.
- [ ] Do not contact PGAI or its employees through email, LinkedIn, or other direct channels.
- [ ] Do not publish, purchase, submit the form, or take another irreversible external action without showing Salvatore the exact final state first.

## Required video alerts

Use these alerts during the build, **before** the corresponding action:

- **[WALKTHROUGH EVIDENCE]** Preserve or note this for Loom Video 1.
- **[VIDEO 1 TALKING POINT]** Be prepared to explain this decision and why it was made.
- **[DEBUG VIDEO OPPORTUNITY]** Stop before fixing; begin recording Loom Video 2 with voice, webcam, and screen visible.
- **[DO NOT FIX YET]** Preserve the genuine failure until its observed behavior and diagnostic prompt are recorded.
- **[WEBCAM/VOICE REQUIRED]** Confirm Salvatore is visible and speaking before continuing.

## Phase 0 — Workspace and source-of-truth setup

- [X] Inspect the workspace and confirm where the Git repository will live.
- [X] Confirm whether an existing repository exists or create a new local repository plan.
- [X] Create this focused structure, adjusting only if a cleaner implementation emerges:
  - `src/`
  - `scenarios/`
  - `recordings/`
  - `transcripts/`
  - `reports/`
  - `scripts/`
  - `README.md`
  - `ARCHITECTURE_DEV.md` for working decisions and notes
  - `submission/ARCHITECTURE.md` for the final reviewer-facing explanation
  - `submission/BUG_REPORT.md`
  - `.env.example`
  - dependency file (`requirements.txt` or `pyproject.toml`)
- [X] Add `.gitignore` protections for `.env`, credentials, temporary audio, caches, and local provider files; extend as new tools introduce local artifacts.
- [X] Establish IDs and filenames that link scenario, call, recording, transcript, metadata, review, and bug evidence (`S##-A##-YYYYMMDDThhmmssZ`).
- [X] Define the artifact publication policy: generated evidence starts under ignored `.local/` staging and only reviewed, sanitized, submission-quality artifacts are promoted into canonical GitHub folders.
- [X] Add a committed cost ledger at `reports/cost-ledger.csv` and a private, ignored receipt location at `.local/receipts/`.

## Phase 1 — Verify current official services before coding

- [X] Read current official documentation for candidate telephony, voice/Realtime, recording, and transcription services.
- [X] Verify outbound calling support to the approved US number.
- [X] Verify one stable outbound E.164 caller number can be used on every call.
- [X] Verify provider-side or application-side recording captures both sides.
- [X] Verify recordings can be downloaded or converted to MP3 or OGG.
- [X] Verify media streaming format, sample rate, encoding, and WebSocket behavior.
- [X] Verify current Realtime/voice turn-detection, interruption, latency, and transcription capabilities.
- [X] Verify current prices for number rental, call minutes, recording, Realtime audio, and post-call transcription.
- [X] Estimate total cost for 12–14 calls of approximately 1–3 minutes each, plus setup/retests.
- [X] Select the best overall reliable architecture that prioritizes coherent voice quality.
- [X] Record alternatives considered and tradeoffs in `ARCHITECTURE_DEV.md`, with a final summary placeholder at `submission/ARCHITECTURE.md`.

**[VIDEO 1 TALKING POINT]** Explain why the chosen services and audio path best balance latency, reliability, evidence capture, and the $20 target.

## Phase 2 — Map the PGAI agent as a black box

### Predicted map before the first call

- [X] Inspect Athena's patient experience without calling its confirmation-screen number.
- **Website research note:** Project-relevant company materials describe appointment scheduling and changes, medication refills, insurance verification, referral intake, office and after-hours routing, escalation, multilingual handling, and athenaOne write-back. The agent is expected to follow practice-specific workflows and avoid providing medical advice. Treat these as predicted capabilities—not verified behavior—until controlled assessment calls provide recordings and transcripts. Evaluate latency, coherence, memory, confirmation accuracy, corrections, interruptions, unclear intent, escalation, loops, silence, and hang-up behavior. Do not perform security testing or use real patient information; company performance figures remain unverified marketing claims.
- [X] Draft and preserve the expected PGAI agent flow and predicted branches in `PGAI_AGENT_MAP_DEV.md`: greeting → identify intent → collect information → check policy/availability → propose action → confirm → close.
- [X] Define what to capture for every PGAI turn in `reports/turn-observation-template.md`:
  - Prompt or event that triggered it
  - Question asked and order
  - Patient information requested
  - Memory of earlier facts
  - Response delay and silence duration
  - Interruption/barge-in behavior
  - Correction and contradiction handling
  - Confirmation accuracy
  - Misunderstanding recovery
  - Transfer, refusal, loop, retry, or hang-up behavior
- [X] Define timestamps and latency measurements to capture in `reports/TIMING_CONVENTION.md`.
- [X] Define success, failure, timeout, repeated-loop, safe-stop, coherent-call, and active-steering rules in `CALL_QUALITY_RULES_DEV.md`; apply them with `reports/call-quality-review-template.md`.

### Observed map after controlled calls

- [ ] Update the map from the first complete recording and transcript.
- [ ] Add actual timing ranges and detected conversational states.
- [ ] Add newly discovered menus, branches, and required fields.
- [ ] Expand relevant branches during later scenarios without exhaustively repeating identical paths.

**[WALKTHROUGH EVIDENCE]** Preserve the predicted map and revised observed map as proof of technical reasoning and iteration.

## Phase 3 — Safe configuration

- [ ] Select and configure one outbound telephony number.
- [ ] Record the exact outbound E.164 number in a private submission worksheet.
- [ ] Confirm the application rejects every dial target except `+18054398008`.
- [ ] Configure secrets locally through environment variables.
- [X] Create `.env.example` containing the agreed LiveKit, OpenAI, Twilio, and project-safety variable names with safe comments and empty values.
- [ ] Configure two-sided recording before enabling outbound calls.
- [ ] Configure transcript capture for both speakers before enabling outbound calls.
- [ ] Configure call metadata, scenario ID, intended outcome, timing, and review fields.
- [ ] Confirm generated audio files can be stored as MP3 or OGG.
- [ ] Confirm provider receipt/usage records can be preserved.
- [X] Run a secret scan before the repository-safety commit (2026-08-17: `detect-secrets` findings 0; targeted token-pattern findings 0; non-empty `.env.example` values 0).
- [ ] Run the secret scan again immediately before final publication/submission.

## Phase 4 — Build the smallest end-to-end bot

Salvatore writes each Python section in a small, reviewable piece with AI code completion. Do not generate the whole project from a single prompt.

- [ ] Add configuration loading and validation.
- [ ] Add a hard allowlist for the one approved destination number.
- [ ] Define the scenario and patient-profile schema.
- [ ] Define conversation state and intended-outcome tracking.
- [ ] Implement telephony call creation using the single outbound number.
- [ ] Implement the inbound/outbound audio stream.
- [ ] Implement low-latency voice/Realtime connection.
- [ ] Implement natural listening and response turn loop.
- [ ] Implement realistic pacing and sensible turn-taking.
- [ ] Implement intentional interruption support for designated scenarios only.
- [ ] Implement scenario steering without rigid benchmark-script reading.
- [ ] Implement confirmation, success, failure, timeout, loop, and hang-up rules.
- [ ] Implement two-sided recording.
- [ ] Implement two-sided post-call transcript generation or normalization.
- [ ] Implement structured metadata and result saving.
- [ ] Implement reproducible scripts for calling, transcription, and report generation.
- [ ] Add focused tests for number allowlisting, configuration, scenario loading, and artifact naming.
- [ ] Verify the smallest local/non-call path before enabling the first call.

**[VIDEO 1 TALKING POINT]** Explain the data/audio flow, state tracking, scenario steering, and why the bot is dynamic rather than a rigid script.

## Phase 5 — First controlled end-to-end call

- [ ] Confirm the destination is exactly `+18054398008`.
- [ ] Confirm the configured caller is the single approved outbound E.164 number.
- [ ] Confirm two-sided recording is enabled.
- [ ] Confirm two-sided transcript capture is enabled.
- [ ] Confirm scenario, intended outcome, timestamps, metadata, and cost capture are enabled.
- [ ] Make only one controlled call.
- [ ] Hold a complete conversation, normally 1–3 minutes—not one question and hang-up.
- [ ] Confirm the bot actively steers toward the intended outcome.
- [ ] Save MP3 or OGG audio containing both sides.
- [ ] Save a transcript containing both sides with speaker labels.
- [ ] Save scenario definition, intended outcome, metadata, and review notes.
- [ ] Listen to the entire recording.
- [ ] Read the entire transcript against the audio.
- [ ] Measure response latency, pauses, interruptions, glitches, and coherence.
- [ ] Verify the actual call cost in the ledger.
- [ ] Decide whether the first call meets the quality bar.
- [ ] Do not begin bulk calls if it does not.

## Phase 6 — Preserve and record genuine AI-assisted debugging

- [ ] Identify a real early problem from audio, transcript, timing, steering, or artifact generation.
- [ ] Preserve the failing artifact and reproduction steps.
- [ ] Choose a problem whose fix can be demonstrated clearly and safely.

**[DEBUG VIDEO OPPORTUNITY] [DO NOT FIX YET] [WEBCAM/VOICE REQUIRED]** Start Loom Video 2 before reproducing or modifying the code.

Loom Video 2 must show, in one genuine sequence:

- [ ] Salvatore's screen, voice, and webcam.
- [ ] The observed failure.
- [ ] The exact AI prompt used to diagnose it.
- [ ] The AI-assisted diagnosis.
- [ ] The relevant code before modification.
- [ ] Salvatore making the code modification with AI assistance.
- [ ] The follow-up test or retest.
- [ ] The resulting improvement or honest remaining limitation.
- [ ] The prompts used at each step.
- [ ] A saved public Loom link before final submission.

- [ ] Document before/after evidence as genuine iteration.
- [ ] Update the architecture or call map if the observed system differs from the predicted design.

## Phase 7 — Improve voice quality before the scenario run

- [ ] Improve latency and reduce awkward pauses.
- [ ] Tune turn detection and end-of-speech behavior.
- [ ] Tune pacing and response length.
- [ ] Reduce clipping, glitches, echoes, and accidental interruptions.
- [ ] Verify intentional barge-in separately from normal turn-taking.
- [ ] Improve scenario steering and fact consistency.
- [ ] Retest one controlled scenario.
- [ ] Listen to and approve the improved call before the remaining run.

## Phase 8 — Complete the scenario set

Every submitted call must have two-sided MP3/OGG audio, two-sided transcript, scenario, intended outcome, metadata, review notes/result, and cost entry.

- [ ] 01 — Basic appointment scheduling
- [ ] 02 — Rescheduling an appointment
- [ ] 03 — Canceling an appointment
- [ ] 04 — Medication refill request
- [ ] 05 — Office-hours question
- [ ] 06 — Office-location question
- [ ] 07 — Insurance question
- [ ] 08 — Weekend, holiday, closed-day, or unavailable appointment request
- [ ] 09 — Unclear, contradictory, or changing patient request
- [ ] 10 — Interruption, barge-in, unusual request, or creative realistic edge case

### Per-call quality gate

- [ ] Call was complete and coherent, normally 1–3 minutes.
- [ ] Bot used natural language rather than reading a rigid script.
- [ ] Bot used realistic pacing and appropriate turn-taking.
- [ ] Bot actively steered toward the intended outcome.
- [ ] Audio clearly contains both sides and is MP3 or OGG.
- [ ] Transcript clearly contains both speakers.
- [ ] Scenario and intended outcome are defined.
- [ ] Metadata and timestamps are complete.
- [ ] Review notes state what happened and whether the outcome was achieved.
- [ ] Potential substantive bugs are marked with exact evidence timestamps.
- [ ] Cost is added to the ledger.

### Run controls

- [ ] Complete at least 10 strong calls—no exceptions.
- [ ] Prefer approximately 12–14 total calls only when mapping, iteration, or reproduction adds value.
- [ ] Do not force meaningless tricks or exhaustively repeat identical branches.
- [ ] Pause and review if cumulative spending approaches $20.
- [ ] Never fabricate calls, artifacts, timestamps, bugs, results, or receipts.

## Phase 9 — Bug investigation and report

- [ ] Select substantive, reproducible issues—not wording or punctuation complaints.
- [ ] Attempt reproduction when safe, useful, and within budget.
- [ ] Link every bug to the exact call, recording, transcript, and timestamp.
- [ ] Complete `submission/BUG_REPORT.md`.

Every bug entry must include:

- [ ] Clear title
- [ ] Severity
- [ ] Call or transcript identifier
- [ ] Timestamp
- [ ] What happened
- [ ] Why it is a problem
- [ ] Expected behavior
- [ ] Relevant evidence
- [ ] Whether it reproduced

## Phase 10 — Documentation and repository deliverables

- [ ] Working, clean, understandable Python code.
- [ ] Clear repository structure.
- [ ] `README.md` with prerequisites, setup, configuration, safety rules, and run instructions.
- [ ] README ideally supports one command after initial configuration.
- [ ] README briefly discloses AI-assisted development.
- [ ] `submission/ARCHITECTURE.md` contains at least one or two strong paragraphs covering:
  - How the system works
  - Data and audio flow
  - Infrastructure and frameworks
  - Key technical choices and reasons
  - Alternatives considered
  - Relevant tradeoffs
  - Why the final design fits the challenge
  - Whether a Realtime API was used and why
- [ ] Safe `.env.example` with all required variables.
- [ ] Dependency file.
- [ ] At least 10 MP3 or OGG recordings.
- [ ] At least 10 corresponding two-sided transcripts.
- [ ] Scenario definitions and call-result metadata.
- [ ] Completed `submission/BUG_REPORT.md`.
- [ ] Reproduction scripts for call execution, transcription, and report generation.
- [ ] Evidence of genuine early failure and later improvement.
- [ ] No secrets, `.env`, credentials, or tokens committed.

## Phase 11 — Repository verification before publication

- [ ] Run automated tests and record the result.
- [ ] Reproduce setup from clean instructions where practical.
- [ ] Verify every selected recording opens and contains both sides.
- [ ] Verify every selected transcript contains both speakers.
- [ ] Verify all filenames and IDs cross-reference correctly.
- [ ] Verify all bug timestamps against recordings and transcripts.
- [ ] Verify recordings are MP3 or OGG.
- [ ] Verify the same outbound number was used for every call.
- [ ] Verify the exact outbound E.164 number for the submission.
- [ ] Scan the working tree and full Git history for secrets.
- [ ] Review the complete public-ready diff with Salvatore.
- [ ] Confirm the repository is public only after approval.
- [ ] Open and verify the public repository and required artifacts.

## Phase 12 — Loom Video 1: project walkthrough

**[WALKTHROUGH EVIDENCE] [WEBCAM/VOICE REQUIRED]** Do not begin until the repository, calls, iteration evidence, and bug report are ready.

- [ ] Maximum length: 3 minutes.
- [ ] Salvatore uses his own voice.
- [ ] Webcam is on and Salvatore is visible.
- [ ] Explain the problem and success criteria.
- [ ] Show the bot holding a coherent conversation.
- [ ] Explain the approach and architecture.
- [ ] Explain data/audio flow and scenario steering.
- [ ] Explain the PGAI black-box call map and timing observations.
- [ ] Explain major technical decisions and why they were made.
- [ ] Explain alternatives and relevant tradeoffs concisely.
- [ ] Show meaningful bugs tied to evidence.
- [ ] Show the genuine early problem and demonstrated improvement.
- [ ] Explain why the final design fits voice quality and budget constraints.
- [ ] Communicate clearly and persuasively rather than only listing features.
- [ ] Make the Loom link public.
- [ ] Verify the public link in a logged-out/private browser state.

## Phase 13 — Final submission gate

- [ ] Public GitHub repository verified.
- [ ] Working Python code verified.
- [ ] Accurate setup instructions verified.
- [ ] Architecture explanation complete.
- [ ] `.env.example` present and safe.
- [ ] No secrets in repository or Git history.
- [ ] Minimum 10 complete calls.
- [ ] Same single outbound number used for every call.
- [ ] Correct outbound number recorded in E.164 format.
- [ ] MP3 or OGG two-sided recording for every submitted call.
- [ ] Two-sided transcript for every submitted call.
- [ ] Defined scenario, intended outcome, metadata, and review for every call.
- [ ] Meaningful bug report tied to call IDs and timestamps.
- [ ] Public walkthrough Loom, no longer than 3 minutes, with Salvatore's voice and webcam.
- [ ] Public genuine AI-debugging Loom with Salvatore's voice and webcam.
- [ ] Both Loom links verified publicly.
- [ ] Receipts and usage records preserved.
- [ ] Total cost and reimbursement evidence summarized accurately.
- [ ] Show Salvatore the exact repository, Loom links, E.164 number, costs, and form answers before submission.
- [ ] After explicit approval, complete the PGAI submission form: <https://forms.gle/sdnbrJX2XbgZeQaY6>
- [ ] Preserve a copy of the final submission details.

## Working-day schedule

### Day 1 — Architecture and first complete call

- [ ] Phases 0–3: workspace, official documentation, architecture, map, and safe configuration.
- [ ] Phase 4: smallest end-to-end bot, written in small Python pieces.
- [ ] Phase 5: one controlled call only.
- [ ] Listen, inspect, and decide whether it meets the quality bar.

### Day 2 — Finish core code and demonstrate iteration

- [ ] Preserve a real early failure.
- [ ] Record Loom Video 2 during genuine AI-assisted diagnosis and repair.
- [ ] Improve latency, pacing, turn-taking, steering, and audio quality.
- [ ] Approve an improved controlled call before bulk scenarios.

### Day 3 — Scenario run and bug evidence

- [ ] Complete at least 10 strong scenario calls.
- [ ] Inspect every recording and transcript.
- [ ] Record outcomes, costs, bugs, timestamps, and reproduced behavior.

### Day 4 — Reports, verification, videos, and submission preparation

- [ ] Finish bug report, README, architecture, and reproducibility scripts.
- [ ] Verify artifacts and scan repository plus Git history for secrets.
- [ ] Review the public-ready repository with Salvatore.
- [ ] Record and verify Loom Video 1.
- [ ] Verify both public Loom links and the public repository.
- [ ] Prepare the exact submission form answers for Salvatore's approval.

### Day 5 — Contingency only

- [ ] Resolve provider/integration failures or replace weak calls.
- [ ] Repeat all affected artifact, cost, documentation, and verification checks.

## Live milestone summary

- [x] Complete challenge requirements captured.
- [x] Four-day working plan established, with a fifth contingency day.
- [x] Video alert system established.
- [x] PGAI black-box call mapping included.
- [x] AI-assisted coding approach established: small Python pieces written by Salvatore with AI completion and review.
- [x] Project execution started: repository and architecture phases are underway; implementation has not started.
- [x] Architecture selected from current official documentation.
- [ ] Single outbound number configured.
- [ ] First complete call approved.
- [ ] Genuine debugging video recorded.
- [ ] Minimum 10 strong calls complete.
- [ ] Documentation and bug report complete.
- [ ] Walkthrough video recorded.
- [ ] Repository and links publicly verified.
- [ ] Final submission approved and completed.
