from flask import Blueprint, render_template, request, redirect, url_for, session
import os
from config import ADMIN_USERNAME, ADMIN_PASSWORD
from models.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

admin_routes = Blueprint('admin', __name__)

@admin_routes.route('/')
def dashboard():
    return 'Admin Dashboard'

@admin_routes.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            error = 'Invalid username or password'
    return f"<h2>Login</h2><form method='post'><input name='username'><input name='password' type='password'><button>Login</button></form>{error if error else ''}"

@admin_routes.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            message = '⚠️ Username already exists'
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            message = '✅ Registration successful'
    return f"<h2>Register</h2><form method='post'><input name='username'><input name='password' type='password'><button>Register</button></form>{message}"
