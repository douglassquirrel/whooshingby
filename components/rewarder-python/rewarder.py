#!/usr/bin/python
from kropotkin import get_all_facts, get_oldest_fact_and_stamp, store_opinion

while True:
    fact = get_oldest_fact_and_stamp('whooshingby', 'completed-task',
                                     {}, 'rewarder_python')
    if not fact:
        continue

    reward_percentages = get_all_facts('whooshingby',
                                       'reward_percentage',
                                       {})

    r = (hash(fact['name']) * 61 + fact['time'] * 47) % 100
    n = 0
    for reward in reward_percentages:
        if r not in range(n, n + reward['percentage']):
            n = n + reward['percentage']
            continue
        content = {'name': reward['name'], 'task_id': fact['kropotkin_id'],
                   'source': 'python'}
        if not store_opinion('whooshingby', 'reward', content):
            print "Could not store reward opinion" # handle better
        break
