#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from httplib import BadStatusLine
from httplib2 import Http
from json import loads
from kropotkin import store_fact
from os import environ
from random import randrange
from urllib import urlencode

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

FACT_URL = environ['KROPOTKIN_URL'] # wrong - should use own factspace
print 'Using facts service at %s' % FACT_URL

PORT = randrange(2000, 3000)
print 'reward-display-html listening on port %d' % PORT

SKELETON_URL  = find_service('reward-display-html-skeleton')
BEHAVIOUR_URL = find_service('reward-display-html-behaviour')
print 'Skeleton URL: %s; behaviour URL: %s' % (SKELETON_URL, BEHAVIOUR_URL)

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

content = {'name':'reward-display-html', 'port':PORT}
store_fact(FACT_URL, 'service-started', content)

server = HTTPServer(('', PORT), handler)
server.serve_forever()
