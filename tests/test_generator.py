from unittest import TestCase
from tempfile import TemporaryDirectory
from typing import List, Dict, Union
import os

from create_dash_app.generators import DashAppGenerator


# TODO(ew) write test that runs the dash app
class GeneratorTests(TestCase):

    def test_root_exists(self):
        """
        Test the app is built in the right place
        """
        with TemporaryDirectory() as _dir:
            gen = DashAppGenerator(path=_dir, cache=_dir)
            gen.run()

            self.assertTrue(os.path.isdir(gen.abs_base))

    @staticmethod
    def get_tree_dict(path: str) -> List[Dict[str, Union[str, List[str]]]]:
        """
        Parses the paths file tree into a list of dictionaries
        """
        output = []
        for root, dirs, files in os.walk(path):
            root_name = root.split('/')[-1]
            output.append({
                'root': root_name,
                'dirs': dirs,
                'files': files,
            })

        return output

    @property
    def true_tree(self) -> List[Dict[str, Union[str, List[str]]]]:
        return [
            {
                'root': 'dash_app',
                'dirs': ['callbacks', 'components', 'assets'],
                'files': ['server.py', '__init__.py', 'app.py', 'wsgi.py'],
            },
            {
                'root': 'callbacks',
                'dirs': [],
                'files': ['index.py', '__init__.py'],
            },
            {
                'root': 'components',
                'dirs': [],
                'files': ['index.py', '__init__.py'],
            },
            {
                'root': 'assets',
                'dirs': [],
                'files': ['dbc.min.css', 'dash.min.css'],
            },
        ]

    def test_file_tree(self):
        with TemporaryDirectory() as _dir:
            gen = DashAppGenerator(path=_dir, cache=_dir)
            gen.run()

            gen_tree = self.get_tree_dict(gen.abs_base)
            self.assertListEqual(gen_tree, self.true_tree)
