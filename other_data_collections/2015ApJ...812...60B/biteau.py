# author: peter.deiml@fau.de

import sys
sys.path.insert(0,'/Users/pdeiml/github/gamma-cat/')
from astropy.table import Table, Row, Column
import gammacat.input
import numpy as np
import os
from astropy.io import ascii
from gammacat.utils import write_yaml, load_yaml

class BiteauMaker:
	def __init__(self):
		filename = './BiteauWilliams2015_AllData_ASDC_v2016_12_20.ecsv'
		self.sources_def_dir = './../../input/sources/'

		print('Reading: {}'.format(filename))
		self.table = Table.read(filename, format='ascii.ecsv', delimiter='|')
		self.source_ids = Table()

	def basic_infos(self):
		self.table.info('attributes')
		print(self.table)

	def get_source_ids(self):
		print(self.source_ids)
		rows = []
		for x in os.listdir(self.sources_def_dir):
			if(x == 'README.md'):
				continue
			else:
				info = gammacat.input.BasicSourceInfo.read(self.sources_def_dir + str(x))
				row_to_add = dict(common_name = info.data['common_name'], source_id = info.data['source_id'])
				rows.append(row_to_add)
		self.source_ids = Table(rows=rows)
		#print(self.source_ids)

	def get_row(self, x):
		row = self.table[x]
		return row

	def get_source_info(self, type):
		if(type == 'source'):
			array_of_source_names = []
			for x in range (0, 736):
				row = self.get_row(x)
				name = row['source']
				if(x != 0):
					if(array_of_source_names[len(array_of_source_names) - 1] == name):
						continue
					else:
						array_of_source_names.append(name)
				else:
					array_of_source_names.append(name)
			return array_of_source_names
		elif(type=='reference_id'):
			array_of_reference_ids = []
			for x in range(0,736):
				row = self.get_row(x)
				reference_id = row['reference_id']
				if(x != 0):
					if(array_of_reference_ids[len(array_of_reference_ids)-1] == reference_id):
						continue
					else:
						array_of_reference_ids.append(reference_id)
				else:
					array_of_reference_ids.append(reference_id)
			return array_of_reference_ids

	def make_ecsv_files(self, source_names):
		print(source_names)
		for x in source_names:
			reference_ids = ["placeholder"]
			for y in range(0, 736):
				if(self.table[y]['source'] == x):
					if(reference_ids[len(reference_ids)-1] == self.table[y]['reference_id']):
						continue
					else:
						reference_ids.append(self.table[y]['reference_id'])
			reference_ids.pop(0)
			for y in reference_ids:
				observer = ["placeholder"]

			#for y in reference_ids:
		#		note = ["placeholder"]
		#		for z in range(0,736):
		#			if(self.table[z]['reference_id'] == y):
		#				if(note[len(note)-1] == self.table[z]['note']):
		#					continue
		#				elif(self.table[z]['note'] = ""):
		#					continue
		#				else:
		#					note.append(self.table[z]['note'])
		#		note.pop(0)
				print('Step1')
		#		print(note)
				filecounter = 0
				for a in note:
					energy = []
					dnde_e2= []
					dnde = []
					dnde_errp = []
					dnde_errn = []
					#TODO: Optional write function that fills the sed_lists
					for z in range(0, 736):
						if(self.table[z]['source'] == x and self.table[z]['reference_id'] == y):
							energy.append((self.table[z]['freq']*4.135667662E-27))		#energy [TeV]
							dnde_e2.append((self.table[z]['e2dnde']/1.602176565))	#energy^2*dnde [TeV cm-2 s-1]
							dnde_errp.append((self.table[z]['e2dnde_errp']/1.602176565))	#dnde_errp [TeV cm-2 s-1]
							dnde_errn.append((self.table[z]['e2dnde_errn']/1.602176565))	#dnde_errn [TeV cm-2 s-1]
						else:
							continue
							
					#print('Current source is {}'.format(x))
					#print('Size of dnde_e2 for source {}: {}'.format(x, len(dnde_e2)))
					#print('Size of dnde_errp for source {}: {}'.format(x, len(dnde_errp)))
					#print('Size of dnde_errn for source {}: {}'.format(x, len(dnde_errn)))
					#print('Size of energy for source {}: {}'.format(x, len(energy)))
					
					for z in range(0, len(dnde_e2)):
						dnde.append((dnde_e2[z])/(energy[z] * energy[z]))	#dnde [TeV-1 s-1 cm-2]
					
					#print('Energy for source {}:'.format(x))
					#print(energy)
					#print('Spectrum times e2 for source {}:'.format(x))
					#print(dnde_e2)
					#print('dnde_errp:')
					#print(dnde_errp)
					#print('dnde_errn:')
					#print(dnde_errn)
					#print('Spectrum for source {}:'.format(x))
					#print(dnde)
					
					year = y[:4]
					dir_path = '../../input/data/' + str(year) + '/' + str(y) + '/'
					dir_path = dir_path.replace('&','%26')
					print(dir_path)
					#file_name_with_rel_path = dir_path + str(y) + 
					#print(dir_path)
					try:
						os.stat(dir_path)
					except:
						os.mkdir(dir_path)
					#Creating the table for the ecsv-file
					t = Table()
					#print('Size of dnde_e2 for source {}: {}'.format(x, len(dnde_e2)))
					#print('Size of dnde_errp for source {}: {}'.format(x, len(dnde_errp)))
					#print('Size of dnde_errn for source {}: {}'.format(x, len(dnde_errn)))
					#print('Size of energy for source {}: {}'.format(x, len(energy)))
					#print('Size of energy_err for source{}: {}'.format(x, len(energy_err)))
					#print('Size of dnde for source{}: {}'.format(x, len(dnde)))
					t = Table([energy, dnde, dnde_errn, dnde_errp], names=['e_ref', 'dnde', 'dnde_errn', 'dnde_errp'])
					#specification of units
					t['e_ref'].unit = 'TeV'
					t['dnde'].unit = 'TeV-1 s-1 cm-2'
					t['dnde_errn'].unit = 'TeV-1 s-1 cm-2'
					t['dnde_errp'].unit = 'TeV-1 s-1 cm-2'
						#specification of datatype
					t['e_ref'].datatype = 'float32'
					t['dnde'].datatype = 'float32'
					t['dnde_errn'].datatype = 'float32'
					t['dnde_errp'].datatype = 'float32'
					#Adding meta data to the tabel
					t.meta['data_type'] = 'sed'
					t.meta['filecounter'] = filecounter
					t.meta['state'] = note
					t.meta['reference_id'] = y
					print('Making ecsv_file and source_def file for source {}'.format(x))
					self.make_ecsv_yaml_files(x, t, y, dir_path, filecounter)
					filecounter = filecounter + 1

	def make_ecsv_yaml_files(self, biteau_name, sed_table, biteau_reference_id, ecsv_path, filecounter):
		table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
		print('Step1')
		if biteau_name in table_lookup_dict: 
			pass
		else:
			print('ERROR: Source name of Biteau {} is not defined in the definition files!', format(biteau_name))
		#for x in range(1,164):		#to make sure that names in Biteau catalog are equal to common_names in source_def_yaml_files

		sed_table.meta['source_id'] = str(table_lookup_dict[biteau_name])
		#if (int(sed_table.meta['source_id']) < 10):
		#	source_def_file_data = load_yaml(self.sources_def_dir + str('tev-00000') + str(table_lookup_dict[def_file_name]))

	"""
	def make_ecsv_yaml_files(self, biteau_name, sed_table, biteau_reference_id, ecsv_path, filecounter):
		#In case of source IC 310
		if(biteau_name == 'IC310'):
			def_file_name = 'IC 310'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of source Mrk 421
		elif(biteau_name == 'Mkn421'):
			def_file_name = 'Markarian 421'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of source Mrk 501
		elif(biteau_name == 'Mkn501'):
			def_file_name = 'Markarian 501'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of source 1ES 2344+514
		elif(biteau_name == '1ES2344+514'):
			def_file_name = '1ES 2344+514'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of source Mrk 180
		elif(biteau_name == 'Mkn180'):
			def_file_name = 'Markarian 180'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of source 1ES 1959+650
		elif(biteau_name == '1ES1959+650'):
			def_file_name = '1ES 1959+650'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of BL Lacertae
		elif(biteau_name == 'BLLac'):
			def_file_name = 'BL Lacertae'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of PKS 2005-489
		elif(biteau_name == 'PKS2005-489'):
			def_file_name = 'PKS 2005-489'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of RGB J0152+017
		elif(biteau_name == 'RGBJ0152+017'):
			def_file_name = 'RGB J0152+017'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-00000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-00000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-00000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-00000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-00000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of SHBL J001355.9-185406
		elif(biteau_name == 'SHBLJ001355.9-185406'):
			def_file_name = 'SHBL J001355.9-185406'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-00000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-00000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-00000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-00000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-00000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of W Comae
		elif(biteau_name == 'WComae'):
			def_file_name = 'W Comae'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 1ES 1312-423
		elif(biteau_name == '1ES1312-423'):
			def_file_name = '1ES 1312-423'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of RGB J0521+212
		elif(biteau_name == 'VERJ0521+211'):
			def_file_name = 'RGB J0521+212'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of RGB J0710+591
		elif(biteau_name == 'RGBJ0710+591'):
			def_file_name = 'RGB J0710+591'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of PKS 2155-304
		elif(biteau_name == 'PKS2155-304'):
			def_file_name = 'PKS 2155-304'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of B3 2247+381
		elif(biteau_name == 'B32247+381'):
			def_file_name = 'B3 2247+381'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of H 1426+428
		elif(biteau_name == 'H1426+428'):
			def_file_name = 'H 1426+428'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 1ES 0806+524
		elif(biteau_name == '1ES0806+524'):
			def_file_name = '1ES 0806+524'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 1ES 0229+200
		elif(biteau_name == '1ES0229+200'):
			def_file_name = '1ES 0229+200'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 1RXS J101015.9-311909
		elif(biteau_name == '1RXSJ101015.9-311909'):
			def_file_name = '1RXS J101015.9-311909'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of H 2356-309
		elif(biteau_name == 'H2356-309'):
			def_file_name = 'H 2356-309'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of RX J0648.7+1516
		elif(biteau_name == 'RX J0648.7+1516'):
			def_file_name = 'RXJ0648.7+1516'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 1ES 1218+304
		elif(biteau_name == '1ES1218+304'):
			def_file_name = '1ES 1218+304'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 1ES 1101-232
		elif(biteau_name == '1ES1101-232'):
			def_file_name = '1ES 1101-232'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 1ES 0347-121
		elif(biteau_name == '1ES0347-121'):
			def_file_name = '1ES 0347-121'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of RBS 0413
		elif(biteau_name == 'RBS0413'):
			def_file_name = 'RBS 0413'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 1ES 1011+496
		elif(biteau_name == '1ES1011+496'):
			def_file_name = '1ES 1011+496'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 1ES 1215+303
		elif(biteau_name == '1ES1215+303'):
			def_file_name = '1ES 1215+303'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of S5 0716+714
		elif(biteau_name == 'S50716+714'):
			def_file_name = 'S5 0716+714'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of PKS 0301-243
		elif(biteau_name == 'PKS0301-243'):
			def_file_name = 'PKS 0301-243'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 1ES 0414+009
		elif(biteau_name == '1ES0414+009'):
			def_file_name = '1ES 0414+009'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 3C 66A
		elif(biteau_name == '3C66A'):
			def_file_name = '3C 66A'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of PKS 0447-439
		elif(biteau_name == 'PKS0447-439'):
			def_file_name = 'PKS 0447-439'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of PKS 1510-089
		elif(biteau_name == 'PKS1510-089'):
			def_file_name = 'PKS 1510-089'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of PKS 1222+216
		elif(biteau_name == 'PKS1222+216'):
			def_file_name = 'PKS 1222+216'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of PG 1553+113
		elif(biteau_name == 'PG1553+113'):
			def_file_name = 'PG 1553+113'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of 3C 279
		elif(biteau_name == '3C279'):
			def_file_name = '3C 279'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')

		#In case of PKS 1424+240
		elif(biteau_name == 'PKS1424+240'):
			def_file_name = 'PKS 1424+240'
			table_lookup_dict = dict(zip(self.source_ids['common_name'], self.source_ids['source_id']))
			sed_table.meta['source_id'] = str(table_lookup_dict[def_file_name])
			source_def_file_data = load_yaml(self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			for a in source_def_file_data['reference_ids']:
				if(a==biteau_reference_id):
					continue
				else:
					reference_to_add = [biteau_reference_id]
					source_def_file_data['reference_ids'] == source_def_file_data['reference_ids'] + reference_to_add
				print('Write source_definition file: ' + self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
				write_yaml(source_def_file_data, self.sources_def_dir + str('tev-0000') + str(table_lookup_dict[def_file_name]) +'.yaml')
			sed_table.meta['reference_id'] = str(biteau_reference_id)
			print('Write sed.ecsv file: ' + ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv')
			sed_table.write(ecsv_path + 'tev-0000' + str(table_lookup_dict[def_file_name]) + '-sed.ecsv', format = 'ascii.ecsv')
	"""
if __name__ == '__main__':
	maker = BiteauMaker()
	maker.get_source_ids()
	#maker.basic_infos()
	test = maker.get_source_info('source')
	#test2 = maker.get_source_info('reference_id')
	maker.make_ecsv_files(test)