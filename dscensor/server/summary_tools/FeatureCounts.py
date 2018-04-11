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

class FeatureCounts:

    def __init__(self, logger, **kwargs):
        if not logger:
            self.logger = sys.stderr
            self.logger.error = sys.stderr.write
        else:
            self.logger = logger
        self.gff_counts = {}
        self.gnm_name = ''

    def get_gnm_name(self, genome):  #this is questionable...
        name = os.path.basename(genome)
        l = len(name.split('.'))
        i = l - 3 #3 is the number of fields for the extensions
        gnm = name.split('.')[-4]
        name = name.split('.')[:i]
        self.gnm_name = name
        return name

    def count_gff_features(self, gff):
        logger = self.logger
        counts = self.gff_counts
        if not check_file(gff):
            logger.error('could not locate {}'.format(gff))
            sys.exit(1)
        fh = return_filehandle(gff)
        if not fh:
            logger.error('could not open {}'.format(gff))
            sys.exit(1)
        with fh as fopen:
            for line in fopen:
                if not line or line.isspace() or line.startswith('#'):
                    continue
                line = line.rstrip()
                f = line.split('\t')
                if f[2] not in counts:
                    counts[f[2]] = 1
                    continue
                counts[f[2]] += 1
        fh.close()


if __name__ == '__main__':
    print('Class for Counts summary tools.  Please import')
    sys.exit(1)

