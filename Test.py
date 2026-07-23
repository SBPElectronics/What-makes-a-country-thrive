import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# -----------------------
# Load Environment Variables
# ----------------------
load_dotenv()

email = "user"
password = "pass"

if not email or not password:
    raise Exception("Email or Password not set in environment variables")

# -----------------------
# Chrome Setup
# -----------------------
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 30)

try:
    driver.get("https://outlook.office.com/mail/")

    # -----------------------
    # STEP 1: Enter Email
    # -----------------------
    email_input = wait.until(
        EC.visibility_of_element_located((By.ID, "i0116"))
    )
    email_input.clear()
    email_input.send_keys(email)
    driver.find_element(By.ID, "idSIButton9").click()

    print("Email entered.")

    # -----------------------
    # STEP 2: Enter Password
    # -----------------------
    password_input = wait.until(
        EC.visibility_of_element_located((By.ID, "i0118"))
    )
    password_input.clear()
    password_input.send_keys(password)
    driver.find_element(By.ID, "idSIButton9").click()

    print("Password entered.")

    # -----------------------
    # STEP 3: Handle Stay Signed In (if appears)
    # -----------------------
    try:
        stay_signed_in = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "idSIButton9"))
        )
        stay_signed_in.click()
        print("Handled Stay signed in.")
    except:
        print("No Stay signed in prompt.")

    # -----------------------
    # STEP 4: Wait for Outlook UI to fully load
    # Wait for "New mail" button instead of generic div
    # -----------------------
    new_mail_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@aria-label='New mail']")
        )
    )

    print("Inbox fully loaded.")
    webdriver.ActionChains(driver).send_keys("n").perform()
    time.sleep(100)

except Exception as e:
    print("Something went wrong:", e)

finally:
    print("Done.")
