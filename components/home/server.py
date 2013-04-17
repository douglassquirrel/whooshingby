#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from httplib import BadStatusLine
from httplib2 import Http
from kropotkin import store_fact, get_newest_fact
from random import randrange
from re import sub
from os import environ

def find_service(service_name):
    fact = get_newest_fact(FACT_URL, 'service-started', {'name': service_name})
    if fact:
        return 'http://localhost:%d' % fact['port']
    raise Exception("Cannot locate service %s" % service_name)

CACHE_MAX_AGE = 5

FACT_URL = environ['KROPOTKIN_URL'] # wrong - should use own factspace

PORT = randrange(2000, 3000)
print 'home listening on port %d' % PORT

TASK_SUBMIT_HTML_URL = find_service('task-submit-html')
REWARD_DISPLAY_HTML_URL = find_service('reward-display-html')

with open('home.html') as f: HOME_HTML = f.read()

TASK_SUBMIT_RE = '<section\s*data-task-submit>\s*</section>'
REWARD_DISPLAY_RE = '<section\s*data-reward-display>\s*</section>'

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        resp, task_submit_section =    Http().request(TASK_SUBMIT_HTML_URL)
        resp, reward_display_section = Http().request(REWARD_DISPLAY_HTML_URL)

        html = sub(TASK_SUBMIT_RE,    task_submit_section,    HOME_HTML)
        html = sub(REWARD_DISPLAY_RE, reward_display_section, html)

        self.send_response(200)
        self.send_header('Cache-Control',  'max-age=%d' % CACHE_MAX_AGE)
        self.send_header('Content-Length', len(html))
        self.send_header('Content-Type',   'text/html')
        self.end_headers()
        self.wfile.write(html)
        return

    def log_message(self, format, *args):
        return

store_fact(FACT_URL, 'service-started', {'name':'home', 'port':PORT})

server = HTTPServer(('', PORT), handler)
server.serve_forever()
