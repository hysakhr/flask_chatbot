
def init_celery(celery, app):
    config = {
        'imports': app.config['CELERY_IMPORTS']
    }
    celery.conf.update(config)
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
