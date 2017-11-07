.. include:: ../references.rst

.. Details
.. =======

This page contains some notes with details about `gamma-cat`. 

Data
----

Reference identifiers
^^^^^^^^^^^^^^^^^^^^^

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

TODO: document properly.

For now, see the list of source classes we're using at the end of this schema file:

https://github.com/gammapy/gamma-cat/blob/master/input/schemas/basic_source_info.schema.yaml


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
