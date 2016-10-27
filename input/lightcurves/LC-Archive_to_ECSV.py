import sys
import numpy as np
from astropy.table import Table, Column
from astropy.units import cds
# import base64
import string


## open file


tab = Table.read(sys.argv[1], format='fits')


## rename column-names to SED format


tab.rename_column('mjd_mid_exp', 'time')
tab.rename_column('mjd_start', 'time_min')
tab.rename_column('mjd_end', 'time_max')
tab.rename_column('integral_flux', 'flux')
tab.rename_column('sigma_int_flux_stat', 'flux_err')
tab.rename_column('experiment', 'telescope')
tab.rename_column('reference', 'paper')


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
       # print(tab['paper'][i])
       papers.append(tab['paper'][i])
       index.append(i)
# print(tab['paper'][-1])
papers.append(tab['paper'][-1])
# print(papers)
# print(index)
# print(len(tab))


## convert paper names to safe filename

filenames = []
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
for p in range(0, len(papers)):
	# print(papers[p])
	# filename = str(papers[p])
	filename = ''.join(c for c in papers[p] if c in valid_chars)
	filename = ''.join(filename.split())
	# print(filename)
	filenames.append(filename)
# print(filenames)


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
		# print(tab[x:index[x]+1])
		# length0 = len(tab[0:index[x]+1])
		tab[x:index[x]+1].write(sys.argv[1] + '_' + filenames[x]+ '.ecsv', format='ascii.ecsv')
	else:
		# print(tab[index[x-1]+1:index[x]+1])
		# length.append(len(tab[index[x-1]+1:index[x]+1]))
		tab[index[x-1]+1:index[x]+1].write(sys.argv[1] + '_' + filenames[x]+ '.ecsv', format='ascii.ecsv')
# print(tab[index[-1]+1:])
tab[index[-1]+1:].write(sys.argv[1] + '_' + filenames[-1]+ '.ecsv', format='ascii.ecsv')

# print(papers)
# print(filenames)

# for x in range(0, len(index)):
# 	print(str(papers[x]))

# file_name_string = base64.urlsafe_b64encode(your_string)

# length.append(len(tab[index[-1]+1:]))

# length.append(length0)
# print(length)
# summe = np.sum(length)
# print('N verschiedene Papers: ' + str(len(index)+1))
# print('Differenz: ' + str(summe-len(tab)))
# print(tab[0:index[0]+1])

## write file


# tab.write(sys.argv[2], format='ascii.ecsv')


# hdulist = pyfits.open(sys.argv[1])
# hdulist.info()
# prihdr = hdulist[0].header
# sechdr = hdulist[1].header

# tbdata = hdulist[1].data

# print tbdata.field(0)

# data_rows = [(tbdata.field(0)), (tbdata.field(1)), (tbdata.field(2)), (tbdata.field(4)), (tbdata.field(11)), (tbdata.field(13)))]

# t = Table(rows=data-rows, names=('TIME', 'TIME_MIN', 'TIME_MAX', 'FLUX', 'FLUX_ERR', 'TELESCOPE', 'REFERENCE'), dtype=('f8', 'f8', 'f8', 'f8', 'f8', 'S30', 'S30'))

# t = Table()

# t['TIME'] = Column([(tbdata.field(0)], unit='MJD', dtype='float32')
# t['TIME_MIN'] = Column((tbdata.field(1), unit='MJD', dtype='float32')
# t['TIME_MAX'] = Column((tbdata.field(2), unit='MJD', dtype='float32')
# t['FLUX'] = Column((tbdata.field(3), unit='Crab', dtype='float32')
# t['FLUX_ERR'] = Column((tbdata.field(4), unit='Crab', dtype='float32')
# t['TELESCOPE'] = Column((tbdata.field(11), unit='', dtype='string')
# t['REFERENCE'] = Column((tbdata.field(13), unit='', dtype='string')

# fh = StringIO()
# t.write(fh, format='ascii.ecsv')
# table_string = fh.getvalue()
# print(table_string)

# col1 = pyfits.Column(name='TIME', format='30A', array=tbdata.field(0))
# col2 = pyfits.Column(name='TIME_MIN', format='30A', array=tbdata.field(1))
# col3 = pyfits.Column(name='TIME_MAX', format='30A', array=tbdata.field(2))
# col4 = pyfits.Column(name='FLUX', format='E', array=tbdata.field(3))
# col5 = pyfits.Column(name='FLUX_ERR', format='E', array=tbdata.field(4))
# col6 = pyfits.Column(name='TELESCOPE', format='30A', array=tbdata.field(11))
# col7 = pyfits.Column(name='REFERENCE', format='30A', array=tbdata.field(13))

# cols = pyfits.ColDefs([col1, col2,  col3, col4, col5, col6, col7])

# tbhdu = pyfits.BinTableHDU.from_columns(cols)

# tbhdu.writeto(sys.argv[2])
