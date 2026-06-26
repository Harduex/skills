---
name: quick-wins-analysis
description: Use when asked to discover and analyze quick wins — high-value, low-effort improvements that ride the existing infrastructure — across a product or codebase: a "find quick wins / low-hanging fruit / what can we improve cheaply" scan spanning UX, architecture simplification, new features, cleanup/dead-code, and performance/cost. Also when judging whether a specific change is "worth it" (value vs effort, risk, and added surface area), tiering an improvement audit, or separating real quick wins from deferred/medium-term work.
---

# Quick Wins Analysis

Find improvements that are **relatively easy and fast, ride the existing infrastructure, and bring more value out of the product.** The loop: frame with a product+architecture lens → fan out parallel research by dimension → consolidate into a tiered audit (with an explicit *NOT-a-quick-win* list) → per chosen item, verify the premise and re-rate honestly, then decide *is it worth it?* → execute surgically on a dedicated branch, pausing for sign-off.

## When to use

- "Find quick wins / low-hanging fruit / what can we improve cheaply" — a broad product- or codebase-level scan.
- Judging whether a specific change is *worth it* (consolidation, a small feature, a cleanup).
- Turning a pile of improvement ideas into a tiered, evidenced, decided plan.

When NOT to use: a single known fix (just do it); green-field design (architecture, not optimization).

## What counts as a quick win (the bar)

- **Rides existing infrastructure** (the load-bearing clause) — a toggle/seam/helper that's already there — and is **small, surgical, reversible**, with real product value.
- **"Is it worth it?" = value − effort − risk − *new surface area*.** A change that adds a path without removing one is *more* surface, not less → usually not a win.
- Rate Effort {S,M,L} × Impact {Low,Med,High} — **but treat every rating as a hypothesis, not a fact** (see step 4). A "broken-feeling" feature is worse than its absence; defer it.

## Workflow

### 1. Frame & ground
Adopt the lens the work needs — **senior architect + product owner + visionary** — and fix the scope (whole product, or one surface like the download/upload/comments area). **Read prior audits / domain docs first** so you don't re-walk solved ground.

### 2. Fan out parallel research by dimension
**REQUIRED SUB-SKILL:** superpowers:dispatching-parallel-agents. One research subagent per **dimension**, so each lens runs blind to the others and you keep the overseer's context clean:
- UX / UI · architecture simplification · new-feature opportunities · finish-it & cleanup (TODOs, incomplete features, **verified-dead code**) · performance & cost.

Each returns **evidenced** findings: `{ what, category, effort, impact, file:line }`. Cross-surface comparison surfaces the highest-leverage items (e.g. a heavy lib eager-loaded on *every* view).

### 3. Consolidate into a tiered audit
Dedupe overlaps; write `docs/audits/quick-wins-YYYY-MM.md`:
- **Tier-0 latent bugs** — stable IDs (`B1`, `B2`…), "fix regardless."
- **Highest-leverage quick wins** — numbered `name — one-line why (Effort, Impact)`.
- **Cheap feature wins · free deletes (verified-dead code) · bigger-but-grounded.**
- An explicit **"NOT a quick win"** list — so nothing gets mis-scoped later.

### 4. Per item: verify-then-decide (before any code)
- **Audit ratings are hypotheses.** Trace the real code path (dispatch an agent), confirm the premise, and **re-rate effort honestly** — expect to be wrong on something in nearly every item.
- **Split conflated items** — one audit row often hides two features of very different effort/risk (e.g. delete-undo vs move-undo; single-file vs recursive-folder).
- Decide **verdict-first**: ✅/⚠️/❌ *worth it?* + reasons + a recommendation.
- **`AskUserQuestion` for scope.** Never write code without an explicit scope answer.

### 5. Execute surgically on a dedicated branch
- Branch off `main` and keep it clean — verify the touched files are identical to `main` first so unrelated/feature work doesn't leak in.
- **One surgical, single-purpose commit per item** — smallest footprint, **match existing patterns**; extra cleverness is a defect ("clean and surgical").
- Verify each: `tsc --noEmit` + formatter + a grep for dangling refs → green.
- **Pause for the user** before committing more or pushing; never push without a go-ahead. Don't fabricate a ticket — use a plain message if none exists.

## Red flags — STOP

- Trusting the audit's effort/impact without tracing the real code (premise unverified).
- A "quick win" that **adds surface area without removing any** (the consolidation trap).
- Gold-plating / not matching existing patterns — re-do it surgically.
- Shipping a feature that *looks* like it works but silently drops data — defer it.
- Skipping the prior-audit read → re-walking solved ground.
- An item that re-rates to M/L on inspection → it's deferred, not a quick win.

## Templates

**Audit doc:** `Tier-0 bugs (B1…)` · `Quick wins (numbered: name — why (Effort, Impact))` · `Cheap features` · `Free deletes` · `Bigger-but-grounded` · `NOT a quick win`.
**Per-item verdict:** **✅/❌ Worth it?** → reasons → recommendation → `AskUserQuestion(scope)`.
**Quick-win commit:** one item · surgical · matches existing patterns · `tsc --noEmit` + formatter green.
