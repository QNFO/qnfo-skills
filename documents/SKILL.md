---
name: documents
description: Create, edit, and analyze all document formats -- Word (.docx) with formatting and tracked changes, PowerPoint (.pptx) presentations from outlines, Excel (.xlsx/.csv/.tsv) spreadsheets with formulas and analysis, and PDF manipulation (form filling, merge, split, text/table extraction). For publication-grade LaTeX PDF builds, use the research skill.
version: "2.5"
triggers: ["docx", "Word", "document", "PowerPoint", "presentation", "slides", "Excel", "spreadsheet", "CSV", "TSV", "xlsx", "pptx", "PDF", "form", "fill form", "merge PDF", "split PDF", "extract PDF", "table extraction", "tracked changes", "comments", "speaker notes", "formula", "chart", "pivot table", "data analysis", "import", "export", "office", "formatting", "styles", "headers", "footers"]
related: ["research"]
priority: 2
platform: local
autonomous: false
self_sufficient: true
---

> **v0.1 UPDATE (2026-08-03, kaizen — skill merge):**
> Merged `doc-coauthoring` skill (376 lines) into this skill.
> Red-team: direct parent-agent ecosystem audit. HARD: 0. SOFT: 0. DESIGN: 1.
> Content appended as ## Document Co-Authoring Workflow (merged from doc-coauthoring skill, 2026-08-03).
> **v2.4 UPDATE (2026-08-02, kaizen — Cloudflare tool discoverability):**
> Ephemeral-memory mandate: memories are NOT permanent. This skill archives to
> R2 (r2-archive.js) — instructions MUST name the actual agent tools. R2 archive
> verification: `workers_list` (confirm R2 bucket exists via account state) or
> `search_cloudflare_documentation` for R2 API; see cloudflare skill
> §Skill Cross-Reference v3.18. NEVER rely on durable memory for Cloudflare
> operational state.
> Cross-reference: cloudflare v3.18.


# DOCUMENTS — v2.5 (Office + PDF + 4-D Export)

> **v2.3 UPDATE (2026-07-25, professional-standard kaizen):** Added the
> **Professional Publication Standards (Cross-Skill Mandate)** section
> below, cross-referencing `research/SKILL.md`'s new journal-grade
> structure/tone/prose/copyediting bar — every .docx/.pptx/.xlsx/.pdf
> deliverable must meet the same professional-quality gate as LaTeX
> research papers, not a lower bar just because the format differs.

> **v2.2 UPDATE (2026-07-21, phantom-claim audit):** Added the
> **Tool-Call Execution Mandate** section below. A document is not
> "created"/"updated"/"filled" until it has been read back and its content
> verified in this turn — the write-tool's return value alone is not proof
> the file is correct.

> **Merges 2:** office-documents + pdf-documents
> **Related:** Load `research` for publication-grade PDFs + 4-D distribution. Load `cloudflare` for R2/IPFS archival.
> **Cloudflare Full-Stack:** Generated documents are ephemeral on local disk. Canonical storage is R2 with 4-D distribution. Published papers use the research pipeline.
> **4-D Mandate:** Every finalized document must be stored in ≥4 locations across ≥2 protocols.

## execute_plan

update_plan([
  {"step": "Identify document type: .docx, .pptx, .xlsx, .csv, or .pdf", "status": "pending"},
  {"step": "Read source data and create/edit document with appropriate tooling", "status": "pending"},
  {"step": "Verify: Test-Path output.ext AND (Get-Item output.ext).Length > 0", "status": "pending"},
])

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — MANDATORY)

Claiming a document was "created", "updated", "filled", or "extracted"
without an invoked tool call showing evidence in this turn is a PHANTOM
CLAIM (`qnfo-core` §9.11 Rule 14) — BLOCKED.

1. **Every creation/edit** — after writing, `Test-Path` (or `read`) the output file AND re-open/re-parse it (extract text or read cell values back) to confirm content matches intent. A successful write-tool return code is NOT proof the document is correct.
2. **.xlsx formula edits** — re-read the saved file and confirm formulas are still formulas (not baked-in values) before claiming "formulas preserved".
3. **PDF form fills** — re-extract the filled field values from the saved PDF and show them; do not claim "form filled" from the fill-call's return alone.
4. **.pptx/.docx from outline** — re-open the generated file and report the actual slide/paragraph count achieved vs the outline requested.
5. If the output cannot be re-verified in this turn, say `[NOT-VERIFIED: reason]` instead of "done"/"created"/"filled".

---

## Word Documents (.docx)

### Creation
- Create from markdown, structured data, or programmatic content
- Apply styles: Heading 1-3, Normal, List Bullet, List Number, Block Text
- Insert tables with header rows, alternating row shading
- Embed images with captions and alt text
- Set page margins (1 inch default), orientation (portrait/landscape)
- Add headers and footers (page numbers, document title, date)

### Editing
- Modify existing content while preserving formatting
- Apply style changes to selected paragraphs
- Replace text with formatting preservation
- Insert/delete paragraphs, tables, images

### Track Changes & Comments
- Enable tracked changes for review workflows
- Accept/reject individual changes or all changes
- Add comments to specific text ranges
- Read existing comments with author and timestamp
- Resolve/delete comments

### Text Extraction
- Extract plain text preserving paragraph structure
- Extract structured content (tables as arrays, images as metadata)
- Handle headers, footers, footnotes, endnotes

### Formatting Checklist
- [ ] Fonts consistent (headings + body)
- [ ] Heading hierarchy correct (H1 > H2 > H3)
- [ ] Table widths fit page margins
- [ ] Images have captions and are inline with text
- [ ] Page numbers in footer
- [ ] Spell check completed
- [ ] File size reasonable (<10MB for documents without images)

---

## PowerPoint Presentations (.pptx)

### Creation from Outline
```markdown
# Slide 1: Title
## Slide 2: Problem Statement
- Bullet 1
- Bullet 2
## Slide 3: Methodology
1. Step one
2. Step two
## Slide 4: Results
| Metric | Value |
|:-------|:------|
| Total | 42 |
```

Each `##` becomes a new slide. Lists become bullet points. Tables become formatted tables.

### Slide Operations
- Add/remove/reorder slides
- Change slide layout (Title, Title+Content, Two Content, Blank)
- Set background color or image
- Apply slide transitions

### Content Elements
- **Text:** Titles, body text, bullet lists, numbered lists
- **Tables:** Row/column counts, header formatting, alternating colors
- **Images:** Embedded with position and sizing
- **Charts:** Bar, line, pie, scatter (linked or embedded data)

### Speaker Notes
- Add per-slide speaker notes
- Read existing speaker notes
- Format notes with line breaks and emphasis

### Verification
- [ ] Slide count matches outline
- [ ] All slides have content (no empty slides)
- [ ] Reading order logical (title -> problem -> method -> results -> conclusion)
- [ ] Speaker notes present if presentation is for delivery
- [ ] File opens without errors in PowerPoint

---

## Excel Spreadsheets (.xlsx, .csv, .tsv)

### Creation
- Create workbooks with multiple named sheets
- Populate cells with values, formulas, and formatting
- Set column widths, row heights
- Apply number formatting (currency, percent, date, scientific)
- Conditional formatting (color scales, data bars, icon sets)

### Formulas
- Basic: SUM, AVERAGE, COUNT, MIN, MAX, IF
- Lookup: VLOOKUP, INDEX/MATCH, XLOOKUP
- Date: TODAY, DATE, DATEDIF
- Text: CONCAT, LEFT, RIGHT, MID
- Logic: IF, AND, OR, NOT
- Statistical: STDEV, CORREL, LINEST

**CRITICAL:** When editing .xlsx, use formula-preserving paths. NEVER read formulas as values and write them back -- the formulas are LOST.

### Data Analysis
- Pivot tables: row/column fields, value fields, aggregation (sum/count/average)
- Charts: bar, line, pie, scatter
- Filtering and sorting
- Statistical analysis (descriptive statistics, regression)

### CSV/TSV
- Import: auto-detect delimiter and data types
- Export: specify delimiter, quoting, encoding (UTF-8 with BOM for Excel compatibility)
- Handle: quoted fields, multi-line fields, null values

### Verification
- [ ] File opens without corruption warning
- [ ] Formulas recalculate correctly (press F9)
- [ ] Charts render with correct data
- [ ] Pivot tables refresh properly
- [ ] CSV encoding is UTF-8 (with BOM if Excel-bound)
- [ ] All sheets named and organized

---

## PDF Manipulation

### Operations
| Operation | Description | Tool Pattern |
|:----------|:------------|:-------------|
| **Fill Form** | Populate PDF form fields programmatically | Read field structure -> set values -> save |
| **Merge** | Combine multiple PDFs into one document | Concatenate pages preserving order |
| **Split** | Extract specific pages or page ranges | Copy pages 1-5, 10-15 to new PDF |
| **Extract Text** | Get plain text from all pages | Iterate pages -> get_text() |
| **Extract Tables** | Extract tabular data with structure | Parse table regions -> return as list of lists |
| **Create** | Generate new PDF from scratch | Add pages -> draw text/images -> save |

### Limitations
- **NOT for publication-grade builds.** Use `research` skill's canonical CDP pipeline (pandoc `--mathjax` → MathJax SVG inline → puppeteer-core `page.pdf()`).
- Scanned PDFs need OCR for text extraction (not included -- handle as images).
- Complex formatting (multi-column, floating elements) may not extract perfectly.
- Encrypted/DRM PDFs cannot be processed.

### Verification
- [ ] `Test-Path output.pdf` -> file exists
- [ ] `(Get-Item output.pdf).Length -gt 500` -> non-trivial size (>500 bytes)
- [ ] Page count matches expected
- [ ] Text extraction produces readable content
- [ ] Form fields populated correctly (verify visually)

---

## Professional Publication Standards (Cross-Skill Mandate, 2026-07-25)

Every deliverable produced by this skill -- .docx, .pptx, .xlsx, or .pdf --
that will be shared externally or delivered as a finished artifact MUST
meet the same professional content, tone, structure, and copyediting bar
defined in `research/SKILL.md` § "Professional Publication Standards":
formal tone (no contractions, no first-person-singular in body content,
no AI-generated-sounding filler like "It is important to note that"),
zero spelling/grammar errors, consistent terminology and formatting
throughout, complete section/slide structure with no orphaned headings,
and a final self-review pass reading the deliverable as a critical
external reviewer would. This applies regardless of format -- a .docx
report or .pptx deck held to a lower bar than a LaTeX paper is still a
Publication Language / Professional Standards Gate failure. For
publication-grade research PDFs specifically (LaTeX-native journal
papers), use the `research` skill's Springer Nature LaTeX Template
(`sn-jnl.cls`) at `research/templates/springer-nature-latex/` rather than
generating a PDF directly from this skill.

## Anti-Patterns
| Anti-Pattern | Fix |
|:-------------|:----|
| Creating documents without verification | Always Test-Path + check content |
| Losing formulas during .xlsx edits | Use formula-preserving edit paths |
| Wrong file extension | Match: .docx/.pptx/.xlsx/.csv/.pdf |
| Using this skill for publication PDFs | Use `research` skill's canonical CDP pipeline (pandoc → MathJax SVG → puppeteer-core `page.pdf()`) |
| Cross-skill document confusion | Documents -> R2 archive -> Papers (via research pipeline) |
| Delivering a .docx/.pptx/.xlsx with informal tone, contractions, or AI-generated-sounding filler phrasing | Apply the same Professional Publication Standards bar as research papers (see above) -- format does not exempt content from the professional-quality gate |
\n\n## R2 Archival Script\n`js\n// _r2_archive.js — Archive any document to R2 for durable storage\nconst TOKEN = process.env.CLOUDFLARE_API_TOKEN;\nconst ACCOUNT = '...';\nconst BUCKET = 'qnfo';\nconst KEY = 'documents/filename.ext';\nconst content = '...'; // file content\n\nawait fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/r2/buckets/' + BUCKET + '/objects/' + encodeURIComponent(KEY), {\n  method: 'PUT',\n  headers: { 'Authorization': 'Bearer ' + TOKEN },\n  body: content\n});\n// Verify: GET same URL returns 200 with content\n// Alt: npx wrangler r2 object put qnfo/{KEY} --file {path} --remote\n`

---

## Document Co-Authoring Workflow (merged from doc-coauthoring skill, 2026-08-03)

# Doc Co-Authoring Workflow

This skill provides a structured workflow for guiding users through collaborative document creation. Act as an active guide, walking users through three stages: Context Gathering, Refinement & Structure, and Reader Testing.

## When to Offer This Workflow

**Trigger conditions:**
- User mentions writing documentation: "write a doc", "draft a proposal", "create a spec", "write up"
- User mentions specific doc types: "PRD", "design doc", "decision doc", "RFC"
- User seems to be starting a substantial writing task

**Initial offer:**
Offer the user a structured workflow for co-authoring the document. Explain the three stages:

1. **Context Gathering**: User provides all relevant context while Claude asks clarifying questions
2. **Refinement & Structure**: Iteratively build each section through brainstorming and editing
3. **Reader Testing**: Test the doc with a fresh Claude (no context) to catch blind spots before others read it

Explain that this approach helps ensure the doc works well when others read it (including when they paste it into Claude). Ask if they want to try this workflow or prefer to work freeform.

If user declines, work freeform. If user accepts, proceed to Stage 1.

## Stage 1: Context Gathering

**Goal:** Close the gap between what the user knows and what Claude knows, enabling smart guidance later.

### Initial Questions

Start by asking the user for meta-context about the document:

1. What type of document is this? (e.g., technical spec, decision doc, proposal)
2. Who's the primary audience?
3. What's the desired impact when someone reads this?
4. Is there a template or specific format to follow?
5. Any other constraints or context to know?

Inform them they can answer in shorthand or dump information however works best for them.

**If user provides a template or mentions a doc type:**
- Ask if they have a template document to share
- If they provide a link to a shared document, use the appropriate integration to fetch it
- If they provide a file, read it

**If user mentions editing an existing shared document:**
- Use the appropriate integration to read the current state
- Check for images without alt-text
- If images exist without alt-text, explain that when others use Claude to understand the doc, Claude won't be able to see them. Ask if they want alt-text generated. If so, request they paste each image into chat for descriptive alt-text generation.

### Info Dumping

Once initial questions are answered, encourage the user to dump all the context they have. Request information such as:
- Background on the project/problem
- Related team discussions or shared documents
- Why alternative solutions aren't being used
- Organizational context (team dynamics, past incidents, politics)
- Timeline pressures or constraints
- Technical architecture or dependencies
- Stakeholder concerns

Advise them not to worry about organizing it - just get it all out. Offer multiple ways to provide context:
- Info dump stream-of-consciousness
- Point to team channels or threads to read
- Link to shared documents

**If integrations are available** (e.g., Slack, Teams, Google Drive, SharePoint, or other MCP servers), mention that these can be used to pull in context directly.

**If no integrations are detected and in Claude.ai or Claude app:** Suggest they can enable connectors in their Claude settings to allow pulling context from messaging apps and document storage directly.

Inform them clarifying questions will be asked once they've done their initial dump.

**During context gathering:**

- If user mentions team channels or shared documents:
  - If integrations available: Inform them the content will be read now, then use the appropriate integration
  - If integrations not available: Explain lack of access. Suggest they enable connectors in Claude settings, or paste the relevant content directly.

- If user mentions entities/projects that are unknown:
  - Ask if connected tools should be searched to learn more
  - Wait for user confirmation before searching

- As user provides context, track what's being learned and what's still unclear

**Asking clarifying questions:**

When user signals they've done their initial dump (or after substantial context provided), ask clarifying questions to ensure understanding:

Generate 5-10 numbered questions based on gaps in the context.

Inform them they can use shorthand to answer (e.g., "1: yes, 2: see #channel, 3: no because backwards compat"), link to more docs, point to channels to read, or just keep info-dumping. Whatever's most efficient for them.

**Exit condition:**
Sufficient context has been gathered when questions show understanding - when edge cases and trade-offs can be asked about without needing basics explained.

**Transition:**
Ask if there's any more context they want to provide at this stage, or if it's time to move on to drafting the document.

If user wants to add more, let them. When ready, proceed to Stage 2.

## Stage 2: Refinement & Structure

**Goal:** Build the document section by section through brainstorming, curation, and iterative refinement.

**Instructions to user:**
Explain that the document will be built section by section. For each section:
1. Clarifying questions will be asked about what to include
2. 5-20 options will be brainstormed
3. User will indicate what to keep/remove/combine
4. The section will be drafted
5. It will be refined through surgical edits

Start with whichever section has the most unknowns (usually the core decision/proposal), then work through the rest.

**Section ordering:**

If the document structure is clear:
Ask which section they'd like to start with.

Suggest starting with whichever section has the most unknowns. For decision docs, that's usually the core proposal. For specs, it's typically the technical approach. Summary sections are best left for last.

If user doesn't know what sections they need:
Based on the type of document and template, suggest 3-5 sections appropriate for the doc type.

Ask if this structure works, or if they want to adjust it.

**Once structure is agreed:**

Create the initial document structure with placeholder text for all sections.

**If access to artifacts is available:**
Use `create_file` to create an artifact. This gives both Claude and the user a scaffold to work from.

Inform them that the initial structure with placeholders for all sections will be created.

Create artifact with all section headers and brief placeholder text like "[To be written]" or "[Content here]".

Provide the scaffold link and indicate it's time to fill in each section.

**If no access to artifacts:**
Create a markdown file in the working directory. Name it appropriately (e.g., `decision-doc.md`, `technical-spec.md`).

Inform them that the initial structure with placeholders for all sections will be created.

Create file with all section headers and placeholder text.

Confirm the filename has been created and indicate it's time to fill in each section.

**For each section:**

### Step 1: Clarifying Questions

Announce work will begin on the [SECTION NAME] section. Ask 5-10 clarifying questions about what should be included:

Generate 5-10 specific questions based on context and section purpose.

Inform them they can answer in shorthand or just indicate what's important to cover.

### Step 2: Brainstorming

For the [SECTION NAME] section, brainstorm [5-20] things that might be included, depending on the section's complexity. Look for:
- Context shared that might have been forgotten
- Angles or considerations not yet mentioned

Generate 5-20 numbered options based on section complexity. At the end, offer to brainstorm more if they want additional options.

### Step 3: Curation

Ask which points should be kept, removed, or combined. Request brief justifications to help learn priorities for the next sections.

Provide examples:
- "Keep 1,4,7,9"
- "Remove 3 (duplicates 1)"
- "Remove 6 (audience already knows this)"
- "Combine 11 and 12"

**If user gives freeform feedback** (e.g., "looks good" or "I like most of it but...") instead of numbered selections, extract their preferences and proceed. Parse what they want kept/removed/changed and apply it.

### Step 4: Gap Check

Based on what they've selected, ask if there's anything important missing for the [SECTION NAME] section.

### Step 5: Drafting

Use `str_replace` to replace the placeholder text for this section with the actual drafted content.

Announce the [SECTION NAME] section will be drafted now based on what they've selected.

**If using artifacts:**
After drafting, provide a link to the artifact.

Ask them to read through it and indicate what to change. Note that being specific helps learning for the next sections.

**If using a file (no artifacts):**
After drafting, confirm completion.

Inform them the [SECTION NAME] section has been drafted in [filename]. Ask them to read through it and indicate what to change. Note that being specific helps learning for the next sections.

**Key instruction for user (include when drafting the first section):**
Provide a note: Instead of editing the doc directly, ask them to indicate what to change. This helps learning of their style for future sections. For example: "Remove the X bullet - already covered by Y" or "Make the third paragraph more concise".

### Step 6: Iterative Refinement

As user provides feedback:
- Use `str_replace` to make edits (never reprint the whole doc)
- **If using artifacts:** Provide link to artifact after each edit
- **If using files:** Just confirm edits are complete
- If user edits doc directly and asks to read it: mentally note the changes they made and keep them in mind for future sections (this shows their preferences)

**Continue iterating** until user is satisfied with the section.

### Quality Checking

After 3 consecutive iterations with no substantial changes, ask if anything can be removed without losing important information.

When section is done, confirm [SECTION NAME] is complete. Ask if ready to move to the next section.

**Repeat for all sections.**

### Near Completion

As approaching completion (80%+ of sections done), announce intention to re-read the entire document and check for:
- Flow and consistency across sections
- Redundancy or contradictions
- Anything that feels like "slop" or generic filler
- Whether every sentence carries weight

Read entire document and provide feedback.

**When all sections are drafted and refined:**
Announce all sections are drafted. Indicate intention to review the complete document one more time.

Review for overall coherence, flow, completeness.

Provide any final suggestions.

Ask if ready to move to Reader Testing, or if they want to refine anything else.

## Stage 3: Reader Testing

**Goal:** Test the document with a fresh Claude (no context bleed) to verify it works for readers.

**Instructions to user:**
Explain that testing will now occur to see if the document actually works for readers. This catches blind spots - things that make sense to the authors but might confuse others.

### Testing Approach

**If access to sub-agents is available (e.g., in Claude Code):**

Perform the testing directly without user involvement.

### Step 1: Predict Reader Questions

Announce intention to predict what questions readers might ask when trying to discover this document.

Generate 5-10 questions that readers would realistically ask.

### Step 2: Test with Sub-Agent

Announce that these questions will be tested with a fresh Claude instance (no context from this conversation).

For each question, invoke a sub-agent with just the document content and the question.

Summarize what Reader Claude got right/wrong for each question.

### Step 3: Run Additional Checks

Announce additional checks will be performed.

Invoke sub-agent to check for ambiguity, false assumptions, contradictions.

Summarize any issues found.

### Step 4: Report and Fix

If issues found:
Report that Reader Claude struggled with specific issues.

List the specific issues.

Indicate intention to fix these gaps.

Loop back to refinement for problematic sections.

---

**If no access to sub-agents (e.g., claude.ai web interface):**

The user will need to do the testing manually.

### Step 1: Predict Reader Questions

Ask what questions people might ask when trying to discover this document. What would they type into Claude.ai?

Generate 5-10 questions that readers would realistically ask.

### Step 2: Setup Testing

Provide testing instructions:
1. Open a fresh Claude conversation: https://claude.ai
2. Paste or share the document content (if using a shared doc platform with connectors enabled, provide the link)
3. Ask Reader Claude the generated questions

For each question, instruct Reader Claude to provide:
- The answer
- Whether anything was ambiguous or unclear
- What knowledge/context the doc assumes is already known

Check if Reader Claude gives correct answers or misinterprets anything.

### Step 3: Additional Checks

Also ask Reader Claude:
- "What in this doc might be ambiguous or unclear to readers?"
- "What knowledge or context does this doc assume readers already have?"
- "Are there any internal contradictions or inconsistencies?"

### Step 4: Iterate Based on Results

Ask what Reader Claude got wrong or struggled with. Indicate intention to fix those gaps.

Loop back to refinement for any problematic sections.

---

### Exit Condition (Both Approaches)

When Reader Claude consistently answers questions correctly and doesn't surface new gaps or ambiguities, the doc is ready.

## Final Review

When Reader Testing passes:
Announce the doc has passed Reader Claude testing. Before completion:

1. Recommend they do a final read-through themselves - they own this document and are responsible for its quality
2. Suggest double-checking any facts, links, or technical details
3. Ask them to verify it achieves the impact they wanted

Ask if they want one more review, or if the work is done.

**If user wants final review, provide it. Otherwise:**
Announce document completion. Provide a few final tips:
- Consider linking this conversation in an appendix so readers can see how the doc was developed
- Use appendices to provide depth without bloating the main doc
- Update the doc as feedback is received from real readers

## Tips for Effective Guidance

**Tone:**
- Be direct and procedural
- Explain rationale briefly when it affects user behavior
- Don't try to "sell" the approach - just execute it

**Handling Deviations:**
- If user wants to skip a stage: Ask if they want to skip this and write freeform
- If user seems frustrated: Acknowledge this is taking longer than expected. Suggest ways to move faster
- Always give user agency to adjust the process

**Context Management:**
- Throughout, if context is missing on something mentioned, proactively ask
- Don't let gaps accumulate - address them as they come up

**Artifact Management:**
- Use `create_file` for drafting full sections
- Use `str_replace` for all edits
- Provide artifact link after every change
- Never use artifacts for brainstorming lists - that's just conversation

**Quality over Speed:**
- Don't rush through stages
- Each iteration should make meaningful improvements
- The goal is a document that actually works for readers
Current: **v2.5** (nomenclature — N-2 nomenclature: H1 version-header delimiter standardized from -- to — (em-dash); version line added; 2026-08-04)


