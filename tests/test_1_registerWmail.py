from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


class SignupPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def signup(self, firstname, lastname, username, email, password):
        # Click the signup button

        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//button[contains(text(), "Register")]')))
        self.driver.find_element(By.XPATH, '//button[contains(text(), "Register")]').click()

        # Wait until the signup form is visible
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="authentication-modal"]/div/div[2]/center/form')))

        # Fill the form
        self.driver.find_element(By.NAME, 'firstName').send_keys(firstname)
        self.driver.find_element(By.NAME, 'lastName').send_keys(lastname)
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'email').send_keys(email)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.NAME, 'confirmPassword').send_keys(password)

        # Click the dropdown button
        self.driver.find_element(By.XPATH, '//*[@id="authentication-modal"]/div/div[2]/center/form/div[1]/div/div/button').click()

        # Select an option from the dropdown
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="listbox-option-1"]/div/span')))
        self.driver.find_element(By.XPATH, '//*[@id="listbox-option-1"]/div/span').click()

        self.driver.find_element(By.XPATH, '//button[contains(text(), "R E G I S T E R")]').click()

        # Wait for the alert to appear
        alert = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class=""][div[@class=""][contains(text(), "User registered successfully")]]')))

        return alert.text
    

    def step2(self, birthdate, phonenumber):
        # Click "Select your country"
        self.driver.find_element(By.XPATH, '//span[contains(text(), "Select your country")]').click()

        # Click "Select" and choose a country
        dropdown = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//ul[@role="listbox"]')))
        dropdown.find_element(By.XPATH, './li[1]').click()

        # Select a gender
        # Select a gender
        self.driver.find_element(By.XPATH, '//span[contains(text(), "Select")]').click()

        # Wait for the dropdown to appear and select the first option
        dropdown = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//ul[@role="listbox"]')))
        dropdown.find_element(By.XPATH, './li[1]').click()

        # Enter birthdate
        self.driver.find_element(By.XPATH, '//input[@placeholder="Select Date"]').send_keys(birthdate)

        # Enter phone number
        self.driver.find_element(By.NAME, 'phonenumber').send_keys(phonenumber)  # Replace with the actual selector

        # Click "Choose Your Interesting Fields"
        self.driver.find_element(By.XPATH, '//span[contains(text(), "Choose Your Intereting Fields")]').click()

        dropdown = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//ul[@role="listbox"]')))
        dropdown.find_element(By.XPATH, './li[1]').click() 

        # Click "FINISH"
        self.driver.find_element(By.XPATH, '//button[contains(text(), "F I N I S H")]').click()

        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="What do you want to learn?"]')))







class TestSignup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get(BASE_URL)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_signup(self):
        signup_page = SignupPage(self.driver)
        alert = signup_page.signup("John", "Doe","testuser","testuser@email.com","P@s5w0rd")

        self.assertEqual("User registered successfully", alert)

        signup_page.step2("01/01/1990", "1234567890")

