import os
from flask import Flask
from dotenv import load_dotenv
from models.models import db, User
from routes.main_routes import main_routes
from routes.admin_routes import admin_routes
from werkzeug.security import generate_password_hash

# Load environment variables
load_dotenv()

# Define the absolute path to the database
basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
db_path = os.path.join(basedir, 'instance', 'site_data.db')

def create_app():
    """
    Create and configure the Flask application instance.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)

    # Application configuration
    app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key')
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_routes)
    app.register_blueprint(admin_routes, url_prefix='/admin')

    return app


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(db_path):
            print("Initializing database for the first time...")
            db.create_all()
        else:
            print("Database already exists and is ready.")

        # Create an admin user from .env variables if not already present
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')

        existing_admin = User.query.filter_by(username=admin_username).first()
        if not existing_admin:
            admin = User(
                username=admin_username,
                password=generate_password_hash(admin_password),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created: {admin_username}")

    app.run(debug=True, host='0.0.0.0', port=8020)
