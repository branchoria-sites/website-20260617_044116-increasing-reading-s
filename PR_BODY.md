## Summary

The [2026-09-30 estate page-weight census](https://github.com/isaackoi/Phoenix-Alpha-workbench/issues/4439) measured this home document at **407,871 B decoded** with the inline `<script type="application/json" data-home-vertical-data>` blob carrying **396,460 B (97.2%)**. The blob is a generated home-cluster build artifact, not editorial content.

This PR moves it to a same-origin static asset and keeps the rendered diagram identical:

- **index.md** 407,871 → 11,471 B; the inline blob is replaced by the empty placeholder shape plus `data-home-vertical-src="/assets/js/home-vertical-data.json"`.
- **assets/js/home-vertical-data.json** (new, 385,328 B): the blob with every `{{ 'path' | relative_url }}` Liquid form rendered to the exact URL Jekyll emits (same transform verified 171/171 nodes / 0 mismatches against the live Jekyll output on the ai-doom carrier).
- **assets/js/page-enhancements.js**: `initHomeVerticalView` now fetches the asset when the inline node ships empty (fetch with XHR fallback, `credentials: same-origin`); inline payloads keep the previous synchronous path; fetch failure falls back to today's empty behavior (tree hidden). Node syntax checked; the refactor shape is proven on the ai-doom carrier (PR #1 on website-20260805_094416-ai-doom-existential) with DOM-stubbed path tests.
- **_config.yml**: `ui_bundle_version` bumped for asset cache-busting.

Projected effect (census share method): home document ≈11,411 B decoded (−97.2%). Zero editorial content touched; zero deploy actions in the producing session.

Part of the estate template page-weight trim work item (alpha-production:estate-template-page-weight-trim:v1, #4439 P0 production quality).