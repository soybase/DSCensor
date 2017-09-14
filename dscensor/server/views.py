from dscensor import app, session, g, render_template
from api import help

@app.route('/')
def document_root():
    return render_template('index.html', static_path='/static')

@app.route('/large_example')
def large_example():
    return app.large_example

@app.route('/medicago_metrics')
def medicago_metrics():
   return render_template(
                   'templating/templates/medicago_assembly_metrics.html',
                   static_path='/static'
          )
