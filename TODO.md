# TODO

Updated: 2026-03-22

## Up next
- [x] Top priority: Resolve `/stocks` vs `/stocks/` parity on Render (routing + asset consistency).
- [ ] Next priority after route parity: audit the whole project for simplicity and reliability (reduce complexity, harden behavior, and remove drift).
    - [ ] Run audit playbook: `SIMPLICITY_RELIABILITY_AUDIT.md` (Phase 0 -> Phase 5 in order).
- [ ] Watchlist management: add ability to reorder watchlist symbols.
- [ ] Watchlist management: add ability to add/remove symbols from the watchlist.
- [ ] Layout stability: fix geometry so component positions do not shift across loading/loaded/error states.
- [ ] Larger project (epic): add short notes linked to stocks (create/read/update/delete notes tied to ticker symbols).

## Stock Notes Discovery (before build)

- [ ] Scope v1 behavior: single note vs multiple notes per ticker, max note length, and whether notes are private per user or shared.
- [ ] Define data model: note id, ticker key normalization, note body, created_at, updated_at, optional tags/pin state.
- [ ] Decide persistence layer: start with local SQLite for MVP vs hosted DB for multi-user durability.
- [ ] Define auth requirement: no-auth local-only MVP vs user accounts/session support for real persistence.
- [ ] Clarify CRUD flows: create/edit/delete UX, autosave vs explicit save, confirmation for delete.
- [ ] Plan search/filter UX: by ticker, text search, sort by recency, optional pinned notes.
- [ ] Set validation and limits: empty note handling, max size, basic sanitization, and markdown/plain-text policy.
- [ ] Add provenance UX: show saved timestamp and clear failure states when writes fail.
- [ ] Decide API contract and routes: `/api/notes`, `/api/notes/<id>`, and ticker-scoped query shape.
- [ ] Add migration + backup plan: schema versioning and export/import path before production use.
- [ ] Define testing plan: unit tests for model and API, plus UI tests for create/edit/delete and reload persistence.

## Design

- [ ] Preserve current visual style while implementing drag/reorder and add/remove controls.
- [ ] Keep table and quote card dimensions stable during loading placeholders.

## Decisions

- 2026-03-20: Page now uses a two-panel layout: single-stock quote on the left, live watchlist on the right on desktop, stacked on mobile.
- 2026-03-20: Watchlist shipped live with 5 default symbols and calculated daily percent change on page load.
- 2026-03-20: Watchlist contract fields selected: displayName, lastPrice, previousClose (see data/selected_fields.json).
- 2026-03-20: Data provenance v1 shipped: live-only by default, explicit 503 on failure, ENABLE_MOCK_DATA dev flag, provenance fields on all responses.
- 2026-03-20: Removed title/subtitle, switched to white background, set primary accent to #325893.
- 2026-03-20: Shifted to terminal aesthetic (monospace, square controls, no shadows, no animation).
- 2026-03-20: Applied mild Tufte treatment (serif/mono split, reduced scaffolding, simplified chart).
- 2026-03-20: Adopted IBM Plex Serif + IBM Plex Mono as matched type pair.
- 2026-03-20: Centralized font stacks into --font-serif and --font-mono CSS variables.
- 2026-03-22: `/stocks` and `/stocks/` should always render the same UI and load identical assets.
