from astropy.table import Table

def adapt_source_names(table):
    for i in range(0, len(table)):
        if(table['source'][i] == 'IC310'):
            table['source'][i] = 'IC 310'
        elif(table['source'][i] == 'Mkn421'):
            table['source'][i] = 'Markarian 421'
        elif(table['source'][i] == 'Mkn501'):
            table['source'][i] = 'Markarian 501'
        elif(table['source'][i] == '1ES2344+514'):
            table['source'][i] = '1ES 2344+514'
        elif(table['source'][i] == 'Mkn180'):
            table['source'][i] = 'Markarian 180'
        elif(table['source'][i] == '1ES1959+650'):
            table['source'][i] = '1ES 1959+650'
        elif(table['source'][i] == 'BLLac'):
            table['source'][i] = 'BL Lacertae'
        elif(table['source'][i] == 'PKS2005-489'):
            table['source'][i] = 'PKS 2005-489'
        elif(table['source'][i] == 'RGBJ0152+017'):
            table['source'][i] = 'RGB J0152+017'
        elif(table['source'][i] == 'SHBLJ001355.9-185406'):
            table['source'][i] = 'SHBL J001355.9-185406'
        elif(table['source'][i] == 'Wcomae'):
            table['source'][i] = 'W Comae'
        elif(table['source'][i] == '1ES1312-423'):
            table['source'][i] = '1ES 1312-423'
        elif(table['source'][i] == 'VERJ0521+211'):
            table['source'][i] = 'RGB J0521+212' 
        elif(table['source'][i] == 'PKS2155-304'):
            table['source'][i] = 'PKS 2155-304'
        elif(table['source'][i] == 'B32247+381'):
            table['source'][i] = 'B3 2247+381'
        elif(table['source'][i] == 'RGBJ0710+591'):
            table['source'][i] = 'RGB J0710+591'
        elif(table['source'][i] == 'H1426+428'):
            table['source'][i] = 'H 1426+428'
        elif(table['source'][i] == '1ES0806+524'):
            table['source'][i] = '1ES 0806+524'
        elif(table['source'][i] == '1ES0229+200'):
            table['source'][i] = '1ES 0229+200' 
        elif(table['source'][i] == '1RXSJ101015.9-311909'):
            table['source'][i] = '1RXS J101015.9-311909'
        elif(table['source'][i] == 'H2356-309'):
            table['source'][i] = 'H 2356-309'
        elif(table['source'][i] == 'RXJ0648.7+1516'):
            table['source'][i] = 'RX J0648.7+1516'
        elif(table['source'][i] == '1ES1218+304'):
            table['source'][i] = '1ES 1218+304'
        elif(table['source'][i] == '1ES1101-232'):
            table['source'][i] = '1ES 1101-232'
        elif(table['source'][i] == '1ES0347-121'):
            table['source'][i] = '1ES 0347-121'
        elif(table['source'][i] == 'RBS0413'):
            table['source'][i] = 'RBS 0413'
        elif(table['source'][i] == '1ES1011+496'):
            table['source'][i] = '1ES 1011+496'
        elif(table['source'][i] == '1ES1215+303'):
            table['source'][i] = '1ES 1215+303' 
        elif(table['source'][i] == 'S50716+714'):
            table['source'][i] = 'S5 0716+714'
        elif(table['source'][i] == 'PKS0301-243'):
            table['source'][i] = 'PKS 0301-243'
        elif(table['source'][i] == '1ES0414+009'):
            table['source'][i] = '1ES 0414+009'
        elif(table['source'][i] == '3C66A'):
            table['source'][i] = '3C 66A'
        elif(table['source'][i] == 'PKS0447-439'):
            table['source'][i] = 'PKS 0447-439'
        elif(table['source'][i] == 'PKS1510-089'):
            table['source'][i] = 'PKS 1510-089'
        elif(table['source'][i] == 'PKS1222+21'):
            table['source'][i] = 'PKS 1222+216'
        elif(table['source'][i] == 'PG1553+113'):
            table['source'][i] = 'PG 1553+113'
        elif(table['source'][i] == '3C279'):
            table['source'][i] = '3C 279'
        elif(table['source'][i] == 'PKS1424+240'):
            table['source'][i] = 'PKS 1424+240'

def create_escv1(table, filecounter, note, experiment, reference_id, source, source_id):
    new_table = Table(names=('e_ref', 'dnde', 'dnde_errn', 'dnde_errp'), dtype=('float32', 'float32', 'float32', 'float32'))

    new_table.meta = table.meta

    print('arguments of function:')
    print(source)
    print(reference_id)
    print('{} \n'.format(experiment))
    print('Biteau Catalog (For debug):')
    print(table['source'][13])
    print(table['reference_id'][13])
    print('{} \n'.format(table['experiment'][13]))

    
    for i in range(0, len(table)):
        if((table['source'][i]==source) and (table['note'][i]==note) and (table['reference_id'][i] == reference_id) and (table['experiment'][i] == experiment)):
            new_table.add_row((4.135667662E-27*table[i]['freq'], table[i]['e2dnde']/1.6022, table[i]['e2dnde_errn']/1.6022, table[i]['e2dnde_errp']/1.6022))
    if(filecounter!=0):
        filename='tev-' + str(source_id) + '-sed-' + str(filecounter) + '.ecsv'
    else:
        filename='tev-' + str(source_id) + '-sed.ecsv'
    if(experiment == 'MAGIC'):
        new_table.meta['telescope'] = 'magic'
    elif(experiment == 'CAT'):
        new_table.meta['telescope'] = 'cat'
    elif(experiment == 'HEGRA'):
        new_table.meta['telescope'] = 'hegra'
    elif(experiment == 'TIBET'):
        new_table.meta['telescope'] = 'tibet'
    elif(experiment == 'HESS'):
        new_table.meta['telescope'] = 'hess'
    elif(experiment == 'TACTIC'):
        new_table.meta['telescope'] = 'tactic'
    elif(experiment == 'ARGO-YBJ'):
        new_table.meta['telescope'] = 'argo'
    elif(experiment == 'VERITAS'):
        new_table.meta['telescope'] = 'veritas'
    elif(experiment == 'Whipple'):
        new_table.meta['telescope'] = 'whipple'
    new_table.meta.pop('author')
    new_table.meta.pop('dataset_reference')
    new_table.meta.pop('creation_date')
    new_table.meta['filecounter'] = filecounter
    new_table.meta['source_id'] = int(source_id)
    new_table.meta['reference_id'] = reference_id
    new_table.meta['note'] = note
    new_table.meta['data_type'] = 'sed'
    print('Length of table: {}'.format(len(new_table)))
    new_table.write(filename, format='ascii.ecsv', delimiter=' ')

def create_escv2(table, experiment, reference_id, source, source_id, start):
    new_table = Table(names=('e_ref', 'dnde', 'dnde_errn', 'dnde_errp'), dtype=('float32', 'float32', 'float32', 'float32'))

    new_table.meta = table.meta

    print('arguments of function:')
    print(source)
    print(reference_id)
    print(experiment)
    print(start)
    print('\n')
    print('Biteau Catalog (For debug):')
    print(table['source'][440])
    print(table['reference_id'][440])
    print('{} \n'.format(table['experiment'][440]))
    print(table['mjd_start'][440])

    for i in range(0, len(table)):
        if((table['source'][i]==source) and (table['mjd_start'][i] == start) and (table['reference_id'][i] == reference_id) and (table['experiment'][i] == experiment)):
            # The constant 4.135667662E-27 is the Planck constant in eV*s
            # The constant 1.6022 arises when erg is transformed into TeV
            new_table.add_row((4.135667662E-27*table[i]['freq'], table[i]['e2dnde']/1.6022, table[i]['e2dnde_errn']/1.6022, table[i]['e2dnde_errp']/1.6022))
        filename='tev-' + str(source_id) + '-sed.ecsv'
    if(experiment == 'MAGIC'):
        new_table.meta['telescope'] = 'magic'
    elif(experiment == 'CAT'):
        new_table.meta['telescope'] = 'cat'
    elif(experiment == 'HEGRA'):
        new_table.meta['telescope'] = 'hegra'
    elif(experiment == 'TIBET'):
        new_table.meta['telescope'] = 'tibet'
    elif(experiment == 'HESS'):
        new_table.meta['telescope'] = 'hess'
    elif(experiment == 'TACTIC'):
        new_table.meta['telescope'] = 'tactic'
    elif(experiment == 'ARGO-YBJ'):
        new_table.meta['telescope'] = 'argo'
    elif(experiment == 'VERITAS'):
        new_table.meta['telescope'] = 'veritas'
    elif(experiment == 'Whipple'):
        new_table.meta['telescope'] = 'whipple'
    new_table.meta.pop('author')
    new_table.meta.pop('dataset_reference')
    new_table.meta.pop('creation_date')
    new_table.meta['source_id'] = int(source_id)
    new_table.meta['reference_id'] = reference_id
    new_table.meta['data_type'] = 'sed'
    print('Length of table: {}'.format(len(new_table)))
    new_table.write(filename, format='ascii.ecsv', delimiter=' ')

def create_escv3(table, experiment, reference_id, source, source_id, start, filecounter):
    new_table = Table(names=('e_ref', 'dnde', 'dnde_errn', 'dnde_errp'), dtype=('float32', 'float32', 'float32', 'float32'))

    new_table.meta = table.meta

    print('arguments of function:')
    print(source)
    print(reference_id)
    print(experiment)
    print(start)
    print('\n')
    print('Biteau Catalog (For debug):')
    print(table['source'][440])
    print(table['reference_id'][440])
    print('{} \n'.format(table['experiment'][440]))
    print(table['mjd_start'][440])

    for i in range(0, len(table)):
        if((table['source'][i]==source) and (table['mjd_start'][i] == start) and (table['reference_id'][i] == reference_id) and (table['experiment'][i] == experiment)):
            # The constant 4.135667662E-27 is the Planck constant in eV*s
            # The constant 1.6022 arises when erg is transformed into TeV
            new_table.add_row((4.135667662E-27*table[i]['freq'], table[i]['e2dnde']/1.6022, table[i]['e2dnde_errn']/1.6022, table[i]['e2dnde_errp']/1.6022))
    if(filecounter!=0):
        filename='tev-' + str(source_id) + '-sed-' + str(filecounter) + '.ecsv'
    else:
        filename='tev-' + str(source_id) + '-sed.ecsv'
    if(experiment == 'MAGIC'):
        new_table.meta['telescope'] = 'magic'
    elif(experiment == 'CAT'):
        new_table.meta['telescope'] = 'cat'
    elif(experiment == 'HEGRA'):
        new_table.meta['telescope'] = 'hegra'
    elif(experiment == 'TIBET'):
        new_table.meta['telescope'] = 'tibet'
    elif(experiment == 'HESS'):
        new_table.meta['telescope'] = 'hess'
    elif(experiment == 'TACTIC'):
        new_table.meta['telescope'] = 'tactic'
    elif(experiment == 'ARGO-YBJ'):
        new_table.meta['telescope'] = 'argo'
    elif(experiment == 'VERITAS'):
        new_table.meta['telescope'] = 'veritas'
    elif(experiment == 'Whipple'):
        new_table.meta['telescope'] = 'whipple'
    new_table.meta.pop('author')
    new_table.meta.pop('dataset_reference')
    new_table.meta.pop('creation_date')
    new_table.meta['source_id'] = int(source_id)
    new_table.meta['reference_id'] = reference_id
    new_table.meta['data_type'] = 'sed'
    new_table.meta['filecounter'] = filecounter
    print('Length of table: {}'.format(len(new_table)))
    new_table.write(filename, format='ascii.ecsv', delimiter=' ')