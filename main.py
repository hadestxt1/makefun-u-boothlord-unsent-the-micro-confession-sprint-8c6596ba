"""Unsent: The Micro-Confession Sprint — model-free entry.

Writes one micro-confession in exactly two parts to /output/entry.txt:
a "To:" line naming who it was meant for, and the unsent message itself,
one line written exactly as it was typed, with no explanation after it.

Deterministic, stdlib only, no model calls, no network, no clock, no
randomness: the same run always writes the same bytes.
"""

import sys
from pathlib import Path

ADDRESSEE = "Gran's voicemail"

MESSAGE = (
    "I still ring you every Sunday just to hear you say "
    "leave a message, and I hang up before the beep."
)

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 260
MESSAGE_MAX_CHARS = 200


def build_confession() -> str:
    """Assemble the two-part confession: To: line, then the message line."""
    to_line = "To: " + ADDRESSEE
    return to_line + "\n" + MESSAGE + "\n"


def check_gate(text: str) -> None:
    """Enforce the competition gate before anything is written."""
    if not (GATE_MIN_CHARS <= len(text) <= GATE_MAX_CHARS):
        raise ValueError(
            f"entry is {len(text)} characters, gate needs "
            f"{GATE_MIN_CHARS}-{GATE_MAX_CHARS}"
        )
    if text.strip() == "":
        raise ValueError("entry is only white space")
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 2:
        raise ValueError(f"entry must be exactly two lines, got {len(lines)}")
    if not lines[0].startswith("To: "):
        raise ValueError("first line must be a To: line")
    if len(lines[1]) > MESSAGE_MAX_CHARS:
        raise ValueError(
            f"message line is {len(lines[1])} characters, "
            f"max {MESSAGE_MAX_CHARS}"
        )


def main(argv: list[str]) -> int:
    out_path = Path(argv[1]) if len(argv) > 1 else Path("/output/entry.txt")
    text = build_confession()
    check_gate(text)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
