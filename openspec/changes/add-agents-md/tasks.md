## 1. Create AGENTS.md

- [x] 1.1 Create `AGENTS.md` at the repo root with the title line and one-line project description
- [x] 1.2 Add the Structure section with annotated 2-level directory tree (proofwatch, truthbeam, beacon-distro, compass, model, templates, hack, docs, openspec, .specify/memory)
- [x] 1.3 Add the Commands section with essential make targets (test, test-race, golangci-lint, deps, api-codegen, weaver-codegen, weaver-docsgen, crapload-check, deploy, undeploy, help)
- [x] 1.4 Add the Constraints section: Go workspace rules, generated files DO NOT EDIT list with regeneration commands, compass stub, podman-not-docker, lint config pointers, cross-references to docs/DESIGN.md, docs/DEVELOPMENT.md, and constitution
- [x] 1.5 Add the Commits section referencing Conventional Commits and trailers with pointer to constitution
- [x] 1.6 Add the Active Technologies section with current versions from go.mod and build configs
- [x] 1.7 Add the Recent Changes section with the migrate-gemara-sdk entry
- [x] 1.8 Add the Manual Additions markers (HTML comment block)

## 2. Verification

- [x] 2.1 Verify all file paths referenced in Constraints exist in the repo
- [x] 2.2 Verify all make targets listed in Commands exist in the Makefile
- [x] 2.3 Verify all dependency versions in Active Technologies match current go.mod files
- [x] 2.4 Verify the file ends with a single empty line (POSIX compliance per constitution)
