#!/usr/bin/python
from kropotkin import create_factspace, store_fact
from os import environ, walk
from os.path import abspath, join
from sys import exit

if 'KROPOTKIN_URL' not in environ:
    print "Must set environment variable KROPOTKIN_URL"
    exit(1)

if not create_factspace('whooshingby'):
    print "Failed to create whooshingby factspace"
    exit(2)

for root, dirs, files in walk('components'):
    for d in dirs:
        content = {'directory': abspath(join(root, d))}
        store_fact('kropotkin', 'component_available', content)
