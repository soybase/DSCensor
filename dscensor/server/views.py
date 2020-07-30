import re
from datetime import datetime
from subprocess import check_call
from dscensor import app, session, g, render_template, request
from flask import render_template_string, make_response, jsonify, send_file
from neo4j_db import neo4j_connection_pool as cpool
from api import api_help, derived_from, taxa_list, nodes, pangenes

logger = app.logger

@app.route('/')
def document_root():
    '''list all routes'''
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    endpoints = sorted(
                      [rule.rule for rule in app.url_map.iter_rules()
                      if rule.endpoint != 'static']
               )
    return jsonify(dict(routes=endpoints))
