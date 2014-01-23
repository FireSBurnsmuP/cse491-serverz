import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r

        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.1\r\n\r\n")
    EOF = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOF \
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

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_get_content():
    conn = FakeConnection("GET /content HTTP/1.1\r\n\r\n")
    EOF = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF \
                    + "<!DOCTYPE html>" + EOF \
                    + "<html>" + EOF \
                    + "  <body>" + EOF \
                    + "  <h1>Hello, world</h1> this is the content on fires' Web server." + EOF \
                    + "  </body>" + EOF \
                    + "</html>" + EOF

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_get_image():
    conn = FakeConnection("GET /image HTTP/1.1\r\n\r\n")
    EOF = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF \
                    + "<!DOCTYPE html>" + EOF \
                    + "<html>" + EOF \
                    + "  <body>" + EOF \
                    + "  <h1>Hello, world</h1> this is the image on fires' Web server." + EOF \
                    + "  </body>" + EOF \
                    + "</html>" + EOF

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_get_file():
    conn = FakeConnection("GET /file HTTP/1.1\r\n\r\n")
    EOF = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF \
                    + "<!DOCTYPE html>" + EOF \
                    + "<html>" + EOF \
                    + "  <body>" + EOF \
                    + "  <h1>Hello, world</h1> this is the file on fires' Web server." + EOF \
                    + "  </body>" + EOF \
                    + "</html>" + EOF

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post():
    conn = FakeConnection("POST / HTTP/1.1\r\n\r\n")
    EOF = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF \
                    + "<!DOCTYPE html>" + EOF \
                    + "<html>" + EOF \
                    + "  <body>" + EOF \
                    + "  <h1>Hello, world</h1> you've attempted to POST to fires' Web server." + EOF \
                    + "  </body>" + EOF \
                    + "</html>" + EOF

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_put():
    conn = FakeConnection("PUT / HTTP/1.1\r\n\r\n")
    EOF = "\r\n"
    expected_return = "HTTP/1.1 405 Method Not Allowed" + EOF + EOF

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_delete():
    conn = FakeConnection("DELETE / HTTP/1.1\r\n\r\n")
    EOF = "\r\n"
    expected_return = "HTTP/1.1 405 Method Not Allowed" + EOF + EOF

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head():
    conn = FakeConnection("HEAD / HTTP/1.1\r\n\r\n")
    EOF = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_content():
    conn = FakeConnection("HEAD /content HTTP/1.1\r\n\r\n")
    EOF = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_file():
    conn = FakeConnection("HEAD /file HTTP/1.1\r\n\r\n")
    EOF = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_image():
    conn = FakeConnection("HEAD /image HTTP/1.1\r\n\r\n")
    EOF = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOF \
                    + "Content-Type: text/html" + EOF \
                    + EOF

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
