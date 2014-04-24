"""
Takes care of handling image storage
"""
# TODO use a database; I don't like this in-memory stuff.

from . import static_files

images = {}

def add_image(data, filetype='jpeg'):
    """
    Adds an image into my internal storage
    """
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0

    if filetype == 'jpg':
        filetype = 'jpeg'

    images[image_num] = {'data': data, 'filetype': filetype}
    return image_num

def get_image(id_num):
    """
    Gets an image by its ID
    Returns None if an image by that ID doesn't exist
    """
    if id_num in images.keys():
        return images[id_num]
    else:
        return None

def get_latest_image():
    """
    Grabs the most recently stored image
    """
    image_num = max(images.keys())
    return images[image_num]

def get_oldest_image():
    """
    Grabs the first image stored
    """
    image_num = min(images.keys())
    return images[image_num]

# add in the initial image on load
add_image(static_files.get_image_file('neuromancer.jpg'), 'jpeg')
