"""
Handles the actual rendering of the pages
"""
# TODO class it, make it less necessary to pass around all these vars

from . import html
from . import static_files
from . import image

from urlparse import urlparse
from urlparse import parse_qs

# constant for the frequently used '\r\n' line-ending
CRLF = "\r\n"

def serve_page(request, start_response):
    """
    figures out which page to serve and serves it.
    """
    # first parse out the path
    uri = urlparse(request['PATH_INFO'])
    path = uri.path.lower()

    if path in ('', '/', 'index'):
        response_body = std_html('index', request, start_response)
    elif path == '/content':
        response_body = std_html('content', request, start_response)
    elif path == '/file':
        response_body = static_file(request, start_response)
    elif path == '/image':
        response_body = static_image(request, start_response)
    elif path == '/form':
        response_body = std_html('form', request, start_response)
    elif path == '/submit':
        response_body = submit(request, start_response)
    elif path == '/imageshare':
        response_body = std_html('imageshare', request, start_response)
    else:
        # This is not the page you are looking for...
        response_body = serve_404(request, start_response)

    if path != '/image':
        response_body = [response_body.encode('utf-8')]

    return response_body

def std_html(page, request, start_response):
    """
    renders a standard page by its name;
    for pages which support GET and HEAD requests,
    and meet all others with a 405.
    """
    if request['REQUEST_METHOD'] == 'GET':
        response_body = html.render(''.join([page,".html"]))
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
                html.render(''.join([page,".html"]))
                )))
            ]
        )
    else:
        response_body = serve_405(request, start_response)
    return response_body

def serve_static_file(filename, request, start_response):
    """
    Processes a request for a text-file by filename.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    If the image isn't in my static directory, 404 it.
    """

    if request['REQUEST_METHOD'] == 'GET':
        response_body = static_files.get_text_file(filename)
        if response_body is not None:
            start_response('200 OK', [
                ('Content-Type', 'text/plain; charset=utf-8'),
                ('Content-Length', str(len(response_body)))
                ]
            )
        else:
            # if the file couldn't be found, serve a 404
            response_body = serve_404(request, start_response)

    elif request['REQUEST_METHOD'] == 'HEAD':
        response_body = static_files.get_text_file(filename)
        if response_body is not None:
            start_response('200 OK', [
                ('Content-Type', 'text/plain; charset=utf-8'),
                ('Content-Length', str(len(response_body)))
                ]
            )
        else:
            # if the file couldn't be found, serve a 404
            response_body = serve_404(request, start_response)
        response_body = ''

    else:
        response_body = serve_405(request, start_response)
    return response_body

def static_file(request, start_response):
    """
    Processes a request for the file.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """
    response_body = serve_static_file(
        'psxrip', request, start_response
        )
    return response_body

def static_image(request, start_response):
    """
    Processes a request for the image.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    """
    response_body = serve_static_image(
        'neuromancer.jpg', request, start_response
        )
    return response_body

def serve_static_image(filename, request, start_response):
    """
    Processes a request for an image by filename.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    If the image isn't in my static directory, 404 it.
    """

    if request['REQUEST_METHOD'] == 'GET':
        response_body = static_files.get_image_file(filename)
        if response_body is not None:
            start_response('200 OK', [
                ('Content-Type', 'image/jpeg'),
                ('Content-Length', str(len(response_body)))
                ]
            )
        else:
            # if the file couldn't be found, serve a 404
            response_body = serve_404(request, start_response)

    elif request['REQUEST_METHOD'] == 'HEAD':
        response_body = static_files.get_image_file(filename)
        if response_body is not None:
            start_response('200 OK', [
                ('Content-Type', 'image/jpeg'),
                ('Content-Length', str(len(response_body)))
                ]
            )
        else:
            # if the file couldn't be found, serve a 404
            response_body = serve_404(request, start_response)
        response_body = ''

    else:
        response_body = serve_405(request, start_response)
    return response_body

def submit(request, start_response):
    """
    Processes a request for the submit page
    This page supports GET, POST and HEAD requests,
    all others are met with a 405.
    """

    if request['REQUEST_METHOD'] == 'GET':
        #query = parse_qs(urlparse(request['uri']).query)
        response_body = html.render("submit.html",
            {
                'firstname': html.escape(
                    request['query']['firstname']
                        if 'firstname' in request['query']
                        else 'Anon'
                ),
                'lastname': html.escape(
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
        response_body = html.render("submit.html",
            {
                'firstname': html.escape(
                    request['content']['firstname']
                        if 'firstname' in request['content']
                        else 'Anon'
                ),
                'lastname': html.escape(
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
        start_response('200 OK',
            [('Content-Type', 'text/html; charset=utf-8')])
    else:
        response_body = serve_405(request, start_response,
            allowed=['GET', 'POST', 'HEAD'])
    return response_body

# client errors...

def serve_404(request, start_response):
    "Processes a request for something that doesn't exist."

    if request['REQUEST_METHOD'] == 'HEAD':
        # Just send the headers for my 404 page.
        response_body = ''
        # Once again, I'm not going to send back
        # a Content-Length for HEAD on a 404,
        # it's not important
        start_response('404 Not Found',
            [('Content-Type', 'text/html; charset=utf-8')])
    else:
        # Actually send the 404 page.
        response_body = html.render("404.html")
        start_response('404 Not Found', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    return response_body

def serve_405(request, start_response, allowed=None):
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
