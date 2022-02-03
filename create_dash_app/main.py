from argparse import ArgumentParser
from typing import Dict
import logging

from rich.logging import RichHandler

from create_dash_app.generators import DashAppGenerator, DEFAULT_ROOT_PATH, DEFAULT_APP_BASE

LOG = logging.getLogger(__file__)


def parse_args() -> Dict[str, str]:
    parser = ArgumentParser()
    parser.add_argument('--base', '-b', default=DEFAULT_APP_BASE, help='Set the name of the dash app')
    parser.add_argument('--path', '-p', default=DEFAULT_ROOT_PATH, help='Set the path the app is built in')
    parser.add_argument('--title', '-t', default=DEFAULT_APP_BASE, help='Set the title of the dash app')
    parser.add_argument('--cache', '-c', default=DEFAULT_ROOT_PATH, help='Set the path the cache is built in')
    parser.add_argument('--force', '-f', action='store_true', help='Force the overwriting of an existing dash app')
    args = parser.parse_args()
    return args.__dict__


def parse_continue() -> bool:
    raw = input('>> ')
    parsed = None
    if raw.lower() == 'y' or raw.lower() == 'yes' or raw == '':
        parsed = True
    if raw.lower() == 'n' or raw.lower() == 'no':
        parsed = False

    return parsed


def main() -> None:
    cli_args = parse_args()
    logging.basicConfig(
        level='NOTSET', format='%(message)s', datefmt='[%X]', handlers=[RichHandler()]
    )
    LOG.debug('Configured logging')
    force = cli_args.pop('force')

    gen = DashAppGenerator(**cli_args)
    if gen.exists and not force:
        LOG.warning(f'The application "{gen.base}" already exists and may be overwritten. '
                    f'Do you want to continue [Y/n]?')
        cont = parse_continue()

        while cont is None:
            LOG.warning('Unable to parse response. Do you want to continue [Y/n]?')
            cont = parse_continue()

        if not cont:
            LOG.info('Exiting')
            return

    gen.run()


if __name__ == '__main__':
    main()
