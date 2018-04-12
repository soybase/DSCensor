#!/usr/bin/env python

import os, sys
import argparse
import re
import subprocess
import datetime
import gzip
import zipfile
#import bz2
import logging
from .fstools import check_file, return_filehandle

class FastaMetrics:

    def __init__(self, logger, **kwargs):
        if not logger:
            self.logger = sys.stderr
            self.logger.error = sys.stderr.write
        else:
            self.logger = logger
        self.metrics = {'N50' : 0, 'N90' : 0, 'L50' : 0,
                        'contigN50' : 0, 'scaffoldN50' : 0,
                        'gaps' : 0, 'gapN50' : 0, 'maxgap' : 0, 'mingap' : 0,
                        'contigs' : 0, 'scaffolds' : 0, 'records' : 0,
                        'maxscaffold' : 0, 'minscaffold' : 0,
                        'maxcontig' : 0, 'mincontig' : 0,
                        'contigbases' : 0, 'scaffoldbases' : 0, 'gapbases' : 0,
                        'allbases' : 0, 'pgc' : 0}
        self.fasta_header = re.compile("^>(\S+)\s*(.*)")
        self.bases = {'A' : 0, 'a' : 0, 'C' : 0, 'c' : 0,
                      'T' : 0, 't' : 0, 'G' : 0, 'g' : 0,
                      'N' : 0, 'n' : 0, 'IUPAC' : 0, 'total' : 0}
        self.lengths = {'scaffolds' : [], 'gaps' : [], 
                        'contigs' : [], 'total' : []}
        self.min_gap = 10  #for kwargs if i want to them
        self.min_contig = 0
        self.min_scaffold = 0

    def get_N50(self, contigs, total):
        c = 0
        n = 0
        for l in reversed(contigs):
            c += int(l)
            n += 1
            if c >= float(total)/2:
                return l

    def get_gc(self):
        gc = self.bases['G'] + self.bases['C']
        total = self.bases['total']
        if not total or not gc:
            return False
        pgc = float(gc)/int(total)
        self.metrics['pgc'] = pgc

    def generate_metrics(self, fasta):
        logger = self.logger
        hcheck = self.fasta_header
        bases = self.bases
        metrics = self.metrics
        min_gap = self.min_gap
        lengths = self.lengths
        scheck = 0
        gcheck = 0
        ccheck = 0
        glen = 0
        clen = 0
        slen = 0
        length = 0
        i = 0
        seq = []
        if not check_file(fasta):
            logger.error('could not locate {}'.format(fasta))
            sys.exit(1)
        fh = return_filehandle(fasta)
        if not fh:
            logger.error('could not open {}'.format(fasta))
            sys.exit(1)
        with fh as fopen:
            for line in fopen:
                if not line or line.isspace():
                    continue
                line = line.rstrip()
                if hcheck.match(line):
                    #similar to gaemr logic
                    metrics['records'] += 1
                    if seq:
                        seq = str(''.join(seq)).upper()
                        length = len(seq)
                        bases['total'] += length
                        lengths['total'].append(length)
                        while True:
                            i = seq.find('N', i)
                            if i < 0:
                                if not scheck:
                                    lengths['contigs'].append(length)
                                    metrics['contigs'] += 1
                                    metrics['contigbases'] += length
                                    for b in seq:
                                        if b in bases:
                                            bases[b] += 1
                                        else:
                                            bases['IUPAC'] += 1
                                else:
                                    clen = length - ccheck
                                    lengths['contigs'].append(clen)
                                    metrics['contigs'] += 1
                                    metrics['contigbases'] += clen
                                    for b in seq[ccheck:]:
                                        if b in bases:
                                            bases[b] += 1
                                        else:
                                            bases['IUPAC'] += 1
                                break
                            gcheck = i
                            while i < length and seq[i] == 'N':
                                i += 1
                            glen = i - gcheck
                            if glen >= min_gap:
                                scheck = 1
                                clen = gcheck - ccheck
                                lengths['gaps'].append(glen)
                                bases['N'] += glen
                                metrics['gaps'] += 1
                                metrics['gapbases'] += glen
                                lengths['contigs'].append(clen)
                                metrics['contigs'] += 1
                                metrics['contigbases'] += clen
                                for b in seq[ccheck:gcheck]:
                                    if b in bases:
                                        bases[b] += 1
                                    else:
                                        bases['IUPAC'] += 1
                                ccheck = i
                        if scheck:
                            metrics['scaffolds'] += 1
                            lengths['scaffolds'].append(length)
                            metrics['scaffoldbases'] += length
                    scheck = 0
                    gcheck = 0
                    ccheck = 0
                    glen = 0
                    clen = 0
                    i = 0
                    pos = 0
                    seq = []
                else:
                    seq.append(line)
        fh.close()
        if seq:
            seq = str(''.join(seq)).upper()
            length = len(seq)
            bases['total'] += length
            lengths['total'].append(length)
            while True:
                i = seq.find('N', i)
                if i < 0:
                    if not scheck:
                        lengths['contigs'].append(length)
                        metrics['contigs'] += 1
                        metrics['contigbases'] += length
                        for b in seq:
                            if b in bases:
                                bases[b] += 1
                            else:
                                bases['IUPAC'] += 1
                    else:
                        clen = length - ccheck
                        lengths['contigs'].append(clen)
                        metrics['contigs'] += 1
                        metrics['contigbases'] += clen
                        for b in seq[ccheck:]:
                            if b in bases:
                                bases[b] += 1
                            else:
                                bases['IUPAC'] += 1
                    break
                gcheck = i
                while i < length and seq[i] == 'N':
                    i += 1
                glen = i - gcheck
                if glen >= min_gap:
                    scheck = 1
                    clen = gcheck - ccheck
                    lengths['gaps'].append(glen)
                    bases['N'] += glen
                    metrics['gaps'] += 1
                    metrics['gapbases'] += glen
                    lengths['contigs'].append(clen)
                    metrics['contigs'] += 1
                    metrics['contigbases'] += clen
                    for b in seq[ccheck:gcheck]:
                        if b in bases:
                            bases[b] += 1
                        else:
                            bases['IUPAC'] += 1
                    ccheck = i
            if scheck:
                metrics['scaffolds'] += 1
                lengths['scaffolds'].append(length)
                metrics['scaffoldbases'] += length
        #contig N50
        lengths['contigs'] = sorted(lengths['contigs'])
        lengths['gaps'] = sorted(lengths['gaps'])
        lengths['scaffolds'] = sorted(lengths['scaffolds'])
        lengths['total'] = sorted(lengths['total'])
        metrics['maxcontig'] = lengths['contigs'][-1]
        metrics['mincontig'] = lengths['contigs'][0]
        metrics['maxgap'] = lengths['gaps'][-1]
        metrics['mingap'] = lengths['gaps'][0]
        metrics['maxscaffold'] = lengths['scaffolds'][-1]
        metrics['minscaffold'] = lengths['scaffolds'][0]
        metrics['contigN50'] = self.get_N50(
                                     lengths['contigs'], 
                                     metrics['contigbases']
                               )
        metrics['gapN50'] = self.get_N50(lengths['gaps'], 
                                         metrics['gapbases'])
        metrics['scaffoldN50'] = self.get_N50(
                                     lengths['scaffolds'], 
                                     metrics['scaffoldbases']
                                 )
        metrics['allbases'] = bases['total']
        metrics['N50'] = self.get_N50(lengths['total'], bases['total'])
        self.get_gc()


if __name__ == '__main__':
    print('Class for FASTA summary tools.  Please import')
    sys.exit(1)

