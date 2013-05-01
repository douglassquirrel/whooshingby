#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from httplib import BadStatusLine
from httplib2 import Http
from kropotkin import store_fact
from random import randrange
from urllib import urlencode

CACHE_MAX_AGE = 5

PORT = randrange(2000, 3000)
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

    def log_message(self, format, *args):
        return

store_fact('whooshingby', 'service-started', {'name':'rewards', 'port':PORT})

server = HTTPServer(('', PORT), handler)
server.serve_forever()
