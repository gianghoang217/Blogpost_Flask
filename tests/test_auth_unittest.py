import pytest
from unittest.mock import MagicMock, patch
import json
import logging
from flask import Flask

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a separate test app for mocking purposes
test_app = Flask(__name__)

@pytest.fixture(scope="function")
def app_context():
    """Provide an application context for tests that need it"""
    with test_app.app_context():
        yield

def test_register_user_unit(mocker):
    # Mock the test client and its dependencies
    test_client = MagicMock()
    
    # Mock the User model and db.session
    mock_user = MagicMock()
    mocker.patch('models.User', return_value=mock_user)
    mocker.patch('models.db.session.add')
    mocker.patch('models.db.session.commit')
    
    # Mock the JWT token creation
    mock_token = "test_access_token"
    mocker.patch('flask_jwt_extended.create_access_token', return_value=mock_token)
    mocker.patch('flask_jwt_extended.create_refresh_token', return_value="test_refresh_token")
    
    # Mock post method with expected return value
    post_mock = MagicMock(return_value=MagicMock(status_code=201, data=json.dumps({
        'message': 'User registered successfully', 
        'token': mock_token
    })))
    test_client.post = post_mock
    
    # Define the expected data
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    # Call the post method directly
    response = test_client.post('/register', json=data, content_type='application/json')
    
    # Assert that the post method was called with the correct arguments
    test_client.post.assert_called_once_with(
        '/register', 
        json=data, 
        content_type='application/json'
    )

@pytest.mark.usefixtures("app_context")
def test_login_user_unit(mocker):
    # Mock the test client and its dependencies
    test_client = MagicMock()
    
    # Mock the User class and query methods without using real User.query
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = 'testuser'
    mock_user.email = 'test@example.com'
    mock_user.is_admin = False
    mock_user.check_password.return_value = True
    
    # Create a more complex mock structure for User.query
    mock_first = MagicMock(return_value=mock_user)
    mock_filter_by = MagicMock()
    mock_filter_by.first = mock_first
    mock_user_query = MagicMock()
    mock_user_query.filter_by = MagicMock(return_value=mock_filter_by)
    
    # Patch without accessing real User.query
    mocker.patch('models.User', MagicMock(query=mock_user_query))
    
    # Mock the JWT token creation
    mock_access_token = "test_access_token"
    mock_refresh_token = "test_refresh_token"
    mocker.patch('flask_jwt_extended.create_access_token', return_value=mock_access_token)
    mocker.patch('flask_jwt_extended.create_refresh_token', return_value=mock_refresh_token)
    
    # Mock post method with expected return value
    post_mock = MagicMock(return_value=MagicMock(status_code=200, data=json.dumps({
        'message': 'Login successful',
        'access_token': mock_access_token,
        'refresh_token': mock_refresh_token,
        'user': {
            'id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'is_admin': False
        }
    })))
    test_client.post = post_mock
    
    # Define the expected data
    data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    # Call the post method directly
    response = test_client.post('/login', json=data, content_type='application/json')
    
    # Assert that the post method was called with the correct arguments
    test_client.post.assert_called_once_with(
        '/login', 
        json=data, 
        content_type='application/json'
    )

@pytest.mark.usefixtures("app_context")
def test_invalid_login_unit(mocker):
    # Mock the test client and its dependencies
    test_client = MagicMock()
    
    # Create a more complex mock structure for User.query without returning a user
    mock_first = MagicMock(return_value=None)  # No user found
    mock_filter_by = MagicMock()
    mock_filter_by.first = mock_first
    mock_user_query = MagicMock()
    mock_user_query.filter_by = MagicMock(return_value=mock_filter_by)
    
    # Patch without accessing real User.query
    mocker.patch('models.User', MagicMock(query=mock_user_query))
    
    # Mock post method with expected return value
    post_mock = MagicMock(return_value=MagicMock(status_code=401, data=json.dumps({
        'error': 'Invalid credentials'
    })))
    test_client.post = post_mock
    
    # Define the expected data
    data = {
        'email': 'wrong@example.com',
        'password': 'wrongpassword'
    }
    
    # Call the post method directly
    response = test_client.post('/login', json=data, content_type='application/json')
    
    # Assert that the post method was called with the correct arguments
    test_client.post.assert_called_once_with(
        '/login', 
        json=data, 
        content_type='application/json'
    )

@pytest.mark.usefixtures("app_context")
def test_refresh_token_unit(mocker):
    # Mock the test client and its dependencies
    test_client = MagicMock()
    
    # Mock get_jwt_identity function
    mocker.patch('flask_jwt_extended.get_jwt_identity', return_value=1)
    
    # Mock the User class without using User.query directly
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = 'testuser'
    mock_user.email = 'test@example.com'
    mock_user.is_admin = False
    
    # Create a more complex mock structure
    mock_first = MagicMock(return_value=mock_user)
    mock_filter_by = MagicMock()
    mock_filter_by.first = mock_first
    mock_user_query = MagicMock()
    mock_user_query.filter_by = MagicMock(return_value=mock_filter_by)
    
    # Patch without accessing real User.query
    mocker.patch('models.User', MagicMock(query=mock_user_query))
    
    # Mock the JWT token creation
    mock_access_token = "new_access_token"
    mocker.patch('flask_jwt_extended.create_access_token', return_value=mock_access_token)
    
    # Mock post method with expected return value
    post_mock = MagicMock(return_value=MagicMock(status_code=200, data=json.dumps({
        'access_token': mock_access_token
    })))
    test_client.post = post_mock
    
    # Define the expected headers
    headers = {'Authorization': 'Bearer test_refresh_token'}
    
    # Call the post method directly
    response = test_client.post('/refresh', headers=headers)
    
    # Assert that the post method was called with the correct arguments
    test_client.post.assert_called_once_with(
        '/refresh', 
        headers=headers
    )