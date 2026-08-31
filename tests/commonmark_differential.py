"""Differential check: verify.py's mark detection against a CommonMark reference.

Not part of `run_fixtures.py`, and not run by it. This needs a third-party
Markdown implementation, and the suite -- like the checker -- has no
dependencies. It is kept because it is what found the defect nobody reasoned
their way to: `a*(invented)*` is literal text to every renderer and was a valid
mark here, in the delimiter these documents are actually written with, while
four rounds of review argued about underscores.

    python -m venv .venv && .venv/bin/pip install markdown-it-py
    .venv/bin/python tests/commonmark_differential.py

Exits non-zero on any divergence and prints each one, labelled by direction:
a FALSE FAIL refuses a mark a reader can see, a FALSE PASS accepts one they
cannot. Run it after any change to the mark patterns, and read the false
failures first -- a checker that rejects real work teaches authors to ignore it.

One class of FALSE PASS is expected and documented in verify.py beside
`_flanking`: a mark flush against another copy of its own delimiter, decided by
Markdown's rule of three.
"""
import importlib.util
import itertools
import os
import re
import sys

from markdown_it import MarkdownIt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, os.pardir))
VERIFY = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    REPO, "skills", "persona-brainstorm", "scripts", "verify.py")

spec = importlib.util.spec_from_file_location("v", VERIFY)
v = importlib.util.module_from_spec(spec)
sys.modules["v"] = v
spec.loader.exec_module(v)

md = MarkdownIt("commonmark")

BT = chr(96)
BS = chr(92)


def renders(text):
    """True when the reference emphasises text opening "(inv".

    <strong> counts: a doubled delimiter renders bold rather than italic,
    and bold is still visible. The needle is the mark's own text, so emphasis
    the surrounding context happens to produce does not count as the mark
    rendering.
    """
    html = md.render(text)
    return bool(re.search(r"<(?:em|strong)>\((?:inv|obs|inf)", html))


def checker(text):
    return bool(v.find_marks(text))


# Every character class that decides flanking, plus the ones that decide code.
NEIGHBOURS = ["", " ", "a", "Z", "7", ".", ")", "(", "-", ",", ";", BT, "*",
              "_", BS, "\U0001F600", "\u2705", "\u00e9", "\u4e2d", "\t"]

MARKS = ["*(invented)*", "_(invented)_", "*(observed: issue #1)*",
         "_(inferred: a note)_"]

# Structures where code spans and escapes decide the answer.
STRUCTURES = [
    BT + "literal " + BT * 3 + " {m} still code" + BT,
    BT * 3 + " {m} " + BT * 3,
    BT + " {m} " + BT,
    BS + BT + "{m}" + BS + BT,
    BT + "a" + BS + BT + " {m} tail",
    BT + "foo" + BS + BT + "bar" + BT + " {m}",
    "{m} " + BT + "code" + BT,
    BT + "code" + BT + " {m}",
    "x {m} y",
    "- {m}",
    "**bold** {m}",
    BS + "{m}",
    BS + BS + "{m}",
    BS + BS + BS + "{m}",
]

# Sources that contain the characters that broke earlier rounds.
SOURCE_MARKS = [
    "*(observed: primitive(s) reported)*",
    "_(observed: primitive(s) reported)_",
    "*(observed: " + BT + "README.md" + BT + " line 3)*",
    "_(observed: " + BT + "README.md" + BT + " line 3)_",
    "*(observed: a" + BT + "x)* y" + BT + " tail",
    "_(observed: a" + BT + "x)_ y" + BT + " tail",
    "_(observed: " + BT + "x)_ y" + BT + " more)_",
    "*(observed: " + BT + "x)* y" + BT + " more)*",
]


# Every case is placed mid-line. A case at the start of a line is a different
# question -- a tab there is an indented code block and three backticks are a
# fence -- and the checker reads document fragments, not block structure, so
# testing it against block context measures the harness rather than the code.
LEAD = "z "


def cases():
    for mark, before, after in itertools.product(MARKS, NEIGHBOURS, NEIGHBOURS):
        yield LEAD + before + mark + after
    for struct, mark in itertools.product(STRUCTURES, MARKS):
        yield LEAD + struct.format(m=mark)
    for text in SOURCE_MARKS:
        yield LEAD + text
        yield LEAD + text + " prose"


def rule_of_three(text):
    """True when the accepted mark is written flush against its own delimiter.

    The one divergence class left, and the reason this script classifies rather
    than merely counting. A signal that fires on every run is a signal nobody
    reads, and recording these as *expected* is what keeps a new divergence
    visible on the line below them.
    """
    found = v.find_marks(text)
    if not found:
        return False
    m = found[0]
    delim = text[m.start()]
    before = text[m.start() - 1] if m.start() else ""
    after = text[m.end()] if m.end() < len(text) else ""
    return before == delim or after == delim


def main():
    known, bad, total = [], [], 0
    for text in cases():
        total += 1
        want, got = renders(text), checker(text)
        if want == got:
            continue
        (known if got and rule_of_three(text) else bad).append((text, want, got))
    print(f"{total} cases, {len(bad)} unexpected divergence(s), "
          f"{len(known)} known (rule of three)")
    for text, want, got in bad:
        label = "FALSE PASS" if got else "FALSE FAIL"
        print(f"  {label}  {text.encode('unicode_escape').decode()!r} "
              f"renders={want} checker={got}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
