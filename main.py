from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os
import random
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from supabase import create_client, Client
load_dotenv()


app = Flask(__name__)

## Amazon API Key logic

api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
reg_headers = {
    "Authorization": f"sso-key {api_key}:{api_secret}",
    "accept": "application/json"
}

## Supabase API Key Logic

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

## Google Sign-in logic

def googlelogin():
    
data = supabase.auth.sign_in_with_oauth({
  "provider": 'google,
  "options": {
    "redirect_to": 'https://example.com/welcome'
  }
})


## Domain Availability Logic

def get_reg_url(check_domain):
    return f"https://api.godaddy.com/v1/domains/available?domain={check_domain}&checkType=FULL&forTransfer=false"

def check_domain_available(check_domain):
    reg_url = get_reg_url(check_domain)
    req = requests.get(reg_url, headers=reg_headers)

    if req.status_code != 200:
        return {"message": "Could not complete the request"}, 500

    response = req.json()
    if response["available"]:
        return {"message": f"Domain {check_domain} is available!"}, 200
    else:
        return {"message": f"Domain {check_domain} is not available"}, 200


## Business Name Availability Logic

def simulate_typing(driver, element, text):
    for char in text:
        ActionChains(driver).send_keys_to_element(element, char).perform()
        time.sleep(random.uniform(0.1, 0.2))

def solve_captcha(driver):
    # Check if the "I'm not a robot" captcha is present on the page
    if "i'm not a robot" in driver.page_source.lower():
        # Find the captcha checkbox element
        captcha_checkbox = driver.find_element(By.XPATH, '//span[@aria-checked="false"]')

        # Scroll into view to interact with the captcha checkbox
        driver.execute_script("arguments[0].scrollIntoView(true);", captcha_checkbox)
        time.sleep(random.uniform(0.5, 1))

        # Click the captcha checkbox to mark it as checked
        captcha_checkbox.click()
        time.sleep(random.uniform(0.5, 1))
        return True
    return False

def check_business_name_availability(driver):
    try:
        # Wait for the element to load on the page
        time.sleep(3)
        # Check if the element is present on the page
        driver.find_element(By.XPATH, '/html/body/div[4]/form/div/section/div/div/div/section/div/div[2]/ul/li')
        return {"message": "Business Name available"}
    except NoSuchElementException:
        return {"message": "Business Name Not Available"}


def custom_wait(driver, timeout, method, locator):
    return WebDriverWait(driver, timeout).until(method(locator))


def get_driver():
    user_data_dir = "/var/folders/7h/mfz36wt95qs6cgvsgn14k7tw0000gn/T/tmp0x0ug69f"  # Replace with your desired path
    # List of user agent strings to randomly choose from
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        # Add more user agents if desired
    ]
    # Use the undetected_chromedriver to set up the Chrome options
    options = uc.ChromeOptions()
    # Randomly select a user agent string
    options.add_argument(f"--user-agent={random.choice(user_agents)}")
    # Use the desired user data directory
    options.add_argument(f"--user-data-dir={user_data_dir}")
    # Set up the undetected_chromedriver instance
    driver = uc.Chrome(options=options)
    return driver

## App Routes Logic

@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/checkdomain", methods=["POST"])
def check_domain_route():
    domain_name = request.form.get("domain_name")
    if not domain_name:
        return {"message": "Domain name is required"}, 400

    result, status_code = check_domain_available(domain_name)
    return jsonify(result), status_code


@app.route("/checkbusiness", methods=["GET", "POST"])
def checkbusiness():
    if request.method == "POST":
        business_name = request.form.get("business_name")
        if not business_name:
            return {"message": "Business name is required"}, 400

        # Use try-except to handle any exceptions raised during the process
        try:
            driver = get_driver()
            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True)

            driver.get("https://apps.ilsos.gov/businessentitysearch/")

            # Wait for the page to load
            custom_wait(driver, 5, EC.presence_of_element_located, (By.XPATH, '//*[@id="name"]'))

            # Click the "Name" checkbox
            name_checkbox = driver.find_element(By.XPATH, '//*[@id="name"]')
            name_checkbox.click()

            # Fill the search input with the provided business name
            search_input = driver.find_element(By.ID, "searchValue")
            search_input.clear()  # Clear any existing text
            simulate_typing(driver, search_input, business_name)

            # Wait for the page to load after filling the input
            custom_wait(driver, 10, EC.presence_of_element_located, (By.XPATH, '//*[@id="report-corp"]/div/div[3]/div/div/input'))

            # Emulate a human-like typing speed
            time.sleep(random.uniform(1.4, 1.5))

            # Click the "Submit" button
            submit_button = driver.find_element(By.XPATH, '//*[@id="report-corp"]/div/div[3]/div/div/input')
            submit_button.click()

            # Check for captcha and solve it
            captcha_solved = solve_captcha(driver)

            if captcha_solved:
                print("Captcha solved")
            else:
                print("No captcha")

            # Scroll to simulate human interaction
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #time.sleep(random.uniform(1, 2))

            # Scroll back up
            driver.execute_script("window.scrollTo(0, 0);")
            #time.sleep(random.uniform(1, 2))

            # Check for business name availability
            availability_result = check_business_name_availability(driver)

            # Simulate navigating back
            driver.back()

            # Display the availability result on the same page
            return jsonify(availability_result), 200

        except Exception as e:
            # Handle any exceptions and return an error message
            return {"message": "An error occurred while checking business name availability.", "error": str(e)}, 500

        finally:
            # Close the browser when done
            driver.quit()
    
    return render_template("checkbusiness.html")


if __name__ == '__main__':
    app.run()

