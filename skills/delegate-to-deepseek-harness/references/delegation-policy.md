# Delegation policy

Delegate complete, independently verifiable implementation units. Good fits
include mechanical multi-file changes, test repair or generation, bounded
repository exploration, migrations, and repetitive maintenance.

Keep architecture, ambiguous product decisions, final review, secrets,
privileged operations, deployments, and irreversible external actions with
the orchestrator. Never run concurrent mutating workers in the same checkout. Separate Git
worktrees naturally receive different session identities.
