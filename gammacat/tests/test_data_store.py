"""
This is an API proposal how `gamma-cat` data access should work.

Python API
----------

The major ideas here are:

* We provide a small Python API that gives access to all data
  from gamma-cat in common ways people want to access the data
  in the simplest way possible.
* The underlying implementation in code and files is not exposed.
  For now we use JSON files as index files.
  In the future we might change to some more fancy linked data standard
  (see http://stackoverflow.com/questions/41544384/python-json-api-for-linked-data-with-flat-files )
* API first means it's easy to use.
  Tests make sure it keeps working as we change the implementation.

Use cases
---------

List of things
++++++++++++++

Users should be able to do common queries what's available:

* List all `source_id`
* List all `reference_id`
* List all `sed`
* List all `lc`

* For given `source_id`, list all `reference_id`, `sed`, `lc`
* For a given `reference_id`, list all `source_id`, `sed`, `lc`

Access data
+++++++++++

* Get basic info for a given `source_id`
* Get basic info for a given `reference_id`

* For given `source_id`, list all `reference_id`, `sed`, `lc`
* For a given `reference_id`, list all `source_id`, `sed`, `lc`




Implementation
--------------

* Like http://jsonapi.org/ but with static JSON files.


We should generate the following files:

* /gammacat-datastore.json
  * Some metadata and links to other datafiles.
* /sources/
  * {source_id}/info.json



TODO: implement this functionality!
"""
import pytest
from gammacat.data_store import GammaCatDataStore


def test_load():
    """
    Use case: create a data store.

    TODO: more fancy ways to create a datastore,
    e.g. for an older version, or by fetching a zip file from the web, ...
    """
    ds = GammaCatDataStore.from_index_file()

    assert 'version' in ds.info()


@pytest.mark.skip
def test_get_source():
    ds = GammaCatDataStore()
    source = ds.get('/sources/{source_id}')


@pytest.mark.skip
def test_get_source():
    ds = GammaCatDataStore()
    source = ds.get('/sources/{source_id}')
