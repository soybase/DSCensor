from dscensor import app, request
from flask import jsonify

base = app.config['API_PATH']
logger = app.logger
panparser = app.panparser

@app.route(base + '/pansets', methods=['GET'])
def all_pansets():
    '''Get Pan-Genome Datasets'''
    if request.method == 'GET':  #get filenames relations at depth
        return_me = True
        return jsonify([d for d in panparser]), 200 #maybe 204 if empty... think still 200


@app.route(base + '/panclusters/<panset>', methods=['GET'])
@app.route(base + '/panclusters/<panset>/<geneid>', methods=['GET'])
def pancluseters_by_panset(panset, geneid=None):
    '''Get Pan-Cluster identifiers for a given panset'''
    if request.method == 'GET':  #get filenames relations at depth
        if geneid:
            if panparser.get(panset):
                if panparser.get(panset).get('pansets'):
                    pansets = panparser.get(panset).get('pansets')
                    if geneid in pansets:
                        pansetid = pansets[geneid]
                        if pansetid:
                            return jsonify({'panset_id': pansetid, 'gene_ids': panparser[panset]['clusters'][pansetid]}), 200
        else:
            if panparser.get(panset):
                return jsonify([p for p in panparser[panset]['clusters']]), 200 #maybe 204 if empty... think still 200
        return jsonify([]), 200



#@app.route(base + '/nodes/parents/<query>', methods=['GET'])
#def parents_by_name(query):
#    '''Get All parents for a given node'''
#    if request.method == 'GET':  #get filenames relations at depth
#        with cpool.get_session() as session:  #get session from driver
#            statement = 'MATCH (n {name:{filename}})-[:CHILD_OF]->(m)'
#            statement += ' return distinct m'  #give me unique nodes
#            return_me = []
#            logger.debug(statement)  #if necessary
#            seen = {}
#            for r in session.run(statement, {'filename': query}):
#                logger.info(r[0].properties)  #testing
#                return_me.append(r[0].properties)  #format this later
#        return jsonify({'data': return_me}), 200 #maybe 204 if empty... think still 200


