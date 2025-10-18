import requests
import pytest
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

try:
    from config.settings import TestConfig
except ImportError:
    # Fallback configuration if settings can't be imported
    class TestConfig:
        BASE_URL = "https://jsonplaceholder.typicode.com"
        OPENAI_API_KEY = "test-key"
        MODEL_NAME = "gpt-3.5-turbo"
        MAX_TOKENS = 100
        TEST_TIMEOUT = 30

class TestRESTAPI:
    BASE_URL = TestConfig.BASE_URL
    
    def test_get_users(self):
        """Test GET request to fetch users"""
        response = requests.get(f"{self.BASE_URL}/users")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0
        
        # Verify user structure
        first_user = response.json()[0]
        assert 'id' in first_user
        assert 'name' in first_user
        assert 'email' in first_user
    
    def test_get_specific_user(self):
        """Test GET request for specific user"""
        response = requests.get(f"{self.BASE_URL}/users/1")
        
        assert response.status_code == 200
        user_data = response.json()
        
        expected_fields = ['id', 'name', 'username', 'email', 'address']
        for field in expected_fields:
            assert field in user_data
    
    def test_create_post(self):
        """Test POST request to create a new post"""
        new_post = {
            "title": "AI QA Automation Test",
            "body": "This is a test post for AI QA automation",
            "userId": 1
        }
        
        response = requests.post(f"{self.BASE_URL}/posts", json=new_post)
        
        assert response.status_code == 201
        response_data = response.json()
        
        assert response_data['title'] == new_post['title']
        assert response_data['body'] == new_post['body']
        assert 'id' in response_data
    
    @pytest.mark.parametrize("user_id,expected_status", [
        (1, 200),
        (999, 404),  # Non-existent user
    ])
    def test_user_endpoints_with_params(self, user_id, expected_status):
        """Test user endpoints with different parameters"""
        response = requests.get(f"{self.BASE_URL}/users/{user_id}")
        assert response.status_code == expected_status
