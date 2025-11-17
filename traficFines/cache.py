# Ivonne Mendoza
# ivonne@imendoza.io

from pathlib import Path
import os
import time

class CacheError(Exception):
    """
    Implementa errores para la clase Cache
    """
    pass
#todo: test this class
#todo: test the methods
#todo: test the properties
#todo: test the exceptions
#todo: test the cache directory
#todo: test the cache file
#todo: test the cache file path
#todo: test the cache file content

class Cache:
    """
    Implementacion de la clase Cache
    """
    def __init__(self, app_name:str, obsolescence:int, cache_dir:str=None)->None:
        self.__app_name = app_name
        self.__cache_dir = cache_dir or str(Path.home() / ".my_cache" / app_name)
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

    # Metodo auxiliar privado que obtiene la ruta del archivo
    def __get_file_path(self, name:str)->Path:
        """
        Retorna: /Users/ivonney/.my_cache/MadridFines/dic_2024.csv
        """
        return Path(self.__cache_dir) / name


    # Metodos de la clase Cache
    def set(self, name:str, data:str)->None:
        """
        Metodo para almacenar datos en cache
        name: nombre del archivo
        data: contenido del mismo
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
        Metodo para comprobar si existe un archivo en cache
        """
        return self.__get_file_path(name).exists()

    def load(self, name:str)->str:
        """
        Metodo que recupera los datos almacenados en cache
        name: nombre del archivo
        return: datos del archivo
        """
        # Build the file path
        file_path = self.__get_file_path(name)
        if not file_path.exists():
            raise CacheError(f"Archivo {name} no existe")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise CacheError(f"Error al LEER el archivo {name}: {e}")

    def how_old(self, name:str)->float:
        """
        Metodo que calcula en milisegundos la edad de un archivo
        """
        file_path = self.__get_file_path(name)
        if not file_path.exists():
            raise CacheError(f"Archivo {name} no existe")
        # Calcular el timestamp
        calc_time = os.path.getmtime(file_path)
        current_time = time.time()
        age_seconds = current_time - calc_time
        #Returns age in miliseconds
        return age_seconds * 1000

    def delete(self, name:str)-> None:
        """
        Metodo que elimina UN archivo en cache

        """
        file_path = self.__get_file_path(name)
        # https://stackoverflow.com/questions/42636018/python-difference-between-os-remove-and-os-unlink-and-which-one-to-use
        if file_path.exists():
            file_path.unlink()
    
    def clear(self)->None:
        """
        Metodo que elimina todos los archivos en el directorio especificado

        """
        cache_path = Path(self.__cache_dir)
        if cache_path.exists():
            for file in cache_path.iterdir():
                if file.is_file():
                    file.unlink()


