# Ivonne Mendoza
# ivonne@imendoza.io
# Implementacion de CacheURL que gestiona archivos extraidos de internet

from .cache import CacheError, Cache
import hashlib
import requests

class CacheURL(Cache):
    """
    La clase CacheURL esta creada para manejar datos extraiddos de internet
    Extiende la clase Cache agregando funcionalidades para descargar y guardar datos de internet
    """
    @staticmethod
    def __url_to_hash(url:str) -> str:
        """
        Convierte la url en un string de tipo hash para facilitar su acceso posterior

        Args:
            url (str): url de internet
        Returns:
            str: Hash MD5 en hexadecimal de 32 caracteres
        """
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        return url_hash

    def get(self, url: str, **kwargs) -> str:
        """
        Descarga el contenido especificado de una URL de internet

        Args:
            url (str): url de internet
        Returns:
            str: el contenido de la url especificada.
        Raises:
            CacheError: Si el status code de response es diferente a 200
        """
        url_hash = self.__url_to_hash(url)
        if self.exists(url):
            return self.load(url)

        # Descarga de internet
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                self.set(url_hash, response.text)
                return response.text
            else:
                raise CacheError(f'Error HTTP {response.status_code} to download {url}')
        except requests.exceptions.RequestException as e:
            raise CacheError(f'Error {e}')

    # Seccion que sobreescribe metodos de la clase padre
    def exists(self, url: str, **kwargs) -> bool:
        """
        Comprueba si los datos de la URL existen en cache
        Sobreescribe el metodo de la clase padre para aceptar url en vez de nombres de archivo y los convierte a hash.

        Args:
            url (str): url de internet
            **kwargs: Argumentos adicionales
        Returns:
            bool: True si existe en cache o False en caso contrario
        """
        url_hash = self.__url_to_hash(url)
        # Con super() redefino la clase padre, super accede a la clase padre reusando logica
        return super().exists(url_hash)

    def load(self, url: str, **kwargs) -> str:
        """
        Recupera los datos ya existentes en cache.
        Transforma la url a hash y carga
        Sobreescribe el metodo de la clase padre para aceptar url

        Args:
            url (str): url de internet
            **kwargs: Argumentos adicionales
        Returns:
            str: El contenido de la url especificada pasada a hash
        """
        url_hash = self.__url_to_hash(url)
        return super().load(url_hash)

    def how_old(self, url:str, **kwargs) -> float:
        """
        Calcula la antiguedad de un archivo en cache
        Sobreescribe el metodo de la clase padre para aceptar url en vez de nombres de archivo

        Args:
            url (str): url de internet
            **kwargs: Argumentos adicionales
        Returns:
            float: Antiguedad de un archivo
        """
        url_hash = self.__url_to_hash(url)
        return super().how_old(url_hash)

    def delete(self, url: str, **kwargs) -> None:
        """
        Elimina el contenido de un archivo en cache
        Sobreescribe el metodo de la clase padre para aceptar url en vez de nombres de archivo

        Args:
            url (str): url de internet
            **kwargs: Argumentos adicionales
        """
        url_hash = self.__url_to_hash(url)
        super().delete(url_hash)