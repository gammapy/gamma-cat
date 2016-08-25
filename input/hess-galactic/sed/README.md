# sed

## Format

Each file has some of these columns:

- `energy` - Energy in `TeV`
- `flux` - Differential flux in `cm-2 s-1 TeV-1`
- `flux_err` - Statistical error on `flux` (if symmetric error is given)
- `flux_hi` - Statistical error on `flux`
- `flux_lo` - Statistical error on `flux`
- `excess` - Excess count
- `sigma` - Statistical significance (sigma)

The `unit` and `description` of these columns is always the same,
so we omit it from these manually created files and add them with a script.

Flux upper limits are declared via magic value of `-1`.
TODO: be specific in which column and point to an example.


TODO
----

Update HESS J1641-463 : http://adsabs.harvard.edu/abs/2014arXiv1408.5280H