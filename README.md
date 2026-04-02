# API для Yatube

REST API для социальной платформы Yatube. Проект позволяет получать публикации, комментарии, сообщества и подписки, а авторизованным пользователям создавать и редактировать свой контент через JWT-аутентификацию.

## Что умеет API

- работать с публикациями: список, просмотр, создание, редактирование и удаление;
- работать с комментариями конкретного поста;
- отдавать список сообществ и детали сообщества;
- создавать подписки и искать их по `username`;
- выдавать JWT-токены для авторизации.

## Установка

1. Клонируйте репозиторий и перейдите в него:

```bash
git clone <repo_url>
cd api-final-yatube-ad
```

2. Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Перейдите в директорию проекта и выполните миграции:

```bash
cd yatube_api
python manage.py migrate
```

5. Запустите сервер разработки:

```bash
python manage.py runserver
```

Документация будет доступна по адресу `http://127.0.0.1:8000/redoc/`.

## Примеры запросов

Получение JWT-токена:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"username":"TestUser","password":"1234567"}'
```

Создание публикации:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"text":"Новый пост","group":1}'
```

Создание подписки:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/follow/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"following":"TestUserAnother"}'
```
