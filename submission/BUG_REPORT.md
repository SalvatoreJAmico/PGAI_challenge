# Bug Report

Document issues discovered during test calls here.

## PGAI-001: Suspected PGAI-side speech interruption during the opening greeting

- **Severity:** Medium — the opening greeting appears incomplete, though the call continued.
- **Call:** `S02-A01-20260831T222747Z` — appointment rescheduling, August 31, 2026.
- **Timestamp:** `00:00:10.400–00:00:12.250` in the Twilio `two-sided-audio.mp3` recording (approximately 1.85 seconds).
- **Details:** Human listening review by Salvatore identified the foreground voice cutting off around the mention of PGAI, with “How may I help you today?” reported missing. He reported that background call-center audio remained audible while the voice stopped and that the cutoff was present in multiple recording sources.
- **Corroborating evidence:** Signal analysis found the same low-level interval in the Twilio recording and the aligned LiveKit export (`observability-RM_A2pto9ardAzX.zip`). The corresponding LiveKit interval is `00:00:09.220–00:00:11.090` (approximately 1.87 seconds on its separate recording clock). Audio immediately after the gap closely matches across both sources. Our patient agent produced no speech during the gap.
- **Assessment:** Suspected interruption of PGAI foreground speech generation or playback. The reported continuing background audio and matching gap across sources favor this explanation over a complete audio-connection dropout or a problem confined to our LiveKit input settings. The internal cause is unconfirmed; upstream media issues are not ruled out.
- **Evidence limitation:** LiveKit's automatic transcript includes “How may I help you today?”; this does not establish that every word was audible. Phrase-level loss and continuing background sound are human observations, while the gap timing and cross-recording match were measured. This is one call captured by two recording sources, not two independent reproductions.
- **Expected behavior:** PGAI delivers its complete opening greeting and question without an unintended foreground speech cutoff.
- **Status:** Open — reported from existing evidence; no settings change or follow-up test call performed.
- **Private evidence:** `.local/candidates/S02-A01-20260831T222747Z/livekit-twilio-comparison.md`, `two-sided-audio.mp3`, and the preserved `livekit-export/` directory. Audio and detailed session evidence are retained locally and are not included in this public report.

## Issue Template

- **Bug:**
- **Severity:**
- **Call:**
- **Details:**
- **Expected behavior:**
