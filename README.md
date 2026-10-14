# HPL Physical Book Check

Free, independent instructions for checking physical print books at Houston Public Library. Published by **Mit**. Not affiliated with or endorsed by Houston Public Library.

![Book and check icon](assets/icon.png)

## What it does

Ask about a book at a named HPL branch, or across HPL. The workflow checks work identity, language and edition, then interprets observed item rows. It reports call numbers, catalog links, check times and what coverage remains. Regular and large print are distinguished. Digital books, audio, DVDs, adaptations and kits are outside an ordinary print-book request.

Try:

- “Check Dune by Frank Herbert at Heights; English physical books only.”
- “Quick check: is The Employees by Olga Ravn available in print anywhere in HPL?”
- “Check The Lion, the Witch and the Wardrobe by C. S. Lewis at Looscan, this volume only.”

A quick check stops at a verified available item. A thorough check aims to resolve every scoped candidate and edition. If evidence is incomplete, the answer must say **Unable to verify** or label a positive as partial; unknown totals stay unknown. Catalog availability can change after a check. Reference and special-collection status does not establish borrowing or transfer eligibility.

## Install and try the friend-test beta

Version **1.3.6** supports manual distribution from this repository. Start with the [installation guide](INSTALL.md), then follow [friend testing](FRIEND-TESTING.md). Send friends the [pinned guide](https://github.com/mit112/hpl-physical-book-check/blob/v1.3.6/INSTALL.md) and [release ZIP](https://github.com/mit112/hpl-physical-book-check/releases/tag/v1.3.6).

- Desktop/Codex users can add the repository marketplace, install the plugin from the host's Plugins browser, and start a new chat.
- Accounts with Plugin Creator may be able to import a private copy of the ZIP. That recipient-account route still needs testing and is not guaranteed for every web/mobile account.

The GitHub link is a download/install starting point, not a one-click ChatGPT conversation link. Workspace sharing does not automatically give unrelated people access. The plugin's workflow can be used after installation only where the host supplies the necessary catalog tools.

This is a **skills-only plugin**. It includes no hosted catalog API, MCP server or browser. Its optional processor needs Python 3.10+ and the standard library to process supplied evidence; manual use does not require Python. See the [evidence toolkit](skills/hpl-physical-book-check/references/evidence-toolkit.md).

Keep checks read-only: no sign-in, holds or account changes. A separate request to place a hold requires separately supported tools and their authorization rules.

## Public-directory status

The uploaded 1.3.5 draft was blocked on October 14, 2026 with “We are not accepting more skills-only submissions at this time.” The portal also flagged pricing wording and category clarity while skill scanning was in progress. This release removes pricing language from the listing and makes its library-research purpose clearer; Productivity is retained as a documented category. It has not been reuploaded or rescanned in the portal, and those changes do not remove the eligibility restriction.

GitHub distribution and private/local installation are separate from OpenAI public-directory approval. This package is **not submitted for review, approved or published in that directory**. Availability may change later; check the actual portal state before attempting a new submission.

## Reliability and release scope

Version **1.3.6** adds manual marketplace distribution and friend-test instructions to the public package. It remains based on 1.3.4. The optional processor is unchanged. Automated tests cover processor behavior, not end-to-end reliability across hosts. This tool is best used with supervision. The separate experimental guarded retrieval prototype and its live-check results are not part of this package and do not certify it. See [validation scope](VALIDATION.md).

## Support and policies

- [Get help or report a problem](SUPPORT.md)
- [Privacy policy](PRIVACY.md)
- [Terms of use](TERMS.md)
- [MIT license](LICENSE)
- [Release notes](CHANGELOG.md)

No payment is required. Target directory country: United States.

## Development

The repository catalog is `.agents/plugins/marketplace.json`; its `./` source points at this plugin root.

From the repository root, run `python3 verify.py`. It runs the full processor suite and checks the public package inventory and manifests. No third-party Python packages are required. Use `python3 build_release.py` to validate and build the release ZIP outside the repository.
