"""
Image-app's SQLite database handler.

Contains all the functions needed to access and store data in the database.

Will use individual connection sockets for each transaction
(to help with future multiprocess/thread support).
"""

import sqlite3

DB_FILE = 'imageapp.sqlite'

# start up a database connection
db = sqlite3.connect(DB_FILE)
# and create the tables on init (if they don't exist)
# image table
db.execute('''
    CREATE TABLE IF NOT EXISTS images
    (
        img_id INTEGER PRIMARY KEY,
        name TEXT,
        filetype TEXT,
        data BLOB,
        added INTEGER DEFAULT CURRENT_TIMESTAMP,
        modified INTEGER DEFAULT CURRENT_TIMESTAMP
    )
    ''')
# ... and its timestamp trigger
db.execute('''
    CREATE TRIGGER IF NOT EXISTS images_mod_trigger
    AFTER UPDATE
    ON images
    FOR EACH ROW
    BEGIN
    UPDATE images SET modified = CURRENT_TIMESTAMP WHERE img_id = old.img_id;
    END
    ''')
db.commit()
db.close()


def add_image(img_name, filetype, data):
    """
    Add an image into the database
    """
    # connect!
    db = sqlite3.connect(DB_FILE)
    db.text_factory = str
    db.row_factory = sqlite3.Row

    # configure to retrieve bytes, not text (shouldn't be needed...)
    # I want text for text objects, this doesn't affect blobs!
    # db.text_factory = bytes

    # get a query handle (or "cursor")
    c = db.cursor()

    # Insert the new image
    c.execute('''
        INSERT INTO images (name, filetype, data) VALUES
        (
            :name,
            :filetype,
            :data
        )
        ''', {'name': img_name, 'filetype': filetype, 'data': data})
    # store the new ID
    new_id = c.lastrowid
    # end connection
    db.commit()
    db.close()
    return new_id

def get_image(img_id):
    """
    Grab an image out of the database by its ID
    """
    # connect!
    db = sqlite3.connect(DB_FILE)
    db.text_factory = str
    db.row_factory = sqlite3.Row

    # get a cursor
    c = db.cursor()

    # select an image by ID
    c.execute('SELECT * FROM images WHERE img_id = :id LIMIT 1',
        {'id': img_id})
    # get it
    row = c.fetchone()
    # get out
    db.commit()
    db.close()
    # go home
    return row

def get_latest_image():
    """
    Grab the newest image from the database
    """
    # Connect!
    db = sqlite3.connect(DB_FILE)
    db.text_factory = str
    db.row_factory = sqlite3.Row

    # get a cursor
    c = db.cursor()

    # select the most recently added image
    c.execute('SELECT * FROM images ORDER BY added DESC LIMIT 1')
    # get it
    row = c.fetchone()
    # get out
    db.commit()
    db.close()
    # go home
    return row

def get_oldest_image():
    """
    Grab the oldest image from the database
    """
    # Connect!
    db = sqlite3.connect(DB_FILE)
    db.text_factory = str
    db.row_factory = sqlite3.Row

    # get a cursor
    c = db.cursor()

    # select the most recently added image
    c.execute('SELECT * FROM images ORDER BY added ASC LIMIT 1')
    # get it
    row = c.fetchone()
    # get out
    db.commit()
    db.close()
    # go home
    return row

def delete_image(img_id):
    """
    Removes a given image from the database by its ID
    """
    # Connect
    db = sqlite3.connect(DB_FILE)
    db.text_factory = str
    db.row_factory = sqlite3.Row

    # get a cursor
    c = db.cursor()

    # delete it
    c.execute('DELETE FROM images WHERE img_id = :id',
        {'id': img_id})
    # and close the coffin
    db.commit()
    db.close()
