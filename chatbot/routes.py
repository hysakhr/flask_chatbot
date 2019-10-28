from flask import Flask


def routes_setting(app: Flask):
    #############################
    # from
    #############################
    from chatbot.front import index as front
    app.register_blueprint(front.bp)
    app.add_url_rule('/', endpoint='index')

    #############################
    # api
    #############################
    from chatbot.api.controllers import talk as api_talk
    app.register_blueprint(api_talk.bp)
    app.add_url_rule('/api/talk', endpoint='api/talk')

    #############################
    # admin
    #############################
    from chatbot.admin.controllers import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule('/admin/auth', endpoint='admin/auth')

    # dash board
    from chatbot.admin.controllers import index as admin
    app.register_blueprint(admin.bp)
    app.add_url_rule('/admin', endpoint='admin')

    # faq list
    from chatbot.admin.controllers import faq_list as admin_faq_list
    app.register_blueprint(admin_faq_list.bp)
    app.add_url_rule('/admin/faq_list', endpoint='admin/faq_list')

    from chatbot.admin.controllers import faq as admin_faq
    app.register_blueprint(admin_faq.bp)
    app.add_url_rule('/admin/faq', endpoint='admin/faq')

    # bot
    from chatbot.admin.controllers import bot as admin_bot
    app.register_blueprint(admin_bot.bp)
    app.add_url_rule('/admin/bot', endpoint='admin/bot')

    # site
    from chatbot.admin.controllers import site as admin_site
    app.register_blueprint(admin_site.bp)
    app.add_url_rule('/admin/site', endpoint='admin/site')

    from chatbot.admin.controllers import site_url_setting as admin_site_url_setting
    app.register_blueprint(admin_site_url_setting.bp)
    app.add_url_rule('/admin/site', endpoint='admin/site/url_setting')
