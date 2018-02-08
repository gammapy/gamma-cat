.. include:: ../references.rst

Why? There's already TeVCat!
----------------------------

Yes, there is `TeVCat`_ .

But TeVCat isn't really open.

You can view the info on their webpage, and copy & paste individual
numbers, but you can't download a catalog and use it for your research.

To quote http://tevcat.uchicago.edu/terms.html (accessed August 26, 2016):

.. pull-quote::

    | Users may not perform systematic downloads of TeVCat data for any purpose,
    | whether commercial or not, without the written permission of the
    | TeVCat team.  This includes scripted parsing of the website data,
    | webpage 'scraping', and the use of robots. If you need access to bulk
    | TeVCat data products, please contact the TeVCat team at tevcat@gmail.com

A second major problem with TeVCat is that there's no version history.
Updates and corrections happen, but only the maintainers know when
that happens and (presumably) what the older values were.

The goal here is to have a fully open TeV catalog that you can download
and use as you like (well, we still require attribution, see next section).

The data here is maintained as text (YAML and ECSV) files in a git repo on Github
following the model of `astrocats`_, so it's fully transparent
and we have version history.

The concrete motivation for Christoph Deil to start this catalog in
August 2016 was to have a TeV catalog for `gamma-sky.net`_,
as well as for checks of all sources in the H.E.S.S. Galactic plane
survey catalog against previous publications, and to have a TeV
source catalog available for the upcoming CTA science challenge.

Open and reproducible research for gamma-ray astronomy!