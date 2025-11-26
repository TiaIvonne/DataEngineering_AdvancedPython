from tests.conftest import temp_cache_dir
from traficFines.cache import Cache, CacheError, CACHE_DIR
from traficFines.cacheURL import CacheURL
import pytest

def test_cacheurl_init(temp_cache_dir):
    """ Test 1: Verifica inicializacion de cacheURL """
    cache_url = CacheURL('TestURL', obsolescence = 7, cache_dir = temp_cache_dir)
    assert cache_url.app_name == 'TestURL'
    assert cache_url.obsolescence == 7

