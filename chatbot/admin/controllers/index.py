from flask import (
    Blueprint, request, render_template
)

bp = Blueprint('admin', __name__, url_prefix='/admin')

from chatbot.admin.domain.tasks.sample import add_together

@bp.route('/')
def index():
    result = add_together.delay(23, 42)
    return render_template('admin/index.html', result=result.wait())
