"""
Test to verify the automation structure is correct
"""
import pytest
import sys
import os

def test_python_paths():
    """Test that Python can import from src"""
    # Add src to path
    src_path = os.path.join(os.path.dirname(__file__), '../../../src')
    sys.path.insert(0, src_path)
    
    try:
        # Try to import config
        from config import ui_config
        print("✓ Successfully imported config.ui_config")
    except ImportError as e:
        pytest.fail(f"Failed to import config: {e}")
    
    try:
        # Try to import utils
        from utils import selenium_helpers
        print("✓ Successfully imported utils.selenium_helpers")
    except ImportError:
        print("⚠ utils.selenium_helpers not found (optional)")

def test_selenium_fixture(selenium):
    """Test that Selenium fixture works"""
    assert selenium is not None
    print("✓ Selenium WebDriver is available")
    
    # Test basic navigation
    selenium.get("https://httpbin.org/html")
    assert "Herman Melville" in selenium.page_source
    print("✓ Basic Selenium navigation works")

def test_test_files_exist():
    """Verify test files exist"""
    test_files = [
        "tests/ui/selenium/test_simple_ui.py",
        "tests/ui/selenium/test_automation_friendly.py", 
        "tests/ui/selenium/test_reliable_sites.py",
        "tests/ui/conftest.py"
    ]
    
    for file_path in test_files:
        assert os.path.exists(file_path), f"Missing test file: {file_path}"
        print(f"✓ Test file exists: {file_path}")

def test_directory_structure():
    """Verify directory structure"""
    required_dirs = [
        "tests/ui/selenium",
        "tests/ui/playwright", 
        "src/config",
        "src/utils",
        "src/pages",
        "reports/screenshots"
    ]
    
    for dir_path in required_dirs:
        assert os.path.exists(dir_path), f"Missing directory: {dir_path}"
        print(f"✓ Directory exists: {dir_path}")
