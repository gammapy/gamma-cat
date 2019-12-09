from gammapy.maps import Map, MapAxis
from astropy.coordinates import SkyCoord
#from gammapy.spectrum.models import PowerLaw,PowerLaw2,ExponentialCutoffPowerLaw
import numpy as np
from astropy import units as u
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy import interpolate
from gammapy.maps import Map, WcsGeom, WcsNDMap
from gammapy.modeling.models import DiskSpatialModel, PointSpatialModel, ExpCutoffPowerLawSpectralModel
import gammalib

#######
def pow(x,N,indice,eref):
    return N*(x/eref)**(-1.*indice)

def expcutoff(x,N,indice,ecut,eref):
    return N*(x/eref)**(-1.*indice) * np.exp(-1.0*x/ecut)
########

### read the file with the spatial extent
rad = np.genfromtxt('radial_extent.txt')
energy = rad[:,0]*1e6
dist = rad[:,1] * 1.357 #the factor 1.357 relates the radius at 1/e with the radius at 90% (0.9/(1/e)**1/3)

rad_interpolate = interpolate.interp1d(energy, dist, fill_value="extrapolate")

### read the file with the spectral parameters and estimate the normalization
spec = np.genfromtxt('Index_vs_flux.txt')
index = spec[:,3]
e_index = spec[:,4]
ang_dist = spec[:,1]
flux_1_5TeV = spec[:,6]
e_flux_1_5TeV = spec[:,7]

### I've estimated a function to model the index and fluxes dependecies, based on Fig. 9 of HESS paper
def fluxes(x):
    a = 1.2 * 1.08686e-12
    b = 0.0326925
    c = 0.528341
    return a * (x + 1)**b * np.exp(-1.0*x/c)

def indexes(x):
    a = 0.697262
    b = 1.87344
    return a*x+b

# Define energy ranges and a cut-off
emin=1e6 #TeV
emax=5e6 #TeV
E_ref = 1e6 #MeV
Ecut = 19e6 # cutoff in MeV

### interpolate the function of index, fluxes and normalizations
d = np.linspace(0.0,1.55,100)

### Position of the pulsar
ra_0_psr = 276.554417
dec_0_psr = -13.580028
position_psr = SkyCoord(ra_0_psr, dec_0_psr, frame='icrs', unit='deg')

### Position of the map center
position = SkyCoord(276.4, -13.966667, frame='icrs', unit='deg')

### Energy axes and size
energy_axis = MapAxis.from_bounds(0.2e5, 250e6, 40, interp='log', name='energy', unit='MeV')

enlarger = 1.2
r_0 = rad_interpolate(energy_axis.center) * u.deg * enlarger
r_0 = np.where(r_0>=0, r_0, 0) * u.deg

### Fill the index and normalization at the positions of the pixels
binsize=0.02
eccentricity = 0.69
ang = 45.
width = 3.

m_wcs = WcsGeom.create(binsz=binsize, coordsys="CEL",
                       skydir=position_psr,
                       width=width*u.deg,
                       axes=[energy_axis])

model = DiskSpatialModel(lon_0=ra_0_psr*u.deg, lat_0=dec_0_psr*u.deg, r_0="1.1 deg", e=eccentricity, phi=ang * u.deg, frame="icrs")

coords = m_wcs.get_coord()
coord_map = SkyCoord(coords.lon, coords.lat, frame='icrs')
separation = position_psr.separation(coord_map)

new_indexes = indexes(separation.value)

N0 = (fluxes(separation.value) * (1-new_indexes) /
      ((emax/E_ref)**(1-new_indexes) - (emin/E_ref)**(1-new_indexes))) / (0.26 * np.pi / 180.)**2

### Create the map
skymap = Map.create(width=width*u.deg, axes=[energy_axis],
                    binsz=binsize, coordsys="CEL",
                    skydir=position_psr)

for idx, energy in enumerate(energy_axis.center):
    
    if r_0[idx] > 0:
        model = DiskSpatialModel(lon_0=ra_0_psr*u.deg, lat_0=dec_0_psr*u.deg,
                                 r_0=r_0[idx],
                                 e=eccentricity,
                                 phi=ang * u.deg,
                                 frame="icrs")
    else:
        model = PointSpatialModel(lon_0=ra_0_psr*u.deg, lat_0=dec_0_psr*u.deg,
                                  frame='icrs')
    
    skymap.data[idx] = model.evaluate_geom(skymap.geom.to_image())

skymap.data = np.where(skymap.data>0,1.,0)

### Fill the map with the flux values
for j in np.arange(len(energy_axis.edges)-1):
        flx = (expcutoff((energy_axis.edges.value[j]/1e6),N0[j],new_indexes[j],Ecut/1e6,E_ref/1e6)
               * (energy_axis.edges.value[j+1]-energy_axis.edges.value[j])/1e6)
        
        flx = flx / (energy_axis.edges.value[j+1]-energy_axis.edges.value[j])
        skymap.data[j] *= flx

### Cut the ellipse in order to get an asymettric shape
for j in np.arange(len(energy_axis.edges)-1):
    for idx1 in np.arange(0,int(width/binsize)):
            for idx2 in (np.arange(0,int(width/binsize))[::-1]):
                if (idx2+1.0)/(idx1+1.0) < (np.tan((125-ang)*np.pi/180.) - 7/binsize/(idx1+1.0)): #+ 80/idx1+1.0:
                    skymap.data[j,idx1,idx2] *= 0
                else:
                    continue

### Smooth the map
skymap = skymap.smooth(width=0.08 * u.deg, kernel="gauss")

### Save the map
skymap.write('hessj1825_cube.fits', hdu='Primary', overwrite='True')

hdul = fits.open('hessj1825_cube.fits')
hdul[0].header.set('BUNIT', 'photon/cm2/s/MeV/sr', 'Photon flux')
hdul[0].verify('fix')
hdul[1].name='ENERGIES'
hdul[1].header['TTYPE2']='Energy'
hdul[1].verify('fix')
hdul.writeto('hessj1825_map.fits',overwrite=True)

### create gammalib model
spatial = gammalib.GModelSpatialDiffuseCube(gammalib.GFilename('hessj1825_map.fits'))
spectral = gammalib.GModelSpectralConst(1.)
model = gammalib.GModelSky(spatial,spectral)
## fill to model container and write to disk
models = gammalib.GModels()
models.append(model)
models.save('hessj1825.xml')

