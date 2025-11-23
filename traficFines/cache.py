# Ivonne Mendoza
# ivonne@imendoza.io
# Implementa la clase Cache para manejo de archivos
# Comentarios en espaniol, errores nombres de variables y resto ingles

from pathlib import Path
import os
import time

# Constante
CACHE_DIR = Path.home() / ".my_cache"

class CacheError(Exception):
    """
    Excepcion que se lanza cuando falla una operacion de cache
    Indica errores durante la lectura, escritura o distribucion de los archivos

    Example:
        >>> raise CacheError("Cannot write the file")
    """
    pass

class Cache:
    """
    Esta clase almacena y recupera datos de un directorio designado como cache, con validacion de antiguedad de archivos

    Attributes:
        __app_name (str): Nombre del directorio donde se desea guardar archivos en cache
        __obsolescence (int): Numero de dias que un archivo en cache sigue siendo valido
        __cache_dir (str): Ruta completa del subdirectorio que se crea en .my_cache. Por defecto va en ~/.my_cache/<app_name>

    Example:
        >>> cache = Cache("mi app", obsolescence=5)
        >>> cache.set('datos', 'contenido')
    """
    def __init__(self, app_name:str, obsolescence:int, cache_dir:str=None)->None:
        self.__app_name = app_name
        self.__cache_dir = cache_dir or str(CACHE_DIR/ app_name)
        self.__obsolescence = obsolescence

    #@property is used to get the value of a private attribute without using any getter methods. \
    #We have to put a line @property in front of the method where we return the private variable.

    """
    Use property to get the private attributes
    """
    @property
    def app_name(self)->str:
        return self.__app_name

    @property
    def cache_dir(self)->str:
        return self.__cache_dir

    @property
    def obsolescence(self)->int:
        return self.__obsolescence

    def __get_file_path(self, name:str)->Path:
        """
        Metodo auxiliar privado que obtiene la ruta del archivo

        Args:
            name (str): nombre del archivo
        Returns:
            Path: /Users/ivonney/.my_cache/MadridFines/dic_2024.csv
        """
        return Path(self.__cache_dir) / name

    # Metodos de la clase Cache
    def set(self, name:str, data:str)->None:
        """
        Metodo para almacenar datos en cache

        Args:
            name (str): nombre del archivo
            data (str): contenido del mismo
        Raises:
            CacheError: Si no puede escribir el archivo
        """
        # Creates directories if they don't exist
        cache_path = Path(self.__cache_dir) 
        cache_path.mkdir(parents=True, exist_ok=True)

        # Creates the file path``
        file_path = self.__get_file_path(name)

        # Write data content to file
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)
        except Exception as e:
            raise CacheError(f"Error: Cannot WRITE the file {name}: {e}")

    def exists(self, name:str)->bool:
        """
        Metodo para comprobar si existe un archivo en cache.

        Args:
            name (str): nombre del archivo
        Returns:
            bool: Si existe o no el nombre de un archivo en cache
        """
        return self.__get_file_path(name).exists()

    def load(self, name:str)->str:
        """
        Metodo que recupera los datos almacenados en cache.

        Args:
            name: nombre del archivo
        Returns:
            str: Datos del archivo
        Raises:
            CacheError: Si el archivo no existe
            CacheError: Si el archivo no se puede leer
        """
        # Build the file path
        file_path = self.__get_file_path(name)
        if not file_path.exists():
            raise CacheError(f"File {name} does not exist")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise CacheError(f"Error to WRITE {name}: {e}")

    def how_old(self, name:str)->float:
        """
        Metodo que calcula en milisegundos la edad de un archivo

        Args:
            name (str): nombre del archivo
        Returns:
            float: La edad del archivo en milisegundos
        Raises:
            CacheError: Si el archivo no existe
        """
        file_path = self.__get_file_path(name)
        if not file_path.exists():
            raise CacheError(f"File {name} does not exist")
        # Calcular el timestamp
        calc_time = os.path.getmtime(file_path)
        current_time = time.time()
        age_seconds = current_time - calc_time
        #Returns age in miliseconds
        return age_seconds * 1000

    def delete(self, name:str)-> None:
        """
        Metodo que elimina UN archivo en cache

        Args:
            name (str): nombre del archivo
        """
        file_path = self.__get_file_path(name)
        # https://stackoverflow.com/questions/42636018/python-difference-between-os-remove-and-os-unlink-and-which-one-to-use
        if file_path.exists():
            file_path.unlink()
    
    def clear(self)->None:
        """
        Metodo que elimina todos los archivos en el directorio especificado

        Warning:
            Operacion irreversible, se eliminan todos los datos
        """
        cache_path = Path(self.__cache_dir)
        if cache_path.exists():
            for file in cache_path.iterdir():
                if file.is_file():
                    file.unlink()


