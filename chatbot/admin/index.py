from flask import (
    Blueprint, request, render_template
)

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
def index():
    return render_template('admin/index.html')
