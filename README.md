# Подготовка системы

Для локального запуска проекта необходимо уставновить Docker и Makefile.

В файл etc/hosts добавить:

```
127.0.0.1 gostarter.local
```

Затем создать .env файл в корне проекта со следующим содержимым:

```
APP_NAME=gostarter
APP_ENV=local
APP_KEY=base64:T1UVaXqrQYxHQ3PORTeca+wIvb9yQRuslsX0CxUTHb8=
APP_DEBUG=true
APP_TIMEZONE=UTC
APP_URL=gostarter.local

PROJECT_NAME=gostarter
WORKING_DIR=/var/www/html
NGINX_PORT=80

FILESYSTEM_DISK=public
```


Далее в каталоге с проектом и выполнить:
```
make init
```
Документация API доступна по адресу gostarter.local/docs/api
