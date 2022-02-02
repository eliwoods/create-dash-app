from typing import Dict
import logging
import os
import shutil

import templates.assets as assets
import templates.callbacks as callbacks
import templates.components as components
import templates.keys as keys
import templates.root as root

LOG = logging.getLogger(__file__)

DEFAULT_APP_BASE = 'dash_app'
DEFAULT_ROOT_PATH = '.'


class FileGenerator:

    def __init__(self, base: str = DEFAULT_APP_BASE, title: str = DEFAULT_APP_BASE,
                 path: str = DEFAULT_ROOT_PATH, cache: str = DEFAULT_ROOT_PATH):
        self.base = base
        self.title = title
        self.root_path = os.path.abspath(path)
        self.abs_base = os.path.join(self.root_path, self.base)

        if cache == DEFAULT_ROOT_PATH:
            self.cache_path = os.path.abspath(cache)
        else:
            self.cache_path = cache

        self._init_root()

    @staticmethod
    def ensure_dir_exists(path):
        if not os.path.isdir(path):
            LOG.debug(f'Creating directory "{path}"')
            os.makedirs(path)

    def _init_root(self):
        LOG.info(f'Initializing base directory "{self.base}"')
        self.ensure_dir_exists(self.abs_base)

    @property
    def exists(self):
        return os.path.isdir(self.abs_base)

    def generate(self, filename: str, template: str, template_kwargs: Dict[str, str] = None, path: str = None):
        if template_kwargs is None:
            template_kwargs = {}
        if path is None:
            path = ''

        self.ensure_dir_exists(os.path.join(self.abs_base, path))

        rel_filepath = os.path.join(path, filename)
        LOG.debug(f'Generating file "{rel_filepath}"')

        if template and template[0] == '\n':
            template = template[1:]

        with open(os.path.join(self.abs_base, rel_filepath), 'w') as f:
            f.write(template.format(**template_kwargs))

    def generate_init(self, path: str = None):
        self.generate('__init__.py', '', path=path)

    def _kwargs(self, **kwargs) -> Dict[str, str]:
        base_kwargs = {
            keys.BASE: self.base,
            keys.TITLE: self.title,
        }
        base_kwargs.update(**kwargs)
        return base_kwargs

    def generate_root_files(self):
        LOG.info('Generating root files')
        self.generate_init()
        self.generate('server.py', root.APP_TEMPLATE, template_kwargs=self._kwargs())
        self.generate('app.py', root.SERVER_TEMPLATE,
                      template_kwargs=self._kwargs(**{keys.CACHE_PATH: self.cache_path}))
        self.generate('wsgi.py', root.WSGI_TEMPLATE, template_kwargs=self._kwargs())

    def generate_callback_files(self):
        LOG.info('Generating callback files')
        self.generate_init(path=callbacks.DIR_NAME)
        self.generate('index.py', callbacks.INDEX_TEMPLATE, template_kwargs=self._kwargs(), path=callbacks.DIR_NAME)

    def generate_component_files(self):
        LOG.info('Generating component files')
        self.generate_init(path=components.DIR_NAME)
        self.generate('index.py', components.INDEX_TEMPLATE, template_kwargs=self._kwargs(), path=components.DIR_NAME)

    def generate_assets(self):
        LOG.info('Generating asset files')
        assets_path = os.path.join(self.abs_base, assets.DIR_NAME)
        shutil.copytree(assets.SRC_PATH, assets_path)

    def run(self):
        self.generate_root_files()
        self.generate_callback_files()
        self.generate_component_files()
        self.generate_assets()
