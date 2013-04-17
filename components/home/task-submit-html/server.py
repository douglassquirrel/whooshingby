#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from httplib import BadStatusLine
from httplib2 import Http
from json import loads
from kropotkin import get_newest_fact, store_fact
from os import environ
from random import randrange
from urllib import urlencode

def find_service(service_name):
    fact = get_newest_fact(FACT_URL, 'service-started', {'name': service_name})
    if fact:
        return 'http://localhost:%d' % fact['port']
    raise Exception("Cannot locate service %s" % service_name)

CACHE_MAX_AGE = 5

FACT_URL      = environ['KROPOTKIN_URL'] # wrong - should use own factspace
PORT = randrange(2000, 3000)

SKELETON_URL  = find_service('task-submit-html-skeleton')
BEHAVIOUR_URL = find_service('task-submit-html-behaviour')

SCRIPT_TEMPLATE = '<script type="text/javascript">\n%s\n</script>\n'

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        resp, skeleton  = Http().request(SKELETON_URL)
        resp, behaviour = Http().request(BEHAVIOUR_URL)

        fragment = SCRIPT_TEMPLATE % behaviour + skeleton

        self.send_response(200)
        self.send_header('Cache-Control',  'max-age=%d' % CACHE_MAX_AGE)
        self.send_header('Content-Length', len(fragment))
        self.send_header('Content-Type',   'text/html')
        self.end_headers()
        self.wfile.write(fragment)
        return

    def log_message(self, format, *args):
        return

content = {'name':'task-submit-html', 'port':PORT}
store_fact(FACT_URL, 'service-started', content)

server = HTTPServer(('', PORT), handler)
server.serve_forever()
