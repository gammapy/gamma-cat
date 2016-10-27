import numpy as np
from astropy.table import Table, Column
from astropy.units import cds
import string

def main(a, b):
	## open file


	tab = Table.read(a, format='fits')


	## rename column-names to SED format


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
	index = []
	for i in range(0, len(tab)-1):
	    if tab['paper'][i] != tab['paper'][i+1]:
	       papers.append(tab['paper'][i])
	       index.append(i)
	papers.append(tab['paper'][-1])


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
	print(filenames)


	## seperate by paper and write file


	length = []
	for x in range(0, len(index)):
		if x == 0:
			tab[x:index[x]+1].write(b + '_' + filenames[x]+ '.ecsv', format='ascii.ecsv')
		else:
			tab[index[x-1]+1:index[x]+1].write(b + '_' + filenames[x]+ '.ecsv', format='ascii.ecsv')
	tab[index[-1]+1:].write(b + '_' + filenames[-1]+ '.ecsv', format='ascii.ecsv')

if __name__ == '__main__':
	main()

