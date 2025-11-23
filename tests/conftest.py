# Ivonne Mendoza
# ivonne@imendoza.io
# Fixtures compartidas para test

import pytest
import tempfile
import shutil
import sys
from pathlib import Path



# agrega el directorio padre para traer el paquete
sys.path.insert(0,str(Path(__file__).parent.parent))
from traficFines.cache import Cache

# Nota para los profesores: Esta parte de la creacion de directorio lo hice con ayuda de cursor
@pytest.fixture
def temp_cache_dir():
    """
    Crea un directorio temporal para los tests
    Se limpia automáticamente después de cada test
    Cada test tiene su propio directorio
    """
    test_dir = tempfile.mkdtemp()
    yield test_dir
    shutil.rmtree(test_dir, ignore_errors=True)


@pytest.fixture
def cache_instance(temp_cache_dir):
    """
    Crea una instancia de Cache lista para usar
    """
    return Cache("TestApp", obsolescence=7, cache_dir=temp_cache_dir)

