# Prompts Directory

This folder contains the system prompts for the dual-judge evaluation system.

## Files

- **judge_triage_christian.md** - Primary judge prompt (used for the main CTTAF scores). Applies Mohler/Ortlund triage strictly (Primary/Secondary/Tertiary), scores the three official dimensions (Doctrinal Accuracy & Fidelity, Internal Coherence with triage hierarchy, Pastoral Sensitivity & Application), and references the official rubric.
- **judge_pluralistic_baseline.md** - Pluralistic/neutral baseline judge (helpfulness, logical coherence, avoidance of harm; no specific Christian doctrinal priors).

Current evaluation code loads the full triage prompt and augments it with per-question Rank + Subtopic + the actual model response. The 3-dimension + triage model is authoritative (see rubric/ and appendices/judge_instructions_full.md for the reconciled current version; older 5-dimension text is retained only for history).

The prompts guide judges to:
- Apply triage weights and strictness correctly (Primary failures are grave).
- Allow legitimate Secondary diversity while penalizing flattening or evasion.
- Evaluate pastoral wisdom on scenario questions, not just abstract correctness.
- Never soften or relativize gospel essentials.

See `rubric/cttaf_rubric_v1.0.md`, `appendices/judge_instructions_full.md`, and the generator/README sections for the full picture.
