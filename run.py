#!/usr/bin/python
from json import load
from kropotkin import create_factspace, store_fact
from os import environ, listdir
from os.path import abspath, join
from sys import exit

if 'KROPOTKIN_URL' not in environ:
    print "Must set environment variable KROPOTKIN_URL"
    exit(1)

if not create_factspace('whooshingby'):
    print "Failed to create whooshingby factspace"
    exit(2)

elements = [{'type': 'completed-task',
             'keys': ['name', 'time'],
             'translation': 'Task %(name)s reported at %(time)s'},
            {'type': 'reward',
             'keys': ['name', 'time'],
             'translation': 'Reward %(name)s granted at %(time)s'},
            {'type': 'reward_percentage',
             'keys': ['name', 'percentage'],
             'translation': 'Reward %(name)s given percentage %(percentage)s'}]

for e in elements:
    if not store_fact('whooshingby', 'constitution_element', e):
        print "Could not store constitution element fact"
        exit(1)

with open('rewards.json') as f:
    rewards = load(f)
for reward in rewards:
    if not store_fact('whooshingby', 'reward_percentage', reward):
        print "Could not store reward percentage"
        exit(1)

for f in listdir('components'):
    content = {'location': abspath(join('components', f))}
    if not store_fact('kropotkin', 'component_available', content):
        print "Could not store component available fact"
        exit(1)
