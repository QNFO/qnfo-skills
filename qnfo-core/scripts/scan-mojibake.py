#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan-mojibake.py — HARD GATE for UTF-8 double-encoding detection + repair (qnfo-core v1.2).

Scans text files for known mojibake patterns (UTF-8 bytes interpreted as
CP1252 and re-encoded as UTF-8). These are ALWAYS corruption signals that
must be fixed before the text enters any durable storage.

Usage:
    python scan-mojibake.py <file>            # scan only (exit 1 if found)
    python scan-mojibake.py <file> --fix      # scan + auto-repair
    python scan-mojibake.py <file> --json     # JSON output

Exit: 0=PASS, 1=FAIL(unfixed), 2=FAIL(fixed with --fix)
Gate: qnfo-core v1.2 §0.2 UTF-8 Source Encoding Mandate
"""

import sys, os

CP1252_TO_BYTE = {
    0x20AC: 0x80, 0x201A: 0x82, 0x0192: 0x83, 0x201E: 0x84,
    0x2026: 0x85, 0x2020: 0x86, 0x2021: 0x87, 0x02C6: 0x88,
    0x2030: 0x89, 0x0160: 0x8A, 0x2039: 0x8B, 0x0152: 0x8C,
    0x017D: 0x8E, 0x2018: 0x91, 0x2019: 0x92, 0x201C: 0x93,
    0x201D: 0x94, 0x2022: 0x95, 0x2013: 0x96, 0x2014: 0x97,
    0x02DC: 0x98, 0x2122: 0x99, 0x0161: 0x9A, 0x203A: 0x9B,
    0x0153: 0x9C, 0x017E: 0x9E, 0x0178: 0x9F,
}

MOJIBAKE_DISPLAY = {
    '\u00e2\u20ac\u201c': 'a\u20ac\u201c (em/en-dash)',
    '\u00e2\u20ac\u2122': 'a\u20ac\u2122 (right single quote)',
    '\u00e2\u20ac\u0153': 'a\u20ac\u0153 (left double quote)',
    '\u00e2\u20ac\u02dc': 'a\u20ac\u02dc (left single quote)',
    '\u00e2\u20ac\u00a2': 'a\u20ac\u00a2 (bullet)',
    '\u00e2\u20ac\u00a6': 'a\u20ac\u00a6 (ellipsis)',
    '\u00e2\u201e\u00a2': 'a\u201e\u00a2 (trademark)',
}


def char_to_cp1252_byte(ch):
    cp = ord(ch)
    if cp < 0x80: return cp
    if cp in CP1252_TO_BYTE: return CP1252_TO_BYTE[cp]
    if 0x80 <= cp <= 0xFF: return cp
    return None


def fix_mojibake(text):
    """Safe fix: only convert CP1252 chars forming valid UTF-8 multi-byte sequences."""
    if not text: return text
    pairs = [(ch, char_to_cp1252_byte(ch)) for ch in text]
    has_fixable = any(bv is not None and 0xC2 <= bv <= 0xF4 for _, bv in pairs)
    if not has_fixable: return text

    result, i = [], 0
    while i < len(pairs):
        ch, bv = pairs[i]
        if bv is None or bv < 0x80: result.append(ch); i += 1; continue
        if 0xC2 <= bv <= 0xDF and i + 1 < len(pairs):
            _, nb = pairs[i + 1]
            if nb is not None and 0x80 <= nb <= 0xBF:
                try: result.append(bytes([bv, nb]).decode('utf-8')); i += 2; continue
                except: pass
            result.append(ch); i += 1; continue
        if 0xE0 <= bv <= 0xEF and i + 2 < len(pairs):
            _, b1 = pairs[i + 1]; _, b2 = pairs[i + 2]
            if b1 is not None and b2 is not None and 0x80 <= b1 <= 0xBF and 0x80 <= b2 <= 0xBF:
                try: result.append(bytes([bv, b1, b2]).decode('utf-8')); i += 3; continue
                except: pass
            result.append(ch); i += 1; continue
        if 0xF0 <= bv <= 0xF4 and i + 3 < len(pairs):
            _, b1 = pairs[i + 1]; _, b2 = pairs[i + 2]; _, b3 = pairs[i + 3]
            if b1 is not None and b2 is not None and b3 is not None and 0x80 <= b1 <= 0xBF and 0x80 <= b2 <= 0xBF and 0x80 <= b3 <= 0xBF:
                try: result.append(bytes([bv, b1, b2, b3]).decode('utf-8')); i += 4; continue
                except: pass
            result.append(ch); i += 1; continue
        result.append(ch); i += 1
    return ''.join(result)


def scan_file(filepath):
    """Scan a file for actual mojibake patterns (multi-byte sequences only).
    Does NOT flag standalone CP1252 characters like properly typed em-dashes."""
    findings = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    
    lines = text.split('\n')
    for num, line in enumerate(lines, 1):
        if '\ufffd' in line:
            findings.append((num, line.strip()[:60], 'U+FFFD REPLACEMENT'))
            continue
        
        # Only flag lines where fixMojibake() would actually change the text
        fixed_line = fix_mojibake(line)
        if fixed_line != line:
            # Find where the first fix occurred
            for idx in range(min(len(line), len(fixed_line))):
                if line[idx] != fixed_line[idx]:
                    ctx = line[max(0,idx-15):min(len(line),idx+30)].strip()
                    findings.append((num, ctx[:60], f'U+{ord(line[idx]):04X} mojibake'))
                    break
    
    return findings


def main():
    do_fix = '--fix' in sys.argv
    json_out = '--json' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print("Usage: scan-mojibake.py <file> [--fix] [--json]", file=sys.stderr)
        sys.exit(1)

    fp = args[0]
    findings = scan_file(fp)

    if json_out:
        import json
        print(json.dumps({'file': fp, 'findings': len(findings),
            'details': [{'line': l, 'context': c, 'pattern': p} for l, c, p in findings],
            'fixed': False}, indent=2))

    if not findings:
        print(f"Mojibake: PASS [{os.path.basename(fp)}]")
        sys.exit(0)

    print(f"Mojibake: FAIL — {len(findings)} pattern(s) in {os.path.basename(fp)}")
    for l, c, p in findings[:10]: print(f"  L{l}: ...{c}... [{p}]")

    if do_fix:
        print("→ fixing...")
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            orig = f.read()
        fixed = fix_mojibake(orig)
        if fixed != orig:
            with open(fp, 'w', encoding='utf-8') as f: f.write(fixed)
            print(f"  FIXED: {len(orig)} -> {len(fixed)} chars")
            sys.exit(2)
        print("  No changes needed")
        sys.exit(0)
    else:
        print("  Run with --fix to auto-repair")
        sys.exit(1)


if __name__ == '__main__': main()
