from __future__ import unicode_literals

import json
import sys
from collections import OrderedDict

import yaml

from jujubundlelib import changeset


def munge(item):
    internals = {}#OrderedDict()
    internals['id'] = item['id']
    internals['args'] = item['args']
    if item['requires']:
        internals['requires'] = map(lambda x: '${}'.format(x), item['requires'])
    return {item['method']: internals}


def main():
    """Dump the changeset objects as JSON, reading the bundle YAML in from
    stdin or a given file.
    """
    source = sys.stdin
    if len(sys.argv) == 2:
        source = open(sys.argv[1])
    bundle = yaml.safe_load(source)
    cs = map(munge, list(changeset.parse(bundle)))
    print yaml.safe_dump(cs, encoding='utf-8', allow_unicode=True)


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

yaml.add_representer(OrderedDict, represent_ordereddict)


if __name__ == '__main__':
    main()
