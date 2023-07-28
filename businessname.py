from playwright.sync_api import Playwright, sync_playwright, expect
import time

def run(playwright: Playwright) -> None:
    user_data_dir = "/var/folders/7h/mfz36wt95qs6cgvsgn14k7tw0000gn/T/tmp0x0ug69f"  # Replace with your desired path
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"

    browser = playwright.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        args=[f"--user-agent={user_agent}"]
    )
    context = browser.new_page()  # Create a new page within the persistent context
    context.goto("https://apps.ilsos.gov/businessentitysearch/")
    context.wait_for_load_state("networkidle")
    context.check('label:has-text("Name")')
    context.click("#searchValue")
    context.wait_for_load_state("networkidle")
    context.fill("#searchValue", "brainfuseaii")
    context.wait_for_load_state("networkidle")
    context.click('button:has-text("Submit")')

    time.sleep(4)
    # ---------------------
    ##context.close()
    ##browser.close()

with sync_playwright() as playwright:
    run(playwright)
