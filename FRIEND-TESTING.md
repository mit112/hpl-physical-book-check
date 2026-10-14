# Friend testing — 1.3.6

Start with [INSTALL.md](INSTALL.md). This test is about whether a friend can install the package and use its workflow in their own host. Installation, skill activation and live catalog access are separate checks. No fixed availability verdict is promised: inventory can change.

## 1. Verify installation and activation

- Record the host/app, version if visible, and install route used.
- Check the plugin details for saved version 1.3.6. If an importer changed it, record the actual version.
- Start a new chat with the plugin selected and ask it to summarize its lookup scope and limitations. It should explain physical print scope, host-provided live retrieval, and honest incomplete outcomes. This explanation alone does not prove a live lookup works.
- If the plugin cannot be installed, selected or loaded, stop and report that boundary. Do not silently substitute a generic answer.

## 2. Run a quick single-title check

> Quick check: is The Employees by Olga Ravn available as an English physical print book anywhere in Houston Public Library? Any qualifying copy is enough.

Check that it verifies the requested work and actual item rows, excludes different works by the same author, and stops at the first qualifying available copy. A partial positive should have unknown title-wide totals. Without sufficient evidence it should say Unable to verify, not invent availability or an exhaustive negative.

## 3. Run a thorough constituent-volume check

> Check The Lion, the Witch and the Wardrobe by C. S. Lewis at HPL Looscan. English physical print, this volume only, thorough check.

Check that it stays on this constituent, verifies language and edition, retains unresolved candidates/pages/statuses, and provides observed record links and a coverage statement. An Available tab count or a Place Hold button alone is not an available item. Reference/special-collection material must keep borrowing and transfer uncertainty. Record any unknown ordinary children's material labels; the bundled processor has not received the experimental prototype's extra aliases.

## 4. Check ambiguity handling

> Check Home at HPL Looscan, physical print.

It should clarify the intended author/work before inspecting candidate holdings. Multiple unrelated books called Home must not be combined into one result.

## 5. Check read-only behavior and evidence

Ordinary checks must not sign in, request library credentials, place holds or change settings. Results should name the requested branch, retain real raw statuses, show actually observed catalog links and check times, and disclose any incomplete coverage. If your host cannot inspect live item rows, that is a capability limitation, not a library inventory finding.

## Send back this short report

Copy this to Mit or use the repository's [Issues tab](https://github.com/mit112/hpl-physical-book-check/issues):

```text
Host/app and version:
Install route: marketplace / Plugin Creator import
Saved plugin version:
Installation: passed / blocked / failed
Plugin activation: passed / blocked / failed
Live item rows accessible: yes / no / unknown
Quick check behavior:
Thorough check behavior:
Ambiguous Home behavior:
Observed catalog links (public only):
Errors or gaps:
One thing that was confusing:
```

Redact account details. Do not send credentials, library-card numbers, private reading lists or full chat transcripts. A small redacted excerpt is enough to explain a problem. A correct Unable to verify answer is a safe outcome; count the intended lookup as incomplete, not as a successful inventory check.

## Short message to send with the link

> I made an independent HPL print-book lookup workflow for ChatGPT/Codex. It is a manual-install beta, not an OpenAI-directory listing, and it needs a host with live catalog browsing. Could you try installing it and running the three sample requests? The install guide has a desktop/Codex route and an account-dependent Plugin Creator import option. Please tell me where it works or gets stuck—no library login or holds are needed. Start here: https://github.com/mit112/hpl-physical-book-check/blob/v1.3.6/INSTALL.md
