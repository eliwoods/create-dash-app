# create-dash-app
***
[![PyPI version](https://badge.fury.io/py/create-dash-app.svg)](https://badge.fury.io/py/create-dash-app)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![Build status](https://github.com/eliwoods/create-dash-app/actions/workflows/test.yml/badge.svg)



**create-dash-app** is a utility for creating a boilerplate [Dash](https://dash.plotly.com/) applications.

## Why?

I made this primarily because I wanted an easy way to initialize a Dash application that logically separates code.

If you're new to Dash, the docs lead you down a design path of single file apps. This may be fine for their simple 
examples, but in the real world your application will quickly grow untenable as you build out more complex views.

I personally have run into this issue at least 2 times, and because I find refactoring to be a tedious chore, 
I decided to build a tool to address it. I even added some other features because I'm just such a nice guy.

## Installing
Installation is simple with `pip` or your preferred package manager.

```sh
python -m pip install create-dash-app
```

To test the installation

```sh
python -m create_dash_app -h
```

## Running
Running is also simple and can be done in one of two ways:

To use the executable:
```sh
create-dash-app
```

To run via python:
```sh
python -m create_dash_app
```

## Structure
The main point of this package is to lay out your new app in a helpful structure, so you might wonder what that is
```markdown
dash_app
├── __init__.py
├── app.py
├── assets
│   ├── dash.min.css
│   └── dbc.min.css
├── callbacks
│   ├── __init__.py
│   └── index.py
├── components
│   ├── __init__.py
│   └── index.py
├── server.py
└── wsgi.py
```

### Root Level Files
`app.py`

Your entrypoint to the Flask development server:
```sh
python dash_app/app.py
```

Typically, you won't have to touch this file.

***
`server.py`

Dash app configuration and cache configuration live here.

***
`wsgi.py`

A clean entrypoint if you run dash via a wsgi server (which you should be doing). For example:
```sh
gunicorn dash_app.wsgi -b :8050
```

### Assets
This folder contains any static assets you want to host. Read [this page](https://dash.plotly.com/dash-enterprise/static-assets)
for more information on the assets folder.

### Callbacks
All of your callback definitions should live here. `callbacks.index` is imported by `app.py` to prevent any circular
dependency issues with the `Dash` object. It also means that if you create additional callback files, you only have
to import them in `index.py` and they will flow through to your app.

### Components
All of your components definitions should live here, with `components.index.Layout` acting as the highest level `Div`.
Similar to the callback directory, if you create additional component files you only need to make their components
children of `Layout`.
