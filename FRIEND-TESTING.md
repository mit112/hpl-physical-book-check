# Try a book search and tell Mit how it went

**New here? [Start with setup](INSTALL.md).** This is an early test version, **1.3.9**. It helps check printed books at Houston Public Library using ChatGPT or Codex. Setup may need help and does not work with every account yet.

## 1. Ask about a book

Start a new chat with **HPL Physical Book Check** selected. Try:

> Is The Hobbit by J. R. R. Tolkien available at the Heights branch of Houston Public Library?

Or use a book you want to read. Include the title, author if you know it, and branch—or say “any Houston Public Library branch.”

## 2. Look at the answer

Could you understand the result from the opening sentence or two? Were **Details** easy to find, including a catalog link you could open? When present, did **Also useful** answer a likely next question? Did it explain whether it found a copy or could not finish checking?

**“Unable to verify” does not mean there are no copies.** It means the check was incomplete. Availability can change; check the linked catalog before making a trip. No library login is needed, and this tool does not place holds.

## 3. Tell Mit what happened

Reply wherever Mit shared the link, or [report a problem here](https://github.com/mit112/hpl-physical-book-check/issues). If setup stopped you, that is useful feedback too.

Copy this if it helps:

```text
I used: ChatGPT / Codex
I tried this on: computer / phone
I got to: setup / selecting the plugin / asking about a book
The book and branch I tried:
What happened:
What was confusing:
Plugin version, if I could find it:
```

You do not need technical knowledge. Do not share library-card numbers, passwords, account details, private reading lists, or full chat transcripts. A short example with personal details removed is enough.

<details>
<summary>Optional extra checks</summary>

If you want to help test more than one search:

- Ask for **The Employees by Olga Ravn at any HPL branch**, and say that any available English print copy is enough. It should stay on that book, rather than another book by the same author.
- Ask for **The Lion, the Witch and the Wardrobe by C. S. Lewis at Looscan**, and specify this book only, English print, with a thorough check. It should explain any unfinished parts of the search.
- Ask for **Home at Looscan** without naming an author. It should ask which book you mean.

These are behavior checks, not promises that copies are available. Installation, plugin selection, and live catalog access are separate checks. A summary of what the plugin does is not proof that it can perform a live search. Reference material may not be borrowable. An available-results count or a hold button alone does not establish an available copy. Unknown totals should remain unknown; a safe incomplete answer is still an incomplete search.

For a detailed report, include the app/version, setup route, saved plugin version, which searches completed, any public catalog links, and any errors. Remove personal details.

</details>

## Message you can share

> I made a tool to help check printed books at Houston Public Library using ChatGPT or Codex. You can ask about a book at your usual branch or anywhere in HPL. It is an early test version: setup may need help, requires a computer, and does not work with every account yet. If you try it, please tell me what worked or where you got stuck. Start here: https://github.com/mit112/hpl-physical-book-check
