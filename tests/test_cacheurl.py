from tests.conftest import temp_cache_dir
from traficFines.cache import Cache, CacheError, CACHE_DIR
from traficFines.cacheURL import CacheURL
import pytest

def test_cacheurl_init(temp_cache_dir):
    """ Test 1: Verifica inicializacion de cacheURL """

    cache_url = CacheURL('TestURL', obsolescence = 7, cache_dir = temp_cache_dir)
    assert cache_url.app_name == 'TestURL'
    assert cache_url.obsolescence == 7

def test_cacheurl_get_downloads(cacheurl_instance):
    """Test 2: Verifica que el metodo get() descarga y guarda usando URL real  """

    url = "https://www.example.com"
    content = cacheurl_instance.get(url)

    # Verificaciones
    assert len(content) > 0
    assert cacheurl_instance.exists(url)

def test_cacheurl_get_use_cache(cacheurl_instance):
    """ Test 3: Verificar que se utiliza la cache"""

    url = "https://example.com"
    content1 = cacheurl_instance.get(url)
    assert len(content1) > 0

    # Second call
    content2 = cacheurl_instance.get(url)

    assert content1 == content2
    assert cacheurl_instance.exists(url)

def test_cacheurl_get_handles_invalid_domain(cacheurl_instance):
    """ Test 4: Verifica que se lance una exception si la URL no funciona"""

    with pytest.raises(CacheError):
        cacheurl_instance.get("https://no-soy-un-sitio.com")


