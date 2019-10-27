from flask import (
    Blueprint, request, render_template, redirect, url_for, current_app
)

from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.domain.services.FaqListService import FaqListService
from chatbot.admin.helpers.forms.FaqListForm import FaqListForm
from chatbot.admin.domain.repositories.FaqRepository import IFaqRepository

bp = Blueprint('admin/faq_list', __name__, url_prefix='/admin/faq_list')


@bp.route('/')
def index(faq_list_repository: IFaqListRepository):
    faq_list_service = FaqListService(faq_list_repository)
    faq_lists = faq_list_service.get_faq_lists()
    return render_template('admin/faq_list/index.html', faq_lists=faq_lists)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(
        id: int,
        faq_list_repository: IFaqListRepository,
        faq_repository: IFaqRepository):
    faq_list_service = FaqListService(faq_list_repository, faq_repository)
    faq_list = faq_list_service.find_by_id(
        id=id)

    form = FaqListForm()
    if request.method == 'POST':
        faq_list.name = request.form['name']
        faq_list.start_faq_id = request.form['start_faq_id']
        faq_list.not_found_faq_id = request.form['not_found_faq_id']

        # validation
        if form.validate_on_submit():
            # save
            faq_list_service.edit(faq_list)
            return redirect(url_for('admin/bot.detail', id=faq_list.bot.id))
    return render_template(
        'admin/faq_list/input.html',
        faq_list=faq_list,
        form=form)
