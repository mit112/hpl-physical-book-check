# Executing a thorough title list

This is the live retrieval path for a thorough multi-title request. It runs inside a host that provides a permitted `cua_repl` browser, Node.js file/subprocess access, and Python 3.10+. It uses the host's browser; it does not install Playwright, launch another browser, request an HPL login, or call a catalog endpoint. Quick and single-title checks retain the existing workflow.

Resolve this package through the host's exact skill locator. Read the access guide and establish the complete manifest first. Initialize the processor ledger as described in the evidence toolkit. Discover the host's Python executable; do not assume the user's default Python meets the version requirement. Users do not need to install software when these capabilities are supplied by the host.

If package resources are returned as URIs, read the actual script resources through that package's supported file tools and materialize them in the host working directory before import. Keep `hpl_browser.mjs` and `hpl_evidence.py` together. Do not use another installation's path or guess a private package locator. A source-read failure and a missing execution capability are separate failures.

## Start the runner

Use the current CUA instructions to create one catalog tab at `https://halan.sdp.sirsi.net/client/en_US/hou/`, then inspect its current state. Import the resolved packaged module in `cua_repl`; ordinary Node file/subprocess access must be permitted by that host. No extra npm or pip package is needed.

```js
var {makeHplRunner} = await import(resolvedSkillDirectory + '/scripts/hpl_browser.mjs');
var runner = makeHplRunner({
  tab: catalogTab,
  ledgerPath: savedLedgerPath,
  processorPath: resolvedSkillDirectory + '/scripts/hpl_evidence.py',
  python: verifiedHostPythonPath
});
var batch = await runner.collect(5);
```

`collect` executes real Advanced Search, follows the observed result pages, inspects print records, and saves rendered metadata and item-cell arrays. It collects up to ten works per call; five keeps ordinary calls shorter. It saves each view before another navigation and each work before the next. Restarting the runner with the same ledger returns retained collections awaiting review. A collection does **not** count as a completed lookup.

The runner searches the main title before a colon to avoid requiring a subtitle to be indexed. This deliberately widens searches for named volumes: identify the requested volume explicitly in review. An initials query with no result retries the surname before an author-relaxed fallback. Every observed candidate remains subject to identity review; a query match is never an identity decision.

If these host capabilities are absent or denied, record the actual capability error and preserve the manifest. A compatible live connector may execute the same saved queue. Do not silently replace the runner with an open-ended manual browser loop or a web-snippet check, and do not claim this runtime was executed. This package cannot grant host capabilities or repair the host's skill loader.

## Review the captured evidence

Inspect `batch.works`, especially each candidate's title, author, format, language, physical description when visible, and item material labels. Full observations are under `candidate.record.observation`. The assistant performs this assessment; ordinary catalog evidence review does not require asking the user for approval.

Supply exactly one decision per candidate:

```js
runner.review([{key: workKey, decisions: [
  {id: observedRecordId, match_state: 'exact', edition: 'Regular print'},
  {id: otherObservedId, match_state: 'excluded', reason: 'Observed different volume: Volume two'}
]}]);
```

Use `exact` only after verifying the intended work and edition. Label large print from its metadata/item material, even when its record Format says Books. Exclude translations only with observed language evidence, and exclude unrelated works, adaptations, films, audio and kits with observed reasons. Blank or undetermined language remains unresolved; a foreign-looking title alone is insufficient. Use `unresolved` for any identity/metadata ambiguity. Never bulk-accept all English results merely because the search was for the requested book.

`review` ingests the captured evidence and marks search/edition closure only when candidate decisions close. When every candidate is excluded after an author-constrained search, it schedules the author-relaxed search instead of accepting a negative. Item statuses, counts and unknowns still pass through the existing processor; review cannot override them. Preserve differing raw statuses. A collection label displayed in the Status column is not an availability claim.

## Continue, recover and finalize

After review, call `runner.finalize()` and inspect its state. `continue` requires another collection/review cycle; a sample, elapsed time or a positive item does not finish a thorough list. Repeat until every requested work is resolved or has its own observed blocker. Include requested other-branch alternatives from the same captured rows.

For a collected work whose rows, counts or metadata remain incomplete, `runner.retry(workKey)` permits one ordinary reopen, then `collect` recaptures it. Re-review the newly captured candidate set; do not assume it is unchanged. If the source still lacks usable evidence, save an isolated checkpoint through the processor with the exact record/cells and attempted recovery, then continue other works. An implementation/parser error needs diagnosis; it is not proof the catalog is unavailable.

A security challenge gets one ordinary reload and a bounded readiness wait. If it remains, the runner records a global access checkpoint and stops once. Do not change browsers, routes or fingerprints to evade it. Follow host confirmation rules for any interactive challenge. Resume only after access is observed to return, using the processor's `resume`, then the same saved ledger.

`finalize` returns `complete`, `continue`, or `blocked` with the full manifest report. Only `complete` permits a complete answer. `blocked` permits an explicitly incomplete answer naming the actual cause, all remaining work and the saved ledger location. Checkpoints do not schedule background work. No skills-only package can stop a host from answering outside this path; validation must distinguish actual runner execution from that unverified host behavior.

Keep the ledger and its adjacent `.browser` directory together in a durable host artifact. A later refresh must use the processor's `refresh` before collecting; the runner rejects prior-run captures as inventory evidence. Report the actual observation interval for a long sweep.
