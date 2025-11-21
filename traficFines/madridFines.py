# Ivonne Mendoza
# ivonne@imendoza.io
# Implementacion de MadridFines

from typing import Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd
from cacheURL import CacheURL
from io import StringIO

# Constantes fuera de la clase
RAIZ = "https://datos.madrid.es/"
MADRID_FINES_URL = "sites/v/index.jsp?vgnextoid=fb9a498a6bdb9410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD"

class MadridError(Exception):
    """ Implementación de errores para la clase MadridFines """
    pass

# Función fuera de la clase MadridFines
def get_url(year:int, month:int) -> str:
    """
    Obtiene un link de descarga de la página del ayuntamiento según año y mes especificado
    Args:
        year: año buscado
        month: mes buscado
    Return:
        Una url con el link de descarga correspondiente al archivo csv de ese año y mes especificado
    Raises:
        MadridError
        Si hay errores al obtener la url (código diferente a 200)
        Si hay fechas que no existen en el link url
    """
    # Valida que los meses esten entre 1 y 12
    if not 1 <= month <= 12:
        raise MadridError(f"Mes invalido: {month}, debe estar entre 1 y 12")

    # Concatena para formar una url
    url = f'{RAIZ}{MADRID_FINES_URL}'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f'Error al obtener la URL: {response.status_code}')
    soup = BeautifulSoup(response.text, 'html.parser')

    # Obtiene todos los tags de la url que contengan 'li'
    listas = soup.find_all('li')

    # Crea diccionario que traduce el número del mes a un string adecuado, el formato de fecha del sitio es 2025 Junio
    dict_months = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio',
                   8:'Agosto', 9:'Septiembre',10:'Octubre', 11:'Noviembre', 12:'Diciembre'}

    # Crea un string acorde al formato que pide la url
    date_string = f'{year} {dict_months[month]}'

    # Recorre todos los tags li y busca los links asociados de href
    for li in listas:
        titulo = li.find('p', class_='info-title')
        if titulo and date_string in titulo.text:
            h_ref = li.find('a', class_='asociada-link').get('href')
            url_file = f'{RAIZ}{h_ref}'
            return url_file
    raise MadridError(f"No se encontro archivo para la fecha {date_string}")


class MadridFines:
    """
    Implementacion de la clase MadridFines
    Methods:
        __init__: constructor de la clase
        __load: Usa cacheurl para acceder a los datos de la aplicacion y crear un df, estatico y privado
        __clean: limpia el dataframe creado en __load, estatico y privado
        add: agrega datos de mes y anio al dataframe actual

    """
    def __init__(self, app_name:str, obsolescence:int):
        """
        Constructor de la clase MadridFines
        Args:
            app_name: nombre del directorio del cache de la aplicacion
            obsolescence: dias que los datos de la cache son validos
        Attributes:
            __cacheurl(CacheURL): gestor de la cache, privado
            __data(pd.DataFrame): DataFrame vacio para inicializar datos, privado
            __loaded: Lista vacia que guarda tuplas con el formato mes y anio, privado
        """
        self.__cacheurl = CacheURL(app_name, obsolescence)
        self.__data = pd.DataFrame() # inicializa vacio
        self.__loaded = [] # inicializa lista vacia


    @staticmethod
    def __load(year:int, month:int, cacheurl)->pd.DataFrame:
        """
        Metodo interno y estatico que usa cacheurl para acceder a los datos del anio y mes
        creando un dataframe de pandas
        Args:
            year: anio buscado
            month: mes buscado
            cacheurl: URL de la cache
        Returns:
            un dataframe de pandas con la informacion de las multas del anio y mes indicado
        Raises:
            MadridError
            Si hay problemas al parsear en csv en el apartadi try/except
        """
        # Invoca a get_url para obtener la url del archivo correspondiente al anio y mes
        url = get_url(year, month)
        # Obtiene el texto asociado a esa url
        csv_text = cacheurl.get(url)
        # Convierte el texto o string a data frame
        # forma mas simple directo a data frame
        # df = pd.read_csv(StringIO(csv_text), sep=';', encoding='utf8')

        try:
            df = pd.read_csv(
                StringIO(csv_text), sep=';', encoding='latin-1', low_memory=False)
            return df
        except Exception as e:
            raise MadridError(f"Problema al parsear CSV de {month} y {year}: {e}")

    @staticmethod
    def __clean(df:pd.DataFrame)-> None:
        """
        Metodo que limpia el dataframe de pandas creado en load (elimina espacios, convierte a numero,
        cambia formato de nombres de columnas
        Args:
            df: dataframe de pandas
        Returns:
            None
        Raises:

        """
        # Constantes de configuracion si se necesitan mas se agregan aqui
        text_columns = ['CALIFICACION','DESCUENTO', 'HECHO_BOL', 'DENUNCIANTE', 'LUGAR']
        numeric_s_columns = ['VEL_LIMITE', 'VEL_CIRCULA']
        numeric_direct = ['COORDENADA_X', 'COORDENADA_Y']
        # Elimina espacios en blanco de los nombres de las columnas
        df.rename(columns=lambda x: x.strip(), inplace=True)

        # Normalizar guiones de los nombres de las columnas
        df.columns = df.columns.str.replace('-', '_')

        #Limpia espacios en blanco de la columna calificacion
        df[text_columns] = df[text_columns].apply(lambda x: pd.Series(x.str.strip()))

        # Transforma de string a numerico las columnas indicadas
        df[numeric_s_columns] = df[numeric_s_columns].apply(lambda x: pd.to_numeric(x.str.strip(), errors='coerce'))

        # Mismo caso con las coordenadas
        df[numeric_direct] = df[numeric_direct].apply(pd.to_numeric, errors='coerce')

        # Crea la columna fecha
        df['FECHA'] = pd.to_datetime({
            'year': df['ANIO']
            , 'month': df['MES']
            , 'day': 1
            , 'hour': df['HORA'].astype(int)
            , 'minute': ((df['HORA'] - df['HORA'].astype(int)) * 100).astype(int)
        })

        # Cambio el formato de fecha a dia mes anio mas la hora
        df['FECHA'] = df['FECHA'].dt.strftime('%d/%m/%Y %H:%M:%S')

        # Setea fecha como indice y con esto la columna fecha desaparece automaticamente
        df.set_index('FECHA', inplace=True)

        # Convierto indice a DateTimeIndex
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index, format='%d/%m/%Y %H:%M:%S')


    def add(self, year: int, month: Optional[int] = None) -> None:
        pass


