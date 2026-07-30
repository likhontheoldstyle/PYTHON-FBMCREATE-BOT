from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import time
import string
import chromedriver_autoinstaller
from config import PROXY, HEADLESS, EMAIL_DOMAINS, FB_SIGNUP_URL

chromedriver_autoinstaller.install()

class FacebookCreator:
    def __init__(self):
        self.driver = None
        self.account_data = {}

    def _setup_driver(self):
        options = Options()
        if HEADLESS:
            options.add_argument('--headless')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        width = random.randint(1000, 1400)
        height = random.randint(700, 900)
        options.add_argument(f'--window-size={width},{height}')
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        ]
        options.add_argument(f'user-agent={random.choice(user_agents)}')
        if PROXY:
            options.add_argument(f'--proxy-server={PROXY}')
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def _generate_name(self):
        first = ['John','Emma','Michael','Sophia','James','Olivia','William','Ava','David','Mia']
        last = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Martinez','Robinson']
        return random.choice(first), random.choice(last)

    def _generate_dob(self):
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        year = random.randint(1985, 2005)
        return month, day, year

    def _generate_password(self):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(chars, k=random.randint(12, 16)))

    def _generate_email(self):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 12)))
        domain = random.choice(EMAIL_DOMAINS)
        return f"{username}@{domain}"

    def _generate_phone(self):
        return f"+1{random.randint(200, 999)}{random.randint(1000000, 9999999)}"

    def create_account(self):
        try:
            self._setup_driver()
            wait = WebDriverWait(self.driver, 20)
            self.driver.get(FB_SIGNUP_URL)
            time.sleep(random.uniform(1, 3))

            first, last = self._generate_name()
            password = self._generate_password()
            month, day, year = self._generate_dob()
            dob_str = f"{month}/{day}/{year}"

            use_email = random.choice([True, False])
            if use_email:
                login_cred = self._generate_email()
            else:
                login_cred = self._generate_phone()

            first_name_field = wait.until(EC.presence_of_element_located((By.NAME, "firstname")))
            first_name_field.send_keys(first)

            last_name_field = self.driver.find_element(By.NAME, "lastname")
            last_name_field.send_keys(last)

            email_field = self.driver.find_element(By.NAME, "reg_email__")
            email_field.send_keys(login_cred)

            password_field = self.driver.find_element(By.NAME, "reg_passwd__")
            password_field.send_keys(password)

            month_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "month")))
            month_dropdown.click()
            month_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//option[@value='{month}']")))
            month_option.click()

            day_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "day")))
            day_dropdown.click()
            day_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//option[@value='{day}']")))
            day_option.click()

            year_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "year")))
            year_dropdown.click()
            year_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//option[@value='{year}']")))
            year_option.click()

            gender = random.choice(['2', '1'])
            gender_button = self.driver.find_element(By.XPATH, f"//input[@value='{gender}']")
            gender_button.click()

            submit_button = self.driver.find_element(By.NAME, "websubmit")
            submit_button.click()

            time.sleep(3)

            self.account_data = {
                "login": login_cred,
                "password": password,
                "dob": dob_str,
                "type": "email" if use_email else "phone"
            }

            return self.account_data

        except Exception as e:
            if self.driver:
                self.driver.quit()
            raise Exception(f"Account creation failed: {str(e)}")

    def close(self):
        if self.driver:
            self.driver.quit()
