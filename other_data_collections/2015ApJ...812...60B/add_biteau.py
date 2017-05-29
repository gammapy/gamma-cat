
from astropy.table import Table
import biteau

path = '/home/hpc/caph/mppi019h/github/gamma-cat/other_data_collections/2015ApJ...812...60B/'
filename = 'BiteauWilliams2015_AllData_ASDC_v2016_12_20.ecsv'

table = Table.read(filename, format='ascii.ecsv', delimiter='|')
# print(table['source'][550])
biteau.adapt_source_names(table)

# new_table = Table(names=('e_ref', 'dnde', 'dnde_errn', 'dnde_errp', 'note', 'experiment', 'reference_id', 'source'), dtype=('float32', 'float32', 'float32', 'float32', 'S10', 'S8', 'S19', 'S20'))

# new_table.meta = table.meta

# for i in range(0, 736):
#     new_table.add_row((4.135667662E-27*table[i]['freq'], table[i]['e2dnde']/1.6022, table[i]['e2dnde_errn']/1.6022, table[i]['e2dnde_errp']/1.6022, str(table[i]['note'], 'utf-8'), table[i]['experiment'], table[i]['reference_id'], table[i]['source']))
# biteau.adapt_source_names(new_table)

# new_table.write('Relevant_Biteau_Data.ecsv', format='ascii.ecsv', delimiter=' ')

filecounter = 7
# note = '2011'
experiment = 'HESS'
reference_id = '2005A&A...430..865A'
source = 'PKS 2155-304'
source_id = '000147'
mjdstart = 52931.

# biteau.create_escv1(table, filecounter, experiment, reference_id, source, source_id, mjdstart)
# biteau.create_escv2(table, experiment, reference_id, source, source_id, mjdstart)
biteau.create_escv3(table, experiment, reference_id, source, source_id, mjdstart, filecounter)