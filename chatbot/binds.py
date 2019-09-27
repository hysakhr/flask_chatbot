from flask import (
    Flask, request
)
from injector import inject

from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.infrastructure.FaqListRepositoryImpl import FaqListRepositoryImpl
from chatbot.admin.domain.repositories.FaqRepository import IFaqRepository
from chatbot.admin.infrastructure.FaqRepositoryImpl import FaqRepositoryImpl


def configure(binder):
    binder.bind(IFaqListRepository, to=FaqListRepositoryImpl, scope=request)
    binder.bind(IFaqRepository, to=FaqRepositoryImpl, scope=request)
