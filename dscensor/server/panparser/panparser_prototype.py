#!/usr/bin/env python

import os
import sys



def clean_ids(my_id):
    '''Removes transcript part of <geneid>.<transcript> if exists'''
    new_id = '.'.join(my_id.split('.')[:-1])
    return new_id


def un_yukify(my_id):
    '''Removes upstream DS information from fully qualified gene names

       ex: glyma.Wm82.gnm1.ann1.Glyma16g30815

       becomes: Glyma16g30815
    '''
    new_id = '.'.join(my_id.split('.')[4:])
    return new_id


def parse_pansets(dataset):
    '''Parses hsh.tsv file for gene assignment'''
    genes = {}
    with open(dataset) as fopen:
        for line in fopen:
            line = line.rstrip()
            if line.startswith('#') or not line:
                continue
            (panset, transcript) = line.split('\t')
            gene = clean_ids(transcript)
            short_name = un_yukify(gene)
            genes[gene] = panset
            genes[short_name] = panset
    return genes


def parse_clusters(dataset):
    '''Parses clust.tsv file for pan set assignment'''
    pansets = {}
    with open(dataset) as fopen:
        for line in fopen:
            line = line.rstrip()
            if line.startswith('#') or not line:
                continue
            panset = line.split('\t')[0]
            pansets[panset] = [ clean_ids(t) for t in line.split('\t')[1:]]
    return pansets


def main():
    '''Main runtime for import

       Needs to be expanded to db access to scale
    '''
    my_datasets = ['glysp.mixed.pan2.TV81']
    dataset_dir = './panparser'
    datasets = {}
    for d in my_datasets:
        my_hsh = f'{os.path.abspath(dataset_dir)}/{d}.hsh.tsv'
        my_clust = f'{os.path.abspath(dataset_dir)}/{d}.clust.tsv'
        pansets = parse_pansets(my_hsh)  # get pansets from files
        clusters = parse_clusters(my_clust)  # get clusters from files
        datasets[d] = {'pansets': pansets, 'clusters': clusters}
    return datasets


if __name__ == '__main__':
    main()

