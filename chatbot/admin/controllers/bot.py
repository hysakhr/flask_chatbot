import copy
from flask import (
    Blueprint, request, render_template, redirect, url_for, current_app
)


from chatbot.admin.domain.repositories.BotRepository import IBotRepository
from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.domain.services.BotService import BotService
from chatbot.admin.domain.services.FaqListService import FaqListService
from chatbot.admin.helpers.forms.BotForm import BotForm

bp = Blueprint('admin/bot', __name__, url_prefix='/admin/bot')


@bp.route('/')
def index(bot_repository: IBotRepository):
    bot_service = BotService(bot_repository=bot_repository)
    bots = bot_service.get_bots()

    return render_template('admin/bot/index.html', bots=bots)


@bp.route('/add', methods=('GET', 'POST'))
def add(faq_list_repository: IFaqListRepository,
        bot_repository: IBotRepository):
    # faq_lists data 取得
    faq_list_service = FaqListService(faq_list_repository)
    faq_lists = faq_list_service.get_faq_lists()

    bot_service = BotService(bot_repository)
    bot = bot_service.get_new_obj()
    form = BotForm()

    if request.method == 'POST':
        bot.name = request.form['name']

        if form.validate_on_submit():
            bot_repository.save(bot)
            return redirect(url_for('admin/bot'))

    return render_template(
        'admin/bot/input.html',
        form=form,
        bot=bot,
        faq_lists=faq_lists,
        operation='追加')


@bp.route('<int:id>/edit', methods=('GET', 'POST'))
def edit(
        id: int,
        faq_list_repository: IFaqListRepository,
        bot_repository: IBotRepository):
    # faq_lists data 取得
    faq_list_service = FaqListService(faq_list_repository)
    faq_lists = faq_list_service.get_faq_lists()

    # bot data 取得
    bot_service = BotService(bot_repository)
    bot = bot_service.find_by_id(id)

    if bot is None:
        return render_template('admin/404.html'), 404

    faq_list = bot.faq_list

    form = BotForm()

    if request.method == 'POST':
        # save 前に 更新前後のデータを比較するために更新前のデータを保持
        # sqlalchemy のsession 内で「あるプラ イマリキーに対応するただ一つのオブジェクト」を保持しているため
        # sqlalchemy経由では更新前後のインスタンスを取得できない
        #
        # http://omake.accense.com/static/doc-ja/sqlalchemy/session.html
        # → セッションの役割
        old_bot = copy.deepcopy(bot)

        bot.name = request.form['name']
        bot.faq_list_id = None
        bot.enable_flag = 'enable_flag' in request.form and request.form['enable_flag'] == 'true'

        # faq_list_id チェック
        if request.form['faq_list_id']:
            faq_list_tmp = faq_list_service.find_by_id(
                request.form['faq_list_id'])
            if not faq_list_tmp:
                form.faq_list_id.errors.append('入力内容に誤りがあります。')
            else:
                bot.faq_list_id = int(request.form['faq_list_id'])

        if form.validate_on_submit():
            bot_service.save(bot, old_bot)
            return redirect(url_for('admin/bot'))

    return render_template(
        'admin/bot/input.html',
        faq_list=faq_list,
        faq_lists=faq_lists,
        form=form,
        bot=bot,
        operation='編集')


@bp.route('<int:id>/fit')
def fit(
        id: int,
        faq_list_repository: IFaqListRepository,
        bot_repository: IBotRepository):
    # bot data
    bot_service = BotService(bot_repository)
    bot_service.fit(bot_id=id)

    return redirect(url_for('admin/bot'))
