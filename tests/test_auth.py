import pytest
from app import app, db
from models import User
from auth import register
from flask import json

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_register_user(test_client):
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    response = test_client.post('/register', json=data)
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == 'User registered successfully'

def test_login_user(test_client):
    # First register a user
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    test_client.post('/register', json=data)

    # Now try to log in
    login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    response = test_client.post('/login', json=login_data)
    assert response.status_code == 200
    assert 'token' in json.loads(response.data)