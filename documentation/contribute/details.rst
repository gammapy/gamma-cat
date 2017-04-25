.. include:: ../references.rst

Details
=======

This page contains some notes with details about `gamma-cat`. 

Data
----

Overview
++++++++

This catalog contains data collected from the literature
(usually one or several papers per source).

In this repository, there's four major folders:

* `input` is where we collect data about sources given in papers.
  This is very heterogeneous and is the place for data entry only.
* `output` is produced with the `make_output.py` script in an
  automatic way from `input`. It's as-homogeneous and complete data
  as possible and what you should access for information lookup.
* `docs` is a webpage that displays part of the information in the
  repo (see link above). Specifically, there's a search field to find
  a given source and then from the source detail view there's links
  to the corresponding files in the `input` folder so that
  submitting corrections and additions is easy.
  This is intentionally very minimal, for a better experience to
  view the catalog online, go to `gamma-sky.net/cat/tev`_
  (not yet, coming soon).
* `seed` contains seed catalogs of TeV source info other people have
  collected previously. It was used to originally populate `input`
  using the `import_seed.py` script (see details below).

Seed
++++

As a starting point, data was ingested from these sources
(see the README files there for further information):

* https://github.com/gammapy/gamma-cat/tree/master/input/hess-galactic
* https://github.com/gammapy/gamma-cat/tree/master/input/tevcat
* https://github.com/gammapy/gamma-cat/tree/master/input/tgevcat

Procedure
+++++++++

Information given in papers is very heterogeneous. Sometimes position
is given in Galactic coordinates, sometimes in RA/DEC coordinates.
There's different morphology and spectral models, sometimes certain
parameters haven't been measured or at least aren't given in the publication.

The idea is that we only collect the information from the papers here
(so that checking against the paper is easy and the manually
edited files are as small as possible), and then the `make_output.py`
script generates an as-homogeneous as possible version of the catalog.

* In the input folder ``input/data``, data is organised by ``reference_id`` first, then ``source_id``.
* In the output folder ``docs/data``, data is organised by ``source_id`` first, then ``reference_id``.

Paper identifiers
^^^^^^^^^^^^^^^^^

For paper identifiers, we use the ADS identifiers.

These are unique, well-known and stable.
This corresponds to the `bibcode` in https://github.com/andycasey/ads/,
i.e. can be used to obtain further info from ADS

Note that some bibcodes contain characters that don't work well
(or at all) as directory or filenames, e.g. `2011A&A...531L..18H`
with the `&` character. 
What ADS does in that case for URLs is to quote them, i.e.
the URL is http://adsabs.harvard.edu/abs/2011A%26A...531L..18H . 
In `gamma-cat` we do the same, we URL quote the bibcode for filenames,
folder names and URLs, and otherwise use the normal bibcode.

>>> papers = list(ads.SearchQuery(bibcode='2011A&A...531L..18H'))
>>> print(papers[0].bibcode)
'2011A&A...531L..18H'

>>> import urllib.parse
>>> urllib.parse.quote('2011A&A...531L..18H')
'2011A%26A...531L..18H'
>>> urllib.parse.unquote('2011A%26A...531L..18H')
'2011A&A...531L..18H'

Source identifiers
^^^^^^^^^^^^^^^^^^

* We use integer source identifiers.
  In many cases they are the same as for the `TeGeV` catalog,
  but generally that is not the case.
* We do not introduce new sources "names" (for now).
  TBD: how should people reference sources from our catalog?
  Maybe we should do a position-based identifier like `TeVCat` or `TeGeV` cat?

* TBD: How do we handle sources that split out into multiple sources
  with deeper observations?

Source classes
^^^^^^^^^^^^^^

* TBD: Define source classes and their semantics


Positions
^^^^^^^^^

Sometimes source positions aren't measured or given in the paper.
This is commonly the case for AGN.
In those cases, we use the position from SIMBAD and look it up like this:

.. code-block:: python

    >>> from astropy.coordinates import SkyCoord
    >>> SkyCoord.from_name('Crab nebula').to_string(precision=7)
    '83.6330830 22.0145000'

and store it like this:

.. code-block:: yaml

    position:
      simbad_id: Crab nebula
      ra: 83.6330830
      dec: 22.0145000

The presence of the `simbad_id` key means that it's a position from `SIMBAD`_.

How it works
------------

This is very much work in progress.
Feedback and contributions welcome!

* At the moment we're just using our own Python scripts,
  and YAML files (because I find them easier to read and edit than JSON),
  as well as ECSV files.
  Maybe we'll switch to use the https://astrocats.space/ machinery later.
* We use Python scripts. Only Python 3.4+ and the latest versions of
  Astropy, Gammapy, ... are supported (very few people will run the scripts,
  no point in supporting old versions here, even if it would be easy to do).

There is a nice Python package `gammacat` that's used to process and
validate the catalog. But you can also use it for analysis if you know
some Python. Start by looking at the examples in `gammacat/tests`,
then look at the source code, then ask questions if you don't know
how to do something.

Tools
-----

The following tool is helpful to lint YAML files:

- `yamllint`_

TODO: it's too picky, showing errors for things that are OK.
Figure out how to make it less picky and document that here.

Website build
-------------

The `gamma-cat` website is a static website generated by Python and Sphinx.

We have a `Sphinx test page <tests/index.html>`__ where we can try out things locally
and check if they also work on ReadTheDocs. It's an orphan page, i.e. doesn't show up
for normal users.

We use several Sphinx extensions, and also have our own in `gammacat/sphinx/exts`.

More info soon ... for now this is just a link collection:

* `sphinxcontrib.rawfiles`
  * Useful example. Not very useful directly, because can't control destination of the copy!?
  * Code: https://bitbucket.org/birkenfeld/sphinx-contrib/src/master/rawfiles/sphinxcontrib/rawfiles.py
  * PyPI: https://pypi.python.org/pypi/sphinxcontrib-rawfiles/
  * Although for now, this is working for what I need: http://www.sphinx-doc.org/en/1.5.1/config.html#confval-html_extra_path
* Looks very useful! http://sphinxcontribdatatemplates.readthedocs.io/en/latest/
* A good Sphinx table extension would be useful: https://github.com/sphinx-doc/sphinx/issues/786
* Not sure if this is useful! https://pythonhosted.org/sphinxcontrib-restbuilder/
* Maybe: https://pypi.python.org/pypi/sphinxcontrib-jsoncall
* Looks interesting, probably not useful here: https://jsdoc-toolkit-rst-template.readthedocs.io/en/latest/