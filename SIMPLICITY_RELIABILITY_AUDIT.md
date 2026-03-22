# Simplicity + Reliability Audit

Updated: 2026-03-22
Owner: Glenn + Copilot
Status: In Progress

## Goal

Reduce avoidable complexity, make behavior predictable, and improve deploy/runtime reliability without changing product scope.

## How To Run This Audit

Work phase by phase in order. Do not start a new phase until the current phase has clear pass/fail outcomes.

## Phase 0: Baseline Snapshot (60-90 min)

### Tasks

- Record current production behavior for:
  - `/`
  - `/stocks`
  - `/stocks/`
  - `/api/health`
  - `/stocks/api/health`
- Capture one successful stock fetch and one provider-failure fetch.
- Save current TODO state and open issues.

### Evidence to collect

- HTTP status + response headers for each route.
- Screenshot of each UI state: loading, success, error.
- One short note in README describing current known quirks.

### Exit criteria

- [x] Baseline route matrix is documented.
- [ ] Baseline UI screenshots are captured.
- [x] Known quirks list exists.

### Phase 0 Baseline Log (2026-03-22)

Production probe (`https://stock-dashboard.onrender.com`) at capture time:

- `/` -> `503` with `x-render-routing: suspend-by-user`
- `/stocks` -> `503` with `x-render-routing: suspend-by-user`
- `/stocks/` -> `503` with `x-render-routing: suspend-by-user`
- `/api/health` -> `503` with `x-render-routing: suspend-by-user`
- `/stocks/api/health` -> `503` with `x-render-routing: suspend-by-user`

Local baseline (`http://127.0.0.1:5001`):

- `/` -> `200`, `Content-Type: text/html; charset=utf-8`, `Cache-Control: no-store, max-age=0`
- `/stocks` -> `200`, `Content-Type: text/html; charset=utf-8`, `Cache-Control: no-store, max-age=0`
- `/stocks/` -> `200`, `Content-Type: text/html; charset=utf-8`, `Cache-Control: no-store, max-age=0`
- `/api/health` -> `200`, `Content-Type: application/json`
- `/stocks/api/health` -> `200`, `Content-Type: application/json`

API behavior samples (local):

- Success sample: `GET /api/stock/AAPL` -> `200`, `source: yfinance`, `is_live: true`
- Failure sample: `GET /api/stock/INVALIDZZZ` -> `503`, `error: Failed to load data from Yahoo Finance`, `is_live: false`

Known quirks list:

- Render can return suspended routing responses (`x-render-routing: suspend-by-user`), which blocks production-route baseline collection at that moment.
- Path-based caching previously caused `/stocks` and `/stocks/` UI divergence; asset path and cache handling should be re-checked after each deploy.

## Phase 1: Routing + Caching Canonicalization (high risk)

### Tasks

- Confirm canonical path strategy (serve both directly vs redirect).
- Verify all page paths resolve identical asset bundles.
- Standardize cache policy for HTML, CSS, JS.
- Remove obsolete compatibility branches if no longer needed.

### Checks

- `/stocks` and `/stocks/` render the same DOM structure.
- Asset URLs and versions are identical from both paths.
- No stale CSS/JS after deploy on normal refresh.

### Exit criteria

- [ ] Route parity verified in browser and curl.
- [ ] Cache behavior documented and stable.
- [ ] No route-specific visual divergence.

## Phase 2: API Contract Hardening

### Tasks

- Define canonical API routes and keep aliases only when justified.
- Standardize response envelope fields (`source`, `is_live`, `provider_error`, `timestamp`).
- Ensure all error responses are explicit and actionable.
- Remove dead API code paths.

### Checks

- Every client request targets canonical endpoint or justified alias.
- 4xx/5xx payload structure is consistent.
- Health endpoint is reliable and independent of provider instability.

### Exit criteria

- [ ] API contract table added to docs.
- [ ] Client and server route mapping has no ambiguity.
- [ ] Error behavior is deterministic.

## Phase 3: Frontend State and Geometry Stability

### Tasks

- Enumerate all UI states for quote card and watchlist.
- Reserve stable space for loading/error/success to prevent layout shift.
- Eliminate duplicate rendering logic.
- Ensure mobile and desktop parity.

### Checks

- No major element movement between loading and loaded states.
- Error state uses same container dimensions as success where feasible.
- Watchlist table dimensions do not jump on data arrival.

### Exit criteria

- [ ] Layout-shift checks pass on desktop and mobile widths.
- [ ] State handling map exists (loading/success/error/empty).
- [ ] Rendering code paths are consolidated.

## Phase 4: Code and Dependency Pruning

### Tasks

- Remove unused imports, dead functions, obsolete comments.
- Minimize fallback branches that are no longer relevant.
- Review dependencies for necessity and pinning quality.
- Align file structure with current architecture.

### Checks

- No orphaned route handlers.
- No unused frontend helpers.
- Dependencies are all justified in README.

### Exit criteria

- [ ] Dead code removed.
- [ ] Dependency list reviewed and documented.
- [ ] Project tree reflects actual architecture.

## Phase 5: Docs + Operational Guardrails

### Tasks

- Rewrite README to reflect only canonical current behavior.
- Add a short pre-deploy reliability checklist.
- Add rollback instructions for bad deploys.
- Keep TODO tightly scoped to active priorities.

### Checks

- New contributor can run and verify app with one short path.
- Deploy checklist is fast (5-10 minutes) and repeatable.
- Route and data provenance behavior are documented clearly.

### Exit criteria

- [ ] README simplified and accurate.
- [ ] Pre-deploy checklist exists.
- [ ] Rollback steps are documented.

## Suggested Working Cadence

- Session A: Phase 0 + Phase 1
- Session B: Phase 2
- Session C: Phase 3
- Session D: Phase 4 + Phase 5

## Audit Scorecard (quick view)

Rate each area from 1 (poor) to 5 (strong).

- Routing consistency: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
- Cache reliability: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
- API contract clarity: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
- Frontend state stability: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
- Codebase simplicity: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
- Documentation quality: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5

## Immediate Next Step

After `/stocks` parity is confirmed, start with Phase 0 and Phase 1 in the same session to prevent drift between diagnosis and fixes.
