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
print "Listening on port %d" % PORT

with open('skeleton.htmlfragment') as f: SKELETON = f.read()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Cache-Control',  'max-age=%d' % CACHE_MAX_AGE)
        self.send_header('Content-Length', len(SKELETON))
        self.send_header('Content-Type',   'text/html')
        self.end_headers()
        self.wfile.write(SKELETON)
        return

content = dumps({'name':'task-submit-html-skeleton', 'port':PORT})
Http().request(FACT_URL + "/service-started", "POST", content, headers={'content-type':'application/x-www-form-urlencoded'})

server = HTTPServer(('', PORT), handler)
server.serve_forever()

    
