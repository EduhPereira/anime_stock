import psycopg2
from environs import Env

env = Env()
env.read_env()

configs = {
    "host":env.str("HOST"),
    "database":env.str("DB"),
    "user":env.str("USER"),
    "password":env.str("PASS")
}

def conn_cur():
    conn = psycopg2.connect(**configs)
    cur = conn.cursor()

    return conn, cur


def commit_n_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()
