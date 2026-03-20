# TODO

Updated: 2026-03-20

## Up next

- [ ] Ticker watchlist: persistent list of 5 to 10 names that always shows price, previous close, and daily percent change on page load.
- [x] Organize asset files: review project structure and move files into logical folders (for example static and src).
- [ ] Explore backend data: audit API responses and surface any useful unused fields.

## Design

- [ ] Typeface revisit: IBM Plex Serif + Mono is the current choice (see comment in styles.css); compare with other options if needed.
- [ ] Chart legend: consider an all-caps, left-aligned label for a stronger terminal-console look.

## Decisions

- 2026-03-20: Removed title/subtitle, switched to white background, set primary accent to #325893.
- 2026-03-20: Shifted to terminal aesthetic (monospace, square controls, no shadows, no animation).
- 2026-03-20: Applied mild Tufte treatment (serif/mono split, reduced scaffolding, simplified chart).
- 2026-03-20: Adopted IBM Plex Serif + IBM Plex Mono as matched type pair.
- 2026-03-20: Centralized font stacks into --font-serif and --font-mono CSS variables.
