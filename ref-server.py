#!/usr/bin/env python

"""
Allows me to make applications run using the reference wsgi server
"""
import socket
import random
import argparse

from wsgiref.simple_server import make_server

import app

import quixote
from quixote.demo import create_publisher
from quixote.demo.mini_demo import create_publisher
from quixote.demo.altdemo import create_publisher
import imageapp

from quotes import QuotesApp
from chat import ChatApp
import cookieapp

###

apps = [
    'fires', 'hw6',
    'imageapp',
    'quixote_demo',
    'quotes',
    'chat',
    'cookie'
]
parser = argparse.ArgumentParser(
    description='A reference wsgi server.',
    formatter_class=argparse.RawTextHelpFormatter
)
# Add the '-?' alias for '--help', which I prefer to use:
parser.add_argument('-?',
    action='help',
    help='Alias for --help')
# Add the application argument:
parser.add_argument('--app',
    nargs='?',
    dest='app',
    default='fires',
    choices=apps,
    help='\n'.join([
        'Which WSGI application to run.',
        '(default: "%(default)s" - my homework 6)',
        'Alias: -A'
        ]))
parser.add_argument('-A',
    nargs='?',
    dest='app',
    default='fires',
    choices=apps,
    help=argparse.SUPPRESS)
# Add the port argument:
parser.add_argument('--port',
    nargs='?',
    default=random.randint(8000, 9999),
    type=int,
    help='\n'.join([
        'Which port to start the server on.',
        '(default: random integer between 8000 and 9999)',
        'Alias: -p'
        ]))
# After that, parse the command-line arguments.
args = parser.parse_args()

app_to_run = args.app
if app_to_run == 'quixote_demo':
    # quixote stuff for testing with that
    p = create_publisher()
    # p.is_thread_safe = True # hack...
    wsgi_app = quixote.get_wsgi_app()
elif app_to_run == 'imageapp':
    imageapp.setup()
    p = imageapp.create_publisher()
    wsgi_app = quixote.get_wsgi_app()
elif app_to_run == 'quotes':
    wsgi_app = QuotesApp('./quotes/quotes.txt', './quotes/html')
elif app_to_run == 'chat':
    wsgi_app = ChatApp('./chat/html')
elif app_to_run == 'cookie':
    wsgi_app = cookieapp.wsgi_app
else: #if app_to_run == 'fires': # default
    wsgi_app = app.make_app()

# get hostname and port number
host = socket.getfqdn()
if host in ('magrathea', 'Thoth'):
    # For testing, I don't want to have to change my url all the damn time.
    port = 8080
else:
    port = args.port

httpd = make_server('', port, wsgi_app)
print "Serving at http://%s:%d/..." % (host, port,)
httpd.serve_forever()
