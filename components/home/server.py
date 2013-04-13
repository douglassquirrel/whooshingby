#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from httplib import BadStatusLine
from httplib2 import Http
from json import dumps, loads
from kropotkin import store_fact
from random import randrange
from re import sub

def find_facts_service():
    for port in range(2000, 3000):
        url = 'http://localhost:%d' % port
        try:
            resp, content = Http().request(url)
            if resp.status == 200 and 'Kropotkin' in content:
                return url
        except IOError:
            pass
        except BadStatusLine:
            pass
    raise Exception('Cannot locate facts service')

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

CACHE_MAX_AGE = 5

FACT_URL      = find_facts_service()
print 'Using facts service at %s' % FACT_URL

PORT = randrange(2000, 3000)
print 'home listening on port %d' % PORT

TASK_SUBMIT_HTML_URL = find_service('task-submit-html')
print 'task-submit-html URL: %s' % TASK_SUBMIT_HTML_URL

REWARD_DISPLAY_HTML_URL = find_service('reward-display-html')
print 'reward-display-html URL: %s' % REWARD_DISPLAY_HTML_URL

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

store_fact(FACT_URL, 'service-started', dumps({'name':'home', 'port':PORT}))

server = HTTPServer(('', PORT), handler)
server.serve_forever()
