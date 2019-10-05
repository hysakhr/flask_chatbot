from flask import (
    Flask, request
)
from injector import inject

from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.infrastructure.FaqListRepositoryImpl import FaqListRepositoryImpl
from chatbot.admin.domain.repositories.FaqRepository import IFaqRepository
from chatbot.admin.infrastructure.FaqRepositoryImpl import FaqRepositoryImpl
from chatbot.admin.domain.repositories.BotRepository import IBotRepository
from chatbot.admin.infrastructure.BotRepositoryImpl import BotRepositoryImpl


def configure(binder):
    binder.bind(IFaqListRepository, to=FaqListRepositoryImpl, scope=request)
    binder.bind(IFaqRepository, to=FaqRepositoryImpl, scope=request)
    binder.bind(IBotRepository, to=BotRepositoryImpl, scope=request)
