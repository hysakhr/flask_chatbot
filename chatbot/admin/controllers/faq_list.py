from flask import (
    Blueprint, request, render_template, redirect, url_for, current_app
)
from injector import inject

from chatbot.models import FaqList
from chatbot.database import db

from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.domain.services.FaqListService import FaqListService
from chatbot.admin.helpers.forms.faqListForm import FaqListForm

bp = Blueprint('admin/faq_list', __name__, url_prefix='/admin/faq_list')


@bp.route('/')
def index(faq_list_repository: IFaqListRepository):
    faq_service = FaqListService(faq_list_repository)
    faq_lists = faq_service.get_faq_lists()
    return render_template('admin/faq_list/index.html', faq_lists=faq_lists)


@bp.route('/new')
def new():
    # for debug endpoint
    # add new record
    # faq_list = FaqList.FaqListModel('test2')
    # db.session.add(faq_list)
    # db.session.commit()
    return redirect(url_for('admin/faq_list'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id: int, faq_list_repository: IFaqListRepository):
    faq_service = FaqListService(faq_list_repository)
    faq_list = faq_service.find_by_id(
        id=id)

    form = FaqListForm()
    if request.method == 'POST':
        faq_list.name = request.form['name']

        # validation
        if form.validate_on_submit():
            # save
            faq_service.save(faq_list)
            return redirect(url_for('admin/faq_list'))
    return render_template(
        'admin/faq_list/update.html',
        faq_list=faq_list,
        form=form)