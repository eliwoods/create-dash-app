import create_dash_app.templates.keys as keys

DIR_NAME = 'components'

INDEX_TEMPLATE = f'''\
import dash.dcc
import dash.html as html
import dash_bootstrap_components as dbc


Layout = html.Div(id='main', children=[
    html.p('Welcome to {{{keys.TITLE}}}!'),
])

'''
