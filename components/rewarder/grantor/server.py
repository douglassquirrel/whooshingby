#!/usr/bin/python
from httplib import BadStatusLine
from httplib2 import Http
from json import loads
from kropotkin import store_fact
from os import environ
from random import randrange
from time import sleep, time

def find_service(service_name):
    for i in range(10000):
        url = '%s/service-started?name=%s' % (FACT_URL, service_name)
        try:
            resp, content = Http().request(url)
            if resp.status == 200:
                facts = loads(content)
                if len(facts) > 0:
                    return 'http://localhost:%d' % loads(content)[0]['port']
        except IOError:
            pass
    raise Exception('Cannot locate %s' % service_name)

FACT_URL = environ['KROPOTKIN_URL'] # wrong - should use own factspace
print 'Using facts service at %s' % FACT_URL

REWARDS_URL = find_service('rewards')
print 'Rewards URL: %s' % REWARDS_URL

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
