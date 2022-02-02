from argparse import ArgumentParser
from typing import Dict
import logging
import logging.config

from generators import FileGenerator, DEFAULT_ROOT_PATH, DEFAULT_APP_BASE

LOG = logging.getLogger(__file__)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s | %(levelname)s | %(processName)s %(name)s:%(lineno)d | %(message)s',
        },
    },
    'handlers': {
        'console': {
            'formatter': 'standard',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
}


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


# TODO(ew) we still are prompted to continue even if folder doesn't exist
def main():
    kwargs = parse_args()
    logging.config.dictConfig(LOGGING_CONFIG)
    LOG.debug('Configured logging')
    force = kwargs.pop('force')

    gen = FileGenerator(**kwargs)
    if gen.exists and not force:
        LOG.info(f'The application "{gen.base}" already exists. Do you want to continue [Y/n]?')
        cont = parse_continue()

        while cont is None:
            LOG.info('Unable to parse response. Do you want to continue [Y/n]?')
            cont = parse_continue()

        if not cont:
            LOG.info('Exiting build')

    gen.run()


if __name__ == '__main__':
    main()
