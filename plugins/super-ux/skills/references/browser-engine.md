# Browser engine — a rendered screen is checked in WebKit (Safari) first

Load this when an audit, a live pass or a research walk is about to open the
product, or someone else's, in a browser. Which tool drives the browser is
open; which engine renders first is not.

## The order

**WebKit first.** Its support envelope is the narrowest of the three big
engines, so a screen that works there is the stricter claim — and iOS Safari
users are the audience every Chrome-only check misses.

| Need | WebKit route (first) |
|---|---|
| a real browser, driven | Safari through `safaridriver` (WebDriver); enable remote automation once with `sudo safaridriver --enable` |
| scripted runs, captures, network and redirect logs | Playwright's `webkit` — the `webkit` project, `--browser webkit`, installed with `npx playwright install webkit` |
| debugging a render | Safari Web Inspector |
| opening a page by hand on macOS | `open -a Safari <url>` — not the system default browser, which may be another engine |
| an automation library (browser-use and the like) | its WebKit/Safari backend, where it has one |

## Chromium is a stated fallback, never the default

Use Chromium only when the task needs Chrome itself — a Chrome-only API,
Lighthouse, a CDP trace, the chrome-devtools MCP or a Chrome extension — and
say which and why in the evidence. Prefer the Chrome Dev build for that run.
When you launch your own Chrome or Chromium for a UI run, give it a temporary
profile (never the user's), record what you started, and close every process
you started before you finish.

## What the evidence says

Every runtime receipt names its engine. A screen checked only in Chromium is
reported as exactly that — "checked only in Chromium" — never as "tested in a
browser" or "verified in the browser". A claim about behaviour across engines
needs a receipt from each. No browser at all is the BLOCKED (unverified) case
the audit already defines, not a reason to fall back silently to whatever
browser is the system default.
