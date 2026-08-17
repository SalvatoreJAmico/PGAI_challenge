# PGAI Agent Predicted Black-Box Map

**Baseline status:** Pre-call hypothesis  
**Created:** 2026-08-17  
**Evidence status:** Not yet verified by an assessment call

This document preserves the expected behavior of the PGAI voice agent before telephone testing. It is based only on the challenge instructions, the fictional-patient Athena demo flow, and project-relevant statements on Pretty Good AI's public website. Company descriptions are treated as predictions, not observed system behavior. After the first controlled call, record the observed map separately instead of rewriting this baseline.

## Predicted main flow

1. Greet the caller and identify the clinic.
2. Ask for the caller's intent.
3. Identify or verify the fictional patient using the minimum information required for the workflow.
4. Ask intent-specific questions and retain facts already supplied.
5. Apply clinic policy, scheduling constraints, or availability.
6. Propose an action, answer, or escalation.
7. Read back material details and request confirmation before committing an action.
8. State the result or next step clearly.
9. Ask whether anything else is needed and close naturally.

## Predicted workflow branches

### Appointment scheduling

- Collect appointment reason, preferred timing, location, and provider preference when relevant.
- Distinguish preferences from hard constraints.
- Offer available alternatives if the first choice is unavailable.
- Confirm date, time, location, provider, and appointment type before completion.
- Escalate when symptoms or policy require staff involvement; do not provide medical advice.

### Rescheduling

- Identify the existing appointment before offering replacements.
- Preserve the original appointment until a replacement is selected and confirmed.
- Confirm both the appointment being changed and the replacement details.
- Avoid creating a duplicate appointment.

### Cancellation

- Identify the correct existing appointment.
- Confirm cancellation intent before completing it.
- State whether follow-up, rescheduling, or staff action is required.

### Medication refill

- Collect the medication, pharmacy, and other identifiers required by clinic policy.
- Avoid promising clinical approval or a completion time that the system cannot guarantee.
- Route or escalate clinical questions and urgent requests appropriately.
- Confirm what was submitted and explain the next step.

### Insurance

- Determine whether the caller is asking about accepted plans, updating coverage, eligibility, or a billing-related issue.
- Collect only information needed for the request.
- Avoid guaranteeing coverage or patient cost when verification is incomplete.
- Confirm what was updated, checked, or routed.

### Referrals and office information

- For referrals, identify the referral type, source, status, or destination and route unresolved cases.
- For office information, answer hours, location, directions, and department-routing questions directly when known.
- Distinguish general office information from patient-specific actions.

### After-hours or unavailable service

- State relevant availability or closure constraints.
- Offer the supported next step, alternate time, message, or escalation.
- Escalate urgent language according to clinic policy without diagnosing or giving medical advice.

## Predicted conversational branches

### Correction or changed information

- Acknowledge the correction explicitly.
- Replace the earlier fact rather than retaining contradictory versions.
- Restate the updated material details before confirmation.

### Unclear or conflicting intent

- Ask one focused clarification question at a time.
- Do not invent missing facts or silently choose between conflicting requests.
- Summarize the understood request once ambiguity is resolved.

### Interruption and barge-in

- Stop speaking promptly when interrupted.
- Preserve the conversation state and respond to the new information.
- Return to the unfinished decision only when still relevant.

### Refusal or unavailable information

- Explain why the information is needed or offer an allowed alternative.
- Do not trap the caller in repeated requests for the same unavailable fact.
- Escalate, defer, or end safely when the workflow cannot continue.

### Transfer or escalation

- Explain why escalation is needed and what will happen next.
- Preserve a concise summary so the caller should not need to repeat the entire request.
- Do not claim that a transfer, message, or action succeeded without confirmation.

### Misunderstanding and retry

- Acknowledge the mismatch and retry with a shorter, clearer question.
- Limit repeated attempts and change strategy rather than repeating identical wording.
- Offer escalation or a safe stop after the retry limit is reached.

### Silence, repeated loop, timeout, or hang-up

- Reprompt after a reasonable silence and state what information is still needed.
- Stop after the defined silence or loop limit rather than continuing indefinitely.
- Before an agent-initiated hang-up, summarize any completed action and unresolved next step when possible.
- Never report an action as complete if the call ends before confirmation.

## Predicted invariants

- Do not provide medical advice or diagnose symptoms.
- Do not fabricate availability, policy, patient data, or completed actions.
- Retain confirmed facts consistently across turns.
- Ask for confirmation before material scheduling, cancellation, or record changes.
- Use escalation when the request is outside the agent's authority or information is insufficient.
- Keep the conversation natural and actively steer toward the scenario's intended outcome.
- Treat marketing performance figures as unverified until measured from our own recordings and transcripts.

## Later comparison rule

Do not revise the predictions above after assessment calls begin. Create a separate observed map that cites exact call IDs, transcript turns, and recording timestamps. Differences between this baseline and observed behavior are iteration evidence, not errors to erase.
