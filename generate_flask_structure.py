import os

# List of folder names to create
folders = [
    "routes", "logic", "utils", "models", "templates", "static/css", "instance"
]

# Dictionary mapping file paths to their content
files = {
    "myapp.py": "import os\nfrom flask import Flask\nfrom dotenv import load_dotenv\nfrom models.models import db\nfrom routes.main_routes import main_routes\nfrom routes.admin_routes import admin_routes\n\nload_dotenv()\n\ndef create_app():\n    app = Flask(__name__)\n\n    app.secret_key = os.getenv('SECRET_KEY')\n    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')\n    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024\n    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'\n    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False\n\n    db.init_app(app)\n    app.register_blueprint(main_routes)\n    app.register_blueprint(admin_routes, url_prefix='/admin')\n\n    return app\n\n\napp = create_app()\n\nif __name__ == '__main__':\n    with app.app_context():\n        db.create_all()\n    app.run(debug=True)\n",
    "config.py": "# General configuration settings\n",
    "requirements.txt": "flask\nflask_sqlalchemy\npython-dotenv\n",
    ".env": "SECRET_KEY=supersecretkey\nADMIN_USERNAME=admin\nADMIN_PASSWORD=admin123\n",
    ".gitignore": "# Python cache files\n__pycache__/\n*.pyc\n*.pyo\n*.pyd\n*.sqlite3\n\n# Virtual environments\nvenv/\nenv/\n.virtualenv/\n\n# Environment files\n.env\n\n# Local databases\ninstance/*.db\n\n# Uploaded images\n\n\n# Log files\n*.log\n\n# OS-specific files\n.DS_Store\nThumbs.db\n\n# IDE configuration files\ngenerate_flask_structure.py\npro_flask.code-workspace\n",
    "routes/__init__.py": "",
    "routes/main_routes.py": "from flask import Blueprint\nmain_routes = Blueprint('main', __name__)\n\n@main_routes.route('/')\ndef home():\n    return 'Homepage'\n",
    "routes/admin_routes.py": "from flask import Blueprint, render_template, request, redirect, url_for, session\nimport os\nfrom config import ADMIN_USERNAME, ADMIN_PASSWORD\nfrom models.models import db, User\nfrom werkzeug.security import generate_password_hash, check_password_hash\n\nadmin_routes = Blueprint('admin', __name__)\n\n@admin_routes.route('/')\ndef dashboard():\n    return 'Admin Dashboard'\n\n@admin_routes.route('/login', methods=['GET', 'POST'])\ndef login():\n    error = None\n    if request.method == 'POST':\n        username = request.form['username']\n        password = request.form['password']\n        user = User.query.filter_by(username=username).first()\n        if user and check_password_hash(user.password, password):\n            session['logged_in'] = True\n            return redirect(url_for('admin.dashboard'))\n        else:\n            error = 'Invalid username or password'\n    return f\"<h2>Login</h2><form method='post'><input name='username'><input name='password' type='password'><button>Login</button></form>{error if error else ''}\"\n\n@admin_routes.route('/register', methods=['GET', 'POST'])\ndef register():\n    message = ''\n    if request.method == 'POST':\n        username = request.form['username']\n        password = request.form['password']\n        if User.query.filter_by(username=username).first():\n            message = '⚠️ Username already exists'\n        else:\n            hashed_pw = generate_password_hash(password)\n            new_user = User(username=username, password=hashed_pw)\n            db.session.add(new_user)\n            db.session.commit()\n            message = '✅ Registration successful'\n    return f\"<h2>Register</h2><form method='post'><input name='username'><input name='password' type='password'><button>Register</button></form>{message}\"\n",
    "logic/__init__.py": "",
    "utils/__init__.py": "",
    "utils/helpers.py": "import os\nimport uuid\nfrom flask import current_app\n\nALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}\n\ndef allowed_file(filename):\n    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS\n\ndef save_uploaded_file(file):\n    if file and allowed_file(file.filename):\n        ext = file.filename.rsplit('.', 1)[1].lower()\n        unique_name = f\"{uuid.uuid4().hex}.{ext}\"\n        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)\n        file.save(filepath)\n        return unique_name\n    return None\n",
    "models/__init__.py": "",
    "models/models.py": "from flask_sqlalchemy import SQLAlchemy\n\ndb = SQLAlchemy()\n\nclass User(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    username = db.Column(db.String(80), unique=True, nullable=False)\n    password = db.Column(db.String(120), nullable=False)\n",
    "static/css/style.css": "body { font-family: Arial; }"
}

def create_project_structure():
    """Create folders and files for the Flask project."""
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    for file_path, content in files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    print("Project structure created successfully.")


if __name__ == "__main__":
    create_project_structure()
