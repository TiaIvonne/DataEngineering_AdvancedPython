from tests.conftest import temp_cache_dir
from traficFines.cache import Cache, CacheError, CACHE_DIR
from pathlib import Path
import pytest

# Comando para ejecutar pytest tests/test_cache.py -v

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
    Test 2: Verificar si esta usando el directorio por defecto para la aplicacion real
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
    Test 3: Verifica que set() crea el archivo en la ruta correcta
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
    """
    Test 4: Verifica que el atributo app_name es el correcto
    """
    assert cache_instance.app_name == "TestApp"
    assert isinstance(cache_instance.app_name, str)

def test_property_cache_dir(cache_instance, temp_cache_dir):
    """
    Test 5: Verifica que el atributo cache_dir es el correcto
    """
    assert cache_instance.cache_dir == temp_cache_dir
    assert isinstance(cache_instance.cache_dir, str)

def test_property_obsolescence(cache_instance):
    """
    Test 6: Verifica que el atributo obsolescence es el correcto
    """
    assert cache_instance.obsolescence == 7
    assert isinstance(cache_instance.obsolescence, int)

def test_set_creates_file(cache_instance):
    """
    Test 7: Verifica creacion del archivo en la ruta correcta
    """
    cache_instance.set('test.txt', 'Test content')
    assert cache_instance.exists('test.txt')
    assert cache_instance.load('test.txt') == 'Test content'

def test_exists_returns_false(cache_instance):
    """
    Test 8: Verifica que devuelva False en caso que el archivo no existe
    """
    assert not cache_instance.exists('inexistent_file.txt')

def test_load_existing_file(cache_instance):
    """
    Test 9: Verifica que el metodo load() carga el archivo
    """
    cache_instance.set('test.txt', 'Test content')
    assert cache_instance.load('test.txt') == 'Test content'

def test_load_non_existing_file(cache_instance):
    """
    Test 10: Verifica que se lanza una excepcion al invocar el metodo load con un archivo inexistente
    """
    # El uso de with lo encontre aqui.
    # https://stackoverflow.com/questions/23337471/how-do-i-properly-assert-that-an-exception-gets-raised-in-pytest
    with pytest.raises(CacheError):
        cache_instance.load('inexistent_file.txt')

def test_delete_file(cache_instance):
    """
    Test 11: Verifica que el archivo ha sido eliminado
    """
    cache_instance.set('test.txt', 'Test content')
    cache_instance.delete('test.txt')
    assert not cache_instance.exists('test.txt')





