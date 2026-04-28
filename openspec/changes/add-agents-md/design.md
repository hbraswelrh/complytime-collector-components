## Context

All 18 agent definitions in `.opencode/agents/` reference `AGENTS.md` as the primary source document for project context (structure, technologies, build commands, conventions). The file does not exist. Agents currently rely on ad-hoc codebase exploration, which is token-expensive and error-prone — particularly for generated file boundaries, Go workspace semantics, and container tooling choices.

The `org-infra` repository has an established AGENTS.md format that serves as the organizational template. This change adopts that format, adapted to the complexity of this Go workspace monorepo.

## Goals / Non-Goals

**Goals:**

- Create a single `AGENTS.md` file at the repo root that all agents can read for immediate project context
- Follow the org-infra established structure (Structure, Commands, Constraints, Commits, Active Technologies, Recent Changes)
- Include all critical constraints that prevent common agent mistakes (generated files, Go workspace, compass stub, podman)
- Keep the file concise (~80 lines) to minimize context window consumption

**Non-Goals:**

- Duplicating content from `docs/DESIGN.md`, `docs/DEVELOPMENT.md`, or `.specify/memory/constitution.md` — AGENTS.md cross-references these instead
- Documenting every Makefile target — only the ~10 targets agents need are listed, with a pointer to `make help`
- Covering agent definitions or convention packs — those are managed by `uf` and are out of scope

## Decisions

### 1. Follow org-infra's AGENTS.md section structure

**Decision**: Use the same sections as org-infra (Structure, Commands, Constraints, Commits, Active Technologies, Recent Changes, Manual Additions) rather than inventing a new format.

**Rationale**: Consistency across ComplyTime repositories means agents (and the divisor-scribe) already understand the format. The structure is proven to work and covers all the sections agents reference.

**Alternatives considered**: A component-focused structure (one section per module) was considered but rejected — it would duplicate what `docs/DESIGN.md` already covers and agents don't need per-component deep dives; they need project-wide context.

### 2. Directory tree at 2 levels with annotations

**Decision**: Show the directory tree 2 levels deep with inline annotations describing each directory's purpose. Omit individual files except generated ones called out in Constraints.

**Rationale**: Agents need to know where things are and what each directory does, but not every file. Deeper detail is available in `docs/DEVELOPMENT.md`.

### 3. Constraints section as the primary error-prevention mechanism

**Decision**: Give the Constraints section the most detail, explicitly calling out: generated file boundaries with regeneration commands, Go workspace rules, compass stub status, podman-not-docker, and lint configuration pointers.

**Rationale**: Agent investigation during explore mode revealed these are the exact categories where agents make costly mistakes without upfront context. Each constraint directly prevents a class of errors.

### 4. Active Technologies as a categorized snapshot

**Decision**: List technologies grouped by role (core language, key libraries, codegen tooling, build/CI, containers) with version numbers from current `go.mod` files.

**Rationale**: The divisor-architect and divisor-sre agents specifically look for Active Technologies to validate that changes use compatible tools. Versions help agents verify dependency compatibility.

### 5. Cross-reference deep docs instead of inlining

**Decision**: Include a brief "Standards" entry in Constraints pointing to `docs/DESIGN.md` (architecture), `docs/DEVELOPMENT.md` (dev setup), and `.specify/memory/constitution.md` (coding standards).

**Rationale**: Keeps AGENTS.md lean. Agents that need deeper context can follow the references. Avoids content duplication that would create maintenance burden.

## Risks / Trade-offs

- **Staleness risk**: AGENTS.md requires manual updates when technologies, commands, or structure change. → Mitigated by divisor-guard and divisor-curator agents, which both check "Was AGENTS.md updated?" during reviews. The Recent Changes section also provides a natural prompt to update.
- **Incomplete coverage**: The file may miss constraints that haven't been discovered yet. → Mitigated by the Manual Additions section where developers can add project-specific notes, and by iterative refinement as agents surface new failure modes.
- **Go version drift**: The go.mod versions listed in Active Technologies will drift as dependencies update. → Mitigated by listing major versions (e.g., "OTel Collector SDK v1.56.0") rather than patch versions, and relying on agents to check `go.mod` directly for exact versions when needed.
