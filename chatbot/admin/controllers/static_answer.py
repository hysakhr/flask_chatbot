from flask import (
    Blueprint, request, render_template, redirect, url_for
)

from chatbot.admin.domain.repositories.StaticAnswerRepository import IStaticAnswerRepository
from chatbot.admin.domain.repositories.BotRepository import IBotRepository
from chatbot.admin.domain.services.StaticAnswerService import StaticAnswerService
from chatbot.admin.domain.services.BotService import BotService

from chatbot.admin.helpers.forms.StaticAnswerForm import StaticAnswerForm

bp = Blueprint('admin/bot/static_answer', __name__,
               url_prefix='/admin/bot/static_answer')


@bp.route('/add/<int:bot_id>', methods=('GET', 'POST'))
def add(bot_id: int, bot_repository: IBotRepository,
        static_answer_repository: IStaticAnswerRepository):
    bot_service = BotService(bot_repository)
    bot = bot_service.find_by_id(bot_id)

    if bot is None:
        return render_template('/admin/404.html'), 404

    static_answer_service = StaticAnswerService(static_answer_repository)
    static_answer = static_answer_service.get_new_obj(bot_id)

    form = StaticAnswerForm()

    if request.method == 'POST':
        static_answer.name = request.form['name']
        static_answer.answer = request.form['answer']
        static_answer.bot_id = bot_id

        if form.validate_on_submit():
            static_answer_service.save(static_answer)
            return redirect(url_for('admin/bot.detail', id=bot_id))

    return render_template(
        'admin/static_answer/input.html',
        static_answer=static_answer,
        bot=bot,
        form=form,
        operation='追加')


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id: int, static_answer_repository: IStaticAnswerRepository):
    static_answer_service = StaticAnswerService(static_answer_repository)
    static_answer = static_answer_service.find_by_id(id)

    if static_answer is None:
        return render_template('admin/404.html'), 404

    bot = static_answer.bot
    form = StaticAnswerForm()

    if request.method == 'POST':
        static_answer.name = request.form['name']
        static_answer.answer = request.form['answer']

        if form.validate_on_submit():
            static_answer_service.save(static_answer)
            return redirect(url_for('admin/bot.detail', id=bot.id))

    return render_template(
        'admin/static_answer/input.html',
        static_answer=static_answer,
        bot=bot,
        form=form,
        operation='編集')
