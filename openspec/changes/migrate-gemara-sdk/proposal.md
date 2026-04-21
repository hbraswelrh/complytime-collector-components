## Why

The project depends on `github.com/ossf/gemara/layer4` (v0.12.1), which is a sub-package of the original Gemara repository. The Gemara project has moved to a dedicated organization with an official Go SDK at `github.com/gemaraproj/go-gemara` (v0.3.0) that implements the Gemara v1 schema. Migrating now ensures the codebase tracks the canonical SDK, receives upstream fixes, and aligns type names and layer numbering with the v1 specification before the old package is deprecated.

## What Changes

- Replace `github.com/ossf/gemara/layer4` with `github.com/gemaraproj/go-gemara` v0.3.0 in both `proofwatch` and `truthbeam` modules
- Rename type references to match the v1 SDK: `Author` type to `Actor` (field name on `Metadata` unchanged), `Mapping` to `EntryMapping`, `Procedure` to `Plan` (now `*EntryMapping`, optional pointer)
- Drop the `Strength` field from `EntryMapping` usage (removed in v1 SDK; not used in this codebase)
- **BREAKING**: `policy.rule.id` is now conditionally emitted -- only when `Plan` is non-nil. Previously `Procedure` was a value type so the attribute was always included (potentially as an empty string)
- Correct GEMARA layer references in the attribute model: Evaluation is Layer 5 (was 4), Enforcement is Layer 6 (was 5)
- Regenerate attribute docs via `weaver-docsgen` to reflect corrected layer numbers
- Update CI workflow Go version references

## Capabilities

### New Capabilities

_(none -- this is a dependency migration, not a new capability)_

### Modified Capabilities

_(no existing openspec specs to modify -- this is the first change specification for this project)_

## Impact

- **proofwatch module**: `gemara.go`, `gemara_test.go`, `cmd/validate-logs/main.go`, `go.mod`, `go.sum` -- all Gemara imports and type references change
- **truthbeam module**: `internal/applier/status.go`, `internal/client/client.gen.go`, `go.mod`, `go.sum` -- Gemara imports change; regenerated client picks up new OCI types from updated API spec
- **Attribute model**: `model/attributes.yaml` -- layer number corrections for compliance and policy attribute groups
- **Documentation**: `docs/attributes/compliance.md`, `docs/attributes/policy.md` -- regenerated from corrected model
- **CI**: `.github/workflows/ci_local.yml` -- Go version alignment
- **Downstream consumers**: Any system consuming `policy.rule.id` must handle its absence when no plan/procedure is associated with an assessment
- **In-repo configs**: `hack/demo/demo-config.yaml`, `beacon-distro/config.yaml`, and `hack/demo/loki-config.yaml` reference `policy.rule.id` but already use nil-safe patterns (`where attributes["policy.rule.id"] != nil`); S3 partitioning usage should be audited for absent attribute handling
- **Documentation**: `docs/DESIGN.md` contains a `GemaraEvidence` code example (lines 88-117) that should be updated to reflect the new struct shape
