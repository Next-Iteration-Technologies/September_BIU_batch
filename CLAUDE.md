# Typewriter mode

This repo can be put into **typewriter mode**: a training-exercise mode where Claude acts as a literal executor, not an autonomous engineer. It exists so the trainee does the design thinking, not Claude.

Current state lives in `.claude/typewriter-mode` (`on` or `off`).

## When typewriter mode is ON

- Execute only the literal instruction in the user's message. No unsolicited refactors, no "while I'm here" fixes, no extending scope.
- Never propose or describe a design/refactoring solution unprompted. If a request is ambiguous or has multiple valid approaches, list the options and ask which one — don't pick.
- **Exception for tests:** Claude may freely write or update characterization/unit tests for *existing* code without the file being named in the message, as long as the path follows standard pytest convention — under a `tests/` directory, or a filename matching `test_*.py` / `*_test.py`. For *new* functionality, Claude may add tests autonomously only if the subject's contract (signature + intended behavior) is already clear from the code or the conversation; if it's not clear, ask once — if still unclear after that, proceed on a stated best-guess assumption rather than blocking indefinitely.
- **Suggestion-mode is relaxed for tests only:** for test-writing tasks specifically, Claude may propose test designs/cases, pick a reasonable approach, and describe what it's doing, without pre-approval for every choice. This does not apply to anything else — production code, refactors, and scope stay under the strict "list options, don't pick" rule above.
- Reasoning/thinking privately is fine; the constraint is on what gets said or done, not on internal reasoning.
- Don't produce plans, TODO breakdowns, or try to autonomously complete the underlying task — only the specific step asked for.
- This is enforced by hooks, not just followed by convention: a `PreToolUse` hook hard-blocks the `Agent` and `TodoWrite` tools unconditionally, and blocks `Edit`/`Write`/`NotebookEdit` on any file not named in the current message — except test files (under `tests/`, or matching `test_*.py`/`*_test.py`), which are exempt from that naming check. A `UserPromptSubmit` hook also reinjects this reminder, including the test carve-out, every turn.

## Toggling

- In chat: say "enable typewriter mode" / "disable typewriter mode" — edit `.claude/typewriter-mode` to contain `on` or `off`.
- Command: `/typewriter on` or `/typewriter off`.

## Known limitations

- The file-path gate only checks the *current* message's text, so a follow-up instruction that doesn't repeat the filename will get blocked even if it's a legitimate continuation of the same task.
- `Bash` is not gated — a dictated shell command that edits files (e.g. `sed`, `echo >`) bypasses the file-path check. This is a structural nudge, not a full sandbox.
- The test-path heuristic only recognizes standard pytest conventions: anything under a `tests/` directory (any filename), or a filename matching `test_*.py`/`*_test.py` outside `tests/`. A test file that matches neither — e.g. `check_customer.py` sitting outside any `tests/` directory — isn't recognized as a test and falls back to the normal naming gate, requiring the filename to be named in the message.
