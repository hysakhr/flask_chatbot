from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, ValidationError


class BotForm(FlaskForm):
    name = StringField('BOT名')
    enable_flag = BooleanField('有効 / 無効')

    def validate_name(self, name):
        """バリデーション

        - 必須
        - 文字数の上限は255文字
        """
        if name.data == '':
            raise ValidationError('必須です。')

        if len(name.data) > 255:
            raise ValidationError('255文字以内で入力してください。')
