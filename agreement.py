#!/usr/bin/env python3
"""
The agreement check. ← UNIT 6, MILESTONE 3

Staff labelled 30 posts with your taxonomy. You label the same 30. This works
out how often you matched and lists every post where you didn't.

    python agreement.py --help
    python agreement.py
    python agreement.py --staff data/staff_labels.csv --mine my_labels.csv

**Label the posts before you run this.** The rate is arithmetic and the script
does it for you. The adjudication is the graded part and the script deliberately
does not touch it — it hands you the disagreements and an empty column.

This is the only instrument you have that can tell a labelling problem from a
model problem, which is exactly what Milestone 4 asks you to use it for.

Both files need a `text` column and a `label` column. Posts are matched on their
text, so paste it unchanged — if you retype or trim a post it won't match and
the script will tell you which one.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Windows consoles default to a codepage that can't encode the characters this
# file prints, and Python only notices when the output is redirected — so
# `python agreement.py > log.txt` would crash where the same command on screen
# is fine. Ask for UTF-8 on the way out.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass

LABEL_COLUMNS = ("label", "staff_label", "my_label", "your_label")


def normalise(text):
    """Match posts on their words, not on stray whitespace."""
    return re.sub(r"\s+", " ", str(text)).strip()


def label_column(df, path):
    """Find the label column, whatever it got called."""
    for name in LABEL_COLUMNS:
        if name in df.columns:
            return name
    print(f"{path} has no label column. Looked for: {', '.join(LABEL_COLUMNS)}.",
          file=sys.stderr)
    print(f"Found: {', '.join(df.columns)}", file=sys.stderr)
    sys.exit(1)


def load(path, pd):
    """One labelled file, as {normalised text: (original text, label)}."""
    if not Path(path).exists():
        print(f"No file at {path}.", file=sys.stderr)
        if "staff" in str(path):
            print("That's the set your TF gives you. Ask in the help channel if you", file=sys.stderr)
            print("haven't been sent it — this milestone can't start without it.", file=sys.stderr)
        else:
            print("Make it by copying the staff set's posts into a CSV with a `text`", file=sys.stderr)
            print("column and a `label` column, then labelling them yourself.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(path)
    if "text" not in df.columns:
        print(f"{path} has no 'text' column. Found: {', '.join(df.columns)}", file=sys.stderr)
        sys.exit(1)

    column = label_column(df, path)
    rows = {}
    for text, label in zip(df["text"], df[column]):
        rows[normalise(text)] = (str(text), str(label).strip())
    return rows


def compare(staff, mine):
    """Returns (matched, disagreements, missing_from_mine, extra_in_mine)."""
    shared = [key for key in staff if key in mine]
    matched = [key for key in shared if staff[key][1] == mine[key][1]]
    disagreements = [
        {"text": staff[key][0], "staff": staff[key][1], "mine": mine[key][1]}
        for key in shared
        if staff[key][1] != mine[key][1]
    ]
    return (
        matched,
        disagreements,
        [staff[key][0] for key in staff if key not in mine],
        [mine[key][0] for key in mine if key not in staff],
    )


def shorten(text, width=70):
    """One line, short enough to sit in a markdown cell."""
    flat = normalise(text).replace("|", "\\|")
    return flat if len(flat) <= width else flat[: width - 1] + "…"


def disagreement_table(disagreements):
    """The skeleton your README needs. The last column is yours to fill in."""
    rows = ["| Post | Staff said | I said | My call, and why |",
            "|---|---|---|---|"]
    for row in disagreements:
        rows.append(
            f"| {shorten(row['text'])} | `{row['staff']}` | `{row['mine']}` |  |"
        )
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Agreement against the staff labels. Runs locally, no key.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--staff", default="data/staff_labels.csv",
                        help="the labelled set your TF gives you")
    parser.add_argument("--mine", default="my_staff_labels.csv",
                        help="the same posts, labelled by you")
    parser.add_argument("--out", default="agreement_results.json")
    args = parser.parse_args()

    try:
        import pandas as pd
    except ImportError:
        print("pandas isn't installed. Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    staff = load(args.staff, pd)
    mine = load(args.mine, pd)
    matched, disagreements, missing, extra = compare(staff, mine)

    compared = len(matched) + len(disagreements)
    if not compared:
        print("No posts matched between the two files.", file=sys.stderr)
        print("Posts are matched on their text, so it has to be pasted unchanged.", file=sys.stderr)
        sys.exit(1)

    rate = len(matched) / compared

    print(f"Compared {compared} posts.\n")
    print(f"  agreed      {len(matched)}")
    print(f"  disagreed   {len(disagreements)}")
    print(f"  agreement   {rate:.0%}\n")

    if missing:
        print(f"[look at] {len(missing)} staff posts aren't in your file. Either you")
        print("          skipped them, or the text was edited and didn't match:")
        for text in missing[:3]:
            print(f"            - {shorten(text, 60)}")
        print()
    if extra:
        print(f"[look at] {len(extra)} posts in your file aren't in the staff set.\n")

    if not disagreements:
        print("You matched staff on every post. Say so in your README — and say")
        print("whether you think the set was easy or your rule is genuinely tight.")
    else:
        print("Here they are. Your README has a block to fill in for each one —")
        print("the post, both labels, your call and why, and which pile it goes in.\n")
        print(disagreement_table(disagreements))
        print()
        print('"Staff is right" every time is not adjudication. Some of these posts')
        print("were picked because they are genuinely ambiguous.")

    Path(args.out).write_text(json.dumps({
        "compared": compared,
        "agreed": len(matched),
        "agreement_rate": rate,
        "disagreements": disagreements,
        "staff_posts_not_in_mine": len(missing),
    }, indent=2), encoding="utf-8")

    print(f"\nWrote {args.out}. Commit it.")
    print("\nThen sort each disagreement into one of three piles:")
    print("  (a) your rule covered it and you applied it loosely — a consistency problem")
    print("  (b) your rule genuinely doesn't say — a taxonomy gap")
    print("  (c) your rule and staff's are both defensible — argue yours")
    print("\n(b) and (c) are the interesting ones, and (c) is a legitimate win.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
