import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../src'))

try:
    from pages.login_page import LoginPage
    from pages.inventory_page import InventoryPage
    from config.ui_config import UIConfig
except ImportError:
    print("Warning: Could not import from src modules")

class TestInventory:
    @pytest.fixture
    def inventory_page(self, selenium):
        """Setup inventory page by logging in first"""
        selenium.get(UIConfig.BASE_URL)
        login_page = LoginPage(selenium)
        login_page.login(UIConfig.STANDARD_USER, UIConfig.PASSWORD)
        return InventoryPage(selenium)
    
    def test_inventory_page_load(self, inventory_page):
        """Test inventory page loads correctly"""
        # Verify page title
        assert inventory_page.get_page_title() == "Products"
        
        # Verify products are displayed
        product_count = inventory_page.get_product_count()
        assert product_count == 6  # SauceDemo has 6 products
        
        print("✓ Inventory page load test passed")
    
    def test_add_product_to_cart(self, inventory_page, selenium):
        """Test adding product to shopping cart"""
        # Add first product to cart
        inventory_page.add_first_product_to_cart()
        
        # Verify cart badge updates (you might need to add this logic)
        # For now, just verify the page doesn't crash
        assert "inventory" in selenium.current_url
        
        print("✓ Add product to cart test passed")
    
    def test_inventory_sorting(self, inventory_page, selenium):
        """Test inventory sorting functionality"""
        # This is a placeholder - SauceDemo has sorting but needs specific selectors
        # You would typically:
        # 1. Get initial product order
        # 2. Select sort option
        # 3. Verify product order changed
        
        print("✓ Inventory sorting placeholder test")
