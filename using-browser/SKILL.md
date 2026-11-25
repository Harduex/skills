---
name: using-browser
description: Tests, verifies and debugs a web app in a real browser through whichever browser tool the agent has (a browser MCP server, a built-in browser pane, a browser extension, or a project's own browser skill), and carries the pitfalls that make browser automation mislead. Use when exercising or verifying a UI change, reproducing a bug in the browser, checking console errors or failed network requests, testing responsive or touch layouts, testing as several users, or when clicks or typing reach the page but the app does not react.
---

# Using a Browser

This skill says how to test a web app in a browser well. How to call the browser tool is the tool's own job: its descriptions and instructions are the reference, and this skill does not repeat them.

## Pick the tool

1. **A project browser skill comes first.** If the project has one (often named `<project>-<tool>`), load it. It carries the app's URLs, test accounts, login flow, fixtures and known console noise, and it builds on this skill.
2. **Otherwise, use the browser tool this session has.** Check the tools you can call instead of assuming one. Common ones are the Chrome DevTools MCP server, the Playwright MCP server, a browser pane built into the agent app, and a browser extension that drives the user's own browser.
3. **When several are available**, take the one the user named, then the one the project's instructions name, then an isolated browser over the user's own. The user's own browser carries their logins, so act in it only as far as the task needs.
4. **When none is available**, say so. Verify what you can with real requests or tests, and name what stays unverified.

## How to work

- **Read the page as structure before you act.** An accessibility snapshot gives stable references to click and fill; a screenshot confirms what the user sees. Read the page again after anything changes it, because old references go stale. When a snapshot is too large, use a screenshot plus a selector lookup.
- **Use the project's selectors.** Test ids the code already carries (`data-testid`, `data-cy`) beat selectors you invent.
- **Set up deterministically.** Use the repo's test accounts and fixtures, seeded data and a known starting page. Keep setup apart from the checks, so the flow can run again.
- **Check the outcome past the pixels.** Look at console errors, failed requests, and the side effect where it lands: the database row, the API response, the server log. A database tool next to the browser is the strongest pairing. Then clean up what this run created, and only that.
- **Report every planned case.** Name a skipped or blocked case with its reason; never leave it out.

## Pitfalls

Each of these has cost a debugging session. The code for each fix is in [REFERENCE.md](REFERENCE.md).

- **Typing that the app ignores.** React-controlled inputs ignore `el.value = …`: use the tool's fill or type action, or the native value setter. Rich-text editors (contenteditable, such as Lexical) ignore `innerText`: focus them and insert text. An editor that mounts lazily needs a click on its visible placeholder first.
- **Clicks that the app ignores on canvas and SVG.** Events made with `dispatchEvent` do not reach React handlers there. Call the handler props on the element, and read them again before each step of a gesture.
- **Touch layouts.** Resizing the window does not make the page a touch device. Use the tool's device emulation with touch on, and reset it between devices. If taps land in the wrong place under mobile emulation, keep touch and drop the mobile flag.
- **Blocking dialogs.** Close them through the UI (Escape, the close button), or switch them off through the app's own storage key. Never delete a dialog's elements from the page: that causes false errors later. Load a fresh page when the page state is in doubt.
- **A persistent browser profile keeps state**: storage, cookies and the logged-in user. Check who is logged in before you call anything a permission bug.
- **Console history is short.** Many tools return only the messages since the last navigation. Ask for preserved messages when an earlier page's error matters.
- **Throttling may not reach WebRTC.** Browser network throttling can leave WebRTC (UDP) media untouched. Limit it in the operating system, and prove in every run that the limit worked.
- **Several users.** Use a separate browser context or profile for each user, and note each user's role and settings before you judge a permission.
- **A UI state that the props do not explain.** Read the component's state from React's fiber on the DOM node.
