# Catalog access and recovery

Entry: https://halan.sdp.sirsi.net/client/en_US/hou/

Use the host's available catalog connector if it exposes live item rows. Otherwise use permitted browser interaction for this dynamic catalog. A skills-only plugin cannot install or supply browser capabilities. Follow the host's tool and fallback rules; do not use this reference as permission to bypass them. If the host cannot inspect live holdings, report that limitation. Titles with no usable inspected holdings evidence remain unverified; preserve complete or partial evidence already obtained for other titles.

## Search and holdings

- In Work, follow [Work lookup workflow](work-workflow.md) for separate Title/Author search fields, efficient candidate screening, and the coverage receipt. Title-only searches are fallbacks; for short titles they can be much broader than an author-constrained search.
- On the observed HPL interface, “Library Search” and the “Physical Materials” tab target physical catalog records, including non-book formats. Confirm each record says Books/Book or Large Print rather than relying on that tab alone.
- Follow the Work reference's separate Title/Author route when applicable; otherwise search title and author using All Fields. If that returns no verified match, use the Title field or known ISBN, then verify author on the result. The search field may appear as a combobox rather than a textbox. Use observed controls and labels; do not hardcode DOM selectors or invent record identifiers.
- Confirm the current query in the destination URL and result state after submission. A filled search input alone is insufficient: the previous detail page can remain visible until navigation completes. Accept a matching-query results page or a matching-query single-result detail redirect; do not require only a results URL. Verify that an auto-opened record is the requested work. Broad title/author searches can return other books by the same author, sequels, compilations, and works mentioning the title. Use the observed Title field/ISBN fallback before exhaustive broad-page inspection when it reduces unrelated results; record both queries.
- Inspect physical description/edition and item material type for large print. “Books” is also used for some large-print records, so a format filter alone does not distinguish editions. Do not classify an edition solely from its publisher's name. Verify language rather than assuming an English search returns only English editions.
- Wait for actual search results or an explicit zero-results message after submitting. Homepage carousels are not search results. “Searching...” in Library/Status cells is not a completed holdings check. Inspect the direct record/detail view if the search row does not finish loading.
- Read Library, Home Location, Material Type, Shelf Number/Call Number, and Status per item. Do not confuse the Home Location (e.g. Fiction) with the branch name. Record exact labels and due dates.
- After detail enrichment finishes, another tab such as Novelist Content may become selected. Reopen the observed holdings tab (its accessible name can change to “Click to show holdings - Available:N”) and inspect the table. The tab's count is not a substitute for item rows.
- Record an aggregate's scope before comparing: record-wide counts need that record's all-branch rows, branch-filtered counts need that same branch's rows. Three available copies across HPL and zero at Looscan are compatible. Missing rows or unknown aggregate scope mean an incomplete comparison, not a demonstrated discrepancy.
- Clear branch or Available-only filters before negative conclusions. Inspect every applicable result page and any holdings pagination or “show more.” Record the last completed page and remaining controls. Search-result copy totals may include unavailable items and must not override inspected item rows.
- Use record links exposed by the catalog. If a detail overlay lacks a reusable URL, use its observed detail/permalink link. If none exists, label the link unavailable; an observed search URL can be offered separately as a search link, not as an inspected record link.

## Recovery budget

For an ordinary failed page or unresolved loading state, use at most **two recovery attempts after the initial attempt**: (1) refresh/reopen the affected view once; (2) inspect an already exposed alternate detail/availability view, if available. If no alternate exists, stop after the refresh. Use condition-based waits provided by tools, at most 15 seconds per wait; do not poll indefinitely or add long fixed sleeps. Host limits override this budget.

After a loading wait fails or times out, inspect the current page title and visible text again before classifying the failure. A security challenge can appear after the initial page check. “Just a moment...” or “Performing security verification” means access is blocked, not zero search results or an unavailable book. Preserve the shared cause in the ledger and report unverified results. Do not recommend local software installation as a requirement for using this plugin.

For a site-served security/bot challenge, use at most **one permitted low-risk recovery attempt** such as a brief wait/reload. Stop if the block remains. Follow host confirmation rules for interactive challenges. Do not change network routes, fingerprints, or guess alternative endpoints to evade it.

If the entry/search page still fails after permitted recovery, stop the batch. If two different record pages show the same access/loading failure, perform one entry/search health check within its remaining recovery budget; stop the batch if that fails. Isolated record failures may be marked partial/unverified while other titles continue. On a site-wide block, preserve completed evidence and report the remaining titles as unverified/not checked, explaining the shared cause once.

When a single method cannot show item rows, switch only to an available, host-permitted method. Do not claim the library is down because a retrieval tool failed. Explain which capability failed and what could not be verified.

## Resume and freshness

Keep completed queries, observed record links, timestamps, remaining titles, and unchecked pages in the ledger. Resume only unresolved work within the same run if access returns. On a later run, reuse bibliographic identity to save search effort but recheck statuses before calling them current. Report the actual check interval for a long run; never label old rows “checked now.”

## Before reporting

For collected-versus-individual requests, verify completion separately for every requested title; all umbrella-query pages screened does not close individual-volume searches. Preserve a confirmed positive while marking unresolved scope partial. For reference/special-collection alternatives, show catalog status and material labels separately from unverified borrowing/transfer eligibility.

- Confirm the candidate list is closed: record actual pages screened, all included/excluded/unresolved record decisions, and remaining records/pages. A negative requires no unresolved candidate or uninspected scoped holdings; a claim such as “3 pages checked” alone does not establish that.
- Confirm title/author/edition identity and requested language.
- Confirm digital/audio and unrelated adaptations were excluded.
- Confirm available counts come from item statuses, not Copies or hold controls.
- Confirm missing/loading rows do not become negative inventory claims.
- Confirm edition totals are labeled complete or unknown.
- Confirm every requested unique work appears and both sets of snapshot counts reconcile.
- Confirm links were observed and the timestamp is real.

