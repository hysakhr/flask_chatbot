from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, ValidationError


class SiteUrlSettingForm(FlaskForm):
    url_pattern = StringField('URLパターン')
    enable_flag = BooleanField('有効 / 無効')
    static_answer_start = StringField('開始時の固定回答')
    static_answer_not_found = StringField('FAQが見つからない場合の固定回答')

    def validate_url_pattern(self, url_pattern):
        """バリデーション

        - 必須
        - 文字数の上限は1000文字
        """
        if url_pattern.data == '':
            raise ValidationError('必須です。')

        if len(url_pattern.data) > 1000:
            raise ValidationError('1000文字以内で入力してください。')

    def validate_static_answer_start(self, static_answer_start):
        """バリデーション

        - 必須
        """
        if static_answer_start.data == '':
            raise ValidationError('必須です。')

    def validate_static_answer_not_found(self, static_answer_not_found):
        """バリデーション

        - 必須
        """
        if static_answer_not_found.data == '':
            raise ValidationError('必須です。')
