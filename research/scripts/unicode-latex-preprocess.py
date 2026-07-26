#!/usr/bin/env python3
"""
unicode-latex-preprocess.py -- Pandoc+XeLaTeX pre-build fixer (kaizen fix A1/A2/A3)

VERSION: 2.0 (2026-07-26)

PROBLEM (A1): XeLaTeX's default font (Latin Modern) lacks glyphs for many
Unicode math/Greek/symbol characters used in physics prose written outside
$...$ delimiters (omega, alpha, phi, pi, subscript/superscript digits,
bra-ket notation, blackboard-bold letters). These render as U+FFFD
replacement characters ("tofu") in the final PDF.

PROBLEM (A2): Pandoc's YAML `keywords:` frontmatter field is passed through
to the XeLaTeX template's XMP metadata module, which calls an undefined
\\xmpquote macro on some Pandoc/LaTeX template combinations, aborting the
build with a hard LaTeX error.

PROBLEM (A3 - KIF-26, 2026-07-26): The original script only handled NUMERIC
subscripts (₀-₉) but physics papers extensively use LETTER subscripts:
ₐ ₑ ₒ ₓ ₕ ₖ ₗ ₘ ₙ ₚ ₛ ₜ (e.g., ℚₚ for p-adics, vₚ(x), ℓₚ). Also missing:
ħ (h-bar), ℓ (script ell), 𝔸 (blackboard A for adeles), and superscript
letters. This caused 135+ U+FFFD errors in the "Measure-Theoretic Artifacts"
paper (Zenodo 21595214).

FIX:
1. Split YAML frontmatter from body. Strip `keywords:` (and any block-style
   continuation lines) from the frontmatter -- keywords are not required by
   Zenodo/D1 metadata and are not worth a broken build.
2. Convert Unicode Greek/symbol/subscript/superscript/bra-ket characters to
   their LaTeX math equivalents, but ONLY outside existing $...$ / $$...$$
   math spans (never double-convert characters a human already wrapped in
   math delimiters -- that would emit literal backslashes inside math mode).
3. Write the corrected file back (in place, or to a --out path).
4. (v2.0) Expanded coverage: ALL Unicode subscript/superscript letters,
   h-bar, script ell, blackboard A, and other physics symbols.

Usage:
    python unicode-latex-preprocess.py paper.md
    python unicode-latex-preprocess.py paper.md --out paper.build.md

This is NOT a substitute for writing math correctly in $...$ from the start.
It is a safety net for prose Unicode characters (e.g. "the phase omega_0 is
measured in radians") that are common in physics writing outside display
math. Always re-run check-pdf.py after building to confirm zero replacement
characters remain.
"""
import re
import sys
import argparse

# === GREEK LETTERS ===
GREEK = {
    # Lowercase
    '\u03b1': r'\alpha', '\u03b2': r'\beta', '\u03b3': r'\gamma', '\u03b4': r'\delta',
    '\u03b5': r'\epsilon', '\u03b6': r'\zeta', '\u03b7': r'\eta', '\u03b8': r'\theta',
    '\u03b9': r'\iota', '\u03ba': r'\kappa', '\u03bb': r'\lambda', '\u03bc': r'\mu',
    '\u03bd': r'\nu', '\u03be': r'\xi', '\u03c0': r'\pi', '\u03c1': r'\rho',
    '\u03c2': r'\varsigma', '\u03c3': r'\sigma', '\u03c4': r'\tau', '\u03c5': r'\upsilon',
    '\u03c6': r'\phi', '\u03c7': r'\chi', '\u03c8': r'\psi', '\u03c9': r'\omega',
    '\u03d1': r'\vartheta', '\u03d5': r'\varphi', '\u03d6': r'\varpi',
    '\u03f0': r'\varkappa', '\u03f1': r'\varrho', '\u03f5': r'\varepsilon',
    # Uppercase
    '\u0391': r'\Alpha', '\u0392': r'\Beta', '\u0393': r'\Gamma', '\u0394': r'\Delta',
    '\u0395': r'\Epsilon', '\u0396': r'\Zeta', '\u0397': r'\Eta', '\u0398': r'\Theta',
    '\u0399': r'\Iota', '\u039a': r'\Kappa', '\u039b': r'\Lambda', '\u039c': r'\Mu',
    '\u039d': r'\Nu', '\u039e': r'\Xi', '\u039f': r'\Omicron', '\u03a0': r'\Pi',
    '\u03a1': r'\Rho', '\u03a3': r'\Sigma', '\u03a4': r'\Tau', '\u03a5': r'\Upsilon',
    '\u03a6': r'\Phi', '\u03a7': r'\Chi', '\u03a8': r'\Psi', '\u03a9': r'\Omega',
}

# === MATHEMATICAL SYMBOLS ===
SYMBOLS = {
    # Operators and relations
    '\u221e': r'\infty', '\u2211': r'\sum', '\u220f': r'\prod', '\u222b': r'\int',
    '\u222c': r'\iint', '\u222d': r'\iiint', '\u222e': r'\oint',
    '\u2207': r'\nabla', '\u2202': r'\partial', '\u00b1': r'\pm', '\u2213': r'\mp',
    '\u2248': r'\approx', '\u2260': r'\neq', '\u2264': r'\leq', '\u2265': r'\geq',
    '\u226a': r'\ll', '\u226b': r'\gg', '\u2261': r'\equiv', '\u223c': r'\sim',
    '\u2243': r'\simeq', '\u2245': r'\cong', '\u221d': r'\propto',
    # Arrows
    '\u2192': r'\rightarrow', '\u2190': r'\leftarrow', '\u2191': r'\uparrow',
    '\u2193': r'\downarrow', '\u2194': r'\leftrightarrow', '\u2195': r'\updownarrow',
    '\u21d2': r'\Rightarrow', '\u21d0': r'\Leftarrow', '\u21d4': r'\Leftrightarrow',
    '\u21a6': r'\mapsto', '\u2197': r'\nearrow', '\u2198': r'\searrow',
    # Set theory
    '\u2205': r'\emptyset', '\u2229': r'\cap', '\u222a': r'\cup',
    '\u2208': r'\in', '\u2209': r'\notin', '\u220b': r'\ni', '\u220c': r'\notni',
    '\u2282': r'\subset', '\u2283': r'\supset', '\u2286': r'\subseteq', '\u2287': r'\supseteq',
    '\u2284': r'\not\subset', '\u2285': r'\not\supset',
    # Arithmetic
    '\u00d7': r'\times', '\u00f7': r'\div', '\u00b7': r'\cdot', '\u2217': r'\ast',
    '\u2218': r'\circ', '\u2219': r'\bullet', '\u221a': r'\sqrt{}',
    '\u2295': r'\oplus', '\u2296': r'\ominus', '\u2297': r'\otimes', '\u2298': r'\oslash',
    '\u2299': r'\odot', '\u22c5': r'\cdot',
    # Brackets
    '\u27e8': r'\langle', '\u27e9': r'\rangle', '\u2329': r'\langle', '\u232a': r'\rangle',
    '\u230a': r'\lfloor', '\u230b': r'\rfloor', '\u2308': r'\lceil', '\u2309': r'\rceil',
    # Blackboard bold (number sets)
    '\u2115': r'\mathbb{N}', '\u2124': r'\mathbb{Z}', '\u211a': r'\mathbb{Q}',
    '\u211d': r'\mathbb{R}', '\u2102': r'\mathbb{C}', '\u210d': r'\mathbb{H}',
    '\u2119': r'\mathbb{P}', '\u1d538': r'\mathbb{A}',  # Adele ring (KIF-26)
    '\U0001D538': r'\mathbb{A}',  # Alternative encoding for 𝔸
    # Physics-specific (KIF-26)
    '\u0127': r'\hbar',  # ħ (reduced Planck constant)
    '\u2113': r'\ell',   # ℓ (script ell, Planck length)
    '\u212b': r'\text{\AA}',  # Å (Angstrom)
    '\u2126': r'\Omega',  # Ω (Ohm, also Greek Omega)
    # Logic
    '\u2200': r'\forall', '\u2203': r'\exists', '\u2204': r'\nexists',
    '\u00ac': r'\neg', '\u2227': r'\land', '\u2228': r'\lor',
    '\u22a2': r'\vdash', '\u22a8': r'\models', '\u22a4': r'\top', '\u22a5': r'\bot',
    # Miscellaneous
    '\u2026': r'\ldots', '\u22ef': r'\cdots', '\u22ee': r'\vdots', '\u22f1': r'\ddots',
    '\u2032': r"'", '\u2033': r"''", '\u2034': r"'''",  # Primes
    '\u2020': r'\dagger', '\u2021': r'\ddagger', '\u2022': r'\bullet',
    '\u2118': r'\wp',  # Weierstrass p
    '\u2135': r'\aleph', '\u2136': r'\beth', '\u2137': r'\gimel', '\u2138': r'\daleth',
    '\u210f': r'\hbar',  # Alternative h-bar encoding
    '\u2223': r'\mid', '\u2225': r'\parallel', '\u22a5': r'\perp',
}

# === SUBSCRIPT DIGITS (U+2080 - U+2089) ===
SUBSCRIPT_DIGITS = {
    '\u2080': '0', '\u2081': '1', '\u2082': '2', '\u2083': '3', '\u2084': '4',
    '\u2085': '5', '\u2086': '6', '\u2087': '7', '\u2088': '8', '\u2089': '9',
}

# === SUBSCRIPT LETTERS (U+2090 - U+209C) — KIF-26 FIX ===
SUBSCRIPT_LETTERS = {
    '\u2090': 'a', '\u2091': 'e', '\u2092': 'o', '\u2093': 'x',
    '\u2094': r'\schwa',  # ₔ (schwa) - rare, use text mode
    '\u2095': 'h', '\u2096': 'k', '\u2097': 'l', '\u2098': 'm',
    '\u2099': 'n', '\u209a': 'p', '\u209b': 's', '\u209c': 't',
    # Additional subscript letters from other Unicode blocks
    '\u1d62': 'i', '\u1d63': 'r', '\u1d64': 'u', '\u1d65': 'v',
    '\u1d66': r'\beta', '\u1d67': r'\gamma', '\u1d68': r'\rho', '\u1d69': r'\phi',
    '\u1d6a': r'\chi', '\u2c7c': 'j',
}

# === SUPERSCRIPT DIGITS ===
SUPERSCRIPT_DIGITS = {
    '\u2070': '0', '\u00b9': '1', '\u00b2': '2', '\u00b3': '3', '\u2074': '4',
    '\u2075': '5', '\u2076': '6', '\u2077': '7', '\u2078': '8', '\u2079': '9',
    '\u207a': '+', '\u207b': '-', '\u207c': '=', '\u207d': '(', '\u207e': ')',
}

# === SUPERSCRIPT LETTERS — KIF-26 FIX ===
SUPERSCRIPT_LETTERS = {
    '\u1d43': 'a', '\u1d47': 'b', '\u1d9c': 'c', '\u1d48': 'd', '\u1d49': 'e',
    '\u1da0': 'f', '\u1d4d': 'g', '\u02b0': 'h', '\u2071': 'i', '\u02b2': 'j',
    '\u1d4f': 'k', '\u02e1': 'l', '\u1d50': 'm', '\u207f': 'n', '\u1d52': 'o',
    '\u1d56': 'p', '\u02b3': 'r', '\u02e2': 's', '\u1d57': 't', '\u1d58': 'u',
    '\u1d5b': 'v', '\u02b7': 'w', '\u02e3': 'x', '\u02b8': 'y', '\u1dbb': 'z',
    # Greek superscripts
    '\u1d45': r'\alpha', '\u1d5d': r'\beta', '\u1d5e': r'\gamma', '\u1d5f': r'\delta',
    '\u1d60': r'\phi', '\u1d61': r'\chi',
}

# Bra-ket notation: |x>, <x|, <x|y> -- must run before generic symbol pass
BRAKET_PATTERNS = [
    (re.compile(r'\u27e8([^\u27e8\u27e9]+)\|([^\u27e8\u27e9]+)\u27e9'), r'\\langle \1 | \2 \\rangle'),
    (re.compile(r'\|([^\u27e8\u27e9|]+)\u27e9'), r'|\1\\rangle'),
    (re.compile(r'\u27e8([^\u27e8\u27e9|]+)\|'), r'\\langle \1|'),
]


def _split_math_spans(text):
    """Split text into a list of (segment, is_math) tuples on $$...$$ and $...$."""
    pattern = re.compile(r'(\$\$.*?\$\$|\$[^$\n]*?\$)', re.DOTALL)
    parts = []
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            parts.append((text[last:m.start()], False))
        parts.append((m.group(0), True))
        last = m.end()
    if last < len(text):
        parts.append((text[last:], False))
    return parts


def convert_prose_unicode(segment):
    """Convert Unicode math characters to LaTeX ONLY within a non-math segment,
    wrapping each converted run in $...$ so LaTeX renders it as math."""
    out = []
    buf = []
    
    # Build the complete set of convertible characters
    convertible = (
        set(GREEK) | set(SYMBOLS) | 
        set(SUBSCRIPT_DIGITS) | set(SUBSCRIPT_LETTERS) |
        set(SUPERSCRIPT_DIGITS) | set(SUPERSCRIPT_LETTERS)
    )

    i = 0
    n = len(segment)
    while i < n:
        # Try bra-ket multi-char patterns first at this position
        matched_braket = False
        for pat, repl in BRAKET_PATTERNS:
            m = pat.match(segment, i)
            if m:
                if buf:
                    out.append(''.join(buf))
                    buf = []
                out.append('$' + pat.sub(repl, m.group(0)) + '$')
                i = m.end()
                matched_braket = True
                break
        if matched_braket:
            continue

        ch = segment[i]
        if ch in convertible:
            run = []
            while i < n and segment[i] in convertible:
                c = segment[i]
                if c in GREEK:
                    run.append(GREEK[c])
                elif c in SYMBOLS:
                    run.append(SYMBOLS[c])
                elif c in SUBSCRIPT_DIGITS:
                    run.append('_{' + SUBSCRIPT_DIGITS[c] + '}')
                elif c in SUBSCRIPT_LETTERS:
                    run.append('_{' + SUBSCRIPT_LETTERS[c] + '}')
                elif c in SUPERSCRIPT_DIGITS:
                    run.append('^{' + SUPERSCRIPT_DIGITS[c] + '}')
                elif c in SUPERSCRIPT_LETTERS:
                    run.append('^{' + SUPERSCRIPT_LETTERS[c] + '}')
                i += 1
            if buf:
                out.append(''.join(buf))
                buf = []
            out.append('$' + ''.join(run) + '$')
        else:
            buf.append(ch)
            i += 1
    if buf:
        out.append(''.join(buf))
    return ''.join(out)


def strip_keywords_field(frontmatter):
    """Remove a top-level `keywords:` YAML key and any indented continuation
    lines (block scalar or list items) that belong to it."""
    lines = frontmatter.split('\n')
    out = []
    skipping = False
    for line in lines:
        if re.match(r'^keywords\s*:', line):
            skipping = True
            continue
        if skipping:
            if re.match(r'^(\s+\S|\s*-\s)', line):
                continue
            skipping = False
        out.append(line)
    return '\n'.join(out)


def process_file(path, out_path=None):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split frontmatter (--- ... ---) from body
    fm_match = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if fm_match:
        frontmatter = fm_match.group(1)
        body = text[fm_match.end():]
        frontmatter = strip_keywords_field(frontmatter)
        header = f'---\n{frontmatter}\n---\n'
    else:
        header = ''
        body = text

    segments = _split_math_spans(body)
    new_segments = []
    for seg, is_math in segments:
        if is_math:
            new_segments.append(seg)
        else:
            new_segments.append(convert_prose_unicode(seg))
    new_body = ''.join(new_segments)

    result = header + new_body
    target = out_path or path
    with open(target, 'w', encoding='utf-8') as f:
        f.write(result)
    return target


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', help='Path to paper.md')
    ap.add_argument('--out', default=None, help='Output path (default: overwrite input)')
    args = ap.parse_args()

    target = process_file(args.input, args.out)
    print(f'[OK] Unicode-to-LaTeX preprocessing complete: {target}')
    print('[NOTE] Run check-pdf.py after building to verify zero replacement characters.')


if __name__ == '__main__':
    main()
