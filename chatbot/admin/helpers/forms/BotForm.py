from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, ValidationError


class BotForm(FlaskForm):
    name = StringField('BOT名')
    faq_list_id = StringField('FAQリスト')
    enable_flag = BooleanField('有効 / 無効')

    def validation_name(self, name):
        """バリデーション

        - 必須
        - 文字数の上限は255文字
        """
        if name.data == '':
            raise ValidationError('必須です。')

        if len(name.date) > 255:
            raise ValidationError('255文字以内で入力してください。')

    def validation_faq_list_id(self, faq_list_id):
        """バリデーション

        - 任意
        - 数字
        """

        if faq_list_id.data == "":
            return

        if not faq_list_id.data.isdigit():
            raise ValidationError('入力内容に誤りがあります。')
