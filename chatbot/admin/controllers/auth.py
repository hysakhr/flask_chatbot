import functools

from flask import (
    Blueprint, g, render_template, request
)

from werkzeug.security import check_password_hash, generate_password_hash

from chatbot.models import User

bp = Blueprint('admin/auth', __name__, url_prefix='/admin/auth')
