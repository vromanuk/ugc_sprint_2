from faust import Stream

from src.db.clickhouse import ClickhouseClient
from src.main import get_faust_app
from src.records import MovieProgress

app = get_faust_app()

movie_progress_topic = app.topic("movie_progress", value_type=MovieProgress)


@app.agent(movie_progress_topic)
async def track_movie_progress(movie_progress: Stream):
    async for event in movie_progress.group_by(MovieProgress.movie_id_user_id):
        await ClickhouseClient.track_movie_progress(
            event.finished_at, event.movie_id_user_id
        )
