import pytest
from Data import data
from Locators import locators
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Test_OrangeHRM:
    @pytest.fixture
    def booting_function(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.driver.implicitly_wait(10)
        yield
        self.driver.close()

    def test_get_title(self, booting_function):
        self.driver.get(data.WebData().url)
        assert self.driver.title == data.WebData().homepage_title
        print("SUCCESS: Web Title Verified")

    def test_login_validcredentials(self, booting_function):
        self.driver.get(data.WebData().url)
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.NAME, locators.WebLocators().username_locator))).send_keys(
            data.WebData().username)
        self.driver.find_element(by=By.NAME, value=locators.WebLocators().password_locator).send_keys(
            data.WebData().password)
        self.driver.find_element(by=By.XPATH, value=locators.WebLocators().login_button_locator).click()
        assert self.driver.current_url == data.WebData().dashboard_url

    def test_login_invalidpassword(self, booting_function):
        self.driver.get(data.WebData().url)
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.NAME, locators.WebLocators().username_locator))).send_keys(
            data.WebData().username)
        self.driver.find_element(by=By.NAME, value=locators.WebLocators().password_locator).send_keys(
            data.WebData().invalid_password)
        self.driver.find_element(by=By.XPATH, value=locators.WebLocators().login_button_locator).click()

        error_message_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, locators.WebLocators().error_message_locator)))
        # assert self.driver.current_url == data.WebData().dashboard_url
        assert error_message_element.is_displayed()
        assert error_message_element.text == "Invalid credentials"

    def test_login_invalidcredentials(self, booting_function):
        self.driver.get(data.WebData().url)
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.NAME, locators.WebLocators().username_locator))).send_keys(
            data.WebData().invalid_username)
        self.driver.find_element(by=By.NAME, value=locators.WebLocators().password_locator).send_keys(
            data.WebData().invalid_password)
        self.driver.find_element(by=By.XPATH, value=locators.WebLocators().login_button_locator).click()

        error_message_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, locators.WebLocators().error_message_locator)))
        # assert self.driver.current_url == data.WebData().dashboard_url
        assert error_message_element.is_displayed()
        assert error_message_element.text == "Invalid credentials"

    def test_login_emptycredentials_positive(self, booting_function):
        self.driver.get(data.WebData().url)
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.NAME, locators.WebLocators().username_locator))).send_keys(
            data.WebData().empty_username)
        self.driver.find_element(by=By.NAME, value=locators.WebLocators().password_locator).send_keys(
            data.WebData().empty_password)
        self.driver.find_element(by=By.XPATH, value=locators.WebLocators().login_button_locator).click()

        username_alert = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, locators.WebLocators().username_alert_locator)))
        assert username_alert.is_displayed()
        assert username_alert.text == "Required"

        password_alert = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, locators.WebLocators().password_alert_locator)))
        assert password_alert.is_displayed()
        assert password_alert.text == "Required"

    def test_login_emptycredentials_negative(self, booting_function):
        self.driver.get(data.WebData().url)
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.NAME, locators.WebLocators().username_locator))).send_keys(
            data.WebData().empty_username)
        self.driver.find_element(by=By.NAME, value=locators.WebLocators().password_locator).send_keys(
            data.WebData().empty_password)
        self.driver.find_element(by=By.XPATH, value=locators.WebLocators().login_button_locator).click()

        error_message_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, locators.WebLocators().error_message_locator)))
        # assert self.driver.current_url == data.WebData().dashboard_url
        assert error_message_element.is_displayed()
        assert error_message_element.text == "Invalid credentials"