import psycopg2
from database import postgres_db_connect
from dscensor import app, request
from flask import jsonify

base = app.config['API_PATH']

@app.route(base + '/initialize_data', methods=['GET'])
def initialize_data():
    '''initialize the data for the page, this is temporary'''
    with postgres_db_connect.get_pooled_cursor() as cursor:
        query = '''
        cursor.execute(query, [sample])
        result = cursor.fetchall()
        return jsonify(result), 200

