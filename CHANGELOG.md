# Changelog

## 1.4.0 — Unreleased candidate

- Add a host-browser runner that executes thorough title-list searches, traverses observed pages, captures print metadata/item cells, and saves each view/work before continuing. Require explicit identity, edition and exclusion review before the existing completion gate can close coverage.
- Add resumable collections, persisted bounded reopen intent, retention/rechecking of known editions omitted by a later search, and fail-closed handling for stale cards, repeated pages, external pagination links and browser transport loss.
- Recognize observed regular-print and teen/collection labels only within verified print records. Preserve explicit unavailable detail and keep undetermined language unresolved. Reset browser recovery state on a later refresh.
- Include the Node runner suite in the full gate and both ZIP variants. Preserve quick/any-one processing semantics.
- Validate live retrieval across 76 unique Goodreads winners (79 award labels), retaining 61 complete and 15 partial checks after real catalog gaps and subsequent host transport failure. This is local candidate evidence, not production ChatGPT certification. Do not update the private plugin or published release until that remaining runtime validation succeeds.

## 1.3.9 — October 16, 2026

- Build a resumable queue from saved per-work evidence, returning at most ten actionable works without consuming them on read.
- Add `finalize`: unfinished work exits 1 with `continue` or `blocked`; only the requested stopping rule exits 0. Retain partial coverage for quick positives and support explicit quick requests accepting any one work.
- Record access/host-limit checkpoints with cause, observed evidence, run and time. Defer isolated failures while continuing other works; resume or refresh without accepting stale blockers or inventory.
- Preserve all award labels when a work wins multiple categories or years. Establish the full manifest before catalog searches and route list lookups through the executable gate when a host executor is available.
- Add a 79-work regression, malformed-input and blocker controls, mutation checks, and a consuming-assistant simulation. Package the new tests in both ZIP variants.

Distribute both ZIP variants and SHA-256 checksums under `v1.3.9`; the setup guide and friend-test instructions now point at this release. Existing private imports need an explicit update. A skills-only plugin still cannot enforce host tool invocation or certify supplied observations.

## Video and repository update — October 16, 2026

- Re-cut the introduction (31.3 seconds) and walkthrough (89.2 seconds) so narration, step titles and end cards no longer name a plugin version: they say to download the file ending in `-chatgpt.zip` from the guide and check that the version matches it. The October 14 screenshots still show 1.3.7 as captured.
- Play both videos inline in README.md ([PR #2](https://github.com/mit112/hpl-physical-book-check/pull/2)) and drop the 1.3.7-only video caveats. The v1.3.8 release notes point to the README players; the v1.3.7 release keeps its 1.3.7-specific MP4s.
- Re-point the `v1.3.8` tag and `main` to rewritten commits that change only the 1.3.8 commit's author email. Every file, tree and message is unchanged, and so are the 1.3.8 release assets.

## 1.3.8 — October 15, 2026

- Lead book-search answers with the practical result, then Details and Also useful. Keep uncertainty upfront and list tables compact, with coverage and edition evidence below.
- Gather a few relevant follow-up facts during the same read-only lookup, reusing evidence before checking additional HPL sources. Preserve quick-check stopping, identity clarification, explicit scope and catalog recovery limits.
- Include the answer guide in release packaging and exercise the response format with simulated cases.
- Build and validate both Codex and ChatGPT ZIPs. Verify that every shared file is identical and only the Codex marketplace catalog is omitted from the ChatGPT ZIP.
- Point setup instructions at the 1.3.8 packages and tag. Keep the existing videos and all 1.3.7 release assets intact.

The evidence processor is unchanged. Existing 1.3.7 installations need an update to receive the new answer format. Simulated response exercises and the offline gate do not certify live lookup or fresh-account installation.

## Published guide and distribution update — October 15, 2026

- Publish `hpl-physical-book-check-1.3.7-chatgpt.zip` and its SHA-256 checksum as additional v1.3.7 release assets. Its 23 files are identical to the tag; only `.agents/plugins/marketplace.json` is omitted. Plugin Creator rejected the plain ZIP and accepted this one. The original Codex ZIP is unchanged.
- Merge [PR #1](https://github.com/mit112/hpl-physical-book-check/pull/1): point INSTALL.md at the ChatGPT ZIP, use the tested setup message and step order, and link both videos from README.md.
- Publish the revised introduction (31.3 seconds) and walkthrough (89.4 seconds), with the repository URL and ChatGPT filename on the end cards. The closing line directs viewers to the setup guide at the link on screen.
- Update the v1.3.7 release notes with the ChatGPT ZIP pointer, video links and setup guide on `main`.

These distribution and guide changes are already live on GitHub; they do not change the released book-search instructions or evidence processor.

## 1.3.7 — October 14, 2026

- Lead with a plain-language introduction, one book question, and a Start here link.
- Explain setup in numbered steps and keep technical details expandable.
- Simplify the plugin description, help page, and feedback form.
- Make computer, account, and catalog-access requirements clear before setup.

Documentation and presentation update only. Book-search instructions and processor behavior are unchanged. Installation on a new user account and end-to-end usability remain unverified.

## 1.3.6 — October 14, 2026

- Add the Mit HPL Plugins repository marketplace with the plugin at the repository root.
- Add pinned desktop/Codex installation steps, an account-dependent Plugin Creator private-import option, and a friend-testing checklist/message.
- Document the observed skills-only public-directory submission restriction and separate it from GitHub/manual distribution.
- Remove pricing wording from the listing and clarify its library-research purpose while retaining the documented Productivity category.
- Validate marketplace routing in the actual ZIP, including a wrong-path rejection control.

The optional processor is unchanged. This friend-test release adds no hosted connector and makes no new end-to-end reliability claim.

## 1.3.5 — October 13, 2026

- Prepare a standalone public skills-only package with an independent icon, MIT license, support, privacy and terms pages.
- Resolve skill resources through the installing host's catalog rather than a private installation's package locator.
- State host requirements, supervised-use limits and unverified-result behavior in the listing and README.
- Set the intended publisher display name to Mit, United States targeting, and no commerce.

The optional evidence processor is unchanged from 1.3.4. The experimental retrieval prototype is excluded. This release makes no new live reliability or performance claim.

## 1.3.4

Added instruction checkpoints for pending pages/candidates, original-answer fidelity in diagnostics, and stopping an any-volume quick request at the first qualifying item. Its processor behavior is retained here.
