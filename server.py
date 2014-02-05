#!/usr/bin/env python
"""
Main server file.
"""
import random
import socket
import time
from urlparse import urlparse
from urlparse import parse_qs


EOL = "\r\n"

def main():
    "Starts up the server and waits for connections"

    # Create a socket object
    sock = socket.socket()
    # Get local machine name
    host = socket.getfqdn()
    port = random.randint(8000, 9999)
    # Bind to the port
    sock.bind((host, port))
    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)
    # Now wait for client connection.
    sock.listen(5)

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        conn, (client_host, client_port) = sock.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(conn)

def handle_connection(conn):
    "Handles a given connection by sending the proper response"

    request = conn.recv(1000)
    # parse the request line
    request = request.splitlines()
    request_line = request[0].split()
    if request_line[0] == 'GET':
        html_response = get(request_line)
    elif request_line[0] == 'POST':
        html_response = post(request_line)
    elif request_line[0] == 'HEAD':
        html_response = head(request_line)
    else:
        # do other stuff
        html_response = 'HTTP/1.1 405 Method Not Allowed{0}{0}'.format(EOL)
    conn.send(html_response)
    conn.close()

def get(request_line):
    "Processes a get request"

    parsed = urlparse(request_line[1])
    path = parsed.path.lower()
    if path in ('/', 'index'):
        html_response = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello, world</h1> this is fires&apos; Web server.',
                    '  <h3>Links:</h3>',
                    '  <div style="padding-left: 1.0em;">',
                    '    <ul>',
                    '      <li><a href="/content">Content</a></li>',
                    '      <li><a href="/file">File</a></li>',
                    '      <li><a href="/image">Image</a></li>',
                    '      <li><a href="/form">Form</a></li>',
                    '    </ul>',
                    '  </div>',
                    '</body>',
                    '</html>'])
    elif path in ('/content'):
        html_response = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello, world</h1> this is the content on fires&apos; Web server.',
                    '</body>',
                    '</html>'])
    elif path in ('/file'):
        html_response = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello, world</h1> this is the file on fires&apos; Web server.',
                    '</body>',
                    '</html>'])
    elif path in ('/image'):
        html_response = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello, world</h1> this is the image on fires&apos; Web server.',
                    '</body>',
                    '</html>'])
    elif path in ('/form'):
        html_response = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello, world</h1> this is the form on fires&apos; Web server.',
                    '  <form action="/submit" method="GET">',
                    '    <input type="text" name="firstname" placeholder="First Name" required />',
                    '    <input type="text" name="lastname" placeholder="Last Name" required /><br />',
                    '    <input type="submit" value="Submit" />',
                    '  </form>',
                    '</body>',
                    '</html>'])
    elif path in ('/submit'):
        # Okay, now to parse out the form variables
        query = parse_qs(parsed.query)
        html_response = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello Mr. {} {}.</h1>'.format(query["firstname"][0],
                        query["lastname"][0]),
                    '</body>',
                    '</html>'])
    else:
        html_response = 'HTTP/1.1 404 Not Found{0}{0}'.format(EOL)
    return html_response;

def post(request_line):
    "processes a POST request"
    # TODO finish adding post capabilities
    html_response = EOL.join(['HTTP/1.1 200 OK',
                'Content-Type: text/html',
                '',
                '<!DOCTYPE html>',
                '<html>',
                '<body>',
                '  <h1>Hello, world</h1> you&apos;ve attempted to POST to fires&apos; Web server.',
                '</body>',
                '</html>'])
    return html_response

def head(request_line):
    "processes a HEAD request"

    parsed = urlparse(request_line[1])
    path = parsed.path.lower()
    if path in ('/', '/index', '/file', '/content', '/image', '/submit', '/form'):
        html_response = 'HTTP/1.1 200 OK{0}Content-Type: text/html{0}{0}'.format(EOL)
    else:
        html_response = 'HTTP/1.1 404 Not Found{0}{0}'.format(EOL)
    return html_response


if __name__ == '__main__':
    main()

def build_html(body=""):
    """
    builds the html based on parameters sent to me
    Allows me to reduce the amount of repeated code and simplify
    the creation of html pages
    """
    html_str = EOL.join(['<!DOCTYPE html>',
                            '<html>',
                            '<head>',
                            '</head>',
                            '<body>',
                            body,
                            '</body>',
                            '</html>'])
    return html_str


