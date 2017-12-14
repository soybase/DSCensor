from dscensor import app, session, g, render_template
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
    return app.neo4j_example
