import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

try:
    from utils.graphql_helpers import GraphQLHelpers
except ImportError:
    import requests
    class GraphQLHelpers:
        def __init__(self, endpoint_url="https://spacex-production.up.railway.app/"):
            self.endpoint_url = endpoint_url
            self.headers = {"Content-Type": "application/json"}
        
        def execute_query(self, query: str, variables: dict = None):
            payload = {"query": query, "variables": variables or {}}
            return requests.post(self.endpoint_url, json=payload, headers=self.headers)

class TestGraphQLComplexitySimple:
    def test_reasonable_complexity_query(self):
        """Test that reasonably complex queries work without internal errors"""
        reasonable_query = """
        query {
            launches(limit: 5) {
                mission_name
                launch_date_utc
                rocket {
                    rocket_name
                    rocket_type
                }
                launch_site {
                    site_name
                }
                links {
                    article_link
                }
            }
        }
        """
        
        helper = GraphQLHelpers()
        response = helper.execute_query(reasonable_query)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should not have internal server errors
        if 'errors' in data:
            for error in data['errors']:
                assert 'INTERNAL_SERVER_ERROR' not in str(error), f"Unexpected internal error: {error}"
        
        # Should have data
        assert 'data' in data
        launches = data['data']['launches']
        assert len(launches) == 5
        
        print("✓ Reasonably complex query works correctly")
    
    def test_field_selection_impact(self):
        """Test that selecting different fields affects response size"""
        minimal_query = """
        query {
            launches(limit: 1) {
                mission_name
            }
        }
        """
        
        detailed_query = """
        query {
            launches(limit: 1) {
                mission_name
                details
                rocket {
                    rocket_name
                    rocket_type
                    country
                    company
                }
                launch_site {
                    site_name_long
                }
                links {
                    article_link
                    wikipedia
                    video_link
                }
            }
        }
        """
        
        helper = GraphQLHelpers()
        
        # Execute minimal query
        minimal_response = helper.execute_query(minimal_query)
        minimal_data = minimal_response.json()
        minimal_size = len(str(minimal_data))
        
        # Execute detailed query  
        detailed_response = helper.execute_query(detailed_query)
        detailed_data = detailed_response.json()
        detailed_size = len(str(detailed_data))
        
        # Detailed query should return more data
        assert detailed_size > minimal_size, f"Detailed response ({detailed_size}) should be larger than minimal ({minimal_size})"
        
        print(f"✓ Field selection affects response size: minimal={minimal_size}, detailed={detailed_size}")
