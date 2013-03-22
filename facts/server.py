#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart, parse_qs
from json import dumps
from os import environ, path
from sys import exit
from time import time

PORT           = int(environ.get('PORT') or None)
FACTS_LOCATION = environ.get('FACTS_LOCATION')
if PORT is None or FACTS_LOCATION is None:
    print "Need to set PORT and FACTS_LOCATION environment variables"
    exit(1)

def save_fact(fact_type, content):
    tstamp = int(time())
    name = '.'.join([fact_type, str(tstamp), 'fact'])
    with open(path.join(FACTS_LOCATION, name), 'w') as fact_file:
        fact_file.write(content)
    
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        
        fact_type = (postvars.get('type')    or [None])[0]
        content   = (postvars.get('content') or [None])[0]
        if fact_type and content:
            save_fact(fact_type, content)
            response_code = 200
        else:
            response_code = 400
        
        self.send_response(response_code)
        self.send_header('Content-Length', 0)
        self.send_header('Content-Type',   'text/plain')
        self.end_headers()
        return

save_fact('service-started', dumps({'name':'facts', 'port':PORT}))
server = HTTPServer(('', PORT), handler)
server.serve_forever()
