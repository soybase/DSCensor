from neo4j_db import neo4j_connection_pool as cpool
from dscensor import app, request
from flask import jsonify

base = app.config['API_PATH']
logger = app.logger
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route(base + '/taxa-list/', methods=['GET'], 
           defaults={'genus' : False})
@app.route(base + '/taxa-list/<genus>', methods=['GET'])
def taxonomoy_list(genus):
    '''search specified attributes and labels, custom query as POST'''
    if request.method == 'GET':  #get filenames relations at depth
        msg = ''
        with cpool.get_session() as session:  #get session from driver
            statement = 'MATCH (n:fasta'
            if genus:
                genus = genus.lower()
                statement += ':{}'.format(genus)
            statement += ') return n'  #give me unique nodes
            return_me = []
            logger.debug(statement)  #if necessary
            seen = {}
            for r in session.run(statement):
                target = r[0].properties['genus']
                if genus:
                    target = r[0].properties['species']
                if target in seen:
                    continue
                seen[target] = 1
                logger.info(target)  #testing
                return_me.append(target)  #format this later
        return jsonify({'data': return_me}), 200 #maybe 204 if empty... think still 200
