from chatbot import celery
import MeCab
from flask import current_app

from chatbot.models.Bot import BotModel, FITTED_STATE_FITTING, FITTED_STATE_FITTED
from chatbot.models.FaqList import FaqListModel
from chatbot.database import db

import tensorflow as tf
import numpy as np
import math
import pickle
import os


@celery.task()
def fit(bot_id: int):
    # タスクの引数には、独自クラスのインスタンスが設定できないので
    # DB操作をここに記述
    bot = db.session.query(BotModel).get(bot_id)
    faq_list = db.session.query(FaqListModel).get(bot.faq_list_id)

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
    # 学習後に作成した model を保存する設定
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

    # bot stateを学習済みに変更
    bot.fitted_state = FITTED_STATE_FITTED
    db.session.add(bot)
    db.session.commit()

    return True


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
