# Changelog

## v1.0.0

- Removed the obsolete `continuous-chat-loop` skill (major bump).
- Every skill now belongs to a bundle — no more root-only skills:
  - `set-output-style` → `harness-evolution`.
  - `formal-verification`, `functional-programming`, `site-refiner` →
    `delivery-lifecycle`.

## v0.1.0

- Initial release of the Evolving Harness framework.
- New `using-evolving-harness` router skill: routes non-trivial tasks through
  the gated lifecycle and runs the session-end evolution loop.
- Four plugin bundles generated from `bundles.json`: `harness-evolution`,
  `delivery-lifecycle`, `git-ops`, `thinking`.
- Plugin marketplace `evolving-harness` (`.claude-plugin/marketplace.json`).
- SessionStart hook nudging the router in the `harness-evolution` bundle.
- `scripts/generate_bundles.py` (bundle generator) and
  `scripts/bump_version.py` (release helper); CI validation workflow.
- The flat root catalog remains unchanged and `npx skills add Harduex/skills`
  keeps working.
