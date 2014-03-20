"""
Contains the tests for server.py
"""
import requests
import server

CRLF = "\r\n"

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
    conn = FakeConnection("GET / HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = '<title>Fires&apos; Index</title>'

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_cookie():
    """
    Test cookie passing
    """

    assert False, 'Cookie test not yet implemented'

#
# 404 tests
#

def test_get_404():
    "Tests the GET method handler for 404 error"
    conn = FakeConnection("GET /idontexist HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = '<h1>This is not the page you are looking for...</h1>'

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)


def test_head_404():
    "Tests the HEAD method handler for 404 error"
    conn = FakeConnection("HEAD /idontexist HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = CRLF.join([
        'HTTP/1.1 404 Not Found',
        'Content-Type: text/html; charset=utf-8'
    ])

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

#
# GET method tests
#

def test_get_content():
    "Tests the GET method handler for /content"
    conn = FakeConnection("GET /content HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = '<title>Fires&apos; Content Page</title>'

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_get_image():
    "Tests the GET method handler for /image"
    conn = FakeConnection("GET /image HTTP/1.1{0}{0}".format(CRLF))
    # TODO better test for images
    expected_in_return = '200 OK'

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_get_file():
    "Tests the GET method handler for /file"
    conn = FakeConnection("GET /file HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = 'PSXDIR'

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_get_form():
    "Tests the GET method handler for /form"
    conn = FakeConnection("GET /form HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = '<h1>Hello, world</h1> this is the form on fires&apos; Web server.'

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_get_submit():
    "Tests the GET method handler for /submit"
    conn = FakeConnection("GET /submit?firstname=Zerxes&lastname=Wafflehouse HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = '<h1>Hello, Zerxes Wafflehouse.</h1>'

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

#
# POST method tests
#

def test_post_index():
    "Tests the the index for POST (405)"
    conn = FakeConnection("POST / HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = CRLF.join([
        'HTTP/1.1 405 Method Not Allowed',
        'Allow: GET, HEAD',
        CRLF
    ])

    server.handle_connection(conn)

    assert conn.sent == expected_in_return, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_post_submit_form_enc():
    "Tests the POST (x-www-form-urlencoded) handler on /submit"
    conn = FakeConnection(CRLF.join([
        'POST /submit HTTP/1.1',
        'Content-Length: 37',
        'Content-Type: application/x-www-form-urlencoded',
        '',
        'firstname=Zerxes&lastname=Wafflehouse'
        ])
    )
    expected_in_return = '<h1>Hello, Zerxes Wafflehouse.</h1>'

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_post_submit_multipart():
    "Tests the POST (multipart/form-data) handler on /submit"
    # TODO FIXME
    # conn = requests.post('/submit', data={
    #         'firstname': 'Zerxes',
    #         'lastname': 'Wafflehouse'
    #     }
    # )
    conn = FakeConnection(CRLF.join([
        'POST /submit HTTP/1.1',
        'Content-Length: 306',
        'Content-Type: multipart/form-data; '
        'boundary=---------------------------19062113681433463560301987834',
        '',
        '-----------------------------19062113681433463560301987834',
        'Content-Disposition: form-data; name="firstname"',
        'Zerxes',
        '-----------------------------19062113681433463560301987834 ',
        'Content-Disposition: form-data; name="lastname"',
        'Wafflehouse ',
        '-----------------------------19062113681433463560301987834--'
        ])
    )
    expected_in_return = '<h1>Hello, Zerxes Wafflehouse.</h1>'

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)
    # assert False, 'multipart/form-data post test not yet implemented'

#
# PUT method tests
#

def test_put_index():
    "Tests the PUT method handler (405)"
    conn = FakeConnection("PUT / HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = CRLF.join([
        'HTTP/1.1 405 Method Not Allowed',
        'Allow: GET, HEAD',
        CRLF
    ])

    server.handle_connection(conn)

    assert conn.sent == expected_in_return, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_put_submit():
    "Tests the PUT method handler for the submit(405)"
    conn = FakeConnection("PUT /submit HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = CRLF.join([
        'HTTP/1.1 405 Method Not Allowed',
        'Allow: GET, POST, HEAD',
        CRLF
    ])

    server.handle_connection(conn)

    assert conn.sent == expected_in_return, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

#
# DELETE method tests
#

def test_delete_index():
    "Tests the DELETE method handler (405)"
    conn = FakeConnection("DELETE / HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = CRLF.join([
        'HTTP/1.1 405 Method Not Allowed',
        'Allow: GET, HEAD',
        CRLF
    ])

    server.handle_connection(conn)

    assert conn.sent == expected_in_return, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

#
# HEAD method tests
#

def test_head_index():
    "Tests the HEAD method handler for /"
    conn = FakeConnection("HEAD / HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = CRLF.join([
        'HTTP/1.1 200 OK',
        'Content-Type: text/html; charset=utf-8'
    ])

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_head_content():
    "Tests the HEAD method handler for /content"
    conn = FakeConnection("HEAD /content HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = CRLF.join([
        'HTTP/1.1 200 OK',
        'Content-Type: text/html; charset=utf-8'
    ])

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_head_file():
    "Tests the HEAD method handler for /file"
    conn = FakeConnection("HEAD /file HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = CRLF.join([
        'HTTP/1.1 200 OK',
        'Content-Type: text/plain; charset=utf-8'
    ])

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_head_submit():
    "Tests the HEAD method handler for /submit"
    conn = FakeConnection("HEAD /submit HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = CRLF.join([
        'HTTP/1.1 200 OK',
        'Content-Type: text/html; charset=utf-8'
    ])

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_head_form():
    "Tests the HEAD method handler for /form"
    conn = FakeConnection("HEAD /form HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = CRLF.join([
        'HTTP/1.1 200 OK',
        'Content-Type: text/html; charset=utf-8'
    ])

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

def test_head_image():
    "Tests the HEAD method handler for /image"
    conn = FakeConnection("HEAD /image HTTP/1.1{0}{0}".format(CRLF))
    expected_in_return = CRLF.join([
        'HTTP/1.1 200 OK',
        'Content-Type: image/jpeg'
    ])

    server.handle_connection(conn)

    assert expected_in_return in conn.sent, 'Got: "{0}",\nExpected: "{1}"'.format(conn.sent, expected_in_return)

