"""Convert HESS J1018-589A spectrum to the format we need.

Data from here:
https://www.mpi-hd.mpg.de/hfm/HESS/pages/publications/auxiliary/auxinfo_HESSJ1018
"""
from astropy.table import QTable
table = QTable.read('HESS_J1018-589A-original.ecsv', format='ascii.ecsv')
e2 = table['Energy'] ** 2

table2 = QTable()
table2['energy'] = table['Energy']
table2['flux'] = (table['Flux'] / e2).to('cm-2 s-1 TeV-1')
table2['flux_err_hi'] = (table['E_Flux'] / e2).to('cm-2 s-1 TeV-1')
table2['flux_err_lo'] = (table['e_Flux'] / e2).to('cm-2 s-1 TeV-1')

filename = 'HESS_J1018-589A.ascii'
print('Writing {}'.format(filename))
table2.write(filename, format='ascii.fixed_width_no_header', delimiter=' ')
