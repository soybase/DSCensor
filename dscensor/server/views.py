from dscensor import app, session, g, render_template
from flask import render_template_string, make_response
from client.templating import neo4j_dscensor_linkout
from api import help

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
