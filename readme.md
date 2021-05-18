<p align="center">
 <img src="https://sun9-64.userapi.com/c11263/u13825615/-6/x_3f964139.jpg">
</p>
<p align="center">
Hello and thanks for visiting! Here is a docker configs for php!
</p>

DOCKER PHP 8 PERCONA RABBIT
==========================================

## Список образов и их локальные адреса

- nginx 1.19.2
- rabbitmq https://rmq
- php 8.0.6
- cron
- pgadmin4 https://pma
- mailtrap https://mailtrap
- redis-commander https://redisc
- redis 6.0.6
- postgres 13.1
- webgrind https://pprofiler

## Установка

1. Копируем `.env.example` в `.env`
2. Редактируем настройки в `.env`
    ```env
    # Пользователь и группа, обычно не требует изменений.
    # В случае с виндой может потребоваться убрать отсюда и из docker-compose.yml
    USER_ID=1000
    GROUP_ID=1000

    # Ip локальной машины, на которой запускается docker
    LOCAL_IP=192.168.0.2
    # mysql
    # Логин и пароль для доступа в веб морду pgadmin
    PGADMIN_DEFAULT_EMAIL=example@mail.com
    PGADMIN_DEFAULT_PASSWORD=123qwe
    # --------------------------
    PGADMIN_ENABLE_TLS=false
    POSTGRES_USER=root
    POSTGRES_PASSWORD=root

    # RabbitMQ
    # Порты для RabbitMQ Нода, к которой будем подключаться из php
    # и Http/Https порты. Их менять не стоит
    RABBITMQ_NODE_HOST_PORT=5673
    RABBITMQ_MANAGEMENT_HTTP_HOST_PORT=15672
    RABBITMQ_MANAGEMENT_HTTPS_HOST_PORT=15671
    # Логин и пароль RabbitMQ
    RABBITMQ_DEFAULT_USER=guest
    RABBITMQ_DEFAULT_PASS=guest

    # mail catch
    # Логин и пароль для мейлтрапа
    MT_USER=mailtrap
    MT_PASSWD=mailtrap
    MT_MAILBOX_LIMIT=512000001
    MT_MESSAGE_LIMIT=102400001

    # domain names
    # Не используется
    DOMAIN_TEMPLATE=%domain%
    ```

3. Добавляем в hosts файл строки из файла `hosts` который лежит рядом в корне. Если будем редактировать nginx домен, то меняем последнюю запись на свою
    ```
    127.0.0.1 pma
    127.0.0.1 rmq
    127.0.0.1 redisc
    127.0.0.1 mailtrap
    127.0.0.1 pprofiler
    127.0.0.1 catmodecode.tk
    ```
4. Открываем `./etc/nginx/cmc_com.conf`. Если залезли сюда сами знаете что делать. Просто меняем все упоминания catmodecode.tk и catmodecode_tk на своё

5. Создаем в `./www` директорию `catmodecode.tk` или с вашим названием. В ней создаем директорию public. Это корень сайта. Поменять корень можно в `./etc/nginx/cmc_com.conf` если неудобно.

5. Из корня выполняем команду `docker-compose build`

6. Если все хорошо, делаем `docker-compose up -d` и готово. Заходим по адресу https://catmodecode.tk


**P.S**
Логи всего и вся пишутся в `./log`


**P.P.S**
Постгрес может не подняться, тут лучше смотреть на то, что говрит `docker-compose up -d`. Есть какие-то проблемы с правами. Уже созданную базу он неплохо видит.
