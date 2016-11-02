# Lightcurve format

Each file has some of these columns:

- `time` - center of obeservation exposure in MJD
- `time_min` - start of observation in MJD
- `time_min` - end of observation in MJD
- `flux` - observed integral flux in Crab
- `flux_err` - statistical error on the observed integral flux in Crab

The table metadata should contain these two information:

- `telescope` - experiment string
- `paper_id` - reference string (pref. ADS format)
- `source_id` - source string based in tev-cat

If any column contains the value `-1`, then it is not specified.

Several lightcurves for a single source should be separeted by its reference following 'source_paper.ECSV.'
The paper should be given in ADS format, the source name may vary as the dicussion continues.