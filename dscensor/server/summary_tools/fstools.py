#!/usr/bin/env python

import time
import sys, os
import subprocess
import errno
import gzip
import json
#import bz2
import zipfile

USAGE='''
fstools.py
usage: {} 
'''.format(sys.argv[0])

def check_file(file):
    b = False
    if not isinstance(file, str):
        raise ValueError('file must be a string')
    try:
        b = os.path.isfile(file) #get bool
    except OSError:
        raise
    if b:
        return True
    else:
        return False


def remove_file(file):
    try:
        os.remove(file)
    except OSError:
        raise


def check_directory(directory):
    b = False
    if not isinstance(directory, str):
        raise ValueError('directory must be a string')
    try:
        b = os.path.isdir(directory) #get bool
    except OSError:
        raise
    if b:
        return True
    else:
        return False


def create_directory(directory):
    if not isinstance(directory, str):
        raise ValueError('directory must be a string')
    try:
        os.mkdir(directory, 0o755)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def create_directories(path):
    if not isinstance(path, str):
        raise ValueError('path must be a string')
    try:
        os.makedirs(path, 0o755)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

 
def change_directory(directory):
    try:
        os.chdir(directory)
    except OSError:
        raise


def absolute_path(file):
    abs_path = ''
    try:
        abs_path = os.path.abspath(file)
    except OSError:
        raise
    if abs_path:
        return abs_path
    return False


def file_size(file):
    size = 0
    if absolute_path(file):
        try:
            size = os.path.getsize(absolute_path(file))
        except OSError:
            raise
        return size
    return False


def return_filehandle(open_me):
    magic_dict = {
                  '\x1f\x8b\x08': 'gz',
 #                 '\x42\x5a\x68': 'bz2',
                  '\x50\x4b\x03\x04': 'zip'
                 }
    max_bytes = max(len(t) for t in magic_dict)
    with open(open_me) as f:
        s = f.read(max_bytes)
    for m in magic_dict:
        if s.startswith(m):
            t = magic_dict[m]
            if t == 'gz':
                return gzip.open(open_me)
  #          elif t == 'bz2':
  #              return bz2.open(open_me)
            elif t == 'zip':
                return zipfile.open(open_me)
    return open(open_me)


def return_json(read_me):
    json_obj = json.loads(open(read_me).read())
    return json_obj

