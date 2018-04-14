# Call March 2, 2018

* 10 - 11 am
* "gamma-cat" on CTA ezuce, no password -> see [connection.txt](connection.txt)
* Participants: Konstancja Satalecka, Roberta Zanin, Matthias Wegen, Michele Doro, Gernot Maier, Christoph Deil

## Agenda

* Christoph: we are starting to make use of gamma-cat in CTA. See slides from Feb 16, 2018 (on CTA Indico, you need a CTA account)
  [PDF](https://indico.cta-observatory.org/event/1752/contributions/15335/attachments/13017/15464/2018-02-16_CTA_GammaCat.pdf)
  On May 14 at the CTA Orsay collaboration meeting there will be a first session on CTA catalog. We could propose a short
  presentation on gamma-cat there, explain how it can be useful as a data collection to compare with for CTA catalog papers,
  and also "lessons learned" for gamma-ray catalog about content / formats from the gamma-cat experience (if we have any,
  this would need some discussion / preparation)
* Christoph: HESS Galactic catalog release coming in March; new measurement for 64 HESS sources given; suggest to add those
  to gamma-cat. Uniform format -> should be easy with a script. Open questions: multi-Gauss sources?
  Which measurement to use for the gamma-cat catalog? For further information see slides 38 & 39 in the Feb 16, 2018
  presentation mentioned above.
* Status VERITAS data (Gernot)
* Status MAGIC data (Michele)


## Minutes

* HESS HGPS data entry: all agree to add it to gamma-cat as a new measurement for the 64 sources.
  For the morphology, we put the source position / extension as given in the catalog (not the multi-gauss model)
* Brief discussion about sources with energy-dependent morphology
  (see [GH 102](https://github.com/gammapy/gamma-cat/issues/102))
  We agree that whoever adds data for a source with energy-dependent morphology first proposes the format.
  Whether to add FITS images or cubes (that would allow energy-dep morphology) to gamma-cat is a discussion for another day.
* VERITAS data entry is on a good way. Gernot is doing all the work of data entry in gamma-cat.
  The people that want the VERITAS data archive in HEASARC seem happy to ingest it from gamma-cat later,
  i.e. there is no duplication of effort on data entry.
* No MAGIC data entry since last call. They also want an archive of their measurements, but discussions
  are still ongoing how to do it. Michele is proposing use of gamma-cat for that in MAGIC,
  similar to how VERITAS does it. Roberta will go to Italy soon and discuss about possible collaboration
  with the people from http://www.asdc.asi.it/tgevcat/ (are they in MAGIC?) Will re-discuss in the next call.
* In HESS there is so far no task group or discussion of an archive of measurements.
  It's not clear if there is enough interest to get a lot of data entry from HESS.
  Christoph will summarise the data entry status for HESS, and ask for a presentation on gamma-cat
  at the next HESS collaboration meeting (April 9-13), with the goal to generate some interest
  and get some manpower for the coming months to also make HESS data entry complete in the coming months.
* Gernot and Michele comment that [GH 187](https://github.com/gammapy/gamma-cat/pull/187)
  (support for non-detections in the input formats) is needed ASAP for VERITAS and MAGIC data entry.
* Not much progress on script or data formats / schema or webpage.
  If anyone has time to help with Python scripting, please email Christoph & Peter.
* Christoph thinks aiming to write a paper on gamma-cat (similar to http://adsabs.harvard.edu/abs/2017ApJ...835...64G)
  in summer or fall could be useful as a "carrot" to motivate us to spend time on it,
  and for others to join the work. Others are not so sure it's time well-spent, they think actual use of gamma-cat
  e.g. for studies of archival data is key and we should just focus on gamma-cat and support such other users.
  No activity on a paper from our side for now, we can re-dicuss whether to aim for such a paper later.

## Action items

* Christoph: implement support for non-detections next week: [GH 187](https://github.com/gammapy/gamma-cat/pull/187)
* Christoph: add HGPS data in March
* Gernot: continue VERITAS data entry
* Michele: try to get MAGIC on-board for gamma-cat and start data entry
* Roberta: talk to TGeVCat guys, see if / how to collaborate
* All: continue with data entry & scripting for gamma-cat as time allows.

## Next call

* Not scheduled yet. Probably some time in April. Will do a Doodle.
* How to add elongation / position angle info for elongated source shapes (Christoph)
* How to expose the data from gamma-cat
* ... tbd ...
