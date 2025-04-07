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

