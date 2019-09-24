from flask import (
    Blueprint, request, render_template
)

bp = Blueprint('admin/faq', __name__, url_prefix='/admin/faq')


@bp.route('/')
def index():
    return render_template('admin/faq/index.html')
