from tests.conftest import temp_cache_dir, madrid_instance
from traficFines.madridFines import MadridFines, MadridError
import pytest
from pathlib import Path
import pandas as pd


def test_init_madridFines(madrid_instance):
    """ Test 1: Verifica que la instancia de madridFines ha sido creada"""
    assert madrid_instance._MadridFines__data.empty
    assert madrid_instance._MadridFines__loaded == []

def test_add_new_files(madrid_instance, temp_cache_dir):
    """ Test 2: Verifica que el metodo add() crea archivos de madridFines """

    cache_dir_path = Path(temp_cache_dir)

    # Contar archivos antes (debería ser 0 en directorio temporal)
    c_before = len([f for f in cache_dir_path.iterdir() if f.is_file()]) if cache_dir_path.exists() else 0

    # Llama al metodo add()
    madrid_instance.add(year=2024, month=4)

    # Valida si se ha creado un archivo
    c_after = len([f for f in cache_dir_path.iterdir() if f.is_file()])

    assert c_after > c_before

def test_add_no_duplicates(madrid_instance):
    """ Test 3: Verificar que add() no recargue datos ya cargados """
    # Cargamos el mismo mes dos veces
    madrid_instance.add(year=2024, month=5)
    loaded_before = len(madrid_instance._MadridFines__loaded)
    num_rows_before = len(madrid_instance._MadridFines__data)

    # Cargamos de nuevo
    madrid_instance.add(year=2024, month=5)
    loaded_after = len(madrid_instance._MadridFines__loaded)
    num_rows_after = len(madrid_instance._MadridFines__data)

    # Verifica que no se carguen duplicados
    assert loaded_before == loaded_after
    assert num_rows_before == num_rows_after

def test_fines_hour_raises_error_no_data(madrid_instance):
    """ Test 4: Verifica que fines_hour() lanza una excepcion si no hay datos encontrados"""
    with pytest.raises(MadridError):
        madrid_instance.fines_hour('test.png')

def test_fines_calification_returns_df(madrid_instance):
    """ Test 5: Verifica que el metodo fines_calification() retorna un df """
    madrid_instance.add(year=2024, month=6)
    califications = madrid_instance.fines_calification()
    assert isinstance(califications, pd.DataFrame)

def test_total_payment_returns_df(madrid_instance):
    """ Test 6: Verifica que total_payment() retorna un df """
    madrid_instance.add(year=2024, month=7)
    total_payments = madrid_instance.total_payment()
    assert total_payments is not None
    assert 'rec_maxima' in total_payments.columns
    assert 'rec_minima' in total_payments.columns
    assert isinstance(total_payments, pd.DataFrame)

def test_add_raises_error_invalid_year(madrid_instance):
    """ Test 7: Verifica que lance un error si el anio esta fuera de rango"""
    with pytest.raises(MadridError):
        madrid_instance.add(year=1990)

def test_deal_with_multiple_months_data(madrid_instance):
    """ Test 8: Verifica que los datos de varios meses han sido cargados en la aplicacion"""
    madrid_instance.add(year=2025, month=1)
    madrid_instance.add(year=2025, month=2)
    madrid_instance.add(year=2025, month=3)

    # Verifica los meses cargados
    assert (1,2025) in madrid_instance._MadridFines__loaded
    assert (2,2025) in madrid_instance._MadridFines__loaded
    assert (3,2025) in madrid_instance._MadridFines__loaded
