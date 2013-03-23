#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import environ
from sys import exit
from httplib2 import Http
from urllib import urlencode
from json import dumps

CACHE_MAX_AGE = environ.get('CACHE_MAX_AGE')
PORT          = int(environ.get('PORT') or None)
FACT_URL      = environ.get('FACT_URL')
if CACHE_MAX_AGE is None or PORT is None:
    content = dumps({'name':'task-submit-html-skeleton', 'reason':'missing environment variables'})
    request_body = urlencode({'type':'service-failed-to-start', 'content':content})
    Http().request(FACT_URL, "POST", request_body, headers={'content-type':'application/x-www-form-urlencoded'})
if CACHE_MAX_AGE is None or PORT is None or FACT_URL is None:    
    print "Need to set CACHE_MAX_AGE, PORT and FACT_URL environment variables"
    exit(1)
with open('skeleton.htmlfragment') as f: SKELETON = f.read()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Cache-Control',  'max-age=' + CACHE_MAX_AGE)
        self.send_header('Content-Length', len(SKELETON))
        self.send_header('Content-Type',   'text/html')
        self.end_headers()
        self.wfile.write(SKELETON)
        return

content = dumps({'name':'task-submit-html-skeleton', 'port':PORT})
request_body = urlencode({'type':'service-started', 'content':content})
Http().request(FACT_URL, "POST", request_body, headers={'content-type':'application/x-www-form-urlencoded'})

server = HTTPServer(('', PORT), handler)
server.serve_forever()

    
