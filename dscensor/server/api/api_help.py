from dscensor import app
from flask import jsonify

r = app.config['API_PATH'] + '/help'
app.logger.info(
    'note: http {} for list of defined routes'.format(r)
)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route(r)
def api_help():
    '''list all routes'''
    endpoints = sorted(
                      [rule.rule for rule in app.url_map.iter_rules() 
                      if rule.endpoint != 'static']
               )
    return jsonify(dict(routes=endpoints))
