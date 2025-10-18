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
    # Fallback configuration
    class UIConfig:
        BASE_URL = "https://www.saucedemo.com"
        STANDARD_USER = "standard_user"
        LOCKED_USER = "locked_out_user"
        PASSWORD = "secret_sauce"

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
        assert "Products" in inventory_page.get_page_title()
        
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
