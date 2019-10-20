from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, ValidationError


class SiteUrlSettingForm(FlaskForm):
    url_pattern = StringField('URLパターン')
    enable_flag = BooleanField('有効 / 無効')

    def validate_url_pattern(self, url_pattern):
        """バリデーション

        - 必須
        - 文字数の上限は1000文字
        """
        if url_pattern.data == '':
            raise ValidationError('必須です。')

        if len(url_pattern.data) > 1000:
            raise ValidationError('1000文字以内で入力してください。')
