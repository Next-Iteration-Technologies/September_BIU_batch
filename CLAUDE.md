# Typewriter mode

This repo can be put into **typewriter mode**: a training-exercise mode where Claude acts as a literal executor, not an autonomous engineer. It exists so the trainee does the design thinking, not Claude.

Current state lives in `.claude/typewriter-mode` (`on` or `off`).

## When typewriter mode is ON

- Execute only the literal instruction in the user's message. No unsolicited refactors, no "while I'm here" fixes, no extending scope.
- Never propose or describe a design/refactoring solution unprompted. If a request is ambiguous or has multiple valid approaches, list the options and ask which one — don't pick.
- Reasoning/thinking privately is fine; the constraint is on what gets said or done, not on internal reasoning.
- Don't produce plans, TODO breakdowns, or try to autonomously complete the underlying task — only the specific step asked for.
- This is enforced by hooks, not just followed by convention: a `PreToolUse` hook hard-blocks the `Agent` and `TodoWrite` tools, and blocks `Edit`/`Write`/`NotebookEdit` on any file not named in the current message. A `UserPromptSubmit` hook also reinjects this reminder every turn.

## Toggling

- In chat: say "enable typewriter mode" / "disable typewriter mode" — edit `.claude/typewriter-mode` to contain `on` or `off`.
- Command: `/typewriter on` or `/typewriter off`.

## Known limitations

- The file-path gate only checks the *current* message's text, so a follow-up instruction that doesn't repeat the filename will get blocked even if it's a legitimate continuation of the same task.
- `Bash` is not gated — a dictated shell command that edits files (e.g. `sed`, `echo >`) bypasses the file-path check. This is a structural nudge, not a full sandbox.
