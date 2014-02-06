"""
Contains the tests for server.py
"""
import requests
import server

EOL = "\r\n"

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
        "receives something?"
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r

        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        "sends something?"
        self.sent += s

    def close(self):
        "closes connection?"
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    """
    Test the function that handles connections by sending
    any request through it.
    """
    conn = FakeConnection("GET / HTTP/1.1{0}{0}".format(EOL))
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
                    '      <li><a href="/submit">Submit</a></li>',
                    '    </ul>',
                    '  </div>',
                    '</body>',
                    '</html>'])

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

#
# 404 tests
#

def test_get_404():
    "Tests the GET method handler for 404 error"
    conn = FakeConnection("GET /idontexist HTTP/1.1{0}{0}".format(EOL))
    expected_return = 'HTTP/1.1 404 Not Found{0}{0}'.format(EOL)

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


def test_head_404():
    "Tests the HEAD method handler for 404 error"
    conn = FakeConnection("HEAD /idontexist HTTP/1.1{0}{0}".format(EOL))
    expected_return = 'HTTP/1.1 404 Not Found{0}{0}'.format(EOL)

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

#
# GET method tests
#

def test_get_content():
    "Tests the GET method handler for /content"
    conn = FakeConnection("GET /content HTTP/1.1{0}{0}".format(EOL))
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
    "Tests the GET method handler for /image"
    conn = FakeConnection("GET /image HTTP/1.1{0}{0}".format(EOL))
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
    "Tests the GET method handler for /file"
    conn = FakeConnection("GET /file HTTP/1.1{0}{0}".format(EOL))
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
    "Tests the GET method handler for /form"
    conn = FakeConnection("GET /form HTTP/1.1{0}{0}".format(EOL))
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
    "Tests the GET method handler for /submit"
    conn = FakeConnection("GET /submit?firstname=Zerxes&lastname=WaffleHouse HTTP/1.1{0}{0}".format(EOL))
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

#
# POST method tests
#

def test_post_index():
    "Tests the the index for POST (405)"
    conn = FakeConnection("POST / HTTP/1.1{0}{0}".format(EOL))
    expected_return = "HTTP/1.1 405 Method Not Allowed{0}{0}".format(EOL)

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post_submit():
    "Tests the POST method handler on /submit"
    conn = FakeConnection("POST /submit HTTP/1.1{0}{0}".format(EOL))
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

def test_post_form():
    "Tests the POST method handler on /form"
    conn = FakeConnection("POST /form HTTP/1.1{0}{0}".format(EOL))
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

#
# PUT method tests
#

def test_put():
    "Tests the PUT method handler (405)"
    conn = FakeConnection("PUT / HTTP/1.1{0}{0}".format(EOL))
    expected_return = "HTTP/1.1 405 Method Not Allowed{0}{0}".format(EOL)

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

#
# DELETE method tests
#

def test_delete():
    "Tests the DELETE method handler (405)"
    conn = FakeConnection("DELETE / HTTP/1.1{0}{0}".format(EOL))
    expected_return = "HTTP/1.1 405 Method Not Allowed{0}{0}".format(EOL)

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

#
# HEAD method tests
#

def test_head():
    "Tests the HEAD method handler for /"
    conn = FakeConnection("HEAD / HTTP/1.1{0}{0}".format(EOL))
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_content():
    "Tests the HEAD method handler for /content"
    conn = FakeConnection("HEAD /content HTTP/1.1{0}{0}".format(EOL))
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_file():
    "Tests the HEAD method handler for /file"
    conn = FakeConnection("HEAD /file HTTP/1.1{0}{0}".format(EOL))
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_submit():
    "Tests the HEAD method handler for /submit"
    conn = FakeConnection("HEAD /submit HTTP/1.1{0}{0}".format(EOL))
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_form():
    "Tests the HEAD method handler for /form"
    conn = FakeConnection("HEAD /form HTTP/1.1{0}{0}".format(EOL))
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_head_image():
    "Tests the HEAD method handler for /image"
    conn = FakeConnection("HEAD /image HTTP/1.1{0}{0}".format(EOL))
    expected_return = "HTTP/1.1 200 OK" + EOL \
                    + "Content-Type: text/html" + EOL \
                    + EOL

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

