from flask import current_app


class TalkResponse():
    def __init__(
            self,
            answer=None,
            faqs: list = None,
            static_answers: list = None,
            error_message: str = '',
            show_faq_info: bool = False):
        self.answer = answer
        self.faqs = faqs
        self.static_answers = static_answers
        self.error_message = error_message
        self.show_faq_info = show_faq_info

    def build_response(self):
        components = {}

        if self.answer:
            answer = {
                'faq_id': self.answer.id,
                'answer': self.answer.answer,
                'question': self.answer.question
            }

            if self.show_faq_info:
                answer['answer'] = 'faq_id: {}<br>question: {}<br><br>{}'.format(
                    self.answer.id, self.answer.question, self.answer.answer)

            components['answer'] = answer

        if self.faqs:
            faqs = []
            for faq in self.faqs:
                faq_res = {
                    'faq_id': faq.id,
                    'question': faq.question
                }
                faqs.append(faq_res)

            components['questionList'] = faqs

        if self.static_answers:
            static_answers = []

            for answer in self.static_answers:
                static_answer = {
                    'id': answer.id,
                    'name': answer.name,
                    'displayText': answer.display_text
                }

                static_answers.append(static_answer)

            components['staticAnswerList']

        return components

    def build_error_message(self):
        return {'error': self.error_message}
