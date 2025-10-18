"""Common GraphQL queries for testing"""

# SpaceX queries
SPACEX_LAUNCHES_QUERY = """
query LaunchesList($limit: Int!) {
    launches(limit: $limit) {
        mission_name
        launch_date_utc
        launch_success
        rocket {
            rocket_name
        }
    }
}
"""

SPACEX_ROCKETS_QUERY = """
query {
    rockets {
        name
        type
        country
        company
    }
}
"""

# Countries queries
COUNTRIES_QUERY = """
query {
    countries {
        code
        name
        capital
        currency
        languages {
            name
        }
    }
}
"""

COUNTRIES_BY_CODE_QUERY = """
query CountryByCode($code: ID!) {
    country(code: $code) {
        name
        capital
        currency
    }
}
"""
