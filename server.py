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
    r_type = request_line[0]

    # find out which page they are accessing...
    parsed = urlparse(request_line[1])
    path = parsed.path.lower()
    if path in ('/', 'index'):
        html_response = serve_index(r_type, request_line, request)
    elif path in ('/content'):
        html_response = serve_content(r_type, request_line, request)
    elif path in ('/file'):
        html_response = serve_file(r_type, request_line, request)
    elif path in ('/image'):
        html_response = serve_image(r_type, request_line, request)
    elif path in ('/form'):
        html_response = serve_form(r_type, request_line, request)
    elif path in ('/submit'):
        html_response = serve_submit(r_type, request_line, request)
    else:
        # This is not the page you are looking for...
        html_response = 'HTTP/1.1 404 Not Found{0}{0}'.format(EOL)

    conn.send(html_response)
    conn.close()

def serve_index(r_type, request_line, request):
    """
    Processes a request for the index of the site.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """
    if r_type == 'GET':
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
                    '      <li><a href="/submit">Submit</a></li>',
                    '    </ul>',
                    '  </div>',
                    '</body>',
                    '</html>'])
    elif r_type == 'HEAD':
        html_response = 'HTTP/1.1 200 OK{0}Content-Type: text/html{0}{0}'.format(EOL)
    else:
        html_response = 'HTTP/1.1 405 Method Not Allowed{0}{0}'.format(EOL)
    return html_response

def serve_content(r_type, request_line, request):
    """
    Processes a request for the content page.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """
    if r_type == 'GET':
        html_response = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello, world</h1> this is the content on fires&apos; Web server.',
                    '</body>',
                    '</html>'])
    elif r_type == 'HEAD':
        html_response = 'HTTP/1.1 200 OK{0}Content-Type: text/html{0}{0}'.format(EOL)
    else:
        html_response = 'HTTP/1.1 405 Method Not Allowed{0}{0}'.format(EOL)
    return html_response

def serve_file(r_type, request_line, request):
    """
    Processes a request for the file.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """
    if r_type == 'GET':
        html_response = EOL.join(['HTTP/1.1 200 OK',
                'Content-Type: text/html',
                '',
                '<!DOCTYPE html>',
                '<html>',
                '<body>',
                '  <h1>Hello, world</h1> this is the file on fires&apos; Web server.',
                '</body>',
                '</html>'])
    elif r_type == 'HEAD':
        html_response = 'HTTP/1.1 200 OK{0}Content-Type: text/html{0}{0}'.format(EOL)
    else:
        html_response = 'HTTP/1.1 405 Method Not Allowed{0}{0}'.format(EOL)
    return html_response

def serve_image(r_type, request_line, request):
    """
    Processes a request for the image.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """
    if r_type == 'GET':
        html_response = EOL.join(['HTTP/1.1 200 OK',
                'Content-Type: text/html',
                '',
                '<!DOCTYPE html>',
                '<html>',
                '<body>',
                '  <h1>Hello, world</h1> this is the image on fires&apos; Web server.',
                '</body>',
                '</html>'])
    elif r_type == 'HEAD':
        html_response = 'HTTP/1.1 200 OK{0}Content-Type: text/html{0}{0}'.format(EOL)
    else:
        html_response = 'HTTP/1.1 405 Method Not Allowed{0}{0}'.format(EOL)
    return html_response

def serve_form(r_type, request_line, request):
    """
    Processes a request for the form page.
    This page supports GET, POST, and HEAD requests,
    all others are met with a 405.
    """
    if r_type == 'GET':
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
    elif r_type == 'POST':
        # TODO Check 2 different Content-Types
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
    elif r_type == 'HEAD':
        html_response = 'HTTP/1.1 200 OK{0}Content-Type: text/html{0}{0}'.format(EOL)
    else:
        html_response = 'HTTP/1.1 405 Method Not Allowed{0}{0}'.format(EOL)
    return html_response

def serve_submit(r_type, request_line, request):
    """
    Processes a request for the submit page
    This page supports GET, POST and HEAD requests,
    all others are met with a 405.
    """
    # Okay, now to parse out the form variables
    parsed = urlparse(request_line[1])
    query = parse_qs(parsed.query)
    if r_type == 'GET':
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
    elif r_type == 'POST':
        # TODO Check 2 different Content-Types
        html_response = EOL.join(['HTTP/1.1 200 OK',
                'Content-Type: text/html',
                '',
                '<!DOCTYPE html>',
                '<html>',
                '<body>',
                '  <h1>Hello, world</h1> you&apos;ve attempted to POST to fires&apos; Web server.',
                '</body>',
                '</html>'])
    elif r_type == 'HEAD':
        html_response = 'HTTP/1.1 200 OK{0}Content-Type: text/html{0}{0}'.format(EOL)
    else:
        html_response = 'HTTP/1.1 405 Method Not Allowed{0}{0}'.format(EOL)
    return html_response

if __name__ == '__main__':
    main()
