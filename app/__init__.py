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
    response_body = pages.serve_page(environ, start_response)

    return response_body

def make_app():
    """
    The Application Start function.
    Returns a reference to whichever function should handle any
    WSGI connections.
    """
    return base_app

