# TODO

Updated: 2026-03-20

## Up next
- [ ] Build two-section layout as top priority: (1) single-stock quote with extra detail, (2) small live-only watchlist (1 to 2 additional tickers).
- [x] Get live data active (Yahoo Finance requests succeeding reliably).
- [ ] what other data can i get from yfinance
- [ ] Explore backend data: audit API responses and surface any useful unused fields.
    - [ ] create a database file in git that i can reference?
- [ ] Future expansion: grow the watchlist from 1 to 2 symbols up to 5 to 10 symbols with price, previous close, and daily percent change on page load.
- [x] Organize asset files: review project structure and move files into logical folders (for example static and src).

## Design

- [ ] Typeface revisit: IBM Plex Serif + Mono is the current choice (see comment in styles.css); compare with other options if needed.
- [ ] Chart legend: consider an all-caps, left-aligned label for a stronger terminal-console look.

## Decisions

- 2026-03-20: Watchlist contract fields selected: displayName, lastPrice, previousClose (see data/selected_fields.json).
- 2026-03-20: Data provenance v1 shipped: live-only by default, explicit 503 on failure, ENABLE_MOCK_DATA dev flag, provenance fields on all responses.
- 2026-03-20: Removed title/subtitle, switched to white background, set primary accent to #325893.
- 2026-03-20: Shifted to terminal aesthetic (monospace, square controls, no shadows, no animation).
- 2026-03-20: Applied mild Tufte treatment (serif/mono split, reduced scaffolding, simplified chart).
- 2026-03-20: Adopted IBM Plex Serif + IBM Plex Mono as matched type pair.
- 2026-03-20: Centralized font stacks into --font-serif and --font-mono CSS variables.
