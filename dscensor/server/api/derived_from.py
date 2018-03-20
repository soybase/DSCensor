import psycopg2
from neo4j_db import neo4j_connection_pool as cpool
from dscensor import app, request
from flask import jsonify

base = app.config['API_PATH']
logger = app.logger

@app.route(base + '/derived-from-file/', methods=['POST'], 
                                         defaults={'filename' : False, 'depth' : False})
@app.route(base + '/derived-from-file/<filename>', methods=['GET'], defaults={'depth' : False})
@app.route(base + '/derived-from-file/<filename>/<depth>', methods=['GET'])
def derived_from_file(filename, depth):
    '''search specified attributes and labels, custom query as POST'''
    if request.method == 'GET':  #get filenames relations at depth
        msg = ''
        if filename:
            msg += 'Searching for {}'.format(filename)
        if depth:
            try:
                depth = int(depth)  #make sure depth is int
            except ValueError:
                logger.error('Depth provided was not int')
                raise
            msg += ' at depth {}'.format(depth)
        logger.info(msg)
        with cpool.get_session() as session:  #get session from driver
            statement = 'MATCH (n {name:{filename}})<-[:DERIVED_FROM*1..'
            if depth:
                statement += '{}'.format(depth)
            statement += ']-(m) return distinct m'  #give me unique nodes
            return_me = []
            logger.debug(statement)  #if necessary
            for r in session.run(statement, {'filename' : filename}):
                logger.info(r[0].properties)  #testing
                return_me.append(r[0].properties)  #format this later for proper return
        return jsonify(return_me), 200 #maybe 204 if empty... think still 200

