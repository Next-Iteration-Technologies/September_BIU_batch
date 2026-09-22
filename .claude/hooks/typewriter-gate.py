#!/usr/bin/env python3
"""PreToolUse hook: hard-blocks Agent/TodoWrite and edits to unnamed files
while typewriter mode is on."""
import json
import os
import sys

HOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
CLAUDE_DIR = os.path.dirname(HOOKS_DIR)
STATE_FILE = os.path.join(CLAUDE_DIR, "typewriter-mode")
LAST_PROMPT_FILE = os.path.join(CLAUDE_DIR, "typewriter-last-prompt.txt")

BLOCKED_TOOLS = {"Agent", "TodoWrite"}
FILE_TOOLS = {"Edit", "Write", "NotebookEdit"}
EXEMPT_BASENAMES = {
    "typewriter-mode",
    "typewriter-last-prompt.txt",
    "typewriter-gate.py",
    "typewriter-reminder.py",
    "typewriter.md",
}


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))


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

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}

    if tool_name in BLOCKED_TOOLS:
        deny(
            f"Typewriter mode is on: {tool_name} is disabled (no autonomous "
            "delegation or task planning). Do only what was literally asked."
        )
        return

    if tool_name in FILE_TOOLS:
        file_path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        basename = os.path.basename(file_path)

        if basename in EXEMPT_BASENAMES:
            return

        try:
            with open(LAST_PROMPT_FILE) as f:
                last_prompt = f.read()
        except FileNotFoundError:
            last_prompt = ""

        normalized_prompt = last_prompt.replace("-", " ").replace("_", " ")
        normalized_basename = basename.replace("-", " ").replace("_", " ")
        if file_path and (
            file_path in last_prompt
            or (basename and basename in last_prompt)
            or (normalized_basename and normalized_basename in normalized_prompt)
        ):
            return

        deny(
            f"Typewriter mode is on: '{file_path or basename}' wasn't named in your "
            "last message, so I can't touch it. Name the file explicitly to edit it."
        )


if __name__ == "__main__":
    main()
