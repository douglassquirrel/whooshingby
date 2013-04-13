#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from httplib import BadStatusLine
from httplib2 import Http
from json import dumps
from kropotkin import store_fact
from os import environ
from random import randrange
from urllib import urlencode

CACHE_MAX_AGE = 5

FACT_URL      = environ['KROPOTKIN_URL'] # wrong - should use own factspace
print "Using facts service at %s" % FACT_URL

PORT = randrange(2000, 3000)
print "task-submit-html-skeleton listening on port %d" % PORT

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

    def log_message(self, format, *args):
        return

content = dumps({'name':'task-submit-html-skeleton', 'port':PORT})
store_fact(FACT_URL, 'service-started', content)

server = HTTPServer(('', PORT), handler)
server.serve_forever()
