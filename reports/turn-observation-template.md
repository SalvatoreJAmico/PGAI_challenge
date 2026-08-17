# Per-Turn Observation Template

Use one copy of this section for every meaningful patient or PGAI turn. Record only what the audio and transcript support. Use `not applicable`, `not observable`, or `not measured` instead of guessing.

## Turn record

- **Call ID:**
- **Scenario ID:**
- **Turn number:**
- **Speaker:** `patient` | `PGAI` | `system`
- **Turn start timestamp:**
- **Turn end timestamp:**

### Trigger

- **Triggering patient prompt or event:** Exact transcript text or a concise factual description of the event that caused this turn.
- **Trigger type:** `spoken request` | `answer` | `correction` | `interruption` | `silence` | `system event` | `other`

### Flow position and question

- **Predicted flow state:** `greeting` | `identify intent` | `collect information` | `check policy or availability` | `propose action` | `confirm` | `close` | `escalate` | `unknown`
- **Question or response:** Exact transcript text or a close transcription.
- **Question order:** Sequential number for PGAI questions in this call; use `not applicable` for non-question turns.
- **Expected next step:** What the scenario or current flow reasonably required next.

### Information requested

- **Patient information requested:** List each requested fact; use `none` when no information was requested.
- **Request necessity:** `required` | `possibly required` | `unnecessary` | `unknown`
- **Repeated request:** `no` | `yes—patient had not answered` | `yes—patient had already answered`

### Memory and consistency

- **Earlier facts relevant to this turn:** List the previously established facts the agent should retain.
- **Facts recalled correctly:**
- **Facts omitted, changed, or contradicted:**
- **Memory result:** `consistent` | `minor omission` | `material inconsistency` | `not tested`

### Timing

- **Previous speaker end timestamp:**
- **PGAI response start timestamp:**
- **Response-start latency:**
- **Silence duration:**
- **Timing note:** Note unusually long pauses, premature responses, clipping, or measurement uncertainty.

### Interruption and barge-in

- **Interruption occurred:** `no` | `patient interrupted PGAI` | `PGAI interrupted patient` | `overlap only`
- **PGAI stopped speaking promptly:** `yes` | `no` | `not applicable` | `unclear`
- **New information retained after interruption:** `yes` | `no` | `not applicable` | `unclear`
- **Interruption result:** Concise description of recovery and whether the conversation stayed coherent.

### Correction and contradiction

- **Correction or contradiction occurred:** `no` | `patient corrected a fact` | `patient contradicted an earlier fact` | `PGAI contradicted an earlier fact`
- **Agent acknowledged the change:** `yes` | `no` | `not applicable`
- **Agent replaced the outdated fact:** `yes` | `no` | `not applicable` | `unclear`
- **Correction result:** `resolved` | `partially resolved` | `unresolved` | `not applicable`

### Confirmation accuracy

- **Confirmation attempted:** `yes` | `no` | `not required`
- **Material details requiring confirmation:**
- **Details confirmed accurately:**
- **Details missing or incorrect:**
- **Confirmation result:** `accurate` | `incomplete` | `incorrect` | `not applicable`

### Misunderstanding recovery

- **Misunderstanding occurred:** `yes` | `no` | `unclear`
- **Recovery action:** `clarifying question` | `paraphrase` | `retry with new wording` | `escalation` | `none` | `not applicable`
- **Recovery attempts so far:**
- **Recovery result:** `recovered` | `partially recovered` | `failed` | `not applicable`

### Exceptional behavior

- **Behavior observed:** `none` | `transfer` | `refusal` | `repeated loop` | `retry` | `timeout` | `hang-up`
- **Trigger for behavior:**
- **Agent explanation or warning:**
- **Outcome:**
- **Appropriate for the situation:** `yes` | `no` | `unclear`

### Turn assessment

- **Turn result:** `pass` | `minor issue` | `major issue` | `not scorable`
- **Evidence timestamp:**
- **Reviewer note:** One factual sentence explaining the result.
- **Potential bug reference:** `none` or `BUG-###`

## Recording rules

- Number turns in chronological order and keep speaker labels consistent.
- Use recording-relative timestamps for evidence; do not substitute wall-clock time.
- Quote the transcript when wording matters and paraphrase only when the event matters more than exact wording.
- Separate observation from interpretation: describe what happened before judging it.
- Do not infer hidden system state, database writes, transfers, or completed actions from confident wording alone.
- Link any material failure to the exact call ID, turn number, and recording timestamp.
