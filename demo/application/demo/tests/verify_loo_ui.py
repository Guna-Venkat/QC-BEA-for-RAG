"""Verification script for Evidence Lab 2.0 LOO Evidence Impact Analysis Transparency.

Verifies the 5 numbered sections in Before/After Answer Inspector via Playwright,
checks that no raw HTML leaked, and captures verification screenshots.
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = ROOT / "demo" / "artifacts" / "redesigned_ui"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
CONV_ARTIFACTS_DIR = Path("/home/gunavenkat/.gemini/antigravity-ide/brain/bfa8110a-6f4e-4ed8-a333-04737cbe2b10")

URL = "http://localhost:8501/?workspace=Live+Lab"


def wait_for_streamlit(page, timeout=30000):
    page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=timeout)
    time.sleep(1.5)


def check_no_raw_html(page, context_name=""):
    body_text = page.locator("body").inner_text()
    for leaked_pattern in ["<div style=", "<p style=", "<span style=", "<div class="]:
        if leaked_pattern in body_text:
            raise AssertionError(f"Leaked raw HTML tag '{leaked_pattern}' found during {context_name}")
    print(f"✓ No raw HTML leaked in {context_name}")


def main():
    print("Launching browser for LOO transparency verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 1600})
        page = context.new_page()

        print(f"Navigating to {URL}...")
        page.goto(URL)
        wait_for_streamlit(page)

        # Confirm Live Lab loaded
        body = page.locator("body").inner_text()
        assert "Live Lab" in body, "Expected Live Lab workspace header"
        print("✓ Live Lab workspace loaded successfully")

        # Fill in Reference Answer
        print("Filling reference answer for LOO analysis...")
        ref_input = page.locator('textarea[aria-label*="Reference Answer"]')
        ref_text = "The 2026 World Cup expanded to 48 teams with 12 groups of 4. Format changed to prevent collusion."
        ref_input.fill(ref_text)
        ref_input.press("Tab")
        time.sleep(1)

        # Select GPU device if available
        sb = page.locator('[data-testid="stSelectbox"]').filter(has_text="Execution Device")
        if sb.count() > 0:
            box = sb.locator("input")
            box.click()
            page.wait_for_timeout(400)
            opt = page.locator('[role="option"]').filter(has_text="GPU")
            if opt.count() > 0:
                opt.first.click()
                wait_for_streamlit(page)

        # Enable Live Models for reader inference
        print("Enabling Live Models toggle...")
        toggle_label = page.locator('[data-testid="stCheckbox"]').filter(has_text="Enable Live Models").locator("label")
        toggle_label.click()
        wait_for_streamlit(page)

        # Run Compare Four Methods
        print("Clicking 'Compare Four Methods' with Live Models enabled...")
        cmp_btn = page.locator('button:has-text("Compare Four Methods")').first
        cmp_btn.click()
        page.wait_for_selector('h3:has-text("Four-Method Evidence Allocation Comparison")', timeout=180000)
        wait_for_streamlit(page, timeout=60000)

        body_after_cmp = page.locator("body").inner_text()
        assert "Best Sentences" in body_after_cmp
        assert "QBGF" in body_after_cmp
        assert "BEA-V1" in body_after_cmp
        assert "BEA-V2" in body_after_cmp
        print("✓ Compare Four Methods completed successfully")

        # Run Analyze Evidence Impact
        print("Clicking 'Analyze Evidence Impact'...")
        impact_btn = page.locator('button:has-text("Analyze Evidence Impact")').first
        impact_btn.click()
        # Wait for LOO inspector section
        page.wait_for_selector('h4:has-text("Before / After Answer Comparison")', timeout=180000)
        time.sleep(2)

        impact_body = page.locator("body").inner_text()
        assert "Evidence Impact Analysis" in impact_body
        assert "Before / After Answer Comparison" in impact_body
        assert "Selected Method:" in impact_body
        assert "① Original Evidence Sent to Reader" in impact_body
        assert "② Removed Evidence" in impact_body
        assert "③ Evidence Sent to Reader After Removal" in impact_body
        assert "④ Reader Answers" in impact_body
        assert "⑤ Evidence Impact" in impact_body
        assert "Remaining evidence tokens" in impact_body
        assert "View Complete Remaining Evidence" in impact_body
        assert "View Exact Serialized Evidence" in impact_body

        print("✓ All 5 numbered transparency sections successfully verified in DOM:")
        print("  - ① Original Evidence Sent to Reader")
        print("  - ② Removed Evidence")
        print("  - ③ Evidence Sent to Reader After Removal (with Remaining evidence tokens)")
        print("  - ④ Reader Answers (side-by-side columns)")
        print("  - ⑤ Evidence Impact (metric delta & classification)")

        check_no_raw_html(page, "LOO Before/After Inspector")

        # Scroll inspector into view
        inspector = page.locator('h4:has-text("Before / After Answer Comparison")')
        inspector.scroll_into_view_if_needed()
        time.sleep(1)

        # Capture upper inspector view
        shot_path_1 = ARTIFACTS_DIR / "08_live_lab_impact_analysis_completed.png"
        page.screenshot(path=str(shot_path_1))
        print(f"Captured screenshot: {shot_path_1}")

        # Scroll to Section ③ to capture ②, ③, ④, ⑤ in full detail
        sec3 = page.locator('h3:has-text("③ Evidence Sent to Reader After Removal")')
        sec3.scroll_into_view_if_needed()
        time.sleep(1)

        shot_path_2 = ARTIFACTS_DIR / "loo_transparency_inspector.png"
        page.screenshot(path=str(shot_path_2))
        print(f"Captured screenshot: {shot_path_2}")

        # Scroll to Section ④ to capture Answers and Impact
        sec4 = page.locator('h3:has-text("④ Reader Answers")')
        sec4.scroll_into_view_if_needed()
        time.sleep(1)
        shot_path_3 = ARTIFACTS_DIR / "loo_transparency_answers.png"
        page.screenshot(path=str(shot_path_3))

        if CONV_ARTIFACTS_DIR.exists():
            import shutil
            conv_shot_1 = CONV_ARTIFACTS_DIR / "loo_transparency_inspector.png"
            shutil.copy2(shot_path_1, conv_shot_1)
            conv_shot_2 = CONV_ARTIFACTS_DIR / "loo_transparency_inspector_lower.png"
            shutil.copy2(shot_path_2, conv_shot_2)
            conv_shot_3 = CONV_ARTIFACTS_DIR / "loo_transparency_inspector_answers.png"
            shutil.copy2(shot_path_3, conv_shot_3)
            print(f"Copied verification screenshots to conversation artifacts: {conv_shot_1}, {conv_shot_2}, {conv_shot_3}")

        browser.close()
        print("\n=== All LOO transparency browser verification checks passed! ===\n")


if __name__ == "__main__":
    main()
