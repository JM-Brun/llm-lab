# Branch hygiene trigger

Editing this file on `main` triggers the branch-hygiene workflow (in addition
to the usual manual `workflow_dispatch` run). The run mode is read from this
file: set `apply: true` to delete branches proven redundant against `main`;
any other value performs a dry run that deletes nothing.

The `delete:` line lists branch names that are deleted as obsolete after
explicit human arbitration (see issue #652), in addition to proven-redundant
branches. Protected branches (main, open pull-request heads, `exclude:`)
are never deleted, even if listed.

apply: true
exclude:
delete: audit/316-entropy-attention-browser-coverage,ci/browser-audit-math-render-gate,ci/targeted-browser-review,docs/audit-position-tensor-precision,docs/cross-entropy-link-api-check,docs/knowledge-architecture-interoperability,docs/pedagogical-breadcrumb-contract,docs/rebase-qkv-self-cross-attention,fix/browser-audit-pageerror-diagnostics,fix/diagnose-overview-svg-transforms,fix/homepage-inline-svg-raw-html,fix/quarto-page-navigation-a11y,fix/remove-misleading-pipeline-steppers,repair/pr-468-sync-main,repair/pr-471-current-main,repair/pr-471-sync-main,repair/pr-471-sync-main-v2,source/medium-neha-kk-qkv-integration,test/build-tour-rendered-navigation,tokenization-embeddings-migration-base,ux/audit-position-tensor-precision,ux/audit-positional-and-tensor-pages,ux/browser-audit-homepage
