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
from chatbot.admin.domain.repositories.StaticAnswerRepository import IStaticAnswerRepository
from chatbot.admin.infrastructure.StaticAnswerRepositoryImpl import StaticAnswerRepositoryImpl

from chatbot.admin.domain.repositories.SiteRepository import ISiteRepository
from chatbot.admin.infrastructure.SiteRepositoryImpl import SiteRepositoryImpl
from chatbot.admin.domain.repositories.SiteUrlSettingRepository import ISiteUrlSettingRepository
from chatbot.admin.infrastructure.SiteUrlSettingRepositoryImpl import SiteUrlSettingRepositoryImpl

# api
from chatbot.api.domain.repositories.FaqRepository import IFaqRepository as IFaqRepository_api
from chatbot.api.infrastructure.FaqRepositoryImpl import FaqRepositoryImpl as FaqRepositoryImpl_api


def configure(binder):
    # admin
    binder.bind(IFaqListRepository, to=FaqListRepositoryImpl, scope=request)
    binder.bind(IFaqRepository, to=FaqRepositoryImpl, scope=request)
    binder.bind(IBotRepository, to=BotRepositoryImpl, scope=request)
    binder.bind(
        IStaticAnswerRepository,
        to=StaticAnswerRepositoryImpl,
        scope=request)
    binder.bind(ISiteRepository, to=SiteRepositoryImpl, scope=request)
    binder.bind(
        ISiteUrlSettingRepository,
        to=SiteUrlSettingRepositoryImpl,
        scope=request)

    # api
    binder.bind(IFaqRepository_api, to=FaqRepositoryImpl_api, scope=request)
