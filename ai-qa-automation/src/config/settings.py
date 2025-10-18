import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TestConfig:
    # API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'test-key')
    BASE_URL = os.getenv('BASE_URL', 'https://jsonplaceholder.typicode.com')
    
    # AI Model Configuration
    MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '100'))
    
    # Test Configuration
    TEST_TIMEOUT = 30
    WAIT_TIME = 10
    
    # Web Configuration
    HEADLESS_MODE = True
