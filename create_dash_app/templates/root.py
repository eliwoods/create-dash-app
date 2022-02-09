import create_dash_app.templates.keys as keys

APP_TEMPLATE = f'''\
from {{{keys.BASE}}}.components.index import Layout
from {{{keys.BASE}}}.server import app

# In order for callbacks to work, they must be imported where Dash is instantiated
# noinspection PyUnresolvedReferences
import {{{keys.BASE}}}.callbacks.index

server = app.server
app.layout = Layout


if __name__ == '__main__':
    app.runserver(debug=True)

'''

SERVER_TEMPLATE = f'''\
import os

from flask_cache import Cache
import dash
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG,
    ],
    # Dash throws exceptions about callbacks from components that might be not loaded yet if
    # elements like Tabs are used. These alerts are annoying so suppress them.
    suppress_callback_exceptions=True,
    title='{{{keys.TITLE}}}',
)
cache = Cache(
    app.server,
    config={{{{
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': os.path.join('{{{keys.CACHE_PATH}}}', 'dash-cache'),
    }}}}
)

'''

WSGI_TEMPLATE = f'''\
# noinspection PyUnresolvedReferences
from {{{keys.BASE}}}.app import server as application

'''
