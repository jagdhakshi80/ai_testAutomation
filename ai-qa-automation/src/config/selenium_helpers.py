from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
from src.config.ui_config import UIConfig

class SeleniumHelpers:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, UIConfig.EXPLICIT_WAIT)
        self.config = UIConfig()
        self.logger = logging.getLogger(__name__)
    
    def navigate_to(self, url):
        """Navigate to a specific URL"""
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")
    
    def find_element(self, locator_type, locator_value):
        """Find element with explicit wait"""
        try:
            locator = self._get_locator(locator_type, locator_value)
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.logger.info(f"Found element: {locator_value}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator_value}")
            raise
    
    def click_element(self, locator_type, locator_value):
        """Click on an element"""
        element = self.find_element(locator_type, locator_value)
        element.click()
        self.logger.info(f"Clicked element: {locator_value}")
    
    def enter_text(self, locator_type, locator_value, text):
        """Enter text into an input field"""
        element = self.find_element(locator_type, locator_value)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Entered text '{text}' into: {locator_value}")
    
    def get_text(self, locator_type, locator_value):
        """Get text from an element"""
        element = self.find_element(locator_type, locator_value)
        text = element.text
        self.logger.info(f"Got text '{text}' from: {locator_value}")
        return text
    
    def is_element_visible(self, locator_type, locator_value, timeout=None):
        """Check if element is visible"""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            locator = self._get_locator(locator_type, locator_value)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def take_screenshot(self, filename=None):
        """Take screenshot and save to file"""
        if filename is None:
            filename = f"screenshot_{int(time.time())}.png"
        
        screenshot_path = f"reports/screenshots/{filename}"
        self.driver.save_screenshot(screenshot_path)
        self.logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    
    def wait_for_page_load(self, timeout=30):
        """Wait for page to fully load"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            self.logger.info("Page loaded completely")
        except TimeoutException:
            self.logger.warning("Page load timeout")
    
    def _get_locator(self, locator_type, locator_value):
        """Convert locator type to Selenium By"""
        locators = {
            'id': By.ID,
            'name': By.NAME,
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'class': By.CLASS_NAME,
            'tag': By.TAG_NAME,
            'link': By.LINK_TEXT,
            'partial_link': By.PARTIAL_LINK_TEXT
        }
        return (locators[locator_type.lower()], locator_value)
