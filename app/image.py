"""
Takes care of handling image storage
"""
# TODO use a database; I don't like this in-memory stuff.

from . import static_files
from . import sqldb

# images = {}

def add_image(filename, data, filetype='jpeg'):
    """
    Adds an image into my internal storage
    """
    # adjust some filetypes...
    if filetype == 'jpg':
        filetype = 'jpeg'
    # and add the image in the database
    image_num = sqldb.add_image(filename, filetype, data)
    # then return the new ID number
    return image_num

def get_image(id_num):
    """
    Gets an image by its ID
    Returns None if an image by that ID doesn't exist
    """
    return sqldb.get_image(id_num)

def get_latest_image():
    """
    Grabs the most recently stored image
    """
    return sqldb.get_latest_image()

def get_oldest_image():
    """
    Grabs the first image stored
    """
    return sqldb.get_oldest_image()

# add in the initial image on load
temp = get_latest_image()
if temp is None:
    add_image('neuromancer',
        static_files.get_image_file('neuromancer.jpg'), 'jpeg')
