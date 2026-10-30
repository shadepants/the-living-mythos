# Claude Extensions for a Deterministic Civilization Sandbox: What to Install, Build, and Skip

Research report, 2026-10-23 (Claude research task). Not yet reviewed in a planning chat.

---

The best setup for this project is a small official core plus a few project-specific pieces you write yourself. The core is the official PixiJS skill pack, the fast-check maintainer's testing skill, Anthropic's official plugin marketplace (hookify, typescript-lsp, a review toolkit), and Google's Chrome DevTools MCP. On top of that, write your own hooks, a determinism-reviewer subagent, and a determinism skill. No vendor ships those last three, and they are where most of the value for this project is. While you are phone-only, the highest-leverage tool is Claude Code cloud sessions launched from the mobile app's Code tab. They can scaffold and test the pnpm monorepo in a cloud VM before the laptop comes back.

## TL;DR

- **Install now (official, verified):** pixijs/pixijs-skills, which has 25 skills: 24 topic skills plus one `pixijs` router. That settles the 25-vs-26 question. Also install dubzzz/fast-check's `javascript-testing-expert` skill, antfu's docs-generated `vitest` and `pnpm` skills, and Chrome DevTools MCP for canvas screenshots, console checks and performance traces. From `claude-plugins-official` (registered automatically), install hookify, pr-review-toolkit or code-review, and claude-md-management.
- **Build yourself (highest value):** hooks that run ESLint, typecheck and Vitest after edits to `sim-core`, a read-only `determinism-reviewer` subagent, and a project skill that encodes your RNG, ID, and event-log rules. No vendor or community extension covers counter-based RNG, fork-and-diff, or bitECS determinism. The only bitECS skill found is an unvetted community one.
- **Watch out:** third-party skills are a real supply-chain risk. Snyk Security Labs (February 2026) confirmed 76 malicious payloads among 3,984 skills on clawhub.ai and skills.sh. On Windows, the official TypeScript LSP plugin has open bugs (npm `.cmd` shims cannot be spawned). Run hooks as Node `.mjs` scripts or set `"shell": "powershell"`. OS-level sandboxing requires WSL 2.

## Key Findings

1. **The PixiJS pack is the only official, library-maintainer skill set that covers your render layer, and it has 25 entries.** The README table lists `pixijs` (described as "Entry point and router") plus 24 topic skills, from `pixijs-accessibility` through `pixijs-ticker`. The figure of 26 is probably a stale or miscounted listing. As of today the repo is MIT-licensed with 356 stars, 19 forks and only 5 commits. The awesomeclaudeplugins tracker shows it was created April 1, 2026 and last pushed June 4, 2026. So it is maintained by the PixiJS org but updated infrequently. Two of its skills matter more than you might expect. `pixijs-environments` covers Web Workers and OffscreenCanvas, which affects your sim-worker/viewer split. `pixijs-performance` covers culling, batching, pooling and resolution trade-offs.

2. **Property-based testing has two credible skills, one from the library's own maintainer.** dubzzz/fast-check ships `skills/javascript-testing-expert/SKILL.md`. It advocates property-based testing with fast-check, "protects against indeterministic code in tests," and recommends vitest, fast-check and @fast-check/vitest. fast-check's latest release is v4.10.2 (September 19, 2026). Trail of Bits' `property-based-testing` skill is broader and language-neutral. Its repo was updated October 22, 2026, has about 7.7k stars, and is licensed CC-BY-SA-4.0. Your invariants fit both skills well: population conservation, determinism (same seed and commands give the same state hash), snapshot round-trips, and fork independence.

3. **Docs-generated skills exist for pnpm, Vitest and Vite but not for bitECS, noise, or Web Workers.** antfu/skills generates `pnpm`, `vitest` and `vite` skills from the official doc repos. The skill metadata says they were generated on 2026-06-22, against pnpm 10.x (with pnpm 11 notes) and Vitest 5.x beta. They may describe newer APIs than the versions you pin. No official skill or MCP server was found for bitECS, simplex noise, or Web Workers/SharedArrayBuffer. That is a search result, not proof that none exist. Context7, which you already have, indexes bitECS docs, and it covers these gaps better than any community skill.

4. **For visually testing a canvas app, Chrome DevTools MCP beats Playwright MCP.** Google's server exposes `performance_start_trace`, `performance_stop_trace`, `performance_analyze_insight`, `take_screenshot`, `list_console_messages`, `evaluate_script`, Lighthouse, and memory heap snapshots. Its README says Google collects usage statistics and that performance tools "may send trace URLs to the Google CrUX API." Its latest verified release is v1.11.0 (October 15, 2026, per the GitHub release page), which added heap-snapshot context analysis, and releases come every few weeks. Playwright MCP (Microsoft, Apache-2.0, v0.0.83 released September 28, 2026) drives pages through accessibility snapshots by default. Those snapshots cannot see inside a WebGL canvas, so canvas work needs screenshots or the `--caps vision` mode. Use Playwright for UI-panel flows. Use DevTools for frame-time and console work.

5. **Your hard rules are best enforced by hooks plus ESLint, not by prompts.** The Claude Code hooks reference documents `PostToolUse`, exit-code feedback to Claude, and a per-hook `"shell": "powershell"` option. That option needs Claude Code v2.1.295 or later and auto-detects `pwsh.exe` before `powershell.exe`. A `PostToolUse` hook cannot undo an edit, but its stderr goes back to Claude, which then fixes the violation. The `Math.random` and transcendental-function bans belong in ESLint `no-restricted-properties` or `no-restricted-syntax` rules scoped to `packages/sim-core`, so they also apply to edits you make by hand. The hook just runs that lint.

6. **Subagents are plain Markdown files, and that makes a determinism reviewer cheap to build.** Files in `.claude/agents/` use YAML frontmatter (`name`, `description`, `tools`, `model`, and others). Omitting `tools` grants all tools. Plugin-supplied subagents ignore `hooks`, `mcpServers` and `permissionMode` for security reasons. Write your reviewer as a project file with `tools: Read, Grep, Glob` so it can read but never edit.

7. **Phone-only does not mean idle.** Claude Code cloud sessions can start from "the Code tab in the Claude mobile app." They clone a GitHub repo into an isolated VM and run an optional setup script. Per third-party guides that track the docs, the script runs as root on Ubuntu 24.04 and is cached as a snapshot. Remote Control, by contrast, only mirrors a session running on your own machine, so it is useless until the laptop returns. The official Excalidraw connector ("Anthropic verified," no sign-in, URL `https://mcp.excalidraw.com/mcp`) draws editable architecture diagrams inside claude.ai.

8. **Third-party extensions are a measured, current threat.** Snyk Security Labs ("Exploring the Threat Landscape of Agent Skills," February 5, 2026) analyzed 3,984 skills on clawhub.ai and skills.sh and confirmed 76 malicious payloads. 13.4% (534 skills) had at least one Critical issue, and 91% of the malicious skills also used prompt injection. Curated skills.sh skills showed negligible Critical findings. A separate study by Liu et al. (arXiv:2601.10338, January 2026) analyzed 31,132 skills and found 26.1% contain at least one vulnerability, with skills that bundle scripts 2.12x more likely to be vulnerable. Trail of Bits warns that published skills "have been found with backdoors and malicious hooks." Plugin hooks run code automatically, which makes them the riskiest component.

## Details by Project Phase

### Phase 0: Now (phone-only, Claude mobile app)

| Item | Type | Official? | Maintenance (verified) | What it does for this project | How to use | Risks |
|---|---|---|---|---|---|---|
| Claude Code cloud sessions (claude.ai/code, mobile Code tab) | Feature | Anthropic | Current docs, Oct 2026 | Scaffold the pnpm monorepo, ESLint determinism rules, and Vitest headless tests in a cloud VM. Review diffs and PRs from the phone. | Create an empty GitHub repo. Connect GitHub (Claude GitHub App). Pick the repo in the Code tab. Use a setup script that enables pnpm via Corepack and runs `pnpm install`. | Needs GitHub and a paid plan. The VM is Linux, so Windows-specific issues will not show up yet. Uses your plan's usage. |
| Claude Projects + Memory | Feature | Anthropic | Current | Keep the spec, architecture decisions and glossary (band, village, Legends record) as project knowledge, so planning chats stay consistent | Create a project and upload the spec, decision log and CLAUDE.md draft | Project knowledge does not sync with the repo's CLAUDE.md. Keep one source of truth (the repo). |
| Artifacts | Feature | Anthropic | Current | Throwaway worldgen previews (noise, biomes, fire spread) and Legends-text mockups, to test ideas before writing sim-core | Ask for a self-contained HTML/JS artifact | Artifact code is not deterministic or production-grade. Treat it as a sketch. Do not port `Math.random` code. |
| Excalidraw connector | MCP connector | Official (Excalidraw), Anthropic verified, added Feb 2026 | Active | Diagrams of the sim-core/worker/viewer split, the causal event graph, and the snapshot+command-log timeline | claude.ai Settings, Connectors, search "Excalidraw" (no sign-in) | Hosted service. Do not put secrets in diagrams. |
| Context7 (already connected) | MCP | Upstash (vendor) | Active | Live docs for PixiJS v8, bitECS, Vitest, fast-check | Already set up | Returned docs are third-party content and could carry an injection. Low risk. |
| algorithmic-art (installed) | Skill | Anthropic | In anthropics/skills | p5.js generative sketches for terrain or vegetation ideas | Use in artifacts only | p5.js is not your stack. Keep it out of the repo. |

### Phase 1: Spec phase (laptop back, before code)

| Item | Type | Official? | Maintenance (verified) | What it does for this project | Install (PowerShell / pnpm) | Risks |
|---|---|---|---|---|---|---|
| pixijs/pixijs-skills | Skill pack (plugin) | Official (PixiJS org), MIT | 356 stars, 5 commits, last push Jun 4, 2026 | Correct v8 patterns: async `init`, render groups, ParticleContainer, culling, workers/OffscreenCanvas | In Claude Code: `/plugin marketplace add pixijs/pixijs-skills`, then install from `/plugin`. Alternative: `pnpx skills add https://github.com/pixijs/pixijs-skills` | Updated infrequently. Cross-check against Context7 if PixiJS releases a new minor version. |
| claude-plugins-official: claude-md-management, claude-code-setup | Plugins | Anthropic first-party | Auto-registered marketplace | Keep CLAUDE.md lean and current. Get suggestions for hooks, skills and MCP servers from your codebase. | `/plugin install claude-md-management@claude-plugins-official` (same pattern for the other) | Low. Review what it proposes before accepting. |
| learning-output-style / explanatory-output-style | Plugins | Anthropic first-party | Auto-registered | Suits a hobbyist who wants to understand ECS, RNG, and replay design choices as they are made | `/plugin install learning-output-style@claude-plugins-official` | Slower sessions. Toggle off for routine edits. |
| skill-creator | Skill | Anthropic (anthropics/skills, ~183k stars, Apache-2.0) | Active | Author your own `determinism-rules` and `legends-narration` skills, with eval testing | `/plugin marketplace add anthropics/skills`, then install example-skills | None significant |
| spec-developer, grill, engineering:architecture (installed) | Skills | Mixed | Already installed | Stress-test the fork/replay design and the v1 success test before coding | Already installed | Keep using |
| Excalidraw MCP in Claude Code | MCP | Official | Active | Same diagrams, generated in the terminal | `claude mcp add --transport http excalidraw https://mcp.excalidraw.com/mcp` | In the terminal you only get a link, not the inline canvas |

### Phase 2: First vertical slice (drought, fork, Legends explanation)

| Item | Type | Official? | Maintenance (verified) | What it does for this project | Install (PowerShell / pnpm) | Risks |
|---|---|---|---|---|---|---|
| fast-check `javascript-testing-expert` | Skill | Official (maintainer dubzzz) | fast-check v4.10.2, Sep 19, 2026 | Property tests for determinism, conservation, snapshot round-trip, and fork-and-diff invariants | `pnpx skills add dubzzz/fast-check --skill javascript-testing-expert`, or copy the folder into `.claude/skills/` | It suggests installing tooling. Approve each dependency yourself. |
| Trail of Bits `property-based-testing` | Skill | Vendor (security firm), CC-BY-SA-4.0 | Repo updated Oct 22, 2026, ~7.7k stars | Reviewing whether your property tests actually assert anything. Interpreting shrunk counterexamples. | `/plugin marketplace add trailofbits/skills` | Overlaps the fast-check skill. Pick one as primary to avoid conflicting advice. |
| antfu `vitest`, `pnpm` skills | Skills | Community-curated (Vite/Vitest core team member), generated from official docs | Generated 2026-06-22 | Workspace config, catalogs, `--frozen-lockfile`, Vitest projects/filters for a monorepo | `pnpx skills add antfu/skills --skill vitest` (same for `pnpm`) | Based on Vitest 5.x beta, which may not match the version you pin. License and stars not verified. |
| typescript-lsp | Plugin | Anthropic first-party | Open Windows bugs (#17718, #32338) | Type-aware navigation and diagnostics in a strict TS monorepo | `/plugin install typescript-lsp@claude-plugins-official` plus `typescript-language-server` on PATH | **Windows: fails with `spawn ... ENOENT` because npm/pnpm `.cmd` shims cannot be spawned without a shell.** Community proxy workaround exists. Otherwise rely on `pnpm -r exec tsc --noEmit` in hooks. |
| hookify | Plugin | Anthropic first-party | Auto-registered | Build hooks from plain-language rules | `/plugin install hookify@claude-plugins-official` | Check the generated hook commands for Windows compatibility |
| Project hooks (your own) | Feature | You | n/a | Run ESLint (determinism bans) and typecheck after edits to sim-core. Run Vitest on Stop. | `.claude/settings.json` with Node `.mjs` scripts (see below) | Hooks run with your user permissions. Keep them in git and review them. |
| `determinism-reviewer` subagent (your own) | Feature | You | n/a | Read-only review of diffs for wall-clock use, iteration-order dependence, float transcendental functions, unkeyed RNG, and unstable IDs | `.claude/agents/determinism-reviewer.md` | None. Read-only by design. |
| Chrome DevTools MCP | MCP | Official (Google) | v1.11.0 (Oct 15, 2026), ~52.8k stars | Screenshot the PixiJS canvas, read console errors, trace frame time during a drought run, take heap snapshots for typed-array leaks | `claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest` (on Windows you may need the `cmd /c` wrapper; see Caveats) | Collects usage statistics. Can read and modify anything in the browser profile, so use a dedicated profile. |
| pr-review-toolkit or code-review | Plugin | Anthropic first-party | Auto-registered | Second-pass review before merging slices | `/plugin install pr-review-toolkit@claude-plugins-official` | Usage cost |

### Phase 3: Later (scale, polish, analysis)

| Item | Type | Official? | Maintenance (verified) | What it does for this project | Install | Risks |
|---|---|---|---|---|---|---|
| Playwright MCP | MCP | Official (Microsoft), Apache-2.0 | v0.0.83, Sep 28, 2026 | Scripted UI-panel flows (trigger drought, fork, open Legends) and regression screenshots | `claude mcp add playwright -- npx @playwright/mcp@latest` | Accessibility snapshots cannot see canvas content. Needs `--caps vision` or screenshots. |
| anthropics `webapp-testing` | Skill | Anthropic | In anthropics/skills | Playwright-based local app testing with console log capture | Via anthropics/skills marketplace | Its example scripts are Python, which adds a Python dependency. Prefer Chrome DevTools MCP. |
| GitHub MCP (remote) | MCP | Official (GitHub) | Hosted at api.githubcopilot.com/mcp/ | Issues and PRs from inside sessions | `claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer $env:GITHUB_PAT"` | Needs a PAT. Use a fine-grained, repo-scoped one. `gh` CLI is usually enough for a solo project. |
| Remote Control | Feature | Anthropic | Since v2.1.52 | Steer a long laptop session (bulk refactor, perf pass) from your phone | `claude remote-control` or `/rc` | Laptop must stay on. One remote session per instance. |
| Claude-built analysis artifacts | Feature | Anthropic | Current | Plot exported run CSV/JSON (population by band, vegetation index, migration events) to compare forks | Export from a Vitest script, upload to claude.ai | No simulation-specific analysis MCP was found. A data or notebook MCP was not researched. |

### Recommended project-owned configuration (inference, based on the verified docs)

**Hooks (`.claude/settings.json`).** Use Node scripts so the same file works on Windows, Linux cloud VMs, and anywhere else:

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Edit|Write",
        "hooks": [{ "type": "command",
          "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/check-sim-core.mjs\"" }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "command",
          "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/run-tests.mjs\"" }] }
    ]
  }
}
```

`check-sim-core.mjs` reads the hook JSON from stdin. If `tool_input.file_path` is under `packages/sim-core`, it runs `pnpm exec eslint <file>` and `pnpm -F sim-core exec tsc --noEmit`, then exits 2 with the errors on stderr so Claude fixes them. `run-tests.mjs` runs `pnpm -F sim-core exec vitest run --reporter=dot`. Before relying on `$CLAUDE_PROJECT_DIR` expansion under PowerShell, test it. If it breaks, set `"shell": "bash"` (Git Bash) or resolve the path inside the script.

**Subagent (`.claude/agents/determinism-reviewer.md`).** Frontmatter: `name: determinism-reviewer`, a description saying "Use after any change to packages/sim-core," `tools: Read, Grep, Glob`. The body is a checklist:
- No `Math.random`, `Date.now`, or `performance.now` in sim-core.
- No `Math.sin`, `exp`, or `pow` with non-integer arguments in sim-core.
- RNG calls keyed by (seed, tick, entity, purpose).
- No `Map`/`Set` iteration feeding sim state unless insertion order is deterministic.
- IDs derived from lineage.
- Every state mutation emits an event with a parent cause.
- Substep counts are fixed.

**Project skill (`.claude/skills/determinism-rules/SKILL.md`).** Write it with skill-creator. It encodes the RNG API, the event-log schema, and the Legends narration templates, so every session, cloud or local, inherits them.

## Skip List

| Item | Reason |
|---|---|
| freshtechbro/claudedesignskills `pixijs-2d` | Community content that duplicates the official pack, with less depth and no maintainer accountability |
| arimxyer/toolchest `pixijs` plugin | Community repackaging of PixiJS guidance. The official pack makes it redundant. |
| "PixiJS Vector Arcade Starter" (mcpmarket) | 1 GitHub star. An arcade ECS-lite template that does not match your observational sim. |
| Kadajett/bitECS-agent-skill | Unvetted community skill, quality and safety unreviewed. Context7's bitECS docs are safer. Only consider it after a full manual read. |
| @executeautomation/playwright-mcp-server | Community fork. Use Microsoft's `@playwright/mcp`. |
| `@modelcontextprotocol/server-github` (old npm) | Deprecated. GitHub ships an official hosted server. |
| anthropics/knowledge-work-plugins (sales, legal, finance, and so on) | Not relevant to a game or simulation codebase |
| ralph-loop | Runs Claude in a loop until done. Poor fit for a hobbyist usage budget and for careful determinism work. |
| adversarial-plan / adversarial-review | Requires Codex. Use pr-review-toolkit plus your determinism reviewer instead. |
| Community Excalidraw MCP (yctimlin/mcp_excalidraw) | Only worth it if you need a live, agent-editable canvas. The official connector covers diagramming. |
| Third-party phone SSH apps (e.g., ServerCC) | Unofficial, and they handle SSH keys. Cloud sessions and Remote Control cover the same need officially. |

## Vetting Checklist for Third-Party Skills, Plugins and MCP Servers

1. **Publisher identity:** Is it from the library maintainer's org (pixijs, dubzzz, microsoft, ChromeDevTools, github) or from Anthropic's `claude-plugins-official`? If not, treat it as untrusted.
2. **Activity and adoption:** Check the last commit or release date, open issues, stars and forks, and whether issues get answered. A large star count with few commits is a weak signal.
3. **License:** It must be present and compatible. Note that Anthropic's document skills are source-available, not open source, and Trail of Bits skills are CC-BY-SA-4.0.
4. **Read every file before installing:** SKILL.md, `references/`, any `scripts/`, plus `plugin.json`, `marketplace.json`, and `hooks/`. Look for instructions such as "do not mention this to the user," encoded blobs, `curl | sh`, downloads, or network calls.
5. **Hooks and MCP declarations in plugins:** These execute automatically. Reject any plugin that ships hooks you did not ask for.
6. **MCP server scope:** Prefer local stdio servers from official packages, pinned to a version (`@playwright/mcp@0.0.83`, not `@latest`, once stable). Give tokens the narrowest scope. Run browser MCPs against a dedicated browser profile.
7. **Telemetry:** Check the README for data collection. Chrome DevTools MCP collects usage statistics and may query CrUX.
8. **Overlap:** Do not stack two skills on the same topic, such as two PixiJS packs or two PBT skills. Conflicting instructions degrade output.
9. **Re-check on update:** Review the marketplace diff before updating plugins. A trusted repo can be compromised later.
10. **Prefer writing your own:** For anything core to your architecture (determinism, event log, IDs), a short project skill you wrote yourself beats any community skill.

## Caveats

- **Windows specifics (verified):** Git for Windows has been optional since Claude Code 2.1.120 (April 28, 2026). Without it, commands run through the PowerShell tool, which does not load PowerShell profiles. With it, the PowerShell tool is still on by default for claude.ai accounts. OS-level sandboxing is not supported on native Windows, only WSL 2. The TypeScript LSP plugin has unresolved `.cmd`-shim spawn failures on Windows. The same shim problem likely affects stdio MCP servers launched via `npx` or `pnpm dlx`. Wrapping the command with `cmd /c` is the usual fix, but that is inference to verify on your machine.
- **npm vs pnpm:** Several official install lines use `npx`. `pnpx`/`pnpm dlx` is the pnpm equivalent and works for the skills CLI (antfu documents `pnpx skills add`). For MCP servers, `pnpm dlx` should work in place of `npx`, but this was not tested on Windows.
- **Counts and metrics:** Star counts came from search snippets and trackers, not live API calls, so treat them as approximate. Official marketplace plugin counts conflict across trackers: "more than 200" as of July 2026, 222, and 274. Use the `/plugin` Discover view as ground truth.
- **Unverified gaps:** No maintainer-published skill or MCP was found for bitECS, procedural noise, or Web Workers. No simulation- or game-dev-specific MCP server was identified. Data and notebook MCPs for analyzing runs were not researched.
- **Hardware note (inference):** On an i7-8665U with integrated graphics, Chrome DevTools traces of a PixiJS app plus a Web Worker sim are useful but noisy. Compare traces relative to each other on the same machine, not against absolute numbers.

## Sources
- https://github.com/anthropics/claude-code/issues/17718
- https://github.com/melodic-software/claude-code-plugins/issues/3537
- https://github.com/anthropics/claude-code/issues/32338
- https://dev.to/aicoding-guide/claude-code-on-windows-native-or-wsl-and-what-trips-people-up-3em3
- https://github.com/pixijs/pixijs-skills
- https://awesomeclaudeplugins.com/pixijs/pixijs-skills
- https://github.com/dubzzz/fast-check/blob/main/skills/javascript-testing-expert/SKILL.md
- https://github.com/dubzzz/fast-check/releases
- https://github.com/trailofbits
- https://github.com/trailofbits/skills/blob/main/plugins/property-based-testing/skills/property-based-testing/SKILL.md
- https://www.skillsdirectory.com/skills/onmax-vitest
- https://skillsmp.com/creators/antfu/skills/skills-vitest
- https://github.com/antfu/skills
- https://www.sofarbot.com/skills/antfu-skills-pnpm
- https://agnxi.com/antfu/skills/pnpm
- https://deepwiki.com/antfu/skills
- https://context7.com/natethegreatt/bitecs
- https://addyosmani.com/blog/devtools-mcp/
- https://promptic.us/mcp/servers/chrome-devtools
- https://github.com/ChromeDevTools/chrome-devtools-mcp
- https://github.com/microsoft/playwright-mcp/releases
- https://mcp.directory/blog/playwright-browser-mcp-guide-2026
- https://roundproxies.com/blog/playwright-mcp/
- https://code.claude.com/docs/en/hooks
- https://dev.to/alexcloudstar/claude-code-hooks-every-event-the-config-format-and-five-working-examples-ef8
- https://code.claude.com/docs/en/sub-agents
- https://hidekazu-konishi.com/entry/claude_code_subagents_and_orchestration_guide.html
- https://claudcod.com/blog/claude-code-subagents/
- https://code.claude.com/docs/en/claude-code-on-the-web
- https://support.claude.com/en/articles/12618689-use-claude-code-in-the-cloud
- https://replicas.dev/resources/claude-code-cloud-sessions
- https://datasciencedojo.com/blog/claude-code-remote-control/
- https://www.helpnetsecurity.com/2026/02/25/anthropic-remote-control-claude-code-feature/
- https://claude.com/connectors/excalidraw-app-demo
- https://github.com/trailofbits/skills-curated
- https://stacknotice.com/blog/claude-projects-memory-guide-2026
- https://deepwiki.com/anthropics/claude-code/4-official-plugins
- https://awesomeclaude.ai/awesome-claude-skills
- https://claude-world.com/articles/anthropic-official-skills-complete-guide/
- https://www.paralect.com/mcp/excalidraw
- https://www.skills.sh/dubzzz/fast-check
- https://github.com/orgs/trailofbits/repositories
- https://gist.github.com/thorn0/1d8df18a0aee9c128447407659fa15e3
- https://www.petegypps.uk/blog/claude-code-official-plugin-marketplace-complete-guide-36-plugins-december-2025
- https://github.com/anthropics/claude-plugins-official/tree/main/plugins
- https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md
- https://www.deployhq.com/blog/best-mcp-servers-for-web-developers
- https://www.nxcode.io/resources/news/claude-code-remote-control-mobile-terminal-handoff-guide-2026
- https://github.com/freshtechbro/claudedesignskills/blob/main/MARKETPLACE.md
- https://github.com/arimxyer/toolchest
- https://mcpmarket.com/tools/skills/pixijs-vector-arcade-starter
- https://skills.lc/Kadajett/bitECS-agent-skill/kadajett-bitecs-agent-skill-skill-md
- https://github.com/antonzherdev/mcp-playwright
- https://www.aibuilderclub.com/blog/claude-code-plugins-official-library-2026
- https://www.claudepluginhub.com/marketplaces/anthropics-claude-plugins-official
- https://github.com/yctimlin/mcp_excalidraw
- https://apps.apple.com/us/app/servercc-remote-claude-code/id6759306046
- https://github.com/anthropics/skills
- https://swapbiswas.com/blog/claude-code-wsl-vs-windows/
- https://code.claude.com/docs/en/setup
- https://github.com/antfu/skills/blob/main/README.md
- https://designrevision.com/blog/official-claude-code-plugins
- https://claudemarketplaces.com/plugins/anthropics-claude-plugins-official
