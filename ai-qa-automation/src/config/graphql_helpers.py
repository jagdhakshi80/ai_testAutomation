import requests
import json
import asyncio
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.aiohttp import AIOHTTPTransport
from src.config.graphql_config import GraphQLConfig

class GraphQLHelpers:
    def __init__(self, endpoint_url=GraphQLConfig.SPACEX_API):
        self.endpoint_url = endpoint_url
        self.headers = GraphQLConfig.HEADERS.copy()
    
    def execute_query(self, query: str, variables: dict = None, operation_name: str = None):
        """Execute GraphQL query using requests"""
        payload = {
            "query": query,
            "variables": variables or {},
            "operationName": operation_name
        }
        
        response = requests.post(
            self.endpoint_url,
            json=payload,
            headers=self.headers
        )
        
        return response
    
    async def execute_query_async(self, query: str, variables: dict = None):
        """Execute GraphQL query asynchronously using gql client"""
        transport = AIOHTTPTransport(url=self.endpoint_url)
        
        async with Client(transport=transport) as session:
            query_obj = gql(query)
            result = await session.execute(query_obj, variable_values=variables)
            return result
    
    def validate_graphql_response(self, response):
        """Validate GraphQL response structure"""
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "data" in data, "Response should contain 'data' field"
        assert "errors" not in data, f"GraphQL errors: {data.get('errors', [])}"
        
        return data
    
    def extract_nested_field(self, data: dict, field_path: str):
        """Extract nested field from GraphQL response using dot notation"""
        keys = field_path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current
