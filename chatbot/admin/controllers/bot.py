from flask import (
    Blueprint, request, render_template, redirect, url_for, current_app
)


from chatbot.admin.domain.repositories.BotRepository import IBotRepository
from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.domain.services.BotService import BotService
from chatbot.admin.domain.services.FaqListService import FaqListService
from chatbot.admin.helpers.forms.BotForm import BotForm

bp = Blueprint('admin/bot', __name__, url_prefix='/admin/bot')


@bp.route('<int:faq_list_id>/list')
def list(
        faq_list_id: int,
        faq_list_repository: IFaqListRepository,
        bot_repository: IBotRepository):
    # faq_list data 取得
    faq_list_service = FaqListService(faq_list_repository)
    faq_list = faq_list_service.find_by_id(faq_list_id)

    # bot data 取得
    bot_service = BotService(bot_repository)
    bots = bot_service.get_bots_by_faq_list_id(faq_list_id)

    return render_template('admin/bot/list.html', faq_list=faq_list, bots=bots)


@bp.route('<int:faq_list_id>/add', methods=('GET', 'POST'))
def add(
        faq_list_id: int,
        faq_list_repository: IFaqListRepository,
        bot_repository: IBotRepository):
    # faq_list data 取得
    faq_list_service = FaqListService(faq_list_repository)
    faq_list = faq_list_service.find_by_id(faq_list_id)

    if faq_list is None:
        return render_template('admin/404.html'), 404

    bot_service = BotService(bot_repository)
    bot = bot_service.get_new_obj(faq_list_id=faq_list_id)
    form = BotForm()

    if request.method == 'POST':
        bot.name = request.form['name']

        if form.validate_on_submit():
            bot_repository.save(bot)
            return redirect(url_for('admin/bot.list', faq_list_id=faq_list_id))

    return render_template(
        'admin/bot/input.html',
        faq_list=faq_list,
        form=form,
        bot=bot,
        operation='追加')


@bp.route('<int:id>/edit', methods=('GET', 'POST'))
def edit(
        id: int,
        faq_list_repository: IFaqListRepository,
        bot_repository: IBotRepository):
    # bot data 取得
    bot_service = BotService(bot_repository)
    bot = bot_service.find_by_id(id)

    if bot is None:
        return render_template('admin/404.html'), 404

    faq_list = bot.faq_list

    form = BotForm()

    if request.method == 'POST':
        bot.name = request.form['name']
        bot.enable_flag = 'enable_flag' in request.form and request.form['enable_flag'] == 'true'

        if form.validate_on_submit():
            bot_service.save(bot)
            return redirect(url_for('admin/bot.list', faq_list_id=faq_list.id))

    return render_template(
        'admin/bot/input.html',
        faq_list=faq_list,
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
    bot = bot_service.find_by_id(id)

    return redirect(url_for('admin/bot.list', faq_list_id=bot.faq_list_id))
