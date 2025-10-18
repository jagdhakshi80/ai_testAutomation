import os

class GraphQLConfig:
    # Public GraphQL APIs for testing
    SPACEX_API = "https://spacex-production.up.railway.app/"
    COUNTRIES_API = "https://countries.trevorblades.com/"
    GITHUB_API = "https://api.github.com/graphql"
    
    # Headers
    HEADERS = {
        "Content-Type": "application/json",
    }
