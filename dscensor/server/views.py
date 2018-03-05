from dscensor import app, session, g, render_template, request
from flask import render_template_string, make_response, jsonify
from neo4j_db import neo4j_connection_pool as cpool
from client.templating import neo4j_dscensor_linkout
from api import help, derived_from, visualize_paths

logger = app.logger

@app.route('/')
def document_root():
    return render_template('index.html', static_path='/static')

#@app.route('/large_example')
#def large_example():
#    return app.large_example

#@app.route('/DSCensor_example')
#def dscensor_example():
#    return app.dscensor_example

@app.route('/DSCensor_example_wscatter')
def dscensor_example_scatter():
    return render_template(
                   'templating/templates/dscensor_fixed_scatterdraft.html',
                   static_path='/static'
          )

@app.route('/medicago_metrics')
def medicago_metrics():
    return render_template(
                   'templating/templates/medicago_assembly_metrics.html',
                   static_path='/static'
          )

@app.route('/DSCensor_neo4j')
def dscensor_neo4j():
#    response = make_response(render_template_string(app.neo4j_example))
#    response.headers['Access-Control-Allow-Origin'] =  '*'
    response = render_template('templating/templates/test_me_linkout.html',
                               static_path='/static')
    return response

@app.route('/DSCensor_neo4j_dynamic')
def dscensor_neo4j_dynamic():
#    response = make_response(render_template_string(app.neo4j_example))
    response = make_response(render_template_string(neo4j_dscensor_linkout.dscensor_neo4j_test('gff')))
#    response.headers['Access-Control-Allow-Origin'] =  '*'
#    response = render_template('templating/templates/test_me_linkout.html',
#                               static_path='/static')
    return response


@app.route('/DSCensor_neo4j_dynamic_fa')
def dscensor_neo4j_dynamic_fa():
#    response = make_response(render_template_string(app.neo4j_example))
    response = make_response(render_template_string(neo4j_dscensor_linkout.dscensor_neo4j_test('fasta')))
#    response.headers['Access-Control-Allow-Origin'] =  '*'
#    response = render_template('templating/templates/test_me_linkout.html',
#                               static_path='/static')
    return response


@app.route('/visualize-igv/<filename>', methods=['GET'])
def visualize_igv(filename):
    '''Get data for filename's assembly to allow user to visualize all

       related data
    '''
    if request.method == 'GET':  # get fasta and then get all others
        visualize_me = {}
        msg = ''
        count = 0
        msg += 'Searching for {}'.format(filename)
        logger.debug(msg)
        with cpool.get_session() as session:  # get session from driver
            statement = 'MATCH (n {name:{filename}})-[:DERIVED_FROM*1..'
            statement += ']->(m:fasta) return distinct m'  # get files fasta
            return_me = []
            logger.debug(statement)  # if necessary
            for r in session.run(statement, {'filename' : filename}):  # run
                if count == 1:  # to report if multiple fasta are found
                    logger.warning('Multiple fasta for {}'.format(filename))
                count += 1
                logger.info(r[0].properties)  # testing
                return_me.append(r[0].properties)  # get dictionary
            if not return_me:  # if empty check to see if already fasta
                statement = 'MATCH (n:fasta {name:{filename}}) return n'
                return_me = []
                for r in session.run(statement, {'filename' : filename}):
                    return_me.append(r[0].properties)
            if not return_me:  # wasn't fasta and no fasta were found not error
                logger.error('No fasta found for {}'.format(filename))
                return jsonify([]), 200  # return empty wasn't an error
            fasta = return_me[0]['name']  # this is dumb fix later
            visualize_me['fasta'] = [fasta]  # set fasta for visualize
            statement = 'MATCH p=(n {name:{filename}})<-[:DERIVED_FROM*1..]-(m) return distinct m'  # should be one line fix later get all files derived from fasta
            return_me = []
            seen = {}
            for r in session.run(statement, {'filename' : fasta}):
                properties = r[0].properties  # get properties of m
                filename = properties['name']
                filetype = properties['filetype']
                assert filename, 'files should have a name this one doesnt' 
                assert filetype, 'files should have a type this one doesnt'
                url = properties['url']
                if not url:  # not an error, but won't return for visual
                    logger.warning('No url for {} will not return'.format(
                                                                     filename))
                    continue
                element = (filename, url)  # create visual tuple
                if filename in seen:  # continue if already seen
                    continue
                seen[filename] = 1
                if filetype not in visualize_me:
                    visualize_me[filetype] = []
                visualize_me[filetype].append(element)
#                return_me.append(r[0].properties)  # get dictionary
            statement = 'MATCH p=(n {name:{filename}})<-[:DERIVED_FROM*1..]-(m)-[:DERIVED_FROM]->(o) return distinct m, o'
            for r in session.run(statement, {'filename' : fasta}):
#                properties_m = r[0].properties  # get properties of m
                properties_o = r[1].properties  # get propteries of o
#                filename_m = properties_m['name']
#                filetype_m = properties_m['filetype']
                filename_o = properties_o['name']
                filetype_o = properties_o['filetype']
#                assert filename, 'files should have a name this one doesnt'
#                assert filetype, 'files should have a type this one doesnt'
                assert filename_o, 'files should have a name this one doesnt'
                assert filetype_o, 'files should have a type this one doesnt'
                if filename_o in seen:  # continue if already seen
                    continue
                seen[filename_o] = 1
                url = properties_o['url']
                if not url:  # not an error, but won't return for visual
                    logger.warning('No url for {} will not return'.format(
                                                                   filename_o))
                    continue
                element = (filename_o, url)  # create visual tuple
                if filetype_o not in visualize_me:
                    visualize_me[filetype_o] = []
                visualize_me[filetype_o].append(element)
        # create template
        return jsonify(visualize_me), 200
#    response = make_response(render_template_string(app.neo4j_example))
#    response = make_response(render_template_string(neo4j_dscensor_linkout.dscensor_neo4j_test('fasta')))
#    response.headers['Access-Control-Allow-Origin'] =  '*'
#    response = render_template('templating/templates/test_me_linkout.html',
#                               static_path='/static')
#    return response

