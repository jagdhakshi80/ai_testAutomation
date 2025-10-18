class LoginTestData:
    VALID_CREDENTIALS = [
        {"username": "standard_user", "password": "secret_sauce", "expected": "success"},
        {"username": "problem_user", "password": "secret_sauce", "expected": "success"},
        {"username": "performance_glitch_user", "password": "secret_sauce", "expected": "success"}
    ]
    
    INVALID_CREDENTIALS = [
        {"username": "invalid_user", "password": "secret_sauce", "expected": "failure"},
        {"username": "standard_user", "password": "wrong_password", "expected": "failure"},
        {"username": "", "password": "secret_sauce", "expected": "failure"},
        {"username": "standard_user", "password": "", "expected": "failure"}
    ]
    
    LOCKED_CREDENTIALS = [
        {"username": "locked_out_user", "password": "secret_sauce", "expected": "locked"}
    ]
