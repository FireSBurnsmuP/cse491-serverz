#!/usr/bin/env python
"""
Main server file.
"""
import socket
from urlparse import urlparse
from urlparse import parse_qs
import jinja2
import cgi
from StringIO import StringIO


EOL = "\r\n"

def main():
    "Starts up the server and waits for connections"

    # Create a socket object
    sock = socket.socket()
    # Get local machine name
    host = socket.getfqdn()
    port = 9082
    #port = random.randint(8000, 9999)
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

    # First load the jinja template environment.
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    # Then get the request data and parse it.
    request = read_request(conn)

    # find out which page they are accessing...
    uri = urlparse(request['uri'])
    path = uri.path.lower()
    if path in ('/', 'index'):
        html_response = serve_index(request, env)
    elif path == '/content':
        html_response = serve_content(request, env)
    elif path == '/file':
        html_response = serve_file(request, env)
    elif path == '/image':
        html_response = serve_image(request, env)
    elif path == '/form':
        html_response = serve_form(request, env)
    elif path == '/submit':
        html_response = serve_submit(request, env)
    else:
        # This is not the page you are looking for...
        html_response = serve_404(request, env)

    conn.send(html_response)
    conn.close()

def read_request(conn):
    """
    Reads and parses the request sent by the client,
    and returns the resulting request as a dictionary.
    The returned dictionary will be of the format:
    {
        'method': (request method),
        'uri': (requested uri),
        'protocol': (protocol (most likely HTTP)),
        'protocol_version': (version of that protocol),
        'headers': {
            (headers go in this sub-dictionary, if present,
                otherwise this is empty.)
        },
        'content': {
            (content goes in here, if it exists,
                otherwise this is empty.)
        }
    }
    """

    # Grab the headers from the connection socket
    temp = ''
    while '\r\n\r\n' not in temp:
        temp += conn.recv(1)
    request = temp.rstrip().split(EOL)

    # Pull/parse the request line...
    temp = request[0].split()
    request_line = {}
    request_line['method'] = temp[0]
    request_line['uri'] = temp[1]
    temp = temp[2].split('/')
    request_line['protocol'] = temp[0]
    request_line['version'] = temp[1]

    # ... and headers...
    # For this I must remove the request line
    request = request[1:len(request)]
    headers = {}
    for line in request:
        key, value = line.split(': ', 1)
        headers[key.lower()] = value
    # ... and content (if it exists)
    if 'content-length' in headers:
        content = conn.recv(int(headers['content-length']))
        if 'content-type' in headers:
            if 'application/x-www-form-urlencoded' in headers['content-type']:
                # form encoding's easy: just parse the query string...
                temp = parse_qs(content)
                # reset content to a dictionary
                content = {}
                # ... and store in my dictionary.
                for key in temp:
                    content[key.lower()] = temp[key][0]
            elif 'multipart/form-data' in headers['content-type']:
                # Multipart's a bit trickier: going cgi on this one.
                # Init the field storage...
                temp = cgi.FieldStorage(
                    headers=headers, fp=StringIO(content),
                    environ={'REQUEST_METHOD' : 'POST'}
                )
                # ... reset content to a dictionary...
                content = {}
                # ... and then parse all keys, values into content.
                for key in temp:
                    content[key] = temp[key].value
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
        'method': request_line['method'],
        'uri': request_line['uri'],
        'protocol': request_line['protocol'],
        'protocol_version': request_line['version'],
        'headers': headers,
        'content': content
    }
    return request

def serve_index(request, env):
    """
    Processes a request for the index of the site.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """

    if request['method'] == 'GET':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            '',
            env.get_template("index.html").render()
        ])
    elif request['method'] == 'HEAD':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            ''
        ])
    else:
        html_response = serve_405(request, env)
    return html_response

def serve_content(request, env):
    """
    Processes a request for the content page.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """

    if request['method'] == 'GET':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            '',
            env.get_template("content.html").render()
        ])
    elif request['method'] == 'HEAD':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            ''
        ])
    else:
        html_response = serve_405(request, env)
    return html_response

def serve_file(request, env):
    """
    Processes a request for the file.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """

    if request['method'] == 'GET':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            '',
            env.get_template("file.html").render()
        ])
    elif request['method'] == 'HEAD':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            ''
        ])
    else:
        html_response = serve_405(request, env)
    return html_response

def serve_image(request, env):
    """
    Processes a request for the image.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """

    if request['method'] == 'GET':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            '',
            env.get_template("image.html").render()
        ])
    elif request['method'] == 'HEAD':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            ''
        ])
    else:
        html_response = serve_405(request, env)
    return html_response

def serve_form(request, env):
    """
    Processes a request for the form page.
    This page supports GET, and HEAD requests,
    all others are met with a 405.
    """

    if request['method'] == 'GET':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            '',
            env.get_template("form.html").render()
        ])
    elif request['method'] == 'HEAD':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            ''
        ])
    else:
        html_response = serve_405(request, env)
    return html_response

def serve_submit(request, env):
    """
    Processes a request for the submit page
    This page supports GET, POST and HEAD requests,
    all others are met with a 405.
    """

    uri = urlparse(request['uri'])

    if request['method'] == 'GET':
        query = parse_qs(uri.query)
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            '',
            env.get_template("submit.html").render({
                'firstname': query['firstname'][0],
                'lastname': query['lastname'][0]
            })
        ])
    elif request['method'] == 'POST':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            '',
            env.get_template("submit.html").render({
                'firstname': request['content']['firstname'],
                'lastname': request['content']['lastname']
            })
        ])
    elif request['method'] == 'HEAD':
        html_response = EOL.join([
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            ''
        ])
    else:
        html_response = serve_405(request, env, ['GET', 'POST', 'HEAD'])
    return html_response

def serve_404(request, env):
    "Processes a request for something that doesn't exist."

    if request['method'] == 'HEAD':
        # Just send the headers for my 404 page.
        html_response = EOL.join([
            'HTTP/1.1 404 Not Found',
            'Content-Type: text/html',
            ''
        ])
    else:
        # Actually send the 404 page.
        html_response = EOL.join([
            'HTTP/1.1 404 Not Found',
            'Content-Type: text/html',
            '',
            env.get_template("404.html").render()
        ])
    return html_response

def serve_405(request, env, allowed=None):
    """
    Processes a request for a resource to which the client
    has requested a method I don't support, including sending
    a list of supported formats.
    Default for 'allowed' is ['GET', 'HEAD'], what most things
    allow.
    """
    html_response = EOL.join([
        'HTTP/1.1 405 Method Not Allowed',
        'Allow: {}'.format(', '.join(allowed or ['GET', 'HEAD'])),
        ''
    ])
    return html_response

if __name__ == '__main__':
    main()
