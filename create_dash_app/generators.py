from typing import Dict, Optional
import logging
import os
import shutil

import create_dash_app.templates.assets as assets
import create_dash_app.templates.callbacks as callbacks
import create_dash_app.templates.components as components
import create_dash_app.templates.keys as keys
import create_dash_app.templates.root as root

LOG = logging.getLogger(__file__)

DEFAULT_APP_BASE = 'dash_app'
DEFAULT_ROOT_PATH = '.'


class DashAppGenerator:

    def __init__(self, base: Optional[str] = DEFAULT_APP_BASE, title: Optional[str] = DEFAULT_APP_BASE,
                 path: Optional[str] = DEFAULT_ROOT_PATH, cache: Optional[str] = DEFAULT_ROOT_PATH) -> None:
        self.base = base
        self.title = title
        self.root_path = os.path.abspath(path)
        self.abs_base = os.path.join(self.root_path, self.base)

        if cache == DEFAULT_ROOT_PATH:
            self.cache_path = os.path.abspath(cache)
        else:
            self.cache_path = cache

    @staticmethod
    def _ensure_dir_exists(path) -> None:
        if not os.path.isdir(path):
            LOG.debug(f'Creating directory "{path}"')
            os.makedirs(path)

    def init_root_dir(self) -> None:
        LOG.info(f'Initializing base directory "{self.base}"')
        self._ensure_dir_exists(self.abs_base)

    @property
    def exists(self) -> bool:
        return os.path.isdir(self.abs_base)

    def _generate(self, filename: str, template: str,
                  template_kwargs: Optional[Dict[str, str]] = None, path: Optional[str] = None) -> None:
        if template_kwargs is None:
            template_kwargs = {}
        if path is None:
            path = ''

        self._ensure_dir_exists(os.path.join(self.abs_base, path))

        rel_filepath = os.path.join(path, filename)
        LOG.debug(f'Generating file {os.path.join(self.abs_base, rel_filepath)}')

        with open(os.path.join(self.abs_base, rel_filepath), 'w') as f:
            f.write(template.format(**template_kwargs))

    def _generate_init(self, path: Optional[str] = None) -> None:
        self._generate('__init__.py', '', path=path)

    def _kwargs(self, **kwargs: str) -> Dict[str, str]:
        base_kwargs = {
            keys.BASE: self.base,
            keys.TITLE: self.title,
        }
        base_kwargs.update(**kwargs)
        return base_kwargs

    def generate_root_files(self) -> None:
        LOG.info('Generating root files')
        self._generate_init()
        self._generate('server.py', root.APP_TEMPLATE, template_kwargs=self._kwargs())
        self._generate('app.py', root.SERVER_TEMPLATE,
                       template_kwargs=self._kwargs(**{keys.CACHE_PATH: self.cache_path}))
        self._generate('wsgi.py', root.WSGI_TEMPLATE, template_kwargs=self._kwargs())

    def generate_callback_files(self) -> None:
        LOG.info('Generating callback files')
        self._generate_init(path=callbacks.DIR_NAME)
        self._generate('index.py', callbacks.INDEX_TEMPLATE, template_kwargs=self._kwargs(), path=callbacks.DIR_NAME)

    def generate_component_files(self) -> None:
        LOG.info('Generating component files')
        self._generate_init(path=components.DIR_NAME)
        self._generate('index.py', components.INDEX_TEMPLATE, template_kwargs=self._kwargs(), path=components.DIR_NAME)

    def generate_assets(self) -> None:
        LOG.info('Generating asset files')
        assets_path = os.path.join(self.abs_base, assets.DIR_NAME)
        if os.path.isdir(assets_path):
            LOG.debug(f'Deleting existing assets dir {assets_path}')
            shutil.rmtree(assets_path)
        shutil.copytree(assets.SRC_PATH, assets_path)

    def run(self):
        self.init_root_dir()
        self.generate_root_files()
        self.generate_callback_files()
        self.generate_component_files()
        self.generate_assets()
