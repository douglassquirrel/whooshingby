#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from httplib2 import Http
from json import dumps
from random import randrange
from urllib import urlencode

def find_facts_service():
    for port in range(2000, 3000):
        url = 'http://localhost:%d' % port
        try:
            resp, content = Http().request(url)
            if resp.status == 200 and 'Kropotkin' in content:
                return url
        except IOError:
            pass
    raise Exception('Cannot locate facts service')

CACHE_MAX_AGE = 5

FACT_URL      = find_facts_service()
print "Using facts service at %s" % FACT_URL

PORT = randrange(2000, 3000)
print "rewards listening on port %d" % PORT

with open('rewards.json') as f: REWARDS = f.read()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Cache-Control',  'max-age=%d' % CACHE_MAX_AGE)
        self.send_header('Content-Length', len(REWARDS))
        self.send_header('Content-Type',   'application/json')
        self.end_headers()
        self.wfile.write(REWARDS)
        return

url = FACT_URL + '/service-started'
content = dumps({'name':'rewards', 'port':PORT})
headers = {'content-type':'application/x-www-form-urlencoded'}
Http().request(url, "POST", content, headers)

server = HTTPServer(('', PORT), handler)
server.serve_forever()
