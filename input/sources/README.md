# Per-source data

This folder defines what a "source" is in our catalog.

One YAML file per source in the format `<source_id>.yaml`.

No source parameters here, only cross-links to other TeV
catalogs and papers.

Schema (examples from `000234.yaml`):

* `source_id` - Source ID in this catalog (str, e.g. `000234`)
* TBD: Maybe we'll add our own source names.

* `tevcat_id` - Source ID in TeVCat (int, e.g. `234`)
* `tevcat2_id` - Source ID in TeVCat2 (str, e.g. `ChXqo`)
* `tevcat_name` - Source name in TeVCat (str, e.g. `TeV J1614-518`)

* `tgevcat_id` - Source ID in TeGeV (int, e.g. `83`)
* `tgevcat_name` - Source name in TeGeV (str, e.g. `TeV J1614-5149`)

* `papers` - List of ADS bibcodes (list of str)

The list of papers is supposed to be roughly the ones most relevant
for gamma-ray astronomy. Not just the ones we take measurements from
for this catalog.

Of 