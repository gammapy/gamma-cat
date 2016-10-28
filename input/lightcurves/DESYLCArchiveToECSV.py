import numpy as np
from astropy.table import Table, Column
from astropy.units import cds
import string

def main(a, b):
	"""This function dumps the FITS files defined in Get_FITS_from_DESY-LC-Archive.py in ECSV follwoing 'source-id_paper-id.ecsv'
	"""


	## open file


	tab = Table.read(a, format='fits')


	## rename column-names to lightcurve-format


	tab.rename_column('mjd_mid_exp', 'time')
	tab.rename_column('mjd_start', 'time_min')
	tab.rename_column('mjd_end', 'time_max')
	tab.rename_column('integral_flux', 'flux')
	tab.rename_column('sigma_int_flux_stat', 'flux_err')
	# column 6: tab.rename_column('sigma_int_flux_stat', '')
	# column 7: tab.rename_column('alpha', '')
	# column 8: tab.rename_column('sigma_aplha_stat', '')
	# column 9: tab.rename_column('sigma_alpha_sys', '')
	# column 10: tab.rename_column('e_thr', '')
	# column 11: tab.rename_column('e_cut', '')
	tab.rename_column('experiment', 'telescope')
	# column 13: tab.rename_column('duration', '')
	tab.rename_column('reference', 'paper')
	# column 15: tab.rename_column('fflag', '')
	# print(tab['telescope'][-12:-1])
	# print(tab['paper'][-12:-1])
	
	
	## delete unused columns
	
	
	del tab['sigma_int_flux_sys']
	del tab['alpha']
	del tab['sigma_alpha_stat']
	del tab['sigma_alpha_sys']
	del tab['e_thr']
	del tab['e_cut']
	del tab['duration']
	del tab['fflag']
	
	
	## set formats
	
	
	tab.replace_column('time', tab['time'].astype(float))
	tab.replace_column('time_min', tab['time_min'].astype(float))
	tab.replace_column('time_max', tab['time_max'].astype(float))
	
	
	## set units
	
	
	tab['time'].unit = tab['time_max'].unit = tab['time_min'].unit = cds.MJD
	tab['flux'].unit = tab['flux_err'].unit = cds.Crab
	
	
	## find different papers
	
	
	papers = []
	# index = []
	index = [0]
	for i in range(0, len(tab)-1):
		if tab['paper'][i] != tab['paper'][i+1]:
			papers.append(tab['paper'][i])
			index.append(i+1)
	papers.append(tab['paper'][-1])


	## find multiple telescopes used in a single paper


	telescopes_list = []
	for p in  range(0, len(papers)-1):
		telescope_paper = tab['telescope'][index[p]:index[p+1]-1].pformat()
		telescope = set([t for t in telescope_paper if telescope_paper.count(t) > 1])
		# print(telescope)
		telescopes_list.append(telescope)
	telescope_paper = tab['telescope'][index[-1]:].pformat()
	telescope = set([t for t in telescope_paper if telescope_paper.count(t) > 1])
	telescopes_list.append(telescope)
	
	
	## get only proper names for that telescopes
	
	
	telescopes = []
	for s in telescopes_list:
	    # print(", ".join(str(e) for e in s))
	    telescope = ", ".join(str(e) for e in s)
	    telescopes.append(telescope)
	# print(telescopes)
	# print(len(telescopes))
	
	
	## convert paper names to safe filename
	
	
	filenames = []
	valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	for p in range(0, len(papers)):
		filename = ''.join(c for c in papers[p] if c in valid_chars)
		filename = ''.join(filename.split())
		filenames.append(filename)
	
	
	## add an index if paper names double, i.e. "reference empty"
	
	
	first_index = 1
	second_index = 2
	for f in range(0, len(filenames)):
		for g in range(0, len(filenames)):
			if filenames[f] == filenames[g]:
				if f != g:
					filenames[f] = ''.join(filenames[f] + '_' + str(second_index))
					filenames[g] = ''.join(filenames[g] + '_' + str(first_index))
					first_index = first_index + 2
					second_index = second_index + 2
				else:
					break
	# print('Filenames: ')
	# print(len(filenames))
	
	
	## seperate by paper, set metadata
	
	
	tables = []
	for x in range(0, len(index)-1):
		table = tab[index[x]:index[x+1]]
		table.meta['source_id'] = str(b)
		table.meta['telescope'] = ''.join(str(telescopes[x]).split())
		table.meta['paper_id'] = str(papers[x])
		del table['telescope']
		del table['paper']
		tables.append(table)
	table = tab[index[-1]+1:]
	table.meta['source_id'] = str(b)
	table.meta['telescope'] = ''.join(str(telescopes[-1]).split())
	table.meta['paper_id'] = str(papers[x])
	del table['telescope']
	del table['paper']
	tables.append(table)
	# print(tab)
	# print(tables)
	# print('Tabellen: ')
	# print(len(tables))
	# print('Papers: ')
	# print(len(papers))
	
	
	## write files
	
	
	for x in range(0, len(tables)):
		tables[x].write(b + '_' + filenames[x]+ '.ecsv', format='ascii.ecsv')
	
	
	
if __name__ == '__main__':
	main()

