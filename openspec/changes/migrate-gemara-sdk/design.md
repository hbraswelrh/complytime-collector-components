## Context

The `proofwatch` and `truthbeam` modules currently import `github.com/ossf/gemara/layer4` (v0.12.1) to work with Gemara compliance assessment types. The Gemara project has reorganized under a new GitHub organization (`gemaraproj`) with an official Go SDK (`github.com/gemaraproj/go-gemara` v0.3.0) that implements the finalized Gemara v1 schema. The old `ossf/gemara` package will be deprecated.

Key differences between the old and new SDK:
- Type renames: `Author` → `Actor` (the type is renamed; the field name on `Metadata` remains `Author`), `Mapping` → `EntryMapping`, `Procedure` → `Plan`
- `Plan` (formerly `Procedure`) is now a `*EntryMapping` pointer (optional) rather than a value type
- The `Strength` field has been removed from `EntryMapping` (not used in this codebase; no action required)
- GEMARA layer numbering has been corrected in v1: Evaluation is Layer 5, Enforcement is Layer 6

The attribute model (`model/attributes.yaml`) currently references incorrect layer numbers inherited from the pre-v1 schema.

## Goals / Non-Goals

**Goals:**
- Replace the deprecated `ossf/gemara/layer4` dependency with the official `gemaraproj/go-gemara` v0.3.0 SDK
- Update all type references across both modules to match v1 naming conventions
- Handle the `Plan` pointer type correctly, emitting `policy.rule.id` only when a plan exists
- Correct GEMARA layer numbering in the attribute model and regenerate documentation
- Maintain full test coverage and build compatibility

**Non-Goals:**
- Adopting new Gemara v1 features beyond what the current codebase uses (e.g., new assessment types, additional layers)
- Refactoring the `GemaraEvidence` struct beyond what the SDK change requires
- Migrating truthbeam's `parseResult`/`mapResult` to use SDK-provided mapping utilities (if any)
- Changing the public API surface of proofwatch or truthbeam beyond the `policy.rule.id` conditionality

## Decisions

### 1. Direct import replacement without adapter layer

Replace `github.com/ossf/gemara/layer4` imports with `"github.com/gemaraproj/go-gemara"`. No adapter or compatibility wrapper is needed because the new SDK's API surface maps 1:1 onto the old one after type renames.

**Alternatives considered:**
- *Adapter pattern*: Wrapping the new SDK to preserve old type names. Rejected -- adds indirection without benefit since all consumers are internal and the rename is mechanical.
- *Vendoring both packages during transition*: Rejected -- increases dependency surface unnecessarily.

### 2. Conditional emission of `policy.rule.id`

Since `Plan` is now `*EntryMapping` (pointer), nil-check before accessing `Plan.EntryId`. This means `policy.rule.id` is only emitted as an OTel attribute when a plan is actually associated with the assessment. This is a correctness improvement aligning with the Gemara v1 schema where the plan/procedure reference is optional.

**Alternatives considered:**
- *Always emit with empty string fallback*: Rejected -- masks missing data and deviates from v1 schema semantics.
- *Emit with sentinel value (e.g., "N/A")*: Rejected -- introduces non-standard attribute values that downstream systems would need to special-case.

### 3. Explicit struct fields on `GemaraEvidence`

Change `GemaraEvidence` from embedding `layer4.Metadata` (promoted fields) to a named `Metadata gemara.Metadata` field with JSON/YAML tags. `AssessmentLog` remains embedded for backward compatibility with existing JSON serialization. This makes the `Metadata` access explicit (`g.Metadata.Author.Name`, `g.Metadata.Id`) and avoids field name collisions.

### 4. In-place attribute model correction

Correct the GEMARA layer references directly in `model/attributes.yaml` and regenerate docs with `make weaver-docsgen`. No version migration script needed since the attribute model is the source of truth and docs are derived.

## Risks / Trade-offs

- **[Breaking change for `policy.rule.id` consumers]** → Downstream systems reading `policy.rule.id` must handle its absence. The attribute model currently declares `policy.rule.id` as `requirement_level: required`; this should be downgraded to `opt_in` to reflect the new conditional emission behavior. Mitigated by documenting the change and updating the requirement level.
- **[Go version bump to 1.25.x in go.mod]** → Required by `go-gemara` v0.3.0's module requirements. The CI workflow is updated to match. Risk is minimal since the project's toolchain already supports this version.
- **[Generated code in client.gen.go]** → The truthbeam client regeneration picks up new OCI distribution types from an updated OpenAPI spec. These are additive (new endpoints/types) and do not change existing behavior, but the diff is large. Mitigated by treating the file as generated and not hand-editing.
