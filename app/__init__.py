#!/usr/bin/env python
"""
app.py - the wsgi application interface for my site
"""
from . import pages
from urlparse import parse_qs
import cgi

def base_app(environ, start_response):
    """
    My WSGI base application's entry function.
    Processes requests for the application at the
    root of this server.
    """

    # first parse out the query string
    query = {}
    temp = parse_qs(environ['QUERY_STRING']).iteritems()
    query = {
        key : val[0]
        for key, val in temp
    }
    # and store the query string
    environ['query'] = query

    # Parse any form data
    if (environ['REQUEST_METHOD'].upper() == 'POST'
        and 'content' not in environ.keys()):
        if ('application/x-www-form-urlencoded' in environ['CONTENT_TYPE']
            or 'multipart/form-data' in environ['CONTENT_TYPE']):
            # in order to process form data, I need to read it out of wsgi.input
            # make a copy of environ...
            temp_env = environ.copy()
            # and remove the query string so it doesn't mix with form-data
            temp_env['QUERY_STRING'] = ''
            # Init the field storage...
            temp = cgi.FieldStorage(
                fp=environ['wsgi.input'],
                environ=temp_env,
                keep_blank_values=1
            )
            # ... reset content to a dictionary...
            content = {}
            # ... and then parse all keys, values into content.
            for key in temp:
                content[key.lower()] = temp[key].value
        else:
            # TODO do something with other types
            # reset content to a dictionary
            content = {}
        # and store the content in the environ
        environ['content'] = content

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

