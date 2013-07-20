#!/usr/bin/python
from json import loads
from kropotkin import get_newest_fact, get_next_fact, store_opinion, subscribe
from time import time

def choose(random_value, percentages, default=None):
    n = 0
    for name, percentage in percentages:
        if random_value in range(n, n + percentage):
            return name
        else:
            n = n + percentage
    return default

def _now():
    return int(round(time()))

subscribe('whooshingby', 'fact', 'completed_task')
while True:
    fact = get_next_fact('whooshingby', 'completed_task')
    if not fact:
        continue

    percentages_fact = get_newest_fact('whooshingby', 'reward_percentages', {})
    reward_percentages = loads(percentages_fact['percentages'])

    random_value = (hash(fact['name']) * 61 + fact['time'] * 47) % 100
    name = choose(random_value, reward_percentages)
    if name:
        content = {'name': name, 'task_id': fact['task_id'],
                   'source': 'python', 'time': _now()}
        if not store_opinion('whooshingby', 'reward', content):
            print "Could not store reward opinion" # handle better
