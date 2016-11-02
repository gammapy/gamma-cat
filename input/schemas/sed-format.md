# SED format

For spectral energy distributions (SEDs), aka "spectral points"
or "flux points", we use the format described here:

http://gamma-astro-data-formats.readthedocs.io/en/latest/results/flux_points/index.html

## Header


See http://gamma-astro-data-formats.readthedocs.io/en/latest/results/flux_points/index.html#header-keywords

- `sed_type` -- `diff_flux_points`
- `ul_conf`

## Fields

The point energy info is given in the following fields:
 
- `e_ref`
- `e_min`
- `e_max`

The default energy unit assumed is `TeV`. 
Using a different unit is possible, if that is declared in the header.

The point flux info fields are:

- `dnde`
- `dnde_err`
- `dnde_errn`
- `dnde_errp`

The default `dnde` unit is `cm-2 s-1 TeV-1`.
Using a different unit is possible, if that is declared in the header.

Additional fields we use for some SEDs:

- `excess`
- `significance`

## Flux upper limits

If the `dnde` column contains the value `nan` (Not a number),
then the `flux_hi` column contains the flux upper limit.

The confidence level is given in the `UL_CONF` key in `meta`.
See `HESS_J1745-290.ecsv` as an example.