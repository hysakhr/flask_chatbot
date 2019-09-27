from flask import (
    Blueprint, request, render_template, redirect, url_for, current_app
)

from chatbot.admin.domain.repositories.FaqRepository import IFaqRepository
from chatbot.admin.domain.services.FaqService import FaqService
# from chatbot.admin.helpers.forms.faqForm import FaqForm

bp = Blueprint('admin/faq', __name__, url_prefix='/admin/faq')


@bp.route('/<int:faq_list_id>/list')
def list(faq_list_id: int, faq_repository: IFaqRepository):
    faq_service = FaqService(faq_repository)
    faqs = faq_service.get_faqs_by_faq_list_id(faq_list_id)
    return render_template('admin/faq/list.html', faqs=faqs)


@bp.route('/new')
def new():
    from chatbot.models.Faq import FaqModel
    from chatbot.database import db
    faq = FaqModel('q', 'a', 'q_ord', 'a_org', 1)
    db.session.add(faq)
    db.session.commit()
    return redirect(url_for('admin/faq/1/list'))


@bp.route('/<int:id>/edit')
def edit(id: int, faq_repository: IFaqRepository):
    pass
