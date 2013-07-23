#!/usr/bin/python
from json import loads, dumps
from kropotkin import get_newest_fact, get_next_set, store_fact, subscribe_sets
from random import randrange
from time import sleep

def choose(random_value, percentages, default=None):
    n = 0
    for name, percentage in percentages:
        if random_value in range(n, n + percentage):
            return name
        else:
            n = n + percentage
    return default

def compare_opinions(opinions, expected_opinions):
    if len(opinions) < expected_opinions:
        return False
    names = set([opinion['name'] for opinion in opinions])
    return len(names) == 1

def classify_opinion(opinion):
    return opinion['task_id']

subscribe_sets('whooshingby', 'opinion', 'reward', classify_opinion, 2, 1)
while True:
    opinions = get_next_set('whooshingby', 'opinion', 'reward')

    if not compare_opinions(opinions, 2):
        if not store_fact('whooshingby', 'opinion_difference',
                          {'opinions': dumps(opinions)}):
            print "Could not store opinion difference fact"

    percentages_fact = get_newest_fact('whooshingby', 'judge_percentages', {})
    percentages = loads(percentages_fact['percentages'])
    random_value = randrange(100)
    source = choose(random_value, percentages, default='python')

    to_promote = next((o for o in opinions if o['source'] == source), None)
    if to_promote:
        for key in to_promote.keys():
            if key.startswith('kropotkin_'):
                del to_promote[key]
        if not store_fact('whooshingby', 'reward', to_promote):
            print "Could not store reward fact"
