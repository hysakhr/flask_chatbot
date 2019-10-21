from flask import (
    Blueprint, redirect, render_template, request, current_app
)

from chatbot.admin.domain.repositories.SiteRepository import ISiteRepository
from chatbot.admin.domain.services.SiteService import SiteService
from chatbot.admin.domain.repositories.BotRepository import IBotRepository
from chatbot.admin.domain.services.BotService import BotService

from chatbot.admin.domain.repositories.SiteUrlSettingRepository import ISiteUrlSettingRepository
from chatbot.admin.domain.services.SiteUrlSettingService import SiteUrlSettingService
from chatbot.admin.helpers.forms.SiteUrlSettingForm import SiteUrlSettingForm

bp = Blueprint('admin/site/url_setting', __name__, url_prefix='/admin/site')


@bp.route('<int:site_id>/url_setting/add', methods=('GET', 'POST'))
def add(site_id: int, site_repository: ISiteRepository,
        site_url_setting_repository: ISiteUrlSettingRepository,
        bot_repository: IBotRepository):
    site_service = SiteService(site_repository)
    site = site_service.find_by_id(site_id)

    if site is None:
        return render_template('admin/404.html'), 404

    site_url_setting_service = SiteUrlSettingService(
        site_url_setting_repository)
    site_url_setting = site_url_setting_service.get_new_obj(site_id=site_id)
    static_answers = {
        'start': '',
        'not_found': ''
    }

    bot_service = BotService(bot_repository)
    bots = bot_service.get_bots()

    form = SiteUrlSettingForm()

    if request.method == 'POST':
        site_url_setting.url_pattern = request.form['url_pattern']
        site_url_setting.bot_id = request.form['bot_id']
        site_url_setting.enable_flag = 'enable_flag' in request.form and request.form[
            'enable_flag'] == 'true'
        static_answers['start'] = request.form['static_answer_start']
        static_answers['not_found'] = request.form['static_answer_not_found']

        if form.validate_on_submit():
            site_url_setting_service.add(site_url_setting, static_answers)
            return redirect('/admin/site')

    return render_template(
        'admin/site_url_setting/input.html',
        site=site,
        site_url_setting=site_url_setting,
        static_answers=static_answers,
        bots=bots,
        form=form,
        operation='追加')


@bp.route('/url_setting/<int:id>/edit', methods=('GET', 'POST'))
def edit(
        id: int,
        site_url_setting_repository: ISiteUrlSettingRepository,
        bot_repository: IBotRepository):
    site_url_setting_service = SiteUrlSettingService(
        site_url_setting_repository)
    site_url_setting = site_url_setting_service.find_by_id(id)
    site = site_url_setting.site
    static_answers = {
        'start': site_url_setting.static_answers['start'],
        'not_found': site_url_setting.static_answers['not_found'],
    }

    bot_service = BotService(bot_repository)
    bots = bot_service.get_bots()

    form = SiteUrlSettingForm()

    if request.method == 'POST':
        site_url_setting.url_pattern = request.form['url_pattern']
        site_url_setting.bot_id = request.form['bot_id']
        site_url_setting.enable_flag = 'enable_flag' in request.form and request.form[
            'enable_flag'] == 'true'
        static_answers['start'] = request.form['static_answer_start']
        static_answers['not_found'] = request.form['static_answer_not_found']

        if form.validate_on_submit():
            site_url_setting_service.edit(site_url_setting, static_answers)
            return redirect('/admin/site')

    return render_template(
        'admin/site_url_setting/input.html',
        site=site,
        site_url_setting=site_url_setting,
        static_answers=static_answers,
        bots=bots,
        form=form,
        operation='編集')
