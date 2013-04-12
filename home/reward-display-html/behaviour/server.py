#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from httplib import BadStatusLine
from httplib2 import Http
from json import dumps
from kropotkin import store_fact
from random import randrange

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

def add_js_var(name, value, javascript):
    return "var %s = '%s';\n%s" % (name, value, javascript)

CACHE_MAX_AGE = 5

FACT_URL      = find_facts_service()
print "Using facts service at %s" % FACT_URL

PORT = randrange(2000, 3000)
print "reward-display-html-behaviour listening on port %d" % PORT

with open('display_reward.js') as f: BEHAVIOUR = f.read()
BEHAVIOUR = add_js_var("FACT_URL", FACT_URL, BEHAVIOUR)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Cache-Control',  'max-age=%d' % CACHE_MAX_AGE)
        self.send_header('Content-Length', len(BEHAVIOUR))
        self.send_header('Content-Type',   'text/html')
        self.end_headers()
        self.wfile.write(BEHAVIOUR)
        return

    def log_message(self, format, *args):
        return

content = dumps({'name':'reward-display-html-behaviour', 'port':PORT})
store_fact(FACT_URL, 'service-started', content)

server = HTTPServer(('', PORT), handler)
server.serve_forever()
