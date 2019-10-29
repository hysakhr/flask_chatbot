from flask import (
    Flask, request
)
from injector import inject

# admin
from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.infrastructure.FaqListRepositoryImpl import FaqListRepositoryImpl
from chatbot.admin.domain.repositories.FaqRepository import IFaqRepository
from chatbot.admin.infrastructure.FaqRepositoryImpl import FaqRepositoryImpl
from chatbot.admin.domain.repositories.BotRepository import IBotRepository
from chatbot.admin.infrastructure.BotRepositoryImpl import BotRepositoryImpl

from chatbot.admin.domain.repositories.SiteRepository import ISiteRepository
from chatbot.admin.infrastructure.SiteRepositoryImpl import SiteRepositoryImpl
from chatbot.admin.domain.repositories.SiteUrlSettingRepository import ISiteUrlSettingRepository
from chatbot.admin.infrastructure.SiteUrlSettingRepositoryImpl import SiteUrlSettingRepositoryImpl

# api
from chatbot.api.domain.repositories.FaqRepository import IFaqRepository as IFaqRepository_api
from chatbot.api.infrastructure.FaqRepositoryImpl import FaqRepositoryImpl as FaqRepositoryImpl_api
from chatbot.api.domain.repositories.SiteRepository import ISiteRepository as ISiteRepository_api
from chatbot.api.infrastructure.SiteRepositoryImpl import SiteRepositoryImpl as SiteRepositoryImpl_api
from chatbot.api.domain.repositories.BotRepository import IBotRepository as IBotRepository_api
from chatbot.api.infrastructure.BotRepositoryImpl import BotRepositoryImpl as BotRepositoryImpl_api
from chatbot.api.domain.repositories.TalkLogReposiroty import ITalkLogRepository as ITalkLogRepository_api
from chatbot.api.infrastructure.TalkLogRepositoryImpl import TalkLogRepositoryImpl as TalkLogRepositoryImpl_api


def configure(binder):
    # admin
    binder.bind(IFaqListRepository, to=FaqListRepositoryImpl, scope=request)
    binder.bind(IFaqRepository, to=FaqRepositoryImpl, scope=request)
    binder.bind(IBotRepository, to=BotRepositoryImpl, scope=request)
    binder.bind(ISiteRepository, to=SiteRepositoryImpl, scope=request)
    binder.bind(
        ISiteUrlSettingRepository,
        to=SiteUrlSettingRepositoryImpl,
        scope=request)

    # api
    binder.bind(IFaqRepository_api, to=FaqRepositoryImpl_api, scope=request)
    binder.bind(ISiteRepository_api, to=SiteRepositoryImpl_api, scope=request)
    binder.bind(IBotRepository_api, to=BotRepositoryImpl_api, scope=request)
    binder.bind(
        ITalkLogRepository_api,
        TalkLogRepositoryImpl_api,
        scope=request)
