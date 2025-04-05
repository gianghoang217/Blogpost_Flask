from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Post, Like

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

# Create a new post
@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created successfully", "post": new_post.to_dict()}), 201

# View a single post
@posts_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def get_single_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict()), 200


# View all posts
@posts_bp.route('/', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts]), 200

# Update your own post
@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    if post.user_id != user_id:
        return jsonify({"error": "You can only update your own posts"}), 403
    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()
    return jsonify({"message": "Post updated successfully", "post": post.to_dict()}), 200

# Delete your own post
@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    if post.user_id != user_id:
        return jsonify({"error": "You can only delete your own posts"}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"}), 200


# Like a post
@posts_bp.route('/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    # Check if the user has already liked the post
    existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if existing_like:
        return jsonify({"error": "You have already liked this post"}), 400

    # Add a new like
    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({"message": "Post liked successfully"}), 201