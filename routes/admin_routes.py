from flask import Blueprint, render_template, request, redirect, url_for, session
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from models.models import db, User

admin_user = os.getenv('ADMIN_USERNAME')
admin_pass = os.getenv('ADMIN_PASSWORD')

admin_routes = Blueprint('admin', __name__)

def login_required(f):
    """Decorator to ensure the user is logged in.

    Args:
        f (function): The view function to wrap.

    Returns:
        function: Wrapped function that checks login status.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to ensure the user has admin privileges.

    Args:
        f (function): The view function to wrap.

    Returns:
        function: Wrapped function that checks admin status.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or not session.get('username'):
            return redirect(url_for('admin.login'))

        user = User.query.filter_by(username=session['username']).first()
        if not user or not user.is_admin:
            return "Access Denied", 403

        return f(*args, **kwargs)
    return decorated_function

@admin_routes.route('/')
@admin_required
def dashboard():
    """Render the admin dashboard.

    Returns:
        str: Rendered HTML template for the dashboard.
    """
    return render_template('admin_dashboard.html', username=session.get('username'))

@admin_routes.route('/login', methods=['GET', 'POST'])
def login():
    """Handle admin login functionality.

    Returns:
        str: Rendered HTML template for login page or redirect after login.
    """
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.home'))

        error = 'Invalid username or password'

    return render_template('login.html', error=error)

@admin_routes.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user.

    Returns:
        str: Rendered HTML template for registration page.
    """
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            message = 'Username already exists'
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            message = 'Registration successful'

    return render_template('register.html', message=message)

@admin_routes.route('/logout')
def logout():
    """Log out the current user and clear the session.

    Returns:
        Response: Redirect to the login page.
    """
    session.clear()
    return redirect(url_for('admin.login'))
