from gammacat.data_store import GammaCatDataStore


def test_init():
    ds = GammaCatDataStore.from_file()
    ds.info()
