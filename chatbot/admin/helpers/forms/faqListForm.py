from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError


class FaqListForm(FlaskForm):
    name = StringField('名前')

    def validate_name(self, name):
        """バリデーション

        - 必須
        - 文字数の上限は100文字
        """
        if name.data == '':
            raise ValidationError('必須です。')

        if len(name.data) > 10:
            raise ValidationError('255文字以内で入力してください。')
