#!/usr/bin/python
from httplib import BadStatusLine
from httplib2 import Http
from json import loads
from kropotkin import get_newest_fact, get_oldest_fact_and_stamp, store_fact
from os import getpid
from random import randrange
from time import sleep, time

def find_service(service_name):
    fact = get_newest_fact('kropotkin', 'service-started',
                           {'name': service_name})
    if fact:
        return 'http://localhost:%d' % fact['port']
    raise Exception("Cannot locate service %s" % service_name)

REWARDS_URL = find_service('rewards')
STAMP = 'grantor.%d' % getpid()

store_fact('kropotkin', 'service-started', {'name':'grantor'})

while True:
    fact = get_oldest_fact_and_stamp('kropotkin', 'completed-task', {}, STAMP)
    if fact:
        resp, rewards_json = Http().request(REWARDS_URL)
        if resp.status != 200:
            raise Exception('Unable to get rewards')

        r = randrange(100)
        n = 0
        for reward in loads(rewards_json):
            if r in range(n, n + reward['percentage']):
                content = {'name': reward['name'], 'time': int(time())}
                store_fact('kropotkin', 'reward', content)
            n = n + reward['percentage']
