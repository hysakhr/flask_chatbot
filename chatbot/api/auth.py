import functools

from flask import (
    Blueprint, g, render_template, request
)

from werkzeug.security import check_password_hash, generate_password_hash

from chatbot.models import user

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
