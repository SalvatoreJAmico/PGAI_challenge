# Timestamp and Latency Measurement Convention

Use this convention for every call, transcript, per-turn observation, review, and bug reference.

## Time bases

- Store call start and end as UTC using ISO 8601 with milliseconds: `YYYY-MM-DDTHH:MM:SS.sssZ`.
- Use recording-relative timestamps for conversational evidence: `HH:MM:SS.mmm` from the beginning of the final two-sided recording.
- Use the same final recording as the timing source for transcripts, reviews, and bug references.
- Never combine provider wall-clock timestamps with recording-relative timestamps in one calculation.

## Turn boundaries

- **Speech start:** first intelligible speech sound belonging to the turn; exclude isolated background noise.
- **Speech end:** end of the final intelligible word before the speaker yields the floor.
- Treat a pause shorter than 500 ms inside one speaker's continuing thought as part of the same turn.
- Treat a pause of 500 ms or longer followed by the other speaker as a turn boundary.
- Record overlapping speech separately for both speakers rather than forcing one shared boundary.

## Response-start latency

For an ordinary response:

`response-start latency = PGAI speech start − patient speech end`

- Report in milliseconds, rounded to the nearest 10 ms.
- A negative result means PGAI began speaking before the patient finished; record it as overlap and preserve the negative value.
- Exclude patient-initiated silence before the patient finishes speaking.
- If the response is not audible or the boundary cannot be determined, record `not measurable` and explain why.

## Silence duration

- Measure silence from the end of the last intelligible speech to the start of the next intelligible speech.
- Label who was expected to respond: `patient`, `PGAI`, or `unclear`.
- Do not count hold music, audible processing messages, or a transfer announcement as silence; record those as separate events.
- Record silences of 1.0 second or longer in the per-turn observations.

## Interruption and barge-in timing

- Record the timestamp where the second speaker begins overlapping the first.
- Measure stop latency from the interruption start to the interrupted speaker's audible stop.
- If the original speaker continues for more than 500 ms after the interruption begins, flag the event for review.
- Distinguish intentional test interruption from accidental overlap.

## Transcript and evidence notation

- Transcript line: `[HH:MM:SS.mmm] SPEAKER: text`
- Interval: `[HH:MM:SS.mmm–HH:MM:SS.mmm]`
- Bug evidence: `Call ID, turn number, timestamp or interval`
- When transcript timing is generated automatically, verify material bug and latency timestamps against the audio manually.
- Record estimated timestamps with `~` and explain the source of uncertainty.

## Required call-level timing summary

- Call start UTC
- Call end UTC
- Total recording duration
- Median PGAI response-start latency
- Maximum PGAI response-start latency
- Longest unexplained silence
- Number of overlaps
- Number of intentional interruptions
- Number of timeouts
