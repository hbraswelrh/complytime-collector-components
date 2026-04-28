# complytime-collector-components

Open-source observability toolkit that collects, normalizes, and enriches compliance evidence by extending the OpenTelemetry standard. Uses a Go workspace monorepo with two active modules (`proofwatch`, `truthbeam`) and an OTel Collector distribution (`beacon-distro`).

## Structure

```text
proofwatch/              # Go module — evidence collection & emission library
  internal/metrics/      # OTel metrics observer (evidence counters)
  cmd/validate-logs/     # CLI tool for validating log output
truthbeam/               # Go module — OTel Collector enrichment processor
  internal/applier/      # Attribute application logic
  internal/client/       # Generated OpenAPI client + otter cache
  internal/metadata/     # Component metadata + test fixtures
beacon-distro/           # OTel Collector distribution (manifest.yaml + Containerfile)
compass/                 # Stub — real service lives at github.com/complytime/gemara-content-service
model/                   # Weaver semantic convention definitions (source of truth for attributes)
templates/               # Weaver Jinja2 code generation templates
hack/                    # Demo configs, sample data, TLS cert generation
docs/                    # Architecture (DESIGN.md), dev guide (DEVELOPMENT.md), attribute docs
openspec/                # OpenSpec change proposals and specs
.specify/memory/         # ComplyTime constitution (org-wide standards)
```

## Commands

```bash
make test                # Unit tests with coverage (proofwatch + truthbeam)
make test-race           # Tests with race detection
make golangci-lint       # Lint all modules (golangci-lint v2)
make deps                # Tidy, verify, download, and vendor all modules
make api-codegen         # Regenerate OpenAPI client (truthbeam)
make weaver-codegen      # Regenerate attribute constants from model/
make weaver-docsgen      # Regenerate attribute docs from model/
make crapload-check      # Check CRAP score regressions against baseline
make deploy              # Start local stack (podman-compose)
make undeploy            # Stop local stack
make help                # List all available targets
```

## Constraints

- **Go workspace, no root go.mod**: This repo uses `go.work` to link modules. All module-level commands iterate over `MODULES := ./proofwatch ./truthbeam`. Running `go test ./...` from root will not work — use `make test`.
- **Generated files — DO NOT EDIT**:
  - `proofwatch/attributes.go` — regenerate with `make weaver-codegen`
  - `truthbeam/internal/applier/attributes.go` — regenerate with `make weaver-codegen`
  - `truthbeam/internal/client/client.gen.go` — regenerate with `make api-codegen`
  - `docs/attributes/*.md` — regenerate with `make weaver-docsgen`
- **compass/ is external**: Do not build or modify. The actual service is maintained at `github.com/complytime/gemara-content-service`. This directory exists only for Go workspace resolution.
- **Podman, not Docker**: Container operations use `podman` and `podman-compose`. Do not reference `docker` commands.
- **Lint**: Go linting uses `.golangci.yml` (v2 format). Multi-language CI linting uses `.mega-linter.yml`. No pre-commit hooks — run `make golangci-lint` locally.
- **Standards**: All coding standards are in `.specify/memory/constitution.md`. For architecture context, see `docs/DESIGN.md`. For dev setup, see `docs/DEVELOPMENT.md`.

## Commits

All commits MUST use Conventional Commits, the `-s` flag (Signed-off-by), and include an `Assisted-by` trailer when AI-assisted. See `.specify/memory/constitution.md` for full details.

## Active Technologies

- Go 1.25.8 (toolchain 1.25.9), multi-module workspace (`go.work`)
- OpenTelemetry Collector SDK v1.56.0 / v0.150.0 (component framework, pipeline data, processor interfaces)
- `github.com/gemaraproj/go-gemara` v0.3.0 (compliance evidence model — Gemara v1 schema)
- `github.com/Santiago-Labs/go-ocsf` (OCSF cybersecurity schema types)
- `github.com/maypok86/otter/v2` (in-memory cache, truthbeam)
- `github.com/oapi-codegen` (OpenAPI client generation, truthbeam)
- `go.uber.org/zap` (structured logging, truthbeam)
- `github.com/stretchr/testify` (test assertions, both modules)
- OTel Weaver (semantic convention model — Go constants + docs)
- OTel Collector Builder v0.144.0 (beacon-distro binary)
- golangci-lint v2, MegaLinter, SonarCloud, gaze (quality tooling)
- Podman + podman-compose (container runtime)
- Container: Alpine 3.22 (certs), golang:1.24.13 (build), distroless (runtime)
- Registries: `ghcr.io` (primary), Quay.io (secondary)

## Recent Changes

- migrate-gemara-sdk: Migrated from `github.com/ossf/gemara/layer4` to `github.com/gemaraproj/go-gemara` v0.3.0, corrected GEMARA layer numbering in attribute model, regenerated docs
  - Spec: `openspec/specs/gemara-evidence-attributes/spec.md`

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->

## Convention Packs

This repository uses convention packs scaffolded by
unbound-force. Agents MUST read the applicable pack(s)
before writing or reviewing code.

- `.opencode/uf/packs/default.md`
- `.opencode/uf/packs/default-custom.md`
- `.opencode/uf/packs/severity.md`
- `.opencode/uf/packs/content.md`
- `.opencode/uf/packs/content-custom.md`
