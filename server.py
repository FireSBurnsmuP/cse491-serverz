#!/usr/bin/env python
import random
import socket
import time

def main():
    "Starts up the server and waits for connections"

    # Create a socket object
    s = socket.socket()
    # Get local machine name
    host = socket.getfqdn()
    port = random.randint(8000, 9999)
    # Bind to the port
    s.bind((host, port))
    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)
    # Now wait for client connection.
    s.listen(5)

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)

def handle_connection(conn):
    "Handles a given connection by sending the proper response"

    EOF = "\r\n"
    request = conn.recv(1000)
    # parse the request line
    request = request.splitlines()
    request_line = request[0].split()
    if request_line[0] == 'GET' :
        html_response = get(request_line)
    elif request_line[0] == 'POST':
        html_response = post(request_line)
    elif request_line[0] == 'HEAD':
        html_response = head(request_line)
    else :
        # do other stuff
        html_response = "HTTP/1.1 405 Method Not Allowed" + EOF + EOF
    conn.send(html_response)
    conn.close()

def get(request_line) :
    "Processes a get request"

    EOF = "\r\n"
    if request_line[1] == '/':
        html_response = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF \
                    + "<!DOCTYPE html>" + EOF \
                    + "<html>" + EOF \
                    + "  <body>" + EOF \
                    + "  <h1>Hello, world</h1> this is fires' Web server." + EOF \
                    + "  <h3>Links:</h3>" + EOF \
                    + "  <div style=\"padding-left: 1.0em;\">" + EOF \
                    + "    <ul>" + EOF \
                    + "      <li><a href=\"/content\">Content</a></li>" + EOF \
                    + "      <li><a href=\"/file\">File</a></li>" + EOF \
                    + "      <li><a href=\"/image\">Image</a></li>" + EOF \
                    + "    </ul>" + EOF \
                    + "  </div>" + EOF \
                    + "  </body>" + EOF \
                    + "</html>" + EOF
    elif request_line[1] == '/content':
        html_response = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF \
                    + "<!DOCTYPE html>" + EOF \
                    + "<html>" + EOF \
                    + "  <body>" + EOF \
                    + "  <h1>Hello, world</h1> this is the content on fires' Web server." + EOF \
                    + "  </body>" + EOF \
                    + "</html>" + EOF
    elif request_line[1] == '/file':
        html_response = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF \
                    + "<!DOCTYPE html>" + EOF \
                    + "<html>" + EOF \
                    + "  <body>" + EOF \
                    + "  <h1>Hello, world</h1> this is the file on fires' Web server." + EOF \
                    + "  </body>" + EOF \
                    + "</html>" + EOF
    elif request_line[1] == '/image':
        html_response = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF \
                    + "<!DOCTYPE html>" + EOF \
                    + "<html>" + EOF \
                    + "  <body>" + EOF \
                    + "  <h1>Hello, world</h1> this is the image on fires' Web server." + EOF \
                    + "  </body>" + EOF \
                    + "</html>" + EOF
    else :
        html_response = "HTTP/1.1 404 Not Found" + EOF + EOF
    return html_response;

def post(request_line) :
    "processes a POST request"

    EOF = "\r\n"
    html_response = "HTTP/1.1 200 OK" + EOF \
                + "Content-Type: text/html" + EOF \
                + EOF \
                + "<!DOCTYPE html>" + EOF \
                + "<html>" + EOF \
                + "  <body>" + EOF \
                + "  <h1>Hello, world</h1> you've attempted to POST to fires' Web server." + EOF \
                + "  </body>" + EOF \
                + "</html>" + EOF
    return html_response

def head(request_line):
    "processes a HEAD request"

    EOF = "\r\n"
    if request_line[1] == '/':
        html_response = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF
    elif request_line[1] == '/content':
        html_response = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF
    elif request_line[1] == '/file':
        html_response = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF
    elif request_line[1] == '/image':
        html_response = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF
    else :
        html_response = "HTTP/1.1 404 Not Found" + EOF + EOF
    return html_response


if __name__ == '__main__':
    main()
