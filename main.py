#!/usr/bin/env python3
"""Seventeen Syllables of Debugging entrypoint.

Writes one haiku (5-7-5, 72 characters) to /output/entry.txt: past
midnight a log insists nothing is wrong, and the last line turns the
poem -- git blame names the debugger. The text is a fixed string
(verified against the gate below), so two runs always produce the
same file. Stdlib only, no network.

The haiku:

    Past midnight, the log
    says nothing is wrong, again
    my name in git blame

Syllables: 5-7-5 (Past mid-night the log / says no-thing is wrong
a-gain / my name in git blame). 71 characters, within the 1-200 gate.

Local check (outside the grader's container):

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from pathlib import Path

HAIKU = (
    "Past midnight, the log\n"
    "says nothing is wrong, again\n"
    "my name in git blame"
)

DEFAULT_OUTPUT = "/output"


def count_syllables(line: str) -> int:
    """Small syllable counter for the three fixed lines (vowel groups)."""
    vowels = "aeiouy"
    total = 0
    for word in line.replace(",", "").replace("-", " ").split():
        word = word.lower().strip(".,")
        groups = 0
        prev_vowel = False
        for ch in word:
            is_vowel = ch in vowels
            if is_vowel and not prev_vowel:
                groups += 1
            prev_vowel = is_vowel
        if word.endswith("e") and groups > 1:
            groups -= 1
        total += max(groups, 1)
    return total


def output_path() -> Path:
    """Where the grader expects the text, creating the folder first."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT)
    folder = Path(wanted)
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.txt"


def main() -> None:
    lines = HAIKU.split("\n")
    if len(lines) != 3:
        print("haiku must have exactly 3 lines", file=__import__("sys").stderr)
        raise SystemExit(1)
    if not 1 <= len(HAIKU) <= 200:
        print(f"haiku is {len(HAIKU)} chars, must be 1-200", file=__import__("sys").stderr)
        raise SystemExit(1)
    shape = [count_syllables(line) for line in lines]
    if shape != [5, 7, 5]:
        print(f"syllable shape is {shape}, must be [5, 7, 5]", file=__import__("sys").stderr)
        raise SystemExit(1)
    if not HAIKU.strip():
        print("haiku is only white space", file=__import__("sys").stderr)
        raise SystemExit(1)
    output_path().write_text(HAIKU + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
