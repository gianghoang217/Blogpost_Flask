import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from models import db
from auth import auth_bp
from posts import posts_bp


app = Flask(__name__, static_folder="static")

CORS(app)
# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql+psycopg2://bloguser:Blogpost12345!@localhost/blogpost_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT Configuration
app.config['JWT_SECRET_KEY'] = "supersecretkey"
jwt = JWTManager(app)

db.init_app(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)


if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(f"Error creating tables: {e}")
    app.run(host="0.0.0.0", debug=True) #port=5000