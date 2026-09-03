# CMD SKILLS UPDATE — 2026-09-03 (system-prompt v4.07 / kaizen v2.130 / cloudflare v3.75 / research v2.150 / qnfo-core v1.44)

RED TEAM SKILLS AUDIT (2026-09-03, same-turn evidence):
- Versions: kaizen v2.129, cloudflare v3.74, research v2.149, qnfo-core v1.43 banners verified current (mirror system-prompt v4.06).
- HARD finding: this session's gates are ABSENT from all four key skills + the system prompt:
  MATH-LATEX-1, GITHUB-PDF-ENGINE-1, GIT-CONTINUOUS-1 -> grep 0 in kaizen/research/cloudflare/qnfo-core.
  WEBSITE-SYNC-COLUMNS-1 -> present in research/cloudflare/qnfo-core (needs kaizen mirror row).
- Verdict: FAIL on gate coverage; remediation = this update block (v4.07) dual-written to system prompt + CMD templates + skill banners.

## Canonical v4.07 MANDATORY block (insert at the top of the system-prompt mandate chain + kaizen mirror rows + CMD templates):
MANDATORY (2026-09-03, system-prompt v4.07 / kaizen v2.130 / research v2.150 / cloudflare v3.75 / qnfo-core v1.44):
preserve the cloud-native-LaTeX + GitHub-continuity + pipeline-hardening gates —
MATH-LATEX-1 (ALL math in PDFs/papers/artifacts/prose renders as real LaTeX math: single $...$ spans per expression; ASCII shorthand like N_g(21) x3 BANNED; converter v3 rules: paren-aware superscripts, placeholder-protected \textbf/\href/\url, explicit \times for x, adjacent-math merge; gate = zero control bytes + balanced $ + zero plain sub/superscript outside math + no \textbf\\{),
GITHUB-PDF-ENGINE-1 (Workers cannot run pdflatex/tectonic; arXiv-grade PDFs render in the cloud via (a) TeXLive.net latexcgi: POST multipart engine=pdflatex return=pdf filename[]=document.tex filecontents[]= -> %PDF-1.7, and (b) GitHub Actions workflow latex-pdf on QNFO/qnfo-research branch res/paper/v2-latex-pdf: tectonic -> commit PDFs + gh release pdf-<slug>; release glob must be papers/**/*.pdf (two-level layout); drop-installer unpacks tectonic to CWD -> sudo mv to /usr/local/bin),
GIT-CONTINUOUS-1 (every research/publish cycle commits + pushes md/tex/provenance/PDF to the GitHub repo BEFORE/with publish; verify with git ls-remote; the Zenodo isSupplementTo related_identifier points at real current repo content),
WEBSITE-SYNC-COLUMNS-1 verified 2026-09-03 (papers.qnfo.org/papers/a-lower-bound... shows DOI 10.5281/zenodo.22283869, ZERO old DOIs, ZERO N_g(21); doi AND zenodo_doi + body_md swapped at publish),
BLAME-EXTERNAL-1 CORRECTION CASE (2026-09-03: GitHub Actions annotation 'account locked due to billing issue' was TRANSIENT/WRONG - repo QNFO/qnfo-research is PUBLIC, org+repo Actions enabled all, plan free; ALWAYS verify settings/visibility via gh api before external attribution),
ZENODO-NETWORK-403-1 (zenodo.org/api 403 'unusual traffic' from the local network AND web_fetch; worker-side events + D1 + papers.qnfo.org are the verification channel when the API is blocked; retry API later),
WORKER-API-CONTENT-V2-CACHE-1 (content/v2 reads are STALE-CACHED after a PUT - always read with ?cb=Date.now() or verify via the versions/deployment API; a '0.5.2 unchanged' read after a successful PUT was a cache artifact),
ZENODO-NEWVERSION-STRAY-PURGE-1 EXTENSION (purge a stale newversion draft by deleting its FILES first (links.self DELETE), THEN DELETE the deposition; file-first ordering is mandatory - DELETE on a draft with files 400s files.enabled 'Please remove all files first'),
TEXLIVE-NET-ENDPOINT-1 (https://texlive.net/cgi-bin/latexcgi - HTTP POST multipart only; fields engine/return/filename[]/filecontents[]; redirects followed; returns the PDF or a text log; latexonline.cc is GET-only ~8KB URI cap - unusable for full papers);
pipeline state: research-exec v0.5.5 (v3 converter + TeXLive.net compile + file-first purge fix) armed */10; version_queue rows 4,5,6,8 PUBLISHED (22283716/22283727/22283869/22283879); row 7 (NV.002 -> 2.0.1) armed;
verify 7 stores byte-identical + header==footer==title + 11/11 CMD templates (id+content+template) + prompt-store-verify.py exit 0 + DEEPCHAT-DEFAULT-MODEL-1 (both JSON model keys flash) after every dual-write (PROMPT-PARITY-1).

## Skill banner bumps to apply (canonical text):
- kaizen v2.130: "> **v2.130 UPDATE (2026-09-03, CMD SKILLS UPDATE: MATH-LATEX-1 + GITHUB-PDF-ENGINE-1 + GIT-CONTINUOUS-1 + WEBSITE-SYNC verified + BLAME-EXTERNAL-1 GitHub-billing correction + WORKER-API-CONTENT-V2-CACHE-1 + ZENODO-NEWVERSION file-first purge + TEXLIVE-NET-ENDPOINT-1; mirrors system-prompt v4.07; preserves v2.129):**"
- cloudflare v3.75: same gate list (mirrors system-prompt v4.07 + kaizen v2.130; preserves v3.74).
- qnfo-core v1.44: same (preserves v1.43).
- research v2.150: same (preserves v2.149).

## Store dual-write checklist (system prompt + CMD templates, 7-store parity):
1. Insert v4.07 block after the v4.06 header block; bump Version footer to v4.07.
2. Mirror rows into kaizen SKILL.md + cloudflare + research + qnfo-core banners.
3. Write canonical to: .deepchat/system-prompt-v2.7.md, qnfo-skills repo copy, .deepchat/skills live, Roaming app-settings.json default_system_prompt, .deepchat/app-settings.json legacy, app_db agent.db systemPrompts, legacy agent.db.
4. 11/11 CMD templates (id+content+template) in the template stores from repo canonical prompt-stores/customPrompts.json.
5. Run prompt-store-verify.py (exit 0) + DEEPCHAT-DEFAULT-MODEL-1 (both keys deepseek-v4-flash).
