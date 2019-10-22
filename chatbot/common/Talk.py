
import os
import MeCab
from flask import current_app

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


def create_input(word_to_id: dict, word_set: set):
    input = [0] * len(word_to_id)
    for word in word_set:
        if word in word_to_id:
            id = word_to_id[word]
            input[id] = 1
    return input


def get_bot_vars_dir(bot_id: int):
    return os.path.join(current_app.config['ML_VARS_DIR'], str(bot_id))


def get_tf_checkpoint_path(bot_id: int):
    return os.path.join(get_bot_vars_dir(bot_id), 'cp.ckpt')


def get_vars_file_path(bot_id: int):
    return os.path.join(get_bot_vars_dir(bot_id), 'vars.pkl')
