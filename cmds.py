import argparse
import logging
import os
import sys

from utils import Spinner

log = logging.getLogger('spinner')


def create(**kw):
    spinner = Spinner(**kw)
    instance = spinner.create()
    log.info('Created instance: %s' % instance.id)
    spinner.wait_for(instance, 'running')
    spinner.setup(instance)


def setup(instance_id, **kw):
    spinner = Spinner(**kw)
    instances = spinner.find_running()
    for instance in instances:
        if instance_id == instance.id:
            spinner.setup(instance)


def setup_logging(level):
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter())
    console.setLevel(level)
    root = logging.getLogger()
    root.addHandler(console)
    root.setLevel(level)


if __name__ == '__main__':
    pem = os.path.expanduser('~/.aws/spinner-app.pem')

    parser = argparse.ArgumentParser()
    parser.add_argument('action')
    parser.add_argument('--v', action='store_true')
    parser.add_argument('--instance_id', nargs='?', default='')
    parser.add_argument('--instance_type', nargs='?', default='ami-99bef1a9')
    parser.add_argument('--key_name', nargs='?', default='spinner-app')
    parser.add_argument('--security_group', nargs='?', default='spinner-app')
    parser.add_argument('--region', nargs='?', default='us-west-2')
    parser.add_argument('--pem', nargs='?', default=pem)
    args = parser.parse_args()

    kw = dict(args._get_kwargs())
    for k in ['action', 'instance_id', 'v']:
        del kw[k]

    setup_logging(logging.DEBUG if args.v else logging.INFO)
    logging.getLogger("boto").propagate = False
    logging.getLogger("paramiko.transport").propagate = False

    if args.action == 'create':
        create(**kw)

    if args.action == 'setup':
        if not args.instance_id:
            print 'Instance id must be specified.'
            sys.exit()
        setup(args.instance_id, **kw)
