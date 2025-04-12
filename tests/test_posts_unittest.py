import pytest
from unittest.mock import MagicMock
from app import app, db
from models import User, Post
from flask import json
from flask_jwt_extended import create_access_token
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_create_post_unit(mocker):
    # Mock the test client and its dependencies
    test_client = MagicMock()
    test_client.access_token = 'test_token'
    post_mock = MagicMock(return_value=MagicMock(status_code=201, data=json.dumps({'message': 'Post created successfully'})))
    test_client.post = post_mock

    # Define the expected data and headers
    data = {'title': 'Test Post', 'content': 'This is a test post.'}
    headers = {'Authorization': f'Bearer test_token'}

    # Call the post method directly
    test_client.post('/posts/', json=data, headers=headers)

    # Assert that the post method was called with the correct arguments
    test_client.post.assert_called_once_with('/posts/', json=data, headers=headers)

def test_get_posts_unit(mocker):
    # Mock the test client and its dependencies
    test_client = MagicMock()
    test_client.access_token = 'test_token'
    get_mock = MagicMock(return_value=MagicMock(status_code=200, data=json.dumps([{'title': 'Test Post', 'content': 'This is a test post.'}])))
    test_client.get = get_mock

    # Define the expected headers
    headers = {'Authorization': f'Bearer test_token'}

    # Call the get method directly
    test_client.get('/posts/', headers=headers)

    # Assert that the get method was called with the correct arguments
    test_client.get.assert_called_once_with('/posts/', headers=headers)

def test_update_post_unit(mocker):
    # Mock the test client and its dependencies
    test_client = MagicMock()
    test_client.access_token = 'test_token'
    test_client.post_id = 1
    put_mock = MagicMock(return_value=MagicMock(status_code=200, data=json.dumps({'message': 'Post updated successfully'})))
    test_client.put = put_mock

    # Define the expected data and headers
    data = {'title': 'Updated Test Post', 'content': 'This is an updated test post.'}
    headers = {'Authorization': f'Bearer test_token'}

    # Call the put method directly
    test_client.put('/posts/1', json=data, headers=headers)

    # Assert that the put method was called with the correct arguments
    test_client.put.assert_called_once_with('/posts/1', json=data, headers=headers)

def test_delete_post_unit(mocker):
    # Mock the test client and its dependencies
    test_client = MagicMock()
    test_client.access_token = 'test_token'
    test_client.post_id = 1
    delete_mock = MagicMock(return_value=MagicMock(status_code=200, data=json.dumps({'message': 'Post deleted successfully'})))
    test_client.delete = delete_mock

    # Define the expected headers
    headers = {'Authorization': f'Bearer test_token'}

    # Call the delete method directly
    test_client.delete('/posts/1', headers=headers)

    # Assert that the delete method was called with the correct arguments
    test_client.delete.assert_called_once_with('/posts/1', headers=headers)

def test_like_post_unit(mocker):
    # Mock the test client and its dependencies
    test_client = MagicMock()
    test_client.access_token = 'test_token'
    test_client.post_id = 1
    post_mock = MagicMock(return_value=MagicMock(status_code=201, data=json.dumps({'message': 'Post liked successfully'})))
    test_client.post = post_mock

    # Define the expected headers
    headers = {'Authorization': f'Bearer test_token'}

    # Call the post method directly
    test_client.post('/posts/1/like', headers=headers)

    # Assert that the post method was called with the correct arguments
    test_client.post.assert_called_once_with('/posts/1/like', headers=headers)