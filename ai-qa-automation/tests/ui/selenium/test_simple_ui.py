import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestSimpleUI:
    def test_saucedemo_login(self, selenium):
        """Simple SauceDemo login test"""
        print("🚀 Starting SauceDemo login test...")
        
        # Navigate to SauceDemo
        selenium.get("https://www.saucedemo.com")
        print("✓ Navigated to SauceDemo")
        
        # Wait for page to load
        WebDriverWait(selenium, 15).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        print("✓ Page loaded successfully")
        
        # Login
        username_field = selenium.find_element(By.ID, "user-name")
        password_field = selenium.find_element(By.ID, "password")
        login_button = selenium.find_element(By.ID, "login-button")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        login_button.click()
        print("✓ Login credentials entered and submitted")
        
        # Verify login success
        WebDriverWait(selenium, 15).until(
            EC.url_contains("inventory")
        )
        print("✓ Successfully redirected to inventory page")
        
        # Verify products page loaded
        products_title = WebDriverWait(selenium, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".title"))
        )
        assert "Products" in products_title.text
        print("✓ Products page title verified")
        
        print("🎉 SauceDemo login test PASSED!")
    
    def test_basic_navigation(self, selenium):
        """Test basic navigation to a simple site"""
        print("🚀 Starting basic navigation test...")
        
        # Navigate to a simple, reliable site
        selenium.get("https://httpbin.org/html")
        print("✓ Navigated to httpbin.org")
        
        # Verify page loaded
        WebDriverWait(selenium, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("✓ Page loaded successfully")
        
        # Check page content
        assert "Herman Melville" in selenium.page_source
        print("✓ Page content verified")
        
        print("🎉 Basic navigation test PASSED!")
