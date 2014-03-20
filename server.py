#!/usr/bin/env python
"""
Main server file.
"""
import random
import socket
from urlparse import urlparse
from urlparse import parse_qs
import cgi
from StringIO import StringIO
from app import make_app

# quixote stuff which is not in use right now
# import quixote
# from quixote.demo import create_publisher
# from quixote.demo.mini_demo import create_publisher
# from quixote.demo.altdemo import create_publisher


CRLF = "\r\n"

def main():
    "Starts up the server and waits for connections"

    # Create a socket object
    sock = socket.socket()
    # Get local machine name
    host = socket.getfqdn()
    if host in ('magrathea', 'Thoth'):
        # For testing, I don't want to have to change my url all the damn time.
        port = 8080
    else:
        port = random.randint(8000, 9999)
    # Bind to the port
    sock.bind((host, port))
    print 'Starting server at http://%s:%d/' % (host, port)
    # Now wait for client connection.
    sock.listen(5)

    wsgi_app = make_app()
    # quixote stuff for testing with that
    # publisher.is_thread_safe = True # hack...
    # p = create_publisher()
    # wsgi_app = quixote.get_wsgi_app()

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        conn, (client_host, client_port) = sock.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(conn, wsgi_app)

def handle_connection(conn, wsgi_app):
    "Handles a given connection by sending the proper response"

    # Then get the request data and parse it.
    request = read_request(conn)

    def start_response(status, response_headers):
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
        'wsgi.input': (a StringIO wrap of the raw content data)
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
        content = conn.recv(int(headers['content-length']))
        if 'content-type' in headers:
            if 'application/x-www-form-urlencoded' in headers['content-type']:
                # form encoding's easy: just parse the query string...
                temp = parse_qs(content)
                _input = StringIO(content)
                # ... and store in my dictionary.
                content = {
                    key.lower(): temp[key][0]
                    for key in temp
                }
            elif 'multipart/form-data' in headers['content-type']:
                # Multipart's a bit trickier: going cgi on this one.
                # Init the field storage...
                _input = StringIO(content)
                temp = cgi.FieldStorage(
                    headers=headers, fp=_input,
                    environ={'REQUEST_METHOD' : 'POST'}
                )
                # ... reset content to a dictionary...
                content = {}
                # ... and then parse all keys, values into content.
                for key in temp:
                    content[key.lower()] = temp[key].value
            else:
                # TODO do something with other types
                # reset content to a dictionary
                content = {}
        else:
            # TODO is there a default content-type, assuming length is given?
            content = {}
    elif 'content-type' in headers:
        # in this case, I may have a complicated situation wherein
        # I need to actually determine the length manually.
        # TODO manual length determination, if possible.
        content = {}
    else:
        # empty content
        content = {}

    # Now to put it all together in one request object:
    request = {
        'REQUEST_METHOD': request_line['method'],
        'SCRIPT_NAME': '',
        'PATH_INFO': request_line['uri'],
        'QUERY_STRING': request_line['query_string'],
        'query': request_line['query'],
        'SERVER_PROTOCOL': request_line['protocol'],
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
