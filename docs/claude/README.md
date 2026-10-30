# Living mythos: Project index

Read order for a new chat: this file, then `design/decision-log.md`, then `claude/handoff-living-mythos.md`.

## Folders
| Folder | Holds | Who writes |
|---|---|---|
| `design/` | Settled decisions; later the spec | Claude proposes, Jordan approves |
| `research/` | Gemini prompts and the reports they produce | Claude writes prompts; Jordan uploads reports |
| `claude/` | Handoff, project instructions, working notes | Claude |
| `archive/` | Closed or fully absorbed docs, kept for evidence and unscheduled ideas. Not part of the read order | Claude, with a status note at the top of each |

## Documents (current)
| Path | Status |
|---|---|
| `design/decision-log.md` | Current (rev 14). Source of truth |
| `claude/handoff-living-mythos.md` | Current (handoff #5) |
| `claude/next-steps-prompts.md` | 2026-10-30: prompt A (laptop tooling setup), prompt B (grill spec v0.1), later triggers; each with Claude's suggested option |
| `design/spec_v0.1.md` | Draft v0.2 (2026-10-30; file name kept); 4 bugs fixed; open questions grilled in the order of section 20 |
| `claude/project-instructions.md` | Copy of the Project custom instructions; updated 2026-10-28; needs pasting into Project settings |
| `research/gemini-prompts.md` | All prompts (1-6) run; consolidated 2026-10-28 (includes the former novelty prompt) |
| `research/pixel-art-review-2026-10-24.md` | Review of prompt 6; partly adopted (rev 8); remaining items settle during the spec |
| `research/tooling-report.md` | Final; cloud sessions decided (rev 10); PBT skill choice and other installs still open |
| `research/novelty-report-gemini.txt` | Prompt 1 report; reviewed; spot-check caveats in decision log |
| `research/timescale-report.md` | Final |
| `research/stack-and-prior-projects-report.md` | Final; threading/tick advice superseded by timescale report |
| `Procedural Pixel Art Simulation Research.pdf` | Gemini prompt 6; reviewed |
| `World and History Simulation Architecture.pdf` | Gemini prompt 2; reviewed |
| `Prehistoric Observational Simulation Design.pdf` | Gemini prompt 3; reviewed (ranges usable, equations not) |
| `Procedural History Narration Pipeline.pdf` | Gemini prompt 4; reviewed |
| `Comparative Simulation Visualization Framework.pdf` | Gemini prompt 5; reviewed; shelved with forks |
| `Open Source Repositories for Civilization Simulati....pdf` | Extra Gemini report; reviewed |

PDFs are Project file uploads; this tool can't move them into `archive/`. Jordan can remove or re-upload them in claude.ai if wanted.

## Archive
| Path | Why archived |
|---|---|
| `archive/research/batch-review-2026-10-23.md` | Review of prompts 2-5 + repos; proposals adopted into the decision log (with changes noted at its top). Kept for spot-check evidence |
| `archive/design/spec-rough-draft-gemini-2026-10-30.md` | Gemini agent's rough spec, not adopted; input for the grilling (status note at its top). The repo also keeps its proposed rev 14 log diff |
| `archive/design/depth-and-visuals-brainstorm.md` | All questions closed (rev 8-11). Kept for unscheduled ideas: lore, dig tool, kinship drift, named herds, foreshadowing, event flares, time ribbon |

Removed 2026-10-28: `research/novelty-research-prompt.md` (content merged into `research/gemini-prompts.md` as prompt 1).

## Naming
- Gemini reports: `research/<topic>-report-gemini.md` (or `.txt` if pasted raw).
- New design docs: `design/<topic>.md`. The spec will be `design/spec_v0.1.md`, versioned on change; first version covers the success-test slice only.
- Archiving: move to `archive/<original folder>/<name>`, add a dated status note at the top, update this index and any references in the decision log and handoff.

## Code
Repo: github.com/shadepants/the-living-mythos (private), branch `Main-REPO` (pnpm workspace, `packages/sim-core` only). Its `CLAUDE.md` carries the code-binding rules for Claude Code; `CONTEXT.md` tracks code state. Laptop clone: `C:\Users\User\Workspace\Repositories\the-living-mythos`.

**Repo mirror:** `docs/` in the repo mirrors this Project (same paths, plus the PDFs under `docs/research/`). The Project is the source of truth. After every decision-log revision, or any change to a doc here, re-sync the changed files to `docs/` in one `docs:` commit.

Cloud sessions stay limited to tests and tooling until the rev 10 gate is decided (Windows `pnpm check` passed 2026-10-30; see the decision log's open questions).
