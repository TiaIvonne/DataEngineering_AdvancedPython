# Ivonne Mendoza
# ivonne@imendoza.io


class Cache(str):
    """
    Implementacion de la clase Cache
    """
    def __init__(self):
        self.__app_name = str
        self.__cache_dir = str
        self.__obsolescence = int

    def set(self, name:str, data:str)-> None:
        pass
    def exist(self, name:str)-> bool:
        pass
    def how_old(self, name:str)-> float:
        pass

    def delete(self, name:str)-> None:
        pass
    def clear(self)-> None:
        pass

class CacheUrl:
    def get(self, url:str)-> str:
        pass
    def exist(self, url:str, **kwargs)-> bool:
        pass
    def load(self, url:str, **kwargs)-> str:
        pass
    def how_old(self, url:str,**kwargs)-> float:
        pass
    def delete(self, url:str, **kwargs)-> None:
        pass