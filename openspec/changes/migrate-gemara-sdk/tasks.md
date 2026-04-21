## 1. Dependency Migration

- [x] 1.1 Replace `github.com/ossf/gemara` with `github.com/gemaraproj/go-gemara v0.3.0` in `proofwatch/go.mod` and run `go mod tidy`
- [x] 1.2 Replace `github.com/ossf/gemara` with `github.com/gemaraproj/go-gemara v0.3.0` in `truthbeam/go.mod` and run `go mod tidy`
- [x] 1.3 Update Go version in both `go.mod` files to match `go-gemara` v0.3.0 requirements

## 2. Proofwatch Type Migration

- [x] 2.1 Update `proofwatch/gemara.go`: change import from `layer4` to `gemara "github.com/gemaraproj/go-gemara"`, update `GemaraEvidence` struct to use named `Metadata` field and new type names (`Actor`, `EntryMapping`, `Plan *EntryMapping`)
- [x] 2.2 Update `proofwatch/gemara.go` `Attributes()` method: change `g.Author.Name` to `g.Metadata.Author.Name`, `g.Id` to `g.Metadata.Id`, and add nil-check for `g.Plan` before emitting `policy.rule.id`
- [x] 2.3 Update `proofwatch/gemara_test.go`: change all type references from `layer4.X` to `gemara.X` (`Author`→`Actor`, `Mapping`→`EntryMapping`, `Procedure`→`Plan` pointer, `Passed`/`Failed`/`NotApplicable` constants)
- [x] 2.4 Add test case `TestGemaraEvidenceAttributes_NilPlan` verifying that when `Plan` is nil, `policy.rule.id` is absent from returned attributes (spec scenario: "Plan is absent")
- [x] 2.5 Update `proofwatch/cmd/validate-logs/main.go`: change import and all type references to use new SDK types

## 3. Truthbeam Type Migration

- [x] 3.1 Update `truthbeam/internal/applier/status.go`: change import from `layer4` to `gemara "github.com/gemaraproj/go-gemara"` and update all `layer4.X` references to `gemara.X`
- [x] 3.2 Regenerate `truthbeam/internal/client/client.gen.go` to pick up updated OpenAPI spec with OCI distribution types

## 4. Attribute Model Corrections

- [x] 4.1 Update `model/attributes.yaml`: correct compliance group GEMARA layer number from 5 to 6 (Enforcement layer)
- [x] 4.1a Update `model/attributes.yaml`: change `policy.rule.id` `requirement_level` from `required` to `opt_in` to align with conditional emission behavior
- [x] 4.2 Update `model/attributes.yaml`: correct any YAML formatting for `examples` arrays (normalize whitespace)
- [x] 4.3 Regenerate attribute docs by running `make weaver-docsgen`

## 5. CI and Verification

- [x] 5.1 Update `.github/workflows/ci_local.yml` Go version references
- [x] 5.2 Verify `go build ./...` passes for both proofwatch and truthbeam
- [x] 5.3 Verify `go test ./...` passes for both proofwatch and truthbeam
