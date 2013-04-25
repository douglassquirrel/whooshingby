#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from httplib2 import Http
from kropotkin import get_newest_fact
from multiprocessing import Process
from os import environ
from SocketServer import ThreadingMixIn
from time import time
from urlparse import urlparse

FACT_URL = environ['KROPOTKIN_URL'] # wrong - should use own factspace
PORT = 2013
ROUTES = {'/'                 : 'home.html', \
          '/completed_task.js': 'completed_task.js', \
          '/display_reward.js': 'display_reward.js'}
MIME_TYPES = {'html': 'text/html',
              'js'  : 'application/javascript'}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        try:
            name = ROUTES[path]
            with open(name, 'r') as f:
                content = f.read()
            mime_type = MIME_TYPES[name.split('.')[-1]]
            if mime_type == 'application/javascript':
                content = "var FACT_URL = '%s';\n%s" % (FACT_URL, content)
            self.give_response(200, content, mime_type)
        except KeyError:
            self.give_response(404, 'No such file %s\n' % path)

    def log_message(self, format, *args):
        return

    def give_response(self, resp_code, text, mime_type='text/plain'):
        self.send_response(resp_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(text))
        self.send_header('Content-Type', mime_type + '; charset=utf-8')
        self.end_headers()
        if text:
            self.wfile.write(text)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass
server = ThreadedHTTPServer(('', PORT), handler)
server.serve_forever()
