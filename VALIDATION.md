# Validation scope

Through 1.3.8, the optional processor and its 54 regression tests were byte-identical to private 1.3.4. They use synthetic and historical public catalog evidence, not current holdings. Version 1.3.9 extends that processor and suite as recorded below. At 1.3.9, the processor had not received the separate retrieval prototype's extra children's-print aliases or a guarded browser implementation.

Version 1.3.6 adds the repository marketplace, friend installation/testing docs, and listing clarification. The publisher's Codex CLI 0.160.1 discovered the local marketplace and its available 1.3.6 plugin using temporary command-line configuration overrides. This did not install the plugin or change the user's persistent marketplace settings. A listed plugin is not proof of installation, skill activation or live catalog access.

The full gate runs the processor suite and actual ZIP inventory, manifests, icon and marketplace routing checks. It includes rejection controls for a forbidden file, private app binding and wrong marketplace path. CLI catalog discovery is a separate runtime smoke check. Plugin Creator accepted the ChatGPT-specific ZIP on Mit's account; installation and live lookups on a new user's account remain pending the tests in FRIEND-TESTING.md. No cross-host, unattended or complete-recall certification is claimed.

The OpenAI portal's October 14 eligibility restriction prevents skills-only directory submission at this time for the observed draft. Pricing wording has been removed from this release's listing and its purpose clarified, but no fresh portal scan or acceptance is claimed. Published support/privacy/terms pages remain in place. GitHub distribution is separate from directory approval.

Unknown labels, reference eligibility, raw statuses and incomplete evidence remain gaps. Keep incomplete negatives Unable to verify and incomplete totals unknown. Run `python3 verify.py` for the full offline gate. The offline gate performs no live catalog searches; executed live checks are recorded separately below.

## Published guide and distribution — October 15, 2026

[PR #1](https://github.com/mit112/hpl-physical-book-check/pull/1) merged as `1c56eab`, establishing the guide and distribution baseline for the answer-format changes. It pointed INSTALL.md at the ChatGPT ZIP and the tested setup message/order, and linked both videos from README.md.

The [v1.3.7 release](https://github.com/mit112/hpl-physical-book-check/releases/tag/v1.3.7) contains the additional ChatGPT ZIP, its checksum and both revised videos. Its notes point ChatGPT users at the correct ZIP and link the videos and setup guide on `main`. The original Codex ZIP retains its October 14 upload/update timestamp. The downloaded ChatGPT ZIP matches its published SHA-256 checksum: all 23 included files are byte-identical to `v1.3.7`, and the only omitted tagged file is `.agents/plugins/marketplace.json`.

The producer reports that the revised introduction is 31.3 seconds and walkthrough 89.4 seconds, both with the repository URL and ChatGPT filename on the end cards, and that the separate media project's `python3 src/verify.py` passed. That media check was not rerun in this repository. These publication checks do not validate live catalog lookup or fresh-account installation.

## Videos and history — October 16, 2026

[PR #2](https://github.com/mit112/hpl-physical-book-check/pull/2) embeds version-neutral re-cuts of both videos as GitHub attachments (web encodes under 10 MB). Both rendered `<video>` sources returned `206 video/mp4` to an unauthenticated request. The 1.3.8 commit was rewritten to change only its author and committer email, and the `v1.3.8` tag's tagger email; trees, messages and dates were compared and are identical. `v1.3.5`–`v1.3.7` and `1c56eab` are unchanged. These checks do not validate live catalog lookup or fresh-account installation.

## 1.3.8 answer presentation — October 15, 2026

The source now routes response composition and bounded related checks through `references/answer-format.md`, which is included in both release ZIPs. The processor and its 54 tests are unchanged. The full offline gate passes with the installed Python 3.14 runtime: a 25-file Codex ZIP, a 24-file ChatGPT ZIP, byte-identical shared files, and rejection controls for a forbidden file, private binding, wrong marketplace path and a marketplace catalog in a ChatGPT ZIP. The new variant check failed against the old builder before the implementation. The Mac's default `python3` is 3.9, below the optional helper's documented 3.10+ requirement; the installed `python3.14` was used.

Before/after simulated response exercises cover a complete positive, an access-blocked incomplete check, a quick positive, a three-book list and ambiguous identity. Additional exercises cover “just the answer,” an explicit branch/edition limit and an available reference copy with unknown borrowing eligibility. The baseline exposed a six-column list table and zero-filled status buckets; the updated answers put the decision first, separate supporting evidence and related findings, and propose bounded official-source follow-ups. Quick and ambiguous cases propose no further retrieval. Missing links, times and eligibility facts stay unknown.

These exercises evaluate answer composition and proposed retrieval decisions from supplied evidence. They are not automated assertions about model output, live searches, executed enrichment, or validation in an installed ChatGPT/Codex host. Existing 1.3.7 downloads retain their original contents; installations need an update to receive 1.3.8.

## 1.3.9 batch completion — October 16, 2026

The observed 1.3.8 host run ended after about 200 seconds with only two partially checked titles. Its recorded browser errors recovered and its last catalog calls succeeded; no recorded error established a hard host limit. The existing continuation instructions did not prevent premature finalization.

Version 1.3.9 extends the existing processor with `next`, `finalize`, `checkpoint` and `resume`, and requires the skill's list flow to use them when a host executor is available. Queue reads do not consume work. Thorough positives remain unfinished until coverage closes. Quick positives retain partial coverage while satisfying their requested stopping rule. Title-specific access failures do not defer unrelated works. Blocked runs never pass the completion gate; they retain their full report and documented cause for an explicitly incomplete answer.

The full offline gate, `python3 verify.py` under Python 3.14, passed with exit 0: 67 tests, a 29-file Codex ZIP and 28-file ChatGPT ZIP, identical shared files, and the existing archive rejection controls. The original processor suite remains green. No new runtime dependency is required.

New CLI regressions exercise 79 simulated works from two partial observations through batches of 10, 10, 10, 10, 10, 10, 10 and 9. Finalization initially exits 1 with all 79 works still pending, and exits 0 only after all are resolved. Repeated queue reads preserve both the batch and ledger bytes. Additional tests cover per-work/global blockers, resume, stale evidence/blockers after refresh, quick stopping, explicit any-one requests, award-label merging, and malformed roots, keys and blocker metadata. The suite failed before implementation; the non-object-root regression separately failed before its review fix.

Four temporary script mutations were rejected by the intended assertions: treating a thorough positive as finished, returning only a two-work sample, accepting blank blocker evidence, and retaining a global blocker after refresh. The source was not mutated for these checks. Positive completion and valid-blocker controls prevent a reject-everything implementation from passing.

A separate consuming assistant read the updated source skill and references, resumed the two-partial-work fixture ledger, and executed all eight batches using the helper. Its command audit records 79 ingests, 79 coverage marks, queue reads after each batch and a final `complete` exit 0. Retained artifacts independently reconcile 79 complete works, 27 simulated Looscan positives, 52 simulated Heights alternatives, 79 editions and 131 item rows. Every requested work appears in its full result artifact. These fictional records and award labels are not live holdings or actual award results.

The helper validates declared evidence and queue state; it cannot authenticate catalog observations, independently prove a complete award manifest or search coverage, force a host to invoke it, or continue after a host ends a turn. Without an executor, the manual queue contract remains instruction-based and must disclose that the executable gate was unavailable. The consuming-assistant exercise used supplied complete-scope fixtures, not live browser navigation or a hard host limit. Live large-list retrieval in the original ChatGPT host remains unverified. That distribution package and setup guide targeted `v1.3.9`; account updates retain the existing private plugin identity and audience. A saved account release or marketplace listing alone does not establish live lookup behavior.


## 1.4.0 live browser runner — October 16, 2026

**Automatic loading and invocation from an installed ChatGPT plugin remain unverified.** Version 1.4.0 adds a real host-browser execution path. It still depends on the host loading the skill, exposing a permitted CUA tab and allowing Node/Python execution; a skills-only package cannot force invocation outside that contract. Publication and the existing private-account update are explicitly authorized for this rollout; they do not certify that remaining host behavior.

The two retained production failures were inspected separately. One reported workflow loading failure and used web lookup; the other retrieved live holdings but ended after one title without closing the requested queue. Retained traces do not expose every loader event or tool output, so the exact loaded releases remain unproven. Account source was verified at 1.3.9; that does not prove which source either failed session used.

### Executed local retrieval

Official yearly/category pages established 79 award labels and 76 unique works for 2021–2025. The local CUA run searched and reviewed every work, including regular and large print, translations, other volumes, unrelated works, films and kits. It retained 531 rendered-view captures, per-work candidate decisions, record links, item-cell arrays, timestamps and a durable ledger. Confirmed inventory observations span **5:17:24–5:41:10 p.m. CDT on October 16, 2026**. They are a dated interval, not a claim that every item was checked at one instant.

The final live receipt has **61 complete and 15 partial works**, with **28 confirmed Looscan-positive works** across those coverage states. Partial positive counts are minimums; incomplete negatives remain Unable to verify. Catalog gaps include item rows showing only a collection label as Status, missing/undetermined language, and copy counters exceeding all displayed rows. Reopening affected records preserved these gaps. After all works had been collected, the browser transport stalled while an alternate MARC view was attempted; subsequent reopen actions failed before dispatch, and a screenshot timed out and reset the CUA session. The full saved queue ended **blocked**, exit **1**, with all remaining causes retained. It did not pass a complete-availability gate.

The runner was revised as live markup differences were found; frozen intermediate modules and captures are retained locally. The final transport-loss, omitted-edition and missing-browser guards were then tested offline. The exact final source has not completed another full 76-work sweep or an installed ChatGPT trial. The fresh final-source smoke test below covers two titles and saved resume.

### Automated checks and independent trials

The full gate is `python3 -B verify.py` using Python 3.10+ and Node.js 18+. On the verified machine it used Python 3.14.8 and Node 20.20.2, with no third-party Python/Node dependency or installation. It passed **71 Python tests and 18 Node tests**, plus actual Codex/ChatGPT ZIP checks, exit **0**. The only package difference remains the omitted Codex marketplace file. New boundary regressions were observed failing before their repairs. Five isolated mutations also failed assertions as intended: stopping after one work, dropping a known edition, retaining stale closure on reopen, accepting an external Next link, and ignoring host transport loss. These simulated browser tests validate control flow and evidence handling, not real server markup by themselves.

An independent Luna High baseline trial retrieved some live rows but first stopped prematurely despite an actionable queue; the assistant identified that stopping decision as its own error. Its continuation encountered a browser capability/context loss. A second Luna High trial read the candidate source and retained a 12-work manifest, but its session exposed no IAB browser. It exercised the helper/restart boundary and saved a host-limit checkpoint with zero verified works. That trial is a real capability failure in a Codex simulation of Work behavior; it is not a successful production ChatGPT test.

The [desktop-only plugin option](https://developers.openai.com/plugins/deploy/desktop-only) was evaluated but not enabled. Changing session eligibility does not demonstrate that a browser is exposed or that this helper runs. No hosted server, browser workaround, security bypass, new account connection or access change was introduced.

### Fresh final-source smoke test

On October 16, 2026, a fresh Codex session directly imported the final runner and used its permitted CUA in-app browser to search The Employees by Olga Ravn and My Friends by Fredrik Backman, English regular and large print, Looscan first with other branches. It executed two separate one-work batches and recreated the runner before reviewing the first work. Resume returned its retained observation without fetching another view; finalization remained `continue` until both works were reviewed.

The final receipt was `complete`, **2 satisfied / 0 remaining**, with three print editions, 45 item rows and ten durable rendered-view captures. Included-record observations span **6:01:37–6:01:59 p.m. CDT**. This run used the exact final runner/processor source, Python 3.14.8 and Node 20.20.2. It did not refresh or relabel the earlier 76-work observations.

This is actual live runner execution in the available Codex host, using a direct source import. It is not a fresh-account installation test or proof that ChatGPT automatically loads and invokes the saved private plugin. That host-specific loading and capability constraint remains explicit after the authorized release. No eligibility flag, permissions, connection or public-directory status was changed.
