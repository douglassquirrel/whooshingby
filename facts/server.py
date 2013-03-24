#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from json import dumps
from os import path
from random import randrange
from tempfile import mkdtemp
from time import time
from urlparse import urlparse

PORT = randrange(2000, 3000)
print "Listening on port %d" % PORT

FACTS_LOCATION = mkdtemp()
print "Storing facts in %s" % FACTS_LOCATION

def save_fact(fact_type, content):
    tstamp = int(time())
    name = '.'.join([fact_type, str(tstamp), str(hash(content)), 'fact'])
    with open(path.join(FACTS_LOCATION, name), 'w') as fact_file:
        fact_file.write(content)
    
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_path = urlparse(self.path).path
        if url_path == '/':
            self.text_response(200, 'Kropotkin Facts Service\n')
        else:
            self.text_response(400, '')

    def do_POST(self):
        fact_type = (urlparse(self.path).path)[1:]
        length = int(self.headers.getheader('Content-Length'))
        content = self.rfile.read(length)

        if fact_type and content:
            save_fact(fact_type, content)
            self.text_response(200, '')
        else:
            self.text_response(400, '')
  
    def text_response(self, response_code, text):
        self.send_response(response_code)
        self.send_header('Content-Length', len(text))
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        if text:
            self.wfile.write(text)

save_fact('service-started', dumps({'name':'facts', 'port':PORT}))
server = HTTPServer(('', PORT), handler)
server.serve_forever()
