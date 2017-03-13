import sys
sys.path.insert(0,'/Users/pdeiml/github/gamma-cat/')
from astropy.table import Table, Row, Column
import gammacat.input
import numpy as np
import os
from astropy.io import ascii
from gammacat.utils import write_yaml, load_yaml

filename = './BiteauWilliams2015_AllData_ASDC_v2016_12_20.ecsv'
self.table = Table.read(filename, format='ascii.ecsv', delimiter='|')