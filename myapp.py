import os
from flask import Flask
from dotenv import load_dotenv
from models.models import db
from routes.main_routes import main_routes
from routes.admin_routes import admin_routes

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(main_routes)
    app.register_blueprint(admin_routes, url_prefix='/admin')

    return app


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
