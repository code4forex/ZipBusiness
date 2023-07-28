from playwright.sync_api import Playwright, sync_playwright, expect
import time
import os
import shutil


def get_proxy_info():
    proxy_server = os.getenv('PROXY_SERVER')
    proxy_username = os.getenv('PROXY_USERNAME')
    proxy_password = os.getenv('PROXY_PASSWORD')
    
    if proxy_server and proxy_username and proxy_password:
        return {
            'server': f'http://{proxy_username}:{proxy_password}@{proxy_server}',
        }
    else:
        return None

def run(playwright: sync_playwright) -> None:
    user_data_dir = "/var/folders/7h/mfz36wt95qs6cgvsgn14k7tw0000gn/T/tmp0x0ug69f"
    shutil.rmtree(user_data_dir, ignore_errors=True)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"

    # Set proxy information
    proxy = get_proxy_info()

    browser = playwright.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        args=[f"--user-agent={user_agent}"],
        proxy=proxy 
    )


    context = browser.new_page()  # Create a new page within the persistent context
    context.goto("https://apps.ilsos.gov/businessentitysearch/")
    context.wait_for_load_state("networkidle")
    context.check('label:has-text("Name")')
    context.click("#searchValue")
    context.wait_for_load_state("networkidle")
    context.fill("#searchValue", "brainfuseaii")
    time.sleep(2)

    # Use JavaScript to click the button
    context.evaluate('''() => {
        const submitButton = document.querySelector("#report-corp > div > div.cta > div > div > input");
        submitButton.click();
    }''')

    time.sleep(4)
    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
