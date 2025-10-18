import pytest
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../src'))

try:
    from pages.login_page import LoginPage
    from pages.inventory_page import InventoryPage
    from config.ui_config import UIConfig
except ImportError:
    print("Warning: Could not import from src modules")

class TestLogin:
    @pytest.fixture
    def login_page(self, selenium):
        """Setup login page fixture"""
        selenium.get(UIConfig.BASE_URL)
        return LoginPage(selenium)
    
    def test_successful_login(self, login_page, selenium):
        """Test successful login with valid credentials"""
        # Login with valid credentials
        login_page.login(UIConfig.STANDARD_USER, UIConfig.PASSWORD)
        
        # Verify we are redirected to inventory page
        inventory_page = InventoryPage(selenium)
        assert "inventory" in selenium.current_url
        assert inventory_page.get_page_title() == "Products"
        assert inventory_page.get_product_count() > 0
        
        print("✓ Successful login test passed")
    
    def test_locked_user_login(self, login_page):
        """Test login attempt with locked out user"""
        # Login with locked user
        login_page.login(UIConfig.LOCKED_USER, UIConfig.PASSWORD)
        
        # Verify error message
        assert login_page.is_error_message_displayed()
        error_text = login_page.get_error_message()
        assert "locked out" in error_text.lower()
        
        print("✓ Locked user login test passed")
    
    def test_invalid_credentials(self, login_page):
        """Test login with invalid credentials"""
        # Login with invalid credentials
        login_page.login("invalid_user", "wrong_password")
        
        # Verify error message
        assert login_page.is_error_message_displayed()
        error_text = login_page.get_error_message()
        assert "username and password do not match" in error_text.lower()
        
        print("✓ Invalid credentials test passed")
    
    def test_logout_functionality(self, login_page, selenium):
        """Test login and logout functionality"""
        # Login first
        login_page.login(UIConfig.STANDARD_USER, UIConfig.PASSWORD)
        
        # Logout
        inventory_page = InventoryPage(selenium)
        inventory_page.logout()
        
        # Verify we are back on login page
        assert "saucedemo.com" in selenium.current_url
        assert login_page.helper.is_element_visible(*login_page.USERNAME_INPUT)
        assert login_page.helper.is_element_visible(*login_page.PASSWORD_INPUT)
        
        print("✓ Logout functionality test passed")
