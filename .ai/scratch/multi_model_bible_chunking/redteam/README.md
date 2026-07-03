# Red-Team / Pre-Mortem — T423 Fork

**Status:** fixes applied — see `REDTEAM_PREMORTEM_REPORT.md`; compare script + validators landed; ready for set-and-forget M1 marathon start after owner OK.

## Instructions for reviewer AI

1. Open and follow **every step** in:
   ```
   .ai/prompts/multi_model_whole_bible_chunking_redteam_premortem_prompt.md
   ```
2. Write your report here:
   ```
   .ai/scratch/multi_model_bible_chunking/redteam/REDTEAM_PREMORTEM_REPORT.md
   ```
3. Do **not** chunk the Bible. Review only.
4. End with verdict: `GO` | `HOLD` | `ABANDON_FORK`

## Owner handoff (paste to another AI)

Copy this block into a new chat with Codex, Claude, or Gemini:

---
You are an independent red-team reviewer for the Logos Scripture Graph repo.

Read and execute exactly:
`.ai/prompts/multi_model_whole_bible_chunking_redteam_premortem_prompt.md`

Write output to:
`.ai/scratch/multi_model_bible_chunking/redteam/REDTEAM_PREMORTEM_REPORT.md`

Assume the fork already failed in 30 days — write the pre-mortem narrative explaining how.
Attack all attack surfaces A–H in the prompt.
Verdict must be GO, HOLD, or ABANDON_FORK with minimum fixes before any marathon starts.

Do not chunk the Bible. Do not write canon surfaces. Read-only review except your report file.
---

## After review

Owner reads report → if GO or HOLD with fixes, apply minimum fixes → then start M1 marathon only.
