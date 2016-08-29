import numpy as np
import yaml
from collections import OrderedDict
from astropy.table import Table


def yaml_make_ordereddict_work():
    """
    Teach YAML how to work with OrderedDict.

    http://stackoverflow.com/a/21048064/498873
    """
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

    def dict_representer(dumper, data):
        return dumper.represent_dict(data.items())

    def dict_constructor(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    yaml.add_representer(OrderedDict, dict_representer)
    yaml.add_constructor(_mapping_tag, dict_constructor)


def table_to_list_of_dict(table):
    """Convert table to list of dict."""
    rows = []
    for row in table:
        data = OrderedDict()
        for name in table.colnames:
            val = row[name]
            if isinstance(val, np.int64):
                val = int(val)
            elif isinstance(val, np.bool_):
                val = bool(val)
            elif isinstance(val, np.float):
                val = float(val)
            elif isinstance(val, np.str):
                val = str(val)
            else:
                raise ValueError('Unknown type: {} {}'.format(val, type(val)))
            data[name] = val

        rows.append(data)

    return rows


def main():
    filename = 'tgevcat.ecsv'
    print('Reading {}'.format(filename))
    table = Table.read(filename, format='ascii.ecsv')

    data = table_to_list_of_dict(table)

    filename = 'tgevcat.yaml'
    print('Writing {}'.format(filename))
    with open(filename, 'w') as fh:
        yaml.dump(data, fh, default_flow_style=False)


if __name__ == '__main__':
    yaml_make_ordereddict_work()
    main()
