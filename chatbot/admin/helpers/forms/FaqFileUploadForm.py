from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, ValidationError
from werkzeug.utils import secure_filename

from flask import current_app


class FaqFileUploadForm(FlaskForm):
    name = StringField('FAQリスト名')
    faq_list = FileField('FAQファイル')

    def validate_name(self, name):
        """バリデーション

        - 必須
        - 文字数の上限は255文字
        """
        if name.data == '':
            raise ValidationError('必須です。')

        if len(name.data) > 255:
            raise ValidationError('255文字以内で入力してください。')

    def validate_faq_list(self, faq_list):
        """バリデーション

        - 必須
        - 拡張子はtsv
        """
        if 'faq_list' not in request.files:
            raise ValidationError('必須です。')

        file = request.files['faq_list']
        filename = secure_filename(file.filename)
        ext = filename.split('.')[-1]
        if ext != 'tsv':
            raise ValidationError('拡張子は tsv にしてください。')
