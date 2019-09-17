from flask import (
    Blueprint, request, jsonify
)

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/talk', methods=('POST',))
def talk():
    if request.json['type'] == 'freeText':
        answer = 'recieve freeText {}'.format(request.json['query'])
        res = {
            'components': {
                'answer': {
                    'qa_id': 1234,
                    'answer': answer
                },
                'questionList': [
                    {
                        'qa_id': 2222,
                        'question': '〇〇はありませんか？'
                    },
                    {
                        'qa_id': 2223,
                        'question': 'ログインできません'
                    }
                ],
                'staticAnswerList': [
                    {
                        'id': 1,
                        'title': 'start',
                        'displayText': '最初の回答'
                    }
                ]
            },
            'request_json': request.json
        }
    elif request.json['type'] == 'question':
        answer = 'recieve question qa_id =  {}'.format(request.json['qa_id'])
        res = {
            'components': {
                'answer': {
                    'qa_id': 1234,
                    'answer': answer
                },
                'questionList': [
                    {
                        'qa_id': 2222,
                        'question': '〇〇はありませんか？'
                    },
                    {
                        'qa_id': 2223,
                        'question': 'ログインできません'
                    }
                ],
                'staticAnswerList': [
                    {
                        'id': 1,
                        'title': 'start',
                        'displayText': '最初の回答'
                    }
                ]
            },
            'request_json': request.json
        }
    elif request.json['type'] == 'staticAnswer':
        answer = 'recieve staticAnswer static_query =  {}'.format(
            request.json['static_query'])
        res = {
            'components': {
                'answer': {
                    'qa_id': 1234,
                    'answer': answer
                },
                'questionList': [
                    {
                        'qa_id': 2222,
                        'question': '〇〇はありませんか？'
                    },
                    {
                        'qa_id': 2223,
                        'question': 'ログインできません'
                    }
                ],
                'staticAnswerList': [
                    {
                        'id': 1,
                        'title': 'start',
                        'displayText': '最初の回答'
                    }
                ]
            },
            'request_json': request.json
        }
    else:
        return jsonify({'error': 'type error'})

    return jsonify(res)
