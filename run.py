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
             'keys': ['name', 'time', 'kropotkin_id'],
             'translation': 'Task %(name)s reported at %(time)s'},
            {'type': 'reward',
             'keys': ['name', 'task_id', 'source'],
             'translation': 'Reward %(name)s for %(task_id)s by %(source)s'},
            {'type': 'reward_percentages',
             'keys': ['percentages'],
             'translation': 'Reward percentages set to %(percentages)s'},
            {'type': 'judge_percentages',
             'keys': ['percentages'],
             'translation': 'Judge percentages set to %(percentages)s'},
            {'type': 'opinion_difference',
             'keys': ['opinions'],
             'translation': 'Opinions differ: %(opinions)s'}]

for e in elements:
    if not store_fact('whooshingby', 'constitution_element', e):
        print "Could not store constitution element fact"
        exit(1)

with open('rewards.json') as f:
    rewards = load(f)
    if not store_fact('whooshingby', 'reward_percentages',
                      {'percentages': rewards}):
        print "Could not store reward percentages"
        exit(1)

if not store_fact('whooshingby', 'judge_percentages',
                  {'percentages': [['python', 100], ['ruby', 0]]}):
        print "Could not store judge percentages"
        exit(1)

for f in listdir('components'):
    content = {'location': abspath(join('components', f))}
    if not store_fact('kropotkin', 'component_available', content):
        print "Could not store component available fact"
        exit(1)
