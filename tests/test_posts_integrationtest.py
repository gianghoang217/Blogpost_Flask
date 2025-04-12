import pytest
from app import app, db
from models import User, Post
from flask import json
from flask_jwt_extended import create_access_token
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

            # Create a test user
            user = User(username='testuser', email='test@example.com', password='password123')
            db.session.add(user)
            db.session.commit()
            logger.info(f"Created test user: {user.username}")

            # Generate a token for the test user
            with app.app_context():
                access_token = create_access_token(identity=user.id)
            client.access_token = access_token
            logger.info(f"Generated access token for user: {user.username}")

            # Create a test post
            post = Post(title='Test Post', content='This is a test post.', user_id=user.id)
            db.session.add(post)
            db.session.commit()
            client.post_id = post.id  # Store the post ID
            logger.info(f"Created test post with ID: {post.id}")

            yield client
            db.session.rollback()
            db.drop_all()
            logger.info("Rolled back session and dropped all tables")

def test_create_post(test_client):
    headers = {
        'Authorization': f'Bearer {test_client.access_token}'
    }
    data = {
        'title': 'Test Post',
        'content': 'This is a test post.'
    }
    logger.info(f"Creating post with data: {data}")
    response = test_client.post('/posts/', json=data, headers=headers)
    logger.info(f"Create post response: {response.status_code}, {response.data}")
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == 'Post created successfully'

def test_get_posts(test_client):
    headers = {
        'Authorization': f'Bearer {test_client.access_token}'
    }
    logger.info("Getting all posts")
    response = test_client.get('/posts/', headers=headers)
    logger.info(f"Get posts response: {response.status_code}, {response.data}")
    assert response.status_code == 200

def test_update_post(test_client):
    headers = {
        'Authorization': f'Bearer {test_client.access_token}'
    }
    data = {
        'title': 'Updated Test Post',
        'content': 'This is an updated test post.'
    }
    logger.info(f"Updating post with ID: {test_client.post_id}, data: {data}")
    response = test_client.put(f'/posts/{test_client.post_id}', json=data, headers=headers)
    logger.info(f"Update post response: {response.status_code}, {response.data}")
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Post updated successfully'

def test_delete_post(test_client):
    headers = {
        'Authorization': f'Bearer {test_client.access_token}'
    }
    logger.info(f"Deleting post with ID: {test_client.post_id}")
    response = test_client.delete(f'/posts/{test_client.post_id}', headers=headers)
    logger.info(f"Delete post response: {response.status_code}, {response.data}")
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Post deleted successfully'
    
    
def test_like_post(test_client):
    headers = {
        'Authorization': f'Bearer {test_client.access_token}'
    }
    logger.info(f"Liking post with ID: {test_client.post_id}")
    response = test_client.post(f'/posts/{test_client.post_id}/like', headers=headers)
    logger.info(f"Like post response: {response.status_code}, {response.data}")
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == 'Post liked successfully'