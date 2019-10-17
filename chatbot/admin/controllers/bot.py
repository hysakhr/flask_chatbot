import copy
import os
from flask import (
    Blueprint, request, render_template, redirect, url_for, current_app
)

from werkzeug.utils import secure_filename

from chatbot.admin.domain.repositories.BotRepository import IBotRepository
from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.domain.repositories.FaqRepository import IFaqRepository
from chatbot.admin.domain.repositories.StaticAnswerRepository import IStaticAnswerRepository

from chatbot.admin.domain.services.BotService import BotService
from chatbot.admin.domain.services.FaqListService import FaqListService
from chatbot.admin.domain.services.FaqService import FaqService
from chatbot.admin.domain.services.FaqFileImportService import FaqFileImportService

from chatbot.admin.helpers.forms.BotForm import BotForm
from chatbot.admin.helpers.forms.FaqFileUploadForm import FaqFileUploadForm

bp = Blueprint('admin/bot', __name__, url_prefix='/admin/bot')


@bp.route('/')
def index(bot_repository: IBotRepository):
    bot_service = BotService(bot_repository=bot_repository)
    bots = bot_service.get_bots()

    return render_template('admin/bot/index.html', bots=bots)


@bp.route('<int:id>/detail')
def detail(id: int, bot_repository: IBotRepository):
    bot_service = BotService(bot_repository)
    bot = bot_service.find_by_id(id)

    return render_template('admin/bot/detail.html', bot=bot)


@bp.route('/add', methods=('GET', 'POST'))
def add(bot_repository: IBotRepository,
        static_answer_repository: IStaticAnswerRepository):

    bot_service = BotService(bot_repository, static_answer_repository)
    bot = bot_service.get_new_obj()
    form = BotForm()

    if request.method == 'POST':
        bot.name = request.form['name']

        if form.validate_on_submit():
            bot_service.add(bot)
            return redirect(url_for('admin/bot'))

    return render_template(
        'admin/bot/input.html',
        form=form,
        bot=bot,
        operation='追加')


@bp.route('<int:id>/edit', methods=('GET', 'POST'))
def edit(
        id: int,
        bot_repository: IBotRepository):

    # bot data 取得
    bot_service = BotService(bot_repository)
    bot = bot_service.find_by_id(id)

    if bot is None:
        return render_template('admin/404.html'), 404

    form = BotForm()

    if request.method == 'POST':

        bot.name = request.form['name']
        bot.enable_flag = 'enable_flag' in request.form and request.form['enable_flag'] == 'true'

        if form.validate_on_submit():
            bot_service.edit(bot)
            return redirect(url_for('admin/bot.detail', id=id))

    return render_template(
        'admin/bot/input.html',
        form=form,
        bot=bot,
        operation='編集')


@bp.route('<int:id>/fit/<int:faq_list_id>')
def fit(
        id: int,
        faq_list_id: int,
        faq_list_repository: IFaqListRepository,
        bot_repository: IBotRepository):
    # bot data
    bot_service = BotService(bot_repository)
    bot = bot_service.find_by_id(id)

    # faq_list data
    faq_list_service = FaqListService(faq_list_repository)
    faq_list = faq_list_service.find_by_id(faq_list_id)

    # check exist
    if bot is None or faq_list is None:
        return render_template('admin/404.html'), 404

    bot_service.fit(bot_id=id, faq_list_id=faq_list_id)

    return redirect(url_for('admin/bot.detail', id=id))


@bp.route('<int:id>/file_upload', methods=('GET', 'POST'))
def file_upload(
        id: int,
        faq_repository: IFaqRepository,
        faq_list_repository: IFaqListRepository,
        bot_repository: IBotRepository):

    bot_service = BotService(bot_repository)
    bot = bot_service.find_by_id(id)

    if bot is None:
        return render_template('admin/404.html'), 404

    faq_file_import_service = FaqFileImportService(
        faq_repository=faq_repository,
        faq_list_repository=faq_list_repository)
    faq_file_import = faq_file_import_service.get_new_obj(bot=bot)
    form = FaqFileUploadForm()

    if request.method == 'POST':
        faq_file_import.name = request.form['name']

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

            return redirect(url_for('admin/bot.detail', id=id))

    return render_template(
        'admin/faq/file_import.html',
        faq_file_import=faq_file_import,
        form=form)
