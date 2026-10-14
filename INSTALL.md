# Install HPL Physical Book Check — friend-test release 1.3.6

This is a manual-install beta for supervised testing. It is available from [GitHub](https://github.com/mit112/hpl-physical-book-check/releases/tag/v1.3.6); it is not listed or approved in OpenAI's public plugin directory. A GitHub link does not automatically install it in ChatGPT.

The plugin supplies instructions and an optional local evidence processor. Your session needs permitted tools that can inspect live HPL record details and item-level holdings. It supplies no browser, server or library-account connection. Python is optional; it is not needed just to use the workflow manually. Installation options depend on your host, account and workspace.

## Route A: desktop/Codex repository marketplace

Use this route if you have a supported ChatGPT/Codex desktop host and Codex CLI available. The publisher checked catalog discovery with Codex CLI 0.160.1; a different account's actual installation and live lookup remain friend-test checks.

1. Review the [source](https://github.com/mit112/hpl-physical-book-check), [privacy policy](PRIVACY.md) and [terms](TERMS.md).
2. Add the pinned GitHub marketplace:

   ```sh
   codex plugin marketplace add mit112/hpl-physical-book-check --ref v1.3.6
   ```

3. Confirm the plugin is offered:

   ```sh
   codex plugin list --marketplace mit-hpl-plugins --available --json
   ```

   The available entry should be `hpl-physical-book-check@mit-hpl-plugins`, version `1.3.6`. Being listed as available is not the same as being installed.
4. Open the desktop Plugins browser, choose **Mit HPL Plugins** / `mit-hpl-plugins`, and install **HPL Physical Book Check**. The CLI plugin browser is also accessible with `/plugins` from an interactive Codex session. If the source does not appear, restart the desktop app and check again. The exact UI labels may differ by host.
5. Start a fresh chat after installation. Confirm version 1.3.6 in the plugin details, then invoke the installed plugin and use a prompt from [FRIEND-TESTING.md](FRIEND-TESTING.md). Invocation menus and live browser tools vary by host.

Do not use the OpenAI submission portal to install this for personal testing. Publisher identity verification and marketplace review are a separate distribution process.

To remove the source later, uninstall the plugin through your host's plugin browser, then run:

```sh
codex plugin marketplace remove mit-hpl-plugins
```

Removing the marketplace source and uninstalling its plugin are separate actions. No HPL accounts or connections are configured by this package.

## Route B: private import through Plugin Creator — account-dependent

Use this only if your ChatGPT account/workspace offers Plugin Creator and permits private plugin creation. This route has not been verified on a fresh recipient account. It is a test option, not a promise that every web or mobile account supports ZIP import.

1. Download **hpl-physical-book-check-1.3.6.zip** from the [friend-test release](https://github.com/mit112/hpl-physical-book-check/releases/tag/v1.3.6).
2. Start a new ChatGPT conversation, select Plugin Creator, and attach the ZIP.
3. Send:

   > Import this ZIP as a private copy of HPL Physical Book Check for my account or workspace. Preserve the package's instructions, references and processor without rewriting them. Do not publish it to the public directory or change access for other people. Tell me the saved version and give me its install link. If this account cannot import the archive, explain the limitation instead of recreating a different workflow.

4. Follow the resulting install flow, check the saved version, and start a fresh conversation with the plugin selected. Run the friend tests. Record any normalization or version change rather than assuming the saved copy is byte-identical.

If Plugin Creator is unavailable or import fails, report that installation as blocked. Do not treat attaching the ZIP as proof that a persistent plugin was installed. Use Route A if appropriate. Workspace permissions still apply.

## Limitations and updates

After installation, use the installed plugin to ask book questions. An ordinary chat that can only search snippets may be unable to inspect the item rows required for a live answer. In that case the result must remain Unable to verify.

A private imported copy does not establish an update connection to this repository. The pinned marketplace route stays on this release until you deliberately select a newer release. To switch it later, use the marketplace add command with the new published tag and follow your host's update/reinstall flow. Do not advertise automatic updates or identical behavior on every host.

The optional processor is unchanged from 1.3.4. Reference material, unfamiliar labels and unknown statuses can still prevent a complete result. The separate experimental retrieval prototype is not included.

References: [OpenAI package and marketplace guide](https://developers.openai.com/plugins/build/plugins), [plugin usage](https://learn.chatgpt.com/docs/plugins), and [Plugin Creator availability](https://learn.chatgpt.com/docs/build-plugins).
