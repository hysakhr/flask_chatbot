from flask import (
    Blueprint, request, jsonify
)

from chatbot.api.domain.repositories.FaqRepository import IFaqRepository
from chatbot.api.domain.services.FaqService import FaqService
from chatbot.api.domain.repositories.SiteRepository import ISiteRepository
from chatbot.api.domain.services.SiteService import SiteService
from chatbot.api.domain.services.TalkService import TalkService
from chatbot.api.domain.repositories.BotRepository import IBotRepository
from chatbot.api.domain.services.BotService import BotService

from chatbot.api.helpers.responses.Talk import TalkResponse

bp = Blueprint('api/talk', __name__, url_prefix='/api/talk')


@bp.route('', methods=('POST',))
def talk(faq_repository: IFaqRepository,
         site_repository: ISiteRepository,
         bot_repository: IBotRepository):

    # 応答に必要な共通変数の準備
    site_id = request.json['site_id']
    site_service = SiteService(site_repository)
    url_setting = site_service.find_url_setting(
        site_id=site_id, url=request.url)

    if url_setting is None:
        talk_response = TalkResponse(error_message='url_setting not found.')
        res = talk_response.build_error_message()
        return jsonify(res), 404

    bot_service = BotService(bot_repository)
    bot = bot_service.find_by_id(url_setting.bot_id)

    if bot is None:
        talk_response = TalkResponse(error_message='bot not found.')
        res = talk_response.build_error_message()
        return jsonify(res), 404

    faq_service = FaqService(faq_repository)

    if request.json['type'] == 'freeText':

        # 入力をもとに返信すべきfaq_idを決定
        query = request.json['query']

        talk_service = TalkService()
        faq_id, top_faq_ids = talk_service.think(bot_id=bot.id, query=query)

        # faq_id をもとに返信用データ作成

        if faq_id:
            faq = faq_service.find_by_id(faq_id)

            # 返信
            talk_response = TalkResponse(faq, faq.related_faqs)
            res = talk_response.build_response()
        else:
            # 候補となるFAQの取得
            faqs = faq_service.get_list_by_ids(top_faq_ids)

            # not_found時の固定回答取得
            static_answer = url_setting.get_static_answer(key='not_found')

            # 返信
            talk_response = TalkResponse(static_answer, faqs)
            res = talk_response.build_response()

    elif request.json['type'] == 'question':
        faq_id = request.json['faq_id']

        # faq_id をもとに返信用データ作成
        faq = faq_service.find_by_id(faq_id)

        if faq is None:
            talk_response = TalkResponse(
                error_message='faq not found.')
            res = talk_response.build_error_message()
            return jsonify(res), 404
        else:
            # 返信
            talk_response = TalkResponse(faq, faq.get_enable_related_faqs())
            res = talk_response.build_response()

    elif request.json['type'] == 'staticAnswer':
        # static_query をもとに返信用データ作成
        name = request.json['name']
        static_answer = bot.get_static_answer(name)

        if static_answer.enable_flag is False:
            talk_response = TalkResponse(
                error_message='static answer not found.')
            res = talk_response.build_error_message()
            return jsonify(res), 404
        else:
            # 返信
            talk_response = TalkResponse(
                static_answer, static_answer.get_enable_related_faqs())
            res = talk_response.build_response()

    else:
        return jsonify({'error': 'type error'})

    return jsonify(res)
