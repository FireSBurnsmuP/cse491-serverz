#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.getfqdn() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.

htmlResponse = """

HTTP/1.0 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <body>
  <h1>Hello, world</h1> this is fires' Web server.
  </body>
</html>

"""
print 'Entering infinite loop; hit CTRL-C to exit'
while True:
    # Establish connection with client.    
    c, (client_host, client_port) = s.accept()
    print c.recv(1000)
    print 'Got connection from', client_host, client_port
    c.send(htmlResponse)
    c.send('Thank you for connecting ')
    c.send("good bye.")
    c.close()
