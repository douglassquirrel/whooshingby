#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from glob import glob
from json import dumps, load
from os import path
from random import randrange
from tempfile import mkdtemp
from time import time
from urlparse import urlparse, parse_qsl

PORT = randrange(2000, 3000)
print "Listening on port %d" % PORT

FACTS_LOCATION = mkdtemp()
print "Storing facts in %s" % FACTS_LOCATION

def save_fact(fact_type, content):
    tstamp = int(time())
    name = '.'.join([fact_type, str(tstamp), str(hash(content)), 'fact'])
    with open(path.join(FACTS_LOCATION, name), 'w') as fact_file:
        fact_file.write(content)

def load_fact(fact_filename):
    with open(fact_filename, 'r') as fact_file:
        return load(fact_file)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        url_path = parsed_url.path
        query_params = set(parse_qsl(parsed_url.query))

        if url_path == '/':
            self.give_response(200, 'Kropotkin Facts Service\n')
        else:
            fact_type = url_path.split('/')[1]
            fact_files = glob(path.join(FACTS_LOCATION, fact_type + ".*"))
            facts = [load_fact(f) for f in fact_files]
            facts = [f for f in facts if query_params < set(f.viewitems())]
            self.give_response(200, dumps(facts), 'application/json')

    def do_POST(self):
        fact_type = (urlparse(self.path).path)[1:]
        length = int(self.headers.getheader('Content-Length'))
        content = self.rfile.read(length)

        if fact_type and content:
            save_fact(fact_type, content)
            self.give_response(200, '')
        else:
            self.give_response(400, '')

    def log_message(self, format, *args):
        return

    def give_response(self, response_code, text, mime_type='text/plain'):
        self.send_response(response_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(text))
        self.send_header('Content-Type', mime_type + '; charset=utf-8')
        self.end_headers()
        if text:
            self.wfile.write(text)

save_fact('service-started', dumps({'name':'facts', 'port':PORT}))
server = HTTPServer(('', PORT), handler)
server.serve_forever()
