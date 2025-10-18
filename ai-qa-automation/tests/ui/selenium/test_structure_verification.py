"""
Test to verify the automation structure is correct
"""
import pytest
import sys
import os

def test_python_paths():
    """Test that Python paths are set up correctly"""
    print("Testing Python paths...")
    
    # Add src to path
    src_path = os.path.join(os.path.dirname(__file__), '../../../src')
    sys.path.insert(0, src_path)
    print(f"✓ Added to path: {src_path}")
    
    # Try to import config
    try:
        from config import ui_config
        print("✓ Successfully imported config.ui_config")
    except ImportError as e:
        pytest.fail(f"Failed to import config: {e}")
    
    # Try to check if we can access the class
    try:
        config = ui_config.UIConfig()
        print(f"✓ UIConfig loaded - Browser: {config.BROWSER}, Headless: {config.HEADLESS}")
    except Exception as e:
        pytest.fail(f"Failed to create UIConfig: {e}")

def test_selenium_fixture(selenium):
    """Test that Selenium fixture works"""
    print("Testing Selenium fixture...")
    assert selenium is not None
    print("✓ Selenium WebDriver is available")
    
    # Test basic navigation
    selenium.get("https://httpbin.org/html")
    print("✓ Successfully navigated to httpbin.org")
    
    # Check page content
    assert "Herman Melville" in selenium.page_source
    print("✓ Page content verified")
    
    # Check page title
    title = selenium.title
    print(f"✓ Page title: {title}")

def test_test_files_exist():
    """Verify test files exist"""
    print("Checking test files...")
    
    test_files = [
        "tests/ui/selenium/test_simple_ui.py",
        "tests/ui/selenium/test_structure_verification.py",
        "tests/ui/conftest.py"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"✓ Test file exists: {file_path}")
        else:
            pytest.fail(f"Missing test file: {file_path}")

def test_directory_structure():
    """Verify directory structure"""
    print("Checking directory structure...")
    
    required_dirs = [
        "tests/ui/selenium",
        "tests/ui/playwright", 
        "src/config",
        "src/utils",
        "src/pages"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ Directory exists: {dir_path}")
        else:
            pytest.fail(f"Missing directory: {dir_path}")

def test_can_run_pytest():
    """Basic pytest functionality test"""
    print("Testing basic pytest functionality...")
    assert 1 + 1 == 2
    print("✓ Basic assertion test passed")
