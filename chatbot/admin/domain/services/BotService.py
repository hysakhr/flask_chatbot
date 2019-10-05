from __future__ import absolute_import, division, print_function, unicode_literals

import MeCab
from chatbot.admin.domain.repositories.BotRepository import IBotRepository
from chatbot.models.Bot import BotModel

from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.models.Faq import FaqModel

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

    def fit(self, bot_id: int, faq_list_repository: IFaqListRepository):
        bot = self.find_by_id(bot_id)
        faq_list = faq_list_repository.find_by_id(bot.faq_list_id)

        # 入力層のデータ用の単語リスト作成

        # 作成したモデルを使う際に単語とIDが同じ、かつ入力層のノードも同じでなければならないため
        # id2word, word2id を作ってファイルに保存

        # パスをDBに保存して、API側でも同じものが使えるようにする

        # 学習

        # モデルファイルの保存とパスのDB保存

        # 学習データの前処理
        ret = {}
        faq_info_list = []
        words = set()
        for faq in faq_list.faqs:
            info, word_set = parse(faq.question)
            faq_info_list.append({
                'question': faq.question,
                'info': info,
                'word_set': word_set
            })

            words = words | word_set

        ret['faq_info_list'] = faq_info_list

        id_to_word = {}
        word_to_id = {}
        for word_id, word in enumerate(words):
            id_to_word[word_id] = word
            word_to_id[word] = word_id

        ret['id_to_word'] = id_to_word
        ret['word_to_id'] = word_to_id

        vars = {
            'id_to_word': id_to_word,
            'word_to_id': word_to_id
        }

        input_dim = len(words)
        middle_layer = math.floor(len(words) * 0.2)
        output_layer = len(faq_list.faqs)

        # 学習データ作成
        data = {
            'inputs': [],
            'labels': []
        }
        for index, faq_info in enumerate(faq_info_list):
            input = [0] * len(id_to_word)
            for word in faq_info['word_set']:
                id = word_to_id[word]
                input[id] = 1
            label = [index]

            data['inputs'].append(input)
            data['labels'].append(label)

        ret['data'] = data

        x = np.array(data['inputs'])
        y = np.array(data['labels'])

        # model 作成
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(middle_layer, input_dim=input_dim),
            tf.keras.layers.Activation('tanh'),
            tf.keras.layers.Dense(output_layer, activation='softmax')
        ])
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

        # 変数保存先ディレクトリ
        bot_vars_dir = os.path.join(
            current_app.config['ML_VARS_DIR'], str(bot_id))

        # tensorflow model 保存用チェックポイントコールバック
        checkpoint_path = os.path.join(bot_vars_dir, 'cp.ckpt')
        cp_callback = tf.keras.callbacks.ModelCheckpoint(
            checkpoint_path, save_weights_only=True, verbose=1)

        # 学習
        model.fit(x, y, epochs=400, callbacks=[cp_callback])
        model.evaluate(x, y)

        # id_to_word, word_to_id の保存
        vars_file_path = os.path.join(bot_vars_dir, 'vars.pkl')

        with open(vars_file_path, 'wb') as fp:
            pickle.dump(vars, fp)

        return ret


# mecab = MeCab.Tagger(
    # '-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
mecab = MeCab.Tagger("-F %s %S %L %m %M")
# mecab = MeCab.Tagger("-Odump")

# MeCab はAPI側でも使用するので、共通で使える状態にしておきたい


def parse(text: str):
    mecab.parse('')
    node = mecab.parseToNode(text)
    ret = []
    word_set = set()

    while node:
        words = []
        features = node.feature.split(',')
        kind = features[0]
        if kind == '名詞':
            words.append(node.surface)
        elif kind in ('動詞', '形容詞'):
            # words.append(node.surface)
            words.append(features[6])
        elif kind == '助動詞' and len(features[6]) > 1:
            words.append(features[6])

        info = {
            'surface': node.surface,
            'feature': node.feature,
            'words': words
        }
        ret.append(info)
        node = node.next

        if words:
            word_set = word_set | set(words)

    return ret, word_set


def preprosess():
    # 事前処理をまとめたい
    pass
