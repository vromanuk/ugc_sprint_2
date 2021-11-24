# UGC service

Сервис отвечает за user generated content: к UGC относится всё, чем пользователь дополняет сайт, например, комментарии и оценки фильмов.
Основная задача сервиса – аналитика, с помощью которой можно выдвигать различные гипотезы и система рекомендаций.

## How to run

Для запуска, воспользуйтесь следующей командой:
`docker-compose up -d --build`

После запуска, проверить работоспособность можно используя следующий запрос **curl**:
```
curl --location --request GET 'http://localhost/smoke'
```

## How to test Kafka
Для того, чтобы протестировать Kafka нужно выполнить следующие действия:
1. Убедиться, что запущен `Zookeeper`, `Kafka`, `Clickhouse` и `Faust Worker` 
```
faust -A src.agents worker --without-web -l info
```
2. Выполнить скрипт `populate_clickhouse`
3. Для отправки сообщения в консьюмер можно воспользоваться такой командой:
```
faust -A src.agents send movie_progress '{"finished_at": 1234, "movie_id_user_id": "foobarbar"}'
```
4. Для того, чтобы проверить, что данные появились в `Clickhouse`, нужно выполнить такой запрос:
```
> docker exec -it <container_id_with_app> /bin/sh
> python

from clickhouse_driver import Client
client = Client(host="clickhouse")
print(client.execute("SELECT * FROM movies_db.events"))

```