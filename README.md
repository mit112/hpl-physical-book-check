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

## Requirements and installation

This is a **skills-only plugin**. Install its release ZIP using your host's supported plugin installation flow. It includes no hosted catalog API, MCP server or browser. Your host must provide permitted tools that can inspect live catalog records and item-level holdings. If those tools are unavailable or HPL blocks access, the plugin cannot verify current availability.

Normal use requires no terminal or Python installation. The optional local evidence processor needs Python 3.10+ and the standard library; it processes supplied observations and does not retrieve catalog data. See the [evidence toolkit](skills/hpl-physical-book-check/references/evidence-toolkit.md).

Keep checks read-only: no sign-in, holds or account changes. A separate request to place a hold requires separately supported tools and their authorization rules.

## Reliability and release scope

Version **1.3.5** is a public packaging and portability release based on 1.3.4. The optional processor is unchanged. Automated tests cover processor behavior, not end-to-end reliability across hosts. This tool is best used with supervision. The separate experimental guarded retrieval prototype and its live-check results are not part of this package and do not certify it. See [validation scope](VALIDATION.md).

## Support and policies

- [Get help or report a problem](SUPPORT.md)
- [Privacy policy](PRIVACY.md)
- [Terms of use](TERMS.md)
- [MIT license](LICENSE)
- [Release notes](CHANGELOG.md)

No payment is required. Target directory country: United States.

## Development

From the repository root, run `python3 verify.py`. It runs the full processor suite and checks the public package inventory and manifests. No third-party Python packages are required. Use `python3 build_release.py` to validate and build the release ZIP outside the repository.
