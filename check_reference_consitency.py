from astropy.table import Table as t
import os
from gammacat.utils import load_yaml

rootdir = './input/data'
sourcedir = './input/sources'
source_def_refs = dict()
gammacat_refs = dict()

filenames = ['empty']
for root, dirs, files in os.walk(rootdir, topdown=False):
    for name in files:
        filepath = os.path.join(root,name)
        replaced_filepath = filepath.replace('%26A', '&')
        filenames.append(os.path.join(root,name))
filenames.pop(0)

source_def_files = ['empty']
for root, dirs, files in os.walk(sourcedir, topdown=False):
    for name in files:
        source_def_files.append(os.path.join(root,name))
source_def_files.pop(0)
#print(source_def_files)

for source_def_file in source_def_files:
    if(source_def_file[len(source_def_file)-4:len(source_def_file)] == 'yaml'):
        data = load_yaml(source_def_file)
        source_def_refs[data['source_id']] = data['reference_ids']
# print(source_def_refs)

for file in filenames:
    if(file[len(file)-4:len(file)] == 'yaml'):
        gammacat_refs[load_yaml(file)['source_id']] = []
    if(file[len(file)-4:len(file)] == 'ecsv'):
        table = t.read(file, format='ascii.ecsv', delimiter=' ')
        gammacat_refs[table.meta['source_id']] = []

for file in filenames:
    if(file[len(file)-4:len(file)] == 'yaml'):
        if(load_yaml(file)['reference_id'] in gammacat_refs[load_yaml(file)['source_id']]):
            continue
        else:
            gammacat_refs[load_yaml(file)['source_id']].append(load_yaml(file)['reference_id'])
    if(file[len(file)-4:len(file)] == 'ecsv'):
        table=t.read(file, format='ascii.ecsv', delimiter=' ')
        if(table.meta['reference_id'] in gammacat_refs[table.meta['source_id']]):
            continue
        else:
            gammacat_refs[table.meta['source_id']].append(table.meta['reference_id'])

print('References in gammacat')
print(gammacat_refs)
print('References in /input/sources')
print(source_def_refs)

# print(len(gammacat_refs))
# print(len(source_def_refs))

# print('Hallo')
# print(gammacat_refs)
# print('Hallohallo')
# print(source_def_refs)

# references['key1'] = 'Hallo1'
# references['key1'].append('Hallo2')
# print(references)
# for file in filenames:
#     if(file[len(file)-4:len(file)] == 'yaml'):
#         references[load_yaml(file)['source_id']] = []
#     if(file[len(file)-4:len(file)] == 'ecsv'):
#         print(file)
#         table = t.read(file, format='ascii.ecsv', delimiter=' ')
#         references[table.meta['source_id']] = []
# print(references)
# for file in filenames:
#     print(file[len(file)-10:len(file)]

# filenameyaml = './input/data/2014/2014ApJ...780..168A/tev-000030-2.yaml'
# data = load_yaml(filenameyaml)
# print(data)
# print(data['source_id'])

# table = t.read(filename, format='ascii.ecsv', delimiter= ' ')
# print(table)
# print(table.meta)
# reference = table.meta['reference_id']
# source_id = table.meta['source_id']
# print(reference)
# print(source_id)