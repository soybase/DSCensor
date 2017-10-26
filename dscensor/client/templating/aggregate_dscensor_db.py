#!/usr/bin/env python

import os, sys
import re
import argparse
import json
import datetime
import textwrap
import logging
import psycopg2
import psycopg2.extras
from server.summary_tools import fstools
#import simplejson as json
from jinja2 import Environment, FileSystemLoader
from shutil import copyfile


msg_format = '%(asctime)s|%(name)s|[%(levelname)s]: %(message)s'
logging.basicConfig(format=msg_format, datefmt='%m-%d %H:%M',
                    level=logging.DEBUG)
log_handler = logging.FileHandler(
                       './DSCensor_test.log')
formatter = logging.Formatter(msg_format)
log_handler.setFormatter(formatter)
logger = logging.getLogger('DSCensor_test')
logger.addHandler(log_handler)


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


def get_json_data(json_obj, data):
    for f in json_obj:
        val = int(json_obj[f])
        f = f.lower()
#        print f  #fill more of these in later
        if f == 'gene':
            data['genes'] = val
        elif f == 'mrna':
            data['mrnas'] = val
        elif f == 'five_prime_utr':
            data['5p_utrs'] = val
        elif f == 'three_prime_utr':
            data['3p_utrs'] = val
        elif f == 'cds':
            data['cds'] = val
        elif f == 'exon':
            data['exons'] = val


def dscensor_test():
    run_dir = os.path.dirname(os.path.realpath(__file__))
    data = {
            'header' : ['Unique Label', 'Origin',
                        'Genus', 'Species', 'infraspecies',
                        'Common Name',
                        'Chromosomes', 'Super Contigs',
                        'Linkage Groups', 'Genetic Markers', 'QTLs',
                        'Syntenic Regions', 'Consensus Regions', 'Primers',
                        'Genes', 'mRNAs', 'Exons', 'Polypeptides', 'CDS',
                        "3' UTR", "5' UTR",
                        'Polypeptide Domains', 'HMM Matches', 'Protein Matches'
                       ],
            'counts' : {},
            'partition' : {'name' : 'Origin', 'children' : []},
            'table_data' : [],
            'json_data' : '',
            'json_header' : '',
            'json_table_data' : '',
            'json_partition_data' : ''
           }
    origins = {}
    check_me = {}
    genus = {}
    db = connect_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    search_path = '''set search_path to dscensor'''
    cursor.execute(search_path)
    query = '''select genus, species, infraspecies, common_name, genome_name,
                 annotation_name, genome_origin, genome_counts, genome_build, 
                 annotation_build, annotation_counts 
               from organisms join genomes g using (organism_id) 
               join annotations a on g.genome_id=a.genome_id'''
    cursor.execute(query)
    result = cursor.fetchall()
    counts = data['counts']
    cursor.close()
    db.close()
    for r in result:
        org_species = r['species']
        org_genus = r['genus']
        org_infra = r['infraspecies']
        genome_data = r['genome_counts']
        annotation_data = r['annotation_counts']
        origin = r['genome_origin']
        org_cname = r['common_name']
        gnmv = r['genome_build']
        annv = r.get('annotation_build', None)
        if not annv:
            continue
        label = '{}_{}_{}_{}_{}'.format(org_genus, org_species,
                                     org_infra, gnmv, annv)
        if label in counts:
            logger.warning('duplicate annotation should not occur... {}'.format(
                                                                         label))
            continue
        datum = {'label' : label, 'origin' : origin,
                 'org_infra' : org_infra, 'org_genus' : org_genus,
                 'org_species' : org_species, 'org_cname' : org_cname,
                 'chrs' : 0, 'scaffolds' : 0, 'lgs' : 0, 'gms' : 0,
                 'qtls' : 0, 'syn_regs' : 0, 'con_regs' : 0, 
                 'primers' : 0, '5p_utrs' : 0, '3p_utrs' : 0, 'cds' : 0,
                 'genes' : 0, 'mrnas' : 0, 'exons' : 0, 'pps' : 0,
                 'ppds' : 0, 'hmms' : 0, 'prot_matches' : 0}
        counts[label] = datum
        if not fstools.check_file(genome_data):
            logger.error('could not find feature counts for {}'.format(
                                                        annotation_data))
            return False
        f_obj = fstools.return_filehandle(annotation_data)
        json_ann_obj = json.loads(f_obj.read())
        get_json_data(json_ann_obj, counts[label])
        f_obj.close()
        f_obj = fstools.return_filehandle(genome_data)
        json_gnm_obj = json.loads(f_obj.read())
        get_json_data(json_gnm_obj, counts[label])
        f_obj.close()
        if origin not in origins:
            origins[origin] = []
            check_me[origin] = {}
        if org_genus not in genus:
            genus[org_genus] = []
        if org_genus not in check_me[origin]:
            check_me[origin][org_genus] = 1
            origins[origin].append(org_genus)
        genus[org_genus].append(datum)
#        print datum
                    
#    sys.exit(1)
#    with open(metadata) as fopen:
#        counts = data['counts']
#        for line in fopen:
#            line = line.rstrip()
#            if line.startswith('#') or line.isspace() or not line:
#                continue
#            fields = line.split('\t')
#            try:
#                org_id = int(fields[0])
#            except:
#                org_id = fields[0]
#            org_genus = fields[1]
#            org_species = fields[2]
#            org_cname = fields[3]
#            count = int(fields[4])
#            ftype = fields[6]
#            origin = fields[7]
#            label = '{}_{}_{}_{}'.format(origin, org_genus, org_species, org_id)
#            if label not in counts:
#                datum = {'label' : label, 'origin' : origin,
#                         'org_id' : org_id, 'org_genus' : org_genus,
#                         'org_species' : org_species, 'org_cname' : org_cname,
#                         'chrs' : 0, 'scaffolds' : 0, 'lgs' : 0, 'gms' : 0,
#                         'qtls' : 0, 'syn_regs' : 0, 'con_regs' : 0, 
#                         'primers' : 0,
#                         'genes' : 0, 'mrnas' : 0, 'exons' : 0, 'pps' : 0,
#                         'ppds' : 0, 'hmms' : 0, 'prot_matches' : 0}
#                if origin not in origins:
#                    origins[origin] = []
#                    check_me[origin] = {}
#                if org_genus not in genus:
#                    genus[org_genus] = []
#                if org_genus not in check_me[origin]:
#                    check_me[origin][org_genus] = 1
#                    origins[origin].append(org_genus)
#                genus[org_genus].append(datum)
#                counts[label] = datum
#            if ftype == 'chromosome':
#                counts[label]['chrs'] = count
#            elif ftype == 'consensus_region':
#                counts[label]['con_regs'] = count
#            elif ftype == 'exon':
#                counts[label]['exons'] = count
#            elif ftype == 'gene':
#                counts[label]['genes'] = count
#            elif ftype == 'genetic_marker':
#                counts[label]['gms'] = count
#            elif ftype == 'linkage_group':
#                counts[label]['lgs'] = count
#            elif ftype == 'mRNA':
#                counts[label]['mrnas'] = count
#            elif ftype == 'polypeptide':
#                counts[label]['pps'] = count
#            elif ftype == 'polypeptide_domain':
#                counts[label]['ppds'] = count
#            elif ftype == 'primer':
#                counts[label]['primers'] = count
#            elif ftype == 'protein_hmm_match':
#                counts[label]['hmms'] = count
#            elif ftype == 'protein_match':
#                counts[label]['prot_matches'] = count
#            elif ftype == 'QTL':
#                counts[label]['qtls'] = count
#            elif ftype == 'supercontig':
#                counts[label]['scaffolds'] = count
#            elif ftype == 'syntenic_region':
#                counts[label]['syn_regs'] = count
#            last = label
    partition = data['partition']['children']
    count = 0
    for o in origins:
     #   print len(origins[o])
        partition.append({'name' : o, 
                          'children' : []})
        p_g = partition[count]['children']
        for g in origins[o]:
      #      print len(genus[g])
            p_g.append({'name' : g,
                        'color' : '{} 0'.format(g),
                        'children' : []})
            p_o = p_g[-1]['children']
            for c in genus[g]:
                if c['origin'] != o:
                    continue
                label = c['label']
                colors = label.split('_')
                cstring = '{} {}'.format(colors[0], colors[1])
                p_o.append(
                       {'name' : label,
                        'color' : cstring,
                        'children' : [
                            {'name' : 'Genes', 'count' : 1, 'number' : c['genes']},
                            {'name' : 'mRNAs', 'count' : 1, 'number' : c['mrnas']},
                            {'name' : 'Exons', 'count' : 1, 'number' : c['exons']},
                            {'name' : 'Polypeptides', 'count' : 1, 'number' : c['pps']},
                            {'name' : 'LGs', 'count' : 1, 'number' : c['lgs']},
                            {'name' : 'Chromosomes', 'count' : 1, 'number' : c['chrs']},
                            {'name' : 'Genetic Markers', 'count' : 1, 'number' : c['gms']},
                            {'name' : 'Scaffolds', 'count' : 1, 'number' : c['scaffolds']}
                        ]
                       }
                )
        count += 1
    ordered = []
    for d in counts:
        o = counts[d]
        datum = [o['label'], o['origin'],
                 o['org_genus'], o['org_species'], o['org_infra'], 
                 o['org_cname'], o['chrs'], o['scaffolds'],
                 o['lgs'], o['gms'], o['qtls'], o['syn_regs'],
                 o['con_regs'], o['primers'], o['genes'],
                 o['mrnas'], o['exons'], o['pps'], o['cds'],
                 o['5p_utrs'], o['3p_utrs'], o['ppds'],
                 o['hmms'], o['prot_matches']]
        data['table_data'].append(datum)
        ordered.append(o)
    header = [{'title' : h} for h in data['header']]
    json_header = json.dumps(header)
    json_data = json.dumps(ordered)
    json_table_data = json.dumps(data['table_data'])
    json_partition_data = json.dumps(data['partition'])
#    print json_header
#    print json_data
#    print json_table_data
    data['json_header'] = json_header
    data['json_data'] = json_data
    data['json_table_data'] = json_table_data
    data['json_partition_data'] = json_partition_data
    env = Environment(loader=FileSystemLoader(run_dir), lstrip_blocks=True, trim_blocks=True)
    template = env.get_template('templates/js.jinja')
    #print data
    #print json_header
    #print data['results'][0]['data'][0]
    return template.render(data=data)
    #print template.render(data=data)


if __name__ == '__main__':
    dscensor_test()

