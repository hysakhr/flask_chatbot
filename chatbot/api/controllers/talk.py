import uuid
from flask import (
    Blueprint, request, jsonify, session
)

from chatbot.api.domain.repositories.FaqRepository import IFaqRepository
from chatbot.api.domain.services.FaqService import FaqService
from chatbot.api.domain.repositories.SiteRepository import ISiteRepository
from chatbot.api.domain.services.SiteService import SiteService
from chatbot.api.domain.repositories.BotRepository import IBotRepository
from chatbot.api.domain.services.BotService import BotService
from chatbot.api.domain.repositories.TalkLogReposiroty import ITalkLogRepository
from chatbot.api.domain.services.TalkService import TalkService

from chatbot.api.helpers.responses.Talk import TalkResponse

from chatbot.api.exceptions.NotFoundException import NotFoundException
from chatbot.common.Debug import flush

bp = Blueprint('api/talk', __name__, url_prefix='/api/talk')


@bp.route('', methods=('POST',))
def talk(faq_repository: IFaqRepository,
         site_repository: ISiteRepository,
         bot_repository: IBotRepository,
         talk_log_repository: ITalkLogRepository):
    status_code = 200
    res = {}
    error_message = ''
    bot_id = None
    talk_response = None
    top_faq_info_list = None

    if 'session_id' not in session:
        session['session_id'] = uuid.uuid4()

    flush('session_id is {}'.format(session['session_id']))
    talk_service = TalkService(talk_log_repository)

    try:
        # 応答に必要な共通変数の準備
        site_id = request.json['site_id']
        site_service = SiteService(site_repository)
        url_setting = site_service.find_url_setting(
            site_id=site_id, url=request.url)

        if url_setting is None:
            raise NotFoundException('url_setting not found.')

        bot_service = BotService(bot_repository)
        bot = bot_service.find_by_id(url_setting.bot_id)

        if bot is None:
            raise NotFoundException('bot not found.')

        faq_service = FaqService(faq_repository)
        bot_id = bot.id

        if request.json['type'] == 'freeText':

            # 入力をもとに返信すべきfaq_idを決定
            query = request.json['query']

            faq_id, top_faq_ids, top_faq_info_list = talk_service.think(
                bot_id=bot.id, query=query)

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
                static_answer = url_setting.bot.get_static_answer('not_found')

                if static_answer is None:
                    raise NotFoundException(
                        'static answer not found. name: not_found')

                # 返信
                talk_response = TalkResponse(static_answer, faqs)
                res = talk_response.build_response()

        elif request.json['type'] == 'question':
            faq_id = request.json['faq_id']

            # faq_id をもとに返信用データ作成
            faq = faq_service.find_by_id(faq_id)

            if faq is None:
                raise NotFoundException('faq not found.')
            else:
                # 返信
                talk_response = TalkResponse(
                    faq, faq.get_enable_related_faqs())
                res = talk_response.build_response()

        elif request.json['type'] == 'staticAnswer':
            # static_query をもとに返信用データ作成
            name = request.json['name']
            static_answer = bot.get_static_answer(name)

            if static_answer.enable_flag is False:
                raise NotFoundException('static answer not found.')
            else:
                # 返信
                talk_response = TalkResponse(
                    static_answer, static_answer.get_enable_related_faqs())
                res = talk_response.build_response()

        else:
            raise NotFoundException('type error')
    except NotFoundException as e:
        res = {'error': 'not found.'}
        status_code = 404
        error_message = e.__str__()
        talk_response = TalkResponse(error_message=error_message)
    except BaseException as e:
        res = {'error': 'internal server error.'}
        status_code = 500
        error_message = e.__str__()
        talk_response = TalkResponse(error_message=error_message)

    # log 出力
    talk_service.add_talk_log(
        request=request,
        response=talk_response,
        top_faq_info_list=top_faq_info_list,
        bot_id=bot_id,
        session_id=str(session['session_id']))

    return jsonify(res), status_code
