from cache import CacheError, Cache
import hashlib
import requests

class CacheURL(Cache):

    def __url_to_hash(self, url:str) -> str:
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        return url_hash

    def get(self, url: str, **kwargs) -> str:
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
                raise CacheError(f'Error HTTP {response.status_code} al descargar {url}')
        except requests.exceptions.RequestException as e:
            raise CacheError(f'Error {e}')


    def exists(self, url: str, **kwargs) -> bool:
        url_hash = self.__url_to_hash(url)
        # Con super() redefino la clase padre
        return super().exists(url_hash)
    def load(self, url: str, **kwargs) -> str:
        url_hash = self.__url_to_hash(url)
        return super().load(url_hash)
    def how_old(self, url:str, **kwargs) -> float:
        url_hash = self.__url_to_hash(url)
        return super().how_old(url_hash)
    def delete(self, url: str, **kwargs) -> None:
        url_hash = self.__url_to_hash(url)
        super().delete(url_hash)