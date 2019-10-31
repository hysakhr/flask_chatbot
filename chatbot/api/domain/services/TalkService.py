import numpy as np
from flask import request
from chatbot.common.Debug import flush
from chatbot.common.Talk import parse, get_ml_vars, get_ml_model, create_input
from chatbot.api.helpers.responses.Talk import TalkResponse
from chatbot.models.TalkLog import TalkLogModel
from chatbot.api.domain.repositories.TalkLogReposiroty import ITalkLogRepository


class TalkService:
    def __init__(self, talk_log_repository: ITalkLogRepository):
        self.talk_log_repository = talk_log_repository

    def think(
            self,
            bot_id: int,
            query: str,
            top_count: int = 5,
            threshold: float = 0.5):

        # 変数の読み込み
        vars = get_ml_vars(bot_id)
        model = get_ml_model(bot_id)

        info, word_set = parse(query)
        input = create_input(word_to_id=vars['word_to_id'], word_set=word_set)
        input = np.array([input])

        result = model.predict(input)[0]
        # index = int(np.argmax(result)) # topのみ取得する場合
        rank = np.argsort(-result)

        top_faq_ids = []
        top_faq_info_list = []
        for i in range(top_count):
            target_index = int(rank[i])
            faq_info = vars['faq_info_list'][target_index]
            faq_info['score'] = float(result[target_index])

            top_faq_ids.append(faq_info['faq_id'])
            top_faq_info_list.append(faq_info)

        self.dump(
            vars,
            info,
            word_set,
            input,
            result,
            rank,
            top_faq_info_list[0])

        if top_faq_info_list[0]['score'] > threshold:
            return top_faq_info_list[0]['faq_id'], None, top_faq_info_list
        else:
            return None, top_faq_ids, top_faq_info_list

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

    def add_talk_log(
            self,
            request: request,
            response: TalkResponse,
            top_faq_info_list: list,
            bot_id: int,
            session_id: str):
        talk_log = TalkLogModel(
            request=request,
            response=response,
            top_faq_info_list=top_faq_info_list,
            bot_id=bot_id,
            session_id=session_id)
        return self.talk_log_repository.add(talk_log)
