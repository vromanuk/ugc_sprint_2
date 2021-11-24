import faust


class MovieProgress(faust.Record):
    finished_at: int
    movie_id_user_id: str
