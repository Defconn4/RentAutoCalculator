import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import login credentials (Ensure login_info.py exists)
try:
    from login_info import LOGIN_URL, EMAIL, PASSWORD
except ImportError:
    raise Exception(
        "Error: 'login_info.py' is missing. Please create it with your credentials.")


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Tell Selenium where the Chromium binary is located.
    chrome_options.binary_location = os.path.join(
        os.getcwd(), "headless-chromium")

    driver = webdriver.Chrome()
    return driver


def lambda_handler(event, context):
    try:
        driver = get_driver()

        # wait up to 20 seconds for elements to appear
        wait = WebDriverWait(driver, 20)

        # 1. Navigate to the initial login page
        driver.get(LOGIN_URL)
        print("\n(1) Navigated to login page\n")

        # 2. Enter the email on the initial login page (if required)
        # (You may need to inspect the page to determine the correct locator for the email input.)
        # For example, if the email field has an id "emailInput":
        email_input = wait.until(
            EC.presence_of_element_located((By.ID, "id-form-element-username")))
        email_input.send_keys(EMAIL)

        # 3. Click the "Log in" button
        # (Adjust the locator according to the button’s attributes)
        login_button = driver.find_element(
            By.XPATH, "//button[@type='submit' and span[text()='Log in']]")
        login_button.click()
        print("\n(2) Clicked initial login button\n")

        # 4. Wait for the redirect to the authorization page.
        # The page might redirect automatically to the OAuth endpoint.
        # You might wait for a specific element to appear on the next page.
        # (For example, wait for an input field for username or password.)
        # If the next page loads a form for RealPage login:

        wait = WebDriverWait(driver, 5)

        password_field = driver.find_element(By.ID, "password-input")
        password_field.clear()
        password_field.send_keys(PASSWORD)

        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.ID, "password-input")))

        # 5. Click the login/submit button on the RealPage login form
        # (Again, adjust the locator as needed)
        submit_button = driver.find_element(By.ID, "submit_form_btn")
        submit_button.click()
        print("\n(3) Submitted RealPage credentials\n")

        # 6. Allow time for redirection and additional authentication steps.
        # Depending on the flow, you may need to wait for several redirects.
        # You can wait until the URL indicates you are on the resident dashboard.
        wait.until(EC.url_contains("/portal/resident-dashboard"))
        print("\n(4) Reached resident dashboard\n")

        # 7. Now, find the "Current Balance" element on the dashboard.
        # You will need to inspect the resident-dashboard page to determine a reliable locator.
        # For example, if the current balance appears in an element with id "currentBalance":
        current_balance_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='balance']//span")))

        current_balance = current_balance_element.text
        print("\n\nCurrent Balance:", current_balance)

        # Optionally, do something with the scraped current_balance (e.g., store it, pass it to your Lambda logic, etc.)

    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        driver.quit()


# Get the current balance
lambda_handler(None, None)
