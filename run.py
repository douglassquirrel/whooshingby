#!/usr/bin/python
from kropotkin import store_fact
from json import dumps
from os import environ
from os.path import abspath
from time import time

KROPOTKIN_URL = environ['KROPOTKIN_URL']

content = dumps({'time': int(time()), 'directory': abspath('components')})
store_fact(KROPOTKIN_URL, 'start-component', content)
