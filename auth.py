from functools import wraps
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from models import db, User
from datetime import timedelta


auth_bp = Blueprint('auth', __name__)

# Register Route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    is_admin = data.get('is_admin', False)
    # Hash the password before storing
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Create a new user
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()

    # Generate JWT token for the new user
    access_token = create_access_token(identity=new_user.id, expires_delta=timedelta(days=1))

    return jsonify({
        "message": "User registered successfully",
        "token": access_token
    }), 201
    
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        additional_claims = {
            "is_admin": user.is_admin  # Assuming your User model has is_admin field
        }
        # Generate both access and refresh tokens
        access_token = create_access_token(identity=user.id,
                                           expires_delta=timedelta(hours=1),
                                           additional_claims=additional_claims)  # 1-hour access token
        refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(days=7))  # 7-day refresh token

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin
            }
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401

