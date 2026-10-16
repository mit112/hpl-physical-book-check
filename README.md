# Find a print book at Houston Public Library

**This branch contains the unreleased 1.4.0 browser-runner candidate.** The published release and private account plugin remain **1.3.9**. Production ChatGPT execution is unverified; the setup links below intentionally still point to the published release. See the [candidate validation record](VALIDATION.md#140-live-browser-candidate--october-16-2026).

Want to know whether Houston Public Library has a book you want to read? **HPL Physical Book Check** helps you check printed books at your favorite branch or anywhere in the library system, using ChatGPT or Codex.

Once it is set up, ask in your own words. For example:

> Is The Hobbit by J. R. R. Tolkien available at the Heights library?

It tries to find a copy and tells you where it is, whether it is available, and where to look for it on the shelf. It includes a library catalog link so you can check the result yourself. If it cannot finish checking, it will say so.

**[Start here: setup and your first book search →](INSTALL.md)**

## Watch first

**30-second introduction**

https://github.com/user-attachments/assets/01a0614c-5487-4a67-b479-450e59e6b575

**90-second setup walkthrough**

https://github.com/user-attachments/assets/44e5f8a5-af11-4453-a892-09c38f7a1178

The book results shown are October 14, 2026 examples; availability changes. The screens show the version installed that day; use the current file from the [setup guide](INSTALL.md).

**Before you start:** this is an early test version, **1.3.9**. Setup may need help, and it does not work with every account. There is no one-click ChatGPT install link yet. Use a computer; plugins are not currently available in the ChatGPT mobile app. Your chat also needs access to the library's live catalog. See the [setup guide](INSTALL.md) and [OpenAI's plugin guide](https://learn.chatgpt.com/docs/plugins).

## What you can ask

- “Is Dune by Frank Herbert available at Heights?”
- “Can you find The Employees by Olga Ravn at any Houston Public Library branch?”
- “Check these three books at Looscan: [book titles and authors].”

Include the author if you know it. You do not need special wording. If more than one book matches, it should ask which one you mean.

## A few things to know

- It checks **printed books**, including large print. It does not check ebooks or audiobooks.
- No library login is needed for these checks. It does not reserve books for you.
- Availability can change. Check the linked catalog before making a trip; ask the library about borrowing or pickup rules.
- This is an independent project by **Mit**, not an official Houston Public Library service. No payment to Mit is required; your ChatGPT or Codex account requirements still apply.

**Got stuck? [Get help](SUPPORT.md).** Already set up? [Try a book search and tell Mit how it went](FRIEND-TESTING.md).

<details>
<summary>Technical details, testing, and directory status</summary>

This is a skills-only plugin with instructions, an evidence processor and a host-browser runner. It has no hosted catalog API, MCP server, browser of its own, or library-account connection. The host must supply tools that can inspect live catalog records and item-level holdings. Single-title and quick manual use does not require Python. The candidate thorough-list runner requires a host with permitted CUA browser access, Node.js 18+ and Python 3.10+; it needs no npm or pip packages. Users need no software installation when the host supplies those capabilities. See the [evidence toolkit](skills/hpl-physical-book-check/references/evidence-toolkit.md).

A quick check stops at a verified available item. A thorough check aims to resolve every scoped candidate and edition. Incomplete evidence must produce **Unable to verify** or a partial positive; unknown totals stay unknown. Regular and large print are distinguished. Digital books, audio, DVDs, adaptations, and kits are excluded from ordinary print requests. Reference and special-collection status does not establish borrowing or transfer eligibility. Checks remain read-only; holds require separately supported tools and authorization.

Version 1.3.7 simplifies the introduction, setup guide, feedback, and plugin description. Version 1.3.6 added manual marketplace distribution. Those releases retained the 1.3.4 processor. Automated tests cover processor behavior, not end-to-end reliability across hosts. Use with supervision. The separate experimental retrieval prototype is excluded and does not certify this package. See [validation scope](VALIDATION.md).

Version 1.3.8 simplifies book-search answers: a direct answer first, **Details** for editions, shelf numbers, links and coverage, then **Also useful** for related findings. During a thorough lookup, it reuses evidence and checks a few relevant HPL sources for likely next questions about the same book or location, such as other copies, branch hours or pickup rules. Quick checks still stop at the first confirmed copy. See the [answer guide](skills/hpl-physical-book-check/references/answer-format.md). Existing 1.3.7 installations need updating to receive these changes.

Version 1.3.9 adds saved batches and a completion gate: unfinished thorough checks cannot pass `finalize`, isolated failures defer only their own work, and real access or host limits require a saved cause and evidence. Award labels survive deduplication. The 79-work simulation and offline tests exercise resume and stopping behavior; they do not certify live retrieval. The helper cannot force ChatGPT to invoke it or authenticate an operator's coverage declarations. Existing installations need an update; follow the [update steps](INSTALL.md#update-an-existing-installation).

The uploaded 1.3.5 draft was blocked on October 14, 2026: “We are not accepting more skills-only submissions at this time.” The portal also flagged pricing wording and category clarity during scanning. Version 1.3.7 removes listing pricing wording and clarifies the library-research purpose; Productivity remains the documented category. It has not been reuploaded or rescanned. This package is **not submitted for review, approved, or published in OpenAI's public directory**. GitHub distribution and private/local installation are separate. Check the actual portal state before attempting another submission.

The repository catalog is `.agents/plugins/marketplace.json`; its `./` source points at this plugin root. From the repository root, run `python3 verify.py` for the full processor suite and both package variants. No third-party Python packages are required. Run `python3 build_release.py` for the Codex ZIP or `python3 build_release.py --chatgpt` for the ChatGPT ZIP, both outside the repository. The gate verifies that the only difference between them is the omitted marketplace catalog. Target directory country: United States.

</details>

[Privacy](PRIVACY.md) · [Terms](TERMS.md) · [MIT license](LICENSE) · [Release notes](CHANGELOG.md)
