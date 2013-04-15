#!/usr/bin/python
from kropotkin import store_fact
from json import dumps
from os import environ
from os.path import abspath
from sys import exit
from time import time

try:
    KROPOTKIN_URL = environ['KROPOTKIN_URL']
except KeyError:
    print "Must set environment variable KROPOTKIN_URL"
    exit(1)

content = dumps({'time': int(time()), 'directory': abspath('components')})
store_fact(KROPOTKIN_URL, 'deploy', content)
