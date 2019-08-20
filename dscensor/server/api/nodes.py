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


@app.route(base + '/nodes/parents', methods=['POST'])
def parents_by_name_post():
    '''Get All parents for a given node by passing a list'''
    if request.method == 'POST':  #get filenames relations at depth
        return_me = []
        posted_data = request.get_json(force=True)
        if not posted_data:
            return 'You must post a list called data containing filenames', 400
        for d in posted_data:
            with cpool.get_session() as session:  #get session from driver
                statement = 'MATCH (n {name:{filename}})-[:CHILD_OF]->(m)'
                statement += ' return distinct m'  #give me unique nodes
#                return_me = []
                logger.debug(statement)  #if necessary
#                seen = {}
                my_obj = {d: {'parents': []}}
                for r in session.run(statement, {'filename': d}):
                    logger.info(r[0].properties)  #testing
                    my_obj[d]['parents'].append(r[0].properties)  #attach parent
                return_me.append(my_obj)
        return jsonify({'data': return_me}), 200 #maybe 204 if empty...


@app.route(base + '/nodes/parents/<query>', methods=['GET'])
def parents_by_name(query):
    '''Get All parents for a given node'''
    if request.method == 'GET':  #get filenames relations at depth
        with cpool.get_session() as session:  #get session from driver
            statement = 'MATCH (n {name:{filename}})-[:CHILD_OF]->(m)'
            statement += ' return distinct m'  #give me unique nodes
            return_me = []
            logger.debug(statement)  #if necessary
            seen = {}
            for r in session.run(statement, {'filename': query}):
                logger.info(r[0].properties)  #testing
                return_me.append(r[0].properties)  #format this later
        return jsonify({'data': return_me}), 200 #maybe 204 if empty... think still 200


