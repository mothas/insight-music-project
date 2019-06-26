from flask import Flask
import psycopg2
import config
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!!!!!!"

@app.route("/hello")
def hello2():
    return "Hello World! ~~~~~~~"

@app.route("/sql/hello")
def sql_hello():
    conn = psycopg2.connect(dbname=config.PGSQL_DBNAME, user=config.PGSQL_USER, password=config.PGSQL_PASSWORD, host=config.PGSQL_HOST, port=config.PGSQL_PORT)
    cur = conn.cursor()
    cur.execute("SELECT * FROM hash_name LIMIT 10;")
    result = cur.fetchone()
    return result[0] + "," + result[1]

if __name__ == "__main__":
    app.run()
