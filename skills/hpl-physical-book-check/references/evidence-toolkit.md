# Local evidence toolkit

Use `python scripts/hpl_evidence.py --help` relative to this skill's resolved local directory. Python 3.10+ and the standard library are sufficient. Resolve/read the packaged script through the host's skill/file tools when needed. This is optional local processing, not a live scraper, browser installation, or MCP server. Never replace unavailable catalog access with cached test fixtures.

## Workflow

1. Create a title list JSON array of objects containing `title` and `author`. Initialize a working ledger with `init --titles titles.json --output ledger.json --branch Looscan`. Use the user's actual branch, or `--all-branches`. Add `--language English` for the actual language scope and `--mode quick` only when requested. The default is thorough. Titles are deduplicated by normalized title+author; the output lists stable keys and the run ID.
2. Retrieve live record metadata and item cells with permitted tools. When the host permits rendered DOM inspection, extract table headers and cell arrays from the visible holdings table. Preserve cell boundaries: concatenated row text makes multiword branch names, material types, and statuses ambiguous. Do not inspect hidden page state or call undocumented endpoints.
3. Write one record evidence JSON per observation using the contract below. `match_state` is an assessment based on inspected title/author/edition identity, not the search query or approximate string matching. Unknown identity becomes `unresolved`. A confidently unrelated work becomes `excluded`. Unknown language remains blank/Unknown, not an assumed English match. Large print must be labeled from edition evidence even when Format says Books.
4. Ingest with `ingest ledger.json --key KEY --record record.json`. This validates and replaces an earlier observation of the same record; it never silently appends duplicate records. Record timestamps must be real, timezone-aware, no earlier than the run's start, and not in the future. The supplied record ID must match the observed HPL record URL. A differing query in the URL is rejected.
5. After actually completing the relevant searches/pages, use `mark ledger.json --key KEY --search-complete --editions-complete`. Add `--fallback-complete` after the no-match fallback. These flags are operator declarations: the processor cannot independently prove browser coverage. Keep the Work coverage receipt alongside the ledger (queries/filters, actual pages screened, candidate IDs/decisions/reasons and pending work). Do not mark flags from result counts alone. Missing pages, statuses, counts, language, or identity remain unresolved. Quick mode permits a complete negative after exhaustive coverage; a quick positive remains partial with unknown title-wide totals.
6. Run `report ledger.json` for structured results with exclusive status/coverage counts and edition/item evidence. Do not describe confirmed minimums as full totals. `pending ledger.json` lists titles that still lack complete coverage, including quick positive results that would need a thorough follow-up. Resume these entries in the same run and preserve already completed evidence.
7. For a later refresh, use `refresh ledger.json` before retrieving fresh statuses. It starts a new run and resets coverage; old observations remain bibliographic hints and cannot count as current inventory. Revisit their observed catalog links, verify identity, and ingest newly observed item evidence. Report real check times from records.

Keep working ledgers separate from immutable test fixtures and skill source. Save a checkpoint through the host's persistence mechanism for cross-session continuation; do not promise that a transient working path survives. If local execution is unavailable, maintain these fields manually and apply the main skill's classifications.

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
