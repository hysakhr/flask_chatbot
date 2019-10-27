from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError


class FaqListForm(FlaskForm):
    name = StringField('名前')
    start_faq_id = StringField('開始時に表示するFAQ')
    not_found_faq_id = StringField('見つからない場合に表示するFAQ')

    def validate_name(self, name):
        """バリデーション

        - 必須
        - 文字数の上限は100文字
        """
        if name.data == '':
            raise ValidationError('必須です。')

        if len(name.data) > 255:
            raise ValidationError('255文字以内で入力してください。')

    def validate_start_faq_id(self, faq_id):
        """バリデーション

        - 必須
        """
        if faq_id.data == '':
            raise ValidationError('必須です。')

    def validate_not_found_faq_id(self, faq_id):
        """バリデーション

        - 必須
        """
        if faq_id.data == '':
            raise ValidationError('必須です。')
