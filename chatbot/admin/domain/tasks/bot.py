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
from datetime import datetime

from chatbot.common.Talk import parse, create_input, get_tf_checkpoint_path, save_ml_vars, save_ml_model


@celery.task()
def fit(bot_id: int, faq_list_id: int):
    # タスクの引数には、独自クラスのインスタンスが設定できないので
    # DB操作をここに記述
    bot = db.session.query(BotModel).get(bot_id)
    faq_list = db.session.query(FaqListModel).get(faq_list_id)

    # 学習データの前処理
    ret = {}
    faq_info_list = []
    words = set()
    for faq in faq_list.faqs:
        info, word_set = parse(faq.question)
        faq_info_list.append({
            'faq_id': faq.id,
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

    input_dim = len(words)
    middle_layer = math.floor(len(words) * 0.2)
    output_layer = len(faq_list.faqs)

    # 学習データ作成
    data = {
        'inputs': [],
        'labels': []
    }
    for index, faq_info in enumerate(faq_info_list):
        input = create_input(
            word_to_id=word_to_id,
            word_set=faq_info['word_set'])
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

    # tensorflow model 保存用チェックポイントコールバック
    # 学習後に作成した model を保存する設定
    checkpoint_path = get_tf_checkpoint_path(bot_id)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        checkpoint_path, save_weights_only=True, verbose=1)

    # 学習
    model.fit(x, y, epochs=400, callbacks=[cp_callback])
    # model.save('my_model.h5')

    loss, acc = model.evaluate(x, y)

    # 変数とモデルの保存``
    vars = {
        'id_to_word': id_to_word,
        'word_to_id': word_to_id,
        'faq_info_list': faq_info_list
    }

    save_ml_vars(bot_id, vars)
    save_ml_model(bot_id=bot_id, model=model)

    # bot data 更新
    bot.fitted_state = FITTED_STATE_FITTED
    bot.fitted_faq_list_id = faq_list_id
    bot.last_fitted_at = datetime.now()

    db.session.add(bot)
    db.session.commit()

    return True
