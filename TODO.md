# TODO
_Last updated: 2026-03-20_

## Up next

- [ ] **Ticker watchlist** — persistent list of 5–10 names that always show price, previous close, and daily % change on page load (no search required)
- [ ] **Organize asset files** — review project structure, move files into logical folders (e.g. `static/`, `src/`)
- [ ] **Explore backend data** — audit what the API actually returns and surface any unused fields worth displaying

## Design / polish

- [ ] **Typeface revisit** — IBM Plex Serif + Mono is the current choice (see comment in `styles.css`); may want to compare against other Tufte-compatible pairings
- [ ] **Chart legend** — consider all-caps left-aligned label as a more terminal-console treatment

## Decisions log

| Date | Decision |
|---|---|
| 2026-03-20 | Removed title/subtitle; white background; primary accent `#325893` |
| 2026-03-20 | Shifted to terminal aesthetic: monospace, square controls, no shadows/animation |
| 2026-03-20 | Applied mild Tufte treatment: serif/mono split, reduced visual scaffolding, chart simplified |
| 2026-03-20 | Adopted IBM Plex Serif + IBM Plex Mono as matched type pair |
| 2026-03-20 | Centralised font stacks into `--font-serif` / `--font-mono` CSS variables |
