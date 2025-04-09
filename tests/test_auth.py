import pytest
from app import app, db
from models import User
from auth import register
from flask import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.rollback()  # Rollback after each test
            db.drop_all()

def test_register_user(test_client):
    try:
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        logger.info(f"Register data: {data}")  # Add logging
        response = test_client.post('/register', json=data)
        logger.info(f"Register response: {response.status_code}, {response.data}")  # Add logging
        assert response.status_code == 201
        assert json.loads(response.data)['message'] == 'User registered successfully'
    finally:
        db.session.rollback()

def test_login_user(test_client):
    try:
        # First register a user
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        logger.info(f"Register data: {data}")  # Add logging
        test_client.post('/register', json=data)

        # Now try to log in
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        logger.info(f"Login data: {login_data}")  # Add logging
        response = test_client.post('/login', json=login_data)
        logger.info(f"Login response: {response.status_code}, {response.data}")  # Add logging
        assert response.status_code == 200
        assert 'access_token' in json.loads(response.data)  # Check for 'access_token'
    finally:
        db.session.rollback()