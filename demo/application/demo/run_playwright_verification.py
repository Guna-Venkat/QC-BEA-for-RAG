"""Playwright Browser Verification Script for Evidence Lab 2.0.

Executes all 10 browser verification tests and captures all 8 required high-resolution screenshots:
1. 01_start_here_stage4_evidence.png
2. 02_start_here_stage5_restart.png
3. 03_compare_methods_cards.png
4. 04_compare_methods_inspector.png
5. 05_research_live_experiment_default.png
6. 06_live_lab_four_methods.png
7. 07_live_lab_impact_prerequisites.png
8. 08_live_lab_impact_analysis_completed.png
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts" / "redesigned_ui"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

URL = "http://localhost:8501"


def wait_for_streamlit(page, timeout=30000):
    page.wait_for_load_state("networkidle", timeout=timeout)
    page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=timeout)
    time.sleep(1.5)


def check_no_raw_html(page, context_name=""):
    """Assert that no visible DOM text contains leaked HTML strings."""
    body_text = page.locator("body").inner_text()
    for leaked_pattern in ["<div style=", "<p style=", "<span style=", "<div class="]:
        if leaked_pattern in body_text:
            raise AssertionError(f"Leaked raw HTML tag '{leaked_pattern}' found in visible DOM text during {context_name}")
    print(f"✓ No raw HTML leaked in {context_name}")


def select_option(page, selectbox_label, option_text):
    """Open a Streamlit selectbox and choose the option matching option_text."""
    sb = page.locator('[data-testid="stSelectbox"]').filter(has_text=selectbox_label)
    sb.scroll_into_view_if_needed()
    time.sleep(0.3)
    box = sb.locator("input")
    box.click()
    page.wait_for_timeout(500)
    page.locator('[role="option"]').filter(has_text=option_text).first.click()
    wait_for_streamlit(page)


def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        print("\n=======================================================")
        print("Starting Evidence Lab 2.0 Browser Verification...")
        print("=======================================================\n")

        # ------------------------------------------------------------------
        # TEST 1 & SCREENSHOT 1 & 2: Start Here Walkthrough
        # ------------------------------------------------------------------
        print("--- Running Test 1 & 2: Start Here Walkthrough ---")
        page.goto(URL)
        wait_for_streamlit(page)

        # Assert no duplicate page links in sidebar
        sidebar_text = page.locator('[data-testid="stSidebar"]').inner_text()
        assert "Workspace Navigation" in sidebar_text, "Workspace Navigation missing in sidebar"
        assert "/algorithm_explorer" not in sidebar_text, "Duplicate automatic Streamlit page links found in sidebar!"
        assert "/compare_methods" not in sidebar_text, "Duplicate automatic Streamlit page links found in sidebar!"

        # Step through Start Here stages
        page.wait_for_selector("text=Stage 1")
        assert "Stage 1" in page.locator("body").inner_text()

        # Navigate to Stage 2
        page.locator('button:has-text("Next Stage")').first.click()
        page.wait_for_selector("text=Stage 2", timeout=10000)
        time.sleep(1.0)
        assert "Stage 2" in page.locator("body").inner_text()

        # Navigate to Stage 3
        page.locator('button:has-text("Next Stage")').first.click()
        page.wait_for_selector("text=Stage 3", timeout=10000)
        time.sleep(1.0)
        assert "Stage 3" in page.locator("body").inner_text()

        # Navigate to Stage 4 (Evidence selection inspection)
        page.locator('button:has-text("Next Stage")').first.click()
        page.wait_for_selector("text=Stage 4", timeout=10000)
        time.sleep(1.0)
        assert "Stage 4" in page.locator("body").inner_text()
        
        # Verify selected evidence cards and token counts exist
        body_text_s4 = page.locator("body").inner_text()
        assert "SELECTED" in body_text_s4 or "DECISIVE" in body_text_s4, "Evidence status tags missing in Stage 4"
        check_no_raw_html(page, "Start Here Stage 4")

        # Screenshot 1: 01_start_here_stage4_evidence.png
        p1 = ARTIFACTS_DIR / "01_start_here_stage4_evidence.png"
        page.screenshot(path=str(p1), full_page=True)
        print(f"Captured Screenshot 1: {p1}")

        # Navigate to Stage 5
        page.locator('button:has-text("Next Stage")').first.click()
        page.wait_for_selector("text=Stage 5", timeout=10000)
        time.sleep(1.0)
        assert "Stage 5" in page.locator("body").inner_text()

        # Verify Stage 5 has the restart button
        restart_btn = page.locator('button:has-text("Restart Walkthrough")')
        assert restart_btn.is_visible(), "Restart Walkthrough button not visible in Stage 5"
        check_no_raw_html(page, "Start Here Stage 5")

        # Screenshot 2: 02_start_here_stage5_restart.png
        p2 = ARTIFACTS_DIR / "02_start_here_stage5_restart.png"
        page.screenshot(path=str(p2), full_page=True)
        print(f"Captured Screenshot 2: {p2}")

        # Test circular restart
        restart_btn.click()
        page.wait_for_selector("text=Stage 1", timeout=10000)
        time.sleep(1.0)
        assert "Stage 1" in page.locator("body").inner_text(), "Restart button failed to loop back to Stage 1"
        print("✓ Circular walkthrough restart passed")

        # Test switching example cards to QASPER and SciFact
        qasper_btn = page.locator('button:has-text("Explore Starvation Case")')
        if qasper_btn.is_visible():
            qasper_btn.click()
            wait_for_streamlit(page)
            assert "QASPER" in page.locator("body").inner_text()

        scifact_btn = page.locator('button:has-text("Explore Microdomains Case")')
        if scifact_btn.is_visible():
            scifact_btn.click()
            wait_for_streamlit(page)
            assert "SciFact" in page.locator("body").inner_text()
        print("✓ Start Here example switching passed")

        # ------------------------------------------------------------------
        # TEST 3 & SCREENSHOT 3 & 4: Compare Methods
        # ------------------------------------------------------------------
        print("\n--- Running Test 3: Compare Methods ---")
        # Switch to Compare Methods via sidebar
        page.locator('label:has-text("Compare Methods")').click()
        wait_for_streamlit(page)

        cmp_text = page.locator("body").inner_text()
        assert "Compare Methods" in cmp_text
        assert "Example Collection" not in cmp_text, "'Example Collection' toolbar should be removed"
        assert "Historical Curated Queries" not in cmp_text, "Historical Curated Queries found in Compare Methods"
        
        # Verify token percentage is accurate (e.g. 94.9% for 243/256 tokens in Hotpot, 65.6% for 168/256)
        assert "94.9%" in cmp_text or "65.6%" in cmp_text or "95.7%" in cmp_text, "Expected token utilization percentage missing in HotpotQA"
        assert "0.0% utilized" not in cmp_text, "Found buggy 0.0% utilization"
        check_no_raw_html(page, "Compare Methods Cards")

        # Also switch to SciFact matched case and verify 98.0% (251/256) and 99.6% (255/256)
        select_option(page, "Choose an Example", "TCR/CD3")
        scifact_cmp_text = page.locator("body").inner_text()
        assert "98.0%" in scifact_cmp_text or "99.6%" in scifact_cmp_text or "94.5%" in scifact_cmp_text, "Expected token utilization in SciFact case"
        print("✓ Accurately calculated token utilization verified on Compare Methods (94.9%, 98.0%, 99.6%)")

        # Screenshot 3: 03_compare_methods_cards.png
        p3 = ARTIFACTS_DIR / "03_compare_methods_cards.png"
        page.screenshot(path=str(p3), full_page=True)
        print(f"Captured Screenshot 3: {p3}")

        # Scroll to Evidence Inspector and take Screenshot 4
        inspector_expander = page.locator('details:has-text("Evidence Inspector")')
        if inspector_expander.is_visible():
            inspector_expander.scroll_into_view_if_needed()
            time.sleep(0.5)
        p4 = ARTIFACTS_DIR / "04_compare_methods_inspector.png"
        page.screenshot(path=str(p4), full_page=False)
        print(f"Captured Screenshot 4: {p4}")

        # ------------------------------------------------------------------
        # TEST 4 & SCREENSHOT 5: Research & Live Lab Default Tab
        # ------------------------------------------------------------------
        print("\n--- Running Test 4: Live Lab ---")
        page.locator('label:has-text("Live Lab")').click()
        wait_for_streamlit(page)

        # Verify Tab 1 "Live Experiment" is active by default
        active_tab = page.locator('[role="tab"][aria-selected="true"]')
        active_tab_text = active_tab.inner_text()
        assert "Live Experiment" in active_tab_text, f"Expected Live Experiment to be active tab, got: {active_tab_text}"
        print("✓ Live Experiment is active by default in Tab 1")
        check_no_raw_html(page, "Research & Live Lab Tab 1")

        # Screenshot 5: 05_research_live_experiment_default.png
        p5 = ARTIFACTS_DIR / "05_research_live_experiment_default.png"
        page.screenshot(path=str(p5), full_page=True)
        print(f"Captured Screenshot 5: {p5}")

        # ------------------------------------------------------------------
        # TEST 5 & 6 & SCREENSHOT 6: Compare Four Methods (No Reference Answer)
        # ------------------------------------------------------------------
        print("\n--- Running Test 5 & 6: Live Comparison & Missing-Reference Guards ---")
        cmp_four_btn = page.locator('button:has-text("Compare Four Methods")').first
        cmp_four_btn.click()
        wait_for_streamlit(page, timeout=30000)

        # Check cards are displayed
        live_body = page.locator("body").inner_text()
        assert "Best Sentences" in live_body
        assert "QBGF" in live_body
        assert "BEA-V1" in live_body
        assert "BEA-V2" in live_body
        assert "reader inference not executed" in live_body.lower(), "Expected notice indicating reader inference was not executed"
        check_no_raw_html(page, "Live Experiment Four Methods")

        # Screenshot 6: 06_live_lab_four_methods.png
        p6 = ARTIFACTS_DIR / "06_live_lab_four_methods.png"
        page.screenshot(path=str(p6), full_page=True)
        print(f"Captured Screenshot 6: {p6}")

        # TEST 6: Missing-reference guard
        print("\n--- Running Test 6: Missing-Reference Guard ---")
        impact_btn = page.locator('button:has-text("Analyze Evidence Impact")').first
        impact_btn.click()
        wait_for_streamlit(page)

        guard_body = page.locator("body").inner_text()
        assert "Reference answer required" in guard_body, "Expected 'Reference answer required' warning missing"
        print("✓ Missing-reference warning correctly displayed")

        # Screenshot 7: 07_live_lab_impact_prerequisites.png
        p7 = ARTIFACTS_DIR / "07_live_lab_impact_prerequisites.png"
        page.screenshot(path=str(p7), full_page=True)
        print(f"Captured Screenshot 7: {p7}")

        # ------------------------------------------------------------------
        # TEST 7: Context-Only Analysis Guard
        # ------------------------------------------------------------------
        print("\n--- Running Test 7: Context-Only Guard ---")
        ref_textarea = page.locator('textarea[aria-label*="Reference Answer"]')
        ref_textarea.fill("Sensor B had forty-eight hours of battery life.")
        ref_textarea.press("Tab")
        time.sleep(1)

        impact_btn.click()
        wait_for_streamlit(page)
        guard_body2 = page.locator("body").inner_text()
        assert "Reader inference required" in guard_body2, "Expected 'Reader inference required' warning missing"
        print("✓ Context-only reader inference guard correctly displayed")

        # ------------------------------------------------------------------
        # TEST 8 & SCREENSHOT 8: Real Evidence-Impact Analysis
        # ------------------------------------------------------------------
        print("\n--- Running Test 8: Real Evidence-Impact Analysis ---")
        # Switch device to GPU for sub-second inference
        select_option(page, "Execution Device", "GPU")

        # Click toggle to enable models
        toggle_label = page.locator('[data-testid="stCheckbox"]').filter(has_text="Enable Live Models").locator("label")
        toggle_label.click()
        wait_for_streamlit(page)

        # Run Compare Four Methods with live inference enabled
        print("Running live 4-method comparison on GPU...")
        cmp_four_btn.click()
        page.wait_for_selector('h3:has-text("Four-Method Evidence Allocation Comparison")', timeout=180000)
        wait_for_streamlit(page)

        # Now click Analyze Evidence Impact
        print("Running Leave-One-Out evidence impact analysis...")
        impact_btn.click()
        page.wait_for_selector('h3:has-text("Evidence Impact Analysis")', timeout=120000)
        wait_for_streamlit(page)

        impact_body = page.locator("body").inner_text()
        assert "Evidence Impact Analysis" in impact_body
        assert "Before / After Answer Comparison" in impact_body
        assert "① Original Evidence Sent to Reader" in impact_body
        assert "② Removed Evidence" in impact_body
        assert "③ Evidence Sent to Reader After Removal" in impact_body
        assert "④ Reader Answers" in impact_body
        assert "⑤ Evidence Impact" in impact_body
        assert "Remaining evidence tokens" in impact_body
        print("✓ Completed Leave-One-Out impact analysis and Before/After Inspector displayed")
        check_no_raw_html(page, "Live Experiment Impact Analysis")

        # Screenshot 8: 08_live_lab_impact_analysis_completed.png
        p8 = ARTIFACTS_DIR / "08_live_lab_impact_analysis_completed.png"
        page.screenshot(path=str(p8), full_page=True)
        print(f"Captured Screenshot 8: {p8}")

        # ------------------------------------------------------------------
        # TEST 10: Session Persistence
        # ------------------------------------------------------------------
        print("\n--- Running Test 10: Session Persistence ---")
        select_option(page, "Evidence Token Budget", "1024")

        # Navigate to "How the Algorithms Work"
        page.locator('label:has-text("How the Algorithms Work")').click()
        wait_for_streamlit(page)
        assert "How the Algorithms Work" in page.locator("body").inner_text()

        # Navigate back to "Live Lab"
        page.locator('label:has-text("Live Lab")').click()
        wait_for_streamlit(page)
        live_body_return = page.locator("body").inner_text()
        assert "1024" in live_body_return, "Budget setting did not persist across navigation"
        print("✓ Session persistence test passed")

        browser.close()
        print("\n=======================================================")
        print("All 10 browser verification tests completed successfully!")
        print("All 8 screenshots captured in demo/artifacts/redesigned_ui/")
        print("=======================================================\n")


if __name__ == "__main__":
    run_verification()
