#!/usr/bin/env python3
"""UserPromptSubmit hook: reinjects typewriter-mode constraints each turn."""
import json
import os
import sys

HOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
CLAUDE_DIR = os.path.dirname(HOOKS_DIR)
STATE_FILE = os.path.join(CLAUDE_DIR, "typewriter-mode")
LAST_PROMPT_FILE = os.path.join(CLAUDE_DIR, "typewriter-last-prompt.txt")

REMINDER = (
    "TYPEWRITER MODE IS ON. Execute only the literal instruction in this message. "
    "Do not propose, describe, or implement a design/refactoring solution unless "
    "explicitly asked for one. If there are multiple valid ways to do what was asked, "
    "list the options and ask which one instead of picking. Exception, scoped to "
    "tests only: for characterization/unit tests under tests/ or named test_*.py / "
    "*_test.py, you may edit such files without them being named in this message, "
    "and you may propose test designs, pick a reasonable approach, and describe what "
    "you're doing. For tests of new functionality, only proceed autonomously if the "
    "contract is already clear; if not, ask once, then proceed on a stated "
    "best-guess assumption if still unclear. Outside of test-writing, none of this "
    "changes: no unsolicited refactors, no scope creep, and Agent/TodoWrite stay "
    "blocked. Do not expand scope beyond this instruction, and do not attempt to "
    "autonomously finish the underlying task. Internal reasoning is fine; keep the "
    "output literal and minimal."
)


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        data = {}

    try:
        with open(STATE_FILE) as f:
            state = f.read().strip().lower()
    except FileNotFoundError:
        state = "off"

    if state != "on":
        return

    try:
        with open(LAST_PROMPT_FILE, "w") as f:
            f.write(data.get("prompt", ""))
    except OSError:
        pass

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": REMINDER,
        }
    }))


if __name__ == "__main__":
    main()
