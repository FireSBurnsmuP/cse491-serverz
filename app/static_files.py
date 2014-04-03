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

def get_image_file(image_filename):
    """
    Get a given static image's bytes
    """
    file_obj = open(''.join([
        get_static_dir(), "/images/", image_filename
        ]), "rb")
    image = file_obj.read()
    file_obj.close()
    return image

def get_text_file(file_filename):
    """
    Get a given static text-file
    """
    file_obj = open(''.join([
        get_static_dir(), "/text/", file_filename
        ]), "rb")
    the_file = file_obj.read()
    file_obj.close()
    return the_file
