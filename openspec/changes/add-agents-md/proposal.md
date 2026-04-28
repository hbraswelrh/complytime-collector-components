## Why

Every agent definition in `.opencode/agents/` references `AGENTS.md` as the first source document for project structure, active technologies, conventions, and build commands — but the file does not exist. This means all 18 agents operate without project-specific context, leading to inefficient codebase exploration, inaccurate assumptions about the build system (Go workspace monorepo, generated files, podman), and wasted tokens on every PR review, spec proposal, and implementation task.

## What Changes

- Create `AGENTS.md` at the repo root following the structure established in `org-infra`
- Populate all sections with current project state: structure, commands, constraints, active technologies, and recent changes
- Include critical constraints that prevent common agent mistakes (generated file boundaries, Go workspace rules, compass stub, podman-not-docker)

## Capabilities

### New Capabilities

- `agent-project-context`: AGENTS.md providing structured project context for AI agents, following the org-infra established format (Structure, Commands, Constraints, Commits, Active Technologies, Recent Changes)

### Modified Capabilities

_(none — no existing specs are affected)_

## Impact

- **AGENTS.md** (new file): Root-level project context document consumed by all agent definitions
- **Agent accuracy**: All 18 agents in `.opencode/agents/` will gain project-specific context on first read, reducing blind exploration and preventing mistakes with generated files, Go workspace commands, and container tooling
- **No code changes**: This change is documentation only — no Go source, tests, or CI modifications
