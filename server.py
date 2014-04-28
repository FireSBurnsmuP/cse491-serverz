#!/usr/bin/env python
"""
Main server file.
"""
import random
import socket
import argparse
from urlparse import urlparse
from urlparse import parse_qs
import cgi
import sys
from StringIO import StringIO

import app
import quixote
from quixote.demo import create_publisher
from quixote.demo.mini_demo import create_publisher
from quixote.demo.altdemo import create_publisher
import imageapp

from quotes import QuotesApp
from chat import ChatApp
import cookieapp

CRLF = "\r\n"

def main():
    """
    Initializes the Server.

    Parses command line arguments (if present),
    then initializes the wsgi_app and starts up the server,
    then waits for connections
    """

    apps = [
        'fires', 'hw6',
        'imageapp',
        'quixote_demo',
        'quotes',
        'chat',
        'cookie'
    ]
    parser = argparse.ArgumentParser(
        description='A WSGI Server implemented for CSE491-001.',
        epilog='Please check the non-existent documentation for more info.',
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

    # Create a socket object
    sock = socket.socket()
    # Get local machine name
    host = socket.getfqdn()

    if host in ('magrathea', 'Thoth'):
        # For testing, I don't want to have to change my url all the damn time.
        port = 8080
    else:
        port = args.port
    # Bind to the port
    # TODO figure out how to immediately unbind when I'm done
    sock.bind((host, port))
    print 'Starting server at http://%s:%d/' % (host, port)
    # Now wait for client connection.
    sock.listen(5)

    # get this from commandline
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


    print 'Entering infinite loop; hit CTRL-C to exit'
    try:
        while True:
            # Establish connection with client.
            conn, (client_host, client_port) = sock.accept()
            print 'Got connection from', client_host, client_port
            handle_connection(conn, wsgi_app)
    finally:
        # teardown stuffs
        if app_to_run == 'imageapp':
            imageapp.teardown()
        sock.shutdown(2)
        sock.close()


def handle_connection(conn, wsgi_app):
    "Handles a given connection by sending the proper response"

    # Then get the request data and parse it.
    request = read_request(conn)
    # print 'parsed request info:'
    # print request['content']

    def start_response(status, response_headers, exc_info=None):
        """
        Starts the response by sending the status line
        Required part of WSGI.
        """
        headers = ''
        for (key, value) in response_headers:
            headers += '{0}: {1}{2}'.format(key, value, CRLF)
        conn.send(CRLF.join([
            'HTTP/1.1 {}'.format(status),
            headers,
            ''
            ])
        )

    result = wsgi_app(request, start_response)
    for data in result:
        conn.send(data)
    conn.close()

def read_request(conn):
    """
    Reads and parses the request sent by the client,
    and returns the resulting request as a dictionary.
    The format of the dictionary will be (mostly) WSGI compliant,
    with the following structure:
    {
        'REQUEST_METHOD': (request method),
        'SCRIPT_NAME': '', (blank)
        'PATH_INFO': (requested uri),
        'QUERY_STRING': (query portion of uri),
        'query': (the query as a dict),
        'CONTENT_TYPE': (content-type of request, if present),
        'CONTENT_LENGTH': (content-length of request, if present),
        'SERVER_PROTOCOL': (protocol, likely 'HTTP/1.x'),
        'SERVER_NAME': 'magrathea'
        'SERVER_PORT': (whatever port we're on),
        'wsgi.input': (a StringIO wrap of the raw content data)
        'wsgi.version': (1, 0) (to signify version 1.0),
        'wsgi.errors': sys.stderr (where to send errors),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'headers': {
            (all headers go in this sub-dictionary, if present,
                otherwise this is empty.)
        },
        'content': {
            (parsed request content goes in here, if it exists,
                otherwise this is empty.)
        }
    }
    I'll provide some pre-parsed stuff for my application,
    like the full headers, parsed content, and parsed query-string,
    but I'll likely switch that to in-app parsing,
    after it's working.
    """

    # Grab the headers from the connection socket
    temp = conn.recv(1)
    while temp[-4:] != CRLF * 2:
        temp += conn.recv(1)
    request = temp.rstrip().split(CRLF)

    # Pull/parse the request line...
    temp = request[0].split()
    request_line = {}
    request_line['method'] = temp[0]
    request_line['uri'] = temp[1]
    request_line['protocol'] = temp[2]
    request_line['query_string'] = urlparse(request_line['uri']).query

    # ... parse the query string into a dict...
    request_line['query'] = {}
    if request_line['query_string']:
        temp = parse_qs(request_line['query_string']).iteritems()
        request_line['query'] = {
            key : val[0]
            for key, val in temp
        }

    # ... and grab headers...
    # For this I must remove the request line
    request = request[1:]
    headers = {}
    for line in request:
        key, value = line.split(': ', 1)
        key = key.lower()
        # now handle duplicate headers
        if key not in headers:
            # if the header isn't already in, add it
            headers[key] = value
        else:
            # it's already in the headers, add it in to previous
            # value delimited by a comma (as per spec)
            headers[key] = ', '.join([headers[key], value])
    # ... and content (if it exists)
    _input = ''
    if 'content-length' in headers:
        content = ''
        while len(content) < int(headers['content-length']):
            content += conn.recv(1)
        # Parse any form data
        if 'content-type' in headers:
            if ('application/x-www-form-urlencoded' in headers['content-type']
                or 'multipart/form-data' in headers['content-type']):
                # Init the field storage...
                _input = StringIO(content)
                temp = cgi.FieldStorage(
                    headers=headers, fp=_input,
                    environ={'REQUEST_METHOD' : 'POST'}
                )
                # ... re-init the input stream
                _input = StringIO(content)
                # ... reset content to a dictionary...
                content = {}
                # ... and then parse all keys, values into content.
                for key in temp:
                    lkey = key.lower()
                    if temp[key].file:
                        # we have a file, so let's store the FieldStorage object
                        content[lkey] = temp[key]
                    else:
                        # we have something else, just store the value (string)
                        content[lkey] = temp[key].value
            else:
                # TODO do something with other types
                # reset content to a dictionary
                content = {}
        else:
            # TODO is there a default content-type, assuming length is given?
            content = {}
    else:
        # empty content
        # WSGI spec says don't process if CONTENT-LENGTH isn't specified
        content = {}

    # Now to put it all together in one request object:
    request = {
        'REQUEST_METHOD': request_line['method'],
        'SCRIPT_NAME': '',
        'PATH_INFO': request_line['uri'],
        'QUERY_STRING': request_line['query_string'],
        'query': request_line['query'],
        'SERVER_PROTOCOL': request_line['protocol'],
        'SERVER_PORT': conn.getsockname()[0],
        'wsgi.version': (1, 0),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'http',
        'CONTENT_TYPE': (
            headers['content-type'] if 'content-type' in headers else ''
        ),
        'CONTENT_LENGTH': (
            headers['content-length'] if 'content-length' in headers else ''
        ),
        'wsgi.input': _input,
        'headers': headers,
        'content': content
    }

    if 'cookie' in headers:
        request['HTTP_COOKIE'] = headers['cookie']
        # TODO think about what to do with Expires, which can contain commas...

    return request

if __name__ == '__main__':
    main()
