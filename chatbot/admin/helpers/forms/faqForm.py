from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, ValidationError


class FaqForm(FlaskForm):
    question = StringField('質問')
    answer = TextAreaField('回答')
    enable_flag = BooleanField('有効 / 無効')

    def validate_question(self, question):
        """バリデーション

        - 必須
        - 文字数の上限は255文字
        """
        if question.data == '':
            raise ValidationError('必須です。')

        if len(question.data) > 255:
            raise ValidationError('255文字以内で入力してください。')

    def validate_answer(self, answer):
        """バリデーション

        - 必須
        - 文字数の上限は1000文字
        """
        if answer.data == '':
            raise ValidationError('必須です。')

        if len(answer.data) > 1000:
            raise ValidationError('1000文字以内で入力してください。')
