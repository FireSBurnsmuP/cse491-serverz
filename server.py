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
    print c.recv(1000)
    print 'Got connection from', client_host, client_port
    handle_connection(c)

def handle_connection(conn):
  "Handles a given connection by sending the proper response"

  # This code was jbull477's, I just added the DOCTYPE.
  EOF = "\r\n"
  htmlResponse = "HTTP/1.0 200 OK" + EOF
  htmlResponse += "Content-Type: text/html" + EOF
  htmlResponse += EOF
  htmlResponse += "<!DOCTYPE html>" + EOF
  htmlResponse += "<html>" + EOF
  htmlResponse += "  <body>" + EOF
  htmlResponse += "  <h1>Hello, world</h1> this is fires' Web server." + EOF
  htmlResponse += "  </body>" + EOF
  htmlResponse += "</html>" + EOF
  conn.send(htmlResponse)
  conn.close()

if __name__ == '__main__':
  main()
