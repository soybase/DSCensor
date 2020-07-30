from neo4j_db import neo4j_connection_pool as cpool
from dscensor import app, request
from flask import jsonify

base = app.config['API_PATH']
logger = app.logger
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route(base + '/visualize-paths/<filename>', methods=['GET'])
def visualize_paths(filename):
    '''Get all data from parent assembly for visualization

       returns a list of url and name tuples
    '''
    if request.method == 'GET':  # get fasta and then get all others
        msg = ''
        count = 0
        if filename:
            msg += 'Searching for {}'.format(filename)
        logger.info(msg)
        with cpool.get_session() as session:  # get session from driver
            statement = 'MATCH (n {name:{filename}})-[:DERIVED_FROM*1..'
            statement += ']->(m:fasta) return distinct m'  # give me unique nodes
            return_me = []
            logger.debug(statement)  # if necessary
            for r in session.run(statement, {'filename' : filename}):
                if count == 1:
                    logger.warning('Multiple fasta for {}'.format(filename))
                count += 1
                logger.info(r[0].properties)  # testing
                return_me.append(r[0].properties)  # get dictionary 
            if not return_me:
                statement = 'MATCH (n:fasta {name:{filename}}) return n'
                return_me = []
                for r in session.run(statement, {'filename' : filename}):
                    return_me.append(r[0].properties)
            if not return_me:
                logger.error('No fasta found for {}'.format(filename))
                return jsonify([]), 200
            fasta = return_me[0]['name']
            statement = 'MATCH p=(n {name:{filename}})-[:DERIVED_FROM*1..]-(m) return distinct m;'  # should be one line fix later
            return_me = []
            for r in session.run(statement, {'filename' : fasta}):
                return_me.append(r[0].properties)  # get dictionary 
        return jsonify(return_me), 200  # maybe 204 if empty... think still 200
