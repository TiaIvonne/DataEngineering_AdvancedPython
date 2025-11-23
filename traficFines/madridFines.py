# Ivonne Mendoza
# ivonne@imendoza.io
# Implementacion de MadridFines

from typing import Optional
from bs4 import BeautifulSoup
from .cacheURL import CacheURL # import relativo busca en el paquete
import requests
import pandas as pd
from io import StringIO
import datetime
import matplotlib.pyplot as plt

# Constantes fuera de la clase
RAIZ = "https://datos.madrid.es/"
MADRID_FINES_URL = "sites/v/index.jsp?vgnextoid=fb9a498a6bdb9410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD"

class MadridError(Exception):
    """
    Implementación de errores para la clase MadridFines
    Example:
        >>> raise MadridError("Error al obtener la url")
    """
    pass

# Función fuera de la clase MadridFines
def get_url(year:int, month:int) -> str:
    """
    Obtiene un link de descarga de la página del ayuntamiento según año y mes especificado

    Args:
        year (int): año buscado
        month (int): mes buscado
    Returns:
        str: Una url con el link de descarga correspondiente al archivo csv de ese año y mes especificado
    Raises:
        MadridError: Si hay errores al obtener la url (código diferente a 200)
        MadridError: Si hay fechas que no existen en el link url
    """
    # Valida anio
    # Esto esta harcodeado 2016 buscar alternativa
    if not (2016 <= year <= datetime.date.today().year):
        raise MadridError(f"Anio fuera de rango: {year}")

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

    Descarga, almacena en cache y procesa los datos de multas de Madrid, utilizando sistema de cache de gestion de datos.

    Attributes:
        __cacheurl(CacheURL): gestor de la cache.
        __data (pd.DataFrame): DataFrame vacio para inicializar datos
        __loaded (list): Lista que guarda tuplas con el formato mes y anio
    """
    def __init__(self, app_name:str, obsolescence:int):
        """
        Constructor de la clase MadridFines

        Args:
            app_name (str): nombre del directorio del cache de la aplicacion
            obsolescence (int): dias que los datos de la cache son validos
        """
        self.__cacheurl = CacheURL(app_name, obsolescence)
        self.__data = pd.DataFrame() # inicializa vacio
        self.__loaded = [] # inicializa lista vacia


    @staticmethod
    def __load(year:int, month:int, cacheurl:CacheURL)->pd.DataFrame:
        """
        Metodo interno y estatico que usa cacheurl para acceder a los datos del anio y mes
        creando un dataframe de pandas.

        Args:
            year (int): anio buscado
            month (int): mes buscado
            cacheurl (CacheURL): URL de la cache
        Returns:
            pd.Dataframe: un dataframe de pandas con la informacion de las multas del anio y mes indicado
        Raises:
            MadridError: Si hay problemas al parsear en csv en el apartado try/except
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
        cambia formato de nombres de columnas.

        Args:
            df (pd.DataFrame): dataframe de pandas
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
        """
        Agrega multas de un mes o anio especificado al dataset

        Args:
            year (int): anio buscado
            month (int): mes buscado, opcional. Si no se especifica mes, carga el anio completo
        Raises:
            MadridError: en caso de ingresar un mes que no existe en el rango 1 a 12
            MadridError: en caso de ingresar un anio fuera de rango (2016, anio actual)
        """
        # Valida el mes
        if month is not None and not (1 <= month <= 12):
            raise MadridError(f'Mes invalido: {month}')

        if not (2016 <= year <= datetime.date.today().year):
            raise MadridError(f'Anio fuera de rango: {year}')

        if month is None:
            months = list(range(1, 13))
        else:
            months = [month]

        for m in months:
            if(m, year) not in self.__loaded:
                df_new = self.__load(year, m, self.__cacheurl)
                self.__clean(df_new)
                self.__data = pd.concat([self.__data, df_new], ignore_index=False)
                self.__loaded.append((m, year))

    def fines_hour(self, fig_name: str) -> None:
        """
        Metodo que genera un grafico a partir de los datos previamente guardados con las multas por hora y fecha

        Args:
            fig_name (str): Nombre del grafico
        Raises:
             MadridError en caso de no existir datos cargados
        """
        if self.__data.empty:
            raise MadridError(f'Datos no encontrados')

        # Crea un dataset temporal extrayendo hora, mes y año del indice
        temp_multas = self.__data.copy()
        temp_multas['horas'] = temp_multas.index.hour
        temp_multas['mes'] = temp_multas.index.month
        temp_multas['anio'] = temp_multas.index.year
        temp_multas['anio_mes'] = temp_multas['anio'].astype(str) + '-' + temp_multas['mes'].astype(str).str.zfill(2)

        # Agrupa los resultados por hora, año y mes
        multas_horas = temp_multas.groupby(['horas', 'anio_mes']).size().reset_index(name='Multas')

        # Crear tabla pivote, los años-meses pasan a ser columnas y se reagrupa para hacer mas facil el grafico
        data_pivot = multas_horas.pivot(index='horas', columns='anio_mes', values='Multas')

        # Crea el grafico
        plt.figure(figsize=(10, 6))
        data_pivot.plot(marker = 'o', linewidth = 2)
        plt.title('Evolucion de multas por hora')
        plt.xlabel('Horas')
        plt.ylabel('Numero de multas')
        plt.legend(title='Año-Mes', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(fig_name)
        plt.show()
        plt.close()

    def fines_calification(self) -> pd.DataFrame:
        """
        Analiza la distribucion de multas por calificacion, mes u anio

        Returns:
            pd.Dataframe: Un dataframe con la distribucion de multas por calificacion
        Raises:
            MadridError en caso de no existir datos cargados
        """
        if self.__data.empty:
            raise MadridError(f'Datos no encontrados')

        temp_calif = self.__data.copy()
        res = temp_calif.groupby(['MES', 'ANIO', 'CALIFICACION']).size().reset_index(name='count')

        # Crea la tabla pivot
        res_pivot = res.pivot_table(
            index=['MES', 'ANIO'],
            columns='CALIFICACION',
            values='count',
            fill_value=0
        )

        return res_pivot

    def total_payment(self) -> pd.DataFrame:
        """
        Genera un resumen del importe total tanto valor normal como minmo para un mes y anio

        Returns:
            pd.Dataframe: Un dataframe con la recaudacion normal y minima de las multas
        Raises:
            MadridError en caso de no existir datos cargados
        """
        if self.__data.empty:
            raise MadridError(f'Datos no encontrados')

        total_payment = self.__data.copy()
        # La recaudacion minima tb se puede calcular por fuera y agregarlo despues al dataset pero queria probar mas con lambda
        total = total_payment.groupby(['MES', 'ANIO']).agg(
            rec_maxima=('IMP_BOL', 'sum'),
            rec_minima=('IMP_BOL', lambda x: x.sum() * 0.5)

        ).reset_index()

        return total

