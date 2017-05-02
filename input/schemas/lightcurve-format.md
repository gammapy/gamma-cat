# Lightcurve format

Each file has some of these columns:

- `time` - center of observation exposure in MJD
- `time_min` - start of observation in MJD
- `time_min` - end of observation in MJD
- `flux` - observed integral flux in Crab
- `flux_err` - statistical error on the observed integral flux in Crab
- `flux_ul` - indicates if a flux is an upper limit
- `index` - spectral index (used as `energy ** (-index)`, i.e. index is a positive number)
- `index_err` - statistical error on the spectral index

If `time_min` or `time_max` are identically with `time`, these columns may be omitted.
If a flux is an upper limit, `flux` and `flux_err` get `np.nan` and `flux_ul` gets the respectively flux value. Otherwise, `flux_ul` gets `np.nan`.

The table metadata should contain the following information:

- `data_type` - lc
- `source_id` - source string based on tev-cat
- `telescope` - experiment string or list of strings
- `reference_id` - reference string (pref. ADS format)
- `timesys` - to indicate if MJD is given in UTC or TT
- `comment` - list of strings for comments, linebreaks allowed


If any entries are missing or not specified, use `np.nan`.
If a column consits exclusively of `np.nan`, this column may be deleted.

Multiple lightcurves for a single source should be separated by its reference as mentioned in `source_paper.ECSV.`
A paper reference should be given in ADS format.
Other references such as private communication, talks or unpublished thesis should be specified in the comment header.
