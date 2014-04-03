#!/usr/bin/env python
"""
app.py - the wsgi application interface for my site
"""
from urlparse import urlparse
from urlparse import parse_qs
from . import pages

def base_app(environ, start_response):
    """
    My WSGI base application's entry function.
    Processes requests for the application at the
    root of this server.
    """

    # find out which page they are accessing...
    uri = urlparse(environ['PATH_INFO'])
    path = uri.path.lower()
    if path in ('', '/', 'index'):
        response_body = pages.std_html('index', environ, start_response)
    elif path == '/content':
        response_body = pages.std_html('content', environ, start_response)
    elif path == '/file':
        response_body = pages.file(environ, start_response)
    elif path == '/image':
        response_body = pages.image(environ, start_response)
    elif path == '/form':
        response_body = pages.std_html('form', environ, start_response)
    elif path == '/submit':
        response_body = pages.submit(environ, start_response)
    elif path == '/imageshare':
        response_body = pages.std_html('imageshare', environ, start_response)
    else:
        # This is not the page you are looking for...
        response_body = pages.serve_404(environ, start_response)

    if path != '/image':
        response_body = [response_body.encode('utf-8')]

    return response_body

def make_app():
    """
    The Application Start function.
    Returns a reference to whichever function should handle any
    WSGI connections.
    """
    return base_app

