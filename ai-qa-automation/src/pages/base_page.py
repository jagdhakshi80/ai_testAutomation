from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.selenium_helpers import SeleniumHelpers

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.helper = SeleniumHelpers(driver)
        self.wait = WebDriverWait(driver, 10)
    
    def get_title(self):
        return self.driver.title
    
    def get_current_url(self):
        return self.driver.current_url
    
    def refresh_page(self):
        self.driver.refresh()
