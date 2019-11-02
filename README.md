# flask_chatbot

chatbot application on local machine

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

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
1. create faq list
  upload file in tsv format.
  refer to [sample_faq_list.tsv](sample_faq_list.tsv). **(only japanese)**
1. set faq_list to be used in specific situations.
    1. when talk start
    1. faq not found
1. train bot
1. create site
    1. when site is created, site default setting is created at the same time.
    1. if you want to set for each URL, you can add it separately.

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