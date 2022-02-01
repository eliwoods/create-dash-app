from abc import ABC, abstractmethod
from typing import Dict
import logging
import os

LOG = logging.getLogger(__file__)


DEFAULT_ROOT_DIR = 'dash_app'
DEFAULT_ROOT_PATH = '.'


class FileGenerator:

    def __init__(self, root_path: str = '.', root_dir: str = DEFAULT_ROOT_DIR, file_suffix: str = None) -> None:
        self.root_path = os.path.abspath(root_path)
        self.root_dir = os.path.join(self.root_path, root_dir)
        self.file_suffix = file_suffix
        if not file_suffix.startswith('.'):
            self.file_suffix = f'.{self.file_suffix}'

        self._init_root()

    def _init_root(self):
        if not os.path.isdir(self.root_dir):
            LOG.info(f'Initializing root directory "{self.root_dir}"')
            os.makedirs(self.root_dir)

    def generate(self, name: str, template: str, template_kwargs: Dict[str, str], path: str = None) -> None:
        """
        Generates the file
        :param name:
        :param template:
        :param template_kwargs:
        :param path:
        :return:
        """
        if path is None:
            path = ''
        filename = f'{name}{self.file_suffix}'
        rel_filepath = os.path.join(path, filename)
        LOG.info(f'Generating file "{rel_filepath}"')

        with open(os.path.join(self.root_dir, rel_filepath), 'w') as f:
            f.write(template.format(**template_kwargs))
