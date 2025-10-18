import requests
import pytest

class TestSimpleRESTAPI:
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    def test_get_users(self):
        """Test GET request to fetch users"""
        response = requests.get(f"{self.BASE_URL}/users")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Verify user structure
        first_user = data[0]
        assert 'id' in first_user
        assert 'name' in first_user
        assert 'email' in first_user
        print(f"✓ Found user: {first_user['name']}")
    
    def test_get_specific_user(self):
        """Test GET request for specific user"""
        response = requests.get(f"{self.BASE_URL}/users/1")
        
        assert response.status_code == 200
        user_data = response.json()
        
        expected_fields = ['id', 'name', 'username', 'email', 'address']
        for field in expected_fields:
            assert field in user_data
        print(f"✓ User data structure is correct for user ID: {user_data['id']}")
    
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
        print(f"✓ Successfully created post with ID: {response_data['id']}")

# Run this test first to verify basic API functionality
