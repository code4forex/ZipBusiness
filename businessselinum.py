import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run():
    user_data_dir = "/var/folders/7h/mfz36wt95qs6cgvsgn14k7tw0000gn/T/tmp0x0ug69f"  # Replace with your desired path

    # List of user agent strings to randomly choose from
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        # Add more user agents if desired
    ]

    chrome_options = webdriver.ChromeOptions()

    # Randomly select a user agent string
    chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")

    # Use the desired user data directory
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    # Launch Chrome with the custom options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://apps.ilsos.gov/businessentitysearch/")

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="name"]')))

        # Click the "Name" checkbox
        name_checkbox = driver.find_element(By.XPATH, '//*[@id="name"]')
        name_checkbox.click()

        # Fill the search input with "brainfuseaii"
        search_input = driver.find_element(By.ID, "searchValue")
        search_input.click()
        search_input.clear()
        search_input.send_keys("brainfuseaii")

        # Wait for the page to load after filling the input
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="report-corp"]/div/div[3]/div/div/input')))

        # Emulate a human-like typing speed
        time.sleep(random.uniform(0.5, 1.5))

        # Click the "Submit" button
        submit_button = driver.find_element(By.XPATH, '//*[@id="report-corp"]/div/div[3]/div/div/input')
        submit_button.click()

        # Wait for the results to appear on the next page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "results")))

        # Scroll to simulate human interaction
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1, 2))

        # Scroll back up
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1, 2))

        # Now you can interact with elements on the results page
        # For example, you can find elements and retrieve their content
        results = driver.find_elements(By.CSS_SELECTOR, ".searchResults")
        for result in results:
            print(result.text)

        # You can also interact with other elements on the page as needed
        # ...

        # Simulate navigating back
        driver.back()
        time.sleep(random.uniform(1, 2))

    finally:
        # Close the browser when done
        driver.quit()

if __name__ == "__main__":
    run()
