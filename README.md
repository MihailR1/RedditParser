# Сервис на FastAPI парсинга пользователей и постов с Reddit
Для работы нужно получить API ключ по адресу https://www.reddit.com/prefs/apps
```
Нужны SECRET_KEY, CLIENT_ID - их прописать в .env файле
```

## Запуск приложения через Docker

1. Сборка образа 
```
docker build --tag reddit_parser .
```

2. Запуск образа с параметрами
```
docker run --env-file=.env -p 80:80 reddit_parser
```

3. Зайти на адрес со всеми роутами
```
http://127.0.0.1:80/docs
```

4. Проверить работоспобность вызвав любой из роутов