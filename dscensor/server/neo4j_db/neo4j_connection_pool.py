import os, sys
import logging
from contextlib import contextmanager
from neo4j.v1 import GraphDatabase, basic_auth
from dscensor import app, session, g

logger = app.logger
driver = False

#    '''connects a driver (which serves as a connection pool)
#       https://neo4j.com/docs/api/python-driver/current/driver.html'''
bolt = 'bolt:{}:{}'.format(app.config['NEO4J_HOST'], app.config['NEO4J_PORT'])
print(bolt)
driver = GraphDatabase.driver(bolt,
                              auth=basic_auth(app.config['NEO4J_AUTH'], 
                                              app.config['NEO4J_PSWD']))
logger.info('connection succeeded, driver:{}'.format(driver))

@contextmanager
def get_session():
    '''Allows the API to get sessions from the driver'''
    session = False
    try:
        session = driver.session()
        yield session
    finally:  #if things go really wrong interpreter should handle... jic
        if session:
            session.close()
