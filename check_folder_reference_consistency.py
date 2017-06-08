from astropy.table import Table as t
import os
from gammacat.utils import load_yaml

datadir = './input/data'
filenames = ['empty']

# Filling filenames with file pathes of ./input/data
for root, dirs, files in os.walk(datadir, topdown=False):
    for name in files:
        filepath = os.path.join(root,name)
        filenames.append(filepath)
filenames.pop(0)

# Check for consistency between filename and source_id given in the file
for file in filenames:
    if(file[len(file)-4:len(file)] == 'yaml'):
        pathlist = file.split('/')
        data = load_yaml(file)
        src_id_filename = pathlist[len(pathlist)-1].split('.')[0].split('-')
        if(src_id_filename[0] == 'tev'):
            if(not(int(src_id_filename[1]) == data['source_id'])):
                print('WARNING: Name of {} not consistent with source_id in it!'.format(file))
    if(file[len(file)-4:len(file)] == 'ecsv'):
        pathlist = file.split('/')
        data = t.read(file, format='ascii.ecsv', delimiter=' ')
        src_id_filename = pathlist[len(pathlist)-1].split('-') 
        if(src_id_filename[0] == 'tev'):
            if(not( int(src_id_filename[1]) == data.meta['source_id'])):
                print('WARNING: Name of {} not consistent with source_id in it!'.format(file))

# Check for consistency between name of folder and reference_id in the files
for file in filenames:
    if(file[len(file)-4:len(file)] == 'yaml'):
        pathlist = file.split('/')
        data = load_yaml(file)
        folder_reference = pathlist[4].replace('%26','&')
        src_id_filename = pathlist[len(pathlist)-1].split('-')
        if(src_id_filename[0] == 'tev'):
            if(not(folder_reference == data['reference_id'])):
                print('WARNING: Name of folder of {} not consistent with reference_id in it!'.format(file))
    if(file[len(file)-4:len(file)] == 'ecsv'):
        pathlist = file.split('/')
        data = t.read(file, format='ascii.ecsv', delimiter=' ')
        folder_reference = pathlist[4].replace('%26','&')
        src_id_filename = pathlist[len(pathlist)-1].split('-')
        if(src_id_filename[0] == 'tev'):
            if(not(folder_reference == data.meta['reference_id'])):
                print('WARNING: Name of folder of {} not consistens with reference_id in it!'.format(file))