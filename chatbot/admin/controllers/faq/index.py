from flask import (
    Blueprint, request, render_template, redirect, url_for
)
from injector import inject

from chatbot.models import FaqList
from chatbot.database import db

from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.domain.services.FaqService import FaqService

bp = Blueprint('admin/faq', __name__, url_prefix='/admin/faq')


@bp.route('/')
def index(faq_list_repository: IFaqListRepository):
    faq_service = FaqService()
    faq_lists = faq_service.getFqaList(faq_list_repository)
    return render_template('admin/faq/index.html', faq_lists=faq_lists)


@bp.route('/new')
def new():
    # for debug endpoint
    # add new record
    faq_list = FaqList.FaqListModel('test2')
    db.session.add(faq_list)
    db.session.commit()
    return redirect(url_for('admin/faq'))
