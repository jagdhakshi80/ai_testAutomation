import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from src.pages.base_page import BasePage
    from src.utils.selenium_helpers import SeleniumHelpers
except ImportError:
    # Fallback imports
    from base_page import BasePage

class LoginPage(BasePage):
    # Locators for SauceDemo
    USERNAME_INPUT = ('id', 'user-name')
    PASSWORD_INPUT = ('id', 'password')
    LOGIN_BUTTON = ('id', 'login-button')
    ERROR_MESSAGE = ('css', '[data-test="error"]')
    
    def __init__(self, driver):
        super().__init__(driver)
        from src.utils.selenium_helpers import SeleniumHelpers
        self.helper = SeleniumHelpers(driver)
    
    def login(self, username, password):
        self.helper.enter_text(*self.USERNAME_INPUT, username)
        self.helper.enter_text(*self.PASSWORD_INPUT, password)
        self.helper.click_element(*self.LOGIN_BUTTON)
    
    def get_error_message(self):
        return self.helper.get_text(*self.ERROR_MESSAGE)
    
    def is_error_message_displayed(self):
        return self.helper.is_element_visible(*self.ERROR_MESSAGE)
