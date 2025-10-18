import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from src.pages.base_page import BasePage
    from src.utils.selenium_helpers import SeleniumHelpers
except ImportError:
    from base_page import BasePage

class InventoryPage(BasePage):
    # Locators for SauceDemo
    PRODUCTS_TITLE = ('css', '.title')
    SHOPPING_CART = ('id', 'shopping_cart_container')
    MENU_BUTTON = ('id', 'react-burger-menu-btn')
    LOGOUT_LINK = ('id', 'logout_sidebar_link')
    PRODUCT_ITEMS = ('css', '.inventory_item')
    ADD_TO_CART_BUTTON = ('css', '.btn_inventory')
    
    def __init__(self, driver):
        super().__init__(driver)
        from src.utils.selenium_helpers import SeleniumHelpers
        self.helper = SeleniumHelpers(driver)
    
    def get_page_title(self):
        return self.helper.get_text(*self.PRODUCTS_TITLE)
    
    def get_product_count(self):
        elements = self.driver.find_elements(*self.helper._get_locator(*self.PRODUCT_ITEMS))
        return len(elements)
    
    def add_first_product_to_cart(self):
        self.helper.click_element(*self.ADD_TO_CART_BUTTON)
    
    def logout(self):
        self.helper.click_element(*self.MENU_BUTTON)
        self.helper.click_element(*self.LOGOUT_LINK)
