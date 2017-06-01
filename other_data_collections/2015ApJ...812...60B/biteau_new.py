# author: peter.deiml@fau.de

import sys
sys.path.insert(0,'/Users/pdeiml/github/gamma-cat/')
from astropy.table import Table, Row, Column
import gammacat.input
import numpy as np
import os
from astropy.io import ascii
from gammacat.utils import write_yaml, load_yaml

class Biteau:
	def __init__(self):
		filename = './BiteauWilliams2015_AllData_ASDC_v2016_12_20.ecsv'
		self.sources_def_dir = './../../input/sources/'

		print('Reading: {}'.format(filename))
		self.table = Table.read(filename, format='ascii.ecsv', delimiter='|')

		print('Creating dictionary   common_name & source_id   from files in {}'.format(self.sources_def_dir))
		self.source_map = dict()
		for x in os.listdir(self.sources_def_dir):
			if(x == 'README.md'):
				continue
			else:
				info = gammacat.input.BasicSourceInfo.read(self.sources_def_dir + str(x))
				#source_map = dict(common_name = info.data['common_name'], source_id = info.data['source_id'])
				self.source_map[info.data['common_name']] = info.data['source_id']
		#print(len(self.table))
		#print(len(self.source_map))

	def modify_source_files(self):
		for x in range(0, len(self.table)):
			# Check whether entry 'source' in Biteau catalog matches any common_name in ./../../input/sources
			if (self.table[x]['source'] not in self.source_map):
				print('ERROR: Source {} in Biteau catalog does not match any common_name in {}'.format(self.table[x]['source'], self.sources_def_dir))
			source_id = self.source_map[self.table[x]['source']]
			#print(source_id)
			if(int(source_id) < 10):
				source_def_file_data = load_yaml(self.sources_def_dir + str('tev-00000') + str(source_id) + '.yaml')
			elif(int(source_id) >= 10 and int(source_id) < 100):
				source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(source_id) + '.yaml')
			else:
				source_def_file_data = load_yaml(self.sources_def_dir + str('tev-000') + str(source_id) + '.yaml')

			print('Current for-loop number: {}'.format(x))
			print(source_def_file_data)
			if(!(self.table[x]['experiment'] in source_def_file_data['discoverer'])):
				source_def_file_data['discoverer'] = source_def_file_data['discoverer'] + self.table[x]['experiment']
			if(!(self.table[x]['reference_id'] in source_def_file_data['reference_id'])):
				source_def_file_data['reference_id'] = source_def_file_data['reference_id'] + self.table[x]['reference_id']

if __name__ == '__main__':
	biteau_catalog = Biteau()
	biteau_catalog.modify_source_files()