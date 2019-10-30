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

from chatbot.common.Talk import (
    parse,
    create_input,
    get_tf_checkpoint_path,
    save_ml_vars,
    save_ml_model,
    kata_to_hira)


@celery.task()
def fit(bot_id: int, faq_list_id: int, epochs: int = 400):
    # タスクの引数には、独自クラスのインスタンスが設定できないので
    # DB操作をここに記述
    bot = db.session.query(BotModel).get(bot_id)
    faq_list = db.session.query(FaqListModel).get(faq_list_id)

    # 学習データの準備
    faq_info_list = []
    words = set()
    for label, faq in enumerate(faq_list.faqs):
        # 質問の文言をそのまま利用する学習データを追加
        info, word_set = parse(faq.question)
        faq_info_list.append({
            'faq_id': faq.id,
            'question': faq.question,
            'info': info,
            'word_set': word_set,
            'label': label
        })

        words = words | word_set

        # parseして抽出した結果から読みをひらがなにして利用する学習データを追加
        words_hira = []
        # word_set_hira = set()
        for item in info:
            if len(item['features']) <= 7:
                continue

            yomi_katakana = item['features'][7]
            if yomi_katakana != '*' and len(yomi_katakana) > 1:
                yomi_hira = kata_to_hira(yomi_katakana)
                words_hira.append(yomi_hira)
                yomi_info, yomi_word_set = parse(yomi_hira)

        word_set_hira = set(words_hira)
        faq_info_list.append({
            'faq_id': faq.id,
            'question': faq.question,
            'info': info,
            'word_set': word_set_hira,
            'label': label
        })
        words = words | word_set_hira

        # ひらがなを再度parseして利用する学習データを追加
        words_hira = []
        for word_hira in word_set_hira:
            info, word_set = parse(word_hira)
            for word in word_set:
                if len(word) > 1:
                    words_hira.append(word)

        word_set_hira = set(words_hira)
        faq_info_list.append({
            'faq_id': faq.id,
            'question': faq.question,
            'info': info,
            'word_set': word_set_hira,
            'label': label
        })
        words = words | word_set_hira

    id_to_word = {}
    word_to_id = {}
    for word_id, word in enumerate(words):
        id_to_word[word_id] = word
        word_to_id[word] = word_id

    word_count = len(words)
    middle_layers = [
        math.floor(word_count * 0.5),
        math.floor(word_count * 0.3)]
    output_layer = len(faq_list.faqs)

    # 学習データ作成
    data = {
        'inputs': [],
        'labels': []
    }
    for faq_info in faq_info_list:
        input = create_input(
            word_to_id=word_to_id,
            word_set=faq_info['word_set'])
        label = [faq_info['label']]

        data['inputs'].append(input)
        data['labels'].append(label)

    x = np.array(data['inputs'])
    y = np.array(data['labels'])

    # model 作成
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(middle_layers[0], input_dim=word_count),
        tf.keras.layers.Activation('tanh'),
        tf.keras.layers.Dense(middle_layers[1]),
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
    model.fit(x, y, epochs=epochs, callbacks=[cp_callback])

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
