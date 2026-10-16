# Local evidence toolkit

Use `python scripts/hpl_evidence.py --help` relative to this skill's resolved local directory. Python 3.10+ and the standard library are sufficient. Resolve/read the packaged script through the host's skill/file tools when needed. This is optional local processing, not a live scraper, browser installation, or MCP server. Never replace unavailable catalog access with cached test fixtures.

## Workflow

1. Before catalog retrieval, create the full title list JSON array of objects containing `title` and `author`, with optional `labels` strings for award years/categories. Verify the complete bounded award list from official sources first and retain those sources with the coverage receipt. Initialize a working ledger with `init --titles titles.json --output ledger.json --branch Looscan`. Use the user's actual branch, or `--all-branches`. Add `--language English` for the actual language scope and `--mode quick` only when requested. Use `--any-one` only for an explicit quick request accepting any one of the listed works; ordinary lists require each work. The default is thorough. Titles are deduplicated by normalized title+author, merging their labels; the output lists stable keys and the run ID. Never replace the manifest with the first few titles checked.
2. Retrieve live record metadata and item cells with permitted tools. When the host permits rendered DOM inspection, extract table headers and cell arrays from the visible holdings table. Preserve cell boundaries: concatenated row text makes multiword branch names, material types, and statuses ambiguous. Do not inspect hidden page state or call undocumented endpoints.
3. Write one record evidence JSON per observation using the contract below. `match_state` is an assessment based on inspected title/author/edition identity, not the search query or approximate string matching. Unknown identity becomes `unresolved`. A confidently unrelated work becomes `excluded`. Unknown language remains blank/Unknown, not an assumed English match. Large print must be labeled from edition evidence even when Format says Books.
4. Ingest with `ingest ledger.json --key KEY --record record.json`. This validates and replaces an earlier observation of the same record; it never silently appends duplicate records. Record timestamps must be real, timezone-aware, no earlier than the run's start, and not in the future. The supplied record ID must match the observed HPL record URL. A differing query in the URL is rejected.
5. After actually completing the relevant searches/pages, use `mark ledger.json --key KEY --search-complete --editions-complete`. Add `--fallback-complete` after the no-match fallback. These flags are operator declarations: the processor cannot independently prove browser coverage. Keep the Work coverage receipt alongside the ledger (queries/filters, actual pages screened, candidate IDs/decisions/reasons and pending work). Do not mark flags from result counts alone. Missing pages, statuses, counts, language, or identity remain unresolved. Quick mode permits a complete negative after exhaustive coverage; a quick positive remains partial with unknown title-wide totals.
6. Use the batch loop below until `finalize ledger.json` permits the appropriate answer. `report ledger.json` is a diagnostic snapshot, not permission to finish. Do not describe confirmed minimums as full totals. `pending ledger.json` remains an exhaustive-coverage audit, including quick positives that would need a thorough follow-up; `next` instead applies the user's stopping rule. Resume the same saved ledger and preserve already completed evidence.
7. For a later refresh, use `refresh ledger.json` before retrieving fresh statuses. It starts a new run and resets coverage; old observations remain bibliographic hints and cannot count as current inventory. Revisit their observed catalog links, verify identity, and ingest newly observed item evidence. Report real check times from records.

Keep working ledgers separate from immutable test fixtures and skill source. Save a checkpoint through the host's persistence mechanism for cross-session continuation; do not promise that a transient working path survives. If local execution is unavailable, maintain these fields manually and apply the main skill's classifications.

## Batch loop and completion gate

Run with the host's Python 3.10+ executor, resolving the script from this skill package. This does not require software on the user's computer.

```sh
python scripts/hpl_evidence.py next ledger.json
# Retrieve live evidence for the returned works; ingest and mark each one.
# Repeat next after this batch, saving the ledger after each work.
python scripts/hpl_evidence.py finalize ledger.json
```

`next` reads at most ten actionable works in manifest order, with their identities, labels and remaining coverage gaps. Reading it never consumes work or advances a cursor. Only newly ingested evidence and actual coverage declarations resolve a work, so restarting the process returns unfinished work. A positive item does not finish a thorough work. A quick positive satisfies that work while its coverage stays partial; `--any-one` stops the whole quick request after a qualifying positive.

`finalize` emits a full report for every manifest work and one of these states:

| State | Exit | Required action |
| --- | --- | --- |
| `continue` | 1 | Execute `next_batch`; no final answer yet. |
| `blocked` | 1 | Every remaining work has a recorded blocker. Give an explicitly incomplete answer with the actual cause, per-work gaps and saved ledger location. Never describe this as a passed completion gate. |
| `complete` | 0 | Answer under the requested stopping rule. Preserve actual coverage; a quick success does not establish exhaustive totals. |
| Invalid input | 2 | Correct the input from retained observations; do not invent evidence or bypass the gate. |

If one record remains inaccessible after permitted recovery, defer that work and continue the others:

```sh
python scripts/hpl_evidence.py checkpoint ledger.json --key KEY --kind access --detail 'Describe the failed view and recovery actually attempted' --evidence 'Retained tool error or rendered failure text'
```

Omit `--key` only for an observed site-wide access failure or an actual host-wide limit (`--kind host_limit`). A global checkpoint affects every unfinished work; it preserves existing positives and complete results. Do not declare a global limit because the list is long or browsing is slow. The helper validates checkpoint structure, run and time, but cannot authenticate the supplied failure evidence.

After access returns, run `resume ledger.json --key KEY` for an isolated blocker or `resume ledger.json` to clear all blockers, then `next`. For a later fresh check, use `refresh` instead; it invalidates old inventory evidence and blockers. Checkpoints do not run background work or schedule a continuation.

Without a host executor, retain the full manifest and the same per-work states manually, use batches of at most ten, and reconcile every remaining work before answering. Disclose that the executable completion gate was unavailable. A skills-only package cannot force the host to invoke this helper or prevent the host from sending a final answer outside it.

## Record contract

Required fields:

| Field | Value |
| --- | --- |
| `record_id` | Numeric SD_ILS record ID from the observed record URL |
| `url` | Exact observed HTTPS HPL detail URL, not a search link |
| `title`, `author` | Observed bibliographic identity |
| `format`, `language` | Observed format and language; blank language means unknown |
| `edition` | Observed regular/large-print/other scoped edition label |
| `match_state` | `exact`, `excluded`, or `unresolved` |
| `holdings_complete` | JSON boolean reflecting inspected holdings coverage |
| `checked_at` | Actual observation ISO timestamp with offset |
| `run_id` | Current ledger run ID |
| `query` | Submitted query, when the record URL carries a `qu` parameter |
| `table` or `items` | Observed cell arrays or normalized item objects |

For `table`, include the first header row and every inspected item row, each as an array of strings. Required columns are Library/Branch, Material Type, and Status. Shelf Number/Call Number and Item ID/Barcode are optional and retained when visible. Row lengths must match the header. Normalize item objects as `branch`, `material_type`, `raw_status`, optional `call_number` and `item_id`. Keep identical-looking rows as separate copies if no item ID is supplied; deduplicate actual IDs. Shared IDs across editions count once globally, and conflicting observations stay unknown.

Optional `expected_copies` and `aggregate_available` are nonnegative integers taken from that record's displayed counters. They are cross-checks only. Disagreements produce partial coverage; they cannot manufacture available items. Collection labels such as Floating Collection are never offered as verified pickup branches. Special service locations such as BOOKLink require separate official pickup/access verification.

## Limits

The toolkit validates structure and applies counting rules; it cannot authenticate evidence, identify every title variant, or infer unobserved catalog pages. Strict validation errors should be corrected from source observations, not worked around by inventing fields. Run regressions from the plugin root with `python -m unittest discover -s tests -v`. Tests use synthetic/historical evidence and are not current holdings checks.
