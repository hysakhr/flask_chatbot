

class TalkResponse():
    def __init__(self, answer, faqs: list = None, static_answers: list = None):
        self.answer = answer
        self.faqs = faqs
        self.static_answers = static_answers

    def build_response(self):
        components = {}

        if self.answer:
            answer = {
                'faq_id': self.answer.id,
                'answer': self.answer.answer
            }

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

        return {
            'components': components
        }
