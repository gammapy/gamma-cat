# sed

## Format

Each file has some of these columns:

- `energy` - Energy in `TeV`
- `energy_min` - Energy measurement bin left edge in `TeV`
- `energy_max` - Energy measurement bin right edge in `TeV`
- `energy_lo` - Sometimes given instead of `energy_min`, where `energy_min = energy - energy_lo`
- `energy_hi` - Sometimes given instead of `energy_max`, where `energy_max = energy + energy_hi`

- `flux` - Differential flux in `cm-2 s-1 TeV-1`
- `flux_err` - Statistical error on `flux` (if symmetric error is given)
- `flux_hi` - Statistical error on `flux`
- `flux_lo` - Statistical error on `flux`

- `excess` - Excess count
- `sigma` - Statistical significance (sigma)

The `unit` and `description` of these columns is always the same,
so we omit it from these manually created files and add them with a script.

### Flux upper limits

If the `flux` column contains the value `nan` (Not a number),
then the `flux_hi` column contains the flux upper limit.
The confidence level is given in the `ul_confidence_level` key in `meta`.
See `HESS_J1745-290.ecsv` as an example.
