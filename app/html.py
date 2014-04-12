"""
Abstracts the html templating/rendering engine,
in case I decide to use another someday.
"""

# TODO class? I don't like these globals...

import os
import jinja2

template_dir = './templates'
loader = None
env = None

def init_templates():
    """
    initializes the template engine
    """
    global loader, env

    # calculate the location of the templates directory relative to the
    # directory this file is in
    dirname = os.path.dirname(__file__)
    t_dir = os.path.join(dirname, template_dir)
    t_dir = os.path.abspath(t_dir)

    print 'loading templates from:', t_dir

    loader = jinja2.FileSystemLoader(t_dir)
    env = jinja2.Environment(loader=loader)

def render(template_name, values=None):
    """
    render the given template with any of the given value, if they exist
    """
    if values is None:
        values = {}
    template = env.get_template(template_name)
    return template.render(values)

def escape(string):
    """
    Escapes strings to make them safe for URI use
    """
    return jinja2.escape(string)

# and auto-load the template env
init_templates()
