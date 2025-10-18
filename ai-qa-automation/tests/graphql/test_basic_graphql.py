import pytest
import requests
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

try:
    from utils.graphql_helpers import GraphQLHelpers
    from config.graphql_config import GraphQLConfig
except ImportError:
    # Fallback if imports fail
    class GraphQLConfig:
        SPACEX_API = "https://spacex-production.up.railway.app/"
        COUNTRIES_API = "https://countries.trevorblades.com/"
    
    class GraphQLHelpers:
        def __init__(self, endpoint_url=GraphQLConfig.SPACEX_API):
            self.endpoint_url = endpoint_url
            self.headers = {"Content-Type": "application/json"}
        
        def execute_query(self, query: str, variables: dict = None):
            payload = {"query": query, "variables": variables or {}}
            response = requests.post(self.endpoint_url, json=payload, headers=self.headers)
            return response
        
        def validate_graphql_response(self, response):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()
            assert "data" in data, "Response should contain 'data' field"
            return data

class TestBasicGraphQL:
    def setup_method(self):
        self.graphql_helper = GraphQLHelpers()
    
    def test_spacex_launches_query(self):
        """Test basic SpaceX launches query"""
        query = """
        query {
            launches(limit: 5) {
                mission_name
                launch_date_utc
                launch_success
                rocket {
                    rocket_name
                }
            }
        }
        """
        
        response = self.graphql_helper.execute_query(query)
        data = self.graphql_helper.validate_graphql_response(response)
        
        # Validate response structure
        launches = data['data']['launches']
        assert len(launches) == 5
        
        for launch in launches:
            assert 'mission_name' in launch
            assert 'rocket' in launch
            assert 'rocket_name' in launch['rocket']
        print("✓ SpaceX launches query test passed")
    
    def test_countries_query(self):
        """Test countries GraphQL query"""
        query = """
        query {
            countries {
                code
                name
                capital
                currency
            }
        }
        """
        
        helper = GraphQLHelpers(endpoint_url="https://countries.trevorblades.com/")
        response = helper.execute_query(query)
        data = helper.validate_graphql_response(response)
        
        countries = data['data']['countries']
        assert len(countries) > 0
        
        # Find a specific country
        usa = next((c for c in countries if c['code'] == 'US'), None)
        assert usa is not None
        assert usa['name'] == 'United States'
        print("✓ Countries query test passed")
    
    def test_graphql_with_variables(self):
        """Test GraphQL query with variables"""
        query = """
        query GetLaunch($limit: Int!) {
            launches(limit: $limit) {
                mission_name
                launch_year
            }
        }
        """
        
        variables = {"limit": 3}
        
        response = self.graphql_helper.execute_query(query, variables=variables)
        data = self.graphql_helper.validate_graphql_response(response)
        
        launches = data['data']['launches']
        assert len(launches) == 3
        print("✓ GraphQL with variables test passed")
