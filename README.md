# flask_chatbot

chatbot application on local machine
日本語での概要説明→[flaskでチャットボットのサンプルアプリ作ってみた【概要編】](https://blog.hysakhr.com/2019/11/06/flask%e3%81%a7%e3%83%81%e3%83%a3%e3%83%83%e3%83%88%e3%83%9c%e3%83%83%e3%83%88%e3%81%ae%e3%82%b5%e3%83%b3%e3%83%97%e3%83%ab%e3%82%a2%e3%83%97%e3%83%aa%e4%bd%9c%e3%81%a3%e3%81%a6%e3%81%bf%e3%81%9f/)

![screenshot_front](https://github.com/hysakhr/flask_chatbot/blob/images/images/screenshot_front.gif?raw=true)


### Prerequisites

- docker
- docker-compose

### Installing and running


```
git clone git@github.com:hysakhr/flask_chatbot.git
cd flask_chatbot
docker-compose up
```

#### access

- front
http://localhost:9000/

- admin
http://localhost:9000/admin

### chatbot settings on admin

configure the following settings.

1. create bot
    - screen : Bot > Bot追加
1. create and upload faq list file in tsv format.
    - refer to [sample_faq_list.tsv](sample_faq_list.tsv). **(only japanese)**
    - screen : Bot > Bot詳細 > ファイルからインポート
1. set faq_list to be used in specific situations.
    - situations : when talk start, faq notfound
    - screen : Bot > Bot詳細 > FAQリスト編集
1. train bot
    - screen : Bot > Bot詳細 > FAQリストの学習ボタン
    - train processing is asynchronous.
    - if 学習状態 is 学習中, please reload the page after a while.
1. create site
    - screen : Site Settings > サイト追加
1. setting bot to use on the site.
    - when site is created, site default setting is created at the same time.
    - if you want to set for each URL, you can add it separately.

### chatbot settings on front

1. site_id
1. show_faq_info

chatbot/templates/front/index.html
```
    data: {
      talk: [],
      config: {
        site_id: 1,
        show_faq_info: true
      }
    },
```

End with an example of getting some data out of the system or using it for a little demo

## libraries
### front
- Vue.js (2.6.0)
- axios (0.19.0)
- node-sass (4.12.0)

### admin
#### main python libraries
- flask (1.1.1)
- flask-SQLAlchemy (2.4.0)
- SQLAlchemy (1.3.8)
- celery (4.3.0)
- numpy (1.17.2)
- tensorflow (2.0.0)

#### other libraries
- AdminLTE (2.4.18)
- mecab (0.996)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Author
- hysakhr