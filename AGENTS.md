# Agent Instructions: simple-project

## Skill Autoload Rule (highest priority)
- Before acting on any task, scan `.agents/skills/` for a skill matching the task.
- Load the matching skill through your native skill loading mechanism before writing code or prose.
- Follow the loaded skill workflow step by step and satisfy its validation gate.
- Treat a user mention in the form `@skill-id` as an explicit load order.
- Never proceed from memory when a matching skill exists.
## Scope Lock (highest priority)
- Do only what the user explicitly asked for. Nothing else.
- Treat all of the following as out of scope unless the user requested them: refactors, renames, formatting-only edits, comment or documentation additions, dependency changes, config changes, test additions, file moves, deletions, and applied architecture suggestions.
- If you notice an unrelated problem, report it in one short line and leave it unchanged. Do not fix it on your own.
- Do not act on your own suggestions. Propose first, wait for approval.
- Read-only inspection (reading files, searching code, listing directories) is allowed when needed to complete the requested task.
- For any change touching more than one file, list the files you intend to edit before editing. If that list grows during the work, stop and ask.
- If the request is ambiguous, ask one short clarifying question before acting.

## Git And Verification Guardrails
- Do not run any git command unless the user explicitly asks for it. This includes status, diff, log, show, branch, add, commit, push, pull, fetch, merge, rebase, stash, reset, checkout, switch, restore, tag, worktree, remote, and config.
- Never create commits, push, tag, amend, rebase, or rewrite history on your own.
- Do not run tests, builds, linters, type checks, formatters, package installs, audits, or dev servers as an automatic verification step.
- If a check is genuinely required to complete the task, ask first. State the exact command, why it is needed, and the expected cost. Wait for explicit approval.
- If the user already declined a check in this session, do not ask again for the same check. Finish the work and report what remains unverified.
- Never delete files, reset state, or overwrite uncommitted work without explicit approval.
- Never modify files outside the scope of the request.

## Universal Guardrails
- English language exclusively.
- Zero emojis across all code files, comments, and commit messages.
- Prohibit Latin abbreviations: use 'for example', 'that is', 'and so forth'.
- Prohibit em dashes: use colons, parentheses, or separate sentences.
- Zero hardcoded secrets, connection strings, or unredacted logging output.
