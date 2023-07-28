from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run():
    user_data_dir = "/var/folders/7h/mfz36wt95qs6cgvsgn14k7tw0000gn/T/tmp0x0ug69f"  # Replace with your desired path

    # Set custom user agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--user-agent={user_agent}")

    # Use the desired user data directory
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    # Launch Chrome with the custom options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://apps.ilsos.gov/businessentitysearch/")

        # Wait for the page to load
        time.sleep(2)

        # Click the "Name" checkbox
        name_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="name"]')))
        name_checkbox.click()

        # Wait for the page to load after clicking the checkbox
        time.sleep(2)

        # Fill the search input with "brainfuseaii"
        search_input = driver.find_element(By.ID, "searchValue")
        search_input.click()
        search_input.clear()
        search_input.send_keys("brainfuseaii")

        # Wait for the page to load after filling the input
        time.sleep(2)

        # Click the "Submit" button
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="report-corp"]/div/div[3]/div/div/input')))
        submit_button.click()

        # Wait for the results to appear on the next page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "results")))

        # Now you can interact with elements on the results page
        # For example, you can find elements and retrieve their content
        results = driver.find_elements(By.CSS_SELECTOR, ".searchResults")
        for result in results:
            print(result.text)

        # You can also interact with other elements on the page as needed
        # ...

    finally:
        # Close the browser when done
        driver.quit()

if __name__ == "__main__":
    run()
