# Live Lab navigation and dark-mode repair

Date: 12 November 2026. Applied to both `demo/` and `FINAL_PROJECT_MAIN/demo/application/demo/`.

## Navigation

The final Start Here walkthrough button previously changed the routing state but left the sidebar radio on Start Here; the next run restored that stale sidebar value. The button now uses a pre-render callback that synchronizes the workspace, sidebar widget and query parameter. The sidebar radio is initialized from state without a competing explicit default.

## Reader-answer readability

The HTML original/removal answer cards previously combined inherited light text with a pale background fallback. Cards now inherit the active foreground and use a subtle translucent background. Score labels inherit the foreground too. Wrapped text, responsive columns, escaped HTML, answer content and score values are unchanged.

## Verification

- Original demo: **193 tests passed**.
- Copied demo, independently run: **193 tests passed**.
- Actual dark Streamlit browser checks: Start Here stage 5 → Open Live Lab succeeds in both applications; sidebar selection and URL agree.
- Answer renderer in the actual dark theme: text `rgb(250,250,250)` on the translucent card over `rgb(14,17,23)`; measured contrast approximately **16.24:1**, no horizontal overflow. Light-parent inheritance also verified.
- Browser answer examples are layout fixtures, not new reader generations. No weights or GPU models loaded; no research run executed.
- Original 15-passage preset, scoring, algorithms, thresholds, research artifacts and saved generations unchanged.

Screenshots and computed color checks: `demo/artifacts/navigation_theme/`. The copied payload checksum manifest is updated for this authorized patch.
