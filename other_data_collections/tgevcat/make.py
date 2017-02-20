import yaml
from astropy.table import Table

from gammacat.utils import table_to_list_of_dict, yaml_make_ordereddict_work


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
