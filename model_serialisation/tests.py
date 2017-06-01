"""
Some tests for model serialisation.

Goal: better spectral model handling / schema.
"""
from pathlib import Path
from pprint import pprint
from jsonschema import validate
from ruamel.yaml import safe_load

MODEL_PATH = Path(__file__).parent / 'models'
SCHEMA_PATH = Path(__file__).parent / 'schema.yaml'


def test_pl_read():
    path = MODEL_PATH / 'power_law.yaml'
    data = safe_load(path.open())['spectrum']
    schema = safe_load(SCHEMA_PATH.open())['power_law']
    # pprint(data)
    # pprint(schema)
    validate(data, schema)


def test_spectral_models():
    path = Path(__file__).parent / 'spectral_models.yaml'
    data = safe_load(path.open())
    pprint(data)


if __name__ == '__main__':
    # test_pl_read()
    test_spectral_models()
