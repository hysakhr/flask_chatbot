from flask import (
    Blueprint, request, render_template, redirect, url_for, current_app
)

from chatbot.admin.domain.repositories.SiteRepository import ISiteRepository
from chatbot.admin.domain.services.SiteService import SiteService
from chatbot.admin.helpers.forms.SiteForm import SiteForm


bp = Blueprint('admin/site', __name__, url_prefix='/admin/site')


@bp.route('/')
def index(site_repository: ISiteRepository):
    site_service = SiteService(site_repository)
    sites = site_service.get_sites()

    return render_template('admin/site/index.html', sites=sites)


@bp.route('/add', methods=('GET', 'POST'))
def add(site_repository: ISiteRepository):
    site_service = SiteService(site_repository)
    site = site_service.get_new_obj()

    form = SiteForm()

    if request.method == 'POST':
        site.name = request.form['name']
        site.enable_flag = 'enable_flag' in request.form and request.form[
            'enable_flag'] == 'true'

        if form.validate_on_submit():
            site_service.add(site)
            return redirect(url_for('admin/site'))

    return render_template(
        'admin/site/input.html',
        site=site,
        form=form,
        operation='追加')


@bp.route('<int:id>/edit', methods=('GET', 'POST'))
def edit(id: int, site_repository: ISiteRepository):
    site_service = SiteService(site_repository)
    site = site_service.find_by_id(id)

    if site is None:
        return render_template('admin/404.html'), 404

    form = SiteForm()

    if request.method == 'POST':
        site.name = request.form['name']
        site.enable_flag = 'enable_flag' in request.form and request.form[
            'enable_flag'] == 'true'

        if form.validate_on_submit():
            site_service.edit(site)
            return redirect(url_for('admin/site'))

    return render_template(
        'admin/site/input.html',
        site=site,
        form=form,
        operation='編集')
