# flake8: noqa

from clickhouse_driver import Client

client = Client(host="localhost")

# client.execute("CREATE DATABASE IF NOT EXISTS example")
# client.execute('CREATE TABLE example.event (finished_at Int64, movie_id_user_id String) Engine=MergeTree() ORDER BY finished_at')
#
# client.execute(
#     "INSERT INTO movies_db.events (finished_at, movie_id_user_id, event_datetime) VALUES (1234, 'bar', now())"
# )

# print(client.execute("SELECT * FROM movies_db.events"))
# print(client.execute('SHOW DATABASES'))
