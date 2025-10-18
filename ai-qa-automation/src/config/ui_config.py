import os

class UIConfig:
    # Browser Configuration
    BROWSER = os.getenv('UI_BROWSER', 'chrome')
    HEADLESS = os.getenv('UI_HEADLESS', 'False').lower() == 'true'
    WINDOW_WIDTH = int(os.getenv('UI_WINDOW_WIDTH', '1920'))
    WINDOW_HEIGHT = int(os.getenv('UI_WINDOW_HEIGHT', '1080'))
    
    # Timeout Configuration
    IMPLICIT_WAIT = int(os.getenv('UI_IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('UI_EXPLICIT_WAIT', '30'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('UI_PAGE_LOAD_TIMEOUT', '60'))
    
    # Test URLs
    BASE_URL = os.getenv('UI_BASE_URL', 'https://www.saucedemo.com')
    
    # Test Data
    STANDARD_USER = os.getenv('UI_STANDARD_USER', 'standard_user')
    LOCKED_USER = os.getenv('UI_LOCKED_USER', 'locked_out_user')
    PASSWORD = os.getenv('UI_PASSWORD', 'secret_sauce')
