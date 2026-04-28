## ADDED Requirements

### Requirement: AGENTS.md provides project structure
The AGENTS.md file SHALL contain an annotated directory tree showing all top-level directories and their purpose, to a depth of 2 levels. Each directory entry SHALL include an inline comment describing its role.

#### Scenario: Agent reads project structure
- **WHEN** an agent reads the Structure section of AGENTS.md
- **THEN** the agent can identify the location and purpose of every top-level directory without additional codebase exploration

#### Scenario: New directory added to project
- **WHEN** a new top-level directory is added to the project
- **THEN** the Structure section MUST be updated to include it with an annotation

### Requirement: AGENTS.md lists essential build commands
The AGENTS.md file SHALL list the make targets that agents need for testing, linting, code generation, and deployment. Each command SHALL include a brief inline description. The list SHALL NOT include all Makefile targets — only those relevant to agent workflows. A pointer to `make help` SHALL be included for discovering additional targets.

#### Scenario: Agent needs to run tests
- **WHEN** an agent needs to verify code changes
- **THEN** the Commands section provides the exact `make` invocations for testing, linting, and CRAP score checks

#### Scenario: Agent needs to regenerate code
- **WHEN** an agent modifies semantic convention model files or OpenAPI specs
- **THEN** the Commands section provides the exact `make` invocations for code regeneration

### Requirement: AGENTS.md declares generated file boundaries
The Constraints section SHALL list every generated file in the repository with its full path and the command to regenerate it. The list SHALL use explicit "DO NOT EDIT" language.

#### Scenario: Agent encounters a generated file
- **WHEN** an agent considers editing `proofwatch/attributes.go`, `truthbeam/internal/applier/attributes.go`, `truthbeam/internal/client/client.gen.go`, or `docs/attributes/*.md`
- **THEN** the Constraints section informs the agent that these are generated files and provides the regeneration command

#### Scenario: Agent reviews a PR that modifies generated files
- **WHEN** a review agent encounters changes to a generated file in a PR diff
- **THEN** the agent can verify whether the change was produced by the correct generation command

### Requirement: AGENTS.md documents workspace and tooling constraints
The Constraints section SHALL document: Go workspace semantics (no root go.mod, module iteration pattern), the compass stub status and its external repository, container tooling (podman not docker), lint configuration pointers, and a cross-reference to deep documentation and constitution.

#### Scenario: Agent attempts to run Go commands from root
- **WHEN** an agent attempts `go test ./...` from the repository root
- **THEN** the Constraints section has already informed the agent that this will not work and to use `make test` instead

#### Scenario: Agent references docker
- **WHEN** an agent generates container-related commands
- **THEN** the Constraints section has already informed the agent to use podman, not docker

### Requirement: AGENTS.md lists active technologies with versions
The Active Technologies section SHALL list all languages, frameworks, key libraries, code generation tools, build/CI tools, and container stack components used in the project, with version numbers sourced from `go.mod` and build configuration files.

#### Scenario: Agent evaluates a new dependency
- **WHEN** an agent or reviewer evaluates whether a new dependency is compatible
- **THEN** the Active Technologies section provides the current technology stack for comparison

### Requirement: AGENTS.md tracks recent changes
The Recent Changes section SHALL list completed openspec changes with their name and a brief summary of what changed. Entries SHALL follow the pattern established in org-infra's AGENTS.md.

#### Scenario: Agent needs context on recent modifications
- **WHEN** an agent needs to understand what has recently changed in the project
- **THEN** the Recent Changes section provides a concise log of completed changes

### Requirement: AGENTS.md follows org-infra format
The AGENTS.md file SHALL follow the section structure established in the org-infra repository: title and description, Structure, Commands, Constraints, Commits, Active Technologies, Recent Changes, Manual Additions.

#### Scenario: Consistency across ComplyTime repositories
- **WHEN** the divisor-scribe or any agent reads AGENTS.md
- **THEN** the format is consistent with other ComplyTime repositories, requiring no format-specific adaptation
