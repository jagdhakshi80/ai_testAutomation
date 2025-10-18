import pytest
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

try:
    from config.ui_config import UIConfig
except ImportError:
    # Fallback configuration
    class UIConfig:
        BROWSER = "chrome"
        HEADLESS = False
        WINDOW_WIDTH = 1920
        WINDOW_HEIGHT = 1080
        IMPLICIT_WAIT = 10
        EXPLICIT_WAIT = 30
        PAGE_LOAD_TIMEOUT = 60

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def selenium(request):
    """Selenium WebDriver fixture"""
    print("🚀 Setting up Chrome WebDriver...")
    
    options = Options()
    if UIConfig.HEADLESS:
        options.add_argument("--headless=new")
        print("✓ Running in headless mode")
    else:
        print("✓ Running in visible mode")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--window-size={UIConfig.WINDOW_WIDTH},{UIConfig.WINDOW_HEIGHT}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    try:
        service = webdriver.ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(UIConfig.IMPLICIT_WAIT)
        driver.set_page_load_timeout(UIConfig.PAGE_LOAD_TIMEOUT)
        
        print("✓ Chrome WebDriver setup successful")
        yield driver
        
    except Exception as e:
        print(f"❌ WebDriver setup failed: {e}")
        raise
    finally:
        if 'driver' in locals():
            driver.quit()
            print("✓ WebDriver closed")
