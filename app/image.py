"""
Takes care of handling image storage
"""
# TODO use a database; I don't like this in-memory stuff.

from . import static_files

images = {}

def add_image(data):
    """
    Adds an image into my internal storage
    """
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0

    images[image_num] = data
    return image_num

def get_image(id_num):
    """
    Gets an image by its ID
    """
    return images[id_num]

def get_latest_image():
    """
    Grabs the most recently stored image
    """
    image_num = max(images.keys())
    return images[image_num]

add_image(static_files.get_image_file('neuromancer.jpg'))
