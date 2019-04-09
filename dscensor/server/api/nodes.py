from neo4j_db import neo4j_connection_pool as cpool
from dscensor import app, request
from flask import jsonify

base = app.config['API_PATH']
logger = app.logger

@app.route(base + '/nodes', methods=['GET'])
def all_nodes():
    '''Get All Nodes'''
    if request.method == 'GET':  #get filenames relations at depth
        with cpool.get_session() as session:  #get session from driver
            statement = 'MATCH (n)'
            statement += ' return distinct n'  #give me unique nodes
            return_me = []
            logger.debug(statement)  #if necessary
            seen = {}
            for r in session.run(statement):
                logger.info(r[0].properties)  #testing
                return_me.append(r[0].properties)  #format this later
        return jsonify({'data': return_me}), 200 #maybe 204 if empty... think still 200


@app.route(base + '/nodes/labels/<query>', methods=['GET'])
def labeled_nodes(query):
    '''Get All Nodes with labels'''
    if request.method == 'GET':  #get filenames relations at depth
        with cpool.get_session() as session:  #get session from driver
            statement = 'MATCH (n:{})'.format(query)
            statement += ' return distinct n'  #give me unique nodes
            return_me = []
            logger.debug(statement)  #if necessary
            seen = {}
            for r in session.run(statement):
                logger.info(r[0].properties)  #testing
                return_me.append(r[0].properties)  #format this later
        return jsonify({'data': return_me}), 200 #maybe 204 if empty... think still 200
