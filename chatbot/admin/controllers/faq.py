import os

from flask import (
    Blueprint, request, render_template, redirect, url_for, current_app
)
from werkzeug.utils import secure_filename

from chatbot.admin.domain.repositories.FaqRepository import IFaqRepository
from chatbot.admin.domain.services.FaqService import FaqService
from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.domain.services.FaqListService import FaqListService
from chatbot.admin.domain.services.FaqFileImportService import FaqFileImportService
from chatbot.admin.helpers.forms.FaqForm import FaqForm
from chatbot.admin.helpers.forms.FaqFileUploadForm import FaqFileUploadForm

bp = Blueprint('admin/faq', __name__, url_prefix='/admin/faq')


@bp.route('/<int:faq_list_id>/list')
def list(
        faq_list_id: int,
        faq_list_repository: IFaqListRepository,
        faq_repository: IFaqRepository):
    # faq_list data 取得
    faq_list_service = FaqListService(faq_list_repository)
    faq_list = faq_list_service.find_by_id(id=faq_list_id)

    # faq data 取得
    faq_service = FaqService(faq_repository)
    faqs = faq_service.get_faqs_by_faq_list_id(faq_list_id)

    return render_template('admin/faq/list.html', faq_list=faq_list, faqs=faqs)


@bp.route('/new')
def new():
    from chatbot.models.Faq import FaqModel
    from chatbot.database import db
    faq = FaqModel('q', 'a', 'q_ord', 'a_org', 1)
    db.session.add(faq)
    db.session.commit()
    return redirect(url_for('admin/faq/1/list'))


@bp.route('<int:faq_list_id>/add', methods=('GET', 'POST'))
def add(
        faq_list_id: int,
        faq_list_repository: IFaqListRepository,
        faq_repository: IFaqRepository):
    # faq_list data 取得
    faq_list_service = FaqListService(faq_list_repository)
    faq_list = faq_list_service.find_by_id(id=faq_list_id)

    if faq_list is None:
        return render_template('admin/404.html'), 404

    faq_service = FaqService(faq_repository)
    form = FaqForm()
    faq = faq_service.get_new_obj(faq_list_id=faq_list_id)

    if request.method == 'POST':
        faq.answer = request.form['answer']
        faq.question = request.form['question']
        faq.enable_flag = 'enable_flag' in request.form and request.form['enable_flag'] == 'true'

        if form.validate_on_submit():
            faq_service.save(faq)
            return redirect(url_for('admin/faq.list', faq_list_id=faq_list_id))

    return render_template(
        'admin/faq/input.html',
        faq_list=faq_list,
        faq=faq,
        form=form,
        operation="新規作成")


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(
        id: int,
        faq_list_repository: IFaqListRepository,
        faq_repository: IFaqRepository):
    # faq data 取得
    faq_service = FaqService(faq_repository)
    faq = faq_service.find_by_id(id)

    if faq is None:
        return render_template('admin/404.html'), 404

    # faq_list data 取得
    faq_list = faq.faq_list

    form = FaqForm()

    if request.method == 'POST':
        faq.answer = request.form['answer']
        faq.question = request.form['question']
        faq.enable_flag = 'enable_flag' in request.form and request.form['enable_flag'] == 'true'

        if form.validate_on_submit():
            faq_service.save(faq)
            return redirect(url_for('admin/faq.list', faq_list_id=faq_list.id))

    return render_template(
        'admin/faq/input.html',
        faq_list=faq_list,
        faq=faq,
        form=form,
        operation="編集")


@bp.route('/file_upload', methods=('GET', 'POST'))
def file_upload(faq_repository: IFaqRepository,
                faq_list_repository: IFaqListRepository):
    faq_file_import_service = FaqFileImportService(
        faq_repository=faq_repository,
        faq_list_repository=faq_list_repository)
    faq_file_import = faq_file_import_service.get_new_obj()
    form = FaqFileUploadForm()

    current_app.logger.debug(current_app.config)
    current_app.logger.debug(current_app.config['FAQ_FILE_UPLOAD_DIR'])

    if request.method == 'POST':
        faq_file_import.name = request.form['name']

        current_app.logger.debug(request.form)
        current_app.logger.debug(request.files)
        if form.validate_on_submit():
            # build file_path
            file = request.files['faq_list']
            filename = secure_filename(file.filename)
            file_path = os.path.join(
                current_app.config['FAQ_FILE_UPLOAD_DIR'], filename)
            # file save
            file.save(file_path)
            faq_file_import.file_path = file_path

            # import
            faq_file_import_service.import_tsv(faq_file_import)

            return redirect(url_for('admin/faq_list'))

    return render_template(
        'admin/faq/file_import.html',
        faq_file_import=faq_file_import,
        form=form)
