###############################################################################
#                  Application to run tests for DSCensor                      #
#                      Connor Cameron (ctc@ncgr.org)                          #
#                      Andrew Farmer  (adf@ncgr.org)                          #
###############################################################################

import os
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
#from client.templating import generate_for_render, aggregate_dscensor_db
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

LOGFILE = 'logs/dscensor.log'
MAXLOGBYTES = 1024 * 1024
MAXLOGFILES = 10

# create flask app
app = Flask(__name__, template_folder='client')
app.config.from_object(__name__)
app.config.update(dict(
    HOST='localhost',
    DATABASE='dscensor_dev',
    PORT=5432,
    SECRET_KEY='this is some secret',
    USERNAME='ctc',
    PASSWORD='',
#    JSONIFY_PRETTYPRINT_REGULAR=False,
    API_PATH='/api/v1'
))

# WILL FILL HERE FOR INITIAL DATA an api view will be required here to serve it

msg_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = Formatter(msg_format)
handler = RotatingFileHandler(
    LOGFILE,
    maxBytes=MAXLOGBYTES,
    backupCount=MAXLOGFILES
)
handler.setFormatter(formatter)

if app.debug:
    handler.setLevel(logging.DEBUG)
else:
    handler.setLevel(logging.INFO)
# Also add the handler to gunicorns loggers and
# let app see the handler for logging inside views
gunicorn_error = logging.getLogger('gunicorn.error')
gunicorn_access = logging.getLogger('gunicorn.access')
gunicorn_error.addHandler(handler)
gunicorn_access.addHandler(handler)
app.logger.addHandler(handler)

# setup large example
#app.large_example = generate_for_render.render_large_example()
#app.dscensor_example = aggregate_dscensor_db.dscensor_test()
# imports which expect plateparty.app to exist:
#from database import postgres_db_connect
import views

# this exists for gunicorn invocation
if __name__ == '__main__':
    app.run()
