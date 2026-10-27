from PIL import Image

from transformaciones import (
    a_azul_rojo,
    a_blanco_negro,
    cuantizar_argus,
)


def azul_rojo_asigna_azul_a_lejos_y_rojo_a_cerca_test():
    proximidad = Image.frombytes("L", (2, 1), bytes([0, 255]))

    assert list(a_azul_rojo(proximidad).getdata()) == [(0, 0, 255), (255, 0, 0)]


def blanco_negro_muestra_blanco_cerca_y_negro_lejos_test():
    proximidad = Image.frombytes("L", (2, 1), bytes([0, 255]))

    assert list(a_blanco_negro(proximidad).getdata()) == [0, 255]


def cuantizar_argus_devuelve_seis_filas_de_diez_enteros_test():
    intensidad = Image.new("L", (20, 12), 255)

    matriz = cuantizar_argus(intensidad)

    assert matriz == tuple(tuple(255 for _ in range(10)) for _ in range(6))
