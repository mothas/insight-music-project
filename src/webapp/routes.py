from flask import Flask, send_file, jsonify
import psycopg2
import config
app = Flask(__name__)

@app.route("/")
def index():
    return send_file('index.html')

@app.route("/load_index.js")
def load_index_js():
    return send_file('load_index.js')

def get_10songs_for_instrument(cursor,instrument_code):
    query = 'SELECT song_name,fi.filename ' + \
            '  FROM filename_instrument_run3 fi ' + \
            '  JOIN hash_name hn ON hn.hash = fi.filename ' + \
            ' WHERE fi.instrument =  \'' + str(instrument_code) + '\' ' + \
            ' LIMIT 10;'
    cursor.execute(query)
    songnames = list(map(lambda x: [x[0], x[1]], cursor))
    return songnames

@app.route("/load_index")
def load_index_page():
    with psycopg2.connect(dbname=config.PGSQL_DBNAME, user=config.PGSQL_USER, password=config.PGSQL_PASSWORD, host=config.PGSQL_HOST, port=config.PGSQL_PORT) as conn:
        with conn.cursor() as cur:
            songs_by_instrument = {
                'Electric Grand Piano': get_10songs_for_instrument(cur, 2),
                'Violin': get_10songs_for_instrument(cur, 40),
                'String Ensemble 1': get_10songs_for_instrument(cur, 48),
                'Clarinet': get_10songs_for_instrument(cur, 71),
                'Flute': get_10songs_for_instrument(cur, 73),
                'Bag pipe': get_10songs_for_instrument(cur, 109),
                'Steel Drums': get_10songs_for_instrument(cur, 114)
            }
    cur.close()
    conn.close()
    return jsonify(songs_by_instrument)

@app.route("/get_similar_songs/<filename>")
def get_similar_songs(filename):
    print('here ',filename)
    conn = psycopg2.connect(dbname=config.PGSQL_DBNAME, user=config.PGSQL_USER, password=config.PGSQL_PASSWORD, host=config.PGSQL_HOST, port=config.PGSQL_PORT)
    cur = conn.cursor()
    query = 'SELECT similar_song_filename, hn.song_name, similarity_score ' + \
            '  FROM ( ' + \
            '	 SELECT (1 - distance) AS similarity_score, ' +\
            '        CASE WHEN fs."filename_A" = \'' + filename + '\' THEN "filename_B" ' + \
            ' 	          ELSE fs."filename_A" ' + \
            '	   	 END AS similar_song_filename ' + \
            '	  FROM filepair_similarity_run3 fs ' + \
            '	 WHERE ("filename_A" = \'' + filename +'\' ' + \
            ' 		     OR "filename_B" = \'' + filename + '\' ) ' + \
            '	 ORDER BY distance ' + \
            ' 	 LIMIT 20 ) AS tbl1 ' + \
            'JOIN hash_name hn ON hn.hash = tbl1.similar_song_filename;'
    cur.execute(query)
    print(query)
    songnames = list(map(lambda x: { 'filename': x[0], 'songname': x[1], 'similarity': x[2] }, cur))
    return jsonify(songnames)

if __name__ == "__main__":
    app.run()