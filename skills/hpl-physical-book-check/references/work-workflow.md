# Work lookup workflow

Use the interactive browser exposed in this Work session under its current instructions. Discover controls from rendered state; this guide does not grant access or override browser policies. If the session lacks such a browser, preserve evidence and report the capability gap.

## Identity checkpoint

When a title has several plausible author matches and the user lacks an identifying clue, stop after gathering a short bibliographic candidate list and ask which work they mean. Holdings do not determine the user's intended identity. Do not open candidate holdings to make this clarification more useful. This checkpoint precedes the default thorough lookup; an explicit request to check all candidate works instead establishes that scope.

## Efficient search

1. Reuse one catalog tab for sequential searches and one ledger for the run. Read current state before choosing controls. Batch deterministic form edits and submission; then verify URL and loaded result identity. An immediate snapshot may still show the preceding query. Wait for the actual destination within the catalog-access recovery budget.
2. For a supplied title and author, use observed **Advanced Search** with separate **Title** and **Author** fields when a common/short title generates many unrelated records. Select **Library Search**; leave **Library: Any Library** and **Only Show Available** unchecked. An explicit language limit is allowed within the requested scope. Keep **Any Format** to retain regular and large print; exclude nonprint records while screening. Do not require multiple format searches if all scoped records are visible already.
3. If the author query has no match or appears restrictive (notably initials), relax it with a title-only search or user-supplied ISBN. Check observed result sizes before choosing a route. Title-only Dune produced 104 results in the live probe; separate Title=Dune and Author=Frank Herbert produced 21. Advanced search matches contributor fields too, so neither route proves identity.
4. Screen bibliographic cards across relevant pages. Record page identity/range, candidate record IDs, decisions and exclusion reasons. Skip waiting for unrelated records' statuses. Search pages may be screened while unrelated holdings say Searching. Matching records' statuses require completed loading. Follow visible Next/page controls, confirming a new result range. Top and bottom pagers describe the same pages.
5. A narrowed search can replace broad-page traversal when its constraints preserve the requested work, language and edition scope. Retain already discovered candidates from the broad search and inspect or explicitly exclude each. A known matching record omitted by the narrowed search must still be checked. Fewer results do not establish preserved coverage. For a title-wide negative, if author indexing/initials, title variants, or filters could exclude a scoped edition and coverage is not established, complete an author-relaxed Title search (with only scope-preserving language/format limits), or report the gap. If restricting format, screen both Books and Large print when both are in scope. Do not call a restrictive ISBN search complete for a request covering all editions.

## Collected-versus-individual coverage

For a thorough series/collected-work request, create one coverage entry for the collected work and one for each requested individual title. Search those individual titles directly, applying the existing author-relaxed fallback when needed. Reuse record IDs and inspected holdings found in umbrella searches; inspect only new or unresolved evidence. Surfacing individual-volume records in an umbrella query proves those records were found, not that each individual title's edition set is closed.

Each entry records its own queries, pages screened/remaining, included records, holdings rows inspected versus displayed total (unknown when not retained), and pending work. The whole request is complete only when all entries are closed. If one entry is incomplete, preserve positive items, show the per-entry gap, and label overall coverage partial. Explicit quick checks still stop at a confirmed requested-branch positive; the receipt preserves each remaining entry's actual checked, partial or unchecked state.

## Record evidence without repeated navigation

Use loaded item tables already attached to result cards when identity, language, edition and row coverage are established. Associate each table with its own record card. Details are needed for missing language, abridgment/adaptation, edition type, unresolved rows or pagination. A successful detail check need not be reopened to read identical rows again.

In the detail view, verify title/author, language, edition and format, then select the current holdings tab. Enrichment can select Novelist Content instead; the holdings tab's accessible name can change. Use its current observed name. Read actual table cells and inspect pagination/show-more and displayed copy-count consistency. “Available:N” is an aggregate cross-check.

Compare record-wide counters with the full record's rows, then calculate the selected branch's counts separately. In the receipt record aggregate scope and comparable row count. Uninspected other-branch rows cannot demonstrate a global discrepancy; an aggregate and a branch subset are different scopes.

“Illustrated edition” does not guarantee the original prose. Read contributor/description/cover text when needed: the observed Tolkien-attributed 2001 Hobbit card was adapted by Charles Dixon with Sean Deming. Exclude adaptations from an original-novel request; keep unclear candidates unresolved. Unabridged original text with illustrations remains eligible.

When supported, perform read-only extraction of rendered metadata, links, headers and cell arrays to avoid repeated full-page snapshots. Preserve table-to-record association and identical-looking separate copy rows. Inspect only rendered data under host permissions; no hidden application state, endpoint guessing or alternative networking.

## Coverage receipt and stopping

### Decision checkpoint before the answer

Reconcile the proposed answer with the ledger while the observations are still available:

| Check | Action |
| --- | --- |
| A page was visited but some cards were truncated, missing or not screened | Keep that page open in coverage; recover its remaining cards within the access budget. Do not count it as fully screened. |
| A known in-scope candidate or its holdings remains unresolved | Continue in thorough mode while access works. If blocked, lead a negative with Unable to verify and name the pending evidence and stopping cause. |
| A branch-filtered search is empty | Clear the branch limit before a title-wide negative; branch membership comes from inspected item rows. |
| A matching query redirects directly to one record | Record the redirect, record ID, identity and holdings coverage. No numbered results page is required; do not invent a page denominator. |
| A candidate is excluded by observed identity or format | Retain the exclusion reason; its uninspected holdings are not a gap for the requested work. |

Use the existing scope-preserving narrowing rules before traversing a broad fallback. A title-only search is conditional on a matching/coverage concern, not a ritual after every closed search. Opening every excluded card is unnecessary. A complete search receipt can still contain an unresolved aggregate-versus-row discrepancy; report search closure and status verification separately.

### Diagnostic fidelity

Build a requested receipt from retained observations and the actual original answer. Separate original claim, supporting observations, correction (if any), and evidence not retained. Quote or identify the original assertion before correcting it; do not invent an earlier mistake or expand the user's scope to manufacture a gap. An observed exclusion needs no holdings check, and an unrequested hypothetical title variant does not by itself reopen coverage. Distinguish an action explicitly not done from one whose details were not retained. Report a displayed Worked-for duration only for the response it accompanies; keep original-answer and receipt durations separate and leave unknown timings unknown.

Keep this ledger per requested work, whether manually or with optional Python:

| Field | Required evidence |
| --- | --- |
| Identity/scope | Resolved intended work, or clarification pending; separate collected/individual coverage entries when requested |
| Search | Submitted fields, scoped filters, observed URL, actual pages/ranges screened and remaining pages |
| Candidates | Unique record IDs; include/exclude/unresolved decision; observed reason for exclusions |
| Included records | Identity/language/edition, item rows, observation time, holdings pagination/count gaps |
| Pending | Every unresolved candidate, unmatched known record, unchecked page or unknown status |
| Completion | For each requested work/volume: all applicable search pages screened and candidate decisions closed; scoped holdings fully inspected |

For a quick request, stop immediately on one verified available item at the requested branch and report partial coverage. If no positive exists, continue checking candidates; a final negative requires the complete receipt. If access or a host limit stops the check, return Unable to verify with remaining pages/editions. Speed targets never authorize skipping evidence.

On request to audit, return query and page coverage, included record IDs/links, excluded candidates/reasons, inspected rows, gaps, actual check interval and time measurements that were actually captured. The ledger records observations; it cannot reconstruct hidden tool calls or expand another chat's Worked-for panel.

