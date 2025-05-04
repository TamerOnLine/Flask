from flask import Blueprint

main_routes = Blueprint('main', __name__)


@main_routes.route('/')
def home():
    """
    Handle the root URL route and return a simple homepage message.

    Returns:
        str: A string message indicating the homepage.
    """
    return 'Homepage'
