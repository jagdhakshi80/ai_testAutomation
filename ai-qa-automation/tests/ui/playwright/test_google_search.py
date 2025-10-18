import pytest
import sys
import os
import time

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../src'))

try:
    from config.ui_config import UIConfig
except ImportError:
    class UIConfig:
        GOOGLE_URL = 'https://www.google.com'

class TestGoogleSearch:
    def test_google_search(self, playwright_page):
        """Test Google search functionality with better error handling"""
        page = playwright_page
        
        # Navigate to Google with timeout
        page.goto(UIConfig.GOOGLE_URL, wait_until='networkidle', timeout=60000)
        
        # Handle cookie consent with better selector
        try:
            # Try multiple possible selectors for cookie consent
            consent_selectors = [
                "button:has-text('Accept all')",
                "button:has-text('I agree')",
                "button:has-text('Accept')",
                "[aria-label*='Accept']"
            ]
            
            for selector in consent_selectors:
                consent_button = page.locator(selector).first
                if consent_button.is_visible(timeout=5000):
                    consent_button.click()
                    page.wait_for_timeout(1000)
                    break
        except:
            print("No cookie consent found or already accepted")
        
        # Find search box with multiple selector strategies
        search_selector = page.locator("textarea[name='q'], input[name='q']").first
        search_selector.wait_for(state='visible', timeout=10000)
        
        # Perform search
        search_selector.fill("AI Quality Assurance")
        search_selector.press("Enter")
        
        # Wait for search results with multiple strategies
        try:
            # Wait for search results to load
            page.wait_for_url("**/search**", timeout=30000)
            
            # Look for search results container
            results_selectors = [
                "#search",
                "#rso",
                ".g",
                "[data-async-context]"
            ]
            
            for selector in results_selectors:
                if page.locator(selector).first.is_visible(timeout=10000):
                    break
            
            # Verify we have some results
            results = page.locator("h1, h2, h3").all()
            assert len(results) > 0, "No search results found"
            
            print("✓ Google search test passed")
            
        except Exception as e:
            # If search fails, check if we got a CAPTCHA or blocking page
            if "sorry" in page.url:
                print("⚠ Google showed CAPTCHA page - test cannot complete")
                return  # Skip test gracefully
            else:
                raise e
    
    def test_google_logo_display(self, playwright_page):
        """Test Google logo is displayed with better selectors"""
        page = playwright_page
        
        page.goto(UIConfig.GOOGLE_URL, wait_until='networkidle', timeout=60000)
        
        # Try multiple logo selectors
        logo_selectors = [
            "img[alt*='Google']",
            ".lnXdpd",
            "img[src*='googlelogo']",
            "div#hplogo img"
        ]
        
        logo_visible = False
        for selector in logo_selectors:
            logo = page.locator(selector).first
            if logo.is_visible(timeout=5000):
                logo_visible = True
                break
        
        assert logo_visible, "Google logo not found with any selector"
        print("✓ Google logo test passed")
