from dscensor import app, request
from flask import jsonify

base = app.config['API_PATH']
logger = app.logger
panparser = app.panparser
main_panset = app.main_panset


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
                        pansetid = pansets[geneid]  # get id for panset to use in geneid retrieval
                        if annotation:  # return only results from the given genome annotation
                            filtered_genes = []
                            for g in panparser[panset]['clusters'][pansetid]:
                                g_annotation = '.'.join(g.split('.')[:4])  # get annotation name from full name
                                if g_annotation == annotation:
                                    filtered_genes.append(g)
                            return jsonify({'panset_id': pansetid,
                                            'gene_ids': filtered_genes, 'annotation': annotation}), 200
                                
                        else:  # return all results
                            if pansetid:
                                return jsonify({'panset_id': pansetid,
                                                'gene_ids': panparser[panset]['clusters'][pansetid]}), 200
        else:
            if panparser.get(panset):
                return jsonify([p for p in panparser[panset]['clusters']]), 200 #maybe 204 if empty...
        return jsonify([]), 200
