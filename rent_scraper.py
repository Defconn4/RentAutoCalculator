import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Use the binaries from the AWS Lambda layer (located in /opt/bin)
    chrome_options.binary_location = "/opt/bin/headless-chromium"
    service = Service(executable_path="/opt/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


def get_latest_rent():

    # Retrieve login credentials from AWS Lambda environment variables.
    LOGIN_URL = os.environ.get('LOGIN_URL')
    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')

    try:
        driver = get_driver()
        wait = WebDriverWait(driver, 20)

        # 1. Navigate to the initial login page
        driver.get(LOGIN_URL)
        print("\n(1) Navigated to login page\n")

        # 2. Enter the email on the initial login page
        email_input = wait.until(
            EC.presence_of_element_located((By.ID, "id-form-element-username")))
        email_input.send_keys(EMAIL)

        # 3. Click the "Log in" button
        login_button = driver.find_element(
            By.XPATH, "//button[@type='submit' and span[text()='Log in']]")
        login_button.click()
        print("\n(2) Clicked initial login button\n")

        # 4. Wait for the redirect to the authorization page.
        wait = WebDriverWait(driver, 5)

        password_field = driver.find_element(By.ID, "password-input")
        password_field.clear()
        password_field.send_keys(PASSWORD)

        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.ID, "password-input")))

        # 5. Click the login/submit button on the RealPage login form
        submit_button = driver.find_element(By.ID, "submit_form_btn")
        submit_button.click()
        print("\n(3) Submitted RealPage credentials\n")

        # 6. Allow time for redirection and additional authentication steps.
        wait.until(EC.url_contains("/portal/resident-dashboard"))
        print("\n(4) Reached resident dashboard\n")

        # 7. Now, find the "Current Balance" element on the dashboard.
        current_balance_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='balance']//span")))

        current_balance = current_balance_element.text

        print("\n(5) Found current balance element\n")

        return {"current_balance": float(current_balance.replace('$', '').replace(',', ''))}

    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        driver.quit()


if __name__ == "__main__":
    rent_data = get_latest_rent()
    print(rent_data)
