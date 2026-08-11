"""check-map-territory.py — MAP-TERRITORY GATE scripted check (research v2.98).

Usage: python check-map-territory.py <paper-draft.md>

GATE: Any QNFO claim asserting a mathematical object IS the physical structure
must carry an explicit map/territory label: `[MAP — model of X]` (analogy, no
ontological claim) vs `[TERRITORY — claimed identity]` (identity asserted).
TERRITORY claims REQUIRE an accompanying falsifiability condition naming the
observation that would break the identity (KIF-60 / qnfo-core §0.0).

PASS = zero `[TERRITORY` labels, OR every paragraph containing a `[TERRITORY`
label also contains a NON-NEGATED falsifiability marker (disconfirm/falsif/
would-break/observably/prediction/DISCONFIRMED-IF...), either inline in the
label itself (`[TERRITORY — disconfirmed if X]`) or in the same paragraph.
FAIL = any `[TERRITORY` label without an accompanying falsifiability condition
(exit code 1). Prints line numbers + FIX instruction. Build-time BLOCK.

NEGATION GUARD: a marker directly preceded by a negation ("no falsifiability
condition", "without disconfirmation", "not falsifiable") does NOT satisfy the
requirement — a sentence denying a condition is not a condition. The negation
must be attached to the marker phrase (last <=3 tokens before the marker), so
unrelated negations in the same paragraph ("This claim is not proven, but the
identity would be broken if X") do NOT nullify a valid condition.

HYGIENE (red-team 2026-08-11): YAML frontmatter and fenced code blocks are
BLANKED (newlines preserved for accurate line numbers) before scanning — a
label inside ``` ``` or the `---` block must not false-FAIL a legitimate draft.

`[MAP` labels are informational context only — they carry no ontological
weight and require no condition. MAP-label count is printed for the audit
trail (the `(?!-)` guard prevents `[MAP-TERRITORY GATE]` from counting).

Enforcement of the UIA Repair Pipeline Protocol v1.0 (2026-08-11) MAP-TERRITORY
GATE (HARD), SCRIPTING MANDATE (PROSE-GATE-ADVISORY-1, kaizen v1.63): prose
gates are advisory until scripted. Canonical lesson: TITLE-DUPLICATION-1
shipped 3 published versions before it was scripted — this gate exists so
map-territory conflation cannot ship unlabelled again.
"""

import re
import sys
import os

# A [TERRITORY ...] label — may carry inline text, e.g.
#   [TERRITORY — claimed identity]
#   [TERRITORY: the brain IS this tree]
#   [TERRITORY — claimed identity; disconfirmed if X]
LABEL_RE = re.compile(r"\[TERRITORY[^\]]*\]", re.IGNORECASE)
# (?!-) so `[MAP-TERRITORY GATE]` is NOT counted as a MAP label.
MAP_RE = re.compile(r"\[MAP(?!-)[^\]]*\]", re.IGNORECASE)

# Falsifiability markers that satisfy the condition requirement. The gate
# accepts either the inline label itself containing a marker, or any marker
# appearing later in the same paragraph.
FALSIFIABILITY_MARKERS = re.compile(
    r"disconfirm|falsif|would\s+break|would\s+be\s+broken|would\s+fail|"
    r"would\s+kill|observably|observable\s+distinction|prediction|"
    r"DISCONFIRMED\s+IF|O_\s*N|O_\s*T|not\s+identical\s+if|"
    r"breaks\s+the\s+identity",
    re.IGNORECASE,
)

# Bare negation tokens. A marker is NEGATED only when one of these directly
# precedes it (checked on the last <=3 tokens before the marker).
NEGATION = re.compile(r"\b(no|not|never|without|lacks?|absent|missing)\b", re.IGNORECASE)

NEGATION_TAIL_TOKENS = 3

# Clause-scoped denial: "no falsifiability condition that would break ..." — the
# negation governs a condition noun phrase that itself carries the marker. A
# marker is NEGATED when the negation token appears BEFORE a condition noun
# within the same clause and the marker follows it (red-team HARD 2026-08-11:
# "there is no falsifiability condition that would break this identity" must FAIL).
CONDITION_NOUN = re.compile(
    r"(falsifiability\s+condition|disconfirmation\s+condition|falsifiable\s+condition|"
    r"condition\s+that\s+would)",
    re.IGNORECASE,
)
CLAUSE_DENIAL_WINDOW = 80


def is_clause_denied(text, marker_match):
    """True when a negation governs a condition noun phrase before this marker.

    Pattern: "[negation] ... [condition noun] ... [marker]" within one clause,
    e.g. "there is NO falsifiability condition THAT WOULD BREAK this identity".
    The marker is part of the negated noun phrase, so the sentence DENIES a
    condition rather than asserting one (red-team HARD, 2026-08-11).
    """
    start = max(0, marker_match.start() - CLAUSE_DENIAL_WINDOW)
    context = text[start:marker_match.start()]
    neg = NEGATION.search(context)
    if not neg:
        return False
    cond = CONDITION_NOUN.search(context)
    if not cond:
        return False
    # The negation must precede the condition noun phrase.
    return neg.start() < cond.start()


def has_real_marker(text):
    """Return True if `text` contains at least one NON-NEGATED falsifiability marker.

    Negation is scoped two ways (red-team S3 + HARD, 2026-08-11):
    (a) direct attachment — the last NEGATION_TAIL_TOKENS tokens immediately
        before the marker ("no falsifiability condition" is NOT a condition);
    (b) clause-scoped denial — a negation governs a condition noun phrase that
        carries the marker downstream ("no falsifiability condition that would
        break this identity" is a denial, not a condition).
    Unrelated negations in the same paragraph ("This claim is not proven, but
    the identity would be broken if X") do NOT nullify a valid condition.
    """
    for m in FALSIFIABILITY_MARKERS.finditer(text):
        preceding = text[max(0, m.start() - 24):m.start()]
        tail = " ".join(preceding.split()[-NEGATION_TAIL_TOKENS:])
        if NEGATION.search(tail):
            continue  # negated marker — "no falsifiability condition" is NOT a condition
        if is_clause_denied(text, m):
            continue  # clause denial — "no ... condition that would break ..." is NOT a condition
        return True
    return False


def blank_keep_newlines(s):
    """Replace every non-newline char with a space — preserves line numbers."""
    return re.sub(r"[^\n]", " ", s)


def strip_frontmatter_and_fences(text):
    """Blank YAML frontmatter and fenced code blocks (red-team S1/S2, 2026-08-11).

    Returns a copy of `text` where those regions are spaces (newlines kept),
    so labels inside them never match AND reported line numbers stay accurate.
    """
    out = text
    # Leading YAML frontmatter: --- ... --- (blank it, keep newlines)
    if out.startswith("---"):
        fm = re.match(r"^---[ \t]*\n.*?\n---[ \t]*\n", out, re.DOTALL)
        if fm:
            out = out[:fm.start()] + blank_keep_newlines(fm.group(0)) + out[fm.end():]
    # Fenced code blocks: ``` ... ``` and ~~~ ... ~~~
    out = re.sub(
        r"```.*?```|~~~.*?~~~",
        lambda m: blank_keep_newlines(m.group(0)),
        out,
        flags=re.DOTALL,
    )
    return out


def main():
    if len(sys.argv) < 2:
        print("ERROR: usage: python check-map-territory.py <paper-draft.md>")
        sys.exit(2)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"ERROR: file not found: {path}")
        sys.exit(2)

    with open(path, encoding="utf-8") as f:
        text = f.read()

    text = strip_frontmatter_and_fences(text)

    # Split into paragraphs (blank-line separated) to scope the
    # falsifiability requirement: the condition must be in the SAME
    # paragraph as the TERRITORY label (or inside the label itself).
    paragraphs = re.split(r"\n\s*\n", text)

    # Precompute line number of each paragraph start (1-based) on the
    # blanked text — line numbers match the ORIGINAL file because newlines
    # were preserved by strip_frontmatter_and_fences.
    paragraph_starts = []
    cursor = 0
    for para in paragraphs:
        idx = text.find(para, cursor)
        paragraph_starts.append(text.count("\n", 0, idx) + 1)
        cursor = idx + len(para)

    territory_total = 0
    map_total = 0
    violations = []

    for idx, para in enumerate(paragraphs):
        territory_labels = LABEL_RE.findall(para)
        map_labels = MAP_RE.findall(para)
        if map_labels:
            map_total += len(map_labels)
        if not territory_labels:
            continue
        territory_total += len(territory_labels)

        # The label's own inline text counts — `[TERRITORY — disconfirmed if X]`
        # is self-contained. Otherwise the paragraph must carry a marker.
        label_text = " ".join(territory_labels)
        inline_ok = has_real_marker(label_text)
        para_ok = inline_ok or has_real_marker(para)

        if not para_ok:
            violations.append((paragraph_starts[idx], territory_labels))

    print(f"File: {path}")
    print(f"  [MAP] labels (context only, no condition required): {map_total}")
    print(f"  [TERRITORY] labels (identity claims, condition REQUIRED): {territory_total}")
    print(f"  Violations (TERRITORY without falsifiability condition): {len(violations)}")

    if violations:
        for line_no, labels in violations:
            print(f"  LINE {line_no}: {labels[0] if labels else '[TERRITORY]'}")
        print("GATE FAIL: MAP-TERRITORY-1 — a [TERRITORY] claim carries no falsifiability condition.")
        print("  A TERRITORY label asserts the math object IS the physical structure — that identity")
        print("  MUST be breakable by an observation (KIF-60). Fix options:")
        print("    (a) Add the condition to the label:   [TERRITORY — claimed identity; disconfirmed if <O>]")
        print("    (b) Add it to the same paragraph:     ... disconfirmed if <O> ...")
        print("    (c) Downgrade to a map:               [MAP — model of X] (no ontological claim, no condition)")
        sys.exit(1)

    if territory_total == 0:
        print("GATE PASS: no TERRITORY identity claims in this draft.")
    else:
        print("GATE PASS: every [TERRITORY] claim carries a falsifiability condition (KIF-60).")
    sys.exit(0)


if __name__ == "__main__":
    main()
