#!/usr/bin/env python

import os, sys
import string
import subprocess
import logging
import argparse
import simplejson as json
import re
import datetime
import gzip
import psycopg2
import psycopg2.extras
import summary_tools.FastaMetrics as fmetrics
import summary_tools.FeatureCounts as fcounts
from summary_tools.fstools import create_directories, check_file
from glob import glob

#from ongenome import app, session, g

parser = argparse.ArgumentParser(description='''

    Loader for Summary Portal Testing

''', formatter_class=argparse.RawTextHelpFormatter)

#parser.add_argument('--fasta', metavar = '<my.gnmN.fasta>',
#help='''Fasta file to generate metrics for.  Can be compressed\n\n''')

#parser.add_argument('--gff', metavar = '<my.gnmN.annN.gff>',
#help='''Annotation file to generate counts for.  Can be compressed\n\n''')

parser.add_argument('--fasta', metavar = '<organism.genotype.build.key.whatever.fna.gz>',
help='''FASTA file for organism.  Will use README and FASTA to load organism, genome and stats information.  Name must follow prototype metavariable\n\n''')

parser.add_argument('--gff', metavar = '<organism.genotype.build.annversion.key.whatever.gff3.gz>',
help='''GFF3 File for this organism.  Fill in rest later\n\n''')

parser.add_argument('--genome_origin', metavar = '<STRING>',
help='''Origin database string for genome. ex. LIS\n\n''')

parser.add_argument('--annotation_origin', metavar = '<STRING>',
help='''Origin database string for annotations. ex. LIS\n\n''')

parser.add_argument('--json_obj', metavar = '<my_org_genome_annotations.json>',
help='''JSON object to load.  Don't use this if you aren't CTC or know what you are doing.\n\n''')

#parser.add_argument('--name', metavar = '<some.build.whatever>',
#help='''Unique Name for Genome\n\n''')

parser._optionals.title = "Program Options"
args = parser.parse_args()

msg_format = '%(asctime)s|%(name)s|[%(levelname)s]: %(message)s'
logging.basicConfig(format=msg_format, datefmt='%m-%d %H:%M',
                    level=logging.DEBUG)
log_handler = logging.FileHandler(
                       './generate_metrics.log')
formatter = logging.Formatter(msg_format)
log_handler.setFormatter(formatter)
logger = logging.getLogger('generate_metrics')
logger.addHandler(log_handler)

fmetrics = fmetrics.FastaMetrics(logger)
fcounts = fcounts.FeatureCounts(logger)


def connect_db():
    database = 'dscensor_dev'
        #    user = ''
    host = 'localhost'
        #    port = ''
        #    conn_str = 'host={} port={} dbname={} user={}'.format(
        #                host, port, database, user)
    conn_str = 'dbname={} host={}'.format(database, host)
    conn = ''
    try:
        conn = psycopg2.connect(conn_str)
        logger.info('connection succeeded {}'.format(conn_str))
    except psycopg2.Error as e:
        raise
    return conn


def fasta_metrics(outpref, fasta):
    logger.info('Generating FASTA metrics for {}...'.format(fasta))
    outfile = outpref + '.genomemetrics.json'
    if check_file(outfile):
        logger.warning('File {} already exists.  Remove to recreate'.format(
                                                                      outfile))
        return outfile
    fmetrics.generate_metrics(fasta)
    logger.info('Writing output to {}...'.format(outfile))
    fout = open(outfile, 'w')
    fout.write(json.dumps(fmetrics.metrics))
    fout.close()
    return outfile


def gff_features(outpref, gff):
    logger.info('Counting GFF features for {}...'.format(gff))
    outfile = outpref + '.gffmetrics.json'
    if check_file(outfile):
        logger.warning('File {} already exists.  Remove to recreate'.format(
                                                                      outfile))
        return outfile
    fcounts.count_gff_features(gff)
    logger.info('Writing output...')
    fout = open(outfile, 'w')
    fout.write(json.dumps(fcounts.gff_counts))
    fout.close()
    return outfile


def parse_attributes(target, t):
    target = os.path.basename(target)
    data = {'abbreviation' : '', 'key' : '', 'build' : '', 'infraspecies' : '',
            'name' : target}
    targets = target.split('.')
    if len(targets) < 6:
        logger.error('File must follow metavar convention. See usage') #this is a stupid message.  too cryptic.  fix later
        return False
    data['abbreviation'] = targets[0]
    data['infraspecies'] = targets[1]
    data['build'] = targets[2]
    if t == 'fa':
        data['key'] = targets[3]
    elif t == 'gff':
        data['annobuild'] = targets[3]
        data['key'] = targets[4]
    else:
        logger.error('format {} not recognized'.format(t))
        return False
    logger.debug(data)
    return data


def parse_readme(readme, data):
    sci_name = '#### Scientific Name'
    sci_name_abr = '#### Scientific Name Abbrev'
    common_name = '#### Common Name'
    sci_error = 'Complete scientific name not found for: {}'.format(readme)
    abr_error = 'Scientific abbreviation not found for: {}'.format(readme)
    count = 0
    sswitch = 0
    aswitch = 0
    cswitch = 0
    with open(readme) as fopen:
        for line in fopen:
            if line.isspace() or not line:
                continue
            line = line.rstrip()
            if line == sci_name:
                count = 0
                sswitch = 1
                continue
            if line == sci_name_abr:
                count = 0
                aswitch = 1
                continue
            if line == common_name:
                count = 0
                cswitch = 1
                continue
            count += 1
            if count%2 == 0:
                if sswitch:
                    if not len(line.split(' ')) >= 2:
                        logger.error(sci_error)
                        return False
                    data['genus'] = line.split(' ')[0]
                    data['species'] = line.split(' ')[1]
                    sswitch = 0
                if aswitch:
                    if not line:
                        logger.error(abr_error)
                        return False
                    abbrv = line
                    if abbrv != data['abbreviation']:
                        logger.warning('abbreviation mismatch between README and file naming.  Consider fixing.  Using README value {}'.format(abbrv))
                    data['abbreviation'] = abbrv
                    aswitch = 0
                if cswitch:
                    if not line:
                        logger.error(common_error)
                        return False
                    data['common_name'] = line
                    cswitch = 0
    data['datastore_home'] = readme
    logger.debug(data)


def load_organism(cursor, data):
    genus = data.get('genus', None)
    species = data.get('species', None)
    abbreviation = data.get('abbreviation', None)
    infraspecies = data.get('infraspecies', None)
    common_name = data.get('common_name', None)
    if not genus:
        logger.error('Genus not found for organism!')
        return False
    if not species:
        logger.error('Species not found for organism!')
        return False
    if not infraspecies:
        logger.error('Genotype not found for organism!')
        return False
    if not abbreviation:
        logger.error('Abbreviation not found for organism!')
        return False
    check = '''select organism_id from dscensor.organisms
                where genus=%s and species=%s and infraspecies=%s'''
    cursor.execute(check, [genus, species, infraspecies])
    result = cursor.fetchone()
    if not result:
        org_insert = '''insert into dscensor.organisms 
                          (genus, species, abbreviation, infraspecies, 
                           common_name) values
                          (%s, %s, %s, %s, %s)
                          returning organism_id
                     '''
        logger.info('Adding new organism {} {} {}...'.format(genus, species,
                                                                infraspecies))
        try:
            cursor.execute(org_insert, [genus, species, abbreviation, 
                                        infraspecies, common_name]
                          )
            data['organism_id'] = cursor.fetchone()['organism_id']
        except psycopg2.Error as e:
            logger.error('Failed to insert new organism: {}'.format(e))
            return False

    else:
        logger.warning('Organism {} {} {} already exists in DB'.format(genus,
                                                                     species,
                                                               infraspecies))
        data['organism_id'] = result['organism_id']
    return True


def load_genome(cursor, data):
    name = data.get('name', None)
    organism_id = data.get('organism_id', None)
    build = data.get('build', None)
    datastore_home = data.get('datastore_home', None)
    counts = data.get('counts', None)
    genome_origin = data.get('genome_origin', None)
    if not name:
        logger.error('Name must exist for genome... Strange...')
        return False
    if not counts:
        logger.error('Counts must exist for genome... Strange...')
        return False
    if not genome_origin:
        logger.error('Genome Origin must exist for genome...')
        return False
    check = '''select genome_id from dscensor.genomes where genome_name=%s'''
    cursor.execute(check, [name])
    result = cursor.fetchone()
    if not result:
        logger.info('Adding new genome {}'.format(name))
        genome_insert = '''insert into dscensor.genomes
                            (genome_name, organism_id, genome_build, 
                             genome_home, genome_origin, genome_counts)
                           values
                            (%s, %s, %s, %s, %s, %s)
                           returning genome_id
                        '''
        try:
            cursor.execute(genome_insert, [name, organism_id, build, 
                                           datastore_home, genome_origin,
                                           counts])
            return cursor.fetchone()['genome_id']
        except psycopg2.Error as e:
            logger.error('Could not insert new genome {}'.format(name))
            return False
    else:
        logger.warning('Genome {} already exists in DB'.format(name))
        return result['genome_id']


def load_annotation(cursor, data):
    name = data.get('name', None)
    build = data.get('annobuild', None)
    organism_id = data.get('organism_id', None)
    genome_id = data.get('genome_id', None)
    datastore_home = data.get('datastore_home', None)
    form = data.get('format', None)
    counts = data.get('counts', None)
    annotation_origin = data.get('annotation_origin', None)
    if not name:
        logger.error('Name must exist for annotation... Strange...')
        return False
    if not counts:
        logger.error('Counts must exist for annotation... Strange...')
        return False
    if not annotation_origin:
        logger.error('Annotation Origin must exist for genome...')
        return False
    check = '''select annotation_id from dscensor.annotations 
               where annotation_name=%s'''
    cursor.execute(check, [name])
    result = cursor.fetchone()
    if not result:
        logger.info('Adding new annotation {}'.format(name))
        annotation_insert = '''insert into dscensor.annotations
                            (annotation_name, annotation_build, 
                             organism_id, genome_id, 
                             annotation_home, format, 
                             annotation_origin, annotation_counts)
                           values
                            (%s, %s, %s, %s, %s, %s, %s, %s)
                        '''
        try:
            cursor.execute(annotation_insert, [name, build, organism_id, 
                                               genome_id, datastore_home, form,
                                               annotation_origin, counts])
        except psycopg2.Error as e:
            logger.error('Could not insert new annotation {}: {}'.format(name,
                                                                         e))
            return False
    else:
        logger.warning('Annotation {} already exists in DB'.format(name))
    return True


if __name__ == '__main__':
    fasta = args.fasta
    gff = args.gff
    json_obj = args.json_obj
    genome_origin = args.genome_origin
    annotation_origin = args.annotation_origin
    gff_data = {}
    fasta_data = {}
    if json_obj:
        try:
            json_obj = json.loads(open(json_obj).read())
        except ValueError as e:
            logger.error('Issue loading JSON file: {}'.format(e))
            sys.exit(1)
        if not json_obj:
            logger.error('JSON object appears to be empty...')
            sys.exit(1)
        fasta_data = json_obj.get('fasta_data', None)
        gff_data = json_obj.get('gff_data', None)
        if not fasta_data:
            logger.error('fasta_data attribute is None')
            sys.exit(1)
        if not check_file(fasta_data['datastore_home']):
            logger.error('datastore_home must point to FASTA file')
            sys.exit(1)
        fasta = os.path.abspath(fasta_data['datastore_home'])
        out_json = '/work/ctc/apps/dscensor/dscensor/server/cstore/json/{}'.format(
                                                    os.path.basename(fasta)
                                                    )
        fasta_data['counts'] = fasta_metrics(out_json, fasta)
        db = connect_db()
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if not load_organism(cursor, fasta_data):
            logger.error('Organism load failed!')
            sys.exit(1)
        cursor.close()
        db.commit()
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        genome_id = load_genome(cursor, fasta_data)
        if not genome_id:
            logger.error('Genome load failed!')
            sys.exit(1)
        cursor.close()
        db.commit()
        if gff_data:
            if not check_file(gff_data['datastore_home']):
                logger.error('datastore_home must point to GFF file')
                sys.exit(1)
            gff = os.path.abspath(gff_data['datastore_home'])
            gff_data['genome_id'] = genome_id
            gff_data['organism_id'] = fasta_data['organism_id']
            if not gff_data:
                logger.error('Data could not be retrieved from {}'.format(gff))
                sys.exit(1)
            out_json = '/work/ctc/apps/dscensor/dscensor/server/cstore/json/{}'.format(
                                                        os.path.basename(gff)
                                                        )
            gff_data['counts'] = gff_features(out_json, gff)
            cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            if not load_annotation(cursor, gff_data):
                logger.error('Annotation load failed!')
                sys.exit(1)
            cursor.close()
            db.commit()
        sys.exit(0)
    if not fasta:
        logger.error('FASTA file required')
        sys.exit(1)
    if not check_file(fasta):
        logger.error('FASTA file {} Not Found'.format(fasta))
        sys.exit(1)
    fasta = os.path.abspath(fasta)
    logger.info('Parsing File Structure...')
    fasta_data = parse_attributes(fasta, 'fa') #get build, key, do checks. see method.
    if not fasta_data:
        logger.error('Data could not be retrieved from {}'.format(fasta))
        sys.exit(1)
    org_readme = '{}/README.{}.md'.format(os.path.dirname(fasta), 
                                           fasta_data['key'])
    if not check_file(org_readme):
        logger.error('README {} could not be located'.format(org_readme))
        sys.exit(1)
    parse_readme(org_readme, fasta_data)
    out_json = '/work/ctc/apps/dscensor/dscensor/server/cstore/json/{}'.format(
                                                    os.path.basename(fasta)
                                                    )
    fasta_data['counts'] = fasta_metrics(out_json, fasta)
    fasta_data['genome_origin'] = genome_origin
    db = connect_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    fasta_data['datastore_home'] = fasta
    if not load_organism(cursor, fasta_data):
        logger.error('Organism load failed!')
        sys.exit(1)
    cursor.close()
    db.commit()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    genome_id = load_genome(cursor, fasta_data)
    if not genome_id:
        logger.error('Genome load failed!')
        sys.exit(1)
    cursor.close()
    db.commit()
    json_obj = {}
    json_obj['fasta_data'] = fasta_data
    if gff:
        if not check_file(gff):
            logger.error('GFF file {} Not Found'.format(gff))
            sys.exit(1)
        gff = os.path.abspath(gff)
        gff_data = parse_attributes(gff, 'gff')
        gff_data['genome_id'] = genome_id
        gff_data['datastore_home'] = gff
        gff_data['organism_id'] = fasta_data['organism_id']
        gff_data['annotation_origin'] = annotation_origin
        if not gff_data:
            logger.error('Data could not be retrieved from {}'.format(gff))
            sys.exit(1)
        out_json = '/work/ctc/apps/dscensor/dscensor/server/cstore/json/{}'.format(
                                                    os.path.basename(gff)
                                                    )
        gff_data['counts'] = gff_features(out_json, gff)
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if not load_annotation(cursor, gff_data):
            logger.error('Annotation load failed!')
            sys.exit(1)
        json_obj['gff_data'] = gff_data
        cursor.close()
        db.commit()
    json_out = open('./loaded_object.json', 'w')
    json_out.write(json.dumps(json_obj) + '\n')

