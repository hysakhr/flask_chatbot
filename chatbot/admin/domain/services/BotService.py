from __future__ import absolute_import, division, print_function, unicode_literals

from chatbot.admin.domain.repositories.BotRepository import IBotRepository
from chatbot.models.Bot import BotModel, FITTED_STATE_FITTING, FITTED_STATE_NO_FIT

from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.models.Faq import FaqModel
from chatbot.admin.domain.tasks.bot import fit as async_fit

from flask import current_app


class BotService:
    def __init__(self, bot_repository: IBotRepository):
        self.bot_repository = bot_repository

    def get_new_obj(self) -> BotModel:
        return BotModel()

    def get_bots(self) -> list:
        return self.bot_repository.get_list()

    def find_by_id(self, id: int) -> BotModel:
        return self.bot_repository.find_by_id(id)

    def add(self, bot: BotModel):
        self.bot_repository.save(bot)

    def edit(self, bot: BotModel):
        return self.bot_repository.save(bot)

    def fit(self, bot_id: int, faq_list_id: int):
        # bot state を学習中に変更
        bot = self.find_by_id(bot_id)
        bot.fitted_state = FITTED_STATE_FITTING
        self.edit(bot)

        # 学習処理を非同期で行う
        async_fit.delay(bot_id, faq_list_id)
