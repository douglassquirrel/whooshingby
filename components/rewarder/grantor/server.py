#!/usr/bin/python
from httplib import BadStatusLine
from httplib2 import Http
from json import loads
from kropotkin import get_newest_fact, store_fact
from os import environ
from random import randrange
from time import sleep, time

def find_service(service_name):
    fact = get_newest_fact(FACT_URL, 'service-started', {'name': service_name})
    if fact:
        return 'http://localhost:%d' % fact['port']
    raise Exception("Cannot locate service %s" % service_name)

FACT_URL = environ['KROPOTKIN_URL'] # wrong - should use own factspace
REWARDS_URL = find_service('rewards')

store_fact(FACT_URL, 'service-started', {'name':'grantor'})

completed_tasks = 0
while True:
    sleep(1)
    resp, content = Http().request(FACT_URL + '/completed-task')
    if resp.status != 200:
        raise Exception('Unable to check facts service')
    facts = loads(content)
    if len(facts) > completed_tasks:
        completed_tasks = len(facts)
        resp, rewards_json = Http().request(REWARDS_URL)
        if resp.status != 200:
            raise Exception('Unable to get rewards')

        r = randrange(100)
        n = 0
        for reward in loads(rewards_json):
            if r in range(n, n + reward['percentage']):
                content = {'name': reward['name'], 'time': int(time())}
                store_fact(FACT_URL, 'reward', content)
            n = n + reward['percentage']
