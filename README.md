# traficFines
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-red.svg)

## Tabla de Contenidos

1. [Descripción](#descripción)
2. [Rango de datos disponibles](#rango-de-datos-disponibles)
3. [Instalación](#instalación)
4. [Dependencias](#dependencias)
5. [Ejemplos de uso](#ejemplos-de-uso)
6. [Estructura del paquete](#estructura-del-paquete)
7. [Soporte](#soporte)
8. [Licencia](#licencia)

## Descripción
Este paquete está construido para analizar datos de multas del ayuntamiento de Madrid para una fecha especificada. El paquete descarga, guarda en caché, limpia y genera diferentes datasets y gráficos listos para ser utilizados.

## Rango de datos disponibles
Los datos están disponibles desde **2016** hasta el año actual. A la fecha de publicación de este paquete el último dataset disponible es junio de 2025. El paquete valida automáticamente que las fechas solicitadas estén en el rango indicado.

### Características del proyecto
- **Descarga** de datos desde el portal de datos abiertos de Madrid
- Incluye **sistema de caché** para evitar descargar archivos ya existentes
- **Limpieza** de datos
- **Generación** de gráficos
- Permite descargar especificando año y mes o solo año.

### Métodos principales
| Método | Descripción |
|--------|-------------|
| `add(year, month=None)` | Carga datos de un mes y año o de año completo.
| `fines_hour(fig_name)` | Genera gráfico de multas por hora |
| `fines_calification()` | Retorna DataFrame con distribución por calificación |
| `total_payment()` | Calcula recaudación máxima y mínima |

## Instalación

### Requisitos
- Python >= 3.8

### Desde el archivo .whl
```bash
pip install dist/traficfines-0.1.0-py3-none-any.whl
```

### Desde el código fuente
```bash
pip install -e .
```

## Dependencias

### Principales
- `requests>=2.28.0`: Descarga de contenido desde una URL seleccionada
- `beautifulsoup4>=4.11.0`: Parsing de HTML
- `pandas>=1.5.0`: Transformación y análisis de datos.
- `matplotlib>=3.5.0`: Generación de gráficos.

### Desarrollo
- `pdoc>=0.1.0`: Generación de documentación en formato HTML

### Instalación de dependencias
```bash
pip install -r requirements.txt
``` 

## Ejemplos de uso
```python
from traficFines import MadridFines
```
#### Crear instancia de MadridFines con caché de 7 días
```python
madrid = MadridFines("MadridFines", obsolescence = 7)
```
#### Cargar datos de año específico, el argumento mes es opcional, si no se indica se descargan los datos del año seleccionado.
```python
madrid.add(year = 2024)
```
#### Cargar datos de mes y año específico (Marzo del 2024)
```python
madrid.add(year=2024, month=3)
```
#### Crear gráfico de distribución de multas por mes y año
```python
madrid.fines_hour("grafico_multas.png")
```
#### Crear un dataframe de distribución de multas
```python
calificaciones = madrid.fines_calification()
print(calificaciones)
```

## Estructura del paquete

### Módulos Principales (`traficFines/`)
- `__init__.py`: Inicialización del módulo.
- `cache.py`: Implementación de clase Cache para gestión de archivos.
- `cacheURL.py`: Extensión de clase Cache con funcionalidades extra de descarga y almacenamiento de datos desde internet.
- `madridFines.py`: Análisis de multas de tráfico de Madrid.

### Tests (`tests/`)
- `test_cache.py`: Tests unitarios de la clase Cache.
- `test_cacheURL.py`: Tests unitarios de la clase CacheURL.
- `test_madrid_fines.py`: Tests unitarios de la clase MadridFines.
- `conftest.py`: Configuración de pytest.
- `data/`: Datos de prueba.

### Documentación (`docs_html/`)
La documentación completa está disponible en formato HTML generada desde docstrings.

### Distribución
- Archivos `.whl` y `tar.gz` para instalación del paquete.


## Soporte
Dudas o problemas:
- **Autor**: Ivonne Mendoza
- **Email**: ivonne@imendoza.io
- **GitHub**: https://github.com/TiaIvonne

## Licencia
Todos los derechos reservados

