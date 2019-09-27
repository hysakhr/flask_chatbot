from flask import Flask


def routes_setting(app: Flask):
    from chatbot.front import index as front
    app.register_blueprint(front.bp)
    app.add_url_rule('/', endpoint='index')

    from chatbot.api import index as api
    app.register_blueprint(api.bp)
    app.add_url_rule('/api', endpoint='api')

    from chatbot.admin.controllers import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule('/admin/auth', endpoint='admin/auth')

    from chatbot.admin.controllers import index as admin
    app.register_blueprint(admin.bp)
    app.add_url_rule('/admin', endpoint='admin')

    from chatbot.admin.controllers import faq_list as admin_faq_list
    app.register_blueprint(admin_faq_list.bp)
    app.add_url_rule('/admin/faq_list', endpoint='admin/faq_list')
