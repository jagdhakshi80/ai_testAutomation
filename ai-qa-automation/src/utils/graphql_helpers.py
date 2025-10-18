import requests
import json
import asyncio
import time

class GraphQLHelpers:
    def __init__(self, endpoint_url="https://spacex-production.up.railway.app/"):
        self.endpoint_url = endpoint_url
        self.headers = {"Content-Type": "application/json"}
    
    def execute_query(self, query: str, variables: dict = None, operation_name: str = None, timeout: int = 30):
        """Execute GraphQL query using requests with timeout"""
        payload = {
            "query": query,
            "variables": variables or {},
            "operationName": operation_name
        }
        
        try:
            response = requests.post(
                self.endpoint_url,
                json=payload,
                headers=self.headers,
                timeout=timeout
            )
            return response
        except requests.exceptions.Timeout:
            raise Exception(f"Query timed out after {timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    async def execute_query_async(self, query: str, variables: dict = None):
        """Execute GraphQL query asynchronously"""
        # Simple sync implementation for now
        return self.execute_query(query, variables)
    
    def validate_graphql_response(self, response, allow_errors: bool = False):
        """Validate GraphQL response structure"""
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "data" in data, "Response should contain 'data' field"
        
        if not allow_errors and "errors" in data and data["errors"]:
            # Check if errors are expected (like complexity errors)
            error_messages = [str(error).lower() for error in data["errors"]]
            has_expected_errors = any(
                'complexity' in msg or 'depth' in msg or 'maximum' in msg
                for msg in error_messages
            )
            if not has_expected_errors:
                raise AssertionError(f"Unexpected GraphQL errors: {data['errors']}")
        
        return data
    
    def extract_nested_field(self, data: dict, field_path: str, default=None):
        """Extract nested field from GraphQL response using dot notation"""
        if data is None:
            return default
            
        keys = field_path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    def measure_query_performance(self, query: str, variables: dict = None, iterations: int = 1):
        """Measure query execution performance"""
        times = []
        for i in range(iterations):
            start_time = time.time()
            response = self.execute_query(query, variables)
            end_time = time.time()
            times.append(end_time - start_time)
            
            # Validate response
            if response.status_code != 200:
                raise Exception(f"Query failed with status {response.status_code}")
        
        return {
            'min_time': min(times),
            'max_time': max(times),
            'avg_time': sum(times) / len(times),
            'iterations': iterations
        }
