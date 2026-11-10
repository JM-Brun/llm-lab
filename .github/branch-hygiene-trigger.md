# Branch hygiene trigger

Editing this file on `main` triggers the branch-hygiene workflow (in addition
to the usual manual `workflow_dispatch` run). The run mode is read from this
file: set `apply: true` to delete branches proven redundant against `main`;
any other value performs a dry run that deletes nothing.

The `delete:` line lists branch names that are deleted as obsolete after
explicit human arbitration (see issue #652), in addition to proven-redundant
branches. Protected branches (main, open pull-request heads, `exclude:`)
are never deleted, even if listed.

The default state is a dry run (`apply: false`): edit this file to trigger a
report on issue #652, and only switch to `apply: true` when the report shows
branches that should really be deleted.

apply: false
exclude:
delete:
