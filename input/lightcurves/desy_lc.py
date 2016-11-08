"""
Dump the FITS Lightcurves from the DESY LC Archive to ECSV files

- URL: https://astro.desy.de/gamma_astronomy/magic/projects/light_curve_archive/index_eng.html
- links and source names are stored in a dictionary
- links can be added if the DESY LC Archive gets extended
- source names can be easily edited and changed to tev-id for example
"""
from astropy.table import Table
from astropy.units import cds
import string
import os


def process_one_file(source_id, filename):
    """This function dumps the FITS files defined in Get_FITS_from_DESY-LC-Archive.py in ECSV follwoing 'source-id_paper-id.ecsv'
    """
    tab = Table.read(filename, format='fits')

    # print('Currently operating source ' + str(source_id))

    # rename column-names to lightcurve-format
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

    # delete unused columns
    del tab['sigma_int_flux_sys']
    del tab['alpha']
    del tab['sigma_alpha_stat']
    del tab['sigma_alpha_sys']
    del tab['e_thr']
    del tab['e_cut']
    del tab['duration']
    del tab['fflag']

    # set formats
    tab.replace_column('time', tab['time'].astype(float))
    tab.replace_column('time_min', tab['time_min'].astype(float))
    tab.replace_column('time_max', tab['time_max'].astype(float))

    # set units
    tab['time'].unit = tab['time_max'].unit = tab['time_min'].unit = cds.MJD
    tab['flux'].unit = tab['flux_err'].unit = cds.Crab

    # find different papers
    papers = []
    # index = []
    index = [0]
    for i in range(0, len(tab) - 1):
        if tab['paper'][i] != tab['paper'][i + 1]:
            papers.append(tab['paper'][i])
            index.append(i + 1)
    papers.append(tab['paper'][-1])
    # print(papers)

    # find multiple telescopes used in a single paper
    telescopes_list = []
    for p in range(0, len(papers) - 1):
        telescope_paper = tab['telescope'][index[p]:index[p + 1] - 1].pformat()
        telescope = set([t for t in telescope_paper if telescope_paper.count(t) > 1])
        # print(telescope)
        telescopes_list.append(telescope)
    telescope_paper = tab['telescope'][index[-1]:].pformat()
    telescope = set([t for t in telescope_paper if telescope_paper.count(t) > 1])
    telescopes_list.append(telescope)

    # get only proper names for these telescopes
    telescopes = []
    for s in telescopes_list:
        telescope = ", ".join(str(e) for e in s)
        telescopes.append(telescope)
    # print(telescopes)

    # convert paper names to safe filename
    filenames = []
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    for p in range(0, len(papers)):
        filename = ''.join(c for c in papers[p] if c in valid_chars)
        filename = ''.join(filename.split())
        filenames.append(filename)
    # print(filenames)

    # convert non-ADS reference names to format 'none'
    temp_filenames = []
    file_index = 1
    valid_chars = "%s" % (string.digits)
    for p in range(0, len(filenames)):
        temp_filename = ''.join(c for c in papers[p][0:4] if c in valid_chars)
        # print(temp_filename)
        if len(temp_filename) != 4:
            filename = str('none' + str(filenames[p]))
            file_index = file_index + 1
            filenames[p]=''.join(c for c in filename)
    # print(filenames)

    # add an index if paper names double, i.e. "reference empty"
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
    # print(filenames)

    # seperate by paper, set metadata
    tables = []
    for x in range(0, len(index) - 1):
        table = tab[index[x]:index[x + 1]]
        table.meta['source_id'] = int(source_id)
        table.meta['telescope'] = ''.join(str(telescopes[x]).split())
        table.meta['paper_id'] = str(papers[x])
        del table['telescope']
        del table['paper']
        tables.append(table)
    table = tab[index[-1] + 1:]
    table.meta['source_id'] = int(source_id)
    table.meta['telescope'] = ''.join(str(telescopes[-1]).split())
    table.meta['paper_id'] = str(papers[x])
    del table['telescope']
    del table['paper']
    tables.append(table)
    # print(tables)

    # ceate folder structure and write files
    count_files = 0
    directory = '/afs/ifh.de/group/amanda/scratch/wegenmat/gamma-cat/input/papers/'
    none_paper_id = 'none'
    for x in range(0, len(filenames)):
        if os.path.lexists(directory + filenames[x][:4]) is False:
            os.mkdir(directory + filenames[x][:4])
        os.chdir(directory + filenames[x][:4] + '/')
        if filenames[x][:4] == none_paper_id:
            if os.path.lexists(directory + filenames[x][:4] + '/' + 'source_id_' + source_id) is False:
                os.mkdir(directory + filenames[x][:4] + '/' + 'source_id_' + source_id)
            os.chdir(directory + filenames[x][:4] + '/' + 'source_id_' + source_id)
        else:
            if os.path.lexists(directory + filenames[x][:4] + '/' + filenames[x]) is False:
                os.mkdir(directory + filenames[x][:4] + '/' + filenames[x])
            os.chdir(directory + filenames[x][:4] + '/' + filenames[x])
        # print('wrote "lightcurve_source_id_' + source_id + '.ecsv' + '" in' + directory + filenames[x][:4] + '/' + filenames[x])
        count_files += 1
    # print(count_files)
    # print(len(filenames))
    return count_files, len(filenames)


def process_all_files():
    files = {
        "138": "http://www-zeuthen.desy.de/multi-messenger/GammaRayData/1es1959+650_combined_lc_v0.2.fits",
        "49": "http://www-zeuthen.desy.de/multi-messenger/GammaRayData/mrk421_combined_lc_v0.2.fits",
        "91": "http://www-zeuthen.desy.de/multi-messenger/GammaRayData/mrk501_combined_lc_v0.2.fits"
    }
    total_files = []
    pub_sources = []
    count_sources = 0
    for source_id, filename in files.items():
        process_one_file(source_id, filename)
        count_sources += 1
        source_files, filenames = process_one_file(source_id, filename)
        total_files.append(source_files)
        pub_sources.append(filenames)

    print('number of sources in the DESY LC Archive: ' + str(count_sources))
    print('number of publsihed lightcurves found: ' + str(sum(pub_sources)))
    print('files totally written: ' + str(sum(total_files)))

if __name__ == '__main__':
    process_all_files()
