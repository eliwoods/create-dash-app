import create_dash_app.templates.keys as keys

DIR_NAME = 'callbacks'

INDEX_TEMPLATE = f'''\
from dash.dependencies import Input, Output

from {{{keys.BASE}}}.server import app

'''
