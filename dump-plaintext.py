from __future__ import unicode_literals

import json
import sys

import yaml

from jujubundlelib import changeset


command_map = {
    'addCharm': 'add the charm',
    'deploy': 'add the service',
    'addMachines': 'add a machine',
    'addUnit': 'add a unit',
    'addRelation': 'add a relation',
}

args_map = {
    'addCharm': lambda x: x[0],
    'deploy': lambda x: '"{}" using charm {}{}'.format(
        x[1], x[0], ' and config {}'.format(json.dumps(x[2])) if x[2] else ''),
    'addMachines': json.dumps,
    'addUnit': json.dumps,
    'addRelation': lambda x: 'between {}:{} and {}:{}'.format(
        x[0][0], x[0][1]['name'], x[1][0], x[1][1]['name']),
}



def main():
    """Dump the changeset objects as JSON, reading the bundle YAML in from
    stdin or a given file.
    """
    source = sys.stdin
    if len(sys.argv) == 2:
        source = open(sys.argv[1])
    bundle = yaml.safe_load(source)
    for change in changeset.parse(bundle):
        print '{method} {args}{requires} and call it "{id}"'.format(
            method=command_map[change['method']],
            id=change['id'],
            args=args_map[change['method']](change['args']),
            requires=' requiring {}'.format(', '.join(change['requires'])) if \
                change['requires'] else '',
        )


if __name__ == '__main__':
    main()
