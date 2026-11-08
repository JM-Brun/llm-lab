# Branch hygiene trigger

Editing this file on `main` triggers the branch-hygiene workflow (in addition
to the usual manual `workflow_dispatch` run). The run mode is read from this
file: set `apply: true` to delete branches proven redundant against `main`;
any other value performs a dry run that deletes nothing.

apply: false
exclude:
