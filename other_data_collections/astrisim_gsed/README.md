# astrisim/gsed

This folder contains a version of
http://www.iasf-milano.inaf.it/~giuliani/astrisim/gsed/
as `index2.fits` as of November 23, 2016.

The idea is to write a script to add info they have
but we don't to gamma-cat.
See https://github.com/gammapy/gamma-cat/issues/32


## SEDs

This is the list of SEDs.
I'll go through them and add them systematically.

### 1418-609

- source_id: 65
- sed : `input/data/2006/2006A%2526A...456..245A/tev-000065.ecsv`

- `1418-609_FERMI.ecsv`
  - Skip
  - Not TeV spectral points
- `1418-609_HESS_2006.ecsv`
  - Skip
  - Was already in gamma-cat
  - **TODO: why are values slightly different?**
- `1418-609_MODEL_HESS2006.ecsv`
  - Skip
  - Looks like a duplicate of `1418-609_HESS_2006.ecsv`!?

### 1420-607

- source_id: 66
- sed : `input/data/2006/2006A%26A...456..245A/tev-000066.ecsv`

- `1420-607_DATI_FERMI-HESS.ecsv`
  - **TODO: this looks like useful TeV spectral points. But where do they come from?**
- `1420-607_DATI_HESS2006.ecsv`
  - Skip
  - Looks like a duplicate of `1420-607_DATI_FERMI-HESS.ecsv`!?
- `1420-607_MODEL_HESS2006.ecsv`
  - Skip
  - Looks like a duplicate of `1420-607_DATI_FERMI-HESS.ecsv`!?

### 1626-490

- source_id: 85
- sed : `input/data/2008/2008A%26A...477..353A/tev-000085.ecsv`

- `1626-490_DATI_HESS.ecsv`
  - Skip
  - Not TeV spectral points
- `1626-490_MODEL_HESS.ecsv`
  - Skip
  - Not TeV spectral points
- `1626-490_UL_FERMI.ecsv`
  - Skip
  - Not TeV spectral points

### 1804-217

- source_id: 113
- sed : `input/data/2006/2006ApJ...636..777A/tev-000113.ecsv`

- `1804-217_DATI_CANGAROO.ecsv`
  - **TODO: this looks like useful TeV spectral points. But where do they come from? Some Cangaroo paper?**
- `1804-217_DATI_FERMI-HESS.ecsv`
  - Skip
  - Was already in gamma-cat
  - **TODO: why are values slightly different?**
- `1804-217_DATI_HESS.ecsv`
- `1804-217_MODEL_CANGAROO.ecsv`
- `1804-217_MODEL_HESS.ecsv`

### 1813-178

- source_id: 116
- sed : `input/data/2006/2006ApJ...636..777A/tev-000116.ecsv`

- `1813-178_DATI_FERMI-HESS.ecsv`
- `1813-178_DATI_HESS2006.ecsv`
- `1813-178_DATI_MAGIC.ecsv`
- `1813-178_MODEL_MAGIC.ecsv`

### 1840-055

- source_id: 125
- sed : `input/data/2008/2008A%26A...477..353A/tev-000125.ecsv`

- `1840-055_DATI_FERMI-HESS.ecsv`
- `1840-055_DATI_HESS.ecsv`
- `1840-055_MODEL_ARGO.ecsv`
- `1840-055_MODEL_HESS.ecsv`

### CTB37A

- source_id: 97
- sed : `input/data/2008/2008A%26A...490..685A/tev-000097.ecsv`

- `CTB37A_fermi1.ecsv`
- `CTB37A_hess.ecsv`

### CTB37B

- source_id: 95
- sed : `input/data/2006/2006ApJ...636..777A/tev-000095.ecsv`

- `CTB37B_fermi.ecsv`
- `CTB37B_hess.ecsv`

### G359.1-0.5

- source_id: 108
- sed : `input/data/2006/2006ApJ...636..777A/tev-000108.ecsv`

- `G359.1-0.5_HESS_2008.ecsv`
- `G359.1-0.5_MODEL_HESS.ecsv`

### HESSJ1640-465

- source_id: 88
- sed : `input/data/2006/2006ApJ...636..777A/tev-000088.ecsv`
- sed : `input/data/2014/2014MNRAS.439.2828A/tev-000088.ecsv`

- `HESSJ1640-465_Fermi.ecsv`
- `HESSJ1640-465_HESS.ecsv`

### RXJ1713

- source_id: 96
- sed : `input/data/2016/2016arXiv160908671H/tev-000096.ecsv`

- `RXJ1713_fermi2011.ecsv`
- `RXJ1713_hess2007.ecsv`

### TeVJ0835-456

- source_id: 37
- sed: `input/data/2006/2006A%26A...448L..43A/tev-000037.ecsv`
- sed: `input/data/2012/2012A%26A...548A..38A/tev-000037.ecsv`

- `TeVJ0835-456_FERMI_2FHL.ecsv`
- `TeVJ0835-456_HESS_2006.ecsv`
- `TeVJ0835-456_MODEL_HESS_2006.ecsv`

### TeVJ0852-463

- source_id: 39
- sed: `input/data/2016/2016arXiv161101863H/tev-000039.ecsv`

- `TeVJ0852-463_FERMI_.ecsv`
- `TeVJ0852-463_HESS_.ecsv`
- `TeVJ0852-463_MODEL_HADRONIC.ecsv`

### TeVJ1023-575

- source_id: 46
- sed: `input/data/2011/2011A%26A...525A..46H/tev-000046.ecsv`

- `TeVJ1023-575_FERMI.ecsv`
- `TeVJ1023-575_HESS.ecsv`

### TeVJ1026-582

- source_id: 47
- status: no SED
- Only `input/data/2011/2011A%26A...525A..46H/tev-000047.yaml`

**TODO: add SED to gamma-cat**

- `TeVJ1026-582_FERMI_2013.ecsv`
- `TeVJ1026-582_HESS_2011.ecsv`
- `TeVJ1026-582_MODEL_HESS.ecsv`

### TeVJ1119-614

- source_id: 50
- status: no data

**TODO: add SED to gamma-cat**

- `TeVJ1119-614_FERMI_DATA.ecsv`
- `TeVJ1119-614_HESS_DATA.ecsv`

### TeVJ1302-638

- source_id: 60
- status: no data

**TODO: add SED to gamma-cat**

- `TeVJ1302-638_HESS.ecsv`
- `TeVJ1302-638_MODEL_HESS.ecsv`

### TeVJ1303-631

- source_id: 61
- sed: `input/data/2012/2012A%26A...548A..46H/tev-000061.ecsv`

- `TeVJ1303-631_HESS.ecsv`
- `TeVJ1303-631_MODEL_HESS.ecsv`

### TeVJ1356-645

- source_id: 64
- status: no sed
- `input/data/2008/2008AIPC.1085..285R/tev-000064.yaml`

**TODO: add SED to gamma-cat**

- `TeVJ1356-645_FERMI_2FHL.ecsv`
- `TeVJ1356-645_HESS_2011.ecsv`
- `TeVJ1356-645_MODEL_HESS_POW.ecsv`

### TeVJ1418-609

- source_id: 65
- sed: `input/data/2006/2006A%26A...456..245A/tev-000065.ecsv`

- `TeVJ1418-609_FERMI.ecsv`
- `TeVJ1418-609_HESS_2006.ecsv`
- `TeVJ1418-609_MODEL_HESS2006.ecsv`

### TeVJ1420-607

- source_id: 66
- sed: `input/data/2006/2006A%26A...456..245A/tev-000066.ecsv`

- `TeVJ1420-607_FERMI.ecsv`
- `TeVJ1420-607_HESS2006.ecsv`
- `TeVJ1420-607_MODEL_HESS2006.ecsv`

### TeVJ1427-608

- source_id: 68
- sed: `input/data/2008/2008A%26A...477..353A/tev-000068.ecsv`

- `TeVJ1427-608_FERMI_2016.ecsv`
- `TeVJ1427-608_HESS_DATA.ecsv`
- `TeVJ1427-608_MODEL_FERMI_HESS.ecsv`
- `TeVJ1427-608_MODEL_HESS_PL.ecsv`

### TeVJ1442-624

- source_id: 70
- sed: `input/data/2016/2016arXiv160104461H/tev-000070.ecsv`

- `TeVJ1442-624_FERMI_2014.ecsv`
- `TeVJ1442-624_HESS_2009.ecsv`
- `TeVJ1442-624_HESS_2016.ecsv`
- `TeVJ1442-624_MODEL_HADRONIC.ecsv`
- `TeVJ1442-624_MODEL_IC.ecsv`

### TeVJ1459-608

- source_id: 73
- status: no data

**TODO: add SED to gamma-cat**

- `TeVJ1459-608_HESS_DATA.ecsv`
- `TeVJ1459-608_MODEL_HESS_PL.ecsv`

### TeVJ1503-582

- source_id: 75
- sed: `input/data/2008/2008AIPC.1085..281R/tev-000075.ecsv`

- `TeVJ1503-582_HESS.ecsv`
- `TeVJ1503-582_MODEL_HESS.ecsv`

### TeVJ1506-623

- source_id: 77
- status: no sed
- `input/data/2011/2011A%26A...525A..45H/tev-000077.yaml`

**TODO: add SED to gamma-cat**

- `TeVJ1506-623_HESS.ecsv`
- `TeVJ1506-623_MODEL_HESS.ecsv`

### TeVJ1514-591

- source_id: 79
- sed: `input/data/2005/2005A%26A...435L..17A/tev-000079.ecsv`

- `TeVJ1514-591_HESS.ecsv`
- `TeVJ1514-591_MODEL_HESS.ecsv`

### TeVJ1614-518

- source_id: 83
- sed: `input/data/2006/2006ApJ...636..777A/tev-000083.ecsv`
- no sed: `input/data/2011/2011A%26A...531L..18H/tev-000083.yaml`

- `TeVJ1614-518_FERMI_2FHL.ecsv`
- `TeVJ1614-518_FERMI_3FGL.ecsv`
- `TeVJ1614-518_HESS_2006.ecsv`
- `TeVJ1614-518_MODEL_HESS_2006.ecsv`

### TeVJ1616-508

- source_id: 84
- sed: `input/data/2006/2006ApJ...636..777A/tev-000084.ecsv`

- `TeVJ1616-508_HESS_2006.ecsv`
- `TeVJ1616-508_MODEL_HESS.ecsv`

### TeVJ1626-490

- source_id: 85
- sed: `input/data/2008/2008A%26A...477..353A/tev-000085.ecsv`

- `TeVJ1626-490_FERMI2013_UL.ecsv`
- `TeVJ1626-490_HESS2008.ecsv`
- `TeVJ1626-490_MODEL_HESS2008.ecsv`

### TeVJ1632-478

- source_id: 86
- sed: `input/data/2006/2006ApJ...636..777A/tev-000086.ecsv`

- `TeVJ1632-478_FERMI_DATA.ecsv`
- `TeVJ1632-478_HESS_DATA.ecsv`
- `TeVJ1632-478_MODEL_HESS_PL.ecsv`

### TeVJ1634-472

- source_id: 87
- sed: `input/data/2006/2006ApJ...636..777A/tev-000087.ecsv`

- `TeVJ1634-472_FERMI.ecsv`
- `TeVJ1634-472_HESS.ecsv`
- `TeVJ1634-472_MODEL_HESS.ecsv`

### TeVJ1640-465

- source_id: 88
- sed: `input/data/2006/2006ApJ...636..777A/tev-000088.ecsv`
- sed: `input/data/2014/2014MNRAS.439.2828A/tev-000088.ecsv`

- `TeVJ1640-465_FERMI.ecsv`
- `TeVJ1640-465_HESS.ecsv`
- `TeVJ1640-465_MODEL_FERMI.ecsv`
- `TeVJ1640-465_MODEL_HESS.ecsv`

### TeVJ1641-463

- source_id: 89
- no sed: `input/data/2013/2013arXiv1303.0979O/tev-000089.yaml`
- sed: `input/data/2014/2014ApJ...794L...1A/tev-000089.ecsv`

- `TeVJ1641-463_FERMI.ecsv`
- `TeVJ1641-463_HESS.ecsv`
- `TeVJ1641-463_MODEL_HESS.ecsv`

### TeVJ1647-458

- source_id: 90
- no sed: `input/data/2012/2012A%26A...537A.114A/tev-000090.yaml`

**TODO: add SED to gamma-cat**

- `TeVJ1647-458_HESS.ecsv`
- `TeVJ1647-458_MODEL_HESS.ecsv`

### TeVJ1702-420

- source_id: 92
- sed: `input/data/2006/2006ApJ...636..777A/tev-000092.ecsv`
- sed: `input/data/2008/2008A%26A...477..353A/tev-000092.ecsv`

- `TeVJ1702-420_HESS_2008.ecsv`
- `TeVJ1702-420_MODEL_HESS_POW.ecsv`

### TeVJ1708-410

- source_id: 93
- sed: `input/data/2006/2006ApJ...636..777A/tev-000093.ecsv`
- sed: `input/data/2008/2008A%26A...477..353A/tev-000093.ecsv`

- `TeVJ1708-410_HESS2006.ecsv`
- `TeVJ1708-410_HESS2008.ecsv`
- `TeVJ1708-410_MODEL_HESS2006.ecsv`
- `TeVJ1708-410_MODEL_HESS2008.ecsv`
- `TeVJ1708-410_MODEL_HESS2008_MAN.ecsv`

### TeVJ1708-443

- source_id: 94
- sed: `input/data/2011/2011A%26A...528A.143H/tev-000094.ecsv`

- `TeVJ1708-443_CANGAROO-III_2009.ecsv`
- `TeVJ1708-443_CANGAROO-I_2009.ecsv`
- `TeVJ1708-443_FERMI_2013.ecsv`
- `TeVJ1708-443_HESS_2011.ecsv`
- `TeVJ1708-443_MODEL_CANGAROO-III_2009.ecsv`
- `TeVJ1708-443_MODEL_HESS.ecsv`

### TeVJ1718-385

- source_id: 99
- sed: `input/data/2007/2007A%26A...472..489A/tev-000099.ecsv`

- `TeVJ1718-385_HESS_DATA.ecsv`
- `TeVJ1718-385_MODEL_HESS_CUTOFFPL.ecsv`

### TeVJ1729-345

- source_id: 102
- no sed: `input/data/2011/2011A%26A...531A..81H/tev-000102.yaml`

**TODO: add SED to gamma-cat**

- `TeVJ1729-345_HESS.ecsv`
- `TeVJ1729-345_MODEL_HESS.ecsv`

### TeVJ1732-347

- source_id: 103
- sed: `input/data/2008/2008A%26A...477..353A/tev-000103.ecsv`
- sed: `input/data/2011/2011A%26A...531A..81H/tev-000103.ecsv`

- `TeVJ1732-347_HESS_.ecsv`
- `TeVJ1732-347_MODEL_HADRONIC.ecsv`

### TeVJ1741-301

- source_id: 104
- no sed: `input/data/2008/2008AIPC.1085..249T/tev-000104.yaml`

**TODO: add SED to gamma-cat**

- `TeVJ1741-301_MODEL_HESS.ecsv`

### TeVJ1745-290

- source_id: 106
- sed: `input/data/2009/2009A%26A...503..817A/tev-000106.ecsv`
- sed: `input/data/2016/2016Natur.531..476H/tev-000106.ecsv`

- `TeVJ1745-290_FERMI.ecsv`
- `TeVJ1745-290_HESS.ecsv`
- `TeVJ1745-290_MODEL_HESS_VERITAS.ecsv`

### TeVJ1747-281

- source_id: 110
- sed: `input/data/2005/2005A%26A...432L..25A/tev-000110.ecsv`

- `TeVJ1747-281_HESS.ecsv`
- `TeVJ1747-281_MODEL_HESS_VERITAS.ecsv`
- `TeVJ1747-281_VERITAS.ecsv`

### TeVJ1804-217

- source_id: 113
- sed: `input/data/2006/2006ApJ...636..777A/tev-000113.ecsv`

- `TeVJ1804-217_CANGAROO2008.ecsv`
- `TeVJ1804-217_FERMI_HESS_2013.ecsv`
- `TeVJ1804-217_HESS2006.ecsv`
- `TeVJ1804-217_MODEL_CANGAROO2008.ecsv`
- `TeVJ1804-217_MODEL_HESS.ecsv`

### TeVJ1808-204

- source_id: 114
- status: no data

**TODO: add SED to gamma-cat**

- `TeVJ1808-204_MODEL_HESS_PL.ecsv`

### TeVJ1810-193

- source_id: 115
- sed: `input/data/2007/2007A%26A...472..489A/tev-000115.ecsv`

- `TeVJ1810-193_HESS.ecsv`
- `TeVJ1810-193_MODEL_HESS.ecsv`

### TeVJ1813-178

- source_id: 116
- sed: `input/data/2006/2006ApJ...636..777A/tev-000116.ecsv`

- `TeVJ1813-178_FERMI_HESS_2013.ecsv`
- `TeVJ1813-178_HESS2006.ecsv`
- `TeVJ1813-178_MAGIC2006.ecsv`
- `TeVJ1813-178_MODEL_MAGIC2006.ecsv`

### TeVJ1826-137

- source_id: 118
- sed: `input/data/2006/2006A%26A...460..365A/tev-000118.ecsv`
- sed: `input/data/2006/2006ApJ...636..777A/tev-000118.ecsv`

- `TeVJ1826-137_CGRO_EGRET_DATA.ecsv`
- `TeVJ1826-137_HESS_DATA.ecsv`
- `TeVJ1826-137_MODEL_HESS.ecsv`

### TeVJ1826-148

- source_id: 119
- status: no data

**TODO: add SED to gamma-cat**

- `TeVJ1826-148_FERMI_INFC.ecsv`
- `TeVJ1826-148_FERMI_SUPC.ecsv`
- `TeVJ1826-148_HESS_INFC.ecsv`
- `TeVJ1826-148_HESS_SUPC.ecsv`
- `TeVJ1826-148_MODEL_HESS_INFC.ecsv`
- `TeVJ1826-148_MODEL_HESS_INFC_MAN.ecsv`
- `TeVJ1826-148_MODEL_HESS_SUPC.ecsv`

### TeVJ1831-098

- source_id: 120
- status: no data

**TODO: add SED to gamma-cat**

- `TeVJ1831-098_HESS_2011.ecsv`
- `TeVJ1831-098_MODEL_HESS.ecsv`

### TeVJ1833-105

- source_id: 122
- sed: `input/data/2015/2015MNRAS.446.1163H/tev-000122.ecsv`

- `TeVJ1833-105_HESS.ecsv`
- `TeVJ1833-105_MODEL_HESS.ecsv`

### TeVJ1834-087

- source_id: 123
- sed: `input/data/2006/2006ApJ...636..777A/tev-000123.ecsv`

- `TeVJ1834-087_FERMI_2013.ecsv`
- `TeVJ1834-087_HESS_2011.ecsv`
- `TeVJ1834-087_MODEL_HADRONIC.ecsv`

### TeVJ1837-069

- source_id: 124
- sed: `input/data/2006/2006ApJ...636..777A/tev-000124.ecsv`

- `TeVJ1837-069_FERMI_2FHL.ecsv`
- `TeVJ1837-069_FERMI_3FGL.ecsv`
- `TeVJ1837-069_HESS_2006.ecsv`
- `TeVJ1837-069_MODEL_2006.ecsv`

### TeVJ1840-055

- source_id: 125
- sed: `input/data/2008/2008A%26A...477..353A/tev-000125.ecsv`

- `TeVJ1840-055_FERMI_HESS_2013.ecsv`
- `TeVJ1840-055_HESS_2008.ecsv`
- `TeVJ1840-055_MODEL_ARGO_2013.ecsv`
- `TeVJ1840-055_MODEL_HESS_2008.ecsv`

### TeVJ1846-029

- source_id: 127
- status: no data

**TODO: add SED to gamma-cat**

- `TeVJ1846-029_HESS_2008.ecsv`
- `TeVJ1846-029_MODEL_HESS.ecsv`

### TeVJ1848-017

- source_id: 128
- sed: `input/data/2008/2008AIPC.1085..372C/tev-000128.ecsv`

- `TeVJ1848-017_FERMI.ecsv`
- `TeVJ1848-017_HESS.ecsv`

### TeVJ1849-000

- source_id: 129
- status: no data

**TODO: add SED to gamma-cat**

- `TeVJ1849-000_FERMI_UPPER_LIMITS.ecsv`
- `TeVJ1849-000_MODEL_CRAB_RESCALED.ecsv`

### W28

- source_id: 112
- sed: `input/data/2008/2008A%26A...481..401A/tev-000112.ecsv`

- `W28_MODEL_HADRONIC.ecsv`
- `W28_agile.ecsv`
- `W28_nord-fermi.ecsv`
- `W28_nord-hess.ecsv`
- `W28_sud_Fermi_3.ecsv`
- `W28_sud_MODEL_HADRONIC.ecsv`
- `W28_sud_sud_hess.ecsv`

### w1457

- source_id: 72
- status: no data

**TODO: add SED to gamma-cat**

- `w1457_fermi.ecsv`
- `w1457_magic.ecsv`
