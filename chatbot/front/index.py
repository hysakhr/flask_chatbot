from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('index', __name__, )


@bp.route('/')
def index():
    return render_template('front/index.html')
