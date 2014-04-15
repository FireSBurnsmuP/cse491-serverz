"""
Allows me easy access to the files in the 'static' files folders
"""

import os

rel_static_dir = './static'

def get_static_dir():
    """
    calculates the static directory's full path.
    """
    global rel_static_dir

    # calculate the location of the static directory relative to the
    # directory this file is in
    dirname = os.path.dirname(__file__)
    t_dir = os.path.join(dirname, rel_static_dir)
    return os.path.abspath(t_dir)

def get_image_file(filename):
    """
    Get a given static image's bytes
    """
    return _get_raw_file(filename, '/images/')

def get_text_file(filename):
    """
    Get a given static text-file by filename.
    """
    return _get_raw_file(filename, '/text/')

def get_js_file(filename):
    """
    Get a given static text-file by filename.
    """
    return _get_raw_file(filename, '/js/')

def _get_raw_file(filename, directory):
    """
    Get a raw file from a given directory
    Internal use function.
    Returns either the file in a string,
    or None if something went wrong
    """
    try:
        # First calc our path.
        path = ''.join([get_static_dir(), directory, filename])
        # Remove any accidental double-slashes...
        if '//' in path:
            # unix...
            path = path.replace('//', '')
        if '\\\\' in path:
            # & windows.
            path = path.replace('\\\\', '')

        # TODO: whitespace escaping win & nix

        # grab the file object...
        file_obj = open(path, "rb")
        # read it in...
        the_file = file_obj.read()
        # close it...
        file_obj.close()
        # and return its contents.
        return the_file
    except:
        # If something went wrong, return None.
        # This will most notably occur when the file doesn't exist.
        return None
