import psycopg2
import config

conn = psycopg2.connect(dbname=config.PGSQL_DBNAME, user=config.PGSQL_USER, password=config.PGSQL_PASSWORD, host=config.PGSQL_HOST, port=config.PGSQL_PORT)

def hello_world():
    cur = conn.cursor()
    cur.execute("select * from hash_name limit 10;")
    print(cur.fetchone())
