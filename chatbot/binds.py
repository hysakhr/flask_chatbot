from flask import (
    Flask, request
)
from injector import inject

from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.infrastructure.FaqListRepositoryImpl import FaqListRepositoryImpl


def configure(binder):
    binder.bind(IFaqListRepository, to=FaqListRepositoryImpl, scope=request)
