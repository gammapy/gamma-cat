.. include:: ../references.rst

.. Status
.. ======

Here you can find information about which sources are known to gamma-cat and what data we already have about them.

Gamma-cat sources
=================

The following sources are known to gamma-cat:

{% for src in data %}
* `{{src.common_name}} <sources/source{{ src.source_id}}.html>`__
{% endfor %}