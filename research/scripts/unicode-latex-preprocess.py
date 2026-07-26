#!/usr/bin/env python3
"""
unicode-latex-preprocess.py -- Pandoc+XeLaTeX pre-build fixer (v3.0, KIF-26 v3)

VERSION: 3.0 (2026-07-26)

THE FUNDAMENTAL PROBLEM:
XeLaTeX text fonts (TeX Gyre Pagella, STIX Two Text, etc.) do NOT contain
mathematical symbols like ℚ, ℤ, ₚ, ⁰, etc. These glyphs only exist in MATH
fonts (STIX Two Math, Latin Modern Math, etc.), which are only used inside
LaTeX math mode ($...$).

THE SOLUTION:
Convert Unicode math characters to LaTeX math commands wrapped in $...$,
so XeLaTeX uses the math font (which has the glyphs) instead of the text
font (which doesn't).

KEY FIX IN v3.0:
Consecutive subscripts/superscripts are now GROUPED into a single ^{...}
or _{...} block. Previously, "10⁻¹²⁰" became "$^{-}^{1}^{2}^{0}$" which is
invalid LaTeX (double superscript error). Now it correctly becomes "$^{-120}$".

Usage:
    python unicode-latex-preprocess.py paper.md
    python unicode-latex-preprocess.py paper.md --out paper.build.md
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
    '\u21aa': r'\hookrightarrow',
    # Set theory
    '\u2205': r'\emptyset', '\u2229': r'\cap', '\u222a': r'\cup',
    '\u2208': r'\in', '\u2209': r'\notin', '\u220b': r'\ni', '\u220c': r'\notni',
    '\u2282': r'\subset', '\u2283': r'\supset', '\u2286': r'\subseteq', '\u2287': r'\supseteq',
    '\u2284': r'\not\subset', '\u2285': r'\not\supset',
    # Arithmetic
    '\u00d7': r'\times', '\u00f7': r'\div', '\u00b7': r'\cdot', '\u2217': r'\ast',
    '\u2218': r'\circ', '\u2219': r'\bullet',
    # Note: √ (U+221A) is handled specially below to capture its argument
    '\u2295': r'\oplus', '\u2296': r'\ominus', '\u2297': r'\otimes', '\u2298': r'\oslash',
    '\u2299': r'\odot', '\u22c5': r'\cdot',
    # Brackets
    '\u27e8': r'\langle', '\u27e9': r'\rangle', '\u2329': r'\langle', '\u232a': r'\rangle',
    '\u230a': r'\lfloor', '\u230b': r'\rfloor', '\u2308': r'\lceil', '\u2309': r'\rceil',
    # Blackboard bold (number sets)
    '\u2115': r'\mathbb{N}', '\u2124': r'\mathbb{Z}', '\u211a': r'\mathbb{Q}',
    '\u211d': r'\mathbb{R}', '\u2102': r'\mathbb{C}', '\u210d': r'\mathbb{H}',
    '\u2119': r'\mathbb{P}', '\u1d538': r'\mathbb{A}',
    '\U0001D538': r'\mathbb{A}',  # Alternative encoding for 𝔸
    # Physics-specific
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
    '\u2223': r'\mid', '\u2225': r'\parallel',
    # Emoji/symbols that need text-mode handling
    '\u2705': r'\checkmark',  # ✅ (green checkmark emoji -> checkmark)
    '\u274c': r'\times',      # ❌ (red X emoji -> times)
    '\u2714': r'\checkmark',  # ✔ (checkmark)
    '\u2718': r'\times',      # ✘ (ballot X)
    # Script letters
    '\u2112': r'\mathcal{L}',  # ℒ (script L / Lagrangian)
    '\u2110': r'\mathcal{I}',  # ℐ (script I)
    '\u2131': r'\mathcal{F}',  # ℱ (script F)
    '\u210b': r'\mathcal{H}',  # ℋ (script H / Hamiltonian)
    '\u2133': r'\mathcal{M}',  # ℳ (script M)
    '\u211b': r'\mathcal{R}',  # ℛ (script R)
    # Mathematical fraktur (from Mathematical Alphanumeric Symbols block)
    '\U0001D530': r'\mathfrak{s}',  # 𝔰
    '\U0001D529': r'\mathfrak{l}',  # 𝔩
    '\U0001D51E': r'\mathfrak{a}',  # 𝔞
    '\U0001D51F': r'\mathfrak{b}',  # 𝔟
    '\U0001D520': r'\mathfrak{c}',  # 𝔠
    '\U0001D521': r'\mathfrak{d}',  # 𝔡
    '\U0001D522': r'\mathfrak{e}',  # 𝔢
    '\U0001D523': r'\mathfrak{f}',  # 𝔣
    '\U0001D524': r'\mathfrak{g}',  # 𝔤
    '\U0001D525': r'\mathfrak{h}',  # 𝔥
    '\U0001D526': r'\mathfrak{i}',  # 𝔦
    '\U0001D527': r'\mathfrak{j}',  # 𝔧
    '\U0001D528': r'\mathfrak{k}',  # 𝔨
    '\U0001D52A': r'\mathfrak{m}',  # 𝔪
    '\U0001D52B': r'\mathfrak{n}',  # 𝔫
    '\U0001D52C': r'\mathfrak{o}',  # 𝔬
    '\U0001D52D': r'\mathfrak{p}',  # 𝔭
    '\U0001D52E': r'\mathfrak{q}',  # 𝔮
    '\U0001D52F': r'\mathfrak{r}',  # 𝔯
    '\U0001D531': r'\mathfrak{t}',  # 𝔱
    '\U0001D532': r'\mathfrak{u}',  # 𝔲
    '\U0001D533': r'\mathfrak{v}',  # 𝔳
    '\U0001D534': r'\mathfrak{w}',  # 𝔴
    '\U0001D535': r'\mathfrak{x}',  # 𝔵
    '\U0001D536': r'\mathfrak{y}',  # 𝔶
    '\U0001D537': r'\mathfrak{z}',  # 𝔷
    # Mathematical italic Greek (from Mathematical Alphanumeric Symbols block)
    '\U0001D6FF': r'\delta',  # 𝛿 (mathematical italic delta)
    '\U0001D6FC': r'\alpha',  # 𝛼 (mathematical italic alpha)
    '\U0001D6FD': r'\beta',   # 𝛽 (mathematical italic beta)
    '\U0001D6FE': r'\gamma',  # 𝛾 (mathematical italic gamma)
    '\U0001D700': r'\epsilon', # 𝜀 (mathematical italic epsilon)
    '\U0001D701': r'\zeta',   # 𝜁 (mathematical italic zeta)
    '\U0001D702': r'\eta',    # 𝜂 (mathematical italic eta)
    '\U0001D703': r'\theta',  # 𝜃 (mathematical italic theta)
    '\U0001D704': r'\iota',   # 𝜄 (mathematical italic iota)
    '\U0001D705': r'\kappa',  # 𝜅 (mathematical italic kappa)
    '\U0001D706': r'\lambda', # 𝜆 (mathematical italic lambda)
    '\U0001D707': r'\mu',     # 𝜇 (mathematical italic mu)
    '\U0001D708': r'\nu',     # 𝜈 (mathematical italic nu)
    '\U0001D709': r'\xi',     # 𝜉 (mathematical italic xi)
    '\U0001D70B': r'\pi',     # 𝜋 (mathematical italic pi)
    '\U0001D70C': r'\rho',    # 𝜌 (mathematical italic rho)
    '\U0001D70E': r'\sigma',  # 𝜎 (mathematical italic sigma)
    '\U0001D70F': r'\tau',    # 𝜏 (mathematical italic tau)
    '\U0001D710': r'\upsilon', # 𝜐 (mathematical italic upsilon)
    '\U0001D711': r'\phi',    # 𝜑 (mathematical italic phi)
    '\U0001D712': r'\chi',    # 𝜒 (mathematical italic chi)
    '\U0001D713': r'\psi',    # 𝜓 (mathematical italic psi)
    '\U0001D714': r'\omega',  # 𝜔 (mathematical italic omega)
    # Mathematical script (from Mathematical Alphanumeric Symbols block)
    '\U0001D49F': r'\mathcal{D}',  # 𝒟 (script D)
    '\U0001D4B6': r'\mathcal{a}',  # 𝒶 (script a)
    # Modifier letters used as superscripts
    '\u1D9C': r'^{c}',  # ᶜ (modifier letter small c)
}

# === SUBSCRIPT CHARACTERS ===
# Map Unicode subscript to the plain character it represents
SUBSCRIPTS = {
    # Digits
    '\u2080': '0', '\u2081': '1', '\u2082': '2', '\u2083': '3', '\u2084': '4',
    '\u2085': '5', '\u2086': '6', '\u2087': '7', '\u2088': '8', '\u2089': '9',
    # Letters
    '\u2090': 'a', '\u2091': 'e', '\u2092': 'o', '\u2093': 'x',
    '\u2095': 'h', '\u2096': 'k', '\u2097': 'l', '\u2098': 'm',
    '\u2099': 'n', '\u209a': 'p', '\u209b': 's', '\u209c': 't',
    # Additional from other blocks
    '\u1d62': 'i', '\u1d63': 'r', '\u1d64': 'u', '\u1d65': 'v',
    '\u2c7c': 'j',
    # Symbols
    '\u208a': '+', '\u208b': '-', '\u208c': '=', '\u208d': '(', '\u208e': ')',
}

# === SUPERSCRIPT CHARACTERS ===
# Map Unicode superscript to the plain character it represents
SUPERSCRIPTS = {
    # Digits
    '\u2070': '0', '\u00b9': '1', '\u00b2': '2', '\u00b3': '3', '\u2074': '4',
    '\u2075': '5', '\u2076': '6', '\u2077': '7', '\u2078': '8', '\u2079': '9',
    # Symbols
    '\u207a': '+', '\u207b': '-', '\u207c': '=', '\u207d': '(', '\u207e': ')',
    '\u207f': 'n', '\u2071': 'i',
    # Letters (limited set available in Unicode)
}

# Square root pattern: √ followed by a number or simple expression
# √5 -> \sqrt{5}
# Complex expressions like √(ħG/c³) need special handling
SQRT_PATTERN = re.compile(r'√(\d+|[a-zA-Z])')

# Bra-ket notation patterns
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
    wrapping each converted run in $...$ so LaTeX renders it as math.
    
    KEY: Consecutive subscripts/superscripts are GROUPED into a single block.
    E.g., "10⁻¹²⁰" becomes "$10^{-120}$", not "$10^{-}^{1}^{2}^{0}$".
    
    ALSO: Adjacent digits/letters next to math symbols are included in the same
    math span. E.g., "∞↔2" becomes "$\infty \leftrightarrow 2$".
    """
    out = []
    buf = []
    
    # Character categories
    subscript_chars = set(SUBSCRIPTS)
    superscript_chars = set(SUPERSCRIPTS)
    greek_chars = set(GREEK)
    symbol_chars = set(SYMBOLS)
    
    all_convertible = subscript_chars | superscript_chars | greek_chars | symbol_chars
    
    # Characters that should be pulled into math mode if adjacent to math
    # Note: Do NOT include {} or () as they have special meaning in markdown/LaTeX
    math_adjacent = set('0123456789')

    i = 0
    n = len(segment)
    
    while i < n:
        # Try sqrt pattern first (√5 -> \sqrt{5})
        sqrt_match = SQRT_PATTERN.match(segment, i)
        if sqrt_match:
            if buf:
                out.append(''.join(buf))
                buf = []
            out.append(r'$\sqrt{' + sqrt_match.group(1) + '}$')
            i = sqrt_match.end()
            continue
        
        # Handle bare √ without argument (rare, but handle gracefully)
        if i < n and segment[i] == '√':
            if buf:
                out.append(''.join(buf))
                buf = []
            out.append(r'$\sqrt{}$')
            i += 1
            continue
        
        # Try bra-ket multi-char patterns
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
        
        if ch in all_convertible:
            # Start a math run - also include adjacent digits/letters
            math_parts = []
            
            while i < n and (segment[i] in all_convertible or segment[i] in math_adjacent):
                c = segment[i]
                
                if c in subscript_chars:
                    # Collect consecutive subscripts into one _{...}
                    sub_content = []
                    while i < n and segment[i] in subscript_chars:
                        sub_content.append(SUBSCRIPTS[segment[i]])
                        i += 1
                    math_parts.append('_{' + ''.join(sub_content) + '}')
                    
                elif c in superscript_chars:
                    # Collect consecutive superscripts into one ^{...}
                    sup_content = []
                    while i < n and segment[i] in superscript_chars:
                        sup_content.append(SUPERSCRIPTS[segment[i]])
                        i += 1
                    math_parts.append('^{' + ''.join(sup_content) + '}')
                    
                elif c in greek_chars:
                    math_parts.append(GREEK[c])
                    i += 1
                    
                elif c in symbol_chars:
                    math_parts.append(SYMBOLS[c])
                    i += 1
                    
                elif c in math_adjacent:
                    # Include adjacent alphanumeric characters in math mode
                    math_parts.append(c)
                    i += 1
                    
                else:
                    i += 1
            
            # Flush any pending text buffer
            if buf:
                out.append(''.join(buf))
                buf = []
            
            # Output the math run
            if math_parts:
                out.append('$' + ''.join(math_parts) + '$')
        else:
            buf.append(ch)
            i += 1
    
    if buf:
        out.append(''.join(buf))
    
    return ''.join(out)


def strip_keywords_field(frontmatter):
    """Remove a top-level `keywords:` YAML key and any indented continuation lines."""
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
    
    # Post-processing: fix subscript/superscript patterns that need braces
    # _\mathbb{X} -> _{\mathbb{X}}
    # ^\mathbb{X} -> ^{\mathbb{X}}
    result = re.sub(r'_\\(mathbb|mathcal|mathfrak)\{([^}]+)\}', r'_{\\\1{\2}}', result)
    result = re.sub(r'\^\\(mathbb|mathcal|mathfrak)\{([^}]+)\}', r'^{\\\1{\2}}', result)
    
    # Also fix patterns like $X$_$Y$ -> $X_Y$ (merge adjacent math spans)
    result = re.sub(r'\$([^$]+)\$_\$([^$]+)\$', r'$\1_{\2}$', result)
    result = re.sub(r'\$([^$]+)\$\^\$([^$]+)\$', r'$\1^{\2}$', result)
    
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
