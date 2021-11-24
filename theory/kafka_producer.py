from time import sleep

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

producer.send(
    topic="movie_progress",
    value=b'{"timestamp": "500271", "movie_id_user_id": "tt0120338"}',
    key=b"500271+tt0120338",
)

sleep(1)
