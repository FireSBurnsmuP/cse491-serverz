import os
import os.path
import mimetypes
import traceback
import random
import time
import datetime
import cgi

class Message(object):
    """
    class for storing messages in a chat context
    """
    def __init__(self, timestamp, user, message):
        self.timestamp = timestamp
        self.user = user
        self.message = message

class ChatApp(object):
    """
    the wsgi app implementation of a chat application
    """
    def __init__(self, files_path):
        self.file_server = FileServer(files_path)
        self.messages = []

    def get_messages_since(self, timestamp):
        """Retrieve any messages received since the given timestamp."""
        msgs = []
        for msg in self.messages:
            if msg.timestamp > timestamp:
                msgs.append(msg)

        return msgs

    def format_response(self, new_messages, timestamp):
        """
        decides how to format a response,
        based on the messages since the given time(stamp)
        """
        xml_msgs = []
        for msg in new_messages:
            xml_msgs.append("\n".join([
                "<message>",
                "<author>%s</author>" % (msg.user),
                "<text>%s</text>" % (msg.message),
                "<time>%s</time>" % (msg.timestamp),
                "</message>"
            ]))

        # new messages received?
        if xml_msgs:
            # yes
            status = 1
        else:
            status = 2                     # no new messages

        xml = "\n".join([
                "<?xml version=\"1.0\"?>",
                "<response>",
                "<status>%d</status>" % status,
                "<timestamp>%f</timestamp>" % timestamp,
                "".join(xml_msgs),
                "</response>"
            ])

        return xml

    def __call__(self, environ, start_response):
        url = environ['PATH_INFO']
        if url == '/get_messages':
            # last_time
            form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
            print form.keys()
            last_time = float(form['last_time'].value)

            new_messages = self.get_messages_since(last_time)
            xml = self.format_response(new_messages, time.time())

            # done; return whatever we've got.
            start_response("200 OK", [('Content-type', 'text/html')])

            print xml
            return [xml]
        elif url == '/post_message':
            form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
            print form.keys()

            # retrieve submitted data
            last_time = float(form['last_time'].value)
            author = form['user'].value
            message = form['message'].value

            # create and add new message:
            timestamp = time.time()
            msg = Message(timestamp, author, message)
            self.messages.append(msg)

            # return any new messages:
            new_messages = self.get_messages_since(last_time)
            xml = self.format_response(new_messages, timestamp)

            # done; return whatever we've got.
            start_response("200 OK", [('Content-type', 'text/html')])

            print xml
            return [xml]

        # by default, just return a file
        return self.file_server(environ, start_response)

class FileServer(object):
    """
    The chat app's file server
    """
    def __init__(self,path):
        self.path = os.path.abspath(path)

    def __call__(self, environ, start_response):
        url = environ['PATH_INFO']

        print 'url:' + url
        if url.endswith('/'):
            url += 'index.html'

        fullpath = self.path + url
        fullpath = os.path.abspath(fullpath)
        assert fullpath.startswith(self.path)

        extension = mimetypes.guess_type(fullpath)
        extension = extension[0]

        if extension is None:
            extension = 'text/plain'

        status = '200 OK'
        headers = [('Content-type', extension)]

        try:
            fp = open(fullpath)
            contents = fp.read()
            start_response(status, headers)
            return [contents]
        except:
            status = '404 Not Found'
            headers = [('Content-type', 'text/html')]
            start_response(status, headers)
            return ['404 Not Found']
