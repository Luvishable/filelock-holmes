# AGENTS.md — Minimal rules for this repo (Codex)

## Engineering standards
- Prioritize **Clean Code**, **SOLID**, and pragmatic **design principles** (high cohesion, low coupling, single responsibility, clear naming).
- Keep solutions simple first; refactor when duplication/complexity appears.
- Prefer maintainability over cleverness.

## Comments & docstrings
- Comments must be **precise, minimal, and useful** (no filler).
- Prefer explaining **intent, invariants, and non-obvious decisions**; do not restate obvious code.
- Code comments/docstrings in **English** by default (unless I ask otherwise).
- Explanations to me in **Turkish**.

## Git guidance (only at meaningful points)
Suggest branch/commit ONLY when it’s genuinely valuable, such as:
- A coherent feature/step is finished and runnable.
- A refactor that changes structure but keeps behavior.
- A bugfix with clear scope.
- A docs/planning milestone.

When suggesting:
- Provide **one** branch name (if needed) and **one** commit message (Conventional Commits).
- Do NOT encourage frequent micro-commits.

## Dependency/API freshness (be strict)
- Use correct APIs for the **versions we actually use**.
- Source of truth: `pyproject.toml` + lock file (`uv.lock` or equivalent).
- If an API might differ by version, check the pinned version from repo files first.
- If unclear, ask me to confirm the installed version before coding against it.

## Planning workflow (architecture → sprints → steps)
- Read `docs/overview.md` to understand the architecture and main flow.
- Create/maintain the **Sprint outline** in `docs/SPRINTS.md`:
  - Sprint ID (S00, S01, ...)
  - Goal
  - In-scope / Out-of-scope
  - End-of-sprint deliverables (short)
- Do NOT plan all steps for all sprints upfront.

### Lazy step planning
- Steps are created **only when I say**: “Start Sprint Sxx”.
- For that sprint, add a small step list under its section in `docs/SPRINTS.md`.
- Each Step must have **one responsibility** and be small.
