import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../src'))

class TestW3Schools:
    def test_w3schools_navigation(self, playwright_page):
        """Test W3Schools website navigation with better selectors"""
        page = playwright_page
        
        # Navigate to W3Schools
        page.goto("https://www.w3schools.com", wait_until='networkidle', timeout=60000)
        
        # Accept cookies if present
        try:
            accept_button = page.locator("button:has-text('Accept'), button:has-text('Agree')").first
            if accept_button.is_visible(timeout=5000):
                accept_button.click()
        except:
            print("No cookie consent found or already accepted")
        
        # Click on HTML tutorial with better selector
        html_link = page.locator("a:has-text('HTML'), [title*='HTML']").first
        html_link.click()
        
        # Wait for navigation
        page.wait_for_url("**/html/**", timeout=30000)
        
        # Verify we're on HTML tutorial page
        assert "html" in page.url.lower()
        assert "HTML" in page.title() or "html" in page.title().lower()
        
        print("✓ W3Schools navigation test passed")
    
    def test_w3schools_search(self, playwright_page):
        """Test W3Schools search functionality with precise selectors"""
        page = playwright_page
        
        page.goto("https://www.w3schools.com", wait_until='networkidle', timeout=60000)
        
        # Use specific search box selector
        search_box = page.locator("#search2").first  # More specific ID
        search_box.wait_for(state='visible', timeout=10000)
        search_box.fill("Python tutorial")
        search_box.press("Enter")
        
        # Wait for search results
        page.wait_for_timeout(2000)  # Small delay for search
        
        # Verify search worked - look for Python-related content
        python_content = page.locator("text=Python").first
        assert python_content.is_visible(timeout=10000), "Python content not found after search"
        
        print("✓ W3Schools search test passed")
