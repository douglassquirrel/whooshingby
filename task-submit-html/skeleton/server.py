#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import environ
from sys import exit

CACHE_MAX_AGE = environ.get('CACHE_MAX_AGE')
PORT          = int(environ.get('PORT') or None)
if CACHE_MAX_AGE is None or PORT is None:
    # Failed to start fact
    print "Need to set both CACHE_MAX_AGE and PORT environment variables"
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

# Start fact
server = HTTPServer(('', PORT), handler)
server.serve_forever()

    
