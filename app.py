#!/bin/env python
"""
app.py - the wsgi application interface for my site
"""
from urlparse import urlparse
from urlparse import parse_qs
import jinja2

def base_app(environ, start_response):
    """
    My WSGI base application's entry function.
    Processes requests for the application at the
    root of this server.
    """

    # First load the jinja template environment.
    jinja = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))

    # find out which page they are accessing...
    uri = urlparse(environ['PATH_INFO'])
    path = uri.path.lower()
    if path in ('', '/', 'index'):
        response_body = serve_index(environ, start_response, jinja)
    elif path == '/content':
        response_body = serve_content(environ, start_response, jinja)
    elif path == '/file':
        response_body = serve_file(environ, start_response, jinja)
    elif path == '/image':
        response_body = serve_image(environ, start_response, jinja)
    elif path == '/form':
        response_body = serve_form(environ, start_response, jinja)
    elif path == '/submit':
        response_body = serve_submit(environ, start_response, jinja)
    else:
        # This is not the page you are looking for...
        response_body = serve_404(environ, start_response, jinja)

    return [response_body.encode('utf-8')]

def make_app():
    """
    The Application Start function.
    Returns a reference to whichever function should handle any
    WSGI connections.
    """
    return base_app


CRLF = "\r\n"

def serve_index(request, start_response, jinja):
    """
    Processes a request for the index of the site.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """

    if request['REQUEST_METHOD'] == 'GET':
        response_body = jinja.get_template("index.html").render()
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    elif request['REQUEST_METHOD'] == 'HEAD':
        response_body = ''
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', '0')
            ]
        )
    else:
        response_body = serve_405(request, start_response, jinja)
    return response_body

def serve_content(request, start_response, jinja):
    """
    Processes a request for the content page.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """

    if request['REQUEST_METHOD'] == 'GET':
        response_body = jinja.get_template("content.html").render()
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    elif request['REQUEST_METHOD'] == 'HEAD':
        response_body = ''
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', '0')
            ]
        )
    else:
        response_body = serve_405(request, start_response, jinja)
    return response_body

def serve_file(request, start_response, jinja):
    """
    Processes a request for the file.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """

    if request['REQUEST_METHOD'] == 'GET':
        response_body = jinja.get_template("file.html").render()
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    elif request['REQUEST_METHOD'] == 'HEAD':
        response_body = ''
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(
                jinja.get_template("file.html").render()
                )))
            ]
        )
    else:
        response_body = serve_405(request, start_response, jinja)
    return response_body

def serve_image(request, start_response, jinja):
    """
    Processes a request for the image.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """

    if request['REQUEST_METHOD'] == 'GET':
        response_body = jinja.get_template("image.html").render()
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    elif request['REQUEST_METHOD'] == 'HEAD':
        response_body = ''
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(
                jinja.get_template("image.html").render()
                )))
            ]
        )
    else:
        response_body = serve_405(request, start_response, jinja)
    return response_body

def serve_form(request, start_response, jinja):
    """
    Processes a request for the form page.
    This page supports GET, and HEAD requests,
    all others are met with a 405.
    """

    if request['REQUEST_METHOD'] == 'GET':
        response_body = jinja.get_template("form.html").render()
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    elif request['REQUEST_METHOD'] == 'HEAD':
        response_body = ''
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(
                jinja.get_template("form.html").render()
                )))
            ]
        )
    else:
        response_body = serve_405(request, start_response, jinja)
    return response_body

def serve_submit(request, start_response, jinja):
    """
    Processes a request for the submit page
    This page supports GET, POST and HEAD requests,
    all others are met with a 405.
    """

    if request['REQUEST_METHOD'] == 'GET':
        #query = parse_qs(urlparse(request['uri']).query)
        response_body = jinja.get_template("submit.html").render(
            {
                'firstname': jinja2.escape(
                    request['query']['firstname']
                        if 'firstname' in request['query']
                        else 'Anon'
                ),
                'lastname': jinja2.escape(
                    request['query']['lastname']
                        if 'lastname' in request['query']
                        else 'Nymous'
                )
            }
        )
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    elif request['REQUEST_METHOD'] == 'POST':
        response_body = jinja.get_template("submit.html").render(
            {
                'firstname': jinja2.escape(
                    request['content']['firstname']
                        if 'firstname' in request['content']
                        else 'Anon'
                ),
                'lastname': jinja2.escape(
                    request['content']['lastname']
                        if 'lastname' in request['content']
                        else 'Nymous'
                )
            }
        )
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    elif request['REQUEST_METHOD'] == 'HEAD':
        response_body = ''
        # I've decided to leave out Content-Length here, because
        # it's too intensive to calculate for a head request
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    else:
        response_body = serve_405(request, start_response, jinja,
            allowed=['GET', 'POST', 'HEAD'])
    return response_body

def serve_404(request, start_response, jinja):
    "Processes a request for something that doesn't exist."

    if request['REQUEST_METHOD'] == 'HEAD':
        # Just send the headers for my 404 page.
        response_body = ''
        # Once again, I'm not going to send back
        # a Content-Length for HEAD on a 404,
        # it's not important
        start_response('404 Not Found', [('Content-Type', 'text/html; charset=utf-8')])
    else:
        # Actually send the 404 page.
        response_body = jinja.get_template("404.html").render()
        start_response('404 Not Found', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    return response_body

def serve_405(request, start_response, jinja, allowed=None):
    """
    Processes a request for a resource to which the client
    has requested a method I don't support, including sending
    a list of supported formats.
    Default for 'allowed' is ['GET', 'HEAD'], what most things
    allow.
    """
    if allowed is None:
        allowed = ['GET', 'HEAD']
    start_response(('405 Method Not Allowed'),
        [('Allow', '{0}'.format(', '.join(allowed)))])
    return ''
