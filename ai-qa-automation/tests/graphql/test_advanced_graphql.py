import pytest
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

try:
    from utils.graphql_helpers import GraphQLHelpers
except ImportError:
    # Fallback implementation
    import requests
    class GraphQLHelpers:
        def __init__(self, endpoint_url="https://spacex-production.up.railway.app/"):
            self.endpoint_url = endpoint_url
            self.headers = {"Content-Type": "application/json"}
        
        def execute_query(self, query: str, variables: dict = None):
            payload = {"query": query, "variables": variables or {}}
            return requests.post(self.endpoint_url, json=payload, headers=self.headers)
        
        def validate_graphql_response(self, response):
            assert response.status_code == 200
            data = response.json()
            assert "data" in data
            return data
        
        def extract_nested_field(self, data: dict, field_path: str):
            keys = field_path.split('.')
            current = data
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return None
            return current

class TestAdvancedGraphQL:
    def test_nested_graphql_query(self):
        """Test complex nested GraphQL query - handle null fields gracefully"""
        query = """
        query {
            launches(limit: 2) {
                mission_name
                launch_site {
                    site_name
                }
                rocket {
                    rocket_name
                    rocket_type
                }
                links {
                    article_link
                    video_link
                }
            }
        }
        """
        
        helper = GraphQLHelpers()
        response = helper.execute_query(query)
        data = helper.validate_graphql_response(response)
        
        launches = data['data']['launches']
        assert len(launches) == 2
        
        for launch in launches:
            # Validate that we have mission_name and rocket info
            assert 'mission_name' in launch
            assert launch['mission_name'] is not None
            
            # Rocket should always be present
            assert 'rocket' in launch
            assert helper.extract_nested_field(launch, 'rocket.rocket_name') is not None
            
            # launch_site might be null for some launches, handle gracefully
            launch_site_name = helper.extract_nested_field(launch, 'launch_site.site_name')
            if launch_site_name is not None:
                # If launch_site exists, it should have a site_name
                assert len(launch_site_name) > 0
            else:
                # If launch_site is null, that's acceptable - just log it
                print(f"Note: launch_site is null for mission {launch['mission_name']}")
            
            # Links should be present but some fields might be null
            assert 'links' in launch
        
        print("✓ Nested GraphQL query test passed (handles null fields gracefully)")
    
    def test_graphql_fragments(self):
        """Test GraphQL query with fragments"""
        query = """
        fragment LaunchDetails on Launch {
            mission_name
            launch_date_utc
            launch_success
            rocket {
                rocket_name
            }
        }
        
        query {
            past: launches(limit: 2, sort: "launch_date_utc", order: "DESC") {
                ...LaunchDetails
            }
            upcoming: launches(limit: 2, sort: "launch_date_utc", order: "ASC") {
                ...LaunchDetails
            }
        }
        """
        
        helper = GraphQLHelpers()
        response = helper.execute_query(query)
        data = helper.validate_graphql_response(response)
        
        assert 'past' in data['data']
        assert 'upcoming' in data['data']
        
        # Both should have data, but upcoming might be empty
        assert data['data']['past'] is not None
        assert data['data']['upcoming'] is not None
        
        # Past launches should have data
        assert len(data['data']['past']) == 2
        
        # Upcoming might have fewer than 2 launches
        assert len(data['data']['upcoming']) <= 2
        
        print("✓ GraphQL fragments test passed")
