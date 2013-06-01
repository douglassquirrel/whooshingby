#!/usr/bin/python
from json import loads
from kropotkin import get_newest_fact, get_oldest_fact_and_stamp, store_opinion

def choose(random_value, percentages, default=None):
    n = 0
    for name, percentage in percentages:
        if random_value in range(n, n + percentage):
            return name
        else:
            n = n + percentage
    return default

while True:
    fact = get_oldest_fact_and_stamp('whooshingby', 'completed_task',
                                     {}, 'rewarder_python')
    if not fact:
        continue

    percentages_fact = get_newest_fact('whooshingby', 'reward_percentages', {})
    reward_percentages = loads(percentages_fact['percentages'])

    random_value = (hash(fact['name']) * 61 + fact['time'] * 47) % 100
    name = choose(random_value, reward_percentages)
    if name:
        content = {'name': name, 'task_id': fact['kropotkin_id'],
                   'source': 'python'}
        if not store_opinion('whooshingby', 'reward', content):
            print "Could not store reward opinion" # handle better
