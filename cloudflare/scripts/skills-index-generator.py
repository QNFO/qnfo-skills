#!/usr/bin/env python3
"""skills-index-generator.py — RFC 0.2.0-compliant Agent Skills Discovery index generator.

Implements https://github.com/cloudflare/agent-skills-discovery-rfc (forked at
QNFO/agent-skills-discovery-rfc). Scans a skills root directory for skill dirs
containing SKILL.md, parses YAML frontmatter (name, description), computes
SHA-256 digests, and emits /.well-known/agent-skills/index.json per the v0.2.0
schema.

Usage:
  python skills-index-generator.py --root <skills-root> [--out index.json]
                                    [--base-url https://example.com]
                                    [--json] [--verify]

Examples:
  python skills-index-generator.py --root C:\\Users\\LENOVO\\.deepchat\\skills \\
      --base-url https://qnfo.org --out index.json --verify
"""
import argparse
import hashlib
import json
import os
import re
import sys

SCHEMA_URI = "https://schemas.agentskills.io/discovery/0.2.0/schema.json"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
NAME_RE = re.compile(r'^name\s*:\s*["\']?([^"\'\n]+)["\']?', re.MULTILINE)
DESC_RE = re.compile(r'^description\s*:\s*["\']?(.*?)["\']?\s*$', re.MULTILINE)


def parse_frontmatter(text: str):
    """Minimal YAML frontmatter extractor (name + description only)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm = m.group(1)
    name = NAME_RE.search(fm)
    desc = DESC_RE.search(fm)
    return {
        "name": name.group(1).strip() if name else None,
        "description": desc.group(1).strip() if desc else None,
    }


def sha256_bytes(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def is_valid_skill_name(name: str) -> bool:
    """Agent Skills spec: 1-64 chars, lowercase alnum + hyphens, no edge/consecutive hyphens."""
    if not name or not (1 <= len(name) <= 64):
        return False
    if not re.fullmatch(r"[a-z0-9-]+", name):
        return False
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False
    return True


def generate_index(root: str, base_url: str = "") -> dict:
    skills = []
    if not os.path.isdir(root):
        return {"$schema": SCHEMA_URI, "skills": []}

    for entry in sorted(os.listdir(root)):
        skill_dir = os.path.join(root, entry)
        if not os.path.isdir(skill_dir):
            continue
        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        with open(skill_md, "rb") as f:
            raw = f.read()
        fm = parse_frontmatter(raw.decode("utf-8", errors="replace"))
        if not fm or not fm["name"] or not fm["description"]:
            print(f"  [WARN] {entry}: missing name/description frontmatter, skipped")
            continue
        if not is_valid_skill_name(fm["name"]):
            print(f"  [WARN] {entry}: invalid skill name '{fm['name']}', skipped")
            continue
        url = f"{base_url}/.well-known/agent-skills/{entry}/SKILL.md" if base_url else f"/.well-known/agent-skills/{entry}/SKILL.md"
        skills.append(
            {
                "name": fm["name"],
                "type": "skill-md",
                "description": fm["description"],
                "url": url,
                "digest": sha256_bytes(raw),
            }
        )

    skills.sort(key=lambda s: s["name"])
    return {"$schema": SCHEMA_URI, "skills": skills}


def verify_digests(root: str, index: dict) -> bool:
    ok = True
    for s in index.get("skills", []):
        # url pattern: {base}/.well-known/agent-skills/{name}/SKILL.md
        name = s["name"]
        skill_md = os.path.join(root, name, "SKILL.md")
        if not os.path.isfile(skill_md):
            print(f"  [FAIL] {name}: artifact not found at {skill_md}")
            ok = False
            continue
        with open(skill_md, "rb") as f:
            actual = sha256_bytes(f.read())
        if actual != s["digest"]:
            print(f"  [FAIL] {name}: digest mismatch {s['digest']} != {actual}")
            ok = False
        else:
            print(f"  [OK]   {name}: {actual[:20]}...")
    return ok


def main():
    ap = argparse.ArgumentParser(description="Generate Agent Skills Discovery index (RFC 0.2.0)")
    ap.add_argument("--root", required=True, help="Skills root directory")
    ap.add_argument("--out", default=None, help="Output JSON path (default: print to stdout)")
    ap.add_argument("--base-url", default="", help="Base URL prefix for absolute artifact URLs")
    ap.add_argument("--verify", action="store_true", help="Verify digests against generated index")
    args = ap.parse_args()

    print(f"Scanning {args.root} ...")
    index = generate_index(args.root, args.base_url)
    print(f"  {len(index['skills'])} skills indexed")

    if args.verify:
        print("Verifying digests ...")
        if not verify_digests(args.root, index):
            sys.exit(1)

    out = json.dumps(index, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Wrote {args.out}")
    else:
        print(out)


if __name__ == "__main__":
    main()
