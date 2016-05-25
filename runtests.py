# -*- coding: utf-8 -*-

import os
import sys
import getpass
import argparse

import django
from django.conf import settings
from django.test.utils import get_runner


DEFAULT_DBNAME = 'test_janyson'
DEFAULT_HOST = '/var/run/postgresql'
DEFAULT_PORT = 5432
DEFAULT_USERNAME = getpass.getuser()


parser = argparse.ArgumentParser(
    description='Django JanySON TestRunner',
    add_help=False,
)
parser.add_argument(
    '--help',
    action='help',
    help='show this help message and exit',
)
parser.add_argument(
    '-d', '--dbname',
    default=DEFAULT_DBNAME,
    help='test database name (default: "{}")'.format(DEFAULT_DBNAME),
)
parser.add_argument(
    '-h', '--host',
    metavar='HOSTNAME',
    default=DEFAULT_HOST,
    help='database server host or socket directory (default: "{}")'.format(
        DEFAULT_HOST),
)
parser.add_argument(
    '-p', '--port',
    type=int,
    default=DEFAULT_PORT,
    help='database server port (default: "{}")'.format(DEFAULT_PORT),
)
parser.add_argument(
    '-U', '--username',
    default=DEFAULT_USERNAME,
    help='database user name (default: "{}")'.format(DEFAULT_USERNAME),
)
parser.add_argument(
    '-P', '--password',
    help='database user password',
)
parser.add_argument(
    '-w', '--no-password',
    action='store_true',
    help='never prompt for password',
)
args = parser.parse_args()

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
django.setup()

if args.password:
    password = args.password
elif not args.no_password:
    password = getpass.getpass()
else:
    password = ''

db_settings = settings.DATABASES['default']
db_settings['TEST']['NAME'] = args.dbname
db_settings['HOST'] = args.host
db_settings['PORT'] = args.port
db_settings['USER'] = args.username
db_settings['PASSWORD'] = password
test_runner = get_runner(settings)()
failures = test_runner.run_tests(['tests'])
sys.exit(bool(failures))
