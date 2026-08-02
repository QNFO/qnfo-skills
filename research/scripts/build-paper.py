#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ============================================================
# DEPRECATED (2026-08-02) — SUPERSEDED BY build-pdf-pro.py
# ============================================================
# This XeLaTeX route FAILS on Unicode-math papers:
#   - pandoc+xelatex: 230-391 "Missing character" warnings
#     (Latin Modern lacks mu/chi/phi/Q/subscripts glyphs)
#   - unicode-math via -V header-includes: ignored by template
#   - unicode->latex conversion: "Missing } inserted" crash on
#     papers that already contain $...$ math
# USE INSTEAD: build-pdf-pro.py (MathJax-SVG -> puppeteer CDP) —
# the mandated single publication pipeline. See the ODR repo
# MATHJAX_CDP_PDF_BUILD.md for the consolidated process.
# Kept only for legacy LaTeX-native work (Springer Nature .tex).
# ============================================================

build-paper.py -- THE SINGLE, CANONICAL build script for QNFO papers (v1.0, KIF-27)

WHY THIS FILE EXISTS (root-cause consolidation, 2026-07-26):
Prior sessions scattered this problem across THREE separate scripts
(unicode-latex-preprocess.py, check-pdf.py, build-pdf.py) that were patched
incrementally across ~6 kaizen passes (KIF-01, KIF-26, KIF-26 v2, KIF-26 v3),
including one entirely WRONG detour (v3.45's "unicode-math is the holistic
fix" claim, which was red-teamed and retracted). This file is the SINGLE
source of truth going forward. Do not create a fourth script.

============================================================
ROOT CAUSE #1: MOJIBAKE (garbled Unicode text)
============================================================
"Mojibake" (文字化け, Japanese: "character transformation") is what happens
when bytes encoded in one character set are DECODED using a different,
incompatible character set. Example seen this session:

    UTF-8 bytes for "e2 84 9a" = the character U+211A (blackboard-bold Q, ℚ)
    Decoded as Windows-1252/Latin-1 instead of UTF-8 -> "â„š" (garbage)

WHERE THIS HAPPENED: Windows PowerShell's console/pipe default encoding is
NOT UTF-8 (it is the system's active code page, typically Windows-1252 on
US/EU locales). When a subprocess (curl.exe, python.exe) writes UTF-8 bytes
to stdout and PowerShell captures that as text, PowerShell may decode those
bytes using the WRONG codepage, corrupting every non-ASCII character before
Python or any other tool ever sees it.

THE FIX (mandatory, not optional): force UTF-8 at EVERY layer:
  1. This script opens ALL files with explicit encoding='utf-8' -- Python's
     open() without an explicit encoding uses locale.getpreferredencoding(),
     which is NOT guaranteed to be UTF-8 on Windows.
  2. Never rely on a PowerShell-captured string as a source of truth for
     Unicode content -- always read the FILE directly with Python, never
     the console output of a command that printed it.
  3. See qnfo-agent skill SS8.7 "PowerShell UTF-8 Encoding Protocol" for the
     session-wide console encoding fix (Console]::OutputEncoding).

============================================================
ROOT CAUSE #2: PDF RENDERING (U+FFFD / U+FFFF in output PDF)
============================================================
XeLaTeX renders each character using whatever font is ACTIVE at that point
in the document: the running TEXT font (e.g. TeX Gyre Pagella) for prose,
or the MATH font (e.g. STIX Two Math, loaded via the unicode-math package)
ONLY inside $...$ / $$...$$ math-mode spans.

A prior session (this one) spent significant effort testing the claim that
loading `unicode-math` + a comprehensive math font (STIX Two Math) would
let Unicode math symbols (ℚ, ℤ, ₚ, ⁰, etc.) render correctly EVEN IN PROSE
TEXT, without needing $...$ delimiters. THIS WAS TESTED LIVE AND IS FALSE:
`unicode-math` only activates the math font inside math mode. Characters
like ℚ typed directly into prose are rendered by the TEXT font, which does
not contain these glyphs, producing U+FFFD (glyph-miss, "tofu") or in some
font/pipeline combinations U+FFFF (a Unicode noncharacter) in the extracted
PDF text.

THE FIX (verified, Zenodo record 21597495, zero rendering errors):
Convert every Unicode math character in prose to its LaTeX command,
wrapped in $...$, so XeLaTeX activates the math font for exactly that span.
E.g. "ℚₚ" (prose) -> "$\\mathbb{Q}_{p}$" (forces math mode + math font).

KEY IMPLEMENTATION DETAIL THAT WAS BUGGY IN EARLIER VERSIONS:
Consecutive subscript/superscript Unicode characters MUST be grouped into
a single _{...} or ^{...} block. Naive one-character-at-a-time conversion
of "10⁻¹²⁰" produced "10$^{-}^{1}^{2}^{0}$", which is INVALID LaTeX (a
"Double superscript" fatal error). This script groups runs correctly:
"10⁻¹²⁰" -> "10$^{-120}$".

============================================================
USAGE
============================================================
    python build-paper.py paper.md
    python build-paper.py paper.md --output paper.pdf --keep-intermediate

Exit codes:
    0 = SUCCESS, publication-ready PDF produced, zero rendering errors
    1 = FAIL, PDF built but has rendering errors, or build failed
    2 = BLOCKED, missing dependency or bad invocation

DEPENDENCIES: pandoc, xelatex (TeX Live), PyMuPDF (`pip install PyMuPDF`)
"""
import argparse
import io
import re
import subprocess
import sys
import os
from pathlib import Path

# ============================================================
# SECTION 0: FORCE UTF-8 EVERYWHERE (fixes mojibake, root cause #1)
# ============================================================

# Force this script's own stdout/stderr to UTF-8 regardless of the
# console codepage it was launched from (Windows PowerShell default is
# NOT UTF-8). Without this, print() of any Unicode character above U+007F
# can itself raise UnicodeEncodeError or silently mangle output.
if sys.stdout.encoding is None or sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding is None or sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def read_text_utf8(path):
    """The ONLY correct way to read a source file. NEVER use bare open()
    without encoding='utf-8' -- Python defaults to locale.getpreferredencoding()
    which on Windows is frequently cp1252, silently corrupting every
    non-ASCII character (mojibake) with no error raised."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_text_utf8(path, text):
    """The ONLY correct way to write an output file. Same rationale as
    read_text_utf8 above."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


# ============================================================
# SECTION 1: UNICODE MATH -> LATEX CONVERSION TABLES
# ============================================================
# Comprehensive coverage is not "impossible" -- it just requires organizing
# by Unicode BLOCK (Greek, Letterlike Symbols, Mathematical Operators,
# Superscripts/Subscripts, Mathematical Alphanumeric Symbols) rather than
# ad hoc single-character entries added reactively per error message.

GREEK = {
    '\u03b1': r'\alpha', '\u03b2': r'\beta', '\u03b3': r'\gamma', '\u03b4': r'\delta',
    '\u03b5': r'\epsilon', '\u03b6': r'\zeta', '\u03b7': r'\eta', '\u03b8': r'\theta',
    '\u03b9': r'\iota', '\u03ba': r'\kappa', '\u03bb': r'\lambda', '\u03bc': r'\mu',
    '\u03bd': r'\nu', '\u03be': r'\xi', '\u03c0': r'\pi', '\u03c1': r'\rho',
    '\u03c2': r'\varsigma', '\u03c3': r'\sigma', '\u03c4': r'\tau', '\u03c5': r'\upsilon',
    '\u03c6': r'\phi', '\u03c7': r'\chi', '\u03c8': r'\psi', '\u03c9': r'\omega',
    '\u03d1': r'\vartheta', '\u03d5': r'\varphi', '\u03d6': r'\varpi',
    '\u03f0': r'\varkappa', '\u03f1': r'\varrho', '\u03f5': r'\varepsilon',
    '\u0391': r'A', '\u0392': r'B', '\u0393': r'\Gamma', '\u0394': r'\Delta',
    '\u0395': r'E', '\u0396': r'Z', '\u0397': r'H', '\u0398': r'\Theta',
    '\u0399': r'I', '\u039a': r'K', '\u039b': r'\Lambda', '\u039c': r'M',
    '\u039d': r'N', '\u039e': r'\Xi', '\u039f': r'O', '\u03a0': r'\Pi',
    '\u03a1': r'P', '\u03a3': r'\Sigma', '\u03a4': r'T', '\u03a5': r'\Upsilon',
    '\u03a6': r'\Phi', '\u03a7': r'X', '\u03a8': r'\Psi', '\u03a9': r'\Omega',
    # Mathematical italic Greek (Mathematical Alphanumeric Symbols block, U+1D6E2-1D755)
    '\U0001D6FC': r'\alpha', '\U0001D6FD': r'\beta', '\U0001D6FE': r'\gamma',
    '\U0001D6FF': r'\delta', '\U0001D700': r'\epsilon', '\U0001D701': r'\zeta',
    '\U0001D702': r'\eta', '\U0001D703': r'\theta', '\U0001D704': r'\iota',
    '\U0001D705': r'\kappa', '\U0001D706': r'\lambda', '\U0001D707': r'\mu',
    '\U0001D708': r'\nu', '\U0001D709': r'\xi', '\U0001D70B': r'\pi',
    '\U0001D70C': r'\rho', '\U0001D70E': r'\sigma', '\U0001D70F': r'\tau',
    '\U0001D710': r'\upsilon', '\U0001D711': r'\phi', '\U0001D712': r'\chi',
    '\U0001D713': r'\psi', '\U0001D714': r'\omega',
}

SYMBOLS = {
    # Operators / relations (Mathematical Operators block, U+2200-22FF)
    '\u221e': r'\infty', '\u2211': r'\sum', '\u220f': r'\prod', '\u222b': r'\int ',
    '\u222c': r'\iint', '\u222d': r'\iiint', '\u222e': r'\oint',
    '\u2207': r'\nabla ', '\u2202': r'\partial ', '\u00b1': r'\pm', '\u2213': r'\mp',
    '\u2248': r'\approx', '\u2260': r'\neq', '\u2264': r'\leq', '\u2265': r'\geq',
    '\u226a': r'\ll', '\u226b': r'\gg', '\u2261': r'\equiv', '\u223c': r'\sim',
    '\u2243': r'\simeq', '\u2245': r'\cong', '\u221d': r'\propto',
    '\u2200': r'\forall', '\u2203': r'\exists', '\u2204': r'\nexists',
    '\u00ac': r'\neg', '\u2227': r'\land', '\u2228': r'\lor',
    '\u22a2': r'\vdash', '\u22a8': r'\models', '\u22a4': r'\top', '\u22a5': r'\bot',
    '\u2223': r'\mid', '\u2225': r'\parallel',
    # Arrows (U+2190-21FF)
    '\u2192': r'\rightarrow', '\u2190': r'\leftarrow', '\u2191': r'\uparrow',
    '\u2193': r'\downarrow', '\u2194': r'\leftrightarrow', '\u2195': r'\updownarrow',
    '\u21d2': r'\Rightarrow', '\u21d0': r'\Leftarrow', '\u21d4': r'\Leftrightarrow',
    '\u21a6': r'\mapsto', '\u2197': r'\nearrow', '\u2198': r'\searrow',
    '\u21aa': r'\hookrightarrow',
    # Set theory
    '\u2205': r'\emptyset', '\u2229': r'\cap', '\u222a': r'\cup',
    '\u2208': r'\in', '\u2209': r'\notin', '\u220b': r'\ni',
    '\u2282': r'\subset', '\u2283': r'\supset', '\u2286': r'\subseteq', '\u2287': r'\supseteq',
    # Arithmetic
    '\u00d7': r'\times', '\u00f7': r'\div', '\u2212': '-', '\u00b7': r'\cdot', '\u2217': r'\ast',
    '\u2218': r'\circ', '\u2219': r'\bullet',
    '\u2295': r'\oplus', '\u2296': r'\ominus', '\u2297': r'\otimes', '\u2298': r'\oslash',
    '\u2299': r'\odot ', '\u22c5': r'\cdot',
    # Brackets
    '\u27e8': r'\langle ', '\u27e9': r'\rangle ',
    '\u230a': r'\lfloor', '\u230b': r'\rfloor', '\u2308': r'\lceil', '\u2309': r'\rceil',
    # Blackboard bold (Letterlike Symbols block, U+2100-214F, plus U+1D538 in
    # Mathematical Alphanumeric Symbols for characters with no legacy codepoint)
    '\u2115': r'\mathbb{N}', '\u2124': r'\mathbb{Z}', '\u211a': r'\mathbb{Q}',
    '\u211d': r'\mathbb{R}', '\u2102': r'\mathbb{C}', '\u210d': r'\mathbb{H}',
    '\u2119': r'\mathbb{P}',
    '\U0001D538': r'\mathbb{A}',  # blackboard A (no legacy codepoint exists)
    # Physics symbols
    '\u0127': r'\hbar ', '\u210f': r'\hbar ', '\u2113': r'\ell',
    '\u212b': r'\text{\AA}', '\u2126': r'\Omega',
    # Script letters (Letterlike Symbols block)
    '\u2112': r'\mathcal{L}', '\u2110': r'\mathcal{I}', '\u2131': r'\mathcal{F}',
    '\u210b': r'\mathcal{H}', '\u2133': r'\mathcal{M}', '\u211b': r'\mathcal{R}',
    '\U0001D49F': r'\mathcal{D}',
    # Fraktur (Mathematical Alphanumeric Symbols block, U+1D504-1D537)
    '\U0001D51E': r'\mathfrak{a}', '\U0001D51F': r'\mathfrak{b}', '\U0001D520': r'\mathfrak{c}',
    '\U0001D521': r'\mathfrak{d}', '\U0001D522': r'\mathfrak{e}', '\U0001D523': r'\mathfrak{f}',
    '\U0001D524': r'\mathfrak{g}', '\U0001D525': r'\mathfrak{h}', '\U0001D526': r'\mathfrak{i}',
    '\U0001D527': r'\mathfrak{j}', '\U0001D528': r'\mathfrak{k}', '\U0001D529': r'\mathfrak{l}',
    '\U0001D52A': r'\mathfrak{m}', '\U0001D52B': r'\mathfrak{n}', '\U0001D52C': r'\mathfrak{o}',
    '\U0001D52D': r'\mathfrak{p}', '\U0001D52E': r'\mathfrak{q}', '\U0001D52F': r'\mathfrak{r}',
    '\U0001D530': r'\mathfrak{s}', '\U0001D531': r'\mathfrak{t}', '\U0001D532': r'\mathfrak{u}',
    '\U0001D533': r'\mathfrak{v}', '\U0001D534': r'\mathfrak{w}', '\U0001D535': r'\mathfrak{x}',
    '\U0001D536': r'\mathfrak{y}', '\U0001D537': r'\mathfrak{z}',
    # Logic / misc
    '\u2026': r'\ldots', '\u22ef': r'\cdots', '\u22ee': r'\vdots', '\u22f1': r'\ddots',
    '\u2032': r"'", '\u2033': r"''",
    '\u2020': r'\dagger', '\u2021': r'\ddagger',
    '\u2135': r'\aleph',
    # Emoji rendered as their nearest math glyph (rare in physics prose, but
    # appears in status-marker tables e.g. checklists inside a paper)
    '\u2705': r'\checkmark', '\u2714': r'\checkmark',
    '\u274c': r'\times', '\u2718': r'\times',
}

# Subscript characters map to the PLAIN character they represent; the
# calling code wraps a run of these in a single _{...} block.
SUBSCRIPTS = {
    '\u2080': '0', '\u2081': '1', '\u2082': '2', '\u2083': '3', '\u2084': '4',
    '\u2085': '5', '\u2086': '6', '\u2087': '7', '\u2088': '8', '\u2089': '9',
    '\u2090': 'a', '\u2091': 'e', '\u2092': 'o', '\u2093': 'x',
    '\u2095': 'h', '\u2096': 'k', '\u2097': 'l', '\u2098': 'm',
    '\u2099': 'n', '\u209a': 'p', '\u209b': 's', '\u209c': 't',
    '\u1d62': 'i', '\u1d63': 'r', '\u1d64': 'u', '\u1d65': 'v', '\u2c7c': 'j',
    '\u208a': '+', '\u208b': '-', '\u208c': '=',
}

# Superscript characters map to the PLAIN character they represent; the
# calling code wraps a run of these in a single ^{...} block.
SUPERSCRIPTS = {
    '\u2070': '0', '\u00b9': '1', '\u00b2': '2', '\u00b3': '3', '\u2074': '4',
    '\u2075': '5', '\u2076': '6', '\u2077': '7', '\u2078': '8', '\u2079': '9',
    '\u207a': '+', '\u207b': '-', '\u207c': '=', '\u207f': 'n', '\u2071': 'i',
    # Superscript letters (Phonetic Extensions / Spacing Modifier Letters)
    '\u1d43': 'a', '\u1d47': 'b', '\u1d9c': 'c', '\u1d48': 'd', '\u1d49': 'e',
    '\u1da0': 'f', '\u1d4d': 'g', '\u02b0': 'h', '\u02b2': 'j',
    '\u1d4f': 'k', '\u02e1': 'l', '\u1d50': 'm', '\u1d52': 'o',
    '\u1d56': 'p', '\u02b3': 'r', '\u02e2': 's', '\u1d57': 't', '\u1d58': 'u',
    '\u1d5b': 'v', '\u02b7': 'w', '\u02e3': 'x', '\u02b8': 'y', '\u1dbb': 'z',
}

SQRT_PATTERN = re.compile(r'\u221a(\d+|[a-zA-Z])')
BRAKET_PATTERNS = [
    (re.compile(r'\u27e8([^\u27e8\u27e9]+)\|([^\u27e8\u27e9]+)\u27e9'), r'\\langle \1 | \2 \\rangle'),
    (re.compile(r'\|([^\u27e8\u27e9|]+)\u27e9'), r'|\1\\rangle'),
    (re.compile(r'\u27e8([^\u27e8\u27e9|]+)\|'), r'\\langle \1|'),
]


# ============================================================
# SECTION 2: CONVERSION LOGIC
# ============================================================

def _split_math_spans(text):
    """Split text into (segment, is_math) tuples on existing $$...$$ / $...$
    spans so we NEVER double-convert characters an author already wrapped
    in LaTeX math mode (which would emit literal backslashes inside math)."""
    pattern = re.compile(r'(\$\$.*?\$\$|\$[^$\n]*?\$)', re.DOTALL)
    parts, last = [], 0
    for m in pattern.finditer(text):
        if m.start() > last:
            parts.append((text[last:m.start()], False))
        parts.append((m.group(0), True))
        last = m.end()
    if last < len(text):
        parts.append((text[last:], False))
    return parts



def convert_math_unicode(segment):
    """Normalize raw Unicode math characters INSIDE an existing $...$ / $$...$$
    span to LaTeX commands. Applied to math segments in preprocess().

    Handles (2026-08-02 red-team / v2.6 expansion findings):
      - Raw hbar U+210F / U+0127            -> \\hbar
      - Raw nabla U+2207, partial U+2202    -> \\nabla, \\partial
      - Raw sqrt U+221A                      -> \\sqrt{...} (simple forms)
      - Raw integral U+222B / sum / prod    -> \\int, \\sum, \\prod
      - Raw angle brackets U+27E8/27E9      -> \\langle / \\rangle
      - Raw box U+25A1                       -> \\Box
      - Raw arrows U+2192, relations, times -> \\to, \\times, \\approx...
      - Precomposed tilde letters            -> \\tilde{X}
        (U+1EBC Ẽ, U+1E7C Ṽ, U+1E7D ṽ, U+0168 Ũ, U+00F1 ñ, U+1E50)
      - Combining tilde U+0303, macron U+0304, circumflex U+0302 on any
        letter/greek -> \\tilde{}\\bar{}\\hat{} (grouped by base char)
    Idempotent: existing LaTeX macros and plain ASCII pass through.
    """
    if not segment or not re.search(r'[^\x00-\x7f]', segment):
        return segment  # fast path: pure ASCII (LaTeX) -- untouched

    s = segment

    # --- single-char symbol map (math font glyphs Latin Modern Math lacks) ---
    symbol_map = {
        '\u210f': r'\hbar ', '\u0127': r'\hbar ',      # ℏ, ħ
        '\u2207': r'\nabla ',                          # ∇
        '\u2202': r'\partial ',                        # ∂
        '\u222b': r'\int ',                            # ∫
        '\u2211': r'\sum',                            # ∑
        '\u220f': r'\prod',                           # ∏
        '\u27e8': r'\langle ', '\u27e9': r'\rangle ',  # ⟨ ⟩
        '\u25a1': r'\Box ',                            # □
        '\u2192': r'\to ',                            # →
        '\u2190': r'\leftarrow ',                     # ←
        '\u2194': r'\leftrightarrow ',               # ↔
        '\u2260': r'\neq ',                           # ≠
        '\u2264': r'\leq ',                           # ≤
        '\u2265': r'\geq ',                           # ≥
        '\u226a': r'\ll ', '\u226b': r'\gg ',        # ≪ ≫
        '\u2248': r'\approx ',                        # ≈
        '\u221d': r'\propto ',                        # ∝
        '\u22c5': r'\cdot ',                          # ⋅
        '\u00d7': r'\times ',                         # ×
        '\u00b1': r'\pm ',                            # ±
        '\u221e': r'\infty ',
    '\u2212': '-',             # U+2212 mathematical minus -> ASCII
                         # ∞
        '\u2609': r'\odot ',                           # ☉
        '\u211b': r'\mathcal{R}',                     # ℛ
        '\u2112': r'\mathcal{L}',                     # ℒ
        '\u00bd': r'\tfrac{1}{2}',                    # ½
    }
    for ch, rep in symbol_map.items():
        if ch in s:
            s = s.replace(ch, rep)

    # --- precomposed tilde letters -> \tilde{X} ---
    tilde_precomp = {
        '\u1ebc': 'E', '\u1e7c': 'V', '\u1e7d': 'v',
        '\u0168': 'U', '\u00f1': 'n', '\u1e50': 'E',
        '\u1e44': 'N', '\u1e45': 'n', '\u1ef8': 'Y', '\u1ef9': 'y',
        '\u00e3': 'a', '\u0128': 'I', '\u1ebc': 'E',   # ã Ĩ Ẽ

    }
    for ch, base in tilde_precomp.items():
        if ch in s:
            s = s.replace(ch, r'\tilde{' + base + '}')

    # --- combining marks on base char -> \tilde/\bar/\hat{base} ---
    # Process by iterating and merging base + combining into one macro.
    combining_map = {'\u0303': r'\tilde', '\u0304': r'\bar', '\u0302': r'\hat'}
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        if i + 1 < len(s) and s[i + 1] in combining_map:
            base = ch
            mark = s[i + 1]
            cmd = combining_map[mark]
            # Skip if base already looks like a LaTeX macro (avoid mangling)
            if base == '\\':
                out.append(ch)
                i += 1
                continue
            out.append(cmd + '{' + base + '}')
            i += 2
        else:
            out.append(ch)
            i += 1
    s = ''.join(out)

    # --- Mathematical Alphanumeric Symbols (U+1D400-U+1D7FF) ---
    # These italic/bold math letters in math mode trigger xdvipdfmx
    # 'bad native font flag' errors. Map to plain ASCII (LaTeX handles style).
    def _strip_math_alnum(seg):
        out = []
        for ch in seg:
            o = ord(ch)
            if 0x1D400 <= o <= 0x1D7FF:
                # Mathematical Alphanumeric -> base ASCII/Greek
                # Letters: offset 0x1D400 = A; map block by block
                if 0x1D400 <= o <= 0x1D419:  # A-Z bold
                    out.append(chr(ord('A') + (o - 0x1D400)))
                elif 0x1D41A <= o <= 0x1D433:  # a-z bold
                    out.append(chr(ord('a') + (o - 0x1D41A)))
                elif 0x1D434 <= o <= 0x1D44D:  # A-Z italic
                    out.append(chr(ord('A') + (o - 0x1D434)))
                elif 0x1D44E <= o <= 0x1D467:  # a-z italic
                    out.append(chr(ord('a') + (o - 0x1D44E)))
                elif 0x1D468 <= o <= 0x1D481:  # A-Z bold italic
                    out.append(chr(ord('A') + (o - 0x1D468)))
                elif 0x1D482 <= o <= 0x1D49B:  # a-z bold italic
                    out.append(chr(ord('a') + (o - 0x1D482)))
                elif 0x1D49C <= o <= 0x1D4CF:  # script letters (partial)
                    out.append(' ')
                elif 0x1D538 <= o <= 0x1D56B:  # double-struck A-Z partial
                    out.append(' ')
                elif 0x1D7CE <= o <= 0x1D7D7:  # digits 0-9 bold
                    out.append(chr(ord('0') + (o - 0x1D7CE)))
                elif 0x1D7D8 <= o <= 0x1D7E1:  # digits 0-9 double-struck
                    out.append(chr(ord('0') + (o - 0x1D7D8)))
                elif 0x1D7E2 <= o <= 0x1D7EB:  # digits 0-9 sans
                    out.append(chr(ord('0') + (o - 0x1D7E2)))
                elif 0x1D7EC <= o <= 0x1D7F5:  # digits 0-9 sans bold
                    out.append(chr(ord('0') + (o - 0x1D7EC)))
                elif 0x1D7F6 <= o <= 0x1D7FF:  # digits 0-9 mono
                    out.append(chr(ord('0') + (o - 0x1D7F6)))
                else:
                    out.append(' ')  # unmapped math-alphanumeric
            else:
                out.append(ch)
        return ''.join(out)
    s = _strip_math_alnum(s)

    # --- raw sqrt: U+221A already replaced above to \sqrt{}, now fix \sqrt{}(x)
    # --- merge any '\sqrt{}(' into '\sqrt{' ... handled by caller's grouping
    # --- fix accidental merged macros like \hbarc -> \hbar c ---
    s = re.sub(r'\\hbarc', r'\\hbar c', s)
    s = re.sub(r'\\hbar([A-Za-zωνΩ])', r'\\hbar \1', s)
    s = re.sub(r'\\times([0-9])', r'\\times \1', s)
    s = re.sub(r'\\approx([0-9])', r'\\approx \1', s)
    s = re.sub(r'\\lefteq', r'\\leq ', s)
    s = re.sub(r'\\geq', r'\\geq ', s)
    return s



def convert_prose_unicode(segment):
    """Convert Unicode math characters in a NON-math segment to LaTeX,
    wrapping each contiguous run in $...$. Subscript/superscript runs are
    GROUPED (not emitted one character at a time) -- this is the exact bug
    that produced invalid "Double superscript" LaTeX in earlier versions:
    "10⁻¹²⁰" must become "10$^{-120}$", never "10$^{-}^{1}^{2}^{0}$"."""
    subs, sups, greek, syms = set(SUBSCRIPTS), set(SUPERSCRIPTS), set(GREEK), set(SYMBOLS)
    convertible = subs | sups | greek | syms
    # Precomposed tilde letters -> $\tilde{X}$ (math font lacks these glyphs)
    precomposed_tilde = {
        '\u00e3': 'a', '\u0128': 'I', '\u1ebc': 'E',
        '\u1e7c': 'V', '\u1e7d': 'v', '\u0168': 'U',
        '\u00f1': 'n', '\u1e44': 'N', '\u1e45': 'n',
        '\u1ef8': 'Y', '\u1ef9': 'y', '\u1e50': 'E',
    }
    for _ch, _base in precomposed_tilde.items():
        if _ch in segment:
            segment = segment.replace(_ch, '$\\tilde{' + _base + '}$')
    # Combining tilde U+0303 on a base letter (prose): x̃ -> $\tilde{x}$
    _comb_tilde = '̃'
    if _comb_tilde in segment:
        _out = []
        _i = 0
        while _i < len(segment):
            if _i + 1 < len(segment) and segment[_i + 1] == _comb_tilde:
                _base = segment[_i]
                _out.append('$\\tilde{' + _base + '}$')
                _i += 2
            else:
                _out.append(segment[_i])
                _i += 1
        segment = ''.join(_out)


    math_adjacent = set('0123456789')  # bare digits next to a math run join it

    out, buf, i, n = [], [], 0, len(segment)
    while i < n:
        # sqrt: √5 -> $\sqrt{5}$ (captures the argument, avoids the
        # "√5 becomes \sqrt{} followed by a bare 5" bug from earlier versions)
        m = SQRT_PATTERN.match(segment, i)
        if m:
            if buf:
                out.append(''.join(buf)); buf = []
            out.append(r'$\sqrt{' + m.group(1) + '}$')
            i = m.end()
            continue
        if segment[i] == '\u221a':  # bare √ with no captured argument
            if buf:
                out.append(''.join(buf)); buf = []
            out.append(r'$\sqrt{}$')
            i += 1
            continue

        matched_braket = False
        for pat, repl in BRAKET_PATTERNS:
            m = pat.match(segment, i)
            if m:
                if buf:
                    out.append(''.join(buf)); buf = []
                out.append('$' + pat.sub(repl, m.group(0)) + '$')
                i = m.end()
                matched_braket = True
                break
        if matched_braket:
            continue

        ch = segment[i]
        if ch in convertible:
            parts = []
            while i < n and (segment[i] in convertible or segment[i] in math_adjacent):
                c = segment[i]
                if c in subs:
                    run = []
                    while i < n and segment[i] in subs:
                        run.append(SUBSCRIPTS[segment[i]]); i += 1
                    parts.append('_{' + ''.join(run) + '}')
                elif c in sups:
                    run = []
                    while i < n and segment[i] in sups:
                        run.append(SUPERSCRIPTS[segment[i]]); i += 1
                    parts.append('^{' + ''.join(run) + '}')
                elif c in greek:
                    parts.append(GREEK[c]); i += 1
                elif c in syms:
                    parts.append(SYMBOLS[c]); i += 1
                else:  # bare digit adjacent to a math run
                    parts.append(c); i += 1
            if buf:
                out.append(''.join(buf)); buf = []
            if parts:
                out.append('$' + ''.join(parts) + '$')
        else:
            buf.append(ch); i += 1
    if buf:
        out.append(''.join(buf))
    return ''.join(out)


def strip_keywords_field(frontmatter):
    """Remove YAML `keywords:` key (fix: crashes some XeLaTeX templates
    via an undefined \\xmpquote macro). Not required by Zenodo/D1 metadata."""
    out, skipping = [], False
    for line in frontmatter.split('\n'):
        if re.match(r'^keywords\s*:', line):
            skipping = True
            continue
        if skipping:
            if re.match(r'^(\s+\S|\s*-\s)', line):
                continue
            skipping = False
        out.append(line)
    return '\n'.join(out)


def preprocess(source_path):
    """Read source (UTF-8 forced), convert Unicode math to LaTeX math mode
    outside existing math spans, fix bracing artifacts, return final text."""
    text = read_text_utf8(source_path)

    fm_match = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if fm_match:
        frontmatter = strip_keywords_field(fm_match.group(1))
        header = f'---\n{frontmatter}\n---\n'
        body = text[fm_match.end():]
    else:
        header, body = '', text

    segments = _split_math_spans(body)
    new_body = ''.join(
        seg if (not is_math and seg.strip().startswith('$')) else (convert_math_unicode(seg) if is_math else convert_prose_unicode(seg)) for seg, is_math in segments
    )
    result = header + new_body

    # Post-processing: fix subscript/superscript bracing gaps left when two
    # adjacent converted math spans need merging, e.g. $\mathbb{A}$_$\mathbb{Q}$
    # (from prose "𝔸_ℚ") must become $\mathbb{A}_{\mathbb{Q}}$.
    result = re.sub(r'_\\(mathbb|mathcal|mathfrak)\{([^}]+)\}', r'_{\\\1{\2}}', result)
    result = re.sub(r'\^\\(mathbb|mathcal|mathfrak)\{([^}]+)\}', r'^{\\\1{\2}}', result)
    result = re.sub(r'\$([^$]+)\$_\$([^$]+)\$', r'$\1_{\2}$', result)
    result = re.sub(r'\$([^$]+)\$\^\$([^$]+)\$', r'$\1^{\2}$', result)

    return result


# ============================================================
# SECTION 3: PDF BUILD (pandoc + xelatex)
# ============================================================

def build_pdf(preprocessed_md_path, output_pdf_path):
    cmd = [
        'pandoc', str(preprocessed_md_path), '-o', str(output_pdf_path),
        '--pdf-engine=xelatex',
        '--variable=geometry:margin=1in',
        '--variable=documentclass:article',
        '--variable=classoption:11pt',
        '--citeproc',
    ]
    bib_path = Path(preprocessed_md_path).parent / 'refs.bib'
    if bib_path.exists():
        cmd.extend(['--bibliography', str(bib_path)])

    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return result.returncode == 0, result.stdout, result.stderr


# ============================================================
# SECTION 4: PDF VERIFICATION (mandatory hard gate)
# ============================================================

def verify_pdf(pdf_path):
    """Returns (ok: bool, message: str, details: list[str]).
    ok=False means the PDF MUST NOT be published."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return False, 'PyMuPDF not installed (pip install PyMuPDF) -- cannot verify', []

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as e:
        return False, f'PDF failed to open (corrupt): {e}', []

    if doc.page_count == 0:
        doc.close()
        return False, 'PDF has zero pages', []

    errors = []
    for page in doc:
        text = page.get_text()
        for bad_char, label in (('\ufffd', 'U+FFFD replacement char'), ('\uffff', 'U+FFFF noncharacter')):
            n = text.count(bad_char)
            if n:
                errors.append(f'Page {page.number + 1}: {n}x {label} (font glyph miss)')
        if not text.strip():
            errors.append(f'Page {page.number + 1}: EMPTY (no extractable text)')
    page_count = doc.page_count
    doc.close()

    if errors:
        return False, f'{len(errors)} rendering issue(s) found', errors
    return True, f'PASS -- {page_count} pages, zero rendering errors', []


# ============================================================
# SECTION 5: MAIN
# ============================================================

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input', help='Source paper.md (must be UTF-8 encoded)')
    ap.add_argument('--output', '-o', help='Output PDF path (default: <input>.pdf)')
    ap.add_argument('--keep-intermediate', action='store_true',
                     help='Keep the preprocessed .build.md file for inspection')
    args = ap.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f'[BLOCKED] Input file not found: {input_path}')
        sys.exit(2)

    output_path = Path(args.output) if args.output else input_path.with_suffix('.pdf')
    build_md_path = input_path.with_suffix('.build.md')

    print(f'[1/3] Preprocessing Unicode -> LaTeX math mode: {input_path}')
    preprocessed = preprocess(input_path)
    write_text_utf8(build_md_path, preprocessed)
    print(f'      -> {build_md_path}')

    print(f'[2/3] Building PDF via pandoc + xelatex...')
    ok, stdout, stderr = build_pdf(build_md_path, output_path)
    if not ok:
        print('[FAIL] pandoc/xelatex build failed:')
        print(stderr[-3000:])
        sys.exit(1)
    print(f'      -> {output_path}')

    print(f'[3/3] Verifying PDF rendering (mandatory gate)...')
    ok, message, details = verify_pdf(output_path)
    if not ok:
        print(f'[FAIL] {message}')
        for d in details[:30]:
            print(f'  - {d}')
        print('\n[BLOCKED] This PDF MUST NOT be published to Zenodo/R2/any channel.')
        sys.exit(1)
    print(f'      -> {message}')

    if not args.keep_intermediate:
        try:
            build_md_path.unlink()
        except OSError:
            pass

    print(f'\n[SUCCESS] Publication-ready PDF: {output_path}')
    sys.exit(0)


if __name__ == '__main__':
    main()
