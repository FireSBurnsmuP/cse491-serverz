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
    EOL = "\r\n"
    expected_return = EOL.join(['HTTP/1.1 200 OK',
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

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_get_content():
    conn = FakeConnection("GET /content HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello, world</h1> this is the content on fires&apos; Web server.',
                    '</body>',
                    '</html>'])

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_get_image():
    conn = FakeConnection("GET /image HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello, world</h1> this is the image on fires&apos; Web server.',
                    '</body>',
                    '</html>'])

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_get_file():
    conn = FakeConnection("GET /file HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello, world</h1> this is the file on fires&apos; Web server.',
                    '</body>',
                    '</html>'])

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_get_form():
    conn = FakeConnection("GET /form HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = EOL.join(['HTTP/1.1 200 OK',
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

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_get_submit():
    conn = FakeConnection("GET /submit?firstname=Zerxes&lastname=WaffleHouse HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello Mr. Zerxes WaffleHouse.</h1>',
                    '</body>',
                    '</html>'])

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post():
    conn = FakeConnection("POST / HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = EOL.join(['HTTP/1.1 200 OK',
                    'Content-Type: text/html',
                    '',
                    '<!DOCTYPE html>',
                    '<html>',
                    '<body>',
                    '  <h1>Hello, world</h1> you&apos;ve attempted to POST to fires&apos; Web server.',
                    '</body>',
                    '</html>'])

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_put():
    conn = FakeConnection("PUT / HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = "HTTP/1.1 405 Method Not Allowed" + EOL + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_delete():
    conn = FakeConnection("DELETE / HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = "HTTP/1.1 405 Method Not Allowed" + EOL + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head():
    conn = FakeConnection("HEAD / HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_content():
    conn = FakeConnection("HEAD /content HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_file():
    conn = FakeConnection("HEAD /file HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_submit():
    conn = FakeConnection("HEAD /file HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_form():
    conn = FakeConnection("HEAD /file HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_image():
    conn = FakeConnection("HEAD /image HTTP/1.1\r\n\r\n")
    EOL = "\r\n"
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

