from tests.conftest import temp_cache_dir
from traficFines.cache import Cache, CacheError, CACHE_DIR
from pathlib import Path


def test_init_basic(cache_instance, temp_cache_dir):
    """
    Test 1: Verificar inicialización básica de Cache
    Utiliza las propiedades del fixture para verificar
    """
    # Verificar tipos de datos
    assert cache_instance.app_name == "TestApp"
    assert isinstance(cache_instance.app_name, str)

    # Verifica valores para obsolescence 
    assert cache_instance.obsolescence == 7
    assert isinstance(cache_instance.obsolescence, int)

    # Verifica que el directorio de cache sea el correcto
    assert cache_instance.cache_dir == temp_cache_dir
    assert isinstance(cache_instance.cache_dir, str)

def test_init_basic_no_cache():
    """
    Verificar si esta usando el directorio por defecto para la aplicacion real
    No usa fixture, crea una instancia propia para comprobar el directorio base
    """
    app_name = "MiApp"
    cache = Cache("MiApp", obsolescence=5)
    route = str(CACHE_DIR / app_name)
    assert cache.cache_dir == route
    assert cache.app_name == app_name
    assert cache.obsolescence == 5

'''
__get_file_path es un metodo prvado y no se debe testear directamente. 
Se debe testear en un metodo publico que lo use
'''
def test_creates_file_correct(cache_instance, temp_cache_dir):
    """
    Verifica que set() crea el archivo en la ruta correcta
    """

    # Preparar el ambiente de prueba
    file_name = 'test.txt'
    content = 'Test content'

    # Llamar a set que de forma interna usa __get_file_path
    cache_instance.set(file_name, content)

    route = Path(temp_cache_dir) / file_name
    # Verificaciones con assert
    assert route.exists()
    assert route.read_text() == content
    assert str(temp_cache_dir) in str(route)

# Se deben testear los atributos de la clase, son privados pero con @property accedemos a ellos
def test_property_app_name(cache_instance):
    assert cache_instance.app_name == "TestApp"
    assert isinstance(cache_instance.app_name, str)

def test_property_cache_dir(cache_instance, temp_cache_dir):
    assert cache_instance.cache_dir == temp_cache_dir
    assert isinstance(cache_instance.cache_dir, str)

def test_property_obsolescence(cache_instance):
    assert cache_instance.obsolescence == 7
    assert isinstance(cache_instance.obsolescence, int)


