from __future__ import absolute_import, division, print_function, unicode_literals

import MeCab
from chatbot.admin.domain.repositories.BotRepository import IBotRepository
from chatbot.models.Bot import BotModel, FITTED_STATE_FITTING

from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.models.Faq import FaqModel
from chatbot.admin.domain.tasks.bot import fit as async_fit

from flask import current_app

import tensorflow as tf
import numpy as np
import math
import pickle
import os


class BotService:
    def __init__(self, bot_repository: IBotRepository):
        self.bot_repository = bot_repository

    def get_new_obj(self, faq_list_id: int) -> BotModel:
        return BotModel(name='', faq_list_id=faq_list_id, fitted_model_path='')

    def get_bots_by_faq_list_id(self, faq_list_id: int) -> list:
        return self.bot_repository.get_list_by_faq_list_id(faq_list_id)

    def find_by_id(self, id: int) -> BotModel:
        return self.bot_repository.find_by_id(id)

    def save(self, bot: BotModel):
        return self.bot_repository.save(bot)

    def fit(self, bot_id: int):
        # bot state を学習中に変更
        bot = self.find_by_id(bot_id)
        bot.fitted_state = FITTED_STATE_FITTING
        self.save(bot)

        # 学習処理を非同期で行う
        async_fit.delay(bot_id)
