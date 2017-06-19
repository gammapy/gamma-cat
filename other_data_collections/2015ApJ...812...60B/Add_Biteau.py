# This script reads in Biteau's catalog stored in 
# BiteauWilliams2015_AllData_ASDC_v2016_12_20.ecsv,
# it creates the corresponding ecsv-sed files and stores
# them in /input/data

from astropy.table import Table
from astropy.io import ascii
from astropy.constants import h,e
from pathlib import Path
import astropy.units as u
import numpy as nump
import os
import glob

class Biteau:
    fBiteauFile = './BiteauWilliams2015_AllData_ASDC_v2016_12_20.ecsv'
    fBiteauSourceIDFile = './Biteau_Sources.txt'
    fBiteauExperimentFile = './Biteau_Experiments.txt'
    fInputDataPath = './../../input/data/'

    def __init__(self):
        self.fBiteauCatalog = self.Load_Catalog(self.fBiteauFile)
        self.fBiteauSources = self.Load_SourceIDs(self.fBiteauSourceIDFile)
        self.fBiteauExperiments = self.Load_Experiments(self.fBiteauExperimentFile)

# Load_Catalog reads Biteau's catalog
    def Load_Catalog(self, filename):
        print('Reading {}'.format(filename))
        biteau_catalog = Table.read(filename, format = 'ascii.ecsv', delimiter='|')
        return biteau_catalog

# Load_SourceIDs read Biteau_Sources.txt in which all sources which are mentioned in
# Biteau's catalog and the corresponding source_id are stored
    def Load_SourceIDs(self, filename):
        biteau_sources = dict()
        print('Reading {}'.format(filename))
        data = ascii.read(filename)
        for i in range(0, len(data)):
            biteau_sources[data[i][0]] = data[i][1]
        return biteau_sources

# Load_Experiments read Biteau_Experiments.txt in which all sources which are mentioned in
# Biteau's catalog and the corresponding telescope from /input/schemas are stored
    def Load_Experiments(self, filename):
        biteau_experiments = dict()
        print('Reading {}'.format(filename))
        data = ascii.read(filename)
        for i in range(0, len(data)):
            biteau_experiments[data[i][0]] = data[i][1]
        return biteau_experiments

# Rename_Experiment renames all source names in Biteau's catalog into the corresponding name
# in /input/schemas
    def Rename_Experiment(self, experiment):
        return self.fBiteauExperiments[experiment]

# Calculate_Energy transforms the 'freq'-column in Biteau's catalog into an energy-column 
    def Calculate_Energy(self, frequency):
        energy = (h*frequency*1/u.second)/e.si * 1E-9* u.teraelectronvolt/u.joule*u.coulomb
        return energy

# Calculate_dnde transforms the 'e2dnde'-column in Biteau's catalog into an dnde-column
    def Calculate_dnde(self, energy, e2dnde):
        dnde = 1/((energy*u.teraelectronvolt)**2)*e2dnde*1/e.si*1E-16*u.erg*1/((u.centimeter)**2)/u.second*u.teraelectronvolt/u.erg
        return dnde

# Create_Subtables splits up Biteau's catalog into the single data sets and stores these sets 
# in a list which contains astropy tables
    def Create_Subtables(self):
        subtables = []
        subtable = Table(names=('source_id', 'e_ref', 'dnde', 'dnde_errn', \
        'dnde_errp', 'mjd_start', 'mjd_stop', 'telescope', 'reference_id'),\
        dtype=('int32', 'float32', 'float32', 'float32', 'float32', \
        'float32', 'float32', 'S8', 'S19'))

        for i in range(0, len(self.fBiteauCatalog)):
            
            # The i-th row of Biteau's catalog is extracted as a list
            row_to_add = [nump.int64(self.fBiteauSources[self.fBiteauCatalog['source'][i]]), \
            self.Calculate_Energy(self.fBiteauCatalog['freq'][i]), \
            self.Calculate_dnde(self.Calculate_Energy(self.fBiteauCatalog['freq'][i]), self.fBiteauCatalog['e2dnde'][i]), \
            self.Calculate_dnde(self.Calculate_Energy(self.fBiteauCatalog['freq'][i]), self.fBiteauCatalog['e2dnde_errn'][i]), \
            self.Calculate_dnde(self.Calculate_Energy(self.fBiteauCatalog['freq'][i]), self.fBiteauCatalog['e2dnde_errp'][i]), \
            self.fBiteauCatalog['mjd_start'][i], self.fBiteauCatalog['mjd_stop'][i], \
            self.Rename_Experiment(self.fBiteauCatalog['experiment'][i]), \
            self.fBiteauCatalog['reference_id'][i]]

            if i==0:
                subtable.add_row(row_to_add)
            else: 
                # Checking whether the source, mjd_start, mjd_stop, experiment or reference_id changes in Biteau's catalog
                if((self.fBiteauSources[self.fBiteauCatalog['source'][i]] == subtable[len(subtable)-1]['source_id']) and
                    (self.fBiteauCatalog['mjd_start'][i] == subtable[len(subtable)-1]['mjd_start']) and \
                    (self.fBiteauCatalog['mjd_stop'][i] == subtable[len(subtable)-1]['mjd_stop']) and \
                    (self.Rename_Experiment(self.fBiteauCatalog['experiment'][i]) == (subtable[len(subtable)-1]['telescope']).decode()) and \
                    (self.fBiteauCatalog['reference_id'][i] == (subtable[len(subtable)-1]['reference_id']).decode())):
                    subtable.add_row(row_to_add)
                else:
                    subtables.append(subtable)
                    subtable=Table(names=('source_id', 'e_ref', 'dnde', 'dnde_errn', \
                    'dnde_errp', 'mjd_start', 'mjd_stop', 'telescope', 'reference_id'),\
                    dtype=('int32', 'float32', 'float32', 'float32', 'float32', \
                    'float32', 'float32', 'S8', 'S19'))
                    subtable.add_row(row_to_add)
        return subtables

# Create_Folders creates the non-existing folders in /input/data which are mentioned in Biteau's catalog
    def Create_Folders(self, subtables):
        for i in range(0, len(subtables)):
            folder = ((subtables[i]['reference_id'][0]).decode()).replace('&', '%26')
            year = ((subtables[i]['reference_id'][0]).decode())[0:4]
            folder_path = self.fInputDataPath + year + '/' + folder
            try:
                os.stat(folder_path)
            except:
                os.mkdir(folder_path)

# Create_ecsv_Files creates the ecsv-files.
# It needs a list of Tables created by Create_Subtables as an input
    def Create_ecsv_Files(self, subtables):
        for table in subtables:
            # Change &-symbol into %26 in all references
            folder = ((table['reference_id'][0]).decode()).replace('&', '%26')
            # Extract the year of the reference
            year = ((table['reference_id'][0]).decode())[0:4]
            folder_path = self.fInputDataPath + year + '/' + folder + '/'
            file_path = ' '
            # Create the file_path/file_name for the following three cases which can happen
            # to the source_id
            if(table['source_id'][0] < 10):
                filename = 'tev-00000' + str(table['source_id'][0]) + '-sed.ecsv'
                file_path = folder_path + filename
            elif((table['source_id'][0] >= 10) and (table['source_id'][0] < 100)):
                filename = 'tev-0000' + str(table['source_id'][0]) + '-sed.ecsv'
                file_path = folder_path + filename
            else:
                filename = 'tev-000' + str(table['source_id'][0]) + '-sed.ecsv'
                file_path = folder_path + filename
            # This if-statement is needed for references with more than 1 data set
            if Path(file_path).is_file():
                files_in_folder = glob.glob((folder_path + filename.split('.')[0]) +'*') 
                existing_data = table.read(file_path, format='ascii.ecsv', delimiter=' ')
                existing_data.meta['file_id'] = int(len(files_in_folder))
                new_filepath = folder_path + filename.split('.')[0] + '-' + str(len(files_in_folder)) + '.ecsv'
                print('Saving file {}'.format(new_filepath))
                existing_data.write(new_filepath, format='ascii.ecsv', delimiter=' ')
                os.remove(file_path)
            # Add meta-data to the tables
            table.meta['data_type'] = 'sed'
            table.meta['source_id'] = int(table['source_id'][0])
            table.meta['reference_id'] = table['reference_id'][0].decode()
            table.meta['telescope'] = table['telescope'][0].decode()
            table.meta['mjd'] = dict(min = float(table['mjd_start'][0]), max = float(table['mjd_stop'][0]))
            table.meta['comments'] = 'This data was collected for 2015ApJ...812...60B and contributed to gamma-cat by Jonathan Biteau.'
            # Saving the ecsv-tables
            print('Saving file {}'.format(file_path))
            table.write(file_path, format='ascii.ecsv', delimiter=' ')
    # Checking all folders of references which have more than 1 dataset and rename 'tev-<source_id>-sed.ecsv'
    # in 'tev-<source_id>-sed-<file_id>.ecsv'
        for table in subtables:
            folder = ((table['reference_id'][0]).decode()).replace('&', '%26')
            year = ((table['reference_id'][0]).decode())[0:4]
            folder_path = self.fInputDataPath + year + '/' + folder + '/'
            if(table['source_id'][0] < 10):
                filename = 'tev-00000' + str(table['source_id'][0]) + '-sed.ecsv'
                file_path = folder_path + filename
            elif((table['source_id'][0] >= 10) and (table['source_id'][0] < 100)):
                filename = 'tev-0000' + str(table['source_id'][0]) + '-sed.ecsv'
                file_path = folder_path + filename
            else:
                filename = 'tev-000' + str(table['source_id'][0]) + '-sed.ecsv'
                file_path = folder_path + filename
            files_in_folder = glob.glob((folder_path + filename.split('.')[0] + '*'))
            if(len(files_in_folder) >1):
                try:
                    existing_data = table.read(file_path, format='ascii.ecsv', delimiter=' ')
                    existing_data.meta['file_id'] = (len(files_in_folder))
                    new_filepath = folder_path + filename.split('.')[0] + '-' + str(len(files_in_folder)) + '.ecsv'
                    existing_data.write(new_filepath, format='ascii.ecsv', delimiter=' ')
                    os.remove(file_path)
                except:
                    continue



if __name__ == '__main__':
    vBiteau = Biteau()
    vSubtables = vBiteau.Create_Subtables()
    vBiteau.Create_Folders(vSubtables)
    vBiteau.Create_ecsv_Files(vSubtables)
