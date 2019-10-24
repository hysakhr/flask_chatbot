from chatbot.common.Talk import parse, get_ml_vars, get_ml_model, create_input
import numpy as np

from chatbot.common.Debug import flush


class TalkService:
    def __init__(self):
        pass

    def think(
            self,
            bot_id: int,
            query: str,
            top_count: int = 5,
            threshold: float = 0.3):

        # 変数の読み込み
        vars = get_ml_vars(bot_id)
        model = get_ml_model(bot_id)

        info, word_set = parse(query)
        input = create_input(word_to_id=vars['word_to_id'], word_set=word_set)
        input = np.array([input])

        result = model.predict(input)[0]
        index = int(np.argmax(result))
        rank = np.argsort(-result)

        top = []
        top_faq_ids = []
        for i in range(top_count):
            b = int(rank[i])
            faq = vars['faq_info_list'][b]
            faq['score'] = float(result[b])
            top.append(faq)
            top_faq_ids.append(faq['faq_id'])

        # self.dump(vars, info, word_set, input, result, rank, top)

        # flush(top[0]['score'])
        # flush(threshold)
        if top[0]['score'] > threshold:
            return vars['faq_info_list'][index]['faq_id'], None
        else:
            return None, top_faq_ids

    def dump(self, vars, info, word_set, input, result, rank, top):
        flush('info : {}'.format(info))
        flush('word_set : {}'.format(word_set))
        flush('input : {}'.format(input))
        flush('input.shape : {}'.format(input.shape))
        flush('word_to_id : {}'.format(vars['word_to_id']))
        flush('result: {}'.format(result))
        flush('argmax ; {}'.format(np.argmax(result)))
        flush('argsort ; {}'.format(np.argsort(result)))
        flush('rank : {}'.format(rank))
        flush('top : {}'.format(top))

        for no, i in enumerate(np.argsort(-result)):
            i = int(i)
            if no > 5:
                break

            flush('no {}: index: {} score: {:5.2f}'.format(
                no + 1, i, (result[i] * 100)))
