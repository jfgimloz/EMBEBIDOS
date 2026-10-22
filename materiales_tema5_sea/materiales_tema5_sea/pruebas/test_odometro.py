"""Alternativa pytest a test_odometro.c: mismo núcleo C, 5 casos y 14 aserciones.

Desde la raíz del paquete: python3 -m pytest -q pruebas/test_odometro.py
Requiere GCC y pytest. Compila únicamente el núcleo en un directorio temporal.
"""
import ctypes as ct
from pathlib import Path
import subprocess

import pytest


class Odometro(ct.Structure):
    # Debe coincidir con comun/include/odometro.h (tipos y orden).
    _fields_ = [("distancia", ct.c_double), ("muestras", ct.c_ulong),
                ("x_anterior", ct.c_int), ("y_anterior", ct.c_int),
                ("referencia_valida", ct.c_bool)]


@pytest.fixture(scope="session")
def nucleo(tmp_path_factory):
    raiz = Path(__file__).resolve().parents[1]
    biblioteca = tmp_path_factory.mktemp("nucleo") / "libodometro_test.so"
    subprocess.run([
        "gcc", "-std=c11", "-Wall", "-Wextra", "-O0", "-g3", "-fPIC", "-shared",
        "-I", str(raiz / "comun/include"),
        str(raiz / "comun/src/odometro.c"),
        str(raiz / "comun/src/odometro_estado.c"),
        "-lm", "-o", str(biblioteca),
    ], check=True, capture_output=True, text=True)
    lib = ct.CDLL(str(biblioteca))
    for nombre in ("inicializar", "pausar", "reiniciar"):
        funcion = getattr(lib, "odometro_" + nombre)
        funcion.argtypes = [ct.POINTER(Odometro)]
        funcion.restype = None
    lib.odometro_actualizar.argtypes = [ct.POINTER(Odometro), ct.c_int, ct.c_int]
    lib.odometro_actualizar.restype = ct.c_double
    return lib


@pytest.fixture
def estado(nucleo):
    o = Odometro()
    nucleo.odometro_inicializar(ct.byref(o))
    return o


def actualizar(nucleo, estado, x, y):
    return nucleo.odometro_actualizar(ct.byref(estado), x, y)


def test_primera_muestra(nucleo, estado):
    assert actualizar(nucleo, estado, 100, 100) == pytest.approx(0, abs=1e-9, rel=0)
    assert estado.distancia == pytest.approx(0, abs=1e-9, rel=0)
    assert estado.muestras == 1


def test_posicion_repetida(nucleo, estado):
    actualizar(nucleo, estado, 40, 20)
    actualizar(nucleo, estado, 40, 20)
    assert estado.distancia == pytest.approx(0, abs=1e-9, rel=0)
    assert estado.muestras == 2


def test_ida_y_vuelta(nucleo, estado):
    for x, y in [(100, 100), (103, 104), (100, 100)]:
        actualizar(nucleo, estado, x, y)
    assert estado.distancia == pytest.approx(10, abs=1e-9, rel=0)
    assert estado.muestras == 3


def test_reinicio(nucleo, estado):
    actualizar(nucleo, estado, 1, 1)
    actualizar(nucleo, estado, 4, 5)
    nucleo.odometro_reiniciar(ct.byref(estado))
    assert estado.distancia == pytest.approx(0, abs=1e-9, rel=0)
    assert estado.muestras == 0
    assert not estado.referencia_valida
    actualizar(nucleo, estado, 50, 60)
    assert estado.distancia == pytest.approx(0, abs=1e-9, rel=0)


def test_pausa_y_reanudacion(nucleo, estado):
    actualizar(nucleo, estado, 10, 10)
    actualizar(nucleo, estado, 13, 14)
    nucleo.odometro_pausar(ct.byref(estado))
    assert not estado.referencia_valida
    assert actualizar(nucleo, estado, 100, 100) == pytest.approx(0, abs=1e-9, rel=0)
    assert estado.distancia == pytest.approx(5, abs=1e-9, rel=0)
