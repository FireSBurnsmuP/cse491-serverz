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
    elif path == '/favicon.ico':
        response_body = serve_static_image(
            'favicon.ico', request, start_response)
    elif '/static/images/' in path:
        image_name = path[15:]
        response_body = serve_static_image(
            image_name, request, start_response)
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
    elif path == '/js/imageshare.js':
        response_body = serve_static_js(
            'imageshare.js', request, start_response)
    elif path == '/imageshare/upload':
        response_body = std_html('imageshare_upload', request, start_response)
    elif path == '/imageshare/upload_receive':
        response_body = receive_dynamic_image(
            request, start_response, '/imageshare')
    elif path == '/imageshare/ajax_upload_receive':
        response_body = receive_dynamic_image(request, start_response)
    elif path == '/imageshare/image_select':
        response_body = imageshare_select(request, start_response)
    elif path == '/imageshare/image_view':
        response_body = imageshare_view(request, start_response)
    elif path == '/imageshare/image_raw':
        response_body = serve_dynamic_image(request, start_response)
    elif path == '/imageshare/image_markup':
        response_body = get_dynamic_image_markup(request, start_response)
    else:
        # This is not the page you are looking for...
        response_body = serve_404(request, start_response)

    if (path not in ['/image', '/imageshare/image_raw', '/favicon.ico']
        and '/static/images/' not in path):
        response_body = [response_body.encode('utf-8')]

    return response_body

def std_html(page, request, start_response):
    """
    renders a standard page by its name
    for pages which support GET and HEAD requests,
    and meet all others with a 405.
    """
    if request['REQUEST_METHOD'] == 'GET':
        response_body = html.render(''.join([page, ".html"]))
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
                html.render(''.join([page, ".html"]))
                )))
            ]
        )
    else:
        response_body = serve_405(request, start_response)
    return response_body

def imageshare_view(request, start_response):
    """
    renders a standard page by its name
    for pages which support GET and HEAD requests,
    and meet all others with a 405.
    """
    if request['REQUEST_METHOD'] in ['GET', 'HEAD']:
        # parse out the img_id from query
        query = request['query']
        img_id = None
        if 'img_id' in query.keys():
            img_id = query['img_id']
        elif 'special' in query.keys():
            the_image = None
            if query['special'] == 'latest':
                the_image = image.get_latest_image()
            elif query['special'] == 'first':
                the_image = image.get_oldest_image()
            else:
                # invalid query
                the_image = None
            if the_image is not None:
                # grab the image's ID
                img_id = the_image['img_id']
            else:
                # invalid query, pretend we just can't find it
                response_body = serve_404(request, start_response)
                return response_body

        response_body = html.render("imageshare_view.html", {
                'imageid': str(img_id),
                'imagequery': 'img_id=' + str(img_id)
            })
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    else:
        response_body = serve_405(request, start_response)
    if request['REQUEST_METHOD'] == 'HEAD':
        response_body = ''
    return response_body

def imageshare_select(request, start_response):
    """
    serves up a page with all the images on it in thumbnail size
    """

    if request['REQUEST_METHOD'] in ['GET', 'HEAD']:
        # then serve the page normally
        # first go through finding images
        the_image = image.get_latest_image()
        # latest should never fail, because there should always be images
        cur_id = the_image['img_id']
        # start up a table to hold the images
        imagehtml = CRLF.join([
            '<table id="imageTable">',
            '\t<tr>',
            ''
            ])
        imagejs = ''
        # set up some variables
        rowcntr = 0
        # and loop through until the oldest image (should have img_id ~= 1)
        while cur_id > 0:
            # first: check if we need a new row
            if rowcntr >= 5:
                imagehtml += CRLF.join([
                    '\t</tr>',
                    '\t<tr>'
                    ])
                rowcntr = 0
            # if we have an image, add it in...
            if the_image is not None:
                # then add in the html to display it in a table
                imagehtml += CRLF.join([
                    '\t\t<td style="width:105px">',
                    '\t\t\t<a id="imgLink' + str(cur_id) + '" ',
                    '\t\t\t\t'
                    'href="/imageshare/image_view?img_id=' + str(cur_id) + '">',
                    '\t\t\t\t<span id="img' + str(cur_id) + '">Loading...</span>'
                    '\t\t\t</a>',
                    '\t\t</td>'
                    ])
                #TODO add javascript and details for each image
                imagejs += ''.join([
                    '\t\t\tGetImage(' + str(cur_id),
                    ', "img' + str(cur_id) + '", true);',
                    CRLF
                    ])
                rowcntr += 1
            # and go to the next image-id down
            cur_id -= 1
            # and grab it
            the_image = image.get_image(cur_id)
        # after the loop, close off the table
        imagehtml += CRLF.join([
            '\t</tr>',
            '</table>'
            ])
        response_body = html.render('imageshare_select.html',
            {
                'imagehtml': imagehtml,
                'imagejs': imagejs
            })
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    # then remove the body of the response for head requests
    if request['REQUEST_METHOD'] == 'HEAD':
        response_body = ''
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

def serve_static_js(filename, request, start_response):
    """
    Processes a request for a text-file by filename.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    If the image isn't in my static directory, 404 it.
    """

    if request['REQUEST_METHOD'] in ['GET', 'HEAD']:
        response_body = static_files.get_js_file(filename)
        if response_body is not None:
            start_response('200 OK', [
                ('Content-Type', 'text/javascript; charset=utf-8'),
                ('Content-Length', str(len(response_body)))
                ]
            )
        else:
            # if the file couldn't be found, serve a 404
            response_body = serve_404(request, start_response)
    else:
        response_body = serve_405(request, start_response)

    if request['REQUEST_METHOD'] == 'HEAD':
        response_body = ''

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
    # get the file extension (supports multiple extensions)
    filetype = filename.split('.')[-1].lower()
    # convert jpg to 'jpeg' for mimetype compatibility
    if filetype == 'jpg':
        filetype = 'jpeg'
    if filetype == 'ico':
        filetype = 'x-icon'

    if request['REQUEST_METHOD'] == 'GET':
        response_body = static_files.get_image_file(filename)
        if response_body is not None:
            start_response('200 OK', [
                ('Content-Type', 'image/%s' % (filetype)),
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
                ('Content-Type', 'image/%s' % (filetype)),
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

def serve_dynamic_image(request, start_response):
    """
    Processes a request for a dynamic image.
    Uses the query-string to determine what to do.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    If the image isn't in my static directory, 404 it.
    """

    query = request['query']

    # first we need to get the image object from my storage
    the_image = None
    if 'special' in query.keys():
        # we have a special command. What's it say?
        if query['special'] == 'latest':
            # then the command says grab the newest image
            the_image = image.get_latest_image()
        elif query['special'] == 'first':
            # then the command says grab the oldest image
            the_image = image.get_oldest_image()
        else:
            # we have an invalid special command.
            the_image = None
        if the_image is not None:
            # do a redirect to the proper image-id
            img_id = the_image['img_id']
            start_response('307 Temporary Redirect', [
                ('Location', '/imageshare/image_raw?img_id=' + str(img_id))
                ]
            )
            return ''
    elif 'img_id' in query.keys():
        # we have a standard request by ID
        the_image = image.get_image(query['img_id'])
    else:
        # we received an invalid query string.
        the_image = None

    # then we can figure out what to do with the image
    if request['REQUEST_METHOD'] not in ['GET', 'HEAD']:
        # serve a 405
        response_body = serve_405(request, start_response)
    elif the_image is not None:
        # valid method, so start a valid response
        response_body = the_image['data']
        start_response('200 OK', [
            ('Content-Type', ''.join(['image/', the_image['filetype']])),
            ('Content-Length', str(len(response_body)))
            ]
        )
    else:
        # if the file couldn't be found, serve a 404
        response_body = serve_404(request, start_response)

    if request['REQUEST_METHOD'] == 'HEAD':
        # if we've got a head request, return no content
        response_body = ''

    return response_body

def get_dynamic_image_markup(request, start_response):
    """
    Processes a request for a dynamic image's required markup.
    That is: returns an HTML string for the display of a given
    image. Added for TIFF support, which requires different markup
    from everything else.
    Uses the query-string to determine what to do.
    This page supports GET and HEAD requests,
    all others are met with a 405.
    If the image isn't in my static directory, 404 it.
    """

    query = request['query']

    # first we need to get the image object from my storage
    the_image = None
    if 'special' in query.keys():
        # we have a special command. What's it say?
        if query['special'] == 'latest':
            # then the command says grab the newest image
            the_image = image.get_latest_image()
        elif query['special'] == 'first':
            # then the command says grab the oldest image
            the_image = image.get_oldest_image()
        else:
            # we have an invalid special command.
            the_image = None
        if the_image is not None:
            # do a redirect to the proper image-id
            img_id = the_image['img_id']
            thumbs = ""
            if 'thumbs' in query.keys():
                thumbs = "&thumbs=" + query['thumbs']
            start_response('307 Temporary Redirect', [
                ('Location', ''.join([
                    '/imageshare/image_markup?img_id=' + str(img_id) + thumbs
                    ]))
                ]
            )
            return ''
    elif 'img_id' in query.keys():
        # we have a standard request by ID
        the_image = image.get_image(query['img_id'])
    else:
        # we received an invalid query string.
        the_image = None

    # are we serving thumbnails?
    thumbs = (
        True if 'thumbs' in query.keys() and query['thumbs'] == 'true'
        else False
        )

    # then we can figure out what to do with the image
    response_body = ''
    if request['REQUEST_METHOD'] not in ['GET', 'HEAD']:
        # serve a 405
        response_body = serve_405(request, start_response)
    elif the_image is not None:
        # valid method, so start a valid response
        if 'tiff' in the_image['filetype']:
            # TODO dynamic image sizes
            response_body = ''.join([
                ('<embed width=512 height=512' if not thumbs
                    else '<embed width=100 height=100'),
                    ' src="/imageshare/image_raw?' + request['QUERY_STRING'],
                    '" type="' + the_image['filetype'] + '" />'
                ]
            )
        else:
            response_body = ''.join([
                ('<img width="40%" ' if not thumbs
                    else '<img width="100px" '),
                'alt="loading..." ',
                'src="/imageshare/image_raw?',
                request['QUERY_STRING'],
                '" />'
                ]
            )
        start_response('200 OK', [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(response_body)))
            ]
        )
    else:
        # if the file couldn't be found, serve a 404
        response_body = serve_404(request, start_response)

    if request['REQUEST_METHOD'] == 'HEAD':
        # if we've got a head request, return no content
        response_body = ''

    return response_body

def receive_dynamic_image(request, start_response, redirect_to=None):
    """
    Processes upload of a dynamic image.
    Uses the query-string to determine what to do.
    This page supports only POST requests,
    all others are met with a 405.
    """

    if request['REQUEST_METHOD'].upper() != 'POST':
        # serve a 405
        response_body = serve_405(request, start_response)
    else:
        # attempt to store in the image...
        img_id = image.add_image(
            request['content']['file'].filename,
            request['content']['file'].value,
            request['content']['file'].type.split('/')[1])
        # if that worked, we'll have the new image's ID.
        #  If it didn't work, then we'll have None
        if img_id is not None:
            if redirect_to is not None:
                # using 303 - See Other (the proper way to redirect after a POST)
                start_response('303 See Other', [
                    ('Location', redirect_to)
                    ]
                )
                response_body = ''
            else:
                # don't redirect, assume AJAX, send response in JSON
                # TODO add in image information
                response_body = '{"success": "true"}'
                start_response('200 OK', [
                    ('Content-Type', 'application/json'),
                    ('Content-Length', str(len(response_body)))
                    ]
                )
        else:
            if redirect_to is not None:
                # if the file couldn't be found, and we're doing
                # a standard web-request, then serve a 500 (idk what went wrong)
                response_body = 'Unable to add image to the database...'
                start_response('500 Internal Server Error', [
                    ('Content-Type', 'text/html'),
                    ('Content-Length', str(len(response_body)))
                    ]
                )
            else:
                response_body = ' '.join([
                    '{"success": "false",',
                    '"message": "Unable to add image to the database..."}'
                ])
                start_response('500 Internal Server Error', [
                    ('Content-Type', 'application/json'),
                    ('Content-Length', str(len(response_body)))
                    ]
                )

    if request['REQUEST_METHOD'] == 'HEAD':
        # if we've got a head request, return no content
        response_body = ''

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
        [('Allow', ', '.join(allowed))])
    return ''
