#!/usr/bin/python
from json import load, dumps
from kropotkin import create_factspace, get_newest_fact, store_fact
from os import environ, listdir
from os.path import abspath, join
from sys import exit, stderr

def fail_and_exit(message):
    stderr.write(message + '\n')
    exit(1)

if 'KROPOTKIN_URL' not in environ:
    fail_and_exit("Must set environment variable KROPOTKIN_URL")

if not create_factspace('whooshingby', environ.get('WHOOSHINGBY_HOME', None)):
    fail_and_exit("Failed to create whooshingby factspace")

elements = [{'type': 'completed_task',
             'keys': dumps(['name', 'time', 'task_id']),
             'translation': 'Task %(name)s reported at %(time)s',
             'options': ''},
            {'type': 'reward',
             'keys': dumps(['name', 'task_id', 'source', 'time']),
             'translation': 'Reward %(name)s for %(task_id)s by %(source)s',
             'options': ''},
            {'type': 'reward_percentages',
             'keys': dumps(['percentages']),
             'translation': 'Reward percentages set to %(percentages)s',
             'options': ''},
            {'type': 'judge_percentages',
             'keys': dumps(['percentages']),
             'translation': 'Judge percentages set to %(percentages)s',
             'options': ''},
            {'type': 'opinion_difference',
             'keys': dumps(['opinions']),
             'translation': 'Opinions differ: %(opinions)s',
             'options': ''},
            {'type': 'subscription',
             'keys': dumps(['type', 'confidence', 'queue']),
             'translation': 'Subscription to %(confidence)ss ' \
                          + 'of type %(type)s using queue %(queue)s',
             'options': ''},
            {'type': 'registration_request',
             'keys': dumps(['name', 'password']),
             'translation': 'User %(name)s requested registration',
             'options': 'memory_only'},
            {'type': 'user',
              'keys': dumps(['name', 'salt', 'hash']),
              'translation': 'User %(name)s is registered',
              'options': ''},
            {'type': 'user_nonce',
             'keys': dumps(['name', 'nonce', 'expiry']),
             'translation': 'User %(name)s can be identified by %(nonce)s' \
                          + 'until %(expiry)s',
             'options': ''}]

for e in elements:
    if not store_fact('whooshingby', 'constitution_element', e):
        fail_and_exit("Could not store constitution element fact")

reward_percentages = get_newest_fact('whooshingby', 'reward_percentages', {})
if not reward_percentages:
    with open('rewards.json') as f:
        reward_percentages = f.read()
        if not store_fact('whooshingby', 'reward_percentages',
                          {'percentages': reward_percentages}):
            fail_and_exit("Could not store reward percentages")

judge_percentages = get_newest_fact('whooshingby', 'judge_percentages', {})
if not judge_percentages:
    if not store_fact('whooshingby', 'judge_percentages',
                      {'percentages': '[["python", 100], ["ruby", 0]]'}):
        fail_and_exit("Could not store judge percentages")

for f in listdir('components'):
    content = {'location': abspath(join('components', f))}
    if not store_fact('kropotkin', 'component_available', content):
        fail_and_exit("Could not store component available fact")

if not store_fact('kropotkin', 'home_component', {'name': 'home.html'}):
    fail_and_exit('Could not store home_component fact')

print "Whooshingby available on %s" % environ['KROPOTKIN_URL']
