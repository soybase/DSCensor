from dscensor import app, request
from flask import jsonify

base = app.config['API_PATH']
logger = app.logger
panparser = app.panparser
main_panset = app.main_panset
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route(base + '/pansets', methods=['GET'])
def all_pansets():
    '''Get Pan-Genome Datasets'''
    if request.method == 'GET':
        return jsonify([d for d in panparser]), 200  # return all pansets


@app.route(base + '/panclusters/<panset>', methods=['GET'])
@app.route(base + '/panclusters/<panset>/<geneid>', methods=['GET'])
@app.route(base + '/panclusters/<panset>/<geneid>/<annotation>', methods=['GET'])
def pancluseters_by_panset(panset, geneid=None, annotation=None):
    '''Get Pan-Cluster identifiers for a given panset'''
    if request.method == 'GET':
        if panset == 'main':
            panset = main_panset  # Main panset 07272020 glycine centric
        if geneid:  # return fully qualified names of genes in pansets with geneid
            if panparser.get(panset):
                if panparser.get(panset).get('pansets'):  # panset exists and isn't empty
                    pansets = panparser.get(panset).get('pansets')
                    if geneid in pansets:
                        pansetids = pansets[geneid]  # get ids for panset to use in geneid retrieval
                        if annotation:  # return only results from the given genome annotation
                            results = []
                            for p in pansetids:  # go through each panset for the given geneid
                                filtered_genes = []
                                for g in panparser[panset]['clusters'][p]:
                                    g_annotation = '.'.join(g.split('.')[:4])  # get annotation name from full name
                                    if g_annotation == annotation:
                                        filtered_genes.append(g)
                                results.append({'panset_id': p, 'gene_ids': filtered_genes, 'annotation': annotation})
                            return jsonify(results), 200
                                
                        else:  # return all results
                            if pansetids:
                                results = [ {'panset_id': p, 'gene_ids': panparser[panset]['clusters'][p]} \
                                            for p in pansetids ]
                                return jsonify(results), 200
        else:
            if panparser.get(panset):
                return jsonify([p for p in panparser[panset]['clusters']]), 200 #maybe 204 if empty...
        return jsonify([]), 200
