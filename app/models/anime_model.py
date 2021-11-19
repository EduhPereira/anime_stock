import psycopg2
from . import conn_cur, commit_n_close
from psycopg2 import sql,errors
from app.exceptions import InvalidKeys

UniqueViolation = errors.lookup('23505')

class AnimeModel:
    anime_keys = ['id', 'anime', 'released_date', 'seasons']

    def __init__(self, anime:str, released_date:str, seasons:int) -> None:
        self.anime = anime.title()
        self.released_date = released_date
        self.seasons = seasons
    

    def create(self):
        conn, cur = conn_cur()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS animes(
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL
            );
        """)

        query = """
            INSERT INTO animes(anime, released_date, seasons) 
            VALUES (%s, %s, %s) 
            RETURNING *
        """

        query_values = list(self.__dict__.values())

        try:
            cur.execute(query, query_values)
            inserted_anime = cur.fetchone()
            commit_n_close(conn, cur)
        except UniqueViolation:
            raise psycopg2.Error
        
        return dict(zip(self.anime_keys, inserted_anime))

    @staticmethod
    def read_all():
        conn, cur = conn_cur()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS animes(
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL
            );
        """)

        cur.execute("""
            SELECT * FROM animes
        """)

        animes = cur.fetchall()
        commit_n_close(conn, cur)
        animes_found = [dict(zip(AnimeModel.anime_keys, anime)) for anime in animes]

        return animes_found

    @staticmethod
    def read_by_id(id):
        conn, cur = conn_cur()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS animes(
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL
            );
        """)

        cur.execute("""
            SELECT * FROM animes WHERE id=(%s);
        """,
            (id,),
        )

        anime = cur.fetchone()
        commit_n_close(conn, cur)
        anime_found = dict(zip(AnimeModel.anime_keys, anime))
        return anime_found

    @staticmethod
    def update(anime_id, payload:dict):
        conn, cur = conn_cur()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS animes(
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL
            );
        """)

        columns = [sql.Identifier(key) for key in payload.keys()]
        values = [sql.Literal(value) for value in payload.values()]

        query = sql.SQL("""
            UPDATE animes 
            SET ({columns}) = row({values}) 
            WHERE id={id} 
            RETURNING *
        """).format(
            id = sql.Literal(anime_id),
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        cur.execute(query)
        updated_anime = cur.fetchone()
        commit_n_close(conn, cur)
        return dict(zip(AnimeModel.anime_keys, updated_anime))

    @staticmethod
    def delete(id):
        conn, cur = conn_cur()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS animes(
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL
            );
        """)

        response = cur.execute("""
            DELETE FROM animes WHERE id=(%s) 
            RETURNING *;
        """,
            (id,),
        )

        anime_deleted = cur.fetchone()
        anime_deleted = dict(zip(AnimeModel.anime_keys, anime_deleted))

        commit_n_close(conn, cur)

    @staticmethod
    def validate(keys:list):
        invalid_keys = []
        valid_keys = []

        for key in keys:
            if key not in AnimeModel.anime_keys:
                invalid_keys.append(key)
            else:
                valid_keys.append(key)

        if len(invalid_keys) > 0:
            raise InvalidKeys(valid_keys, invalid_keys)
