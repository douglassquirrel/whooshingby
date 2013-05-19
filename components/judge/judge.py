#!/usr/bin/python
from kropotkin import get_newest_fact, make_query_function, \
                      store_fact, store_opinion
from random import randrange
from time import sleep

get_oldest_opinion_and_stamp = make_query_function('opinion', True, 'oldest')
get_all_opinions_and_stamp = make_query_function('opinion', True, 'all')

def choose(random_value, percentages, default=None):
    n = 0
    for name, percentage in percentages:
        if random_value in range(n, n + percentage):
            return name
        else:
            n = n + percentage
    return default

while True:
    opinion = get_oldest_opinion_and_stamp('whooshingby', 'reward',
                                           {}, 'judge')
    if not opinion:
        continue

    sleep(1) # wait for all components to finish; could be much improved

    task_id = opinion['task_id']
    opinions = [opinion] + \
        get_all_opinions_and_stamp('whooshingby', 'reward',
                                   {'task_id': task_id}, 'judge')

    percentages = get_newest_fact('whooshingby',
                                  'judge_percentages', {})['percentages']
    random_value = randrange(100)
    source = choose(random_value, percentages, default='python')

    to_promote = next((o for o in opinions if o['source'] == source), None)
    if to_promote:
        if not store_fact('whooshingby', 'reward', to_promote):
            print "Could not store fact"
