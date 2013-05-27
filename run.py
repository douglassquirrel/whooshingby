#!/usr/bin/python
from json import load
from kropotkin import create_factspace, store_fact
from os import environ, listdir
from os.path import abspath, join
from sys import exit, stderr

def fail_and_exit(message):
    stderr.write(message + '\n')
    exit(1)

if 'KROPOTKIN_URL' not in environ:
    fail_and_exit("Must set environment variable KROPOTKIN_URL")

if not create_factspace('whooshingby'):
    fail_and_exit("Failed to create whooshingby factspace")

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
        fail_and_exit("Could not store constitution element fact")

with open('rewards.json') as f:
    rewards = load(f)
    if not store_fact('whooshingby', 'reward_percentages',
                      {'percentages': rewards}):
        fail_and_exit("Could not store reward percentages")

if not store_fact('whooshingby', 'judge_percentages',
                  {'percentages': [['python', 100], ['ruby', 0]]}):
        fail_and_exit("Could not store judge percentages")

for f in listdir('components'):
    content = {'location': abspath(join('components', f))}
    if not store_fact('kropotkin', 'component_available', content):
        fail_and_exit("Could not store component available fact")

home_url = '/'.join([environ['KROPOTKIN_URL'], 'component', 'home.html'])
print "Whooshingby available on %s" % home_url
