APP_TEMPLATE = '''
from {base}.components.main import Layout
from {base}.server import app

# In order for callbacks to work, they must be imported where Dash is instantiated 
# noinspection PyUnresolvedReferences
import {base}.callbacks.main

server = app.server
app.layout = Layout


if __name__ == '__main__':
    app.runserver(debug=True)
    
'''

SERVER_TEMPLATE = '''
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
    title={title},
)
cache = Cache(
    app.server,
    config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': os.path.join({cache_dir}, 'dash-cache'),
    }
)

'''

WSGI_TEMPLATE = '''
# noinspection PyUnresolvedReferences
from {base}.app import server as application

'''
