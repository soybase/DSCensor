import os, sys
import psycopg2
import psycopg2.extras
from psycopg2.pool import ThreadedConnectionPool
from contextlib import contextmanager
from dscensor import app, session, g

MIN_CONNECTIONS = 2
MAX_CONNECTIONS = 50  # postgresql default is 100

logger = app.logger
logger.info('setting up db connection pool')

db_pool = ''

try:
    db_pool = ThreadedConnectionPool(
        MIN_CONNECTIONS,
        MAX_CONNECTIONS,
        database = app.config['DATABASE'],
        user = app.config['USERNAME'],
        host = app.config['HOST'],
        port = app.config['PORT']
    )
except psycopg2.Error as e:
    error_msg = 'Could not create postgres connection pool: {}'.format(e)
    logger.error(error_msg)
    sys.exit(1)


@contextmanager
def get_pooled_connection():
    '''
    psycopg2 connection context manager.
    Fetch a connection from the connection pool and release it.
    '''
    try:
        connection = db_pool.getconn()
        yield connection
    finally:
        if connection:
            db_pool.putconn(connection)


@contextmanager
def get_pooled_cursor(commit=False):
    '''
    psycopg2 cursor context manager.
    Get a cursor into the db from the pooled coonections
    '''
    with get_pooled_connection() as connection:
        cursor = connection.cursor(
                            cursor_factory=psycopg2.extras.RealDictCursor
                 )
        try:
            yield cursor
            if commit:
                connection.commit()
        finally:
            cursor.close()


@app.cli.command('initSchema')
def initdb_command():
    '''Initializes the schema.'''
    try:
        with get_pooled_cursor(commit=True) as cursor:
            open_me = 'database/ongenome_schema/ongenome-schema.sql'
            with app.open_resource(open_me, mode='r') as f:
                try:
                    cursor.execute(f.read())
                except psycopg2.Error as e:
                    logger.error('Error occured on db init {}'.format(e))
                    sys.exit(1)
        logger.info('Initialized the schema.')
    except psycopg2.Error as e:
        logger.error('Error occured on cursor {}'.format(e))
        sys.exit(1)


@app.cli.command('dropSchema')
def dropschema_command():
    '''Drop the schema.'''
    try:
        with get_pooled_cursor(commit=True) as cursor:
            delete = '''drop schema ongenome cascade'''
            logger.info('Drop ongenome from {}...'.format(app.config['DATABASE']))
            try:
                cursor.execute(delete)
            except psycopg2.Error as e:
                logger.error('Error occured on schema drop {}'.format(e))
                sys.exit(1)
    except psycopg2.Error as e:
        logger.error('Error occured on cursor {}'.format(e))
        sys.exit(1)
    logger.info('Dropped\nDone')

