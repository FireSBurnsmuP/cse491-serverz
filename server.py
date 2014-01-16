#!/usr/bin/env python
import random
import socket
import time

# @CAT Consistency of comment placement would be nice
# Also, it doesn't work for me on ff or chrome

s = socket.socket()         # Create a socket object
host = socket.getfqdn() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.


print 'Entering infinite loop; hit CTRL-C to exit'


while True:
    # Establish connection with client.    
    c, (client_host, client_port) = s.accept()
    print 'Got connection from', client_host, client_port
    
    #c.send('Thank you for connecting')
    c.send("HTTP/1.0 200 OK\r\n")
    c.send("Content-type: text/html\r\n")
    # @CAT         ^^^ "Type" needs to be capitalized to be valid.
    # Also, there should be another newline here, could be why it's broke.
    c.send("<html>\r\n")
    c.send("<body>\r\n")
    c.send("<h1>Hello World</h1>\r\n")
    c.send("This is QSSS's web server\r\n")
    c.send("</body>\r\n")
    c.send("</html>\r\n")
    #c.send("good bye.")
    c.close()
