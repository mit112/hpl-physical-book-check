# Start here: find your first library book

**HPL Physical Book Check** helps you check printed books at Houston Public Library using ChatGPT or Codex.

**Already installed?** Skip to [Ask about a book](#ask-about-a-book).

## Before you start

This is an early test version, **1.3.7**. It takes some setup, may need help, and does not work with every account yet. Installation and a book search still need to be tested on a new user's account.

Use a **computer**. Plugins are not currently available in the ChatGPT mobile app. You will need an account that lets you install this plugin, and a chat that can open the library's live catalog pages. See [OpenAI's plugin guide](https://learn.chatgpt.com/docs/plugins).

You do not need to sign in to a library account for these checks. This tool does not place holds.

## If you use ChatGPT

**This is a setup option to test, not a confirmed install method for every account.** It worked on Mit's account on October 14, 2026. Try it only if your account offers Plugin Creator. That is the ChatGPT tool that helps add plugins.

Prefer to watch first? The [walkthrough video](https://github.com/mit112/hpl-physical-book-check/releases/download/v1.3.7/hpl-physical-book-check-walkthrough.mp4) shows these steps.

1. On your computer, [download the ChatGPT plugin file](https://github.com/mit112/hpl-physical-book-check/releases/download/v1.3.7/hpl-physical-book-check-1.3.7-chatgpt.zip) (`hpl-physical-book-check-1.3.7-chatgpt.zip`). Leave it zipped: do not open or unpack it. Use this file, not the plain 1.3.7 ZIP, which is for Codex.
2. Open a new ChatGPT chat. Type **@** in the message box, search for **Plugin Creator**, and select it. If you cannot find it, stop here and [ask Mit for help](SUPPORT.md).
3. Attach the file you downloaded. Copy and send this message exactly:

   > Create a private plugin from this HPL package. Keep its instructions and files. Give me the installation link and saved version. Do not publish or share it. If your account cannot import it, say so instead of creating a replacement.

4. Open the installation link it gives you, and install if asked. Check that the name is **HPL Physical Book Check** and the saved version is **1.3.7**; if it differs, tell Mit.
5. Choose **Try in chat**. Or start a new chat, type **@**, search for **HPL Physical Book Check**, and select it under **Plugins**. Then [ask about a book](#ask-about-a-book).

If no installation link appears, or you cannot select the plugin afterward, setup has not finished. [Get help](SUPPORT.md). Attaching the file alone does not install it. You do not need the OpenAI developer submission website.

## If you use Codex

This option requires the Codex command-line tool. If you do not already use it, [ask Mit for setup help](SUPPORT.md); do not install extra software just to follow these instructions.

<details>
<summary>Show Codex setup steps</summary>

The publisher confirmed that Codex CLI 0.160.1 could find the previous 1.3.6 release. Discovery of this documentation update has not been checked in a new account. Installation and a live book search on a new user's account still need testing.

1. Open your terminal and copy this command:

   ```sh
   codex plugin marketplace add mit112/hpl-physical-book-check --ref v1.3.7
   ```

2. Open the desktop **Plugins** browser. Choose **Mit HPL Plugins** and install **HPL Physical Book Check**. In an interactive Codex session, `/plugins` opens the plugin browser. If the source does not appear, restart the desktop app and try again. Labels may differ by app.
3. Check the plugin details for **1.3.7**. Start a new chat and select or invoke the installed plugin, then ask the book question below. If you cannot find it or it cannot open the catalog, get help.

For a technical check that the source was added:

```sh
codex plugin list --marketplace mit-hpl-plugins --available --json
```

Look for `hpl-physical-book-check@mit-hpl-plugins`, version `1.3.7`. An available listing does not mean the plugin has been installed.

</details>

## Ask about a book

With **HPL Physical Book Check** selected, copy this or use your own book and branch:

> Is The Hobbit by J. R. R. Tolkien available at the Heights branch of Houston Public Library?

Include the author if you know it. To check all branches, say “at any Houston Public Library branch.”

The answer should give you a catalog link and explain what it could check. **“Unable to verify” means it could not finish checking. It does not mean the library has no copies.** Your chat may be unable to open the catalog pages it needs, even after installation.

Check the linked catalog before making a trip. Ask the library about borrowing or pickup rules.

## If something goes wrong

- **Cannot find Plugin Creator or install the file?** Your account may not support this setup option.
- **Cannot find HPL Physical Book Check in a new chat?** Installation or selection may not have finished.
- **Installed, but no book result?** The chat may lack catalog access, or the check may be incomplete.

[Get help from Mit](SUPPORT.md). Tell him which app you used and which step stopped working. You do not need to diagnose the problem yourself.

<details>
<summary>Updates, removal, and technical notes</summary>

A private imported copy does not update automatically from this repository. The Codex setup is pinned to 1.3.7; switching versions requires adding the newer published tag and following your app's update or reinstall flow.

To remove the Codex installation, uninstall the plugin in the Plugins browser, then remove its source:

```sh
codex plugin marketplace remove mit-hpl-plugins
```

Uninstalling the plugin and removing its source are separate actions.

This skills-only package supplies instructions and an optional evidence processor, not a browser, server, or library-account connection. Python is optional for manual use. Live checks need permitted tools that can inspect record details and item-level holdings; search snippets alone are insufficient. Unknown labels or statuses and reference material can prevent a complete result. The processor is unchanged from 1.3.4; the experimental retrieval prototype is excluded.

The ChatGPT plugin file is the 1.3.7 release without `.agents/plugins/marketplace.json`, the Codex marketplace catalog that Plugin Creator rejected; every other file is identical to the `v1.3.7` tag.

This GitHub release is separate from OpenAI's public plugin directory; it is not listed or approved there. Import availability and saved version depend on your account and workspace. Do not treat an imported copy as necessarily byte-identical to the ZIP.

See the [source](https://github.com/mit112/hpl-physical-book-check), [privacy policy](PRIVACY.md), [terms](TERMS.md), [OpenAI package guide](https://developers.openai.com/plugins/build/plugins), and [Plugin Creator guide](https://learn.chatgpt.com/docs/build-plugins).

</details>
