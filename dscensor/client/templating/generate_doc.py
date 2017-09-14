#!/usr/bin/env python

import os, sys
import re
import argparse
import json
import datetime
import textwrap
#import simplejson as json
from jinja2 import Environment, FileSystemLoader
from shutil import copyfile

parser = argparse.ArgumentParser(description="""
Example Organism Feature Ontology Data Formatter
""", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--feature_table', metavar = '<feature_counts.tab>', required=True,
help="""Table of features to parse into report.\nAs this is an example the fields are fixed.\nSee '/work/ctc/LIS/organism_feature_counts/organism_feature_count.tsv'\n\n""")

parser._optionals.title = "Program Options"

args = parser.parse_args()


if __name__ == '__main__':
    metadata = args.feature_table
    data = {
            'header' : ['Unique Label', 'Origin',
                        'Organism ID', 'Genus', 'Species', 'Common Name',
                        'Chromosomes', 'Super Contigs',
                        'Linkage Groups', 'Genetic Markers', 'QTLs', 
                        'Syntenic Regions', 'Consensus Regions', 'Primers',
                        'Genes', 'mRNAs', 'Exons', 'Polypeptides',
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
    with open(metadata) as fopen:
        counts = data['counts']
        for line in fopen:
            line = line.rstrip()
            if line.startswith('#') or line.isspace() or not line:
                continue
            fields = line.split('\t')
            try:
                org_id = int(fields[0])
            except:
                org_id = fields[0]
            org_genus = fields[1]
            org_species = fields[2]
            org_cname = fields[3]
            count = int(fields[4])
            ftype = fields[6]
            origin = fields[7]
            label = '{}_{}_{}_{}'.format(origin, org_genus, org_species, org_id)
            if label not in counts:
                datum = {'label' : label, 'origin' : origin,
                         'org_id' : org_id, 'org_genus' : org_genus,
                         'org_species' : org_species, 'org_cname' : org_cname,
                         'chrs' : 0, 'scaffolds' : 0, 'lgs' : 0, 'gms' : 0,
                         'qtls' : 0, 'syn_regs' : 0, 'con_regs' : 0, 
                         'primers' : 0,
                         'genes' : 0, 'mrnas' : 0, 'exons' : 0, 'pps' : 0,
                         'ppds' : 0, 'hmms' : 0, 'prot_matches' : 0}
                if origin not in origins:
                    origins[origin] = []
                    check_me[origin] = {}
                if org_genus not in genus:
                    genus[org_genus] = []
                if org_genus not in check_me[origin]:
                    check_me[origin][org_genus] = 1
                    origins[origin].append(org_genus)
                genus[org_genus].append(datum)
                counts[label] = datum
            if ftype == 'chromosome':
                counts[label]['chrs'] = count
            elif ftype == 'consensus_region':
                counts[label]['con_regs'] = count
            elif ftype == 'exon':
                counts[label]['exons'] = count
            elif ftype == 'gene':
                counts[label]['genes'] = count
            elif ftype == 'genetic_marker':
                counts[label]['gms'] = count
            elif ftype == 'linkage_group':
                counts[label]['lgs'] = count
            elif ftype == 'mRNA':
                counts[label]['mrnas'] = count
            elif ftype == 'polypeptide':
                counts[label]['pps'] = count
            elif ftype == 'polypeptide_domain':
                counts[label]['ppds'] = count
            elif ftype == 'primer':
                counts[label]['primers'] = count
            elif ftype == 'protein_hmm_match':
                counts[label]['hmms'] = count
            elif ftype == 'protein_match':
                counts[label]['prot_matches'] = count
            elif ftype == 'QTL':
                counts[label]['qtls'] = count
            elif ftype == 'supercontig':
                counts[label]['scaffolds'] = count
            elif ftype == 'syntenic_region':
                counts[label]['syn_regs'] = count
            last = label
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
                cstring = '{} {}'.format(colors[1], colors[2])
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
                 o['org_id'], o['org_genus'], o['org_species'],
                 o['org_cname'], o['chrs'], o['scaffolds'],
                 o['lgs'], o['gms'], o['qtls'], o['syn_regs'],
                 o['con_regs'], o['primers'], o['genes'],
                 o['mrnas'], o['exons'], o['pps'], o['ppds'],
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
    env = Environment(loader=FileSystemLoader('/work/ctc/apps/dscensor/dscensor/server/templating'), lstrip_blocks=True, trim_blocks=True)
    template = env.get_template('templates/js.jinja')
    #print data
    #print json_header
    #print data['results'][0]['data'][0]
    print template.render(data=data)

